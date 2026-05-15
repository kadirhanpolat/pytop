"""Gömü profilleri ve Jordan eğri hattı (EMB-01).

Bu modül Adams & Franzosa Bölüm 11.1--11.2 için Türkçe öğretim kayıtları
sağlar. Amaç genel gömü tanıma algoritması yazmak değildir; Jordan eğrisi,
çember/disk gömüleri ve Alexander Boynuzlu Küre gibi standart örnekleri
profil tabanlı biçimde görünür kılmaktır.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingProfile:
    """Bir topolojik gömü örneği için öğretim profili."""

    key: str
    display_name: str
    domain: str
    ambient_space: str
    embedding_description: str
    is_embedding: bool
    source_section: str
    teaching_note: str


def get_embedding_profiles() -> tuple[EmbeddingProfile, ...]:
    """Standart gömü örneklerini döndür."""
    return (
        EmbeddingProfile(
            key="circle_standard_embedding_plane",
            display_name="S^1'in düzlemde standart gömüsü",
            domain="S^1",
            ambient_space="R^2",
            embedding_description="t |-> (cos t, sin t)",
            is_embedding=True,
            source_section="Adams & Franzosa Bölüm 11.1",
            teaching_note=(
                "Bu örnek gömü kavramının en temel modelidir: harita birebirdir, "
                "süreklidir ve görüntüsü üzerinde homeomorfizma verir."
            ),
        ),
        EmbeddingProfile(
            key="interval_arc_embedding_plane",
            display_name="[0,1] aralığının düzlemde yay olarak gömüsü",
            domain="[0,1]",
            ambient_space="R^2",
            embedding_description="t |-> (t, t(1-t))",
            is_embedding=True,
            source_section="Adams & Franzosa Bölüm 11.1",
            teaching_note=(
                "Kapalı aralık kompakt olduğu ve düzlem Hausdorff olduğu için "
                "birebir sürekli model, görüntüsü üzerine homeomorfizma olarak okunur."
            ),
        ),
        EmbeddingProfile(
            key="figure_eight_immersion_not_embedding",
            display_name="Sekiz şekli: gömü olmayan immersiyon kontrastı",
            domain="S^1",
            ambient_space="R^2",
            embedding_description="kendini kesen sekiz şekli parametrizasyonu",
            is_embedding=False,
            source_section="Adams & Franzosa Bölüm 11.1",
            teaching_note=(
                "Kendi kendini kesme noktası birebirliği bozar. Bu örnek, her "
                "güzel görünen parametrik eğrinin gömü olmadığını hatırlatır."
            ),
        ),
    )


def embedding_status_summary() -> dict[str, list[str]]:
    """Gömü profillerini gömü olup olmamalarına göre grupla."""
    result: dict[str, list[str]] = {"embedding": [], "not_embedding": []}
    for profile in get_embedding_profiles():
        key = "embedding" if profile.is_embedding else "not_embedding"
        result[key].append(profile.key)
    return result


@dataclass(frozen=True)
class JordanCurveProfile:
    """Jordan Eğri Teoremi için öğretim profili."""

    key: str
    display_name: str
    curve_model: str
    theorem_statement: str
    inside_region: str
    outside_region: str
    source_section: str
    teaching_note: str


def get_jordan_curve_profiles() -> tuple[JordanCurveProfile, ...]:
    """Jordan Eğri Teoremi profillerini döndür."""
    return (
        JordanCurveProfile(
            key="standard_circle_jordan_curve",
            display_name="Standart çember Jordan eğrisi",
            curve_model="S^1'in R^2 içindeki standart görüntüsü",
            theorem_statement=(
                "Basit kapalı bir eğri düzlemi iki bileşene ayırır: sınırlı iç "
                "bölge ve sınırsız dış bölge."
            ),
            inside_region="Açık bir diskle homeomorf sınırlı bileşen",
            outside_region="Sınırsız dış bileşen",
            source_section="Adams & Franzosa Bölüm 11.2",
            teaching_note=(
                "Standart çember sezgisel olarak açık görünür, fakat teorem "
                "bütün basit kapalı eğriler için aynı ayrımın geçerli olduğunu söyler."
            ),
        ),
        JordanCurveProfile(
            key="wild_polygonal_jordan_curve",
            display_name="Kırıklı ama basit kapalı Jordan eğrisi",
            curve_model="Kendi kendini kesmeyen çokgenal kapalı eğri",
            theorem_statement=(
                "Köşeli veya pürüzlü olmak ayrımı bozmaz; eğri basit ve kapalı "
                "olduğu sürece düzlem iki bileşene ayrılır."
            ),
            inside_region="Çokgenin iç bölgesi",
            outside_region="Çokgenin dış bölgesi",
            source_section="Adams & Franzosa Bölüm 11.2",
            teaching_note=(
                "Bu profil, düzgünlük varsayımının topolojik sonuç için zorunlu "
                "olmadığını vurgular."
            ),
        ),
    )


@dataclass(frozen=True)
class AlexanderHornedSphereProfile:
    """Alexander Boynuzlu Küre için uyarı profili."""

    key: str
    display_name: str
    embedded_space: str
    ambient_space: str
    tame_or_wild: str
    complement_behavior: str
    source_section: str
    teaching_note: str


def get_alexander_horned_sphere_profiles() -> tuple[AlexanderHornedSphereProfile, ...]:
    """Alexander Boynuzlu Küre profilini döndür."""
    return (
        AlexanderHornedSphereProfile(
            key="alexander_horned_sphere_wild_embedding",
            display_name="Alexander Boynuzlu Küre: vahşi gömü",
            embedded_space="S^2",
            ambient_space="R^3",
            tame_or_wild="wild",
            complement_behavior=(
                "Görüntü S^2'ye homeomorf olsa da tümleyen beklenen basit "
                "bağlantılılık davranışını göstermez."
            ),
            source_section="Adams & Franzosa Bölüm 11.2",
            teaching_note=(
                "Bu örnek, Jordan-Brouwer ayrım sezgisinin yüksek boyutta ne kadar "
                "dikkatli kullanılması gerektiğini gösterir: gömülen uzay standart "
                "olabilir, ama gömülüş biçimi vahşi olabilir."
            ),
        ),
    )


def embedding_profile_registry() -> dict[str, int]:
    """EMB-01 profil ailelerinin kayıt sayılarını döndür."""
    return {
        "embedding_profiles": len(get_embedding_profiles()),
        "jordan_curve_profiles": len(get_jordan_curve_profiles()),
        "alexander_horned_sphere_profiles": len(get_alexander_horned_sphere_profiles()),
    }


__all__ = [
    "AlexanderHornedSphereProfile",
    "EmbeddingProfile",
    "JordanCurveProfile",
    "embedding_profile_registry",
    "embedding_status_summary",
    "get_alexander_horned_sphere_profiles",
    "get_embedding_profiles",
    "get_jordan_curve_profiles",
]
