"""An optional Regina bridge for 3-manifold triangulations.

Regina computes things pure-Python pytop cannot: normal surfaces, census
recognition, and homology of triangulations built from its own example library.
It is also an independent source of ``H_1`` for lens spaces, which pytop computes
from the linking matrix via Smith normal form.

The bridge is **entirely optional**. pytop has no runtime dependencies and this
module adds none: it shells out to a locally built Docker image, and
:func:`regina_available` returns ``False`` rather than raising when that image is
absent.

**The image must be built, not pulled.** Regina publishes no official image and
is not on PyPI; it is packaged for Debian by its own author. Build it with::

    docker build -t pytop-regina -f docker/Dockerfile.regina .

Design notes, mirroring :mod:`pytop.experimental.gap_bridge` (whose shape was
settled by a security review, and the same hazards apply here):

* **No caller string ever reaches the container.** Inputs are integers and names
  drawn from a fixed allowlist; both are validated here, not assumed.
* **Success is detected by a sentinel, never by the exit code**, so a traceback
  cannot be mistaken for a result.
* **A client-side timeout does not stop the interpreter inside the container**,
  so the session reaps it explicitly.
* A warm container runs a **fresh interpreter per call**: isolation over latency.
"""

from __future__ import annotations

import atexit
import os
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from types import TracebackType

__all__ = [
    "REGINA_EXAMPLES",
    "ReginaHomology",
    "ReginaSession",
    "ReginaTimeout",
    "ReginaUnavailableError",
    "regina_available",
    "regina_example_homology",
    "regina_lens_homology",
    "regina_normal_surface_count",
    "regina_version",
]

REGINA_IMAGE = os.environ.get("PYTOP_REGINA_IMAGE", "pytop-regina")

#: Example triangulations this bridge will construct, by Regina's own names.
#: An allowlist rather than a free-form string: the value is interpolated into
#: generated Python, so it must not be caller-controlled text.
REGINA_EXAMPLES = (
    "poincare",
    "rp3rp3",
    "s2xs1",
    "figureEight",
    "gieseking",
    "rp2xs1",
    "ball",
    "lens",
)

_SENTINEL = "@@PYTOP_REGINA_OK@@"
_LABEL = "pytop-regina=1"
_MAX_PARAM = 10**6


class ReginaUnavailableError(RuntimeError):
    """Regina could not be reached."""


class ReginaTimeout(RuntimeError):
    """Regina did not answer within the budget."""


@dataclass(frozen=True)
class ReginaHomology:
    """``H_1`` of a triangulation.

    ``free_rank`` and ``torsion`` come from Regina's structured accessors
    (``rank()``, ``countInvariantFactors()``, ``invariantFactor()``), not from
    parsing its display string -- ``2 Z_2`` means two factors of order 2, and a
    regex over that notation is a needless way to get it wrong. ``raw`` is kept
    only for messages.
    """

    raw: str
    free_rank: int
    torsion: tuple[int, ...]


# ---------------------------------------------------------------------------
# Validation and code generation
# ---------------------------------------------------------------------------


