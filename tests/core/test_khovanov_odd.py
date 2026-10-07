"""Odd Khovanov homology (Ozsváth–Rasmussen–Szabó 2013) on diagrams with crossings.

Audit 2026-09-24, finding 3.1: the previous engine returned total rank 25 on the
trefoil, where ORS §5 states the rank is 6, and every test it had used a diagram
with no crossings. Each expectation below comes from a theorem or a published
computation rather than from the engine:

* ``d ∘ d = 0`` on the cube of resolutions;
* ORS Lemma 2.1: every 3-cube has an even number of faces of types A+X and A+Y;
* ORS Prop. 1.6: the mod-2 reduction is the mod-2 reduction of even Khovanov homology;
* the graded Euler characteristic is the unnormalised Jones polynomial;
* ORS Prop. 1.7: ``Kh'_{m,s} ≅ R_{m,s-1} ⊕ R_{m,s+1}`` over ℤ, two copies of the
  reduced theory ``R``;
* ORS Prop. 1.8 / 5.2: for alternating knots ``R`` is σ-thin, free, of rank det(K);
* ORS §5: ``R(8_19) ⊗ ℚ`` has Poincaré polynomial ``q^6 + q^10 t^2 + q^16 t^5``,
  where even reduced Khovanov homology has rank 5;
* invariance under Reidemeister moves, crossing reordering and edge relabelling.
"""

from __future__ import annotations

import random
from collections import Counter
from itertools import combinations

import pytest

from pytop.khovanov import khovanov_homology
from pytop.khovanov_odd import (
    _cube_face_types,
    _odd_khovanov_complex,
    compare_khovanov_parities,
    khovanov_homology_odd,
)
from pytop.knot_invariants import KnotDiagram

# ---------------------------------------------------------------------------
# Diagrams: braid closures (pytop PD convention: counterclockwise, understrand
# first; positive σ_i crosses the strand from lower left over the other one)
# ---------------------------------------------------------------------------


def braid_diagram(word: list[int], n_strands: int) -> KnotDiagram:
    labels = list(range(1, n_strands + 1))
    initial = list(labels)
    fresh = n_strands + 1
    pd: list[tuple[int, int, int, int]] = []
    signs: list[int] = []
    for letter in word:
        i = abs(letter) - 1
        a, b = labels[i], labels[i + 1]
        up_left, up_right = fresh, fresh + 1
        fresh += 2
        if letter > 0:
            pd.append((b, up_right, up_left, a))
            signs.append(1)
        else:
            pd.append((a, b, up_right, up_left))
            signs.append(-1)
        labels[i], labels[i + 1] = up_left, up_right
    closing = {labels[s]: initial[s] for s in range(n_strands)}
    pd = [tuple(closing.get(x, x) for x in crossing) for crossing in pd]  # type: ignore[misc]
    perm = list(range(n_strands))
    for letter in word:
        i = abs(letter) - 1
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    seen: set[int] = set()
    components = 0
    for start in range(n_strands):
        if start not in seen:
            components += 1
            s = start
            while s not in seen:
                seen.add(s)
                s = perm[s]
    return KnotDiagram(pd, signs, components=components)


# name: (braid word, strands, determinant or None for links)
BRAIDS: dict[str, tuple[list[int], int]] = {
    "unknot_positive_kink": ([1], 2),
    "unknot_negative_kink": ([-1], 2),
    "unknot_two_crossings": ([1, 2], 3),
    "unlink_two_components": ([1, -1], 2),
    "trefoil": ([1, 1, 1], 2),
    "trefoil_mirror": ([-1, -1, -1], 2),
    "hopf_link": ([1, 1], 2),
    "figure_eight": ([1, -2, 1, -2], 3),
    "torus_link_2_4": ([1, 1, 1, 1], 2),
    "cinquefoil": ([1] * 5, 2),
    "5_2": ([1, 1, 1, 2, -1, 2], 3),
    "6_1": ([1, 1, 2, -1, -3, 2, -3], 4),
    "6_2": ([1, 1, 1, -2, 1, -2], 3),
    "6_3": ([1, 1, -2, 1, -2, -2], 3),
    "8_19": ([1, 2] * 4, 3),
    "8_19_mirror": ([-1, -2] * 4, 3),
    "8_20": ([1, 1, 1, -2, -1, -1, -1, -2], 3),
}

ALTERNATING_KNOT_DETERMINANTS = {
    "trefoil": 3,
    "trefoil_mirror": 3,
    "figure_eight": 5,
    "cinquefoil": 5,
    "5_2": 7,
    "6_1": 9,
    "6_2": 11,
    "6_3": 13,
}

