"""Kompakt yuzey siniflandirmasi profilleri (MAN-01).

Bu modul Adams & Franzosa Bolum 14.2 icin ogretim odakli yuzey siniflandirma
kayitlari saglar. Amac bir homeomorfizma karar motoru yazmak degildir; Euler
karakteristigi, orientability ve temel kompakt yuzey ailelerini denetlenebilir
profil kayitlari olarak paketlemektir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompactSurfaceClassificationProfile:
    """Kompakt baglantili yuzey sinifi icin ogretim profili."""

    key: str
    display_name: str
    orientability: str
    genus_or_crosscap_count: int
    euler_characteristic: int
    classification_model: str
    source_section: str
    teaching_note: str


def get_compact_surface_classification_profiles() -> tuple[
    CompactSurfaceClassificationProfile, ...
]:
    """MAN-01 icin temel kompakt yuzey siniflandirma profillerini dondur."""
    return (
        CompactSurfaceClassificationProfile(
            key="sphere_surface",
            display_name="Kure yuzeyi",
            orientability="orientable",
            genus_or_crosscap_count=0,
            euler_characteristic=2,
            classification_model="Orientable genus 0 kompakt yuzey",
            source_section="Adams & Franzosa Bolum 14.2",
            teaching_note=(
                "Kure, kompakt orientable yuzey siniflandirmasinda baslangic "
                "modelidir ve Euler karakteristigi 2 olarak okunur."
            ),
        ),
        CompactSurfaceClassificationProfile(
            key="torus_surface",
            display_name="Torus yuzeyi",
            orientability="orientable",
            genus_or_crosscap_count=1,
            euler_characteristic=0,
            classification_model="Orientable genus 1 kompakt yuzey",
            source_section="Adams & Franzosa Bolum 14.2",
            teaching_note=(
                "Torus, bir kulp eklemenin Euler karakteristigini iki azalttigini "
                "gosteren temel modeldir."
            ),
        ),
        CompactSurfaceClassificationProfile(
            key="double_torus_surface",
            display_name="Iki kulplu orientable yuzey",
            orientability="orientable",
            genus_or_crosscap_count=2,
            euler_characteristic=-2,
            classification_model="Orientable genus 2 kompakt yuzey",
            source_section="Adams & Franzosa Bolum 14.2",
            teaching_note=(
                "Iki kulplu yuzey, orientable ailede genus arttikca Euler "
                "karakteristiginin nasil degistigini vurgular."
            ),
        ),
        CompactSurfaceClassificationProfile(
            key="projective_plane_surface",
            display_name="Projektif duzlem",
            orientability="nonorientable",
            genus_or_crosscap_count=1,
            euler_characteristic=1,
            classification_model="Nonorientable crosscap 1 kompakt yuzey",
            source_section="Adams & Franzosa Bolum 14.2",
            teaching_note=(
                "Projektif duzlem, nonorientable yuzey ailesinin ilk modelidir ve "
                "orientability sinyalinin siniflandirmada zorunlu oldugunu gosterir."
            ),
        ),
        CompactSurfaceClassificationProfile(
            key="klein_bottle_surface",
            display_name="Klein sisesi",
            orientability="nonorientable",
            genus_or_crosscap_count=2,
            euler_characteristic=0,
            classification_model="Nonorientable crosscap 2 kompakt yuzey",
            source_section="Adams & Franzosa Bolum 14.2",
            teaching_note=(
                "Klein sisesi, torus ile ayni Euler karakteristigine sahip olsa da "
                "orientability verisiyle ondan ayrilir."
            ),
        ),
    )


def surface_euler_characteristic_summary() -> dict[str, int]:
    """Yuzey profillerini Euler karakteristigine gore indeksle."""
    return {
        profile.key: profile.euler_characteristic
        for profile in get_compact_surface_classification_profiles()
    }


def surface_orientability_summary() -> dict[str, list[str]]:
    """Yuzey profillerini orientability degerine gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_compact_surface_classification_profiles():
        result.setdefault(profile.orientability, []).append(profile.key)
    return result


def compact_surface_classification_registry() -> dict[str, int]:
    """MAN-01 profil ailelerinin kayit sayilarini dondur."""
    return {
        "compact_surface_classification_profiles": len(
            get_compact_surface_classification_profiles()
        )
    }


__all__ = [
    "CompactSurfaceClassificationProfile",
    "compact_surface_classification_registry",
    "get_compact_surface_classification_profiles",
    "surface_euler_characteristic_summary",
    "surface_orientability_summary",
]