def _check_int(value: object, name: str) -> int:
    """Reject anything that is not a genuine ``int``.

    ``bool`` is excluded deliberately: ``True`` would render as ``1``. Python does
    not enforce annotations, so this is a real check rather than a restatement of
    the signature.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{name} must be an int, got {type(value).__name__} ({value!r}). "
            f"This value is written into generated Python that runs inside the "
            f"Regina container, so a non-integer would be executed as code "
            f"rather than read as a number. Pass an integer, e.g. "
            f"regina_lens_homology(5, 1)."
        )
    if abs(value) > _MAX_PARAM:
        raise ValueError(
            f"{name} magnitude {abs(value)} exceeds the limit {_MAX_PARAM}. "
            f"Triangulations of that size are not constructible in reasonable "
            f"time, so the call would hang rather than answer. Use a smaller "
            f"parameter."
        )
    return value


def _check_example(name: object) -> str:
    if name not in REGINA_EXAMPLES:
        raise ValueError(
            f"unknown example {name!r}; this bridge constructs only "
            f"{list(REGINA_EXAMPLES)}. The name is interpolated into generated "
            f"Python, so it is taken from a fixed allowlist rather than from "
            f"caller text. Pass one of the listed names."
        )
    return str(name)


def _script(body: str) -> str:
    """Wrap a generated body so failures are visible and success is provable."""
    return (
        "import regina\n"
        "try:\n"
        + "".join(f"    {line}\n" for line in body.strip().splitlines())
        + "except Exception as exc:\n"
        "    print('ERROR=' + type(exc).__name__ + ': ' + str(exc))\n"
        f"print('{_SENTINEL}')\n"
    )


_HOMOLOGY_BODY = (
    "h = t.homology()\n"
    "print('RAW=' + h.str())\n"
    "print('RANK=' + str(h.rank()))\n"
    "print('INV=' + ','.join("
    "str(h.invariantFactor(i)) for i in range(h.countInvariantFactors())))"
)


def _lens_script(p: int, q: int) -> str:
    return _script(f"t = regina.Example3.lens({p}, {q})\n" + _HOMOLOGY_BODY)


def _example_script(name: str) -> str:
    return _script(f"t = regina.Example3.{name}()\n" + _HOMOLOGY_BODY)


def _normal_surface_script(name: str) -> str:
    return _script(
        f"t = regina.Example3.{name}()\n"
        "s = regina.NormalSurfaces(t, regina.NormalCoords.NS_STANDARD)\n"
        "print('TETRAHEDRA=' + str(t.size()))\n"
        "print('SURFACES=' + str(s.size()))"
    )


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _require_sentinel(out: str) -> str:
    if _SENTINEL not in out:
        raise ValueError(
            "Regina response is missing its sentinel, so the script did not run "
            "to completion. Raw response: " + out.strip()[:200]
        )
    for line in out.splitlines():
        if line.startswith("ERROR="):
            raise ValueError(f"Regina raised {line[6:]}")
    return out


def _field(out: str, key: str) -> str:
    for line in out.splitlines():
        if line.startswith(f"{key}="):
            return line[len(key) + 1 :].strip()
    raise ValueError(f"Regina response has no {key} field: {out.strip()[:200]}")


def _read_homology(out: str) -> ReginaHomology:
    """Build a :class:`ReginaHomology` from the structured fields."""
    inv = _field(out, "INV")
    return ReginaHomology(
        raw=_field(out, "RAW"),
        free_rank=int(_field(out, "RANK")),
        torsion=tuple(int(x) for x in inv.split(",") if x.strip()),
    )


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------


def _docker() -> str | None:
    return shutil.which("docker")


def regina_available() -> bool:
    """Whether a Regina round trip is possible. Never raises."""
    docker = _docker()
    if docker is None:
        return False
    try:
        probe = subprocess.run(  # noqa: S603
            [docker, "image", "inspect", REGINA_IMAGE],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return probe.returncode == 0


class ReginaSession:
    """A warm container running a fresh Python interpreter per call."""

    def __init__(self, *, image: str = REGINA_IMAGE, lifetime_s: int = 3600) -> None:
        self._image = image
        self._lifetime = lifetime_s
        self._name = f"pytop-regina-{uuid.uuid4().hex[:12]}"
        self._started = False

    def __enter__(self) -> ReginaSession:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def start(self) -> None:
        docker = _docker()
        if docker is None or not regina_available():
            raise ReginaUnavailableError(
                f"the Regina bridge needs Docker and the image {REGINA_IMAGE!r}, "
                f"and one of them is missing. Regina publishes no official image "
                f"and is not on PyPI, so the image must be built rather than "
                f"pulled: `docker build -t pytop-regina -f docker/Dockerfile.regina .` "
                f"pytop itself never needs this; the bridge is optional."
            )
        subprocess.run(  # noqa: S603
            [
                docker, "run", "-d", "--rm",
                "--name", self._name,
                "--pids-limit", "256",
                "--label", _LABEL,
                self._image, "sleep", str(self._lifetime),
            ],
            capture_output=True, text=True, timeout=300, check=True,
        )
        self._started = True
        atexit.register(self.close)

    def close(self) -> None:
        if not self._started:
            return
        self._started = False
        docker = _docker()
        if docker is not None:
            subprocess.run(  # noqa: S603
                [docker, "rm", "-f", self._name],
                capture_output=True, text=True, timeout=120,
            )

    def _exec(self, args: list[str], *, stdin: str = "", timeout: float = 60.0):
        docker = _docker()
        assert docker is not None
        return subprocess.run(  # noqa: S603
            [docker, "exec", "-i", self._name, *args],
            input=stdin, capture_output=True, text=True, timeout=timeout,
        )

    def running_python_processes(self) -> int:
        """How many interpreters are alive in the container."""
        out = self._exec(["ps", "-eo", "comm"], timeout=60).stdout
        return sum(1 for line in out.splitlines() if line.strip() == "python3")

    def _reap(self) -> None:
        """Kill the interpreter inside the container.

        A client-side timeout kills only the ``docker exec`` client; without this
        the interpreter keeps running on exactly the inputs slow enough to need a
        timeout.
        """
        try:
            self._exec(["pkill", "-9", "-x", "python3"], timeout=60)
        except (OSError, subprocess.SubprocessError):
            pass

    def evaluate(self, script: str, *, timeout: float = 120.0) -> str:
        """Run one generated script inside the container and return its stdout."""
        if not self._started:
            raise ReginaUnavailableError(
                "this ReginaSession is not running. Use it as a context manager "
                "(`with ReginaSession() as s:`) or call start() first."
            )
        try:
            done = self._exec(["python3", "-"], stdin=script, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            self._reap()
            raise ReginaTimeout(
                f"Regina did not answer within {timeout}s and was terminated. "
                f"Normal-surface enumeration is exponential in the number of "
                f"tetrahedra, so a larger triangulation may simply not finish. "
                f"Raise the timeout, or use a smaller example."
            ) from exc
        return _require_sentinel(done.stdout)


# ---------------------------------------------------------------------------
# Public queries
# ---------------------------------------------------------------------------


def _run(script: str, session: ReginaSession | None, timeout: float) -> str:
    if session is not None:
        return session.evaluate(script, timeout=timeout)
    with ReginaSession() as owned:
        return owned.evaluate(script, timeout=timeout)


def regina_version(*, session: ReginaSession | None = None) -> str:
    """The Regina version inside the image."""
    script = _script("print('VERSION=' + regina.versionString())")
    return _field(_run(script, session, 60.0), "VERSION")


def regina_lens_homology(
    p: int, q: int, *, session: ReginaSession | None = None, timeout: float = 120.0
) -> ReginaHomology:
    """``H_1(L(p, q))`` as computed by Regina.

    An independent check on pytop's :func:`~pytop.lens_space_first_homology`,
    which derives the same group from the linking matrix via Smith normal form.
    """
    _check_int(p, "p")
    _check_int(q, "q")
    return _read_homology(_run(_lens_script(p, q), session, timeout))


def regina_example_homology(
    name: str, *, session: ReginaSession | None = None, timeout: float = 120.0
) -> ReginaHomology:
    """``H_1`` of one of Regina's example triangulations."""
    return _read_homology(_run(_example_script(_check_example(name)), session, timeout))


def regina_normal_surface_count(
    name: str, *, session: ReginaSession | None = None, timeout: float = 300.0
) -> tuple[int, int]:
    """``(tetrahedra, vertex normal surfaces)`` in standard coordinates.

    Normal-surface enumeration is the capability pytop does not have and does not
    intend to grow: it is exponential in the tetrahedron count and is exactly the
    kind of work the roadmap defers to Regina rather than reimplementing.
    """
    out = _run(_normal_surface_script(_check_example(name)), session, timeout)
    return int(_field(out, "TETRAHEDRA")), int(_field(out, "SURFACES"))
