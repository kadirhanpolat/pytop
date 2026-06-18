"""Seifert–van Kampen theorem: π₁ of a union via amalgamated free product.

Given X = A ∪ B where A, B, A∩B are path-connected and the inclusions are
basepoint-preserving, the Seifert–van Kampen theorem states

    π₁(X, x₀) ≅ π₁(A, x₀) *_{π₁(A∩B, x₀)} π₁(B, x₀)

the amalgamated free product over π₁(A∩B, x₀).

In terms of presentations: if
    π₁(A) = ⟨S_A | R_A⟩,
    π₁(B) = ⟨S_B | R_B⟩,
    π₁(A∩B) = ⟨T | Q⟩,
    φ_A : π₁(A∩B) → π₁(A),   φ_B : π₁(A∩B) → π₁(B)  (inclusion-induced),
then
    π₁(X) = ⟨S_A ∪ S_B | R_A ∪ R_B ∪ {φ_A(t)φ_B(t)⁻¹ : t ∈ T}⟩.

This module also supports the CW-complex route: given a finite connected CW
complex with explicit 1-skeleton and 2-cell attaching maps, it computes π₁
directly from a maximal spanning tree (standard algorithm).

Public API
----------
GroupPresentation    — finite group presentation ⟨S | R⟩
GroupHomomorphism    — source, target, generator images as words
VanKampenResult      — raw + simplified presentation, abelianization, group type

van_kampen(...)      — amalgamated free product from two presentations + maps
group_homomorphism(source, target, images)  — convenience constructor

cw_complex_pi1(cw)  — π₁ from a finite CW complex with attaching words

trivial_group()                 — ⟨ | ⟩ = {1}
infinite_cyclic_group(gen)      — ⟨a | ⟩ = ℤ
free_group(*gens)               — ⟨a, b, … | ⟩ = Fₙ
cyclic_group(n, gen)            — ⟨a | aⁿ⟩ = ℤ/nℤ
surface_group(g)                — orientable genus g
surface_group_nr(n)             — non-orientable, n crosscaps

van_kampen_wedge_circles(n)     — S¹ ∨ ⋯ ∨ S¹  → Fₙ
van_kampen_sphere()             — S² via two hemispheres  → trivial
van_kampen_torus()              — T² → ⟨a,b | aba⁻¹b⁻¹⟩
van_kampen_klein_bottle()       — Klein bottle → ⟨a,b | abab⁻¹⟩
van_kampen_real_projective_plane()  — RP² → ⟨a | a²⟩
"""
from __future__ import annotations

from dataclasses import dataclass

from .homology import HomologyResult, _smith_normal_form

# ── Type aliases ──────────────────────────────────────────────────────────────

# A Letter is (generator_name, exponent); exponent is a nonzero integer.
Letter = tuple[str, int]
# A Word is an immutable sequence of Letters in a free group.
Word = tuple[Letter, ...]


# ── Word arithmetic ───────────────────────────────────────────────────────────

def _free_reduce(word: Word) -> Word:
    """Cancel adjacent inverse letters and merge same-generator letters."""
    stack: list[Letter] = []
    for gen, exp in word:
        if exp == 0:
            continue
        if stack and stack[-1][0] == gen:
            total = stack[-1][1] + exp
            stack.pop()
            if total != 0:
                stack.append((gen, total))
        else:
            stack.append((gen, exp))
    return tuple(stack)


def _invert(word: Word) -> Word:
    return tuple((g, -e) for g, e in reversed(word))


def _concat(*words: Word) -> Word:
    result: list[Letter] = []
    for w in words:
        result.extend(w)
    return _free_reduce(tuple(result))


def _substitute(word: Word, gen: str, replacement: Word) -> Word:
    """Replace every occurrence of ``gen^e`` with ``replacement^e``."""
    result: list[Letter] = []
    inv_rep = _invert(replacement)
    for g, e in word:
        if g != gen:
            result.append((g, e))
        elif e > 0:
            for _ in range(e):
                result.extend(replacement)
        else:
            for _ in range(-e):
                result.extend(inv_rep)
    return _free_reduce(tuple(result))


