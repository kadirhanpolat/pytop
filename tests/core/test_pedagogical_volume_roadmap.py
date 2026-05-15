from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_engelking_level_scope_matrix_exists_and_declares_non_destructive_policy():
    text = _read("docs/roadmap/engelking_level_scope_matrix.md")
    assert "pytop v0.1.25" in text
    assert "No text, examples, or proofs are copied" in text
    assert "Physical reorganization" in text
    assert "Function spaces and compact-open topology" in text
    assert "Dimension theory" in text
    assert "Uniform spaces" in text
    assert "Proximity spaces" in text


def test_pedagogical_volume_map_defines_six_cilt_architecture():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "pytop v0.1.36" in text
    assert "six-cilt" in text
    assert "Cilt I" in text
    assert "Cilt VI" in text
    assert "Undergraduate" in text
    assert "Master's" in text
    assert "Doctoral" in text
    assert "v0.2.0" in text


def test_pedagogical_volume_map_declares_route_identifiers():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    for token in ("UG-I-01", "UG-II-22", "MS-III-29", "MS-IV-42", "DR-V-49", "DR-VI-52"):
        assert token in text
    for prefix in ("M:", "QC:", "NB:", "QB:", "PLANNED:"):
        assert prefix in text
    assert "src/pytop_questionbank/chapter_01_item_families.py" in text
    assert "notebooks/exploration/11_nets.ipynb" in text
    assert "manuscript/volume_3/chapters/36_advanced_directions_and_research_paths.tex" in text


def test_level_based_roadmap_preserves_versioned_phase_boundaries():
    text = _read("docs/roadmap/level_based_engelking_integration_roadmap.md")
    for token in ("v0.1.25", "v0.1.30", "v0.1.64", "v0.1.80", "v0.1.96", "v0.2.0"):
        assert token in text
    assert "Create function-spaces chapter skeleton" in text
    assert "Physical reorganization threshold" in text


def test_pedagogical_volume_map_classifies_existing_manuscript_chapters():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "v0.1.27 existing manuscript chapter classification register" in text
    for token in ("keep", "strengthen", "split", "move-pedagogically", "postpone"):
        assert token in text
    for chapter in (
        "volume_1/15_metric_spaces",
        "volume_2/18_neighborhood_systems",
        "volume_3/32_tightness_and_network_invariants",
        "volume_3/36_advanced_directions_and_research_paths",
    ):
        assert chapter in text
    assert "every physical chapter from 1 through 36 has exactly one primary classification" in text

def test_pedagogical_volume_map_records_physical_renumbering_risks():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "v0.1.28 physical renumbering risk report" in text
    for token in (
        "LaTeX assembly",
        "Assessment surfaces",
        "Notebook surfaces",
        "Questionbank contracts",
        "Split chapters",
        "No-move gate",
        "do not physically renumber yet",
    ):
        assert token in text
    for route in ("UG-I-03", "MS-III-23", "DR-V-43", "DR-VI-60"):
        assert route in text


def test_pedagogical_volume_map_adds_level_reading_routes():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "v0.1.29 level reading routes" in text
    for token in (
        "UG-READING-ROUTE-A",
        "UG-READING-ROUTE-B",
        "MS-READING-ROUTE-A",
        "MS-READING-ROUTE-B",
        "DR-READING-ROUTE-A",
        "DR-READING-ROUTE-B",
        "Recommended undergraduate sequence",
        "Recommended master's sequence",
        "Recommended doctoral sequence",
        "Cross-level gate after v0.1.29",
    ):
        assert token in text
    for route_id in ("UG-I-01", "UG-II-22", "MS-III-23", "MS-IV-42", "DR-V-43", "DR-VI-60"):
        assert route_id in text
    assert "not file-move instructions" in text
    assert "no-move gate remains active" in text



