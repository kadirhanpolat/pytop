"""An optional SnapPy bridge for hyperbolic 3-manifolds.

SnapPy supplies what pytop has no route to: hyperbolic volume, census
identification, and symmetry groups of cusped 3-manifolds. It is also an
independent source of ``H_1`` for Dehn surgeries, which pytop computes from the
linking matrix via Smith normal form.

This completes the bridge family: :mod:`~pytop.experimental.gap_bridge` for
groups, :mod:`~pytop.experimental.regina_bridge` for triangulations and normal
surfaces, and this one for hyperbolic geometry. All three share a transport and
a safety posture that a security review settled on the first of them.

The bridge is **entirely optional**. pytop has no runtime dependencies and this
module adds none: it shells out to a locally built Docker image, and
:func:`snappy_available` returns ``False`` rather than raising when that image is
absent. Build it with the Dockerfile recorded in
``tests/core/test_snappy_oracle.py``, tagged ``pytop-snappy``.

Design notes carried over from the sibling bridges, each a defect the family had
to be shaped around:

* **No caller string reaches the container.** Manifold names come from an
  allowlist and surgery coefficients are validated as genuine ints; Python does
  not enforce annotations, so these are real checks.
* **Success is detected by a sentinel, never the exit code.**
* **A client-side timeout does not stop the interpreter inside the container**,
  so the session reaps it.
* A warm container runs a **fresh interpreter per call**.
"""

from __future__ import annotations

import atexit
import os
import re
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from types import TracebackType
from typing import Any

__all__ = [
    "SNAPPY_MANIFOLDS",
    "SnappyManifoldInfo",
    "SnappySession",
    "SnappyTimeout",
    "SnappyUnavailableError",
    "snappy_available",
    "snappy_manifold_info",
    "snappy_surgery_homology",
    "snappy_version",
]

SNAPPY_IMAGE = os.environ.get("PYTOP_SNAPPY_IMAGE", "pytop-snappy")

#: Manifolds this bridge will construct. An allowlist, not free-form text: the
#: value is interpolated into generated Python.
SNAPPY_MANIFOLDS = (
    "4_1",
    "5_2",
    "6_1",
    "m003",
    "m004",
    "m009",
    "m015",
    "figure8",
    "Whitehead",
)

_SENTINEL = "@@PYTOP_SNAPPY_OK@@"
_LABEL = "pytop-snappy=1"
_MAX_COEFF = 10**6

_NAME_RE = re.compile(r"^[A-Za-z0-9_]+$")


class SnappyUnavailableError(RuntimeError):
    """SnapPy could not be reached."""


class SnappyTimeout(RuntimeError):
    """SnapPy did not answer within the budget."""


@dataclass(frozen=True)
class SnappyManifoldInfo:
    """What SnapPy reports about a manifold."""

    name: str
    volume: float | None
    homology: str
    identifications: tuple[str, ...]


# ---------------------------------------------------------------------------
# Validation and code generation
# ---------------------------------------------------------------------------


def _check_manifold(name: object) -> str:
    if name not in SNAPPY_MANIFOLDS:
        raise ValueError(
            f"unknown manifold {name!r}; this bridge constructs only "
            f"{list(SNAPPY_MANIFOLDS)}. The name is interpolated into generated "
            f"Python that runs inside the container, so it comes from a fixed "
            f"allowlist rather than caller text. Pass one of the listed names."
        )
    text = str(name)
    if not _NAME_RE.match(text):
        raise ValueError(f"manifold name {text!r} has unexpected characters")
    return text


def _check_coefficient(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"surgery coefficient {label} must be an int, got "
            f"{type(value).__name__} ({value!r}). It is written into generated "
            f"Python, so a non-integer would be executed as code rather than "
            f"read as a number. Pass integers, e.g. snappy_surgery_homology("
            f"'4_1', 5, 1)."
        )
    if abs(value) > _MAX_COEFF:
        raise ValueError(
            f"surgery coefficient {label} magnitude {abs(value)} exceeds the "
            f"limit {_MAX_COEFF}; SnapPy's filling becomes numerically "
            f"unreliable long before that. Use a smaller coefficient."
        )
    return value


def _script(body: str) -> str:
    return (
        "import snappy\n"
        "try:\n"
        + "".join(f"    {line}\n" for line in body.strip().splitlines())
        + "except Exception as exc:\n"
        "    print('ERROR=' + type(exc).__name__ + ': ' + str(exc))\n"
        f"print('{_SENTINEL}')\n"
    )


def _info_script(name: str) -> str:
    return _script(
        f"M = snappy.Manifold({name!r})\n"
        "try:\n"
        "    print('VOLUME=' + repr(float(M.volume())))\n"
        "except Exception:\n"
        "    print('VOLUME=none')\n"
        "print('HOMOLOGY=' + str(M.homology()))\n"
        "print('IDENT=' + '|'.join(str(x) for x in M.identify()))"
    )


def _surgery_script(name: str, p: int, q: int) -> str:
    return _script(
        f"M = snappy.Manifold({name!r})\n"
        f"M.dehn_fill(({p}, {q}))\n"
        "print('HOMOLOGY=' + str(M.homology()))\n"
        "try:\n"
        "    print('VOLUME=' + repr(float(M.volume())))\n"
        "except Exception:\n"
        "    print('VOLUME=none')"
    )


# ---------------------------------------------------------------------------
# Response handling
# ---------------------------------------------------------------------------