def _word_to_str(word: Word) -> str:
    if not word:
        return "1"
    parts = []
    for g, e in word:
        if e == 1:
            parts.append(g)
        elif e == -1:
            parts.append(f"{g}^(-1)")
        else:
            parts.append(f"{g}^{e}")
    return "".join(parts)


# ── GroupPresentation ─────────────────────────────────────────────────────────

class GroupPresentationError(ValueError):
    """Raised when a group presentation or homomorphism is malformed."""


@dataclass(frozen=True)
class GroupPresentation:
    """A finite group presentation ⟨S | R⟩.

    Parameters
    ----------
    generators:
        Tuple of generator names.  Names must be nonempty and distinct.
    relators:
        Tuple of Words; each word represents an element set equal to the
        identity (a relator, not a relation).
    """

    generators: tuple[str, ...]
    relators: tuple[Word, ...]

    def __post_init__(self) -> None:
        if len(set(self.generators)) != len(self.generators):
            raise GroupPresentationError("Generator names must be distinct.")
        for g in self.generators:
            if not g:
                raise GroupPresentationError("Generator names must be nonempty.")
        gen_set = set(self.generators)
        for rel in self.relators:
            for g, _ in rel:
                if g not in gen_set:
                    raise GroupPresentationError(
                        f"Relator references unknown generator {g!r}."
                    )

    @property
    def rank(self) -> int:
        return len(self.generators)

    @property
    def is_free(self) -> bool:
        return not self.relators

    def presentation_string(self) -> str:
        gens = ", ".join(self.generators) if self.generators else "—"
        rels = (
            ", ".join(_word_to_str(r) for r in self.relators)
            if self.relators
            else "—"
        )
        return f"< {gens} | {rels} >"


# ── GroupHomomorphism ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class GroupHomomorphism:
    """A group homomorphism specified by generator images.

    Parameters
    ----------
    source:
        Domain presentation.
    target:
        Codomain presentation.
    images:
        Tuple of ``(source_gen, target_word)`` pairs — one entry per
        source generator.
    """

    source: GroupPresentation
    target: GroupPresentation
    images: tuple[tuple[str, Word], ...]

    def __post_init__(self) -> None:
        image_dict = dict(self.images)
        for g in self.source.generators:
            if g not in image_dict:
                raise GroupPresentationError(
                    f"No image defined for source generator {g!r}."
                )
        tgt_gens = set(self.target.generators)
        for g, w in self.images:
            for h, _ in w:
                if h not in tgt_gens:
                    raise GroupPresentationError(
                        f"Image of {g!r} uses {h!r} which is not in the target."
                    )

    def image_of(self, gen: str) -> Word:
        return dict(self.images)[gen]

    def apply(self, word: Word) -> Word:
        """Extend φ homomorphically to a word."""
        result: list[Letter] = []
        for g, e in word:
            img = self.image_of(g)
            inv_img = _invert(img)
            if e > 0:
                for _ in range(e):
                    result.extend(img)
            else:
                for _ in range(-e):
                    result.extend(inv_img)
        return _free_reduce(tuple(result))


def group_homomorphism(
    source: GroupPresentation,
    target: GroupPresentation,
    images: dict[str, Word],
) -> GroupHomomorphism:
    """Convenience constructor: build a :class:`GroupHomomorphism` from a dict."""
    return GroupHomomorphism(
        source=source,
        target=target,
        images=tuple(images.items()),
    )


# ── Tietze simplification ─────────────────────────────────────────────────────

