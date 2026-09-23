# P12.5 Infinite Complexes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `pytop.experimental.infinite_complexes` — integral homology of four standard infinite CW complexes (proven), homology of user-supplied towers (conditional, machine-checked), and a claim-free Rips Betti scan.

**Architecture:** Three independent parts in one module. Part A evaluates a shipped or in-module skeleton at index `degree+1` and returns a plain `HomologyResult` — no uncertainty machinery, because there is no caller-supplied tower. Part B takes explicit stages plus signed inclusion data, verifies the chain-map law and a **non-empty** dimension window, and returns a `ConditionalHomology` naming every tail assumption. Part C builds Rips complexes on metric balls and reports Betti numbers per radius while making no claim about any colimit.

**Tech Stack:** Pure Python 3.11+, stdlib only. Reuses `pytop.cellular_homology` (`CWComplex`, `cellular_homology`, private `_mat_mul`), `pytop.homology` (`SimplicialComplex`, `betti_numbers`), `pytop.persistent_homology.vietoris_rips_filtration`, `pytop.metric_spaces.FiniteMetricSpace`.

**Spec:** `docs/superpowers/specs/2026-09-22-p12-5-infinite-complexes-design.md` (revision 4)
**Critique registers:** `docs/architecture-critique{,-round2,-round3}.md`

**Interpreter:** always `py -3.14` on this machine.

---

## File Structure

| File | Responsibility |
|---|---|
| `src/pytop/experimental/infinite_complexes.py` | Everything. Single module (~450 LOC): errors, Part A skeletons + functions, Part B types + algorithm, Part C protocol + lattice + scan. |
| `src/pytop/experimental/__init__.py` | Add 16 exports following the existing `from .module import (...)` + `__all__` pattern. |
| `tests/experimental/test_infinite_complexes.py` | All tests (~600 LOC). |
| `CHANGELOG.md` | `[Unreleased]` entry. |
| `docs/CAPABILITIES_AND_ROADMAP.md` | Flip P12.5 to ✅; update Phase 12 count 2/5 → 3/5. |
| `CLAUDE.md` | Branching-strategy status line. |

Single module is deliberate: round 1 rejected a five-module package as structure invented before content (register C-14). Split only if a part exceeds ~600 real lines.

---

## Task 1: Module skeleton and errors

**Files:**
- Create: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest
from pytop.experimental.infinite_complexes import (
    InsufficientStagesError,
    NotATowerError,
)


def test_errors_are_value_errors():
    assert issubclass(NotATowerError, ValueError)
    assert issubclass(InsufficientStagesError, ValueError)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'pytop.experimental.infinite_complexes'`

- [ ] **Step 3: Write minimal implementation**

Module docstring must state the two facts the critique rounds established, because they are the reason the module is shaped this way:

```python
"""Countably infinite CW complexes and claim-free Rips scans.

Homology commutes with direct limits, so ``H_k(K) = colim H_k(K_i)`` for an
exhaustion ``K = union K_i`` by finite subcomplexes. Two facts shape this module:

* A direct limit is **not** determined by the groups alone. In
  ``Z --x2--> Z --x2--> ...`` every group is ``Z`` and every Betti number is 1,
  yet the colimit is ``Z[1/2]``. Nothing here ever infers stabilisation from
  observation -- not from repeated Betti numbers, and not from repeated
  isomorphisms (a lacunary wedge defeats any fixed patience).
* The only proof route used is structural: attaching a cell of dimension ``d``
  affects only ``H_{d-1}`` and ``H_d``, so if every cell added after stage ``N``
  has dimension ``>= k+2`` then ``H_k(K_N) = H_k(K)``. The threshold is ``k+2``,
  not ``k+1``: a ``(k+1)``-cell can kill a class in ``H_k``.
"""

from __future__ import annotations


class NotATowerError(ValueError):
    """The supplied stages and inclusions do not form a tower of chain complexes."""


class InsufficientStagesError(ValueError):
    """No non-empty window of stages satisfies the dimension hypothesis."""
```

- [ ] **Step 4: Run test to verify it passes**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q`
Expected: 1 passed

- [ ] **Step 5: Commit**

```bash
git add src/pytop/experimental/infinite_complexes.py tests/experimental/test_infinite_complexes.py
git commit -m "feat(infinite-complexes): module skeleton and error types"
```

---

## Task 2: Part A skeleton builders

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

These two builders are new mathematics; both were verified numerically before entering the spec. `cw_lens_space` **cannot** be reused — it takes only `p` and returns a fixed 3-dimensional complex (register R2-C-03).

- [ ] **Step 1: Write the failing tests**

```python
from pytop import cellular_homology, cw_lens_space, cw_real_projective_space
from pytop.experimental.infinite_complexes import (
    _lens_skeleton,
    _s_infinity_skeleton,
)


def test_lens_skeleton_matches_rp_byte_for_byte_at_p_2():
    for n in range(8):
        got = _lens_skeleton(2, n)
        want = cw_real_projective_space(n)
        assert got.cell_counts == want.cell_counts
        assert got.boundary_maps == want.boundary_maps


def test_lens_skeleton_truncation_matches_shipped_lens_space():
    assert _lens_skeleton(5, 3).boundary_maps == cw_lens_space(5).boundary_maps


@pytest.mark.parametrize("p", [2, 3, 5])
def test_lens_skeleton_homology_at_evaluation_index(p):
    # "at the evaluation index" is load-bearing: on a FIXED skeleton the top
    # degree is ker(d_n), so H_5(_lens_skeleton(5, 5)) is Z, not Z/5.
    for k in range(7):
        h = cellular_homology(_lens_skeleton(p, k + 1), k)
        if k == 0:
            assert (h.betti, h.torsion) == (1, ())
        elif k % 2 == 1:
            assert (h.betti, h.torsion) == (0, (p,))
        else:
            assert (h.betti, h.torsion) == (0, ())


def test_s_infinity_skeleton_sphere_homology():
    assert cellular_homology(_s_infinity_skeleton(0), 0).betti == 2  # S^0 is two points
    for n in range(1, 6):
        betti = [cellular_homology(_s_infinity_skeleton(n), k).betti for k in range(n + 1)]
        assert betti == [1] + [0] * (n - 1) + [1]


def test_s_infinity_all_zero_boundaries_would_be_wrong():
    # Guards against "simplifying" the boundary matrices away: the all-zero
    # variant passes CWComplex's d.d == 0 check and yields Z^2 in every degree.
    from pytop import CWComplex

    bogus = CWComplex({k: 2 for k in range(4)}, {})
    assert cellular_homology(bogus, 2).betti == 2
    assert cellular_homology(_s_infinity_skeleton(3), 2).betti == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q`
