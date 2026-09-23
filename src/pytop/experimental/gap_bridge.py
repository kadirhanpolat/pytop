"""An optional GAP bridge for group presentations.

pytop's :mod:`~pytop.van_kampen` produces :class:`~pytop.van_kampen.GroupPresentation`
objects and names them with a small hand-rolled classifier; anything outside its
fixed list falls through unnamed. GAP answers the general question -- order,
abelian invariants, structure description, SmallGroups id -- and doubles as an
independent oracle for pytop's own SNF-based abelianization.

The bridge is **entirely optional**. pytop has no runtime dependencies and this
module adds none: it shells out to a Docker image, and :func:`gap_available`
returns ``False`` rather than raising when that image is not present.

Design notes, each of which is a defect this module had to be shaped around and
which a change should not casually undo:

* **Generator names never reach GAP.** They are user-controlled strings with no
  character restrictions, so generators are emitted positionally (``FreeGroup(n)``
  and ``f.1``, ``f.2``, ...) and the name-to-index map stays in Python.
* **Exponents are validated, not assumed.** ``GroupPresentation`` does not check
  them and Python does not enforce the ``int`` annotation, so a string exponent
  would otherwise reach the generated source and execute.
* **Newlines are emitted with ``Chr(10)``.** A newline inside a GAP string
  literal is a syntax error, after which GAP's parser recovery swallows the rest
  of the input and the call returns *empty stdout with exit code 0*.
* **``SizeScreen`` is set.** GAP otherwise wraps stdout at 80 columns and splits
  long invariant lists across lines.
* **``IdGroup`` is guarded by order.** The SmallGroups library does not cover
  every order; an unguarded call drops GAP into its break loop, which writes a
  prompt and ANSI escapes into stdout, still exits 0, and reads stdin.
* **Success is detected by a sentinel, never by the exit code.** GAP exits 0 on
  syntax errors, runtime errors and break loops alike.
* **A client-side timeout does not stop GAP.** Killing the ``docker exec`` client
  leaves the GAP process inside the container spinning at 100% CPU, so the
  session reaps it explicitly.
"""

from __future__ import annotations

import atexit
import os
import re
import shutil
import subprocess
import uuid
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import TracebackType

from pytop.van_kampen import GroupPresentation

__all__ = [
    "GapGroupInfo",
    "GapSession",
    "GapTimeout",
    "GapUnavailableError",
    "gap_abelian_invariants",
    "gap_available",
    "gap_group_info",
]

#: Image carrying GAP. Overridable for a site-local mirror.
GAP_IMAGE = os.environ.get("PYTOP_GAP_IMAGE", "sagemath/sagemath:latest")

#: Paths tried in order; each is *run*, not merely looked up.
_GAP_CANDIDATES = (
    "/home/sage/sage/local/bin/gap",
    "/usr/bin/gap",
    "/usr/local/bin/gap",
    "gap",
)

_SENTINEL = "@@PYTOP_GAP_OK@@"
_EXPONENT_LIMIT = 10**6
_LABEL = "pytop-gap=1"

#: Orders the SmallGroups library does not cover.
_SMALLGROUPS_GAPS = (512, 1024)
#: Above this, IdGroup is not attempted even when the order is covered.
_SMALLGROUPS_MAX = 2000


class GapUnavailableError(RuntimeError):
    """GAP could not be reached."""


class GapTimeout(RuntimeError):
    """GAP did not answer within the budget.

    Not necessarily a defect: the word problem for finitely presented groups is
    undecidable, so ``Size`` may legitimately never terminate.
    """


@dataclass(frozen=True)
class GapGroupInfo:
    """What GAP could determine about a presentation.

    ``abelian_invariants`` is ``None`` when nothing was determined and ``()`` for
    the trivial group -- GAP returns an empty list there, so ``()`` is a real
    value and cannot double as "not determined".
    """

    abelian_invariants: tuple[int, ...] | None
    is_finite: bool | None
    order: int | None
    structure_description: str | None
    small_group_id: tuple[int, int] | None

    @property
    def determined(self) -> bool:
        """True when GAP returned an answer at all."""
        return self.abelian_invariants is not None


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------


def _check_exponent(exponent: object, generator: object) -> int:
    if isinstance(exponent, bool) or not isinstance(exponent, int):
        raise ValueError(
            f"relator exponent for generator {generator!r} is "
            f"{type(exponent).__name__}, not int (got {exponent!r}). Exponents "
            f"are written directly into generated GAP source, so a non-integer "
            f"would be executed as code rather than read as a number. Build "
            f"relators with integer exponents, e.g. (('a', 2), ('b', -1))."
        )
    if abs(exponent) > _EXPONENT_LIMIT:
        raise ValueError(
            f"relator exponent {exponent} exceeds the magnitude limit "
            f"{_EXPONENT_LIMIT}. Exponents this large make GAP's own word "
            f"operations intractable long before the bridge is the bottleneck. "
            f"Reduce the relator, or raise the limit deliberately."
        )
    return exponent


