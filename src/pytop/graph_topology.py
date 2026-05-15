"""Topolojik graf profil kayitlari (GTOP-01/GTOP-02/GTOP-03).

Bu modul Adams & Franzosa Bolum 13.1--13.4 icin ogretim odakli graf topolojisi
kayitlari saglar. Amac genel bir graf algoritma motoru yazmak degildir; vertex,
edge, baglantililik, gomulu graf, planarity, kimyasal graf, gecis sayisi ve
kalinlik sinyallerini paket icinde denetlenebilir bir API yuzeyi olarak
sunmaktir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TopologicalGraphProfile:
    """Topolojik graf modeli icin ogretim profili."""

    key: str
    display_name: str
    vertex_count: int
    edge_count: int
    component_count: int
    graph_model: str
    euler_characteristic: int
    source_section: str
    teaching_note: str


def get_topological_graph_profiles() -> tuple[TopologicalGraphProfile, ...]:
    """GTOP-01 icin temel topolojik graf profillerini dondur."""
    return (
        TopologicalGraphProfile(
            key="interval_graph_arc",
            display_name="Aralik grafi",
            vertex_count=2,
            edge_count=1,
            component_count=1,
            graph_model="Iki vertex ve tek edge iceren baglantili yay modeli",
            euler_characteristic=1,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Tek edge, graf topolojisinde 1-boyutlu hucre okumasina baslamak "
                "icin en kucuk baglantili modeldir."
            ),
        ),
        TopologicalGraphProfile(
            key="cycle_graph_circle",
            display_name="Cevrim grafi",
            vertex_count=4,
            edge_count=4,
            component_count=1,
            graph_model="Dort vertexli kapali poligonal cevrim",
            euler_characteristic=0,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Cevrim grafi, cemberin graf modeli gibi okunur: vertex ve edge "
                "sayilari esit oldugunda Euler karakteristigi sifirdir."
            ),
        ),
        TopologicalGraphProfile(
            key="theta_graph",
            display_name="Theta grafi",
            vertex_count=2,
            edge_count=3,
            component_count=1,
            graph_model="Iki vertex arasinda uc ayrik edge yolu",
            euler_characteristic=-1,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Theta grafi, birden fazla cevrim tasiyan baglantili 1-kompleksler "
                "icin kucuk ama ayirt edici bir ornektir."
            ),
        ),
        TopologicalGraphProfile(
            key="disconnected_two_intervals",
            display_name="Iki bilesenli aralik grafigi",
            vertex_count=4,
            edge_count=2,
            component_count=2,
            graph_model="Birbirinden ayrik iki tek-edge bileseni",
            euler_characteristic=2,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Bu profil, Euler karakteristiginin bilesen sayisi ve edge sayisi "
                "ile birlikte okunmasi gerektigini hatirlatir."
            ),
        ),
    )


@dataclass(frozen=True)
class GraphEmbeddingProfile:
    """Bir grafin yuzey veya duzlem icindeki gomulme profili."""

    key: str
    display_name: str
    graph_key: str
    ambient_space: str
    embedding_signal: str
    face_count: int | None
    source_section: str
    teaching_note: str


def get_graph_embedding_profiles() -> tuple[GraphEmbeddingProfile, ...]:
    """GTOP-01 icin temel graf gomulme profillerini dondur."""
    return (
        GraphEmbeddingProfile(
            key="cycle_graph_plane_embedding",
            display_name="Cevrim grafinin duzlem gomulmesi",
            graph_key="cycle_graph_circle",
            ambient_space="plane",
            embedding_signal="Basit kapali cevrim duzlemi ic ve dis bolgeye ayirir.",
            face_count=2,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Bu kayit, Jordan sezgisinin graf gomulmeleri icin nasil bir yuz "
                "sayimi sinyaline donustugunu gosterir."
            ),
        ),
        GraphEmbeddingProfile(
            key="theta_graph_plane_embedding",
            display_name="Theta grafinin duzlem gomulmesi",
            graph_key="theta_graph",
            ambient_space="plane",
            embedding_signal="Uc yol iki kapali bolge ve dis bolge okumasina izin verir.",
            face_count=3,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Theta grafi, V-E+F sayiminin duzlemsel gomulmede nasil izlenecegini "
                "gosteren kompakt bir sinif ornegidir."
            ),
        ),
        GraphEmbeddingProfile(
            key="interval_graph_line_embedding",
            display_name="Aralik grafinin dogru gomulmesi",
            graph_key="interval_graph_arc",
            ambient_space="line",
            embedding_signal="Tek edge kesismeden dogru parcasi gibi gomulur.",
            face_count=None,
            source_section="Adams & Franzosa Bolum 13.1",
            teaching_note=(
                "Bu profil, her topolojik graf gomulmesinin yuz sayimi gerektirmeyen "
                "daha temel bir alt uzay okumasina da sahip olabilecegini belirtir."
            ),
        ),
    )


def graph_euler_characteristic_summary() -> dict[str, int]:
    """Graf profillerini Euler karakteristigi degerine gore indeksle."""
    return {
        profile.key: profile.euler_characteristic
        for profile in get_topological_graph_profiles()
    }


def graph_embedding_ambient_summary() -> dict[str, list[str]]:
    """Graf gomulme profillerini ortam uzayina gore grupla."""
    result: dict[str, list[str]] = {}
    for profile in get_graph_embedding_profiles():
        result.setdefault(profile.ambient_space, []).append(profile.key)
    return result


def graph_topology_profile_registry() -> dict[str, int]:
    """GTOP profil ailelerinin kayit sayilarini dondur."""
    return {
        "topological_graph_profiles": len(get_topological_graph_profiles()),
        "graph_embedding_profiles": len(get_graph_embedding_profiles()),
        "graph_planarity_profiles": len(get_graph_planarity_profiles()),
        "chemical_graph_profiles": len(get_chemical_graph_profiles()),
        "graph_crossing_thickness_profiles": len(
            get_graph_crossing_thickness_profiles()
        ),
    }


@dataclass(frozen=True)
class GraphPlanarityProfile:
    """Planarity ve Kuratowski tipi uyarilar icin ogretim profili."""

    key: str
    display_name: str
    graph_model: str
    vertex_count: int
    edge_count: int
    is_planar: bool
    obstruction_signal: str
    source_section: str
    teaching_note: str


def get_graph_planarity_profiles() -> tuple[GraphPlanarityProfile, ...]:
    """GTOP-02 icin planarity profillerini dondur."""
    return (
        GraphPlanarityProfile(
            key="k5_nonplanar_profile",
            display_name="K5 duzlemsel olmayan profil",
            graph_model="Bes vertexli tam graf",
            vertex_count=5,
            edge_count=10,
            is_planar=False,
            obstruction_signal="Kuratowski engeli; her iki vertex cifti edge ile baglidir.",
            source_section="Adams & Franzosa Bolum 13.2--13.3",
            teaching_note=(
                "K5, planarity tartismasinda ilk temel engel modelidir ve duzlemde "
                "kesisimsiz gomulmenin neden her graf icin mumkun olmadigini gosterir."
            ),
        ),
        GraphPlanarityProfile(
            key="k33_nonplanar_profile",
            display_name="K3,3 duzlemsel olmayan profil",
            graph_model="Iki uclu parcali tam bipartite graf",
            vertex_count=6,
            edge_count=9,
            is_planar=False,
            obstruction_signal="Kuratowski engeli; uc ev-uc kuyu problemiyle okunur.",
            source_section="Adams & Franzosa Bolum 13.2--13.3",
            teaching_note=(
                "K3,3, bipartite yapinin bile duzlemsel gomulmeye yetmedigini "
                "gosteren klasik ikinci engel profilidir."
            ),
        ),
        GraphPlanarityProfile(
            key="cycle_graph_planar_profile",
            display_name="Cevrim grafinin planarity profili",
            graph_model="Basit kapali cevrim",
            vertex_count=4,
            edge_count=4,
            is_planar=True,
            obstruction_signal="Kuratowski engeli yok; standart duzlem gomulmesi vardir.",
            source_section="Adams & Franzosa Bolum 13.2",
            teaching_note=(
                "Cevrim grafigi, planarity icin pozitif temel modeldir ve GTOP-01 "
                "gomulme profilleriyle dogrudan baglanir."
            ),
        ),
    )


@dataclass(frozen=True)
class ChemicalGraphProfile:
    """Kimyasal graf teorisi icin ogretim profili."""

    key: str
    display_name: str
    molecule_model: str
    graph_model: str
    atom_vertex_rule: str
    bond_edge_rule: str
    topology_signal: str
    source_section: str
    teaching_note: str


def get_chemical_graph_profiles() -> tuple[ChemicalGraphProfile, ...]:
    """GTOP-02/GTOP-03 icin kimyasal graf profillerini dondur."""
    return (
        ChemicalGraphProfile(
            key="benzene_cycle_graph",
            display_name="Benzen cevrim grafigi",
            molecule_model="Benzen halkasi",
            graph_model="Alti vertexli cevrim grafigi",
            atom_vertex_rule="Karbon atomlari vertex olarak okunur.",
            bond_edge_rule="Kimyasal baglar edge olarak okunur.",
            topology_signal="Halka yapisi cevrim grafigi ve planarity profiliyle izlenir.",
            source_section="Adams & Franzosa Bolum 13.2",
            teaching_note=(
                "Benzen profili, kimyasal bag grafinin topolojik cevrim diliyle "
                "nasil temsil edilecegini gosterir."
            ),
        ),
        ChemicalGraphProfile(
            key="isomer_graph_distinction",
            display_name="Izomer graf ayrimi",
            molecule_model="Ayni atom sayili farkli baglanma duzenleri",
            graph_model="Ayni vertex sayisina sahip farkli edge iliskileri",
            atom_vertex_rule="Atom turleri etiketli vertex siniflari olarak tutulur.",
            bond_edge_rule="Baglanma duzeni edge setini belirler.",
            topology_signal="Graf izomorfizmi kimyasal izomer ayrimini modellemek icin kullanilir.",
            source_section="Adams & Franzosa Bolum 13.2",
            teaching_note=(
                "Izomer profili, ayni sayisal atom verisinin farkli graf topolojileri "
                "uretebilecegini anlatir."
            ),
        ),
    )


@dataclass(frozen=True)
class GraphCrossingThicknessProfile:
    """Planarity otesi gecis sayisi ve kalinlik profili."""

    key: str
    display_name: str
    graph_key: str
    crossing_number_signal: str
    thickness_signal: str
    chemistry_context: str
    source_section: str
    teaching_note: str


def get_graph_crossing_thickness_profiles() -> tuple[GraphCrossingThicknessProfile, ...]:
    """GTOP-03 icin gecis sayisi ve kalinlik profillerini dondur."""
    return (
        GraphCrossingThicknessProfile(
            key="k5_crossing_thickness_signal",
            display_name="K5 gecis ve kalinlik sinyali",
            graph_key="k5_nonplanar_profile",
            crossing_number_signal="Duzlem ciziminde en az bir gecis zorunlu okunur.",
            thickness_signal="K5 tek duzlemsel katmanda temsil edilemez; katman ayrimi gerekir.",
            chemistry_context="Yogun baglanma aglarinda planarity otesi gorsellestirme uyarisi.",
            source_section="Adams & Franzosa Bolum 13.4",
            teaching_note=(
                "Bu profil, planarity engelinden sonra gecis sayisi ve kalinlik "
                "olcutlerinin neden dogal oldugunu aciklar."
            ),
        ),
        GraphCrossingThicknessProfile(
            key="molecular_bond_graph_crossing_warning",
            display_name="Molekuler bag grafinda gecis uyarisi",
            graph_key="benzene_cycle_graph",
            crossing_number_signal="Cizimdeki gecis her zaman kimyasal bag kesisimi anlamina gelmez.",
            thickness_signal="Farkli temsil katmanlari molekul gorsellestirmesinde ayrilabilir.",
            chemistry_context="Molekuler bag graflari, geometrik cizimden cok baglanma topolojisini kodlar.",
            source_section="Adams & Franzosa Bolum 13.4",
            teaching_note=(
                "Kimya orneklerinde topolojik graf ile fiziksel 3B geometriyi "
                "ayirmak gerekir; cizimdeki gecis tek basina bag bilgisi degildir."
            ),
        ),
    )


def graph_planarity_summary() -> dict[str, bool]:
    """Planarity profillerini anahtarlarina gore indeksle."""
    return {
        profile.key: profile.is_planar for profile in get_graph_planarity_profiles()
    }


def chemical_graph_molecule_summary() -> dict[str, str]:
    """Kimyasal graf profillerini molekul modeline gore indeksle."""
    return {
        profile.key: profile.molecule_model
        for profile in get_chemical_graph_profiles()
    }


__all__ = [
    "ChemicalGraphProfile",
    "GraphEmbeddingProfile",
    "GraphCrossingThicknessProfile",
    "GraphPlanarityProfile",
    "TopologicalGraphProfile",
    "chemical_graph_molecule_summary",
    "get_chemical_graph_profiles",
    "get_graph_crossing_thickness_profiles",
    "get_graph_embedding_profiles",
    "get_graph_planarity_profiles",
    "get_topological_graph_profiles",
    "graph_embedding_ambient_summary",
    "graph_euler_characteristic_summary",
    "graph_planarity_summary",
    "graph_topology_profile_registry",
]