Expected: FAIL, `ImportError: cannot import name '_lens_skeleton'`

- [ ] **Step 3: Write minimal implementation**

```python
from pytop.cellular_homology import CWComplex


def _lens_skeleton(p: int, n: int) -> CWComplex:
    """``n``-skeleton of ``S^inf / Z_p`` -- one cell per dimension.

    ``d_k`` is ``[[p]]`` for even ``k`` and ``[[0]]`` for odd ``k``. At ``p = 2``
    this is byte-identical to :func:`cw_real_projective_space`, whose
    ``d_k = 1 + (-1)^k`` takes the same values on the same parity.
    """
    return CWComplex(
        cell_counts={k: 1 for k in range(n + 1)},
        boundary_maps={k: [[p if k % 2 == 0 else 0]] for k in range(1, n + 1)},
    )


def _s_infinity_skeleton(n: int) -> CWComplex:
    """``n``-skeleton of ``S^inf`` in the antipodal structure -- two cells per dimension.

    ``d_k(e^k_pm) = e^{k-1}_pm + (-1)^k e^{k-1}_mp``.

    :func:`cw_sphere` must not be used here: it is ``{0: 1, n: 1}``, under which
    ``S^n`` is not a subcomplex of ``S^{n+1}`` and the stages are not nested.
    """
    return CWComplex(
        cell_counts={k: 2 for k in range(n + 1)},
        boundary_maps={
            k: [[1, (-1) ** k], [(-1) ** k, 1]] for k in range(1, n + 1)
        },
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): lens and antipodal sphere skeleton builders"
```

---

## Task 3: Part A public functions with parameter guards

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

Part A's freedom from witnesses is a claim about *towers*, not *parameters* (register R3-C-02): unguarded `p=0` gives all-zero boundaries and returns `Z` in every degree, where `BZ/0 = S^1` has `H_k = 0` for `k >= 2`.

- [ ] **Step 1: Write the failing tests**

```python
from pytop.experimental.infinite_complexes import (
    cp_infinity_homology,
    infinite_lens_homology,
    rp_infinity_homology,
    s_infinity_homology,
)

RP_INF = [(1, ()), (0, (2,)), (0, ()), (0, (2,)), (0, ()), (0, (2,)), (0, ()), (0, (2,)), (0, ())]
CP_INF = [(1, ()), (0, ()), (1, ()), (0, ()), (1, ()), (0, ()), (1, ()), (0, ()), (1, ())]
S_INF = [(1, ())] + [(0, ())] * 8


@pytest.mark.parametrize("k,want", list(enumerate(RP_INF)))
def test_rp_infinity_blocking_literals(k, want):
    h = rp_infinity_homology(k)
    assert (h.betti, h.torsion) == want


@pytest.mark.parametrize("k,want", list(enumerate(CP_INF)))
def test_cp_infinity_blocking_literals(k, want):
    h = cp_infinity_homology(k)
    assert (h.betti, h.torsion) == want


@pytest.mark.parametrize("k,want", list(enumerate(S_INF)))
def test_s_infinity_blocking_literals(k, want):
    h = s_infinity_homology(k)
    assert (h.betti, h.torsion) == want


def test_infinite_lens_agrees_with_rp_at_p_2():
    for k in range(9):
        a, b = infinite_lens_homology(2, k), rp_infinity_homology(k)
        assert (a.betti, a.torsion) == (b.betti, b.torsion)


@pytest.mark.parametrize("bad_p", [0, -1, -5])
def test_infinite_lens_rejects_p_below_one(bad_p):
    with pytest.raises(ValueError, match="p must be at least 1"):
        infinite_lens_homology(bad_p, 3)


@pytest.mark.parametrize(
    "fn", [rp_infinity_homology, cp_infinity_homology, s_infinity_homology]
)
def test_negative_degree_rejected(fn):
    with pytest.raises(ValueError, match="degree must be >= 0"):
        fn(-1)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q`
Expected: FAIL, `ImportError: cannot import name 'rp_infinity_homology'`

- [ ] **Step 3: Write minimal implementation**

Error messages follow P19.1 WHY-HOW-THEN: what is wrong, why it matters, what to do.

