"""3-manifold profil kayitlari ve hesaplamalı motorlar (MAN-02).

Profil katmani: Adams & Franzosa Bolum 14.3 icin ogretim odakli kayitlar.
Hesaplama katmani: mapping torus H₁ (Wang dizisi), lens uzayi π₁.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exact_linalg import AbelianGroup, cokernel

if TYPE_CHECKING:
    from .van_kampen import GroupPresentation


@dataclass(frozen=True)
class ThreeManifoldProfile:
    """Klasik bir 3-manifold ailesi icin ogretim profili."""

    key: str
    display_name: str
    model_family: str
    construction_model: str
    orientability: str
    compactness: str
    primary_invariant_signal: str
    source_section: str
    teaching_note: str


def get_three_manifold_profiles() -> tuple[ThreeManifoldProfile, ...]:
    """MAN-02 icin temel 3-manifold profillerini dondur."""
    return (
        ThreeManifoldProfile(
            key="three_sphere_baseline",
            display_name="Uc kure temel modeli",
            model_family="sphere",
            construction_model="R4 icinde birim 3-kure veya iki 3-topun sinir yapistirmasi",
            orientability="orientable",
            compactness="compact",
            primary_invariant_signal="Basit baglantili kapali 3-manifold icin referans model.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "S3, 3-manifold katalogunda kure yuzeyinin 3-boyutlu karsiligi "
                "gibi okunur ve diger modeller icin baslangic referansidir."
            ),
        ),
        ThreeManifoldProfile(
            key="lens_space_l_p_q",
            display_name="Lens uzayi L(p,q)",
            model_family="lens_space",
            construction_model="S3 uzerinde sonlu devirsel grup etkisiyle bolum uzayi",
            orientability="orientable",
            compactness="compact",
            primary_invariant_signal="Temel grup cogunlukla Z/pZ sinyaliyle izlenir.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "Lens uzaylari, ayni homoloji sinyallerine ragmen farkli "
                "3-manifoldlarin ortaya cikabilecegini gosteren klasik ailedir."
            ),
        ),
        ThreeManifoldProfile(
            key="seifert_fibered_space",
            display_name="Seifert lifli uzay",
            model_family="seifert_fibered",
            construction_model="Cember lifleriyle ayrisan 3-manifold modeli",
            orientability="context-dependent",
            compactness="usually_compact_in_classical_examples",
            primary_invariant_signal="Baz orbifold ve lif verisi siniflandirma dilini tasir.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "Seifert profili, 3-manifoldlari liflenme verisiyle okumaya gecis "
                "kapisidir; her noktanin etrafinda cember lif yapisi aranir."
            ),
        ),
        ThreeManifoldProfile(
            key="torus_bundle_mapping_torus",
            display_name="Torus demeti mapping torus",
            model_family="torus_bundle",
            construction_model="T2 yuzeyinin bir homeomorfizmasindan mapping torus",
            orientability="orientable_when_monodromy_preserves_orientation",
            compactness="compact",
            primary_invariant_signal="Monodromy matrisi geometrik ve topolojik tipi etkiler.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "Torus demeti, yuzey topolojisiyle 3-manifold yapisini birlestirir: "
                "bir yuzeyin zaman yonunde yapistirilmasi yeni bir 3-manifold verir."
            ),
        ),
    )


@dataclass(frozen=True)
class ThreeManifoldInvariantProfile:
    """3-manifold ailesi icin ogretim amacli invariant profili."""

    key: str
    manifold_key: str
    invariant_kind: str
    symbolic_signal: str
    comparison_note: str
    source_section: str
    teaching_note: str


def get_three_manifold_invariant_profiles() -> tuple[
    ThreeManifoldInvariantProfile, ...
]:
    """MAN-02 icin 3-manifold invariant profillerini dondur."""
    return (
        ThreeManifoldInvariantProfile(
            key="lens_space_fundamental_group_signal",
            manifold_key="lens_space_l_p_q",
            invariant_kind="fundamental_group",
            symbolic_signal="pi_1(L(p,q)) ~= Z/pZ",
            comparison_note="q parametresi yalnizca temel grup sinyaliyle tamamen ayrilmayabilir.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "Lens uzaylari, invariantlarin ayirt etme gucunu ve sinirlarini "
                "birlikte anlatmak icin iyi bir modeldir."
            ),
        ),
        ThreeManifoldInvariantProfile(
            key="seifert_fibration_signal",
            manifold_key="seifert_fibered_space",
            invariant_kind="fibration_data",
            symbolic_signal="base orbifold + exceptional fiber data",
            comparison_note="Lif verisi 3-manifoldun global yapisini kaydeder.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "Seifert invariant profili, uzayin tek bir sayidan cok liflenme "
                "paketiyle okunmasi gerektigini vurgular."
            ),
        ),
        ThreeManifoldInvariantProfile(
            key="torus_bundle_monodromy_signal",
            manifold_key="torus_bundle_mapping_torus",
            invariant_kind="monodromy",
            symbolic_signal="A in SL(2,Z) veya GL(2,Z) monodromy sinifi",
            comparison_note="Monodromy izi ve ozdeger davranisi geometri sinyaline baglanir.",
            source_section="Adams & Franzosa Bolum 14.3",
            teaching_note=(
                "Torus demeti profili, yuzey homeomorfizmasinin 3-boyutlu topolojik "
                "sonuca nasil tasindigini gosterir."
            ),
        ),
    )


def three_manifold_family_summary() -> dict[str, list[str]]:
    """3-manifold profillerini ailelerine gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_three_manifold_profiles():
        result.setdefault(profile.model_family, []).append(profile.key)
    return result