def test_roadmap_refresh_and_phase_one_handoff_remain_without_file_moves():
    project = _read("PROJECT_ROADMAP.md")
    current = _read("docs/roadmap/current_roadmap.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    level = _read("docs/roadmap/level_based_engelking_integration_roadmap.md")

    for text in (project, current, map_text, level):
        assert "v0.1.32" in text
        assert "Cilt I" in text
        assert "physical" in text.lower()

    assert "continues Phase 1" in current
    assert "Phase 0 closure table" in map_text
    assert "v0.1.31 Cilt I foundation-strengthening record" in map_text
    assert "v0.1.31 Phase 1 activation note" in level
    assert "No active source file was deleted" in _read("docs/status/current_status.md")
    assert "Physical renumbering remains blocked" in project



def test_cilt_i_foundation_strengthening_records_v031():
    chapter = _read("manuscript/volume_1/chapters/01_sets_functions_families.tex")
    examples = _read("examples_bank/set_relation_function_examples.md")
    roadmap = _read("docs/roadmap/current_roadmap.md")
    quiz = _read("manuscript/volume_1/quick_checks/quiz_forms/00_foundations_sets_relations_quiz.tex")
    key = _read("manuscript/volume_1/quick_checks/answer_keys/00_foundations_sets_relations_key.tex")
    qb = _read("src/pytop_questionbank/chapter_01_item_families.py")

    for token in (
        "Okuma önkoşulları ve gösterim sözleşmeleri",
        "Tümleyen bağlama bağlıdır",
        "Aile ile aileyi indeksleyen küme farklıdır",
        "Örtü ve bölümleme diline hazırlık",
        "Fonksiyon eşitliğinde üç veri",
    ):
        assert token in chapter

    assert "A0. Gösterim, bağlam ve tip kontrolü" in examples
    assert "v0.1.32" in roadmap
    assert "relation/order" in roadmap or "relation" in roadmap
    assert "Toplam puan: 15" in quiz
    assert "X\\setminus A=\\{3\\}" in key
    assert "notation-discipline" in qb
    assert "without changing the public family count" in qb


def test_cilt_i_relation_order_strengthening_records_v032():
    chapter = _read("manuscript/volume_1/chapters/02_relations_equivalences_orders.tex")
    examples = _read("examples_bank/set_relation_function_examples.md")
    roadmap = _read("docs/roadmap/current_roadmap.md")
    quiz = _read("manuscript/volume_1/quick_checks/quiz_forms/00_foundations_sets_relations_quiz.tex")
    key = _read("manuscript/volume_1/quick_checks/answer_keys/00_foundations_sets_relations_key.tex")
    rubric = _read("manuscript/volume_1/quick_checks/rubrics/00_foundations_sets_relations_rubric.md")
    qb = _read("src/pytop_questionbank/chapter_02_real_integration_families.py")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "Okuma önkoşulları ve Chapter 01 bağlantısı",
        "Bağıntının taşıyıcı çarpımı",
        "Eşdeğerlik bağıntısı ile bölümleme aynı veri değildir",
        "Önsıra, kısmi sıralama ve doğrusal sıralama ayrımı",
        "Topolojiye hazırlık köprüsü",
    ):
        assert token in chapter

    assert "B0. Chapter 01--02 geçiş kontrolü" in examples
    assert "carrier-product discipline" in roadmap
    assert "Toplam puan: 15" in quiz
    assert "fonksiyonun grafiği değildir" in key
    assert "Relation carrier/product control" in rubric
    assert "carrier-product-discipline" in qb
    assert "order-language-alignment" in qb
    assert "v0.1.32 Cilt I relation-order strengthening record" in map_text
    assert "No-move gate after v0.1.32" in map_text