```python
from pytop.cellular_homology import (
    cellular_homology,
    cw_complex_projective_space,
    cw_real_projective_space,
)
from pytop.homology import HomologyResult


def _check_degree(degree: int) -> None:
    if degree < 0:
        raise ValueError(
            f"degree must be >= 0, got {degree}. Homology is not defined in "
            f"negative degrees, so there is nothing to compute. Pass a "
            f"non-negative degree, e.g. rp_infinity_homology(1)."
        )


def rp_infinity_homology(degree: int) -> HomologyResult:
    """``H_degree(RP^inf; Z)`` -- ``Z``, then ``Z/2`` in odd degrees, 0 in even.

    ``RP^n -> RP^{n+1}`` attaches one ``(n+1)``-cell, so every cell added after
    stage ``degree+1`` has dimension ``>= degree+2`` and the structural theorem
    applies at that index.
    """
    _check_degree(degree)
    return cellular_homology(cw_real_projective_space(degree + 1), degree)


def cp_infinity_homology(degree: int) -> HomologyResult:
    """``H_degree(CP^inf; Z)`` -- ``Z`` in even degrees, 0 in odd.

    ``CP^n -> CP^{n+1}`` attaches one ``(2n+2)``-cell.
    """
    _check_degree(degree)
    return cellular_homology(cw_complex_projective_space(degree + 1), degree)


def s_infinity_homology(degree: int) -> HomologyResult:
    """``H_degree(S^inf; Z)`` -- ``Z`` in degree 0, 0 above. ``S^inf`` is contractible."""
    _check_degree(degree)
    return cellular_homology(_s_infinity_skeleton(degree + 1), degree)


def infinite_lens_homology(p: int, degree: int) -> HomologyResult:
    """``H_degree(BZ/p; Z)`` -- ``Z``, then ``Z/p`` in odd degrees, 0 in even.

    ``p`` is caller input and is guarded: ``p = 0`` would give all-zero boundary
    maps and return ``Z`` in every degree, where ``BZ/0 = K(Z,1) = S^1`` has
    ``H_k = 0`` for ``k >= 2``.
    """
    _check_degree(degree)
    if p < 1:
        raise ValueError(
            f"p must be at least 1, got {p}. BZ/p is the classifying space of a "
            f"cyclic group of order p, and p < 1 names no such group -- at p = 0 "
            f"the skeleton degenerates to all-zero boundary maps and would report "
            f"Z in every degree. Pass p >= 1, e.g. infinite_lens_homology(5, 3)."
        )
    return cellular_homology(_lens_skeleton(p, degree + 1), degree)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): Part A standard-space homology with parameter guards"
```

---

## Task 4: Part B data types

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

`StageInclusion` stores signed entries as **tuples, not a Mapping**, so the frozen dataclass is genuinely hashable (register R3-L-02). The truthiness guard goes on `ConditionalHomology`, the object callers hold — rev 3 put it on `Assumptions` where `bool(result)` stayed constantly `True` from the dataclass default (R3-H-05).

- [ ] **Step 1: Write the failing tests**

```python
from pytop.experimental.infinite_complexes import (
    Assumptions,
    ConditionalHomology,
    StageInclusion,
    TailAssumption,
)


def test_stage_inclusion_is_hashable():
    inc = StageInclusion(images=((0, ((0, 1),)), (1, ((0, -1),))))
    assert hash(inc) == hash(StageInclusion(images=((0, ((0, 1),)), (1, ((0, -1),)))))


def test_stage_inclusion_lookup():
    inc = StageInclusion(images=((0, ((0, 1), (1, 1))), (2, ((3, -1),))))
    assert inc.at(0) == ((0, 1), (1, 1))
    assert inc.at(2) == ((3, -1),)
    assert inc.at(5) == ()


def test_conditional_homology_is_falsy_when_anything_assumed():
    from pytop import cellular_homology, cw_sphere

    group = cellular_homology(cw_sphere(2), 2)
    assumed = Assumptions(
        assumed=frozenset(TailAssumption),
        min_tail_cell_dimension=4,
        evaluated_stage=1,
        verified_steps=(1, 2),
    )
    result = ConditionalHomology(group=group, assumptions=assumed)
    assert not result
    assert ConditionalHomology(group=group, assumptions=Assumptions(
        assumed=frozenset(), min_tail_cell_dimension=4,
        evaluated_stage=1, verified_steps=(1,),
    ))
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: FAIL, `ImportError: cannot import name 'StageInclusion'`

- [ ] **Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from enum import Enum


class TailAssumption(Enum):
    """What was assumed about the stages beyond the last one supplied."""

    STAGES_EXIST = "stages_exist"
    INCLUSIONS_VALID = "inclusions_valid"
    CELL_DIMENSIONS = "cell_dimensions"


@dataclass(frozen=True)
class StageInclusion:
    """Signed cell map ``C_*(K_i) -> C_*(K_{i+1})``, one entry per degree.

    ``images`` is a tuple of ``(degree, entries)`` pairs where ``entries[j]`` is
    ``(target_index, sign)`` for the ``j``-th cell of that degree, ``sign`` in
    ``{+1, -1}``.

    The sign is required, not decorative: a cellular inclusion is the identity on
    cells only when both complexes orient the shared cells identically. ``RP^2``
    sitting inside an ``RP^3`` whose 2-cell is oppositely oriented is a genuine
    subcomplex inclusion that an unsigned map cannot express.

    Stored as nested tuples rather than a ``Mapping`` so the frozen dataclass is
    actually hashable.
    """

    images: tuple[tuple[int, tuple[tuple[int, int], ...]], ...]

    def at(self, degree: int) -> tuple[tuple[int, int], ...]:
        """Entries for ``degree``; empty when that degree carries no cells."""
        for k, entries in self.images:
            if k == degree:
                return entries
        return ()


@dataclass(frozen=True)
class Assumptions:
    """Exactly what was not proven."""

    assumed: frozenset[TailAssumption]
    min_tail_cell_dimension: int
    evaluated_stage: int
    verified_steps: tuple[int, ...]


@dataclass(frozen=True)
class ConditionalHomology:
    """A computed group plus the assumptions standing behind it."""

    group: HomologyResult
    assumptions: Assumptions

    def __bool__(self) -> bool:
        """False whenever anything was assumed -- which, for towers, is always."""
        return not self.assumptions.assumed
```

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): Part B data types with signed inclusions"
```

---

## Task 5: Chain-map verification

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

Comparing `cell_counts` verifies nothing (register R2-C-02): `cw_moore_space(i+2, 1)` has constant counts `{0:1, 1:1, 2:1}`, is pairwise non-nested, and `H_1` runs `Z/2, Z/3, Z/4, ...`.

- [ ] **Step 1: Write the failing tests**

```python
from pytop import CWComplex, cw_moore_space
from pytop.experimental.infinite_complexes import _inclusion_matrix, _verify_chain_map


