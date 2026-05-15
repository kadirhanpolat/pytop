"""Dijital görüntü işleme topolojisi örnekleri (EMB-02).

Bu modül Adams & Franzosa Bölüm 11.3 hattı için Türkçe öğretim profilleri
sağlar. Amaç gerçek görüntü işleme algoritması yazmak değildir; dijital eğri,
4/8-bağlılık ve topolojik tutarlılık ilkelerini küçük, denetlenebilir kayıtlar
olarak paketlemektir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DigitalAdjacencyProfile:
    """Dijital düzlemde bir komşuluk seçimi profili."""

    key: str
    display_name: str
    adjacency_kind: str
    neighbor_rule: str
    typical_use: str
    topological_warning: str
    source_section: str
    teaching_note: str


def get_digital_adjacency_profiles() -> tuple[DigitalAdjacencyProfile, ...]:
    """4/8-bağlılık komşuluk profillerini döndür."""
    return (
        DigitalAdjacencyProfile(
            key="four_adjacency_pixels",
            display_name="4-bağlı piksel komşuluğu",
            adjacency_kind="4-adjacency",
            neighbor_rule="Bir piksel yalnızca yatay ve dikey komşularıyla bitişik sayılır.",
            typical_use="Nesne piksellerinde ince geçişleri ve köşe temaslarını ayrı tutmak.",
            topological_warning=(
                "Yalnızca 4-bağlılık kullanılırsa köşeden temas eden iki piksel "
                "aynı bileşen sayılmayabilir."
            ),
            source_section="Adams & Franzosa Bölüm 11.3",
            teaching_note=(
                "4-bağlılık, dijital eğrilerde sınırın çok hızlı birleşmesini "
                "engelleyen tutucu bir modeldir."
            ),
        ),
        DigitalAdjacencyProfile(
            key="eight_adjacency_pixels",
            display_name="8-bağlı piksel komşuluğu",
            adjacency_kind="8-adjacency",
            neighbor_rule="Bir piksel yatay, dikey ve çapraz komşularıyla bitişik sayılır.",
            typical_use="Arka plan veya dolgu bölgelerinde köşe temaslarını bağlı saymak.",
            topological_warning=(
                "Nesne ve arka plan için aynı anda 8-bağlılık seçilirse dijital "
                "ayrım sezgisi bozulabilir."
            ),
            source_section="Adams & Franzosa Bölüm 11.3",
            teaching_note=(
                "8-bağlılık daha cömerttir; köşegen temasları tek bileşen içinde "
                "toplar. Bu yüzden nesne/arka plan ikiliğinde dikkatli eşleştirilmelidir."
            ),
        ),
    )


@dataclass(frozen=True)
class DigitalCurveProfile:
    """Dijital eğri ve ayrım davranışı profili."""

    key: str
    display_name: str
    curve_model: str
    foreground_adjacency: str
    background_adjacency: str
    separation_behavior: str
    source_section: str
    teaching_note: str


def get_digital_curve_profiles() -> tuple[DigitalCurveProfile, ...]:
    """Dijital eğri profillerini döndür."""
    return (
        DigitalCurveProfile(
            key="simple_closed_digital_curve_4_8",
            display_name="4/8 uyumlu basit kapalı dijital eğri",
            curve_model="Sonlu piksel ızgarasında kendini kesmeyen kapalı piksel zinciri",
            foreground_adjacency="4-adjacency",
            background_adjacency="8-adjacency",
            separation_behavior=(
                "Nesne 4-bağlı, arka plan 8-bağlı okunduğunda iç/dış ayrımı daha "
                "istikrarlı izlenir."
            ),
            source_section="Adams & Franzosa Bölüm 11.3",
            teaching_note=(
                "Bu profil dijital Jordan sezgisini paketler: sürekli düzlemdeki "
                "ayrımın pikselli dünyada komşuluk seçimine bağlı olduğunu gösterir."
            ),
        ),
        DigitalCurveProfile(
            key="diagonal_touching_curve_warning",
            display_name="Köşeden temas eden dijital eğri uyarısı",
            curve_model="İki piksel parçası yalnızca köşede temas eder",
            foreground_adjacency="8-adjacency",
            background_adjacency="4-adjacency",
            separation_behavior=(
                "Köşe teması nesneyi bağlı yapabilir; arka planın ayrımı ise ters "
                "komşuluk seçimine göre değişir."
            ),
            source_section="Adams & Franzosa Bölüm 11.3",
            teaching_note=(
                "Aynı piksel resmi, seçilen komşuluk kuralına göre farklı topolojik "
                "sonuçlar verebilir. EMB-02'nin ana uyarısı budur."
            ),
        ),
    )


@dataclass(frozen=True)
class DigitalImageSegmentationProfile:
    """Görüntü bölütleme için topolojik kontrol profili."""

    key: str
    display_name: str
    segmentation_task: str
    topology_signal: str
    failure_mode: str
    source_section: str
    teaching_note: str


def get_digital_image_segmentation_profiles() -> tuple[DigitalImageSegmentationProfile, ...]:
    """Dijital görüntü bölütleme profillerini döndür."""
    return (
        DigitalImageSegmentationProfile(
            key="boundary_detection_component_count",
            display_name="Sınır bulmada bileşen sayısı kontrolü",
            segmentation_task="Eşiklenmiş görüntüde nesne sınırını izlemek",
            topology_signal=(
                "Bağlı bileşen sayısı ve delik sayısı, bölütlemenin topolojik "
                "olarak beklenen nesneyle uyumlu olup olmadığını gösterir."
            ),
            failure_mode=(
                "Gürültü tek piksellik köprüler veya kopukluklar üreterek yanlış "
                "bileşen sayısına yol açabilir."
            ),
            source_section="Adams & Franzosa Bölüm 11.3",
            teaching_note=(
                "Bu profil, topolojik sinyalin piksel düzeyindeki gürültüyü "
                "fark etmek için nasıl kullanılacağını özetler."
            ),
        ),
        DigitalImageSegmentationProfile(
            key="foreground_background_duality",
            display_name="Nesne-arka plan komşuluk ikiliği",
            segmentation_task="Siyah-beyaz görüntüde nesne ve arka planı birlikte okumak",
            topology_signal=(
                "Nesne için 4-bağlılık seçiliyorsa arka plan için 8-bağlılık, "
                "nesne için 8-bağlılık seçiliyorsa arka plan için 4-bağlılık "
                "kullanmak ayrım paradokslarını azaltır."
            ),
            failure_mode=(
                "Aynı komşuluk kuralını iki tarafa da uygulamak, hem nesnenin hem "
                "arka planın aynı anda beklenmedik biçimde bağlı görünmesine yol açabilir."
            ),
            source_section="Adams & Franzosa Bölüm 11.3",
            teaching_note=(
                "Dijital görüntü topolojisi yalnızca piksel listesi değil, komşuluk "
                "sözleşmesiyle birlikte anlam kazanır."
            ),
        ),
    )


def digital_image_topology_registry() -> dict[str, int]:
    """EMB-02 profil ailelerinin kayıt sayılarını döndür."""
    return {
        "digital_adjacency_profiles": len(get_digital_adjacency_profiles()),
        "digital_curve_profiles": len(get_digital_curve_profiles()),
        "digital_image_segmentation_profiles": len(
            get_digital_image_segmentation_profiles()
        ),
    }


__all__ = [
    "DigitalAdjacencyProfile",
    "DigitalCurveProfile",
    "DigitalImageSegmentationProfile",
    "digital_image_topology_registry",
    "get_digital_adjacency_profiles",
    "get_digital_curve_profiles",
    "get_digital_image_segmentation_profiles",
]