def _require_sentinel(out: str) -> str:
    if _SENTINEL not in out:
        raise ValueError(
            "SnapPy response is missing its sentinel, so the script did not run "
            "to completion. Raw response: " + out.strip()[:200]
        )
    for line in out.splitlines():
        if line.startswith("ERROR="):
            raise ValueError(f"SnapPy raised {line[6:]}")
    return out


def _field(out: str, key: str) -> str:
    for line in out.splitlines():
        if line.startswith(f"{key}="):
            return line[len(key) + 1 :].strip()
    raise ValueError(f"SnapPy response has no {key} field: {out.strip()[:200]}")


def _optional_float(text: str) -> float | None:
    return None if text == "none" else float(text)


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------


def _docker() -> str | None:
    return shutil.which("docker")


def snappy_available() -> bool:
    """Whether a SnapPy round trip is possible. Never raises."""
    docker = _docker()
    if docker is None:
        return False
    try:
        probe = subprocess.run(  # noqa: S603
            [docker, "image", "inspect", SNAPPY_IMAGE],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return probe.returncode == 0


class SnappySession:
    """A warm container running a fresh Python interpreter per call."""

    def __init__(self, *, image: str = SNAPPY_IMAGE, lifetime_s: int = 3600) -> None:
        self._image = image
        self._lifetime = lifetime_s
        self._name = f"pytop-snappy-{uuid.uuid4().hex[:12]}"
        self._started = False

    def __enter__(self) -> SnappySession:
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
        if docker is None or not snappy_available():
            raise SnappyUnavailableError(
                f"the SnapPy bridge needs Docker and the image "
                f"{SNAPPY_IMAGE!r}, and one of them is missing. Build it from "
                f"the Dockerfile recorded in tests/core/test_snappy_oracle.py. "
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

    def _exec(self, args: list[str], *, stdin: str = "", timeout: float = 60.0) -> Any:
        docker = _docker()
        assert docker is not None
        return subprocess.run(  # noqa: S603
            [docker, "exec", "-i", self._name, *args],
            input=stdin, capture_output=True, text=True, timeout=timeout,
        )

    def running_python_processes(self) -> int:
        """How many interpreters are alive in the container."""
        out = self._exec(["ps", "-eo", "comm"], timeout=60).stdout
        return sum(1 for line in out.splitlines() if line.strip().startswith("python"))

    def _reap(self) -> None:
        try:
            self._exec(["pkill", "-9", "-f", "python"], timeout=60)
        except (OSError, subprocess.SubprocessError):
            pass

    def evaluate(self, script: str, *, timeout: float = 180.0) -> str:
        """Run one generated script inside the container and return its stdout."""
        if not self._started:
            raise SnappyUnavailableError(
                "this SnappySession is not running. Use it as a context manager "
                "(`with SnappySession() as s:`) or call start() first."
            )
        try:
            done = self._exec(["python", "-"], stdin=script, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            self._reap()
            raise SnappyTimeout(
                f"SnapPy did not answer within {timeout}s and was terminated. "
                f"Volume computation on a difficult triangulation can take "
                f"arbitrarily long. Raise the timeout, or use a simpler manifold."
            ) from exc
        return _require_sentinel(done.stdout)


# ---------------------------------------------------------------------------
# Public queries
# ---------------------------------------------------------------------------


def _run(script: str, session: SnappySession | None, timeout: float) -> str:
    if session is not None:
        return session.evaluate(script, timeout=timeout)
    with SnappySession() as owned:
        return owned.evaluate(script, timeout=timeout)


def snappy_version(*, session: SnappySession | None = None) -> str:
    """The SnapPy version inside the image."""
    script = _script("print('VERSION=' + str(snappy.version()))")
    return _field(_run(script, session, 60.0), "VERSION")


def snappy_manifold_info(
    name: str, *, session: SnappySession | None = None, timeout: float = 180.0
) -> SnappyManifoldInfo:
    """Volume, ``H_1`` and census identifications for a manifold.

    Hyperbolic volume has no counterpart in pytop and is not planned to: it needs
    a geometric structure, where pytop is combinatorial throughout.
    """
    checked = _check_manifold(name)
    out = _run(_info_script(checked), session, timeout)
    idents = _field(out, "IDENT")
    return SnappyManifoldInfo(
        name=checked,
        volume=_optional_float(_field(out, "VOLUME")),
        homology=_field(out, "HOMOLOGY"),
        identifications=tuple(x for x in idents.split("|") if x),
    )


def snappy_surgery_homology(
    name: str,
    p: int,
    q: int,
    *,
    session: SnappySession | None = None,
    timeout: float = 180.0,
) -> str:
    """``H_1`` of the ``(p, q)`` Dehn filling, as SnapPy reports it.

    An independent check on :func:`pytop.first_homology_of_surgery`, which
    derives the same group from the linking matrix via Smith normal form rather
    than by filling a triangulation. Note the two use different conventions at
    the extremes -- pytop rejects ``q = 0`` as an invalid fraction where SnapPy
    reads ``(1, 0)`` as a meridian filling -- so compare them only on
    coefficients valid for both.
    """
    checked = _check_manifold(name)
    _check_coefficient(p, "p")
    _check_coefficient(q, "q")
    out = _run(_surgery_script(checked, p, q), session, timeout)
    return _field(out, "HOMOLOGY")