UNKNOT = {(0, 1): (1, ()), (0, -1): (1, ())}


def diagram(name: str) -> KnotDiagram:
    word, strands = BRAIDS[name]
    return braid_diagram(word, strands)


# ---------------------------------------------------------------------------
# Helpers: GF(2) ranks, elementary divisors, the two-copy decomposition
# ---------------------------------------------------------------------------


def _gf2_rank(matrix: list[list[int]]) -> int:
    basis: dict[int, int] = {}
    for row in matrix:
        bits = 0
        for col, entry in enumerate(row):
            if entry % 2:
                bits |= 1 << col
        while bits:
            top = bits.bit_length() - 1
            if top not in basis:
                basis[top] = bits
                break
            bits ^= basis[top]
    return len(basis)


def _mod2_betti(elements: dict, differentials: dict) -> dict[tuple[int, int], int]:
    ranks = {key: _gf2_rank(matrix) for key, matrix in differentials.items()}
    betti = {}
    for (i, j), basis in elements.items():
        dim = len(basis) - ranks.get((i, j), 0) - ranks.get((i - 1, j), 0)
        if dim:
            betti[(i, j)] = dim
    return betti


def _prime_powers(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            q = 1
            while n % p == 0:
                n //= p
                q *= p
            out.append(q)
        p += 1
    if n > 1:
        out.append(n)
    return out


def _as_counter(group: tuple[int, tuple[int, ...]]) -> Counter:
    free, torsion = group
    counter: Counter = Counter({0: free}) if free else Counter()
    for d in torsion:
        counter.update(_prime_powers(d))
    return counter


def _two_copy_root(groups: dict) -> dict[tuple[int, int], Counter] | None:
    """Solve ``G_{m,s} ≅ R_{m,s-1} ⊕ R_{m,s+1}`` for ``R``; ``None`` if impossible."""

    root: dict[tuple[int, int], Counter] = {}
    for m in sorted({i for i, _ in groups}):
        column = {s: _as_counter(g) for (i, s), g in groups.items() if i == m}
        column = {s: c for s, c in column.items() if c}
        if not column:
            continue
        lo, hi = min(column), max(column)
        previous: Counter = Counter()  # R_{m, s-1}
        for s in range(lo, hi + 1, 2):
            current = column.get(s, Counter())
            if previous - current:  # R_{m,s-1} is not a summand of G_{m,s}
                return None
            remainder = current - previous
            if remainder:
                root[(m, s + 1)] = remainder
            previous = remainder
        if previous:  # R_{m, hi+1} would leak into G_{m, hi+2} = 0
            return None
    return root


def _shuffled(d: KnotDiagram, seed: int) -> KnotDiagram:
    rng = random.Random(seed)
    order = list(range(len(d.pd)))
    rng.shuffle(order)
    labels = sorted({x for c in d.pd for x in c})
    renamed = dict(zip(labels, rng.sample(range(1000, 1000 + len(labels)), len(labels)), strict=True))
    pd = [tuple(f"e{renamed[x]}" for x in d.pd[k]) for k in order]
    return KnotDiagram(pd, [d.signs[k] for k in order], components=d.components)


# ---------------------------------------------------------------------------
# Chain-level structure
# ---------------------------------------------------------------------------


def _columns(matrix: list[list[int]]) -> list[dict[int, int]]:
    cols: list[dict[int, int]] = [{} for _ in range(len(matrix[0]))]
    for r, row in enumerate(matrix):
        for c, entry in enumerate(row):
            if entry:
                cols[c][r] = entry
    return cols


@pytest.mark.parametrize("name", sorted(BRAIDS))
def test_differential_squares_to_zero(name: str) -> None:
    _, differentials = _odd_khovanov_complex(diagram(name))
    checked = 0
    for (i, j), first in differentials.items():
        second = differentials.get((i + 1, j))
        if not second:
            continue
        second_cols = _columns(second)
        for column in _columns(first):
            image: dict[int, int] = {}
            for t, coefficient in column.items():
                for r, entry in second_cols[t].items():
                    image[r] = image.get(r, 0) + coefficient * entry
            assert not any(image.values()), (name, i, j)
        checked += 1
    if len(diagram(name).pd) >= 2:
        assert checked > 0  # the composite was actually formed somewhere


@pytest.mark.parametrize("name", ["trefoil", "figure_eight", "6_1", "8_19", "8_20"])
def test_face_types_satisfy_ors_lemma_2_1(name: str) -> None:
    d = diagram(name)
    types = _cube_face_types(d)
    assert set(types.values()) <= {"A", "C", "X", "Y"}
    n = len(d.pd)
    for u in range(1 << n):
        for a, b, c in combinations(range(n), 3):
            if u >> a & 1 or u >> b & 1 or u >> c & 1:
                continue
            faces = []
            for (p, q), r in (((a, b), c), ((a, c), b), ((b, c), a)):
                faces.append(types[(u, p, q)])
                faces.append(types[(u | 1 << r, p, q)])
            count = Counter(faces)
            assert (count["A"] + count["X"]) % 2 == 0, (name, u, a, b, c, faces)
            assert (count["A"] + count["Y"]) % 2 == 0, (name, u, a, b, c, faces)


def test_ladybug_faces_occur_in_the_corpus() -> None:
    """Lemma 2.1 only constrains X/Y if ladybug faces actually appear."""

    types = Counter(_cube_face_types(diagram("8_19")).values())
    assert types["X"] + types["Y"] > 0


# ---------------------------------------------------------------------------
# Theorems relating odd and even Khovanov homology
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(BRAIDS))
def test_mod_2_reduction_equals_even_khovanov(name: str) -> None:
    from pytop.khovanov import _khovanov_complex

    d = diagram(name)
    assert _mod2_betti(*_odd_khovanov_complex(d)) == _mod2_betti(*_khovanov_complex(d))