def _identity_inclusion(complex_: CWComplex) -> StageInclusion:
    return StageInclusion(
        images=tuple(
            (k, tuple((j, 1) for j in range(n)))
            for k, n in sorted(complex_.cell_counts.items())
        )
    )


def test_inclusion_matrix_shape_and_signs():
    inc = StageInclusion(images=((1, ((0, 1), (2, -1))),))
    m = _inclusion_matrix(inc, degree=1, source_cells=2, target_cells=3)
    assert m == [[1, 0], [0, 0], [0, -1]]


def test_moore_tower_is_rejected():
    # constant cell counts, pairwise non-nested: a count check would pass.
    stages = [cw_moore_space(k + 2, 1) for k in range(4)]
    for i in range(3):
        with pytest.raises(NotATowerError):
            _verify_chain_map(stages[i], stages[i + 1], _identity_inclusion(stages[i]), step=i)


def test_genuine_skeletal_inclusion_is_accepted():
    a, b = cw_real_projective_space(2), cw_real_projective_space(3)
    _verify_chain_map(a, b, _identity_inclusion(a), step=0)  # must not raise


def test_orientation_reversing_inclusion_needs_signs():
    rp2 = CWComplex({0: 1, 1: 1, 2: 1}, {1: [[0]], 2: [[2]]})
    rp3_flipped = CWComplex({0: 1, 1: 1, 2: 1, 3: 1}, {1: [[0]], 2: [[-2]], 3: [[0]]})
    unsigned = _identity_inclusion(rp2)
    with pytest.raises(NotATowerError):
        _verify_chain_map(rp2, rp3_flipped, unsigned, step=0)
    signed = StageInclusion(images=((0, ((0, 1),)), (1, ((0, 1),)), (2, ((0, -1),))))
    _verify_chain_map(rp2, rp3_flipped, signed, step=0)  # must not raise
```

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Write minimal implementation**

`CWComplex.__post_init__` strips zero-valued keys, so all cell-count arithmetic must use `.get(k, 0)`.

```python
from pytop.cellular_homology import _mat_mul

Matrix = list[list[int]]


def _inclusion_matrix(
    inclusion: StageInclusion, degree: int, source_cells: int, target_cells: int
) -> Matrix:
    """Signed ``target_cells x source_cells`` matrix of ``iota_degree``."""
    m = [[0] * source_cells for _ in range(target_cells)]
    entries = inclusion.at(degree)
    if len(entries) != source_cells:
        raise NotATowerError(
            f"inclusion at degree {degree} lists {len(entries)} cells but the "
            f"source complex has {source_cells}. Every cell of the source must "
            f"be assigned a (target_index, sign) pair. Add the missing entries."
        )
    seen: set[int] = set()
    for j, (target, sign) in enumerate(entries):
        if sign not in (1, -1):
            raise NotATowerError(
                f"inclusion sign at degree {degree}, cell {j} is {sign}; only "
                f"+1 and -1 describe a cellular inclusion. Use -1 when the two "
                f"complexes orient that shared cell oppositely."
            )
        if not 0 <= target < target_cells:
            raise NotATowerError(
                f"inclusion at degree {degree}, cell {j} targets index {target}, "
                f"but the target complex has {target_cells} cells in that degree."
            )
        if target in seen:
            raise NotATowerError(
                f"inclusion at degree {degree} is not injective: two source cells "
                f"both map to target index {target}. A subcomplex inclusion is "
                f"injective on cells."
            )
        seen.add(target)
        m[target][j] = sign
    return m


def _verify_chain_map(
    source: CWComplex, target: CWComplex, inclusion: StageInclusion, step: int
) -> None:
    """Raise :class:`NotATowerError` unless ``d.iota == iota.d`` in every degree.

    Cell counts cannot do this job: they carry no cell identity and no attaching
    data, so a sequence of unrelated complexes with monotone counts passes a
    count check while having no colimit at all.
    """
    top = max([*source.cell_counts, *target.cell_counts], default=0)
    for k in range(1, top + 1):
        src_k = source.cell_counts.get(k, 0)
        src_km1 = source.cell_counts.get(k - 1, 0)
        tgt_k = target.cell_counts.get(k, 0)
        tgt_km1 = target.cell_counts.get(k - 1, 0)
        if src_k == 0:
            continue
        iota_k = _inclusion_matrix(inclusion, k, src_k, tgt_k)
        iota_km1 = _inclusion_matrix(inclusion, k - 1, src_km1, tgt_km1)
        lhs = _mat_mul(target._boundary_matrix(k), iota_k)  # d^{i+1} . iota_k
        rhs = _mat_mul(iota_km1, source._boundary_matrix(k))  # iota_{k-1} . d^i
        if lhs != rhs:
            raise NotATowerError(
                f"step {step}, degree {k}: the chain-map law fails -- "
                f"d.iota = {lhs} but iota.d = {rhs}. The stages and inclusions "
                f"do not describe a subcomplex inclusion. If the two complexes "
                f"orient a shared cell oppositely, give that cell sign -1."
            )
```

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): signed chain-map verification"
```

---

## Task 6: Window search and `colimit_homology`

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

The window's upper bound `M-1` is what makes it non-empty. Allowing `N = M` made the condition vacuously true for every input and returned confident wrong groups on the designated negative controls (register R3-C-01). There is **no** `N >= degree+1` floor: that is a property of Part A's towers, not a hypothesis of the theorem (R3-H-01).

- [ ] **Step 1: Write the failing tests**

