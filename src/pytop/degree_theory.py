"""Derece teorisi profil modülü (DEG-01).

Bu modül Adams & Franzosa Bölüm 9'daki çember derecesi hattı için öğretim
amaçlı profil kayıtları ekler. Paket mimarisine uygun biçimde sembolik cebir
veya otomatik kanıt üretimi yapmaz; değişmez dataclass kayıtları, küçük
kayıt tabloları ve özet yardımcıları sağlar.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CircleDegreeProfile:
    """Derecesi belirlenmiş bir S^1 -> S^1 haritası profili."""

    key: str
    display_name: str
    map_description: str
    degree: int
    orientation_behavior: str
    induced_fundamental_group_map: str
    homotopy_class: str
    source_section: str
    notes: str


def get_circle_degree_profiles() -> tuple[CircleDegreeProfile, ...]:
    """Standart çember derecesi örneklerini döndür."""
    return (
        CircleDegreeProfile(
            key="identity_circle_degree_one",
            display_name="Çember üzerinde özdeşlik haritası",
            map_description="id: S^1 -> S^1, id(z) = z",
            degree=1,
            orientation_behavior="orientation_preserving",
            induced_fundamental_group_map="n |-> n",
            homotopy_class="generator",
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Özdeşlik haritası pi_1(S^1)'in pozitif üretecini korur. "
                "Derecesi 1'dir; bu yüzden çember öz-haritalarının temel "
                "sıfıra homotopik olmayan sınıfını temsil eder."
            ),
        ),
        CircleDegreeProfile(
            key="constant_circle_degree_zero",
            display_name="Çemberden tek noktaya sabit harita",
            map_description="c: S^1 -> S^1, c(z) = 1",
            degree=0,
            orientation_behavior="collapses_loop",
            induced_fundamental_group_map="n |-> 0",
            homotopy_class="null_homotopic",
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Sabit harita temel grup üretecini yok eder. Derece 0, her "
                "döngünün sıfıra homotopik bir döngüye çöktüğünü kaydeder."
            ),
        ),
        CircleDegreeProfile(
            key="power_map_degree_two",
            display_name="Kuvvet haritası z |-> z^2",
            map_description="p_2: S^1 -> S^1, p_2(z) = z^2",
            degree=2,
            orientation_behavior="wraps_twice_positive",
            induced_fundamental_group_map="n |-> 2n",
            homotopy_class="degree_two",
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Bu harita tanım çemberindeki bir turu hedef çemberde iki "
                "pozitif tura dönüştürür. Derecenin hedef çemberin işaretli "
                "sarılma sayısını nasıl saydığını gösteren temel modeldir."
            ),
        ),
        CircleDegreeProfile(
            key="conjugation_degree_minus_one",
            display_name="Çember üzerinde karmaşık eşlenik alma",
            map_description="conj: S^1 -> S^1, conj(z) = conjugate(z)",
            degree=-1,
            orientation_behavior="orientation_reversing",
            induced_fundamental_group_map="n |-> -n",
            homotopy_class="reflection",
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Karmaşık eşlenik alma yönelimi ters çevirir. Negatif derece, "
                "her ikisi de S^1 homeomorfizması olsa bile bu haritayı "
                "özdeşlikten ayırır."
            ),
        ),
    )


def circle_degree_summary() -> dict[str, list[str]]:
    """Çember derecesi profillerini yönelim davranışına göre grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_circle_degree_profiles():
        result.setdefault(profile.orientation_behavior, []).append(profile.key)
    return result


def circle_degree_by_value(degree: int) -> tuple[CircleDegreeProfile, ...]:
    """İstenen dereceye sahip çember profillerini döndür."""
    return tuple(p for p in get_circle_degree_profiles() if p.degree == degree)