@pytest.mark.parametrize("name", sorted(BRAIDS))
def test_compare_parities_reports_mod_2_agreement(name: str) -> None:
    d = diagram(name)
    result = compare_khovanov_parities(khovanov_homology(d), khovanov_homology_odd(d))
    assert result["agree_mod_2"] is True
    assert result["mod_2_differences"] == []


@pytest.mark.parametrize("name", sorted(BRAIDS))
def test_graded_euler_characteristic_is_the_jones_polynomial(name: str) -> None:
    d = diagram(name)
    odd = khovanov_homology_odd(d)
    even = khovanov_homology(d).graded_euler_characteristic()
    assert {j: c for j, c in odd.jones_graded_euler.items() if c} == even


@pytest.mark.parametrize("name", sorted(BRAIDS))
def test_unreduced_is_two_copies_of_reduced(name: str) -> None:
    assert _two_copy_root(khovanov_homology_odd(diagram(name)).groups) is not None


def test_even_khovanov_does_not_split_on_the_trefoil() -> None:
    """The splitting test is not vacuous: even Kh(trefoil) has ℤ/2 and fails it."""

    assert _two_copy_root(khovanov_homology(diagram("trefoil")).groups) is None


@pytest.mark.parametrize("name", sorted(ALTERNATING_KNOT_DETERMINANTS))
def test_alternating_knots_are_thin_free_and_of_rank_det(name: str) -> None:
    groups = khovanov_homology_odd(diagram(name)).groups
    assert all(not torsion for _, torsion in groups.values())
    root = _two_copy_root(groups)
    assert root is not None
    assert len({s - 2 * m for (m, s) in root}) == 1  # σ-thin: one diagonal
    assert sum(c[0] for c in root.values()) == ALTERNATING_KNOT_DETERMINANTS[name]


# ---------------------------------------------------------------------------
# Exact values
# ---------------------------------------------------------------------------


def test_trefoil_has_rank_six_and_no_torsion() -> None:
    """ORS §5: rank 6 for the trefoil, against rank 4 for even Khovanov."""

    kh = khovanov_homology_odd(diagram("trefoil"))
    assert kh.groups == {
        (0, 1): (1, ()),
        (0, 3): (1, ()),
        (2, 5): (1, ()),
        (2, 7): (1, ()),
        (3, 7): (1, ()),
        (3, 9): (1, ()),
    }
    assert kh.total_rank() == 6
    assert khovanov_homology(diagram("trefoil")).total_rank() == 4


def test_hopf_link() -> None:
    kh = khovanov_homology_odd(diagram("hopf_link"))
    assert kh.groups == {(0, 0): (1, ()), (0, 2): (1, ()), (2, 4): (1, ()), (2, 6): (1, ())}


@pytest.mark.parametrize(
    "name", ["unknot_positive_kink", "unknot_negative_kink", "unknot_two_crossings"]
)
def test_unknot_diagrams_give_the_unknot(name: str) -> None:
    assert khovanov_homology_odd(diagram(name)).groups == UNKNOT