```python
from pytop.experimental.infinite_complexes import colimit_homology


def _tower(stages):
    return stages, [_identity_inclusion(s) for s in stages[:-1]]


def test_vacuity_discrete_points_raises():
    stages, incs = _tower([CWComplex({0: i + 1}, {}) for i in range(1, 6)])
    with pytest.raises(InsufficientStagesError):
        colimit_homology(stages, incs, degree=0)


def test_vacuity_wedge_of_circles_raises():
    stages, incs = _tower([CWComplex({0: 1, 1: i}, {1: [[0] * i]}) for i in range(1, 5)])
    with pytest.raises(InsufficientStagesError):
        colimit_homology(stages, incs, degree=1)


def test_no_spurious_floor_wedge_of_spheres():
    stages, incs = _tower([CWComplex({0: 1, 2: i}, {}) for i in range(1, 5)])
    result = colimit_homology(stages, incs, degree=0)
    assert result.assumptions.evaluated_stage == 0
    assert result.group.betti == 1


def test_no_spurious_floor_high_dimensional_cells():
    stages, incs = _tower([CWComplex({0: 1, 3: 1, 5: j}, {}) for j in range(1, 5)])
    result = colimit_homology(stages, incs, degree=3)
    assert result.assumptions.evaluated_stage == 0
    assert result.group.betti == 1


@pytest.mark.parametrize("degree,want_stage", [(1, 2), (3, 4)])
def test_rp_tower_evaluates_at_degree_plus_one(degree, want_stage):
    stages, incs = _tower([cw_real_projective_space(n) for n in range(degree + 4)])
    result = colimit_homology(stages, incs, degree=degree)
    assert result.assumptions.evaluated_stage == want_stage
    assert (result.group.betti, result.group.torsion) == (0, (2,))


def test_result_is_falsy_and_names_every_tail_assumption():
    stages, incs = _tower([cw_real_projective_space(n) for n in range(5)])
    result = colimit_homology(stages, incs, degree=1)
    assert not result
    assert result.assumptions.assumed == frozenset(TailAssumption)
    assert result.assumptions.min_tail_cell_dimension == 3
    assert result.assumptions.verified_steps  # non-empty by construction


def test_chain_embedding_that_is_not_a_subcomplex_is_accepted():
    # S^4 -> CP^2 at chain level: all boundaries zero, so the law holds trivially.
    # The algebra is sound; the topological reading is the caller's job, and the
    # docstring says so. This test pins that documented scope.
    s4 = CWComplex({0: 1, 4: 1}, {})
    cp2 = cw_complex_projective_space(2)
    inc = StageInclusion(images=((0, ((0, 1),)), (4, ((0, 1),))))
    result = colimit_homology([s4, cp2], [inc], degree=0)
    assert result.group.betti == 1
```

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Write minimal implementation**

```python
from collections.abc import Sequence


def _added_dimensions(
    source: CWComplex, target: CWComplex, inclusion: StageInclusion
) -> set[int]:
    """Dimensions in which ``target`` has cells outside the image of ``iota``."""
    top = max([*source.cell_counts, *target.cell_counts], default=0)
    added = set()
    for k in range(top + 1):
        covered = len(inclusion.at(k))
        if target.cell_counts.get(k, 0) > covered:
            added.add(k)
    return added


def colimit_homology(
    stages: Sequence[CWComplex],
    inclusions: Sequence[StageInclusion],
    degree: int,
) -> ConditionalHomology:
    """``H_degree`` of the colimit of the supplied chain complexes and chain maps.

    This equals ``H_degree(union K_i)`` **only** if the supplied inclusions really
    come from subcomplex inclusions, which this function cannot check: cellular
    chain complexes retain only the degrees of attaching maps, so a chain-level
    embedding that no subcomplex inclusion induces (``{e^0, e^4}`` into ``CP^2``,
    say) passes verification. The algebra is sound; the topological reading is
    the caller's responsibility.

    The result is always conditional: the tail beyond ``stages[-1]`` is assumed,
    never verified. :attr:`ConditionalHomology.assumptions` names what was assumed.
    """
    _check_degree(degree)
    if len(stages) < 2:
        raise InsufficientStagesError(
            f"at least 2 stages are needed, got {len(stages)}. A single complex "
            f"carries no information about a tail, so nothing can be concluded "
            f"about a colimit. Supply more stages."
        )
    if len(inclusions) != len(stages) - 1:
        raise NotATowerError(
            f"{len(stages)} stages need {len(stages) - 1} inclusions, got "
            f"{len(inclusions)}. Supply one inclusion per consecutive pair."
        )

    steps = len(stages) - 1
    for i in range(steps):
        _verify_chain_map(stages[i], stages[i + 1], inclusions[i], step=i)

    min_dim = degree + 2
    added = [_added_dimensions(stages[i], stages[i + 1], inclusions[i]) for i in range(steps)]

    # The window must be non-empty: N ranges over 0 .. steps-1, never steps.
    # Allowing N = steps would make the quantifier empty and the check vacuous.
    chosen = None
    for n in range(steps):
        if all(all(d >= min_dim for d in added[i]) for i in range(n, steps)):
            chosen = n
            break
    if chosen is None:
        last_bad = max(i for i in range(steps) if any(d < min_dim for d in added[i]))
        raise InsufficientStagesError(
            f"no non-empty window of the supplied stages satisfies the dimension "
            f"hypothesis for degree {degree}: step {last_bad} adds cells of "
            f"dimension {sorted(d for d in added[last_bad] if d < min_dim)}, below "
            f"the required {min_dim}. Without such a window nothing connects the "
            f"supplied stages to the colimit. Supply stages far enough out that "
            f"the tail adds only cells of dimension >= {min_dim} -- note this "
            f"function cannot predict how far that is."
        )

    return ConditionalHomology(
        group=cellular_homology(stages[chosen], degree),
        assumptions=Assumptions(
            assumed=frozenset(TailAssumption),
            min_tail_cell_dimension=min_dim,
            evaluated_stage=chosen,
            verified_steps=tuple(range(chosen, steps)),
        ),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): non-vacuous window search and colimit_homology"
```

