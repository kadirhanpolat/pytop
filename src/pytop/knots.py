"""Dugum teorisi profil kayitlari (KNOT-01/KNOT-02/KNOT-03).

Bu modul Adams & Franzosa Bolum 12.1--12.4 icin ogretim odakli kayitlar
saglar. Amac dugum diyagramlarini algoritmik olarak siniflandirmak degildir;
temel dugum, link, Reidemeister hamlesi, sembolik degismez ve uygulama
profillerini paket icinde denetlenebilir bir API yuzeyi olarak sunmaktir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnotProfile:
    """Temel bir dugum modeli icin ogretim profili."""

    key: str
    display_name: str
    diagram_model: str
    crossing_count: int
    orientable_context: str
    source_section: str
    teaching_note: str


def get_knot_profiles() -> tuple[KnotProfile, ...]:
    """Adams & Franzosa hattina uygun temel dugum profillerini dondur."""
    return (
        KnotProfile(
            key="unknot_baseline",
            display_name="Cozuk dugum temel modeli",
            diagram_model="Duzlemde kesisimsiz kapali halka diyagrami",
            crossing_count=0,
            orientable_context="Yon secimi degismezligi etkilemez; dugum cozuk dugumdur.",
            source_section="Adams & Franzosa Bolum 12.1",
            teaching_note=(
                "Cozuk dugum, butun dugum profilleri icin referans modeldir: kapali "
                "egri vardir, fakat zorunlu kesisim veya dolanma bilgisi yoktur."
            ),
        ),
        KnotProfile(
            key="trefoil_knot",
            display_name="Uc yaprakli dugum",
            diagram_model="Uc kesisimli standart trefoil diyagrami",
            crossing_count=3,
            orientable_context="Yonlendirme secimi sag/sol elli trefoil karsilastirmasini acabilir.",
            source_section="Adams & Franzosa Bolum 12.1",
            teaching_note=(
                "Trefoil, cozuk dugumden farkli oldugu sezgisel olarak gorulen en "
                "kucuk kesisim sayili klasik ornektir."
            ),
        ),
        KnotProfile(
            key="figure_eight_knot",
            display_name="Sekiz dugumu",
            diagram_model="Dort kesisimli figure-eight dugum diyagrami",
            crossing_count=4,
            orientable_context="Ayna simetrisi ve yon tartismalari icin standart kontrasttir.",
            source_section="Adams & Franzosa Bolum 12.1",
            teaching_note=(
                "Sekiz dugumu, trefoil sonrasinda kesisim sayisi ve ayna davranisi "
                "karsilastirmasi icin dogal ikinci modeldir."
            ),
        ),
        KnotProfile(
            key="cinquefoil_knot",
            display_name="Bes yaprakli dugum",
            diagram_model="Bes kesisimli torus dugumu ornegi",
            crossing_count=5,
            orientable_context="Torus dugumleri ailesine gecis icin okunur.",
            source_section="Adams & Franzosa Bolum 12.1",
            teaching_note=(
                "Cinquefoil profili, temel katalogun yalnizca trefoil ve sekiz "
                "dugumunden ibaret olmadigini gosterir."
            ),
        ),
    )


@dataclass(frozen=True)
class LinkProfile:
    """Birden fazla bilesenli link modeli icin ogretim profili."""

    key: str
    display_name: str
    component_count: int
    diagram_model: str
    basic_linking_signal: str
    source_section: str
    teaching_note: str


def get_link_profiles() -> tuple[LinkProfile, ...]:
    """Temel link profillerini dondur."""
    return (
        LinkProfile(
            key="unlink_two_components",
            display_name="Iki bilesenli cozuk link",
            component_count=2,
            diagram_model="Birbirine dolanmayan iki ayrik halka",
            basic_linking_signal="Baglanti sinyali yok; bilesenler ayrilabilir okunur.",
            source_section="Adams & Franzosa Bolum 12.1",
            teaching_note=(
                "Cozuk link, link kuraminin cozuk dugum karsiligidir ve Hopf link "
                "ile karsilastirma icin temel zemindir."
            ),
        ),
        LinkProfile(
            key="hopf_link",
            display_name="Hopf link",
            component_count=2,
            diagram_model="Birbirine bir kez dolanan iki halka",
            basic_linking_signal=(
                "Iki bilesen dolanik ve ayrilamaz; yonlu okumada baglanti sayisi "
                "hattina hazirlar."
            ),
            source_section="Adams & Franzosa Bolum 12.1",
            teaching_note=(
                "Hopf link, dugumden linke gecisi en az karmasayla gosteren modeldir: "
                "her bilesen tek basina cozuk gorunse de birlikte dolaniktir."
            ),
        ),
    )


@dataclass(frozen=True)
class ReidemeisterMoveProfile:
    """Reidemeister hamlesi icin ogretim profili."""

    key: str
    display_name: str
    move_type: str
    local_effect: str
    preserves_knot_type: bool
    source_section: str
    teaching_note: str


def get_reidemeister_move_profiles() -> tuple[ReidemeisterMoveProfile, ...]:
    """R1, R2 ve R3 Reidemeister hamle profillerini dondur."""
    return (
        ReidemeisterMoveProfile(
            key="reidemeister_r1",
            display_name="Reidemeister I",
            move_type="R1",
            local_effect="Tek bir bukle ekler veya kaldirir.",
            preserves_knot_type=True,
            source_section="Adams & Franzosa Bolum 12.2",
            teaching_note=(
                "R1 hamlesi, diyagramdaki yerel buklenin dugum tipini degistirmeden "
                "eklenip silinebilecegini gosterir."
            ),
        ),
        ReidemeisterMoveProfile(
            key="reidemeister_r2",
            display_name="Reidemeister II",
            move_type="R2",
            local_effect="Karsit iki kesisimi birlikte ekler veya kaldirir.",
            preserves_knot_type=True,
            source_section="Adams & Franzosa Bolum 12.2",
            teaching_note=(
                "R2, iki yerel kesisimin birbirini iptal edebilecegi diyagram "
                "okumasini temsil eder."
            ),
        ),
        ReidemeisterMoveProfile(
            key="reidemeister_r3",
            display_name="Reidemeister III",
            move_type="R3",
            local_effect="Uc ip parcasi arasindaki kesisim siralamasini kaydirir.",
            preserves_knot_type=True,
            source_section="Adams & Franzosa Bolum 12.2",
            teaching_note=(
                "R3, dugum diyagraminda yerel gecislerin kaydirilmasinin izotopi "
                "tipini korudugunu vurgular."
            ),
        ),
    )


def knot_crossing_summary() -> dict[str, int]:
    """Temel dugum profillerini kesisim sayilarina gore indeksle."""
    return {profile.key: profile.crossing_count for profile in get_knot_profiles()}


def knot_theory_profile_registry() -> dict[str, int]:
    """KNOT-01/KNOT-02/KNOT-03 profil ailelerinin kayit sayilarini dondur."""
    return {
        "knot_profiles": len(get_knot_profiles()),
        "link_profiles": len(get_link_profiles()),
        "reidemeister_move_profiles": len(get_reidemeister_move_profiles()),
        "knot_invariant_profiles": len(get_knot_invariant_profiles()),
        "knot_application_profiles": len(get_knot_application_profiles()),
    }


@dataclass(frozen=True)
class KnotInvariantProfile:
    """Bir dugum veya link degismezinin ogretim profili."""

    key: str
    display_name: str
    invariant_kind: str
    applies_to: str
    symbolic_value: str
    normalization_note: str
    source_section: str
    teaching_note: str


def get_knot_invariant_profiles() -> tuple[KnotInvariantProfile, ...]:
    """KNOT-02 icin sembolik dugum degismez profillerini dondur."""
    return (
        KnotInvariantProfile(
            key="hopf_link_linking_number",
            display_name="Hopf link baglanti sayisi",
            invariant_kind="linking_number",
            applies_to="hopf_link",
            symbolic_value="+1 veya -1; yonlendirme secimine baglidir",
            normalization_note=(
                "KNOT-02 bu degeri hesaplama motoru olarak degil, yonlu link "
                "okumasinda isaretli baglanti sinyali olarak kaydeder."
            ),
            source_section="Adams & Franzosa Bolum 12.3",
            teaching_note=(
                "Baglanti sayisi, iki bilesenli linklerde her bilesen cozuk olsa bile "
                "bilesenlerin birlikte ayrilamazligini olcen ilk sayisal degismezdir."
            ),
        ),
        KnotInvariantProfile(
            key="unlink_linking_number_zero",
            display_name="Cozuk link baglanti sayisi",
            invariant_kind="linking_number",
            applies_to="unlink_two_components",
            symbolic_value="0",
            normalization_note="Ayrilabilir iki bilesenli cozuk link icin baglanti sinyali yoktur.",
            source_section="Adams & Franzosa Bolum 12.3",
            teaching_note=(
                "Bu profil Hopf link ile yan yana okunur: iki bilesen sayisi ayni "
                "kalirken baglanti sayisi link tipini ayirt etmeye yardim eder."
            ),
        ),
        KnotInvariantProfile(
            key="trefoil_alexander_polynomial",
            display_name="Trefoil Alexander polinomu",
            invariant_kind="alexander_polynomial",
            applies_to="trefoil_knot",
            symbolic_value="t^-1 - 1 + t",
            normalization_note=(
                "Polinom birim carpan ve t kuvveti kaydirma secimlerine kadar "
                "okunur; kayit ogretim amacli simetrik normalizasyon kullanir."
            ),
            source_section="Adams & Franzosa Bolum 12.3",
            teaching_note=(
                "Alexander polinomu, Reidemeister hamleleri altinda korunan daha "
                "zengin cebirsel bir dugum degismezine gecis kapisidir."
            ),
        ),
        KnotInvariantProfile(
            key="unknot_alexander_polynomial",
            display_name="Cozuk dugum Alexander polinomu",
            invariant_kind="alexander_polynomial",
            applies_to="unknot_baseline",
            symbolic_value="1",
            normalization_note="Cozuk dugum, Alexander polinomu icin temel referans degeridir.",
            source_section="Adams & Franzosa Bolum 12.3",
            teaching_note=(
                "Cozuk dugumun polinomu, polinom degismezlerinin ayirt edici gucunu "
                "anlatmak icin baslangic sabitidir."
            ),
        ),
        KnotInvariantProfile(
            key="trefoil_jones_polynomial",
            display_name="Trefoil Jones polinomu",
            invariant_kind="jones_polynomial",
            applies_to="trefoil_knot",
            symbolic_value="q^-1 + q^-3 - q^-4",
            normalization_note=(
                "Jones polinomu icin farkli degisken ve ayna normalizasyonlari "
                "kullanilabilir; bu kayit sembolik ogretim modeli olarak tutulur."
            ),
            source_section="Adams & Franzosa Bolum 12.3",
            teaching_note=(
                "Jones polinomu, skein iliskileri ve ayna ayrimi uzerinden dugum "
                "teorisinin cebirsel yonunu gorunur kilar."
            ),
        ),
        KnotInvariantProfile(
            key="unknot_jones_polynomial",
            display_name="Cozuk dugum Jones polinomu",
            invariant_kind="jones_polynomial",
            applies_to="unknot_baseline",
            symbolic_value="1",
            normalization_note="Cozuk dugum, Jones polinomu icin temel referans degeridir.",
            source_section="Adams & Franzosa Bolum 12.3",
            teaching_note=(
                "Bu profil, Jones polinomunun cozuk dugumu hangi normal degerle "
                "baslattigini acik hale getirir."
            ),
        ),
    )


def knot_invariant_kind_summary() -> dict[str, list[str]]:
    """Degismez profillerini degismez turune gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_knot_invariant_profiles():
        result.setdefault(profile.invariant_kind, []).append(profile.key)
    return result