def _tietze_eliminate_once(
    gens: list[str],
    rels: list[Word],
) -> tuple[list[str], list[Word], bool]:
    """One Tietze-II move: eliminate a generator that appears exactly once.

    Scans every relator for a generator ``g`` with a single occurrence and
    exponent ±1.  Solves ``g = w`` (a word in the remaining generators) and
    substitutes throughout.  Returns ``(new_gens, new_rels, changed)``.
    """
    for i, rel in enumerate(rels):
        counts: dict[str, int] = {}
        for g, e in rel:
            counts[g] = counts.get(g, 0) + abs(e)
        candidates = [g for g, c in counts.items() if c == 1]
        if not candidates:
            continue
        g_elim = candidates[0]
        pos = next(k for k, (g, _) in enumerate(rel) if g == g_elim)
        g_name, e = rel[pos]
        prefix = rel[:pos]
        suffix = rel[pos + 1:]
        if e == 1:
            # g · rest = 1  →  g = invert(prefix)⁻¹ · invert(suffix)
            replacement = _free_reduce(_invert(prefix) + _invert(suffix))
        else:
            # g⁻¹ · rest = 1  →  g = suffix · prefix (rearranged)
            replacement = _free_reduce(tuple(suffix) + tuple(prefix))
        if any(h == g_elim for h, _ in replacement):
            continue
        new_rels = []
        for j, r in enumerate(rels):
            if j == i:
                continue
            nr = _substitute(r, g_elim, replacement)
            if nr:
                new_rels.append(nr)
        new_gens = [g for g in gens if g != g_elim]
        return new_gens, new_rels, True
    return gens, rels, False


def _cyclically_reduce(word: Word) -> Word:
    """Remove prefix/suffix letter pairs that are mutual inverses.

    A relator ``r`` and any cyclic conjugate ``g·r·g⁻¹`` define the same
    normal subgroup element, so we may freely cyclically reduce.  Repeated
    until the first and last letters are not mutual inverses.
    """
    w = list(word)
    changed = True
    while changed and len(w) >= 2:
        changed = False
        if w[0][0] == w[-1][0] and w[0][1] + w[-1][1] == 0:
            w = w[1:-1]
            changed = True
    return _free_reduce(tuple(w))


def _canonical_relator_key(rel: Word) -> Word:
    """Canonical key for a relator: min over all cyclic conjugates and their inverses.

    Used to detect duplicate relators up to cyclic conjugation and inversion.
    """
    if not rel:
        return rel
    n = len(rel)
    conjugates = [rel[i:] + rel[:i] for i in range(n)]
    inv = _invert(rel)
    inv_conj = [inv[i:] + inv[:i] for i in range(n)]
    return min(conjugates + inv_conj)


def _dedup_relators(rels: list[Word]) -> list[Word]:
    """Remove duplicate relators up to cyclic conjugation and inversion (Tietze I)."""
    seen: set[Word] = set()
    result: list[Word] = []
    for rel in rels:
        key = _canonical_relator_key(rel)
        if key not in seen:
            seen.add(key)
            result.append(rel)
    return result


def _tietze_simplify(
    gens: list[str],
    rels: list[Word],
    *,
    max_rounds: int = 64,
) -> tuple[list[str], list[Word]]:
    """Iteratively simplify a group presentation using Tietze moves.

    Steps applied each round:
    1. Free-reduce and cyclically reduce every relator.
    2. Remove trivial (empty) relators.
    3. Deduplicate relators up to cyclic conjugation and inversion.
    4. Eliminate one generator that appears exactly once in some relator
       (Tietze II elimination).
    """
    def _clean(rs: list[Word]) -> list[Word]:
        rs = [_cyclically_reduce(r) for r in rs]
        rs = [r for r in rs if r]
        return _dedup_relators(rs)

    rels = _clean(rels)
    for _ in range(max_rounds):
        gens, rels, changed = _tietze_eliminate_once(gens, rels)
        rels = _clean(rels)
        if not changed:
            break
    return gens, rels


# ── Abelianization ────────────────────────────────────────────────────────────

def _abelianize(gens: list[str], rels: list[Word]) -> HomologyResult:
    """Compute H₁ = π₁^{ab} via Smith Normal Form of the relation matrix."""
    n = len(gens)
    if n == 0:
        return HomologyResult(degree=1, betti=0, torsion=())
    gen_idx = {g: j for j, g in enumerate(gens)}
    rows = []
    for rel in rels:
        row = [0] * n
        for g, e in rel:
            if g in gen_idx:
                row[gen_idx[g]] += e
        rows.append(row)
    if not rows:
        return HomologyResult(degree=1, betti=n, torsion=())
    factors = _smith_normal_form(rows)
    rank = len(factors)
    torsion = tuple(d for d in factors if d > 1)
    free_rank = max(n - rank, 0)
    return HomologyResult(degree=1, betti=free_rank, torsion=torsion)