---

## Task 7: Part C protocol and lattice helper

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

Nothing in the repo supplies a lattice metric: `coarse_geometry`'s `"z_lattice"` is a Descriptive-layer tag, `grid_graph` is a test fixture, and `closed_ball` comprehends over `space.carrier` so cannot serve an infinite lattice (register R3-M-04). Without this helper `ProperMetric` would ship with zero implementations.

- [ ] **Step 1: Write the failing tests**

```python
from pytop.experimental.infinite_complexes import z_lattice


def test_z_lattice_ball_sizes_euclidean():
    lat = z_lattice(2)
    assert [len(lat.ball((0, 0), r)) for r in (1, 2, 3, 4, 5)] == [5, 13, 29, 49, 81]


def test_z_lattice_norms_differ():
    assert len(z_lattice(2, norm="linf").ball((0, 0), 1)) == 9
    assert len(z_lattice(2, norm="l1").ball((0, 0), 1)) == 5


def test_z_lattice_distance():
    lat = z_lattice(2)
    assert lat.distance((0, 0), (1, 1)) == pytest.approx(2**0.5)
    assert z_lattice(2, norm="l1").distance((0, 0), (1, 1)) == 2
    assert z_lattice(2, norm="linf").distance((0, 0), (1, 1)) == 1


def test_z_lattice_rejects_bad_dimension():
    with pytest.raises(ValueError, match="n must be >= 1"):
        z_lattice(0)
```

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Write minimal implementation**

```python
import itertools
import math
from typing import Any, Literal, Protocol, runtime_checkable

Norm = Literal["l2", "l1", "linf"]


@runtime_checkable
class ProperMetric(Protocol):
    """A metric space whose balls are finite.

    Finiteness is the provider's contract -- ``ball`` returns a ``Sequence`` --
    not a runtime assertion. Deciding it would mean enumerating a ball, which
    does not terminate for Q^2 or R^2.
    """

    def ball(self, center: Any, radius: float) -> Sequence[Any]: ...

    def distance(self, x: Any, y: Any) -> float: ...


@dataclass(frozen=True)
class _ZLattice:
    n: int
    norm: Norm

    def distance(self, x: Any, y: Any) -> float:
        deltas = [abs(a - b) for a, b in zip(x, y, strict=True)]
        if self.norm == "l1":
            return float(sum(deltas))
        if self.norm == "linf":
            return float(max(deltas, default=0))
        return math.sqrt(sum(d * d for d in deltas))

    def ball(self, center: Any, radius: float) -> Sequence[Any]:
        r = int(math.floor(radius))
        ranges = [range(c - r, c + r + 1) for c in center]
        return [
            point
            for point in itertools.product(*ranges)
            if self.distance(center, point) <= radius
        ]


def z_lattice(n: int, *, norm: Norm = "l2") -> ProperMetric:
    """The integer lattice ``Z^n`` as a :class:`ProperMetric`.

    The norm is explicit because reported Betti numbers depend on it: at
    ``eps = 1`` the Euclidean disks give ``b_1 = 0, 4, 16, 32, 60`` while
    ``linf`` balls give ``4, 16, 36, 64, 100`` and ``l1`` balls ``0, 4, 12, 24, 40``.
    """
    if n < 1:
        raise ValueError(
            f"n must be >= 1, got {n}. Z^0 is a single point and carries no "
            f"lattice structure. Pass n >= 1, e.g. z_lattice(2)."
        )
    if norm not in ("l2", "l1", "linf"):
        raise ValueError(
            f"norm must be 'l2', 'l1' or 'linf', got {norm!r}. The norm decides "
            f"the shape of every ball and therefore the Betti numbers reported. "
            f"Pass one of the three, e.g. z_lattice(2, norm='l2')."
        )
    return _ZLattice(n=n, norm=norm)
```

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): ProperMetric protocol and Z^n lattice helper"
```

---

## Task 8: `rips_betti_scan`

**Files:**
- Modify: `src/pytop/experimental/infinite_complexes.py`
- Test: `tests/experimental/test_infinite_complexes.py`

Two bounds, both stop-and-record. `max_points` caps the ball **before** the complex is built — the `d_k` guard needs `f_vector()`, which exists only after construction, so a reduction-side bound alone cannot stop an enumeration blow-up (register R3-H-03). Rows are normalised to `max_degree+1` entries because `betti_numbers` returns length `complex.dimension + 1`, which varies with radius (R3-H-04).

- [ ] **Step 1: Write the failing tests**

```python
from pytop.experimental.infinite_complexes import ScanStop, rips_betti_scan


def test_scan_epsilon_one_euclidean_matches_measured_values():
    scan = rips_betti_scan(z_lattice(2), (0, 0), eps=1.0, radii=[1, 2, 3, 4, 5], max_degree=1)
    assert [row[1] for row in scan.betti_z] == [0, 4, 16, 32, 60]
    assert all(row[0] == 1 for row in scan.betti_z)


def test_scan_rows_are_normalised_across_ragged_radii():
    # R=1 has no 3-simplex (dimension 2 -> raw 3-tuple); R>=2 has dimension 3.
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=2**0.5, radii=[1, 2, 3], max_degree=3
    )
    assert all(len(row) == 4 for row in scan.betti_z)
    assert scan.betti_z[0] == (1, 0, 0, 0)
    assert scan.betti_z[1] == (1, 0, 0, 0)


def test_scan_stops_on_point_cap_and_keeps_partial_results():
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=1.0, radii=[1, 2, 10], max_degree=1, max_points=30
    )
    assert scan.stopped_reason is ScanStop.POINT_CAP
    assert scan.stopped_at_radius == 10
    assert len(scan.radii) == 2 < 3
    assert len(scan.betti_z) == len(scan.radii)