@dataclass(frozen=True)
class KnotApplicationProfile:
    """Dugum teorisi uygulamasi icin ogretim profili."""

    key: str
    display_name: str
    application_domain: str
    topological_object: str
    application_signal: str
    source_section: str
    teaching_note: str


def get_knot_application_profiles() -> tuple[KnotApplicationProfile, ...]:
    """KNOT-03 icin DNA ve kimya uygulama profillerini dondur."""
    return (
        KnotApplicationProfile(
            key="dna_supercoiling_topology",
            display_name="DNA supercoiling topolojisi",
            application_domain="dna_topology",
            topological_object="Kapali DNA halkasi ve supercoil dugum/link modeli",
            application_signal=(
                "DNA uzerindeki dolanma, bukulme ve baglanti verisi biyolojik "
                "durum degisimlerini topolojik olarak izlenebilir kilar."
            ),
            source_section="Adams & Franzosa Bolum 12.4",
            teaching_note=(
                "Bu profil, dugum teorisinin soyut diyagramlardan biyolojik DNA "
                "topolojisine nasil tasindigini gosteren ana KNOT-03 ornegidir."
            ),
        ),
        KnotApplicationProfile(
            key="topoisomerase_strand_passage",
            display_name="Topoizomeraz gecis uyarisi",
            application_domain="dna_topology",
            topological_object="DNA iplik gecisi ve enzim etkisi",
            application_signal=(
                "Topoizomeraz islemi gercek topolojik tipi degistirebilir; bu, "
                "yalnizca duzlem diyagraminda yapilan Reidemeister hamlesi degildir."
            ),
            source_section="Adams & Franzosa Bolum 12.4",
            teaching_note=(
                "Reidemeister hamleleri dugum tipini korurken topoizomeraz gecisi "
                "biyolojik surecte dugum veya link sinifini degistirebilir."
            ),
        ),
        KnotApplicationProfile(
            key="synthetic_chemistry_chiral_knots",
            display_name="Kiral molekuler dugumler",
            application_domain="chemical_topology",
            topological_object="Sag ve sol elli molekuler trefoil benzeri yapilar",
            application_signal=(
                "Ayna goruntusuyle cakismayan dugumlu molekuller kiralite ve "
                "sentez okumasinda topolojik ayirt edici verir."
            ),
            source_section="Adams & Franzosa Bolum 12.4",
            teaching_note=(
                "Trefoilin sag/sol elli ayrimi, kimyasal kiralite anlatimina "
                "baglanarak dugum teorisinin laboratuvar motivasyonunu aciklar."
            ),
        ),
        KnotApplicationProfile(
            key="molecular_link_detection",
            display_name="Molekuler link tespiti",
            application_domain="chemical_topology",
            topological_object="Birbirine bagli molekuler halkalar",
            application_signal=(
                "Baglanti sayisi ve polinom profilleri, molekuler halkalarin "
                "ayrilabilir mi yoksa linkli mi oldugunu ogretim duzeyinde isaretler."
            ),
            source_section="Adams & Franzosa Bolum 12.4",
            teaching_note=(
                "KNOT-02 degismezleri burada uygulamaya baglanir: linkli molekuler "
                "halkalari ayirt etmek icin sayisal ve sembolik sinyaller kullanilir."
            ),
        ),
    )


def knot_application_domain_summary() -> dict[str, list[str]]:
    """Uygulama profillerini uygulama alanina gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_knot_application_profiles():
        result.setdefault(profile.application_domain, []).append(profile.key)
    return result


__all__ = [
    "KnotProfile",
    "LinkProfile",
    "KnotInvariantProfile",
    "KnotApplicationProfile",
    "ReidemeisterMoveProfile",
    "get_knot_profiles",
    "get_link_profiles",
    "get_knot_invariant_profiles",
    "get_knot_application_profiles",
    "get_reidemeister_move_profiles",
    "knot_application_domain_summary",
    "knot_invariant_kind_summary",
    "knot_crossing_summary",
    "knot_theory_profile_registry",
]