def test_crossingless_unknot() -> None:
    assert khovanov_homology_odd(KnotDiagram(pd=(), signs=())).groups == UNKNOT


def test_8_19_matches_ors_rational_computation() -> None:
    """ORS §5: R(8_19) ⊗ ℚ = q^6 + q^10 t^2 + q^16 t^5 (rank 3; even has rank 5)."""

    odd = khovanov_homology_odd(diagram("8_19"))
    free = {key: free for key, (free, _) in odd.groups.items() if free}
    assert free == {(0, 5): 1, (0, 7): 1, (2, 9): 1, (2, 11): 1, (5, 15): 1, (5, 17): 1}
    assert khovanov_homology(diagram("8_19")).total_rank() == 8


# ---------------------------------------------------------------------------
# External oracle: KnotInfo's integral odd Khovanov homology
# ---------------------------------------------------------------------------

# Reduced odd Khovanov homology over ℤ of every prime knot with at most 8
# crossings, with KnotInfo's braid word for that knot, as published by KnotInfo
# (C. Livingston and A. H. Moore, https://knotinfo.org; database_knotinfo
# 2026.10.5, column khovanov_odd_integral_polynomial). ``t`` is the homological
# degree, ``q`` the quantum degree, and ``T^(k)`` marks a ℤ/k summand.
KNOTINFO_REDUCED_ODD: dict[str, tuple[list[int], str]] = {
    "3_1": (
        [1, 1, 1],
        "q^(2)+t^(2)*q^(6)+t^(3)*q^(8)",
    ),
    "4_1": (
        [1, -2, 1, -2],
        "t^(-2)*q^(-4)+t^(-1)*q^(-2)+1+t*q^(2)+t^(2)*q^(4)",
    ),
    "5_1": (
        [1, 1, 1, 1, 1],
        "q^(4)+t^(2)*q^(8)+t^(3)*q^(10)+t^(4)*q^(12)+t^(5)*q^(14)",
    ),
    "5_2": (
        [1, 1, 1, 2, -1, 2],
        "q^(2)+t*q^(4)+2*t^(2)*q^(6)+t^(3)*q^(8)+t^(4)*q^(10)+t^(5)*q^(12)",
    ),
    "6_1": (
        [1, 1, 2, -1, -3, 2, -3],
        "t^(-2)*q^(-4)+t^(-1)*q^(-2)+2+2*t*q^(2)+t^(2)*q^(4)+t^(3)*q^(6)+t^(4)*q^(8)",
    ),
    "6_2": (
        [1, 1, 1, -2, 1, -2],
        "t^(-2)*q^(-2)+t^(-1)+2*q^(2)+2*t*q^(4)+2*t^(2)*q^(6)+2*t^(3)*q^(8)+t^(4)*q^(10)",
    ),
    "6_3": (
        [1, 1, -2, 1, -2, -2],
        "t^(-3)*q^(-6)+2*t^(-2)*q^(-4)+2*t^(-1)*q^(-2)+3+2*t*q^(2)+2*t^(2)*q^(4)+t^(3)*q^(6)",
    ),
    "7_1": (
        [1, 1, 1, 1, 1, 1, 1],
        "q^(6)+t^(2)*q^(10)+t^(3)*q^(12)+t^(4)*q^(14)+t^(5)*q^(16)+t^(6)*q^(18)+t^(7)*q^(20)",
    ),
    "7_2": (
        [1, 1, 1, 2, -1, 2, 3, -2, 3],
        "q^(2)+t*q^(4)+2*t^(2)*q^(6)+2*t^(3)*q^(8)+2*t^(4)*q^(10)+t^(5)*q^(12)+t^(6)*q^(14)+t^(7)*q^(16)",
    ),
    "7_3": (
        [1, 1, 1, 1, 1, 2, -1, 2],
        "q^(4)+t*q^(6)+2*t^(2)*q^(8)+2*t^(3)*q^(10)+3*t^(4)*q^(12)+2*t^(5)*q^(14)+t^(6)*q^(16)+t^(7)*q^(18)",
    ),
    "7_4": (
        [1, 1, 2, -1, 2, 2, 3, -2, 3],
        "q^(2)+2*t*q^(4)+3*t^(2)*q^(6)+2*t^(3)*q^(8)+3*t^(4)*q^(10)+2*t^(5)*q^(12)+t^(6)*q^(14)+t^(7)*q^(16)",
    ),
    "7_5": (
        [1, 1, 1, 1, 2, -1, 2, 2],
        "q^(4)+t*q^(6)+3*t^(2)*q^(8)+3*t^(3)*q^(10)+3*t^(4)*q^(12)+3*t^(5)*q^(14)+2*t^(6)*q^(16)+t^(7)*q^(18)",
    ),
    "7_6": (
        [1, 1, -2, 1, 3, -2, 3],
        "t^(-2)*q^(-2)+2*t^(-1)+3*q^(2)+3*t*q^(4)+4*t^(2)*q^(6)+3*t^(3)*q^(8)+2*t^(4)*q^(10)+t^(5)*q^(12)",
    ),
    "7_7": (
        [-1, 2, -1, 2, -3, 2, -3],
        "t^(-4)*q^(-8)+2*t^(-3)*q^(-6)+3*t^(-2)*q^(-4)+4*t^(-1)*q^(-2)+4+3*t*q^(2)+3*t^(2)*q^(4)+t^(3)*q^(6)",
    ),
    "8_1": (
        [1, 1, 2, -1, 2, 3, -2, -4, 3, -4],
        "t^(-2)*q^(-4)+t^(-1)*q^(-2)+2+2*t*q^(2)+2*t^(2)*q^(4)+2*t^(3)*q^(6)+t^(4)*q^(8)+t^(5)*q^(10)+t^(6)*q^(12)",
    ),
    "8_2": (
        [1, 1, 1, 1, 1, -2, 1, -2],
        "t^(-2)+t^(-1)*q^(2)+2*q^(4)+2*t*q^(6)+3*t^(2)*q^(8)+3*t^(3)*q^(10)+2*t^(4)*q^(12)+2*t^(5)*q^(14)+t^(6)*q^(16)",
    ),
    "8_3": (
        [1, 1, 2, -1, -3, 2, -3, -4, 3, -4],
        "t^(-4)*q^(-8)+t^(-3)*q^(-6)+2*t^(-2)*q^(-4)+3*t^(-1)*q^(-2)+3+3*t*q^(2)+2*t^(2)*q^(4)+t^(3)*q^(6)+t^(4)*q^(8)",
    ),
    "8_4": (
        [-1, -1, -1, 2, -1, 2, 3, -2, 3],
        "t^(-4)*q^(-10)+2*t^(-3)*q^(-8)+3*t^(-2)*q^(-6)+3*t^(-1)*q^(-4)+3*q^(-2)+3*t+2*t^(2)*q^(2)+t^(3)*q^(4)+t^(4)*q^(6)",
    ),
    "8_5": (
        [1, 1, 1, -2, 1, 1, 1, -2],
        "t^(-2)+t^(-1)*q^(2)+3*q^(4)+3*t*q^(6)+3*t^(2)*q^(8)+4*t^(3)*q^(10)+3*t^(4)*q^(12)+2*t^(5)*q^(14)+t^(6)*q^(16)",
    ),
    "8_6": (
        [1, 1, 1, 1, 2, -1, -3, 2, -3],
        "t^(-2)*q^(-2)+t^(-1)+3*q^(2)+4*t*q^(4)+4*t^(2)*q^(6)+4*t^(3)*q^(8)+3*t^(4)*q^(10)+2*t^(5)*q^(12)+t^(6)*q^(14)",
    ),
    "8_7": (
        [-1, -1, -1, -1, 2, -1, 2, 2],
        "t^(-5)*q^(-12)+2*t^(-4)*q^(-10)+3*t^(-3)*q^(-8)+4*t^(-2)*q^(-6)+4*t^(-1)*q^(-4)+4*q^(-2)+2*t+2*t^(2)*q^(2)+t^(3)*q^(4)",
    ),
    "8_8": (
        [-1, -1, -1, -2, 1, 3, -2, 3, 3],
        "t^(-5)*q^(-10)+2*t^(-4)*q^(-8)+3*t^(-3)*q^(-6)+4*t^(-2)*q^(-4)+4*t^(-1)*q^(-2)+5+3*t*q^(2)+2*t^(2)*q^(4)+t^(3)*q^(6)",
    ),
    "8_9": (
        [1, 1, 1, -2, 1, -2, -2, -2],
        "t^(-4)*q^(-8)+2*t^(-3)*q^(-6)+3*t^(-2)*q^(-4)+4*t^(-1)*q^(-2)+5+4*t*q^(2)+3*t^(2)*q^(4)+2*t^(3)*q^(6)+t^(4)*q^(8)",
    ),
    "8_10": (
        [-1, -1, -1, 2, -1, -1, 2, 2],
        "t^(-5)*q^(-12)+2*t^(-4)*q^(-10)+4*t^(-3)*q^(-8)+5*t^(-2)*q^(-6)+4*t^(-1)*q^(-4)+5*q^(-2)+3*t+2*t^(2)*q^(2)+t^(3)*q^(4)",
    ),
    "8_11": (
        [1, 1, 2, -1, 2, 2, -3, 2, -3],
        "t^(-2)*q^(-2)+2*t^(-1)+4*q^(2)+4*t*q^(4)+5*t^(2)*q^(6)+5*t^(3)*q^(8)+3*t^(4)*q^(10)+2*t^(5)*q^(12)+t^(6)*q^(14)",
    ),
    "8_12": (
        [1, -2, 1, 3, -2, -4, 3, -4],
        "t^(-4)*q^(-8)+2*t^(-3)*q^(-6)+4*t^(-2)*q^(-4)+5*t^(-1)*q^(-2)+5+5*t*q^(2)+4*t^(2)*q^(4)+2*t^(3)*q^(6)+t^(4)*q^(8)",
    ),
    "8_13": (
        [1, 1, -2, 1, -2, -2, -3, 2, -3],
        "t^(-5)*q^(-10)+2*t^(-4)*q^(-8)+3*t^(-3)*q^(-6)+5*t^(-2)*q^(-4)+5*t^(-1)*q^(-2)+5+4*t*q^(2)+3*t^(2)*q^(4)+t^(3)*q^(6)",
    ),
    "8_14": (
        [1, 1, 1, 2, -1, 2, -3, 2, -3],
        "t^(-2)*q^(-2)+2*t^(-1)+4*q^(2)+5*t*q^(4)+6*t^(2)*q^(6)+5*t^(3)*q^(8)+4*t^(4)*q^(10)+3*t^(5)*q^(12)+t^(6)*q^(14)",
    ),
    "8_15": (
        [1, 1, -2, 1, 3, 2, 2, 2, 3],
        "q^(4)+2*t*q^(6)+5*t^(2)*q^(8)+5*t^(3)*q^(10)+6*t^(4)*q^(12)+6*t^(5)*q^(14)+4*t^(6)*q^(16)+3*t^(7)*q^(18)+t^(8)*q^(20)",
    ),
    "8_16": (
        [-1, -1, 2, -1, -1, 2, -1, 2],
        "t^(-5)*q^(-12)+3*t^(-4)*q^(-10)+5*t^(-3)*q^(-8)+6*t^(-2)*q^(-6)+6*t^(-1)*q^(-4)+6*q^(-2)+4*t+3*t^(2)*q^(2)+t^(3)*q^(4)",
    ),
    "8_17": (
        [1, 1, -2, 1, -2, 1, -2, -2],
        "t^(-4)*q^(-8)+3*t^(-3)*q^(-6)+5*t^(-2)*q^(-4)+6*t^(-1)*q^(-2)+7+6*t*q^(2)+5*t^(2)*q^(4)+3*t^(3)*q^(6)+t^(4)*q^(8)",
    ),
    "8_18": (
        [1, -2, 1, -2, 1, -2, 1, -2],
        "t^(-4)*q^(-8)+4*t^(-3)*q^(-6)+6*t^(-2)*q^(-4)+7*t^(-1)*q^(-2)+9+7*t*q^(2)+6*t^(2)*q^(4)+4*t^(3)*q^(6)+t^(4)*q^(8)",
    ),
    "8_19": (
        [1, 1, 1, 2, 1, 1, 1, 2],
        "q^(6)+t^(2)*q^(10)+t^(5)*q^(16)+t^(4)*q^(12)*T^(2)+t^(5)*q^(14)*T^(3)",
    ),
    "8_20": (
        [1, 1, 1, -2, -1, -1, -1, -2],
        "t^(-5)*q^(-10)+t^(-4)*q^(-8)+t^(-3)*q^(-6)+2*t^(-2)*q^(-4)+t^(-1)*q^(-2)+2+t*q^(2)",
    ),
    "8_21": (
        [1, 1, 1, 2, -1, -1, 2, 2],
        "2*q^(2)+2*t*q^(4)+3*t^(2)*q^(6)+3*t^(3)*q^(8)+2*t^(4)*q^(10)+2*t^(5)*q^(12)+t^(6)*q^(14)",
    ),
}