# ── Group identification ──────────────────────────────────────────────────────

def _identify_group(gens: list[str], rels: list[Word]) -> str:
    """Identify the presentation as a named group, or return 'unknown'."""
    n = len(gens)
    r = len(rels)

    if n == 0:
        return "trivial"
    if r == 0:
        return "infinite_cyclic" if n == 1 else f"free_rank_{n}"

    # Single generator with one relator: cyclic group
    if n == 1 and r == 1:
        rel = rels[0]
        total_exp = sum(e for _, e in rel)
        if all(g == gens[0] for g, _ in rel) and total_exp > 0:
            return f"cyclic_{total_exp}"

    # Surface groups: 2g generators, one commutator-product relator
    if r == 1 and n >= 2 and n % 2 == 0:
        g = n // 2
        expected_rel: list[Letter] = []
        for i in range(1, g + 1):
            expected_rel += [(f"a{i}", 1), (f"b{i}", 1), (f"a{i}", -1), (f"b{i}", -1)]
        if (
            list(gens) == [s for i in range(1, g + 1) for s in (f"a{i}", f"b{i}")]
            and rels[0] == tuple(expected_rel)
        ):
            return "free_abelian_rank_2" if g == 1 else f"surface_group_orientable_genus_{g}"

    # Non-orientable surface groups: n generators, relator a₁²⋯aₙ²
    if r == 1:
        expected_nr: list[Letter] = [(f"a{i}", 2) for i in range(1, n + 1)]
        if (
            list(gens) == [f"a{i}" for i in range(1, n + 1)]
            and rels[0] == tuple(expected_nr)
        ):
            return f"surface_group_non_orientable_{n}"

    # Klein bottle: ⟨a,b | abab⁻¹⟩ or ⟨a,b | aba⁻¹b⟩
    if n == 2 and r == 1:
        a, b = gens
        rel = rels[0]
        if rel in (
            ((a, 1), (b, 1), (a, 1), (b, -1)),
            ((a, 1), (b, 1), (a, -1), (b, 1)),
        ):
            return "klein_bottle_group"

    return "unknown"


# ── VanKampenResult ───────────────────────────────────────────────────────────

@dataclass
class VanKampenResult:
    """Result of the Seifert–van Kampen computation.

    Attributes
    ----------
    generators:
        Generators of the raw amalgamated free product.
    relators:
        Relators of the raw presentation.
    simplified_generators:
        Generators after Tietze elimination.
    simplified_relators:
        Relators after Tietze elimination.
    abelianization:
        H₁ = π₁^{ab} from the simplified presentation.
    group_type:
        Identifier string: ``"trivial"``, ``"infinite_cyclic"``,
        ``"free_rank_n"``, ``"cyclic_n"``, ``"abelian_Z2"``,
        ``"surface_group_orientable_genus_g"``,
        ``"surface_group_non_orientable_n"``,
        ``"klein_bottle_group"``, ``"unknown"``.
    notes:
        Human-readable notes about the computation steps.
    """

    generators: tuple[str, ...]
    relators: tuple[Word, ...]
    simplified_generators: tuple[str, ...]
    simplified_relators: tuple[Word, ...]
    abelianization: HomologyResult
    group_type: str
    notes: tuple[str, ...]

    def presentation_string(self) -> str:
        """Simplified presentation as a string."""
        gens = ", ".join(self.simplified_generators) if self.simplified_generators else "—"
        rels = (
            ", ".join(_word_to_str(r) for r in self.simplified_relators)
            if self.simplified_relators
            else "—"
        )
        return f"< {gens} | {rels} >"

    def raw_presentation_string(self) -> str:
        """Raw (unsimplified) presentation as a string."""
        gens = ", ".join(self.generators) if self.generators else "—"
        rels = (
            ", ".join(_word_to_str(r) for r in self.relators)
            if self.relators
            else "—"
        )
        return f"< {gens} | {rels} >"


