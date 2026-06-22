"""Mayer–Vietoris long exact sequence for finite simplicial complexes.

Given two subcomplexes A, B of K = A ∪ B, this module constructs and
verifies the long exact sequence

    ⋯ → H_n(A ∩ B) ─φ→ H_n(A) ⊕ H_n(B) ─ψ→ H_n(K) ─δ→ H_{n-1}(A ∩ B) → ⋯

Maps:
  φ(x)   = (i_*(x), −j_*(x))   where i: A∩B→A, j: A∩B→B inclusions
  ψ(a,b) = k_*(a) + l_*(b)      where k: A→K,   l: B→K  inclusions
  δ                              connecting homomorphism (snake lemma)

All groups are computed from first principles (boundary matrices → extended
Smith Normal Form gives explicit homology bases and cycle representatives).
The connecting homomorphism is derived via the snake lemma construction.
Exactness is verified at every position.
"""
from __future__ import annotations

from dataclasses import dataclass

from .homology import (
    HomologyResult,
    _simplices_of_dimension,
    boundary_matrix,
)
from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]
Vector = list[int]


# ── Matrix utilities ──────────────────────────────────────────────────────────

def _imat(n: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def _mat_mul(A: Matrix, B: Matrix) -> Matrix:
    if not A or not A[0] or not B or not B[0]:
        return [[0] * (len(B[0]) if B and B[0] else 0) for _ in range(len(A))]
    r, k, c = len(A), len(B), len(B[0])
    return [[sum(A[i][s] * B[s][j] for s in range(k)) for j in range(c)] for i in range(r)]


def _mat_vec(M: Matrix, v: Vector) -> Vector:
    if not M or not v:
        return [0] * len(M)
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def _col(M: Matrix, j: int) -> Vector:
    return [M[i][j] for i in range(len(M))]


# ── Extended Smith Normal Form ────────────────────────────────────────────────

def _snf_ext(
    M: Matrix,
    *,
    compute_transforms: bool = True,
) -> tuple[Matrix, Matrix, Matrix, Matrix, Matrix]:
    """Extended Smith Normal Form with all transformation matrices.

    Returns ``(D, P, Pinv, Q, Qinv)`` (all integer) such that
    ``P @ M @ Q = D`` (diagonal, non-negative, divisibility chain) and
    ``P @ Pinv = I_{rows}``, ``Q @ Qinv = I_{cols}``.

    Parameters
    ----------
    compute_transforms:
        When ``False`` the row/column transformation matrices P, Pinv, Q, Qinv
        are not updated during the reduction (they remain identity matrices).
        Only ``D`` is meaningful in that case.  Use this when only the diagonal
        (rank / invariant factors) is needed — it skips ~80 % of the inner-loop
        work for large matrices.
    """
    if not M or not M[0]:
        m = len(M)
        n = len(M[0]) if M else 0
        return [], _imat(m), _imat(m), _imat(n), _imat(n)

    m, n = len(M), len(M[0])
    D = [list(map(int, row)) for row in M]
    P, Pinv = _imat(m), _imat(m)
    Q, Qinv = _imat(n), _imat(n)

    def swap_rows(i: int, j: int) -> None:
        D[i], D[j] = D[j], D[i]
        if compute_transforms:
            P[i], P[j] = P[j], P[i]
            for r in range(m):
                Pinv[r][i], Pinv[r][j] = Pinv[r][j], Pinv[r][i]

    def add_row(src: int, dst: int, f: int) -> None:
        for c in range(n):
            D[dst][c] += f * D[src][c]
        if compute_transforms:
            for c in range(m):
                P[dst][c] += f * P[src][c]
            for r in range(m):
                Pinv[r][src] -= f * Pinv[r][dst]

    def negate_row(i: int) -> None:
        for c in range(n):
            D[i][c] = -D[i][c]
        if compute_transforms:
            for c in range(m):
                P[i][c] = -P[i][c]
            for r in range(m):
                Pinv[r][i] = -Pinv[r][i]

    def swap_cols(i: int, j: int) -> None:
        for r in range(m):
            D[r][i], D[r][j] = D[r][j], D[r][i]
        if compute_transforms:
            for r in range(n):
                Q[r][i], Q[r][j] = Q[r][j], Q[r][i]
            Qinv[i], Qinv[j] = Qinv[j], Qinv[i]

    def add_col(src: int, dst: int, f: int) -> None:
        for r in range(m):
            D[r][dst] += f * D[r][src]
        if compute_transforms:
            for r in range(n):
                Q[r][dst] += f * Q[r][src]
            for c in range(n):
                Qinv[src][c] -= f * Qinv[dst][c]

    def negate_col(j: int) -> None:
        for r in range(m):
            D[r][j] = -D[r][j]
        if compute_transforms:
            for r in range(n):
                Q[r][j] = -Q[r][j]
            for c in range(n):
                Qinv[j][c] = -Qinv[j][c]

    step = 0
    while step < min(m, n):
        pivot = None
        best = 0
        for r in range(step, m):
            for c in range(step, n):
                v = D[r][c]
                if v != 0 and (pivot is None or abs(v) < best):
                    pivot = (r, c)
                    best = abs(v)
        if pivot is None:
            break
        swap_rows(step, pivot[0])
        swap_cols(step, pivot[1])

        changed = True
        while changed:
            changed = False
            if D[step][step] < 0:
                negate_row(step)
            for r in range(m):
                if r != step and D[r][step] != 0:
                    q = D[r][step] // D[step][step]
                    add_row(step, r, -q)
                    if D[r][step] != 0:
                        swap_rows(step, r)
                        changed = True
            for c in range(n):
                if c != step and D[step][c] != 0:
                    q = D[step][c] // D[step][step]
                    add_col(step, c, -q)
                    if D[step][c] != 0:
                        swap_cols(step, c)
                        changed = True
            if not changed:
                for r in range(step + 1, m):
                    for c in range(step + 1, n):
                        if D[r][c] % D[step][step] != 0:
                            add_row(r, step, 1)
                            changed = True
                            break
                    if changed:
                        break
        step += 1

    return D, P, Pinv, Q, Qinv


# ── Simplicial complex set operations ────────────────────────────────────────

def sc_intersection(A: SimplicialComplex, B: SimplicialComplex) -> SimplicialComplex:
    """Return A ∩ B (simplices common to both subcomplexes)."""
    common = A.simplexes & B.simplexes
    if not common:
        raise ValueError("A ∩ B is empty — Mayer–Vietoris requires A ∩ B ≠ ∅.")
    return SimplicialComplex(common)


def sc_union(A: SimplicialComplex, B: SimplicialComplex) -> SimplicialComplex:
    """Return A ∪ B (face-closed because both inputs are)."""
    return SimplicialComplex(A.simplexes | B.simplexes)


# ── Chain-level inclusion map ─────────────────────────────────────────────────

def _inclusion_chain(src: SimplicialComplex, tgt: SimplicialComplex, k: int) -> Matrix:
    """Matrix of the inclusion i_k: C_k(src) → C_k(tgt).

    Rows indexed by tgt k-simplices, columns by src k-simplices (canonical order).
    Each src simplex maps to itself in tgt with coefficient +1.
    """
    src_simp = _simplices_of_dimension(src, k)
    tgt_simp = _simplices_of_dimension(tgt, k)
    tgt_idx = {s: i for i, s in enumerate(tgt_simp)}
    n_src, n_tgt = len(src_simp), len(tgt_simp)
    mat = [[0] * n_src for _ in range(n_tgt)]
    for j, s in enumerate(src_simp):
        if s in tgt_idx:
            mat[tgt_idx[s]][j] = 1
    return mat


# ── Homology data (SNF-derived) ───────────────────────────────────────────────

@dataclass
class _HomologyData:
    """Extended SNF data for H_k(K; Z) enabling explicit basis computations.

    From SNF of ∂_k: P_k @ ∂_k @ Q_k = D_k (rank r_k).
    ker(∂_k) = Z_k is spanned by columns r_k..n_k-1 of Q_k.

    Relative boundary matrix B = (Qinv_k @ ∂_{k+1})[r_k:, :] expresses
    im(∂_{k+1}) in the Z_k basis.  From SNF of B: P_B @ B @ Q_B = D_B.
    H_k = Z_k / im(B) is read off from D_B.
    """

    complex_obj: SimplicialComplex
    degree: int
    n_k: int
    r_k: int
    Q_k: Matrix
    Qinv_k: Matrix
    r_B: int
    D_B_diag: list[int]
    P_B: Matrix
    Pinv_B: Matrix
    group: HomologyResult
    torsion_indices: list[int]
    free_indices: list[int]

    @property
    def total_generators(self) -> int:
        return len(self.torsion_indices) + len(self.free_indices)

    def cycle_rep(self, gen_idx: int) -> Vector:
        """Cycle in C_k representing the gen_idx-th H_k generator."""
        if self.n_k == 0 or not self.Q_k:
            return []
        if gen_idx < len(self.torsion_indices):
            j = self.torsion_indices[gen_idx]
        else:
            j = self.free_indices[gen_idx - len(self.torsion_indices)]
        zk_dim = self.n_k - self.r_k
        pinv_col = _col(self.Pinv_B, j) if self.Pinv_B and j < len(self.Pinv_B[0]) else [0] * zk_dim
        rep = [0] * self.n_k
        for i in range(zk_dim):
            coeff = pinv_col[i]
            if coeff == 0:
                continue
            for row in range(self.n_k):
                rep[row] += coeff * self.Q_k[row][self.r_k + i]
        return rep

    def coords_in_hk(self, z: Vector) -> Vector:
        """Express a cycle z ∈ Z_k(K) as a coordinate vector in H_k.

        Returns a vector of length ``total_generators``.
        Torsion coordinates are reduced modulo their order.
        """
        if self.total_generators == 0 or not z:
            return [0] * self.total_generators
        c_full = _mat_vec(self.Qinv_k, z)
        c_Zk = c_full[self.r_k:]
        c_new = _mat_vec(self.P_B, c_Zk) if self.P_B else c_Zk
        result = []
        for j in self.torsion_indices:
            d = self.D_B_diag[j]
            result.append(c_new[j] % d if d else 0)
        for j in self.free_indices:
            result.append(c_new[j])
        return result


def _compute_homology_data(K: SimplicialComplex, k: int) -> _HomologyData:
    """Compute extended SNF data for H_k(K; Z)."""
    n_k = len(_simplices_of_dimension(K, k))

    if n_k == 0:
        trivial = HomologyResult(degree=k, betti=0, torsion=())
        return _HomologyData(
            complex_obj=K, degree=k, n_k=0, r_k=0,
            Q_k=[], Qinv_k=[], r_B=0, D_B_diag=[],
            P_B=[], Pinv_B=[], group=trivial,
            torsion_indices=[], free_indices=[],
        )

    dk_mat = boundary_matrix(K, k)
    if not dk_mat or (dk_mat and not dk_mat[0]):
        # ∂_k = 0 (k = 0 or no (k-1)-simplices)
        r_k = 0
        Q_k = _imat(n_k)
        Qinv_k = _imat(n_k)
    else:
        D_k, _, _, Q_k, Qinv_k = _snf_ext(dk_mat)
        r_k = sum(
            1 for i in range(min(len(D_k), n_k))
            if i < len(D_k) and i < len(D_k[i]) and D_k[i][i] != 0
        )

    zk_dim = n_k - r_k

    # Relative boundary matrix B = (Qinv_k @ ∂_{k+1})[r_k:, :]
    dk1_mat = boundary_matrix(K, k + 1)
    n_k1 = len(_simplices_of_dimension(K, k + 1))

    if zk_dim == 0 or not dk1_mat or n_k1 == 0:
        B: Matrix = [[0] * n_k1 for _ in range(zk_dim)]
    else:
        full = _mat_mul(Qinv_k, dk1_mat)
        B = full[r_k:]

    if not B or not B[0] or all(all(v == 0 for v in row) for row in B):
        r_B = 0
        D_B_diag = [0] * zk_dim
        P_B = _imat(zk_dim) if zk_dim else []
        Pinv_B = _imat(zk_dim) if zk_dim else []
    else:
        D_B_raw, P_B, Pinv_B, _, _ = _snf_ext(B)
        r_B = 0
        D_B_diag = []
        for i in range(zk_dim):
            if i < len(D_B_raw) and i < len(D_B_raw[i]):
                val = abs(D_B_raw[i][i])
            else:
                val = 0
            D_B_diag.append(val)
            if val != 0:
                r_B += 1

    torsion_indices = [j for j in range(r_B) if D_B_diag[j] > 1]
    free_indices = list(range(r_B, zk_dim))
    torsion = tuple(D_B_diag[j] for j in torsion_indices)
    betti = len(free_indices)
    group = HomologyResult(degree=k, betti=betti, torsion=torsion)

    return _HomologyData(
        complex_obj=K, degree=k, n_k=n_k, r_k=r_k,
        Q_k=Q_k, Qinv_k=Qinv_k, r_B=r_B, D_B_diag=D_B_diag,
        P_B=P_B, Pinv_B=Pinv_B, group=group,
        torsion_indices=torsion_indices, free_indices=free_indices,
    )


# ── Induced map on homology ───────────────────────────────────────────────────

def _induced_on_hk(
    f_chain: Matrix,
    hdata_src: _HomologyData,
    hdata_tgt: _HomologyData,
) -> Matrix:
    """Matrix of f_*: H_k(src) → H_k(tgt) induced by the chain map f_chain.

    Rows = tgt generators, columns = src generators.
    """
    n_src = hdata_src.total_generators
    n_tgt = hdata_tgt.total_generators
    if n_src == 0:
        return [[] for _ in range(n_tgt)]
    if n_tgt == 0:
        return []  # semantically correct: 0 rows (no target generators)

    result = [[0] * n_src for _ in range(n_tgt)]
    for j in range(n_src):
        rep = hdata_src.cycle_rep(j)
        if not rep or not f_chain or not f_chain[0]:
            continue
        f_rep = _mat_vec(f_chain, rep)
        coords = hdata_tgt.coords_in_hk(f_rep)
        for i in range(n_tgt):
            if i < len(coords):
                result[i][j] = coords[i]
    return result


# ── Connecting homomorphism ───────────────────────────────────────────────────

def _connecting_hom(
    A: SimplicialComplex,
    B: SimplicialComplex,
    K: SimplicialComplex,
    n: int,
    hdata_K_n: _HomologyData,
    hdata_AB_n1: _HomologyData,
    AB: SimplicialComplex,
) -> Matrix:
    """Matrix of δ: H_n(K) → H_{n-1}(A∩B) (connecting homomorphism).

    For each H_n(K) generator [z], split z = z_A + z_B (A-part and B-part),
    then δ([z]) = [∂(z_A)] ∈ H_{n-1}(A∩B).  Since z is a cycle,
    ∂(z_A) = −∂(z_B) lands in C_{n-1}(A∩B).
    """
    n_src = hdata_K_n.total_generators
    n_tgt = hdata_AB_n1.total_generators
    if n_src == 0 or n_tgt == 0 or n < 1:
        return [[0] * n_src for _ in range(n_tgt)]

    K_n_simp = _simplices_of_dimension(K, n)
    A_n_simp_set = set(_simplices_of_dimension(A, n))
    in_A = [s in A_n_simp_set for s in K_n_simp]

    K_n1_simp = _simplices_of_dimension(K, n - 1)
    K_n1_idx = {s: i for i, s in enumerate(K_n1_simp)}
    AB_n1_simp = _simplices_of_dimension(AB, n - 1)
    AB_n1_idx = {s: i for i, s in enumerate(AB_n1_simp)}

    result = [[0] * n_src for _ in range(n_tgt)]
    for j in range(n_src):
        z = hdata_K_n.cycle_rep(j)
        # Compute ∂(z_A) in C_{n-1}(K)
        partial_zA_in_K = [0] * len(K_n1_simp)
        for i, sigma in enumerate(K_n_simp):
            if not in_A[i] or z[i] == 0:
                continue
            for fi in range(len(sigma)):
                face = sigma[:fi] + sigma[fi + 1:]
                ki = K_n1_idx.get(face)
                if ki is not None:
                    partial_zA_in_K[ki] += ((-1) ** fi) * z[i]
        # Restrict to A∩B (guaranteed to be there since z is a cycle)
        partial_in_AB = [0] * len(AB_n1_simp)
        for s, ai in AB_n1_idx.items():
            ki = K_n1_idx.get(s)
            if ki is not None:
                partial_in_AB[ai] = partial_zA_in_K[ki]
        coords = hdata_AB_n1.coords_in_hk(partial_in_AB)
        for i in range(n_tgt):
            if i < len(coords):
                result[i][j] = coords[i]
    return result


# ── Public data structures ────────────────────────────────────────────────────

@dataclass(frozen=True)
class MVDegree:
    """Groups and maps for one degree in the Mayer–Vietoris LES."""

    degree: int
    h_intersection: HomologyResult
    h_A: HomologyResult
    h_B: HomologyResult
    h_union: HomologyResult
    # φ: H_n(A∩B) → H_n(A) ⊕ H_n(B)   (rows = A-block then B-block)
    phi: Matrix
    # ψ: H_n(A) ⊕ H_n(B) → H_n(K)      (rows = K generators)
    psi: Matrix
    # δ: H_n(K) → H_{n-1}(A∩B)           (rows = (A∩B)_{n-1} generators)
    delta: Matrix
    # Is the LES exact at each of the three positions in this degree?
    exact_at_AB: bool
    exact_at_AB2: bool
    exact_at_K: bool

    def _grp(self, h: HomologyResult) -> str:
        s = h.describe()
        return s if s else "0"

    def describe_line(self) -> str:
        n = self.degree
        ab = self._grp(self.h_intersection)
        a = self._grp(self.h_A)
        b = self._grp(self.h_B)
        k = self._grp(self.h_union)
        return f"  H_{n}(A∩B)={ab}  →φ  H_{n}(A)⊕H_{n}(B)={a}⊕{b}  →ψ  H_{n}(K)={k}  →δ"


@dataclass(frozen=True)
class MayerVietorisSequence:
    """The Mayer–Vietoris long exact sequence for K = A ∪ B."""

    A: SimplicialComplex
    B: SimplicialComplex
    intersection: SimplicialComplex
    union: SimplicialComplex
    degrees: tuple[MVDegree, ...]
    euler_check_passed: bool

    @property
    def is_exact(self) -> bool:
        return all(
            d.exact_at_AB and d.exact_at_AB2 and d.exact_at_K
            for d in self.degrees
        )

    def h_union_at(self, n: int) -> HomologyResult | None:
        for d in self.degrees:
            if d.degree == n:
                return d.h_union
        return None

    def describe(self) -> str:
        lines = [
            "Mayer–Vietoris Long Exact Sequence  K = A ∪ B",
            "═" * 55,
            "",
        ]
        for d in sorted(self.degrees, key=lambda x: -x.degree):
            lines.append(d.describe_line())
        lines.append("  ⋯ → 0")
        lines.append("")
        chi_K = sum(
            (-1) ** d.degree * d.h_union.betti for d in self.degrees
        )
        chi_A = sum((-1) ** d.degree * d.h_A.betti for d in self.degrees)
        chi_B = sum((-1) ** d.degree * d.h_B.betti for d in self.degrees)
        chi_AB = sum(
            (-1) ** d.degree * d.h_intersection.betti for d in self.degrees
        )
        chi_label = "✓" if self.euler_check_passed else "✗"
        lines.append(
            f"Euler characteristic: χ(K)={chi_K} = χ(A)+χ(B)-χ(A∩B) = "
            f"{chi_A}+{chi_B}-{chi_AB} = {chi_A+chi_B-chi_AB}  {chi_label}"
        )
        lines.append("")
        exact_label = "✓ exact at all positions" if self.is_exact else "✗ exactness failure detected"
        lines.append(f"Sequence: {exact_label}")
        return "\n".join(lines)


# ── Exactness verification ────────────────────────────────────────────────────

def _image_subspace(M: Matrix) -> set[tuple[int, ...]]:
    """Return the integer image of M as a set of column vectors (for small groups)."""
    if not M or not M[0]:
        return {tuple([0] * len(M))}
    cols = set()
    for j in range(len(M[0])):
        cols.add(tuple(_col(M, j)))
    # For verification we only compare image and kernel by checking
    # rank equality: dim im(A) + dim ker(A) = dim domain.
    # Actual exactness: im(f) = ker(g) ↔ rank(g∘f) = 0 and
    # rank(f) + rank(g) - dim(middle) = 0, i.e. rank(f) = dim(middle) - rank(g).
    return cols


def _gen_orders(hdata: _HomologyData) -> list[int]:
    """Order of each homology generator: d > 1 for torsion (order d), 0 for free."""
    orders = [hdata.D_B_diag[j] for j in hdata.torsion_indices]
    orders += [0] * len(hdata.free_indices)
    return orders


def _mat_rank(M: Matrix) -> int:
    """Rank of an integer matrix via partial SNF."""
    if not M or not M[0]:
        return 0
    D, _, _, _, _ = _snf_ext(M, compute_transforms=False)
    return sum(
        1 for i in range(min(len(D), len(D[0]) if D else 0))
        if i < len(D) and i < len(D[i]) and D[i][i] != 0
    )


def _check_exact_at_middle(
    left: Matrix,
    right: Matrix,
    mid_dim: int,
    tgt_orders: list[int] | None = None,
) -> bool:
    """Check im(left) = ker(right) via rank-nullity and torsion-aware composition.

    For free abelian middle groups this is exact.  When ``tgt_orders`` is
    supplied, the composition check reduces ``(right∘left)[i][j]`` modulo the
    order of the *i*-th target generator, correctly handling groups with torsion
    (e.g. Z/2 ⊕ Z where integer entry 2 is 0 in the torsion component).

    Parameters
    ----------
    tgt_orders:
        Order of each generator in the codomain of ``right`` (0 = infinite /
        free).  Pass ``_gen_orders(hdata_target)`` at each call site.
    """
    if mid_dim == 0:
        return True
    r_left = _mat_rank(left)
    r_right = _mat_rank(right)
    if r_left + r_right != mid_dim:
        return False
    if left and left[0] and right and right[0]:
        comp = _mat_mul(right, left)
        cols_comp = len(comp[0]) if comp else 0
        for i in range(len(comp)):
            d = tgt_orders[i] if (tgt_orders and i < len(tgt_orders)) else 0
            for j in range(cols_comp):
                val = comp[i][j]
                if d:
                    if val % d != 0:
                        return False
                elif val != 0:
                    return False
    return True


# ── Main entry point ──────────────────────────────────────────────────────────

def mayer_vietoris(
    A: SimplicialComplex,
    B: SimplicialComplex,
) -> MayerVietorisSequence:
    """Compute the Mayer–Vietoris long exact sequence for K = A ∪ B.

    Parameters
    ----------
    A, B:
        Two subcomplexes whose union is K = A ∪ B.
        Both must be face-closed (standard ``SimplicialComplex`` invariant).
        Their intersection A ∩ B must be non-empty.

    Returns
    -------
    MayerVietorisSequence
        Contains homology groups at each degree, the three maps (φ, ψ, δ)
        as integer matrices, and exactness flags for every position.
    """
    AB = sc_intersection(A, B)
    K = sc_union(A, B)

    max_dim = max(A.dimension, B.dimension)

    # Precompute extended homology data for all four complexes.
    # range(max_dim + 1) suffices: the loop runs n=0..max_dim and accesses
    # hd_XY[n] and hd_AB[n-1] (i.e. indices 0..max_dim).
    def hdata_all(X: SimplicialComplex) -> list[_HomologyData]:
        return [_compute_homology_data(X, k) for k in range(max_dim + 1)]

    hd_AB = hdata_all(AB)
    hd_A = hdata_all(A)
    hd_B = hdata_all(B)
    hd_K = hdata_all(K)

    degrees: list[MVDegree] = []

    for n in range(max_dim + 1):
        ab_n = hd_AB[n]
        a_n = hd_A[n]
        b_n = hd_B[n]
        k_n = hd_K[n]
        ab_n1 = hd_AB[n - 1] if n >= 1 else None  # A∩B at degree n-1

        # Inclusion chain maps at degree n
        i_chain = _inclusion_chain(AB, A, n)   # i: A∩B → A
        j_chain = _inclusion_chain(AB, B, n)   # j: A∩B → B
        ka_chain = _inclusion_chain(A, K, n)   # k: A → K
        lb_chain = _inclusion_chain(B, K, n)   # l: B → K

        # φ = (i_*, -j_*): H_n(A∩B) → H_n(A) ⊕ H_n(B)
        i_star = _induced_on_hk(i_chain, ab_n, a_n)
        j_star = _induced_on_hk(j_chain, ab_n, b_n)
        # Stack vertically: rows = A-block then B-block
        phi: Matrix = []
        for row in i_star:
            phi.append(list(row))
        for row in j_star:
            phi.append([-x for x in row])

        # ψ = (k_*, l_*): H_n(A) ⊕ H_n(B) → H_n(K)
        k_star = _induced_on_hk(ka_chain, a_n, k_n)
        l_star = _induced_on_hk(lb_chain, b_n, k_n)
        n_a = a_n.total_generators
        n_b = b_n.total_generators
        n_k = k_n.total_generators
        psi: Matrix = [[0] * (n_a + n_b) for _ in range(n_k)]
        for i in range(n_k):
            for jj in range(n_a):
                psi[i][jj] = k_star[i][jj] if k_star and jj < len(k_star[0] if k_star else []) else 0
            for jj in range(n_b):
                psi[i][n_a + jj] = l_star[i][jj] if l_star and jj < len(l_star[0] if l_star else []) else 0

        # δ: H_n(K) → H_{n-1}(A∩B)
        if n >= 1 and ab_n1 is not None:
            delta = _connecting_hom(A, B, K, n, k_n, ab_n1, AB)
        else:
            delta = [[] for _ in range(0)]

        # Exactness checks
        n_ab_prev = ab_n1.total_generators if ab_n1 is not None else 0
        n_sum = n_a + n_b

        # At H_n(A∩B): im(δ_{n+1}) = ker(φ_n)  [checked at next degree]
        # At H_n(A)⊕H_n(B): im(φ_n) = ker(ψ_n)  [target of ψ = H_n(K)]
        exact_at_AB2 = _check_exact_at_middle(phi, psi, n_sum, _gen_orders(k_n))
        # At H_n(K): im(ψ_n) = ker(δ_n)  [target of δ = H_{n-1}(A∩B)]
        tgt_orders_delta = _gen_orders(ab_n1) if ab_n1 is not None else []
        exact_at_K = _check_exact_at_middle(psi, delta, n_k, tgt_orders_delta)
        # At H_{n-1}(A∩B): im(δ_n) = ker(φ_{n-1}) [target of φ_{n-1} = H_{n-1}(A)⊕H_{n-1}(B)]
        if n >= 1 and ab_n1 is not None:
            a_n1 = hd_A[n - 1]   # H_{n-1}(A)
            b_n1 = hd_B[n - 1]   # H_{n-1}(B)
            phi_prev_i = _induced_on_hk(_inclusion_chain(AB, A, n - 1), ab_n1, a_n1)
            phi_prev_j = _induced_on_hk(_inclusion_chain(AB, B, n - 1), ab_n1, b_n1)
            phi_prev: Matrix = [list(r) for r in phi_prev_i] + [[-x for x in r] for r in phi_prev_j]
            tgt_orders_phi = _gen_orders(a_n1) + _gen_orders(b_n1)
            exact_at_AB = _check_exact_at_middle(delta, phi_prev, n_ab_prev, tgt_orders_phi)
        else:
            exact_at_AB = True

        degrees.append(MVDegree(
            degree=n,
            h_intersection=ab_n.group,
            h_A=a_n.group,
            h_B=b_n.group,
            h_union=k_n.group,
            phi=phi,
            psi=psi,
            delta=delta,
            exact_at_AB=exact_at_AB,
            exact_at_AB2=exact_at_AB2,
            exact_at_K=exact_at_K,
        ))

    # Euler characteristic check
    chi_K = K.euler_characteristic()
    chi_A = A.euler_characteristic()
    chi_B = B.euler_characteristic()
    chi_AB = AB.euler_characteristic()
    euler_ok = (chi_K == chi_A + chi_B - chi_AB)

    return MayerVietorisSequence(
        A=A,
        B=B,
        intersection=AB,
        union=K,
        degrees=tuple(degrees),
        euler_check_passed=euler_ok,
    )