def _parse_knotinfo(polynomial: str) -> dict[tuple[int, int], Counter]:
    groups: dict[tuple[int, int], Counter] = {}
    for term in polynomial.split("+"):
        factors = term.split("*")
        multiplicity = int(factors.pop(0)) if factors[0].isdigit() and factors[0] != "1" else 1
        degree = {"t": 0, "q": 0, "T": 0}
        for factor in factors:
            if factor == "1":
                continue
            var, _, exponent = factor.partition("^")
            degree[var] = int(exponent.strip("()")) if exponent else 1
        summands = Counter(_prime_powers(degree["T"])) if degree["T"] else Counter({0: 1})
        bucket = groups.setdefault((degree["t"], degree["q"]), Counter())
        for summand, count in summands.items():
            bucket[summand] += count * multiplicity
    return groups


@pytest.mark.parametrize("name", sorted(KNOTINFO_REDUCED_ODD))
def test_matches_knotinfo_over_the_integers(name: str) -> None:
    """Unreduced = R{1} ⊕ R{-1} (ORS Prop. 1.7), compared summand by summand."""

    word, polynomial = KNOTINFO_REDUCED_ODD[name]
    expected: dict[tuple[int, int], Counter] = {}
    for (i, j), summands in _parse_knotinfo(polynomial).items():
        for shift in (-1, 1):
            expected.setdefault((i, j + shift), Counter()).update(summands)
    groups = khovanov_homology_odd(braid_diagram(word, max(map(abs, word)) + 1)).groups
    assert {key: _as_counter(group) for key, group in groups.items()} == expected