@dataclass(frozen=True)
class RetractionDegreeProfile:
    """Derece teorisini retraksiyon yokluğu ifadelerine bağlayan profil."""

    key: str
    display_name: str
    ambient_space: str
    boundary_space: str
    candidate_retraction: str
    retraction_exists: bool
    degree_obstruction: str
    source_section: str
    notes: str


def get_retraction_degree_profiles() -> tuple[RetractionDegreeProfile, ...]:
    """Derece-teorik retraksiyon engeli profillerini döndür."""
    return (
        RetractionDegreeProfile(
            key="disk_to_circle_no_retraction",
            display_name="D^2'den S^1'e retraksiyon yok",
            ambient_space="D^2",
            boundary_space="S^1",
            candidate_retraction="r: D^2 -> S^1 ve r|_{S^1} = id",
            retraction_exists=False,
            degree_obstruction=(
                "Sınır dahil etmesi D^2 üzerinden uzanırsa sınırdaki derece 0 "
                "olmalıdır; retraksiyon ise özdeşlik nedeniyle derece 1'i zorlar."
            ),
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Böyle bir r var olsaydı r ile sınır dahil etmesinin bileşkesi "
                "id_S1 olurdu ve derece 1 taşırdı. Oysa D^2 üzerinden uzayan "
                "her S^1 -> S^1 haritasının derecesi 0'dır. Çelişki buradan gelir."
            ),
        ),
        RetractionDegreeProfile(
            key="ball_to_sphere_no_retraction",
            display_name="D^n'den S^(n-1)'e retraksiyon yok",
            ambient_space="D^n",
            boundary_space="S^(n-1)",
            candidate_retraction="r: D^n -> S^(n-1) ve r|_{S^(n-1)} = id",
            retraction_exists=False,
            degree_obstruction=(
                "S^(n-1) üzerindeki özdeşlik derece 1 taşır; D^n üzerinden "
                "uzayan haritalar ise karşılık gelen üst homoloji derecesinde "
                "sıfırlanır."
            ),
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Bu, Brouwer sabit nokta teoremi kanıtında kullanılan yüksek "
                "boyutlu biçimdir. Engel aynıdır: top üzerinden uzama, sınır "
                "derecesini yok eder."
            ),
        ),
        RetractionDegreeProfile(
            key="annulus_to_core_circle_retraction",
            display_name="Halka çekirdek çemberine retrakte olur",
            ambient_space="S^1 x [0, 1]",
            boundary_space="S^1 x {1/2}",
            candidate_retraction="r(z, t) = (z, 1/2)",
            retraction_exists=True,
            degree_obstruction="Engel yoktur: retraksiyon çekirdek çember üzerinde derece 1 taşır.",
            source_section="Adams & Franzosa Bölüm 9.2",
            notes=(
                "Bu pozitif örnek, derece teorisinin bütün retraksiyonları "
                "yasaklamadığını açıklaştırır. Engel, sınır küresi üzerindeki "
                "özdeşliğin bir top üzerinden uzamaya zorlanması durumunda ortaya çıkar."
            ),
        ),
    )


def retraction_degree_summary() -> dict[str, list[str]]:
    """Retraksiyon-derece profillerini varlık bayrağına göre grupla."""
    result: dict[str, list[str]] = {"retraction_exists": [], "no_retraction": []}
    for profile in get_retraction_degree_profiles():
        key = "retraction_exists" if profile.retraction_exists else "no_retraction"
        result[key].append(profile.key)
    return result


def degree_theory_profile_registry() -> dict[str, int]:
    """DEG-01 profil ailelerinin kayıt sayılarını döndür."""
    return {
        "circle_degree_profiles": len(get_circle_degree_profiles()),
        "retraction_degree_profiles": len(get_retraction_degree_profiles()),
    }


__all__ = [
    "CircleDegreeProfile",
    "RetractionDegreeProfile",
    "circle_degree_by_value",
    "circle_degree_summary",
    "degree_theory_profile_registry",
    "get_circle_degree_profiles",
    "get_retraction_degree_profiles",
    "retraction_degree_summary",
]