def three_manifold_invariant_kind_summary() -> dict[str, list[str]]:
    """3-manifold invariant profillerini turune gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_three_manifold_invariant_profiles():
        result.setdefault(profile.invariant_kind, []).append(profile.key)
    return result


def three_manifold_profile_registry() -> dict[str, int]:
    """MAN-02 profil ailelerinin kayit sayilarini dondur."""
    return {
        "three_manifold_profiles": len(get_three_manifold_profiles()),
        "three_manifold_invariant_profiles": len(
            get_three_manifold_invariant_profiles()
        ),
    }


# ===========================================================================
# Computational engines
# ===========================================================================


def mapping_torus_h1(monodromy: list[list[int]]) -> AbelianGroup:
    """Compute H₁ of the mapping torus T(φ) via the Wang exact sequence.

    For a surface automorphism φ with monodromy matrix M acting on H₁(Σ),
    the Wang long exact sequence of the fibration Σ → T(φ) → S¹ gives

        H₁(T(φ)) ≅ coker(M − I) ⊕ ℤ

    where the ℤ summand comes from the base circle direction.

    Parameters
    ----------
    monodromy:
        Square integer matrix M representing φ_* : H₁(Σ) → H₁(Σ).
        For a torus bundle this is a 2×2 matrix in GL(2, ℤ).
        For a genus-g surface bundle this is a 2g×2g symplectic matrix.

    Returns
    -------
    AbelianGroup — H₁(T(φ)) as a finitely generated abelian group.

    Raises
    ------
    ValueError
        If *monodromy* is not a square matrix.

    Examples
    --------
    Identity monodromy on T² gives the 3-torus T³ with H₁ = ℤ³:

    >>> mapping_torus_h1([[1, 0], [0, 1]])
    AbelianGroup(free_rank=3, torsion=())

    Anosov map M = [[2,1],[1,1]] (det=1, |tr|>2) gives H₁ = ℤ:

    >>> mapping_torus_h1([[2, 1], [1, 1]])
    AbelianGroup(free_rank=1, torsion=())

    Dehn twist M = [[1,1],[0,1]] gives H₁ = ℤ²:

    >>> mapping_torus_h1([[1, 1], [0, 1]])
    AbelianGroup(free_rank=2, torsion=())
    """
    n = len(monodromy)
    if n == 0:
        return AbelianGroup(free_rank=1, torsion=())
    if any(len(row) != n for row in monodromy):
        raise ValueError("monodromy must be a square matrix")
    m_minus_i = [
        [monodromy[i][j] - (1 if i == j else 0) for j in range(n)]
        for i in range(n)
    ]
    cok = cokernel(m_minus_i)
    return AbelianGroup(free_rank=cok.free_rank + 1, torsion=cok.torsion)


def lens_space_pi1(p: int) -> GroupPresentation:
    """Return a GroupPresentation of π₁(L(p, q)) = ℤ/pℤ.

    The fundamental group of the lens space L(p, q) is ℤ/pℤ, depending
    only on *p* (independent of *q* at the group level).  Special cases:

    * p = 0 → ℤ  (e.g. S¹ × S²)
    * p = 1 → trivial group  (S³)

    Parameters
    ----------
    p:
        Non-negative integer; the first parameter of L(p, q).

    Returns
    -------
    GroupPresentation — cyclic group ℤ/pℤ.

    Raises
    ------
    ValueError
        If ``p < 0``.
    """
    from .van_kampen import cyclic_group, infinite_cyclic_group, trivial_group

    if p < 0:
        raise ValueError(f"Lens space parameter p must be non-negative, got {p!r}")
    if p == 0:
        return infinite_cyclic_group()
    if p == 1:
        return trivial_group()
    return cyclic_group(p)


__all__ = [
    "AbelianGroup",
    "ThreeManifoldInvariantProfile",
    "ThreeManifoldProfile",
    "get_three_manifold_invariant_profiles",
    "get_three_manifold_profiles",
    "lens_space_pi1",
    "mapping_torus_h1",
    "three_manifold_family_summary",
    "three_manifold_invariant_kind_summary",
    "three_manifold_profile_registry",
]