# KnotInfo's own PD codes: minimal diagrams rather than braid closures. Edges are
# numbered along the orientation, so X[i,j,k,l] is positive iff j - l = 1 (mod 2n).
KNOTINFO_PD: dict[str, list[list[int]]] = {
    "3_1": [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]],
    "4_1": [[4, 2, 5, 1], [8, 6, 1, 5], [6, 3, 7, 4], [2, 7, 3, 8]],
    "5_2": [[1, 5, 2, 4], [3, 9, 4, 8], [5, 1, 6, 10], [7, 3, 8, 2], [9, 7, 10, 6]],
    "7_4": [[2, 10, 3, 9], [4, 12, 5, 11], [6, 14, 7, 13], [8, 4, 9, 3], [10, 2, 11, 1],
            [12, 8, 13, 7], [14, 6, 1, 5]],
    "8_17": [[6, 2, 7, 1], [14, 8, 15, 7], [8, 3, 9, 4], [2, 13, 3, 14], [12, 5, 13, 6],
             [4, 9, 5, 10], [16, 12, 1, 11], [10, 16, 11, 15]],
    "8_19": [[2, 14, 3, 13], [5, 11, 6, 10], [7, 15, 8, 14], [9, 5, 10, 4], [11, 7, 12, 6],
             [12, 2, 13, 1], [15, 9, 16, 8], [16, 4, 1, 3]],
    "8_20": [[1, 7, 2, 6], [4, 13, 5, 14], [5, 9, 6, 8], [7, 3, 8, 2], [10, 15, 11, 16],
             [12, 9, 13, 10], [14, 3, 15, 4], [16, 11, 1, 12]],
    "8_21": [[1, 7, 2, 6], [4, 13, 5, 14], [5, 9, 6, 8], [7, 3, 8, 2], [9, 13, 10, 12],
             [11, 1, 12, 16], [14, 3, 15, 4], [15, 11, 16, 10]],
}


