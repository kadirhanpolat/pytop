# P12.4 — GAP Bridge (and the Regina finding)

**Status:** DRAFT — revision 2 (post security/correctness review)
**Date:** 2026-09-23
**Milestone:** Phase 12, P12.4 ("Native GAP / Regina integration — currently only Docker oracles; in-process FFI or persistent subprocess bridge")
**Target version:** v1.8.0 (alongside P12.5)
**Layer:** `src/pytop/experimental/`

> **Revision 2.** Revision 1 drew three Criticals from a security/correctness
> review, all reproduced live. The worst: §4's claim that code generation was
> "injection-proof by construction" was **false** — `GroupPresentation` does not
> validate relator exponents, Python does not enforce the `int` annotation, and a
> string exponent reached the generated source, executed a shell command inside
> the container, and returned a plausible answer to the caller. Revision 2
> replaces assumption with an explicit check.
>
> Every quantitative claim below was measured. Claims that failed re-measurement
> are marked as such rather than quietly corrected.

---

## 1. What this milestone can and cannot deliver

**GAP: deliverable now.** GAP 4.15.1 ships inside the `sagemath/sagemath:latest`
image already present on this machine. Verified directly:

```
$ docker run -i --rm sagemath/sagemath:latest gap -q -b
GAP VERSION: 4.15.1
T2 abelian inv:    [ 0, 0 ]
Klein abelian inv: [ 0, 2 ]
Q8: size 8, IdGroup [ 8, 4 ], StructureDescription "Q8"
```

No new image is required.

**Regina: blocked, and this is reported rather than quietly dropped.** Probed and
found absent:

| Probe | Result |
|---|---|
| `docker manifest inspect regina/regina:latest` | not found |
| `docker manifest inspect regina-normal/regina:latest` | not found |
| `docker manifest inspect benburton/regina:latest` | not found |
| `import regina` inside the Sage image | `ModuleNotFoundError` |
| `pip index versions regina` / `regina-normal` | no distributions |

Regina would need a purpose-built image (`apt-get install regina-normal`,
mirroring the existing `pytop-snappy` pattern). That is a separate deliverable
with its own build, cache and CI story, and the roadmap already lists
Regina-scale normal surfaces as out of scope for pure-Python pytop (Phase 3,
P3.3). **This spec therefore delivers the GAP half and proposes the Regina image
as its own milestone (P12.6), with the evidence above recorded so the question
is not re-opened from scratch.**

---

## 2. Why a GAP bridge is worth having

pytop's `van_kampen` produces `GroupPresentation` objects and classifies them
with `_identify_group` — a hand-rolled classifier covering a fixed list
(`"trivial"`, `"infinite_cyclic"`, `"free_rank_n"`, `"free_abelian_rank_2"`,
`"klein_bottle_group"`, `"cyclic_2"`, surface groups). Anything else falls
through unnamed.

GAP answers the general question. On a presentation pytop cannot name, GAP
supplies the order, the abelian invariants, a structure description and the
SmallGroups id. Measured:

| Presentation | pytop today | GAP |
|---|---|---|
| ⟨a,b \| [a,b]⟩ (T²) | `free_abelian_rank_2` | `Size = infinity`, `AbelianInvariants = [0,0]`, `StructureDescription = "Z x Z"` |
| ⟨a,b \| abab⁻¹⟩ (Klein) | `klein_bottle_group` | `AbelianInvariants = [0,2]` |
| ⟨a,b \| a²b⁻², a²(ab)⁻²⟩ | unnamed | `Size = 8`, `"Q8"`, `IdGroup = [8,4]` |
| ⟨a,b \| a², b³, (ab)²⟩ | unnamed | `Size = 6`, `"S3"`, `IdGroup = [6,1]` |

It is also a **differential oracle** for pytop's own SNF-based `abelianization`
— the Phase 4 value the project already holds for planarity (networkx),
persistence (GUDHI) and knots (Sage).

---

## 3. Transport

### 3.1 The design: warm container, fresh GAP per call

```python
class GapSession:
    """A warm container; each evaluation runs a fresh GAP process inside it."""
    def __enter__(self) -> GapSession: ...
    def evaluate(self, code: str, *, timeout: float = 60.0) -> str: ...
    def __exit__(self, *exc) -> None: ...   # removes the container
```

Start once: `docker run -d --rm --name pytop-gap-<uuid> --pids-limit 256
--label pytop-gap=1 <image> sleep 3600`.

`--rm` fires when a container *stops*, and `sleep infinity` never does — so on a
crash, a `SIGKILL`, or an aborted test run, `__exit__` never runs and a full Sage
container leaks indefinitely (verified: an abandoned container sits at `Up`
forever). Hence a **finite** sleep so an abandoned container self-reaps, a label
so stale ones can be swept at session start, and an `atexit` hook.
Per call: `docker exec -i <name> <gap_path> -q -b` with the generated code on
stdin. Close: `docker rm -f <name>`.