# ── Main van Kampen function ──────────────────────────────────────────────────

def van_kampen(
    pi1_A: GroupPresentation,
    pi1_B: GroupPresentation,
    pi1_intersection: GroupPresentation,
    phi_A: GroupHomomorphism,
    phi_B: GroupHomomorphism,
    *,
    simplify: bool = True,
) -> VanKampenResult:
    """Compute π₁(A ∪ B) via the Seifert–van Kampen theorem.

    Parameters
    ----------
    pi1_A:
        Presentation of π₁(A).
    pi1_B:
        Presentation of π₁(B).  **Generator names must be disjoint from
        pi1_A's generators.**
    pi1_intersection:
        Presentation of π₁(A ∩ B).
    phi_A:
        Homomorphism π₁(A ∩ B) → π₁(A) induced by the inclusion A ∩ B ↪ A.
    phi_B:
        Homomorphism π₁(A ∩ B) → π₁(B) induced by the inclusion A ∩ B ↪ B.
    simplify:
        Apply Tietze elimination to the raw presentation (default True).

    Returns
    -------
    VanKampenResult
        Raw and simplified presentations, abelianization, and group type.
    """
    common = set(pi1_A.generators) & set(pi1_B.generators)
    if common:
        raise GroupPresentationError(
            f"Generator name collision between π₁(A) and π₁(B): {common!r}. "
            "Rename generators before calling van_kampen()."
        )

    raw_gens = list(pi1_A.generators) + list(pi1_B.generators)
    raw_rels = list(pi1_A.relators) + list(pi1_B.relators)

    amalgam_rels: list[Word] = []
    for t in pi1_intersection.generators:
        img_A = phi_A.apply(((t, 1),))
        img_B = phi_B.apply(((t, 1),))
        rel = _concat(img_A, _invert(img_B))
        if rel:
            amalgam_rels.append(rel)

    raw_rels.extend(amalgam_rels)

    notes = [
        f"π₁(A)   = {pi1_A.presentation_string()}",
        f"π₁(B)   = {pi1_B.presentation_string()}",
        f"π₁(A∩B) = {pi1_intersection.presentation_string()}",
        f"{len(amalgam_rels)} amalgam relator(s) added.",
    ]

    if simplify:
        simp_gens, simp_rels = _tietze_simplify(list(raw_gens), list(raw_rels))
        notes.append(
            f"Tietze: {len(raw_gens)}→{len(simp_gens)} generator(s), "
            f"{len(raw_rels)}→{len(simp_rels)} relator(s)."
        )
    else:
        simp_gens, simp_rels = list(raw_gens), list(raw_rels)

    ab = _abelianize(simp_gens, simp_rels)
    group_type = _identify_group(simp_gens, simp_rels)

    return VanKampenResult(
        generators=tuple(raw_gens),
        relators=tuple(raw_rels),
        simplified_generators=tuple(simp_gens),
        simplified_relators=tuple(simp_rels),
        abelianization=ab,
        group_type=group_type,
        notes=tuple(notes),
    )


# ── CW complex → π₁ ──────────────────────────────────────────────────────────

@dataclass(frozen=True)
class DirectedEdge:
    """A 1-cell with explicit source and target vertices."""

    name: str
    src: str
    tgt: str


@dataclass(frozen=True)
class Face2:
    """A 2-cell with an attaching word in the 1-skeleton.

    ``attaching_word`` is a tuple of ``(edge_name, sign)`` pairs where
    sign ∈ {+1, −1} indicates the traversal direction.
    """

    name: str
    attaching_word: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class CW1Complex:
    """A finite connected CW complex with explicit attaching data up to dim 2.

    Parameters
    ----------
    vertices:
        Frozenset of vertex names (0-cells).
    edges:
        Tuple of :class:`DirectedEdge` objects (1-cells).
    faces:
        Tuple of :class:`Face2` objects (2-cells).
    basepoint:
        The chosen basepoint vertex.  If ``None``, the lexicographically
        smallest vertex is used.
    """

    vertices: frozenset[str]
    edges: tuple[DirectedEdge, ...]
    faces: tuple[Face2, ...]
    basepoint: str | None = None

    def _get_basepoint(self) -> str:
        return self.basepoint if self.basepoint is not None else min(self.vertices)


