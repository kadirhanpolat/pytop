"""Simplicial cohomology and cup product ring for finite simplicial complexes.

The cochain complex is the algebraic dual of the chain complex:

    C^k = Hom(C_k, Z) ≅ Z^{n_k}

with coboundary  δ^k = (∂_{k+1})^T : C^k → C^{k+1}   (transpose of boundary).

The cohomology groups are

    H^k(K; Z) = ker(δ^k) / im(δ^{k-1})

computed via extended Smith Normal Form — the identical algorithm used in
:mod:`pytop.mayer_vietoris` but applied to the transposed boundary matrices.

Universal Coefficient Theorem (UCT)
-------------------------------------
For a finitely generated free chain complex:

    H^k(K; Z)  ≅  Free(H_k(K; Z))  ⊕  Torsion(H_{k-1}(K; Z))

This is verified automatically; the direct cochain computation is the
primary one and the UCT provides a cross-check.

Cup product
-----------
The Alexander-Whitney cup product on cochains:

    (f ∪ g)(σ)  =  f(σ|_{front p})  ·  g(σ|_{back q})

for f ∈ C^p, g ∈ C^q and σ = [v_0 < … < v_{p+q}] a canonically-ordered
(p+q)-simplex.  front_p σ = [v_0,…,v_p],  back_q σ = [v_p,…,v_{p+q}].

If f, g are cocycles (δf = δg = 0) then f∪g is a cocycle (Leibniz rule).
The cup product descends to cohomology and makes H*(K; Z) a graded ring.
It is graded-commutative:  [f] ∪ [g] = (−1)^{pq} [g] ∪ [f].

Public API
----------
``coboundary_matrix(K, k)``        δ^k as a matrix (transpose of ∂_{k+1})
``simplicial_cohomology(K, k)``    H^k(K; Z)
``cohomology_groups(K)``           (H^0, …, H^dim)
``cohomology_betti_numbers(K)``    (b^0, …, b^dim) — equals betti_numbers(K)
``cup_product_cochain(K,f,g,p,q)`` cochain-level cup product
``CohomologyRing``                 groups + cup product table
``simplicial_cohomology_ring(K)``  computes the full ring
"""
from __future__ import annotations

from dataclasses import dataclass

from .homology import _simplices_of_dimension, boundary_matrix
from .mayer_vietoris import _col, _imat, _mat_mul, _mat_vec, _snf_ext
from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]
Vector = list[int]


# ── Matrix helper ─────────────────────────────────────────────────────────────

def _transpose(M: Matrix) -> Matrix:
    """Return the transpose of M."""
    if not M or not M[0]:
        return []
    m, n = len(M), len(M[0])
    return [[M[i][j] for i in range(m)] for j in range(n)]


# ── CohomologyResult ──────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CohomologyResult:
    """The integral cohomology group H^k(K; Z) in degree ``degree``.

    ``betti`` is the rank of the free part; ``torsion`` is the tuple of
    invariant factors greater than one.

    By the UCT, ``betti = betti_k(K)`` and the torsion factors come from
    the torsion of H_{k-1}(K; Z).
    """

    degree: int
    betti: int
    torsion: tuple[int, ...]

    @property
    def is_free(self) -> bool:
        return not self.torsion

    def describe(self) -> str:
        parts: list[str] = []
        if self.betti == 1:
            parts.append("Z")
        elif self.betti > 1:
            parts.append(f"Z^{self.betti}")
        parts.extend(f"Z/{f}" for f in self.torsion)
        return " (+) ".join(parts) if parts else "0"


# ── Extended SNF data for cohomology ─────────────────────────────────────────