The gap binary is **located by probing and running**, not assumed and not looked
up: `docker exec` does not inherit the image's entrypoint environment, so a bare
`gap` fails with `OCI runtime exec failed: executable file not found`, and
`bash -lc 'command -v gap'` prints nothing and exits 1 on this image. The session
tries each candidate path with a trivial program (`Print(1);`) and keeps the
first that returns `1`; `/home/sage/sage/local/bin/gap` wins on the current
image. See §5 for why the `command -v` route was wrong.

### 3.2 Measured cost

Best of 3–4 runs, same query (`AbelianInvariants` of the torus presentation):

| Run | cold (`docker run --rm`) | warm (`docker exec`) | ratio |
|---|---|---|---|
| first measurement | 1.34 s | 0.78 s | 1.7× |
| independent re-measurement | 2.11 s | 0.75 s | 2.8× |
| third measurement | 1.44 s | 0.93 s | 1.55× |

**The warm figure is stable (0.75–0.93 s); the cold figure is not (1.34–2.11 s),
so the ratio is not a reportable number.** What holds: warm avoids per-call image
setup and is consistently faster, and the residue in both is GAP's own startup
rather than Docker. No speedup ratio is quoted in the module documentation.

### 3.3 Two rejected alternatives, with their failure modes

**A single persistent GAP process** (stdin/stdout REPL with a sentinel) would cut
per-call cost to milliseconds — measured 0.758 s for the first call and
**0.001–0.003 s** thereafter. It was built and rejected: the session has a
demonstrated hang mode. With `BreakOnError := false` set, a `StructureDescription`
/ `IdGroup` call that lazily loads the SmallGroups library never returned, and
the reader blocked until its timeout — on a query (Q8) that completes in under a
second as a one-shot. Error recovery also swallows the sentinel: GAP's parser
recovery consumes input up to the next `;`, so a failed command can eat the
very line that would have terminated the read.

**Wrapping each command in `CALL_WITH_CATCH(function() … end, [])`** to guarantee
the sentinel does not work either: inside a GAP `function`, assigning to an
undeclared variable is a parse error, so ordinary generated code (`f := …;;`)
fails before it runs. Verified: every case timed out.

A 0.78 s → 0.003 s gain does not justify shipping a demonstrated hang in an
opt-in oracle bridge. The roadmap asks for a "persistent subprocess bridge"; the
expensive resource — the container — is what persists here.

### 3.4 Failure handling

- `gap_available()` returns `False` (never raises) when Docker is missing, the
  daemon is down, or the image is absent.
- Every `evaluate` carries a timeout. **This is not defensive padding: the word
  problem for finitely presented groups is undecidable, so `Size(g)` may not
  terminate on a perfectly ordinary input.**
- **A client-side timeout does not stop GAP.** `subprocess.run(timeout=...)`
  kills the `docker exec` client; the GAP process inside the container keeps
  running. Measured: four successive timed-out calls left four orphans, each
  pegged at 100% CPU until the container died. On timeout the session therefore
  runs `docker exec <name> pkill -9 -x gap` — verified to take the count from 1
  to 0 — and the container is capped with `--pids-limit`.
- **Success is detected by a sentinel token, never by the exit code.** GAP exits
  0 on syntax errors, runtime errors and break loops alike. Every generated
  script ends with a sentinel; a missing sentinel is a failure regardless of
  status.
- `GapUnavailableError` carries a WHY-HOW-THEN message naming the image and the
  opt-in environment variable.

---

## 4. Code generation is injection-safe by explicit validation

`GroupPresentation.__post_init__` validates that generator names are non-empty
and distinct and that every relator references a known generator — but **not**
the exponents. Python does not enforce the `int` annotation, so a relator entry
carrying GAP source as its exponent constructs without complaint. Revision 1
asserted exponents "cannot carry text"; **that was wrong, and was demonstrated
to give arbitrary code execution inside the container while returning a
well-formed wrong answer to the caller.** `GroupPresentation` is public API, so
the path is reachable from the documented surface.

Two independent measures, neither sufficient alone:

1. **Names never reach GAP.** Generators are emitted **positionally**:

```
f := FreeGroup(3);;              # n = len(presentation.generators)
g := f / [ f.1*f.2*f.1^-1*f.2^-1 ];;
```

   The name to index map stays in Python, so no generator name is ever escaped.

2. **Exponents are validated, not assumed.** The emitter rejects any exponent
   that is not a real `int` (`bool` excluded, since `True` would render as `1`)
   and bounds its magnitude. Unknown generators are rejected in the emitter too,
   rather than trusted to `__post_init__`.