def _bfs_spanning_tree(
    vertices: frozenset[str],
    edges: tuple[DirectedEdge, ...],
    root: str,
) -> set[str]:
    """BFS spanning tree; returns the set of edge names that form the tree."""
    adj: dict[str, list[tuple[str, str]]] = {v: [] for v in vertices}
    for e in edges:
        adj[e.src].append((e.name, e.tgt))
        adj[e.tgt].append((e.name, e.src))
    visited = {root}
    tree: set[str] = set()
    queue = [root]
    while queue:
        v = queue.pop(0)
        for ename, w in adj[v]:
            if w not in visited:
                visited.add(w)
                tree.add(ename)
                queue.append(w)
    return tree


def cw_complex_pi1(cw: CW1Complex) -> GroupPresentation:
    """Compute π₁(cw) from a :class:`CW1Complex`.

    Algorithm:
    1. BFS spanning tree T in the 1-skeleton.
    2. Generators = {edge names not in T}.
    3. Each 2-cell gives one relator: traverse the attaching word, keeping
       non-tree edges as letters and discarding tree edges (= identity).
    """
    root = cw._get_basepoint()
    tree = _bfs_spanning_tree(cw.vertices, cw.edges, root)
    num_vertices = len(cw.vertices)
    if len(tree) + 1 < num_vertices:
        raise ValueError(
            "1-skeleton is disconnected; π₁ via spanning tree requires a "
            "connected 1-skeleton."
        )
    gen_names = tuple(e.name for e in cw.edges if e.name not in tree)
    gen_set = set(gen_names)
    relators: list[Word] = []
    for face in cw.faces:
        letters: list[Letter] = []
        for ename, sign in face.attaching_word:
            if ename in gen_set:
                letters.append((ename, sign))
        rel = _free_reduce(tuple(letters))
        if rel:
            relators.append(rel)
    return GroupPresentation(generators=gen_names, relators=tuple(relators))


# ── Standard group constructors ───────────────────────────────────────────────

def trivial_group() -> GroupPresentation:
    """Return the trivial group presentation ⟨ | ⟩."""
    return GroupPresentation(generators=(), relators=())


def infinite_cyclic_group(gen: str = "t") -> GroupPresentation:
    """Return ⟨gen | ⟩ ≅ ℤ."""
    return GroupPresentation(generators=(gen,), relators=())


def free_group(*gens: str) -> GroupPresentation:
    """Return ⟨gens | ⟩ ≅ Fₙ."""
    if not gens:
        return trivial_group()
    return GroupPresentation(generators=tuple(gens), relators=())


def cyclic_group(n: int, gen: str = "a") -> GroupPresentation:
    """Return ⟨gen | gen^n⟩ ≅ ℤ/nℤ.  Requires n ≥ 1."""
    if n < 1:
        raise GroupPresentationError(f"Cyclic group order must be ≥ 1, got {n}.")
    if n == 1:
        return GroupPresentation(generators=(gen,), relators=(((gen, 1),),))
    return GroupPresentation(generators=(gen,), relators=(((gen, n),),))


def surface_group(g: int) -> GroupPresentation:
    """Return the fundamental group of the orientable surface Σ_g.

    Presentation: ⟨a₁,b₁,…,aₘ,bₘ | [a₁,b₁]⋯[aₘ,bₘ]⟩.
    """
    if g < 0:
        raise GroupPresentationError(f"Genus must be ≥ 0, got {g}.")
    if g == 0:
        return trivial_group()
    gens = tuple(s for i in range(1, g + 1) for s in (f"a{i}", f"b{i}"))
    relator: list[Letter] = []
    for i in range(1, g + 1):
        relator += [(f"a{i}", 1), (f"b{i}", 1), (f"a{i}", -1), (f"b{i}", -1)]
    return GroupPresentation(generators=gens, relators=(tuple(relator),))


