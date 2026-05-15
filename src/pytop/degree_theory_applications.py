"""Degree theory applications (DEG-02).

DEG-02 keeps the package's profile-first style while adding Turkish teaching
records for two Adams & Franzosa Chapter 9 application lanes: the topological
proof of the Fundamental Theorem of Algebra and the heartbeat/biology degree
model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FundamentalTheoremAlgebraProfile:
    """Türkçe öğretim profili: cebirin temel teoremi ve derece teorisi."""

    key: str
    display_name: str
    polynomial_family: str
    topological_setup: str
    degree_argument: str
    conclusion: str
    source_section: str
    teaching_note: str


def get_fundamental_theorem_algebra_profiles() -> tuple[FundamentalTheoremAlgebraProfile, ...]:
    """Cebirin temel teoremine ait derece-teorisi profillerini döndür."""
    return (
        FundamentalTheoremAlgebraProfile(
            key="fta_monic_polynomial_degree_n",
            display_name="Monik polinom için topolojik FTA profili",
            polynomial_family="p(z) = z^n + a_{n-1}z^{n-1} + ... + a_0, n >= 1",
            topological_setup=(
                "Büyük yarıçaplı bir çember üzerinde p(z), baş terim z^n ile "
                "homotopiktir; çember görüntüsü orijini sarmadan yok edilemez."
            ),
            degree_argument=(
                "z |-> z^n haritasının S^1 üzerindeki derecesi n'dir. Eğer p "
                "hiç kök taşımasaydı p/|p|: S^1 -> S^1 haritası diske doğru "
                "uzatılabilir ve derece 0 olmak zorunda kalırdı. Bu, derece n "
                "ile çelişir."
            ),
            conclusion="Her sabit olmayan karmaşık polinom en az bir karmaşık köke sahiptir.",
            source_section="Adams & Franzosa Section 9.3",
            teaching_note=(
                "Bu profil cebirsel bir kök bulma algoritması değildir; "
                "derecenin homotopi altında değişmemesiyle varlık kanıtını "
                "paketler."
            ),
        ),
        FundamentalTheoremAlgebraProfile(
            key="fta_linear_boundary_winding",
            display_name="Doğrusal polinom için sınır sarma profili",
            polynomial_family="p(z) = z - a",
            topological_setup=(
                "a noktasını içeren büyük bir disk seçildiğinde p, diskin "
                "sınır çemberini orijin etrafında bir kez dolaştırır."
            ),
            degree_argument=(
                "Sınırdaki normalize harita p/|p| derece 1 taşır. İçeride kök "
                "olmasaydı normalize harita diske uzar ve derece 0 olurdu."
            ),
            conclusion="Doğrusal örnek, genel FTA kanıtındaki derece çelişkisinin en yalın modelidir.",
            source_section="Adams & Franzosa Section 9.3",
            teaching_note=(
                "Öğrenci burada derece 1'in geometrik anlamını görür: sınır "
                "görüntüsü orijini bir kez sarar ve bu sarım içeride bir sıfır "
                "olmadan kaybolamaz."
            ),
        ),
    )


def fta_profile_summary() -> dict[str, int]:
    """FTA profilleri için küçük bir kayıt özeti döndür."""
    return {
        "fundamental_theorem_algebra_profiles": len(
            get_fundamental_theorem_algebra_profiles()
        )
    }


@dataclass(frozen=True)
class HeartbeatDegreeModelProfile:
    """Türkçe öğretim profili: kalp atışı modelinde derece sezgisi."""

    key: str
    display_name: str
    biological_context: str
    phase_space: str
    degree_signal: str
    interpretation: str
    source_section: str
    teaching_note: str


def get_heartbeat_degree_model_profiles() -> tuple[HeartbeatDegreeModelProfile, ...]:
    """Kalp atışı/biyoloji uygulama profillerini döndür."""
    return (
        HeartbeatDegreeModelProfile(
            key="heartbeat_phase_return_map",
            display_name="Kalp atışı faz dönüş haritası",
            biological_context=(
                "Periyodik bir kalp atımı döngüsü, faz çemberi üzerinde geri "
                "dönüş haritası olarak modellenir."
            ),
            phase_space="S^1 faz çemberi; her nokta döngü içindeki bir fazı temsil eder.",
            degree_signal=(
                "Düzenli bir döngüde geri dönüş haritası çemberi çember etrafında "
                "bir kez dolaştırır; derece 1 stabil ritim sinyali olarak okunur."
            ),
            interpretation=(
                "Derece, modelin ayrıntılı diferansiyel denklemini çözmeden, "
                "faz döngüsünün topolojik olarak kaybolmadığını gösteren kaba ama "
                "dayanıklı bir işarettir."
            ),
            source_section="Adams & Franzosa Section 9.4",
            teaching_note=(
                "Bu kayıt tıbbi tanı aracı değildir. Amaç, biyolojik döngülerin "
                "topolojik dereceyle nasıl öğretilebilir hale getirileceğini "
                "göstermektir."
            ),
        ),
        HeartbeatDegreeModelProfile(
            key="heartbeat_arrhythmia_contrast",
            display_name="Ritim bozulması için derece-kontrast profili",
            biological_context=(
                "Düzensiz ritimlerde faz dönüşü hâlâ çember üzerinde izlenebilir, "
                "ama sarma davranışı düzenli döngüden sapabilir."
            ),
            phase_space="S^1 üzerinde faz kayması ve geri dönüş gözlemi",
            degree_signal=(
                "Derece değişmezliği, küçük bozulmalar altında temel sarma "
                "sayısının korunmasını; büyük bozulmalarda ise model varsayımlarının "
                "yeniden denetlenmesi gerektiğini anlatır."
            ),
            interpretation=(
                "Topolojik model, sürekli bozulmalarla gerçek kopuşları ayırmak "
                "için kavramsal bir dil sağlar."
            ),
            source_section="Adams & Franzosa Section 9.4",
            teaching_note=(
                "Öğrenci açısından kritik nokta şudur: derece sayısal bir ritim "
                "ölçümü değil, döngüsel yapının korunup korunmadığını izleyen "
                "topolojik bir özettir."
            ),
        ),
    )


def heartbeat_degree_summary() -> dict[str, int]:
    """Kalp atışı derece modeli için kayıt özeti döndür."""
    return {
        "heartbeat_degree_model_profiles": len(get_heartbeat_degree_model_profiles())
    }


def degree_theory_applications_registry() -> dict[str, int]:
    """DEG-02 profil ailelerinin kayıt sayılarını döndür."""
    return {
        **fta_profile_summary(),
        **heartbeat_degree_summary(),
    }


__all__ = [
    "FundamentalTheoremAlgebraProfile",
    "HeartbeatDegreeModelProfile",
    "degree_theory_applications_registry",
    "fta_profile_summary",
    "get_fundamental_theorem_algebra_profiles",
    "get_heartbeat_degree_model_profiles",
    "heartbeat_degree_summary",
]