def test_metric_split_axis_records_v033():
    chapter = _read("manuscript/volume_1/chapters/15_metric_spaces.tex")
    worksheet = _read("manuscript/volume_1/worksheets/05_metric_spaces_sequences.md")
    metric_examples = _read("examples_bank/metric_space_examples.md")
    bridge_examples = _read("examples_bank/metric_topology_bridge_examples.md")
    roadmap = _read("docs/roadmap/current_roadmap.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    preview_routes = _read("src/pytop_questionbank/chapter_15_preview_routes.py")
    rubric = _read("manuscript/volume_1/quick_checks/rubrics/06_metric_spaces_rubric.md")

    for token in (
        "v0.1.36 okuma yerleşimi",
        "Metrik sezgi çekirdeği",
        "İleri metrik yapı",
        "Bu ayrım bir dosya taşıma kararı değildir",
    ):
        assert token in chapter

    assert "v0.1.36 metric split-axis note" in worksheet
    assert "Öğretim kararı — v0.1.36" in metric_examples
    assert "Contract MTB-05: metric split-axis discipline" in bridge_examples
    assert "metric split-axis marker" in roadmap
    assert "v0.1.36 Cilt I metric split-axis record" in map_text
    assert "chapter-15-metric-split-axis" in preview_routes
    assert "v0.1.36 split-axis criterion" in rubric


def test_neighborhood_layer_strengthening_records_v037():
    chapter = _read("manuscript/volume_2/chapters/18_neighborhood_systems.tex")
    examples = _read("examples_bank/neighborhoods_nets_filters_examples.md")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    subset_ops = _read("src/pytop/subset_operators.py")
    api_init = _read("src/pytop/__init__.py")
    quick = _read("manuscript/volume_2/quick_checks/01_convergence_tools.tex")
    worksheet = _read("manuscript/volume_2/worksheets/01_convergence_tools.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.37 yerel kontrol köprüsü",
        "açık komşuluk",
        "Yerel kontrol şeması",
        "Aday kümenin kendisinin açık olup olmaması ikinci plandadır",
    ):
        assert token in chapter

    assert "v0.1.37 local checking bridge" in examples
    assert "open-neighborhood witness" in current
    assert "Chapter 18 neighborhood-system" in project
    assert "is_neighborhood_of_point" in subset_ops
    assert "all subsets that contain at least one open set" in subset_ops
    assert "is_neighborhood_of_point" in api_init
    assert "açık çekirdek" in quick
    assert "yerel kontrol köprüsünü ölçer" in worksheet
    assert "v0.1.37 Cilt II neighborhood layer strengthening record" in map_text



def test_nets_handoff_strengthening_records_v038():
    chapter = _read("manuscript/volume_2/chapters/19_nets.tex")
    examples = _read("examples_bank/neighborhoods_nets_filters_examples.md")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    nets = _read("src/pytop/nets.py")
    api_init = _read("src/pytop/__init__.py")
    quick = _read("manuscript/volume_2/quick_checks/01_convergence_tools.tex")
    worksheet = _read("manuscript/volume_2/worksheets/01_convergence_tools.md")
    notebook = _read("notebooks/exploration/11_nets.ipynb")
    api_doc = _read("docs/api/finite_topology_api.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.38 son-kuyruk",
        "son-kuyruk tanığı",
        "is_directed_set",
        "net_converges_to",
    ):
        assert token in chapter

    assert "v0.1.38 nets handoff bridge" in examples
    assert "eventual-containment witness" in current
    assert "Chapter 19 nets" in project
    assert "is_eventually_in" in nets
    assert "Every open neighborhood" in nets
    assert "is_directed_set" in api_init
    assert "son-kuyruk tanığı" in quick
    assert "eventual-containment kontrolü" in worksheet
    assert "pytop.net_converges_to" in notebook
    assert "Nets handoff" in api_doc
    assert "v0.1.38 Cilt II nets handoff strengthening record" in map_text

def test_filters_handoff_strengthening_records_v039():
    chapter = _read("manuscript/volume_2/chapters/20_filters.tex")
    examples = _read("examples_bank/neighborhoods_nets_filters_examples.md")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    filters = _read("src/pytop/filters.py")
    api_init = _read("src/pytop/__init__.py")
    quick = _read("manuscript/volume_2/quick_checks/01_convergence_tools.tex")
    worksheet = _read("manuscript/volume_2/worksheets/01_convergence_tools.md")
    notebook = _read("notebooks/exploration/12_filters.ipynb")
    api_doc = _read("docs/api/finite_topology_api.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.39 süzgeç tabanı",
        "süzgeç tabanı rafine tanık",
        "is_filter_base",
        "filter_converges_to",
    ):
        assert token in chapter

    assert "v0.1.39 filters handoff bridge" in examples
    assert "filter-base refinement witness" in current
    assert "Chapter 20 filters" in project
    assert "is_filter_base" in filters
    assert "Every open neighborhood" in filters
    assert "is_filter_base" in api_init
    assert "süzgeç tabanı rafine tanık" in quick
    assert "filter_converges_to testinin" in worksheet
    assert "pytop.filter_converges_to" in notebook
    assert "Filters handoff" in api_doc
    assert "v0.1.39 Cilt II filters handoff strengthening record" in map_text

def test_cilt1_capstone_strengthening_records_v040():
    chapter = _read("manuscript/volume_1/chapters/17_finite_topological_spaces.tex")
    catalog = _read("examples_bank/finite_spaces_catalog.md")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    worksheet = _read("manuscript/volume_1/worksheets/06_closure_invariants_finite_spaces.md")
    quick = _read("manuscript/volume_1/quick_checks/06_closure_invariants_finite_spaces.tex")
    notebook = _read("notebooks/teaching/lesson_07_finite_spaces.ipynb")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.40",
        "construction-matrix capstone bridge",
        "finite-laboratory synthesis",
        "FiniteTopologicalSpace",
        "finite_product_contract",
        "finite_quotient_contract",
        "finite_subspace",
        "specialization_preorder",
        "operator_table",
    ):
        assert token in chapter, f"{token!r} not found in chapter 17"

    assert "v0.1.40 inşaat matrisi capstone" in catalog
    assert "construction-matrix capstone bridge" in current
    assert "Chapter 17 Cilt I capstone" in project
    assert "v0.1.40 instructor cue" in worksheet
    assert "v0.1.40 inşaat matrisi kapanış köprüsü" in quick
    assert "construction-matrix capstone bridge" in notebook
    assert "v0.1.40 Cilt I capstone strengthening record" in map_text