def surface_group_nr(n: int) -> GroupPresentation:
    """Return the fundamental group of the non-orientable surface Nₙ.

    Presentation: ⟨a₁,…,aₙ | a₁²⋯aₙ²⟩.
    """
    if n < 1:
        raise GroupPresentationError(f"Non-orientable surface requires n ≥ 1, got {n}.")
    gens = tuple(f"a{i}" for i in range(1, n + 1))
    relator: list[Letter] = [(f"a{i}", 2) for i in range(1, n + 1)]
    return GroupPresentation(generators=gens, relators=(tuple(relator),))


# ── Standard van Kampen decompositions ────────────────────────────────────────

def van_kampen_wedge_circles(n: int) -> VanKampenResult:
    """π₁(S¹ ∨ ⋯ ∨ S¹) = Fₙ via iterated free product.

    Decomposition: X = A ∪ B where A carries n−1 circles, B carries one,
    and A ∩ B = basepoint (trivial intersection).  Iterated n−1 times.
    """
    if n < 1:
        raise GroupPresentationError(f"Need at least 1 circle, got {n}.")
    trivial = trivial_group()
    if n == 1:
        pi1 = infinite_cyclic_group("a1")
        ab = _abelianize(list(pi1.generators), list(pi1.relators))
        return VanKampenResult(
            generators=pi1.generators,
            relators=pi1.relators,
            simplified_generators=pi1.generators,
            simplified_relators=pi1.relators,
            abelianization=ab,
            group_type="infinite_cyclic",
            notes=("S¹: one circle, π₁ = ℤ.",),
        )
    # Build Fₙ iteratively
    result_gens = [f"a{i}" for i in range(1, n + 1)]
    pi1_A = free_group(*result_gens[:-1])
    pi1_B = free_group(result_gens[-1])
    phi_A = group_homomorphism(trivial, pi1_A, {})
    phi_B = group_homomorphism(trivial, pi1_B, {})
    base = van_kampen(pi1_A, pi1_B, trivial, phi_A, phi_B)
    return VanKampenResult(
        generators=base.generators,
        relators=base.relators,
        simplified_generators=base.simplified_generators,
        simplified_relators=base.simplified_relators,
        abelianization=base.abelianization,
        group_type=f"free_rank_{n}",
        notes=(f"S¹ ∨ ⋯ ∨ S¹ ({n} circles): π₁ = F_{n}.",) + base.notes,
    )


def van_kampen_sphere() -> VanKampenResult:
    """π₁(S²) = trivial via two-hemisphere decomposition.

    A = upper hemisphere (contractible), B = lower hemisphere (contractible),
    A ∩ B = equator ≅ S¹.  Both inclusions send the equator to identity.
    """
    trivial = trivial_group()
    S1 = infinite_cyclic_group("c")
    phi_A = group_homomorphism(S1, trivial, {"c": ()})
    phi_B = group_homomorphism(S1, trivial, {"c": ()})
    base = van_kampen(trivial, trivial, S1, phi_A, phi_B)
    return VanKampenResult(
        generators=base.generators,
        relators=base.relators,
        simplified_generators=base.simplified_generators,
        simplified_relators=base.simplified_relators,
        abelianization=base.abelianization,
        group_type="trivial",
        notes=("S²: π₁ = trivial (both hemispheres contractible).",) + base.notes,
    )


def van_kampen_torus() -> VanKampenResult:
    """π₁(T²) = ⟨a,b | aba⁻¹b⁻¹⟩ ≅ ℤ² via standard decomposition.

    A = T² minus a small open disk ≃ S¹ ∨ S¹, π₁(A) = F₂ = ⟨a,b | ⟩.
    B = open disk (contractible), π₁(B) = trivial.
    A ∩ B = annulus ≃ S¹, π₁(A∩B) = ℤ = ⟨c | ⟩.
    φ_A(c) = aba⁻¹b⁻¹  (the boundary circle in A = the commutator).
    φ_B(c) = identity   (c bounds a disk in B).
    """
    pi1_A = free_group("a", "b")
    trivial = trivial_group()
    S1 = infinite_cyclic_group("c")
    commutator: Word = (("a", 1), ("b", 1), ("a", -1), ("b", -1))
    phi_A = group_homomorphism(S1, pi1_A, {"c": commutator})
    phi_B = group_homomorphism(S1, trivial, {"c": ()})
    base = van_kampen(pi1_A, trivial, S1, phi_A, phi_B)
    return VanKampenResult(
        generators=base.generators,
        relators=base.relators,
        simplified_generators=base.simplified_generators,
        simplified_relators=base.simplified_relators,
        abelianization=base.abelianization,
        group_type="free_abelian_rank_2",
        notes=("T²: π₁ = ⟨a,b | aba⁻¹b⁻¹⟩ ≅ ℤ².",) + base.notes,
    )