Tests cover **both** slots: a payload in a generator name *and* a payload in an
exponent. Revision 1's test covered only the first and would have passed while
the container was compromised.

---

## 5. Public API

```python
@dataclass(frozen=True)
class GapGroupInfo:
    abelian_invariants: tuple[int, ...] | None   # None = not determined; () = trivial group
    is_finite: bool | None                   # None = not determined within the timeout
    order: int | None                        # None when infinite or not determined
    structure_description: str | None
    small_group_id: tuple[int, int] | None   # only for finite groups GAP can identify


def gap_available() -> bool: ...
def gap_group_info(presentation, *, session=None, timeout=60.0) -> GapGroupInfo: ...
def gap_abelian_invariants(presentation, *, session=None, timeout=60.0) -> tuple[int, ...]: ...
```

`is_finite: bool | None` and `order: int | None` are separate because they answer
different questions: `None` for `is_finite` means the bridge ran out of budget,
while `order=None` with `is_finite=False` means the group is genuinely infinite.

`abelian_invariants` is `| None` for the same reason, which revision 1 got wrong
in the very dataclass that claimed to avoid the mistake: GAP returns the empty
list for the trivial group, so `()` is a **legitimate value** and cannot double
as "not determined". `gap_abelian_invariants` raises `GapTimeout` rather than
returning `()`.

The generated query asks `Size` first and only asks for `IdGroup` when the group
is finite **and of an order the SmallGroups library actually covers**. Measured
on the elementary abelian group of order 512, which it does not cover: with the
guard, `ID=NONE` and the sentinel come back cleanly; without it, GAP drops into
the break loop and writes its prompt plus raw ANSI escapes into stdout **with
exit code 0** — and the break loop reads stdin, which is the same hang mechanism
§3.3 cites for rejecting the persistent-process design. The guard and the
sentinel together are what keep it out of the chosen design.

Three further mechanics, each verified:

- **Newlines must be emitted as `Chr(10)`, never as an escape inside a GAP
  string.** A string literal containing a newline is a syntax error, and GAP's
  parser recovery then swallows the rest of the input — producing *empty stdout
  with exit code 0*. Several probe runs failed this way before the cause was
  isolated.
- **`SizeScreen([256, 40])` must precede the query.** Without it GAP wraps stdout
  at 80 columns: `AbelianInvariants` of a rank-30 free abelian group comes back
  with a literal newline mid-list. With it, the same query is one line.
- The gap binary is found by **probing candidates and running each one**, not by
  `command -v`: on this image `bash -lc 'command -v gap'` prints nothing and
  exits 1, while the absolute path works. Revision 1 stated the `command -v`
  route as verified; it was not, and as written the bridge would have reported
  itself unavailable, skipped every opt-in test, and shipped non-functional
  behind green CI.

---

## 6. Validation

Opt-in via `PYTOP_GAP_BRIDGE=1`, following the existing
`PYTOP_SAGE_ORACLE` / `PYTOP_SNAPPY_ORACLE` pattern. Skipped by default so CI
without Docker stays green.

| Check | Assertion |
|---|---|
| Differential: abelianization | pytop's SNF `abelianization` == GAP `AbelianInvariants` for T², Klein, ℝP², S¹∨S¹, trefoil group |
| Identification | Q8 → `("Q8", (8,4), 8)`; S3 → `("S3", (6,1), 6)` |
| Infinite groups | T² → `is_finite=False`, `order=None`, invariants `(0,0)` |
| Injection (name) | a presentation with a GAP payload as a generator name produces source containing none of it |
| Injection (exponent) | a non-`int` exponent is rejected by the emitter before any container is touched |
| Timeout | a tiny timeout yields the not-determined result and leaves **no** GAP process alive in the container |
| Line wrapping | a rank-40 free abelian group returns 40 invariants on one line |
| SmallGroups gap | the order-512 elementary abelian group returns `small_group_id=None` with the sentinel intact, not break-loop text |
| Trivial group | invariants `()` is distinguishable from a timed-out `None` |
| Unavailable | `gap_available()` is `False` and `GapUnavailableError` is raised with guidance when the image is absent |

**Always-on tests** (no Docker): code generation, sanitization-by-construction,
the name→index mapping, result-type semantics, and `gap_available()` returning
`False` gracefully. Only the GAP round-trips are opt-in.

---

## 7. Non-goals

- Regina integration — blocked, evidence in §1, proposed as P12.6.
- In-process FFI (`libgap`). It would remove the container entirely, but
  requires building GAP against the host Python; out of scope for a pure-Python
  package with no runtime dependencies.
- Replacing `van_kampen._identify_group`. The bridge is an optional second
  opinion, not a dependency: pytop must keep working with no Docker present.
- Sending arbitrary user GAP code. `evaluate` is internal; the public surface
  takes presentations only.