@dataclass
class _CohomologyData:
    """Extended SNF data for H^k(K; Z) via the cochain complex.

    Parallel to ``_HomologyData`` in :mod:`pytop.mayer_vietoris` but uses
    coboundary matrices δ^k = (∂_{k+1})^T instead of boundary matrices.

    From SNF of δ^k : P_k @ δ^k @ Q_k = D_k  (rank r_k).
    ker(δ^k) = span of columns r_k … n_k-1 of Q_k.

    Relative coboundary  B = (Qinv_k @ δ^{k-1})[r_k:, :]  expresses
    im(δ^{k-1}) in the ker(δ^k) basis.  SNF of B gives H^k.
    """

    complex_obj: SimplicialComplex
    degree: int
    n_k: int         # dim C^k = #k-simplices
    r_k: int         # rank δ^k
    Q_k: Matrix      # n_k × n_k right change-of-basis for δ^k
    Qinv_k: Matrix
    r_B: int         # rank of relative coboundary B
    D_B_diag: list[int]
    P_B: Matrix
    Pinv_B: Matrix
    group: CohomologyResult
    torsion_indices: list[int]
    free_indices: list[int]

    @property
    def total_generators(self) -> int:
        return len(self.torsion_indices) + len(self.free_indices)

    def cocycle_rep(self, gen_idx: int) -> Vector:
        """Cocycle in C^k representing the gen_idx-th H^k generator."""
        if self.n_k == 0 or not self.Q_k:
            return []
        if gen_idx < len(self.torsion_indices):
            j = self.torsion_indices[gen_idx]
        else:
            j = self.free_indices[gen_idx - len(self.torsion_indices)]
        zk_dim = self.n_k - self.r_k
        pinv_col = (
            _col(self.Pinv_B, j)
            if self.Pinv_B and j < (len(self.Pinv_B[0]) if self.Pinv_B else 0)
            else [0] * zk_dim
        )
        rep = [0] * self.n_k
        for i in range(zk_dim):
            coeff = pinv_col[i]
            if coeff == 0:
                continue
            for row in range(self.n_k):
                rep[row] += coeff * self.Q_k[row][self.r_k + i]
        return rep

    def coords_in_cohk(self, z: Vector) -> Vector:
        """Express a cocycle z ∈ ker(δ^k) as H^k coordinates.

        Returns a vector of length ``total_generators``; torsion entries are
        reduced modulo their order.
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


def _compute_cohomology_data(K: SimplicialComplex, k: int) -> _CohomologyData:
    """Compute extended SNF data for H^k(K; Z).

    Uses  δ^k = (∂_{k+1})^T  and  δ^{k-1} = (∂_k)^T.
    The logic is identical to ``_compute_homology_data`` with boundary
    matrices replaced by their transposes.
    """
    n_k = len(_simplices_of_dimension(K, k))

    if n_k == 0:
        trivial = CohomologyResult(degree=k, betti=0, torsion=())
        return _CohomologyData(
            complex_obj=K, degree=k, n_k=0, r_k=0,
            Q_k=[], Qinv_k=[], r_B=0, D_B_diag=[],
            P_B=[], Pinv_B=[], group=trivial,
            torsion_indices=[], free_indices=[],
        )

    # δ^k = (∂_{k+1})^T : C^k → C^{k+1}   (shape: n_{k+1} × n_k)
    delta_k = _transpose(boundary_matrix(K, k + 1))

    if not delta_k or not delta_k[0]:
        # δ^k = 0 : top dimension, or no (k+1)-simplices
        r_k = 0
        Q_k: Matrix = _imat(n_k)
        Qinv_k: Matrix = _imat(n_k)
    else:
        D_k, _, _, Q_k, Qinv_k = _snf_ext(delta_k)
        r_k = sum(
            1 for i in range(min(len(D_k), n_k))
            if i < len(D_k) and i < len(D_k[i]) and D_k[i][i] != 0
        )

    zk_dim = n_k - r_k  # dimension of ker(δ^k)

    # δ^{k-1} = (∂_k)^T : C^{k-1} → C^k   (shape: n_k × n_{k-1})
    delta_km1 = _transpose(boundary_matrix(K, k))
    n_km1 = len(_simplices_of_dimension(K, k - 1)) if k >= 1 else 0

    if zk_dim == 0 or not delta_km1 or not delta_km1[0] or n_km1 == 0:
        B: Matrix = [[0] * n_km1 for _ in range(zk_dim)]
    else:
        full = _mat_mul(Qinv_k, delta_km1)
        B = full[r_k:]

    if not B or not B[0] or all(all(v == 0 for v in row) for row in B):
        r_B = 0
        D_B_diag: list[int] = [0] * zk_dim
        P_B: Matrix = _imat(zk_dim) if zk_dim else []
        Pinv_B: Matrix = _imat(zk_dim) if zk_dim else []
    else:
        D_B_raw, P_B, Pinv_B, _, _ = _snf_ext(B)
        r_B = 0
        D_B_diag = []
        for i in range(zk_dim):
            val = abs(D_B_raw[i][i]) if i < len(D_B_raw) and i < len(D_B_raw[i]) else 0
            D_B_diag.append(val)
            if val != 0:
                r_B += 1

    torsion_indices = [j for j in range(r_B) if D_B_diag[j] > 1]
    free_indices = list(range(r_B, zk_dim))
    torsion = tuple(D_B_diag[j] for j in torsion_indices)
    betti = len(free_indices)
    group = CohomologyResult(degree=k, betti=betti, torsion=torsion)

    return _CohomologyData(
        complex_obj=K, degree=k, n_k=n_k, r_k=r_k,
        Q_k=Q_k, Qinv_k=Qinv_k, r_B=r_B, D_B_diag=D_B_diag,
        P_B=P_B, Pinv_B=Pinv_B, group=group,
        torsion_indices=torsion_indices, free_indices=free_indices,
    )


# ── Public cohomology functions ───────────────────────────────────────────────

def coboundary_matrix(K: SimplicialComplex, k: int) -> Matrix:
    """Return the coboundary matrix δ^k = (∂_{k+1})^T of K.

    Maps C^k → C^{k+1}.  Rows are indexed by (k+1)-simplices, columns by
    k-simplices (both in canonical order).  Returns [] for k < 0 or when
    there are no (k+1)-simplices.
    """
    return _transpose(boundary_matrix(K, k + 1))


def simplicial_cohomology(K: SimplicialComplex, degree: int) -> CohomologyResult:
    """Return H^{degree}(K; Z) as a :class:`CohomologyResult`."""
    return _compute_cohomology_data(K, degree).group


def cohomology_groups(K: SimplicialComplex) -> tuple[CohomologyResult, ...]:
    """Return (H^0, …, H^dim) of K."""
    return tuple(simplicial_cohomology(K, k) for k in range(K.dimension + 1))


def cohomology_betti_numbers(K: SimplicialComplex) -> tuple[int, ...]:
    """Return (b^0, …, b^dim); equals ``betti_numbers(K)`` by UCT."""
    return tuple(g.betti for g in cohomology_groups(K))


# ── Cup product ───────────────────────────────────────────────────────────────

def cup_product_cochain(
    K: SimplicialComplex,
    f: Vector,
    g: Vector,
    p: int,
    q: int,
) -> Vector:
    """Compute the Alexander-Whitney cup product f ∪ g as a (p+q)-cochain.

    For each (p+q)-simplex σ = (v_0 < … < v_{p+q}):

        (f ∪ g)(σ) = f([v_0,…,v_p])  ·  g([v_p,…,v_{p+q}])

    Parameters
    ----------
    K:
        The ambient simplicial complex.
    f:
        p-cochain as a vector of length ``#p-simplices``.
    g:
        q-cochain as a vector of length ``#q-simplices``.
    p, q:
        Degrees.

    Returns
    -------
    (p+q)-cochain as a vector of length ``#(p+q)-simplices``.
    """
    simp_p = _simplices_of_dimension(K, p)
    simp_q = _simplices_of_dimension(K, q)
    simp_pq = _simplices_of_dimension(K, p + q)

    p_idx = {s: i for i, s in enumerate(simp_p)}
    q_idx = {s: i for i, s in enumerate(simp_q)}

    result: Vector = [0] * len(simp_pq)
    for k, sigma in enumerate(simp_pq):
        front = sigma[: p + 1]
        back = sigma[p:]
        fi = p_idx.get(front)
        gi = q_idx.get(back)
        if fi is not None and gi is not None:
            result[k] = f[fi] * g[gi]
    return result


# ── Cohomology ring ───────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CohomologyRing:
    """The integral cohomology ring  H*(K; Z) = ⊕_k H^k(K; Z)  with cup product.

    ``cup_table[(p, q)]`` is an integer matrix with shape
    ``(n_{p+q}, n_p · n_q)`` where  n_k = H^k generators (torsion first):

        cup_table[(p, q)][r][i * n_q + j]  =  coefficient of the r-th H^{p+q}
        generator in  [α^p_i] ∪ [β^q_j].
    """

    complex_obj: SimplicialComplex
    groups: tuple[CohomologyResult, ...]
    cup_table: dict[tuple[int, int], Matrix]

    def h(self, k: int) -> CohomologyResult | None:
        for g in self.groups:
            if g.degree == k:
                return g
        return None

    def cup(self, key: tuple[int, int]) -> Matrix:
        """Cup product matrix for H^p ⊗ H^q → H^{p+q}."""
        return self.cup_table.get(key, [])

    def betti_numbers(self) -> tuple[int, ...]:
        return tuple(g.betti for g in self.groups)

    def is_trivial_ring(self) -> bool:
        """True if all cup products H^p ⊗ H^q → H^{p+q} (p,q ≥ 1) are zero."""
        for (p, q), M in self.cup_table.items():
            if p == 0 or q == 0:
                continue
            if M and any(any(v != 0 for v in row) for row in M):
                return False
        return True

    def verify_graded_commutativity(self) -> bool:
        """Verify the graded-commutativity relation for all cup product pairs.

        Checks that  [α^p] ∪ [β^q] = (-1)^{p·q} [β^q] ∪ [α^p]  holds for
        every pair (p, q) with p+q ≤ dim.

        Returns
        -------
        bool
            True if graded-commutativity holds for all checked pairs; False
            if any violation is found (a violation message is printed).

        Raises
        ------
        ValueError
            If a violation is detected (in addition to printing the message).
        """
        ok = True
        for (p, q), M_pq in self.cup_table.items():
            M_qp = self.cup_table.get((q, p))
            if M_qp is None:
                continue  # symmetric pair not computed — skip
            hp = self.h(p)
            hq = self.h(q)
            hpq = self.h(p + q)
            if not hp or not hq or not hpq:
                continue
            n_p = hp.betti + len(hp.torsion)
            n_q = hq.betti + len(hq.torsion)
            n_pq = hpq.betti + len(hpq.torsion)
            sign = (-1) ** (p * q)
            for i in range(n_p):
                for j in range(n_q):
                    col_pq = i * n_q + j  # column in M_pq: α^p_i ∪ β^q_j
                    col_qp = j * n_p + i  # column in M_qp: β^q_j ∪ α^p_i
                    for r in range(n_pq):
                        v_pq = M_pq[r][col_pq] if (M_pq and col_pq < len(M_pq[r])) else 0
                        v_qp = M_qp[r][col_qp] if (M_qp and col_qp < len(M_qp[r])) else 0
                        expected = sign * v_qp
                        if v_pq != expected:
                            msg = (
                                f"Graded-commutativity violated at (p={p}, q={q}), "
                                f"generators (i={i}, j={j}), H^{p+q} coordinate r={r}: "
                                f"α^{p}_{i} ∪ β^{q}_{j} = {v_pq} but "
                                f"(-1)^{{{p}·{q}}} · β^{q}_{j} ∪ α^{p}_{i} = {expected}"
                            )
                            print(msg)
                            ok = False
                            raise ValueError(msg)
        return ok

    def describe(self) -> str:
        lines = ["Cohomology Ring  H*(K; Z)", "═" * 45, ""]
        for g in self.groups:
            lines.append(f"  H^{g.degree} = {g.describe()}")
        lines.append("")
        nontrivial: list[str] = []
        for (p, q) in sorted(self.cup_table):
            if p == 0 or q == 0:
                continue
            M = self.cup_table[(p, q)]
            hp = self.h(p)
            hq = self.h(q)
            hpq = self.h(p + q)
            if not hp or not hq or not hpq:
                continue
            np_ = hp.total_generators if hasattr(hp, "total_generators") else (hp.betti + len(hp.torsion))
            nq_ = hq.total_generators if hasattr(hq, "total_generators") else (hq.betti + len(hq.torsion))
            npq = hpq.total_generators if hasattr(hpq, "total_generators") else (hpq.betti + len(hpq.torsion))
            if not M or np_ == 0 or nq_ == 0 or npq == 0:
                continue
            for i in range(np_):
                for j in range(nq_):
                    col = i * nq_ + j
                    if col >= (len(M[0]) if M else 0):
                        continue
                    entry = [M[r][col] for r in range(len(M))]
                    if any(v != 0 for v in entry):
                        nontrivial.append(
                            f"  α^{p}_{i} ∪ β^{q}_{j}  =  {entry}  in H^{p + q}"
                        )
        if nontrivial:
            lines.append("Non-zero cup products (p,q ≥ 1):")
            lines.extend(nontrivial)
        else:
            lines.append("All cup products H^p ⊗ H^q → H^{p+q} (p,q ≥ 1) are zero.")
        return "\n".join(lines)


def simplicial_cohomology_ring(K: SimplicialComplex) -> CohomologyRing:
    """Compute the full cohomology ring H*(K; Z) with cup product.

    Returns a :class:`CohomologyRing` containing:
    * The cohomology groups H^0, …, H^dim.
    * For each pair (p, q) with p+q ≤ dim, the cup product matrix
      H^p ⊗ H^q → H^{p+q} with explicit cocycle representatives.

    The computation is exact (Smith Normal Form) and works for any
    finite simplicial complex.
    """
    dim = K.dimension
    hdata = [_compute_cohomology_data(K, k) for k in range(dim + 2)]
    groups = tuple(hd.group for hd in hdata[: dim + 1])

    cup_table: dict[tuple[int, int], Matrix] = {}
    for p in range(dim + 1):
        for q in range(dim + 1 - p):
            if p + q > dim:
                continue
            hp = hdata[p]
            hq = hdata[q]
            hpq = hdata[p + q]
            n_p = hp.total_generators
            n_q = hq.total_generators
            n_pq = hpq.total_generators

            if n_p == 0 or n_q == 0:
                cup_table[(p, q)] = [[] for _ in range(n_pq)]
                continue
            if n_pq == 0:
                cup_table[(p, q)] = [[0] * (n_p * n_q)]
                continue

            M: Matrix = [[0] * (n_p * n_q) for _ in range(n_pq)]
            for i in range(n_p):
                f_rep = hp.cocycle_rep(i)
                for j in range(n_q):
                    g_rep = hq.cocycle_rep(j)
                    fg = cup_product_cochain(K, f_rep, g_rep, p, q)
                    coords = hpq.coords_in_cohk(fg)
                    col = i * n_q + j
                    for r in range(n_pq):
                        M[r][col] = coords[r] if r < len(coords) else 0
            cup_table[(p, q)] = M

    return CohomologyRing(
        complex_obj=K,
        groups=groups,
        cup_table=cup_table,
    )


__all__ = [
    "CohomologyResult",
    "CohomologyRing",
    "coboundary_matrix",
    "simplicial_cohomology",
    "cohomology_groups",
    "cohomology_betti_numbers",
    "cup_product_cochain",
    "simplicial_cohomology_ring",
]