def van_kampen_klein_bottle() -> VanKampenResult:
    """π₁(Klein bottle) = ⟨a,b | abab⁻¹⟩ via standard decomposition.

    Same structure as the torus but the boundary word is abab⁻¹.
    """
    pi1_A = free_group("a", "b")
    trivial = trivial_group()
    S1 = infinite_cyclic_group("c")
    boundary: Word = (("a", 1), ("b", 1), ("a", 1), ("b", -1))
    phi_A = group_homomorphism(S1, pi1_A, {"c": boundary})
    phi_B = group_homomorphism(S1, trivial, {"c": ()})
    base = van_kampen(pi1_A, trivial, S1, phi_A, phi_B)
    return VanKampenResult(
        generators=base.generators,
        relators=base.relators,
        simplified_generators=base.simplified_generators,
        simplified_relators=base.simplified_relators,
        abelianization=base.abelianization,
        group_type="klein_bottle_group",
        notes=("Klein bottle: π₁ = ⟨a,b | abab⁻¹⟩.",) + base.notes,
    )


def van_kampen_real_projective_plane() -> VanKampenResult:
    """π₁(RP²) = ⟨a | a²⟩ ≅ ℤ/2ℤ via Möbius-band decomposition.

    A = RP² minus an open disk ≃ Möbius band, π₁(A) = ℤ = ⟨a | ⟩.
    B = open disk (contractible), π₁(B) = trivial.
    A ∩ B = annulus ≃ S¹, π₁(A∩B) = ℤ = ⟨c | ⟩.
    φ_A(c) = a²  (boundary of Möbius band wraps around twice).
    φ_B(c) = identity.
    """
    pi1_A = infinite_cyclic_group("a")
    trivial = trivial_group()
    S1 = infinite_cyclic_group("c")
    phi_A = group_homomorphism(S1, pi1_A, {"c": (("a", 2),)})
    phi_B = group_homomorphism(S1, trivial, {"c": ()})
    base = van_kampen(pi1_A, trivial, S1, phi_A, phi_B)
    return VanKampenResult(
        generators=base.generators,
        relators=base.relators,
        simplified_generators=base.simplified_generators,
        simplified_relators=base.simplified_relators,
        abelianization=base.abelianization,
        group_type="cyclic_2",
        notes=("RP²: π₁ = ⟨a | a²⟩ ≅ ℤ/2ℤ.",) + base.notes,
    )


# ── Public API ────────────────────────────────────────────────────────────────

__all__ = [
    # Types
    "Letter",
    "Word",
    "GroupPresentationError",
    "GroupPresentation",
    "GroupHomomorphism",
    "VanKampenResult",
    "DirectedEdge",
    "Face2",
    "CW1Complex",
    # Constructors
    "group_homomorphism",
    "trivial_group",
    "infinite_cyclic_group",
    "free_group",
    "cyclic_group",
    "surface_group",
    "surface_group_nr",
    # Main functions
    "van_kampen",
    "cw_complex_pi1",
    # Convenience decompositions
    "van_kampen_wedge_circles",
    "van_kampen_sphere",
    "van_kampen_torus",
    "van_kampen_klein_bottle",
    "van_kampen_real_projective_plane",
    # Word utilities (exported for testing)
    "_free_reduce",
    "_invert",
    "_concat",
    "_substitute",
    "_word_to_str",
]