def test_scan_stops_on_boundary_cap():
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=2**0.5, radii=[1, 6], max_degree=3,
        max_boundary_dim=50,
    )
    assert scan.stopped_reason is ScanStop.BOUNDARY_CAP
    assert len(scan.radii) == 1


def test_scan_makes_no_colimit_claim_in_its_fields():
    scan = rips_betti_scan(z_lattice(2), (0, 0), eps=1.0, radii=[1, 2], max_degree=1)
    assert not any(
        "colimit" in f or "converge" in f or "stable" in f
        for f in scan.__dataclass_fields__
    )


@pytest.mark.parametrize(
    "kwargs,match",
    [
        ({"radii": [2, 1]}, "strictly increasing"),
        ({"eps": 0.0}, "eps must be > 0"),
        ({"max_degree": -1}, "max_degree must be >= 0"),
    ],
)
def test_scan_preconditions(kwargs, match):
    base = dict(metric=z_lattice(2), center=(0, 0), eps=1.0, radii=[1, 2], max_degree=1)
    with pytest.raises(ValueError, match=match):
        rips_betti_scan(**{**base, **kwargs})
```

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Write minimal implementation**

Two adapters are required and neither exists in the repo: `vietoris_rips_filtration` needs `.carrier` + `.distance_between`, and `simplicial_homology` needs a `SimplicialComplex`. `SimplicialComplex(fc.simplices)` is sound only because `max_scale=eps` keeps the truncated complex face-closed — a face's diameter never exceeds its coface's.

```python
from pytop.homology import betti_numbers
from pytop.metric_spaces import FiniteMetricSpace
from pytop.persistent_homology import vietoris_rips_filtration
from pytop.simplicial_complexes import SimplicialComplex


class ScanStop(Enum):
    """Why a scan stopped early."""

    POINT_CAP = "point_cap"
    BOUNDARY_CAP = "boundary_cap"


@dataclass(frozen=True)
class RipsBettiScan:
    """Betti numbers of Rips complexes on metric balls, per radius.

    This records what was computed on **finite** complexes. It makes no claim
    about any infinite complex: a growing sequence does not imply a large
    colimit, and this scan tests no induced map.
    """

    eps: float
    max_degree: int
    radii: tuple[float, ...]
    betti_z: tuple[tuple[int, ...], ...]
    stopped_at_radius: float | None
    stopped_reason: ScanStop | None


def rips_betti_scan(
    metric: ProperMetric,
    center: Any,
    eps: float,
    radii: Sequence[float],
    max_degree: int,
    *,
    max_points: int = 200,
    max_boundary_dim: int = 400,
) -> RipsBettiScan:
    """Integral Betti numbers of ``Rips_eps`` on balls of the given radii.

    **Makes no claim about the homology of any infinite complex.** A growing
    Betti sequence does not imply a large colimit -- a system with
    ``H_1(K_i) = Z^i`` whose inclusions kill every earlier generator has colimit
    0 -- and this function tests no induced map, so it licenses no rank
    statement in either direction.

    The complex is built to dimension ``max_degree + 1`` because ``H_k`` is
    faithful only when simplices up to dimension ``k+1`` are present. Rows are
    normalised to exactly ``max_degree + 1`` entries.

    Both bounds stop and record rather than raising, so partial results survive.
    """
    if eps <= 0:
        raise ValueError(
            f"eps must be > 0, got {eps}. At eps <= 0 the Rips complex has no "
            f"edges and every ball reports its own point count. Pass a positive "
            f"scale, e.g. eps=1.0."
        )
    if max_degree < 0:
        raise ValueError(
            f"max_degree must be >= 0, got {max_degree}. Pass the top homological "
            f"degree you want reported, e.g. max_degree=1 for H_0 and H_1."
        )
    radii = tuple(radii)
    if any(b <= a for a, b in zip(radii, radii[1:], strict=False)):
        raise ValueError(
            f"radii must be strictly increasing, got {radii}. Each radius names a "
            f"larger ball than the last; repeats and reversals make the scan's "
            f"rows meaningless. Sort and de-duplicate the radii."
        )

    done_radii: list[float] = []
    rows: list[tuple[int, ...]] = []
    stop_radius: float | None = None
    stop_reason: ScanStop | None = None

    for radius in radii:
        points = list(metric.ball(center, radius))
        if len(points) > max_points:
            stop_radius, stop_reason = radius, ScanStop.POINT_CAP
            break
        space = FiniteMetricSpace(carrier=tuple(points), distance=metric.distance)
        filtration = vietoris_rips_filtration(
            space, max_dimension=max_degree + 1, max_scale=eps
        )
        complex_ = SimplicialComplex(filtration.simplices)
        if any(
            max(len(complex_._boundary(k)), len(complex_._boundary(k)[0]) if complex_._boundary(k) else 0)
            > max_boundary_dim
            for k in range(1, complex_.dimension + 1)
        ):
            stop_radius, stop_reason = radius, ScanStop.BOUNDARY_CAP
            break
        raw = betti_numbers(complex_)
        rows.append(tuple(raw[k] if k < len(raw) else 0 for k in range(max_degree + 1)))
        done_radii.append(radius)

    return RipsBettiScan(
        eps=eps,
        max_degree=max_degree,
        radii=tuple(done_radii),
        betti_z=tuple(rows),
        stopped_at_radius=stop_radius,
        stopped_reason=stop_reason,
    )