def _pd_signs(pd: list[list[int]]) -> list[int]:
    two_n = 2 * len(pd)
    return [1 if (second - fourth) % two_n == 1 else -1 for (_, second, _, fourth) in pd]


@pytest.mark.parametrize("name", sorted(KNOTINFO_PD))
def test_matches_knotinfo_on_its_own_pd_codes(name: str) -> None:
    pd = KNOTINFO_PD[name]
    expected: dict[tuple[int, int], Counter] = {}
    for (i, j), summands in _parse_knotinfo(KNOTINFO_REDUCED_ODD[name][1]).items():
        for shift in (-1, 1):
            expected.setdefault((i, j + shift), Counter()).update(summands)
    groups = khovanov_homology_odd(KnotDiagram([tuple(c) for c in pd], _pd_signs(pd))).groups
    assert {key: _as_counter(group) for key, group in groups.items()} == expected


def test_non_planar_pd_code_is_rejected() -> None:
    """Every label appears twice, but this code draws the curve on a torus
    (V - E + F = 0), so the ladybug arrows have no X/Y type."""

    torus = KnotDiagram([(2, 4, 3, 1), (3, 6, 5, 2), (5, 1, 6, 4)], [1, 1, 1])
    with pytest.raises(ValueError, match="not planar"):
        khovanov_homology_odd(torus)