def test_cilt2_property_language_reframing_records_v041():
    chapter = _read("manuscript/volume_1/chapters/10_topological_properties_and_invariants.tex")
    examples_inv = _read("examples_bank/basic_invariants_examples.md")
    examples_prop = _read("examples_bank/properties_cardinal_functions_links_examples.md")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    worksheet = _read("manuscript/volume_1/worksheets/06_closure_invariants_finite_spaces.md")
    quick = _read("manuscript/volume_1/quick_checks/06_closure_invariants_finite_spaces.tex")
    notebook = _read("notebooks/research/invariant_experiments.ipynb")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.41",
        "property-language explicit bridge",
        "undergraduate preservation route",
        "basic preservation table",
        "analyze_predicate",
        "analyze_invariant",
        "preservation",
    ):
        assert token in chapter, f"{token!r} not found in chapter 10"

    assert "v0.1.41 Cilt II property-language bridge note" in examples_inv
    assert "v0.1.41 Cilt II opening note" in examples_prop
    assert "property-language explicit bridge" in current
    assert "Chapter 10 Cilt II property-language" in project
    assert "v0.1.41 instructor cue" in worksheet
    assert "v0.1.41 undergraduate preservation route" in quick
    assert "property-language explicit bridge" in notebook
    assert "v0.1.41 Cilt II property-language reframing record" in map_text


def test_cilt2_separation_axiom_atlas_records_v042():
    chapter = _read("manuscript/volume_1/chapters/11_separation_axioms.tex")
    examples_sep = _read("examples_bank/separation_axioms_examples.md")
    examples_cex = _read("examples_bank/counterexamples.md")
    examples_scm = _read("examples_bank/separation_compactification_metrization_examples.md")
    nb_cex = _read("notebooks/counterexamples/t1_not_hausdorff_cocountable.ipynb")
    nb_lesson = _read("notebooks/teaching/lesson_04_separation.ipynb")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.42",
        "separation-axiom relation table",
        "counterexample atlas",
        "is_t0",
        "is_t1",
        "is_hausdorff",
        "analyze_separation",
        "CA-1",
        "CA-2",
        "CA-3",
    ):
        assert token in chapter, f"{token!r} not found in chapter 11"

    assert "v0.1.42" in examples_sep
    assert "v0.1.42" in examples_cex
    assert "v0.1.42" in examples_scm
    assert "separation-axiom relation table" in nb_cex
    assert "counterexample atlas" in nb_cex
    assert "separation-axiom relation table" in nb_lesson
    assert "counterexample atlas" in nb_lesson
    assert "separation-axiom relation table" in current
    assert "separation-axiom relation table" in project
    assert "v0.1.42 Cilt II separation-axiom atlas record" in map_text


def test_cilt2_countability_corridor_records_v043():
    chapter = _read("manuscript/volume_1/chapters/12_countability_axioms.tex")
    examples_cnt = _read("examples_bank/countability_examples.md")
    examples_inv = _read("examples_bank/basic_invariants_examples.md")
    nb_inv = _read("notebooks/research/invariant_experiments.ipynb")
    nb_lesson = _read("notebooks/teaching/lesson_05_countability.ipynb")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.43",
        "countability corridor table",
        "metric bridge",
        "is_first_countable",
        "is_second_countable",
        "is_separable",
        "is_lindelof",
        "weight",
        "density",
        "analyze_countability",
    ):
        assert token in chapter, f"{token!r} not found in chapter 12"

    assert "v0.1.43" in examples_cnt
    assert "v0.1.43" in examples_inv
    assert "countability corridor table" in nb_inv
    assert "metric bridge" in nb_inv
    assert "countability corridor table" in nb_lesson
    assert "metric bridge" in nb_lesson
    assert "countability corridor table" in current
    assert "countability corridor table" in project
    assert "v0.1.43 Cilt II countability-axioms corridor record" in map_text