def _relator_to_gap(
    relator: Iterable[tuple[str, object]], index_of: Mapping[str, int]
) -> str:
    """Render one relator word as positional GAP source.

    The exponent is typed ``object`` deliberately: ``GroupPresentation`` annotates
    it ``int`` but does not check it, and Python does not enforce annotations, so
    treating it as an ``int`` here is exactly the assumption that made this a
    code-execution path.
    """
    parts = []
    for generator, exponent in relator:
        if generator not in index_of:
            raise ValueError(
                f"relator references unknown generator {generator!r}; the "
                f"presentation declares {sorted(index_of)}. Every generator in a "
                f"relator must appear in the presentation's generator tuple."
            )
        power = _check_exponent(exponent, generator)
        parts.append(f"f.{index_of[generator]}^{power}")
    return "*".join(parts)


def _generate_query(presentation: GroupPresentation) -> str:
    """Build the GAP script for one presentation.

    No generator name appears in the result: generators are positional and the
    name-to-index map stays here.
    """
    index_of = {name: i + 1 for i, name in enumerate(presentation.generators)}
    relators = ",".join(
        _relator_to_gap(rel, index_of) for rel in presentation.relators
    )
    nl = "Print(Chr(10));"
    skip = " and ".join(f"s<>{order}" for order in _SMALLGROUPS_GAPS)
    return (
        "SizeScreen([256,40]);;\n"
        f"f:=FreeGroup({len(presentation.generators)});;\n"
        f"g:=f/[{relators}];;\n"
        "s:=Size(g);;\n"
        'Print("SIZE=",s,"|");\n'
        'Print("ABI=",AbelianInvariants(g),"|");\n'
        f"if s<>infinity and s<={_SMALLGROUPS_MAX} and {skip} then\n"
        '  Print("ID=",IdGroup(g),"|");\n'
        "else\n"
        '  Print("ID=NONE|");\n'
        "fi;\n"
        f'Print("{_SENTINEL}");{nl}\n'
    )


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

_INT_RE = re.compile(r"-?\d+")


def _parse_int_list(text: str) -> tuple[int, ...]:
    return tuple(int(m.group()) for m in _INT_RE.finditer(text))


def _parse_response(body: str) -> GapGroupInfo:
    """Parse one GAP response, requiring the sentinel.

    The exit code is useless here -- GAP returns 0 on syntax errors, runtime
    errors and break loops alike -- so a missing sentinel is the only reliable
    failure signal.
    """
    if _SENTINEL not in body:
        raise ValueError(
            "GAP response is missing its sentinel, so the script did not run to "
            "completion; GAP exits 0 even on a break loop, so the status code "
            "cannot be trusted. Raw response: " + body.strip()[:200]
        )
    # Defence in depth: SizeScreen should prevent wrapping, but a continuation
    # would otherwise split a list across lines.
    flat = body.replace("\\\n", "").replace("\n", " ")
    fields = {}
    for chunk in flat.split("|"):
        if "=" in chunk:
            key, _, value = chunk.partition("=")
            fields[key.strip()] = value.strip()

    size = fields.get("SIZE", "")
    if size == "infinity":
        is_finite: bool | None = False
        order: int | None = None
    elif size.lstrip("-").isdigit():
        is_finite, order = True, int(size)
    else:
        is_finite, order = None, None

    abi = fields.get("ABI")
    invariants = _parse_int_list(abi) if abi is not None else None

    raw_id = fields.get("ID", "NONE")
    ids = _parse_int_list(raw_id) if raw_id != "NONE" else ()
    small_group_id = (ids[0], ids[1]) if len(ids) == 2 else None

    return GapGroupInfo(
        abelian_invariants=invariants,
        is_finite=is_finite,
        order=order,
        structure_description=fields.get("SD") or None,
        small_group_id=small_group_id,
    )


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------


def _docker() -> str | None:
    return shutil.which("docker")