def test_split_diagram_is_accepted() -> None:
    trefoil = KNOTINFO_PD["3_1"]
    figure_eight = [[x + 100 for x in c] for c in KNOTINFO_PD["4_1"]]
    split = KnotDiagram(
        [tuple(c) for c in trefoil + figure_eight],
        _pd_signs(trefoil) + _pd_signs(KNOTINFO_PD["4_1"]),
        components=2,
    )
    result = compare_khovanov_parities(khovanov_homology(split), khovanov_homology_odd(split))
    assert result["agree_mod_2"] is True


def test_accessors_report_the_8_19_torsion() -> None:
    """KnotInfo: reduced Kh'(8_19) has ℤ/2 at (4, 12) and ℤ/3 at (5, 14)."""

    kh = khovanov_homology_odd(braid_diagram(*BRAIDS["8_19"]))
    assert kh.torsion(4, 11) == kh.torsion(4, 13) == (2,)
    assert kh.torsion(5, 13) == kh.torsion(5, 15) == (3,)
    assert kh.betti(5, 15) == 1 and kh.betti(5, 13) == 0
    assert all(kh.euler_characteristic(j) == c for j, c in kh.jones_graded_euler.items())


def test_complex_builder_needs_a_crossing() -> None:
    with pytest.raises(ValueError, match="at least one crossing"):
        _odd_khovanov_complex(KnotDiagram(pd=(), signs=()))


def test_knotinfo_table_is_complete_through_eight_crossings() -> None:
    assert len(KNOTINFO_REDUCED_ODD) == 35  # 1 + 1 + 2 + 3 + 7 + 21 prime knots


# ---------------------------------------------------------------------------
# Invariance
# ---------------------------------------------------------------------------

EQUIVALENT_BRAIDS = [
    # Reidemeister I (Markov stabilisation, both signs)
    (([1, 1, 1], 2), ([1, 1, 1, 2], 3)),
    (([1, 1, 1], 2), ([1, 1, 1, -2], 3)),
    # Reidemeister II
    (([1, 1, 1], 2), ([1, 1, 1, 1, -1], 2)),
    (([1, -2, 1, -2], 3), ([1, 2, -2, -2, 1, -2], 3)),
    # Reidemeister III, positive and mixed
    (([1, 2, 1, 2, 1, 2, 1, 2], 3), ([2, 1, 2, 2, 1, 2, 1, 2], 3)),
    (([-2, 1, 2, 1, 1], 3), ([1, 2, -1, 1, 1], 3)),
    # conjugation: a different diagram of the same closure
    (([1, 2] * 4, 3), ([2, 1] * 4, 3)),
    (([1, -2, 1, -2], 3), ([-2, 1, -2, 1], 3)),
]


@pytest.mark.parametrize(("first", "second"), EQUIVALENT_BRAIDS)
def test_invariant_under_braid_moves(first: tuple, second: tuple) -> None:
    a = khovanov_homology_odd(braid_diagram(*first)).groups
    b = khovanov_homology_odd(braid_diagram(*second)).groups
    assert a == b


@pytest.mark.parametrize("name", ["trefoil", "figure_eight", "6_2", "8_19"])
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_invariant_under_crossing_order_and_labels(name: str, seed: int) -> None:
    d = diagram(name)
    assert khovanov_homology_odd(_shuffled(d, seed)).groups == khovanov_homology_odd(d).groups


@pytest.mark.parametrize("name", ["trefoil", "figure_eight", "5_2", "6_2"])
def test_mirror_reverses_free_bigradings_of_alternating_knots(name: str) -> None:
    """For alternating knots this follows from σ-thinness, freeness and V(m(K))(t) = V(K)(1/t).

    No general mirror duality for odd Khovanov homology is assumed here.
    """
    word, strands = BRAIDS[name]
    kh = khovanov_homology_odd(braid_diagram(word, strands)).groups
    mirror = khovanov_homology_odd(braid_diagram([-x for x in word], strands)).groups
    free = {key: f for key, (f, _) in kh.items() if f}
    free_mirror = {(-i, -j): f for (i, j), (f, _) in mirror.items() if f}
    assert free == free_mirror


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_edge_label_used_once_is_rejected() -> None:
    with pytest.raises(ValueError, match="exactly twice"):
        khovanov_homology_odd(KnotDiagram([(1, 2, 3, 4)], [1]))