def test_cilt2_connectedness_corridor_records_v044():
    chapter = _read("manuscript/volume_1/chapters/13_connectedness.tex")
    examples_conn = _read("examples_bank/connectedness_examples.md")
    examples_inv = _read("examples_bank/basic_invariants_examples.md")
    nb_inv = _read("notebooks/research/invariant_experiments.ipynb")
    nb_lesson = _read("notebooks/teaching/lesson_06_compactness_connectedness.ipynb")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.44",
        "connectedness corridor table",
        "advanced variants",
        "is_connected",
        "connected_components",
        "is_path_connected",
        "path_components",
        "is_locally_connected",
        "analyze_connectedness",
    ):
        assert token in chapter, f"{token!r} not found in chapter 13"

    assert "v0.1.44" in examples_conn
    assert "v0.1.44" in examples_inv
    assert "connectedness corridor table" in nb_inv
    assert "advanced variants" in nb_inv
    assert "connectedness corridor table" in nb_lesson
    assert "advanced variants" in nb_lesson
    assert "connectedness corridor table" in current
    assert "connectedness corridor table" in project
    assert "v0.1.44 Cilt II connectedness corridor record" in map_text


def test_cilt2_compactness_corridor_records_v045():
    chapter = _read("manuscript/volume_1/chapters/14_compactness.tex")
    examples_comp = _read("examples_bank/compactness_examples.md")
    examples_inv = _read("examples_bank/basic_invariants_examples.md")
    nb_inv = _read("notebooks/research/invariant_experiments.ipynb")
    nb_lesson = _read("notebooks/teaching/lesson_06_compactness_connectedness.ipynb")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.45",
        "compactness corridor table",
        "finite-subcover witness",
        "is_compact",
        "is_locally_compact",
        "is_sigma_compact",
        "finite_subcover_witness",
        "analyze_compactness",
        "heine_borel_check",
    ):
        assert token in chapter, f"{token!r} not found in chapter 14"

    assert "v0.1.45" in examples_comp
    assert "v0.1.45" in examples_inv
    assert "compactness corridor table" in nb_inv
    assert "finite-subcover witness" in nb_inv
    assert "compactness corridor table" in nb_lesson
    assert "finite-subcover witness" in nb_lesson
    assert "compactness corridor table" in current
    assert "compactness corridor table" in project
    assert "v0.1.45 Cilt II compactness corridor record" in map_text


def test_cilt2_sequences_positioning_records_v046():
    chapter = _read("manuscript/volume_1/chapters/16_sequences_and_convergence.tex")
    examples_conv = _read("examples_bank/convergence_examples.md")
    examples_inv = _read("examples_bank/basic_invariants_examples.md")
    nb_inv = _read("notebooks/research/invariant_experiments.ipynb")
    nb_lesson = _read("notebooks/teaching/lesson_06b_metric_and_sequences.ipynb")
    current = _read("docs/roadmap/current_roadmap.md")
    project = _read("PROJECT_ROADMAP.md")
    map_text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")

    for token in (
        "v0.1.46",
        "sequences-nets-filters positioning table",
        "undergraduate convergence route",
        "sequence_converges_to",
        "is_sequentially_compact",
        "sequence_cluster_point",
        "sequential_closure",
        "analyze_sequences",
    ):
        assert token in chapter, f"{token!r} not found in chapter 16"

    assert "v0.1.46" in examples_conv
    assert "v0.1.46" in examples_inv
    assert "sequences-nets-filters positioning table" in nb_inv
    assert "undergraduate convergence route" in nb_inv
    assert "sequences-nets-filters positioning table" in nb_lesson
    assert "undergraduate convergence route" in nb_lesson
    assert "sequences-nets-filters positioning table" in current
    assert "sequences-nets-filters positioning table" in project
    assert "v0.1.46 Cilt II sequences positioning record" in map_text

def test_cilt4_route_registry_completion_audit_fix1():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "v0.1.70-fix1 -- Cilt IV route-registry completion audit" in text
    for route in ("MS-IV-35", "MS-IV-36", "MS-IV-38", "MS-IV-39"):
        assert route in text
    assert ("QB:OBJECTIVE-ONLY" in text) or ("src/pytop_questionbank/cilt4_entry_assessment_routes.py" in text)
    for token in (
        "generated-question route pending",
        "v0.1.65` | DONE",
        "v0.1.66` | ROUTE-DONE, generated-question route pending",
        "v0.1.67` | ROUTE-DONE, generated-question route pending",
        "v0.1.68` | DONE-AS-PEDAGOGICAL-MOVE",
        "v0.1.69` | ROUTE-DONE, generated-question route pending",
        "v0.1.70` | FRAMEWORK-DONE, generated-question route pending",
    ):
        assert token in text
