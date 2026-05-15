"""Kozmoloji ve evren topolojisi ogretim profilleri (MAN-03).

Bu modul Adams & Franzosa Bolum 14.4--14.5 hattini davranissal kozmoloji
simulasyonuna donusturmez. Amac, evrenin olasi global topolojik modellerini,
yerel geometri sinyallerini ve gozlemsel ayirt etme yaklasimlarini denetlenebilir
ogretim profilleri olarak paketlemektir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UniverseGeometryProfile:
    """Bir evren modeli icin yerel geometri ve global topoloji profili."""

    key: str
    display_name: str
    local_geometry: str
    curvature_signal: str
    compactness_signal: str
    model_examples: tuple[str, ...]
    source_section: str
    teaching_note: str


@dataclass(frozen=True)
class CosmicTopologyObservationProfile:
    """Kozmik topoloji icin gozlemsel ayirt etme profili."""

    key: str
    observation_method: str
    target_manifold_family: str
    topological_signal: str
    limitation_note: str
    source_section: str
    teaching_note: str


def get_universe_geometry_profiles() -> tuple[UniverseGeometryProfile, ...]:
    """MAN-03 icin temel evren geometri profillerini dondur."""
    return (
        UniverseGeometryProfile(
            key="spherical_universe_models",
            display_name="Kuresel geometri modelleri",
            local_geometry="positive_curvature",
            curvature_signal="Yerel model S^3 benzeri pozitif egrilik sinyali tasir.",
            compactness_signal="Klasik kapali orneklerde sonlu hacim ve kompaktlik beklenir.",
            model_examples=("3-sphere", "lens spaces", "spherical space forms"),
            source_section="Adams & Franzosa Bolum 14.4--14.5",
            teaching_note=(
                "Kuresel model, ogrenciye 'yerel olarak 3-boyutlu gorunen ama globalde "
                "kapali olabilen evren' fikrini anlatmak icin kullanilir."
            ),
        ),
        UniverseGeometryProfile(
            key="flat_universe_models",
            display_name="Duz geometri modelleri",
            local_geometry="zero_curvature",
            curvature_signal="Yerel geometri Oklidyen 3-uzay gibi davranir.",
            compactness_signal="3-torus gibi bolum modelleri kompakt; R^3 modeli kompakt degildir.",
            model_examples=("Euclidean 3-space", "3-torus", "half-twist flat manifold"),
            source_section="Adams & Franzosa Bolum 14.4--14.5",
            teaching_note=(
                "Duz geometri tek bir global topoloji zorlamaz: R^3 ile 3-torus yerel "
                "olarak benzesebilir, fakat tekrar eden goruntu sinyalleriyle ayrilabilir."
            ),
        ),
        UniverseGeometryProfile(
            key="hyperbolic_universe_models",
            display_name="Hiperbolik geometri modelleri",
            local_geometry="negative_curvature",
            curvature_signal="Yerel model H^3 benzeri negatif egrilik sinyali tasir.",
            compactness_signal="Sonlu hacimli kompakt veya cusp iceren kompakt olmayan ornekler ayirt edilir.",
            model_examples=("closed hyperbolic 3-manifolds", "finite-volume hyperbolic quotients"),
            source_section="Adams & Franzosa Bolum 14.4--14.5",
            teaching_note=(
                "Hiperbolik profil, geometri-topoloji etkilesiminin en zengin "
                "orneklerinden biridir ve 3-manifold kataloguyla dogrudan bag kurar."
            ),
        ),
    )


def get_cosmic_topology_observation_profiles() -> tuple[CosmicTopologyObservationProfile, ...]:
    """MAN-03 icin kozmik topoloji gozlem profillerini dondur."""
    return (
        CosmicTopologyObservationProfile(
            key="cosmic_crystallography_distance_peaks",
            observation_method="cosmic_crystallography",
            target_manifold_family="flat_or_quotient_models",
            topological_signal="Galaksi/kume uzaklik dagiliminda tekrar eden mesafe tepeleri aranir.",
            limitation_note="Astrofiziksel veri gürültüsü ve evrimsel etkiler yalanci veya zayif sinyal uretir.",
            source_section="Adams & Franzosa Bolum 14.5",
            teaching_note=(
                "Bu profil, global yapistirma modelinin gozlemsel veride tekrar eden "
                "uzaklik desenleri olarak okunabilecegini aciklar."
            ),
        ),
        CosmicTopologyObservationProfile(
            key="circles_in_the_sky_pattern",
            observation_method="matched_circles_in_cmb",
            target_manifold_family="compact_3_manifold_candidates",
            topological_signal="CMB yuzeyinde eslesmis daire desenleri aranir.",
            limitation_note="Cozunurluk, kozmolojik parametre belirsizligi ve esleme toleransi siniri vardir.",
            source_section="Adams & Franzosa Bolum 14.5",
            teaching_note=(
                "Eslesmis daireler, sonlu hacimli evrende ayni fiziksel bolgenin farkli "
                "yonlerden gorunmesi sezgisini tasir."
            ),
        ),
        CosmicTopologyObservationProfile(
            key="cmb_temperature_pattern_constraints",
            observation_method="cmb_temperature_pattern_comparison",
            target_manifold_family="spherical_flat_hyperbolic_candidates",
            topological_signal="CMB sicaklik haritasindaki buyuk olcekli desenler model adaylariyla karsilastirilir.",
            limitation_note="Topolojik sinyal, baslangic kosullari ve olcum belirsizligiyle karisabilir.",
            source_section="Adams & Franzosa Bolum 14.4--14.5",
            teaching_note=(
                "CMB profili, topolojinin nicel metrik olcumden cok global desen ve "
                "olasilik dislama mantigiyla calistigini vurgular."
            ),
        ),
    )


def universe_geometry_summary() -> dict[str, list[str]]:
    """Evren modellerini yerel geometri turune gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_universe_geometry_profiles():
        result.setdefault(profile.local_geometry, []).append(profile.key)
    return result


def cosmic_observation_method_summary() -> dict[str, list[str]]:
    """Kozmik topoloji profillerini gozlem yontemine gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_cosmic_topology_observation_profiles():
        result.setdefault(profile.observation_method, []).append(profile.key)
    return result


def cosmology_topology_profile_registry() -> dict[str, int]:
    """MAN-03 profil ailelerinin kayit sayilarini dondur."""
    return {
        "universe_geometry_profiles": len(get_universe_geometry_profiles()),
        "cosmic_topology_observation_profiles": len(
            get_cosmic_topology_observation_profiles()
        ),
    }


__all__ = [
    "CosmicTopologyObservationProfile",
    "UniverseGeometryProfile",
    "cosmic_observation_method_summary",
    "cosmology_topology_profile_registry",
    "get_cosmic_topology_observation_profiles",
    "get_universe_geometry_profiles",
    "universe_geometry_summary",
]
