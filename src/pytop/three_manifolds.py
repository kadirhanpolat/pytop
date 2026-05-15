"""3-manifold profil kayitlari (MAN-02).

Bu modul Adams & Franzosa Bolum 14.3 icin ogretim odakli 3-manifold kayitlari
saglar. Amac 3-manifold tanima algoritmasi yazmak degildir; lens uzaylari,
Seifert uzaylari, torus demetleri ve temel homoloji/fibration sinyallerini paket
icinde denetlenebilir bir API yuzeyi olarak sunmaktir.
"""

from __future__ import annotations

from dataclasses import dataclass


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


__all__ = [
    "ThreeManifoldInvariantProfile",
    "ThreeManifoldProfile",
    "get_three_manifold_invariant_profiles",
    "get_three_manifold_profiles",
    "three_manifold_family_summary",
    "three_manifold_invariant_kind_summary",
    "three_manifold_profile_registry",
]