def gap_available() -> bool:
    """Whether a GAP round trip is possible. Never raises."""
    docker = _docker()
    if docker is None:
        return False
    try:
        probe = subprocess.run(  # noqa: S603
            [docker, "image", "inspect", GAP_IMAGE],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return probe.returncode == 0


class GapSession:
    """A warm container in which each evaluation runs a fresh GAP process.

    A single long-lived GAP process would be far faster per call but has a
    demonstrated hang mode, so isolation is preferred over latency here.

    Use as a context manager; the container is removed on exit. It is also
    started with a finite sleep and a label so that an abandoned container
    self-reaps and stale ones can be swept.
    """

    def __init__(self, *, image: str = GAP_IMAGE, lifetime_s: int = 3600) -> None:
        self._image = image
        self._lifetime = lifetime_s
        self._name = f"pytop-gap-{uuid.uuid4().hex[:12]}"
        self._gap: str | None = None
        self._started = False

    # -- lifecycle ---------------------------------------------------------

    def __enter__(self) -> GapSession:
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
        if docker is None or not gap_available():
            raise GapUnavailableError(
                f"the GAP bridge needs Docker and the image {GAP_IMAGE!r}, and "
                f"one of them is missing, so no GAP call can be made. Install "
                f"Docker and run `docker pull {GAP_IMAGE}`, or set "
                f"PYTOP_GAP_IMAGE to a local mirror. pytop itself never needs "
                f"this: the bridge is optional."
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
        self._gap = self._resolve_gap()

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

    # -- internals ---------------------------------------------------------

    def _exec(self, args: list[str], *, stdin: str = "", timeout: float = 60.0):
        docker = _docker()
        assert docker is not None
        return subprocess.run(  # noqa: S603
            [docker, "exec", "-i", self._name, *args],
            input=stdin, capture_output=True, text=True, timeout=timeout,
        )

    def _resolve_gap(self) -> str:
        """Find the GAP binary by running candidates.

        ``command -v gap`` is not usable: ``docker exec`` does not inherit the
        image's entrypoint environment, and on the Sage image it prints nothing
        and exits 1 even though the binary is present.
        """
        for candidate in _GAP_CANDIDATES:
            try:
                probe = self._exec(
                    [candidate, "-q", "-b"], stdin="Print(1);", timeout=120
                )
            except (OSError, subprocess.SubprocessError):
                continue
            if probe.returncode == 0 and probe.stdout.strip() == "1":
                return candidate
        raise GapUnavailableError(
            f"no working GAP binary found in {self._image!r}; tried "
            f"{list(_GAP_CANDIDATES)}. Each candidate is run rather than looked "
            f"up, because `command -v gap` fails on this image even where GAP "
            f"exists. Set PYTOP_GAP_IMAGE to an image that ships GAP."
        )

    def running_gap_processes(self) -> int:
        """How many GAP processes are alive in the container."""
        out = self._exec(["ps", "-eo", "comm"], timeout=60).stdout
        return sum(1 for line in out.splitlines() if line.strip() == "gap")

    def _reap(self) -> None:
        """Kill GAP inside the container.

        Necessary because a client-side timeout kills only the ``docker exec``
        client; the GAP process keeps running, and on the undecidable inputs
        that make timeouts necessary it spins at 100% CPU until the container
        dies.
        """
        try:
            self._exec(["pkill", "-9", "-x", "gap"], timeout=60)
        except (OSError, subprocess.SubprocessError):
            pass

    # -- evaluation --------------------------------------------------------

    def evaluate(self, code: str, *, timeout: float = 60.0) -> str:
        """Run one GAP script and return its stdout."""
        if not self._started:
            raise GapUnavailableError(
                "this GapSession is not running, so it cannot evaluate anything. "
                "Use it as a context manager (`with GapSession() as s:`) or call "
                "start() first."
            )
        assert self._gap is not None
        try:
            done = self._exec([self._gap, "-q", "-b"], stdin=code, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            self._reap()
            raise GapTimeout(
                f"GAP did not answer within {timeout}s and was terminated. This "
                f"is not always a defect: the word problem for finitely "
                f"presented groups is undecidable, so Size() may never "
                f"terminate. Raise the timeout, or simplify the presentation."
            ) from exc
        return done.stdout


# ---------------------------------------------------------------------------
# Public queries
# ---------------------------------------------------------------------------


_UNDETERMINED = GapGroupInfo(
    abelian_invariants=None,
    is_finite=None,
    order=None,
    structure_description=None,
    small_group_id=None,
)


def gap_group_info(
    presentation: GroupPresentation,
    *,
    session: GapSession | None = None,
    timeout: float = 60.0,
) -> GapGroupInfo:
    """Ask GAP what it can determine about ``presentation``.

    A timeout yields an undetermined result rather than an exception, since an
    unanswerable presentation is an ordinary outcome here. Passing ``session``
    reuses a warm container; without one a container is started and removed for
    this single call, which is markedly slower.
    """
    code = _generate_query(presentation)  # validates before touching Docker
    if session is not None:
        try:
            return _parse_response(session.evaluate(code, timeout=timeout))
        except GapTimeout:
            return _UNDETERMINED
    with GapSession() as owned:
        try:
            return _parse_response(owned.evaluate(code, timeout=timeout))
        except GapTimeout:
            return _UNDETERMINED


def gap_abelian_invariants(
    presentation: GroupPresentation,
    *,
    session: GapSession | None = None,
    timeout: float = 60.0,
) -> tuple[int, ...]:
    """GAP's abelian invariants for ``presentation``.

    Raises :class:`GapTimeout` rather than returning ``()`` on a timeout: ``()``
    is the honest answer for the trivial group and must not be overloaded.
    """
    info = gap_group_info(presentation, session=session, timeout=timeout)
    if info.abelian_invariants is None:
        raise GapTimeout(
            f"GAP did not determine the abelian invariants within {timeout}s, "
            f"and an empty tuple would be indistinguishable from the trivial "
            f"group's genuine answer. Raise the timeout, or call "
            f"gap_group_info() which reports the undetermined state explicitly."
        )
    return info.abelian_invariants