```

**Note for the implementer:** `complex_._boundary(k)` is a placeholder — check the real helper name in `pytop/homology.py` (`boundary_matrix(complex_obj, k)`) and use it. Compute each boundary matrix once and reuse; do not call it twice per degree as the sketch does.

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Measure and fix the two defaults**

The spec marks `max_points=200` and `max_boundary_dim=400` **provisional**. Measure before finalising:

```bash
py -3.14 - <<'PY'
import time, math
from pytop.experimental.infinite_complexes import z_lattice, rips_betti_scan
for r in (3,4,5,6,7):
    t=time.perf_counter()
    s=rips_betti_scan(z_lattice(2),(0,0),eps=math.sqrt(2),radii=[r],max_degree=3,
                      max_points=10**6, max_boundary_dim=10**6)
    print(r, len(z_lattice(2).ball((0,0),r)), s.betti_z, f"{time.perf_counter()-t:.2f}s")
PY
```

Pick defaults so a first call stays under ~2 s on this machine, and record the measured table in the module docstring. Known datum: with python-flint the 392x368 boundary at R=6 takes 0.20 s.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): claim-free Rips Betti scan with two stop-and-record bounds"
```

---

## Task 9: Exports

**Files:**
- Modify: `src/pytop/experimental/__init__.py`

- [ ] **Step 1: Write the failing test**

```python
def test_all_public_names_exported_from_experimental():
    import pytop.experimental as ex

    for name in (
        "rp_infinity_homology", "cp_infinity_homology", "s_infinity_homology",
        "infinite_lens_homology", "colimit_homology", "StageInclusion",
        "TailAssumption", "Assumptions", "ConditionalHomology", "rips_betti_scan",
        "ProperMetric", "ScanStop", "RipsBettiScan", "z_lattice",
        "NotATowerError", "InsufficientStagesError",
    ):
        assert hasattr(ex, name), name
        assert name in ex.__all__, name


def test_nothing_added_to_top_level_pytop():
    import pytop

    assert not hasattr(pytop, "colimit_homology")
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Add the imports and `__all__` entries** following the file's existing `from .module import (...)` pattern.

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(infinite-complexes): export public surface from pytop.experimental"
```

---

## Task 10: Non-blocking consistency check against `eilenberg_maclane`

**Files:**
- Test: `tests/experimental/test_infinite_complexes.py`

`eilenberg_maclane` is **not** an oracle — `km_homology_cyclic` is a hard-coded transcription of the known answer. A blocking gate on it would convert independence into coupling: a maintainer facing red CI could fix either side, and a legitimate future correction to that Descriptive-layer module would red this one for an unrelated reason. The blocking literals live in Task 3; this test is a separate, non-blocking consistency note.

`HomologyResult.torsion` is flat while `KGnHomology.torsion[k]` is per-degree — the comparison needs an explicit adapter or it fails on shape rather than mathematics.

- [ ] **Step 1: Write the test**

```python
@pytest.mark.xfail(
    reason="consistency note, not an oracle: eilenberg_maclane is a curated "
    "transcription, so a divergence here is a prompt to investigate, not a gate",
    strict=False,
)
@pytest.mark.parametrize("p", [2, 3, 5])
def test_consistency_with_eilenberg_maclane(p):
    from pytop import km_homology_cyclic

    curated = km_homology_cyclic(p, 8)
    for k in range(9):
        ours = infinite_lens_homology(p, k)
        assert ours.betti == curated.betti[k]
        assert tuple(ours.torsion) == tuple(curated.torsion[k])
```

- [ ] **Step 2: Run it** — `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py -q -rxX`; expected XPASS (it should agree; the marker keeps it non-blocking either way).

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "test(infinite-complexes): non-blocking consistency note vs eilenberg_maclane"
```

---

## Task 11: Quality gates and documentation

**Files:**
- Modify: `CHANGELOG.md`, `docs/CAPABILITIES_AND_ROADMAP.md`, `CLAUDE.md`

- [ ] **Step 1: Full suite**

Run: `py -3.14 -m pytest tests/ -q`
Expected: all pass, count up by the new tests (baseline 12 022 collected).

- [ ] **Step 2: Lint and types**

Run: `py -3.14 -m ruff check src/ tests/` then `py -3.14 -m mypy src/pytop`
Expected: `All checks passed!` and `Success: no issues found`.

- [ ] **Step 3: Coverage of the new module**

Run: `py -3.14 -m pytest tests/experimental/test_infinite_complexes.py --cov=pytop.experimental.infinite_complexes --cov-report=term-missing -q`
Expected: >= 80%.

- [ ] **Step 4: Documentation**

- `CHANGELOG.md` under `[Unreleased]` → `### Added`: the three parts, naming that Part B is always conditional and Part C makes no colimit claim.
- `docs/CAPABILITIES_AND_ROADMAP.md`: P12.5 ⬜ → ✅ with a one-line summary; Phase 12 milestone count 2/5 → 3/5 in Part V.
- `CLAUDE.md`: add the release line to the Branching Strategy block.

- [ ] **Step 5: Commit and open the PR**

```bash
git add -A && git commit -m "docs: record P12.5 in changelog and roadmap"
git push -u origin feature/p12-5-infinite-complexes
gh pr create --base master --title "feat: P12.5 infinite complexes" --body "..."
```

Do **not** merge to master — that is the maintainer's call.

---

## Notes for the implementer

- Interpreter is `py -3.14`. Never `python` or bare `py`.
- `CWComplex.__post_init__` strips zero-valued keys from `cell_counts`; always use `.get(k, 0)`.
- `_mat_mul` and `CWComplex._boundary_matrix` are private but reusable (ruff's selected rules do not include `SLF`).
- `fc.simplices` from `vietoris_rips_filtration` are **positional indices** into `list(space.carrier)`, not points. Never compare them across radii.
- Error messages follow WHY-HOW-THEN (P19.1): what is wrong, why it matters, what to do — see `docs/P19_API_STABILITY.md`.
- Every claim about an existing API must be checked with `inspect.signature` before being relied on. Three critique rounds each caught an unverified reuse claim.
