from pathlib import Path
import importlib
import importlib.util
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]


_PACKAGE_AUDIT_MODULE = None


def _load_package_audit_module():
    global _PACKAGE_AUDIT_MODULE
    if _PACKAGE_AUDIT_MODULE is not None:
        return _PACKAGE_AUDIT_MODULE

    module_path = ROOT / "tools" / "package_audit.py"
    spec = importlib.util.spec_from_file_location("package_audit_for_tests", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _PACKAGE_AUDIT_MODULE = module
    return module


def test_project_version_is_clean_baseline():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["name"] == "pytop"
    assert data["project"]["version"] == "0.1.64"


def test_no_root_per_version_reports():
    forbidden = re.compile(r"^(DATA_PRESERVATION_REPORT|TEST_REPORT|UPDATE_REPORT|VERIFY_REPORT)_v|^RELEASE_NOTES_v")
    assert not [p.name for p in ROOT.iterdir() if p.is_file() and forbidden.search(p.name)]


def test_no_nonruntime_forbidden_active_surface():
    audit_module = _load_package_audit_module()
    violations = audit_module.audit(ROOT, include_runtime_artifacts=False)
    assert violations == []


def test_package_audit_keeps_runtime_cache_patterns_separate():
    audit_module = _load_package_audit_module()
    runtime_patterns = [pattern.pattern for pattern in audit_module.RUNTIME_ARTIFACT_PATTERNS]
    historical_patterns = [pattern.pattern for pattern in audit_module.HISTORICAL_SURFACE_PATTERNS]

    assert any("__pycache__" in pattern for pattern in runtime_patterns)
    assert any("\\.pyc" in pattern for pattern in runtime_patterns)
    assert not any("__pycache__" in pattern for pattern in historical_patterns)


def test_fixed_surface_docs_exist():
    required = [
        "docs/status/changelog.md",
        "docs/status/test_status.md",
        "docs/status/verification_status.md",
        "docs/roadmap/current_roadmap.md",
        "docs/developer_guide/file_governance.md",
    ]
    for rel in required:
        assert (ROOT / rel).is_file(), rel



def test_fixed_surface_identity_docs_are_current():
    current = "0.1.64"
    required = [
        "README.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "docs/current_docs_index.md",
        "docs/status/current_status.md",
        "docs/status/test_status.md",
        "docs/status/verification_status.md",
        "docs/status/data_preservation_status.md",
    ]
    for rel in required:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert current in text, rel



def test_version_sync_uses_pytop_distribution_root_name():
    sys.path.insert(0, str(ROOT / "src"))
    from pytop_publish.version_sync import expected_distribution_root_name

    assert expected_distribution_root_name(ROOT) == "pytop_v0_1_64"


def test_legacy_release_workflow_import_audit_identifies_deletion_ready_modules():
    audit_module = _load_package_audit_module()
    snapshot = audit_module.collect_legacy_release_workflow_import_audit(ROOT)

    assert snapshot.legacy_module_count == 11
    assert snapshot.deletion_ready_count == 11
    assert snapshot.blocked_module_count == 0
    assert snapshot.blocked_modules == ()
    assert snapshot.direct_import_edge_count == 0
    assert "release_disposition" in snapshot.deletion_ready_modules
    assert "release_preflight_gate" in snapshot.deletion_ready_modules
    assert "release_final_review_packet" in snapshot.deletion_ready_modules
    assert "release_regression_matrix" in snapshot.deletion_ready_modules
    assert not any(record.direct_import_callers for record in snapshot.records)

def test_compatibility_wrapper_import_audit_identifies_retirement_ready_wrappers():
    audit_module = _load_package_audit_module()
    snapshot = audit_module.collect_compatibility_wrapper_import_audit(ROOT)

    assert snapshot.wrapper_count == 8
    assert snapshot.retirement_ready_count == 8
    assert snapshot.blocked_module_count == 0
    assert snapshot.blocked_modules == ()
    assert snapshot.direct_import_edge_count == 0
    assert "release_hygiene" in snapshot.retirement_ready_modules
    assert "release_reliability" in snapshot.retirement_ready_modules
    assert "release_volume_3_assessment_closure" in snapshot.retirement_ready_modules
    assert not any(record.direct_import_callers for record in snapshot.records)


def test_compatibility_artifact_source_import_audit_keeps_facade_static_import_free():
    audit_module = _load_package_audit_module()
    snapshot = audit_module.collect_compatibility_artifact_source_import_audit(ROOT)

    assert snapshot.artifact_source_count == 1
    assert snapshot.facade_ready_count == 1
    assert snapshot.blocked_source_count == 0
    assert snapshot.blocked_sources == ()
    assert snapshot.direct_import_edge_count == 0
    assert snapshot.facade_ready_sources == ("release_reports",)
    assert not any(record.direct_import_callers for record in snapshot.records)



def test_release_prefixed_source_removal_gate_requires_explicit_approval():
    audit_module = _load_package_audit_module()
    snapshot = audit_module.collect_release_prefixed_source_removal_gate(ROOT)

    assert snapshot.release_prefixed_file_count == 20
    assert snapshot.technical_candidate_count == 20
    assert snapshot.approved_module_count == 0
    assert snapshot.approval_required_count == 20
    assert snapshot.approved_classification_count == 0
    assert snapshot.invalid_approval_module_count == 0
    assert snapshot.unknown_release_module_count == 0
    assert snapshot.technical_candidate_classification_count == 3
    assert snapshot.approved_module_record_count == 0
    assert snapshot.blocked_module_record_count == 20
    assert snapshot.planned_removal_count == 0
    assert snapshot.planned_retention_count == 20
    assert snapshot.scope_preview_count == 5
    assert snapshot.batch_plan_count == 3
    assert snapshot.batch_dependency_count == 3
    assert snapshot.batch_prerequisite_edge_count == 3
    assert snapshot.batch_readiness_count == 3
    assert snapshot.executable_batch_count == 0
    assert snapshot.blocked_batch_count == 3
    assert snapshot.batch_blocker_count == 3
    assert snapshot.blocked_batch_blocker_count == 3
    assert snapshot.batch_blocker_reason_count == 5
    assert snapshot.batch_blocker_missing_prerequisite_count == 3
    assert snapshot.batch_blocker_blocked_module_count == 20
    assert snapshot.batch_decision_guidance_count == 3
    assert snapshot.batch_approval_command_count == 3
    assert snapshot.actionable_approval_command_count == 1
    assert snapshot.recommended_approval_flag_count == 1
    assert snapshot.batch_approval_sequence_count == 3
    assert snapshot.approval_sequence_flag_count == 6
    assert snapshot.full_scope_approval_sequence_count == 1
    assert snapshot.next_decision_candidate_count == 1
    assert snapshot.approved_executable_decision_count == 0
    assert snapshot.prerequisite_blocked_decision_count == 2
    assert snapshot.removal_allowed_now is False
    assert snapshot.technical_candidate_modules_by_classification == (
        ("compatibility_artifact_source", ("release_reports",)),
        (
            "compatibility_wrapper",
            (
                "release_hygiene",
                "release_manuscript_bridge_closure",
                "release_manuscript_followup",
                "release_reliability",
                "release_research_path_closure_consolidation",
                "release_volume_2_bridge_closure",
                "release_volume_3_assessment_closure",
                "release_volume_3_specialized_contrast_closure",
            ),
        ),
        (
            "legacy_release_workflow",
            (
                "release_convergence",
                "release_decision_ledger",
                "release_decision_path",
                "release_disposition",
                "release_final_review_packet",
                "release_preflight_gate",
                "release_recommendation",
                "release_regression_matrix",
                "release_signoff_handoff",
                "release_threshold_partition",
                "release_validation",
            ),
        ),
    )
    assert tuple(
        (record.classification, record.technical_count, record.approved_count, record.blocked_count, record.fully_approved)
        for record in snapshot.classification_approval_records
    ) == (
        ("compatibility_artifact_source", 1, 0, 1, False),
        ("compatibility_wrapper", 8, 0, 8, False),
        ("legacy_release_workflow", 11, 0, 11, False),
    )
    assert len(snapshot.action_plan_records) == 20
    assert {record.planned_action for record in snapshot.action_plan_records} == {
        "retain_pending_explicit_approval"
    }
    assert tuple(
        (record.scope_name, record.planned_removal_count, record.planned_retention_count, record.removal_allowed_now)
        for record in snapshot.scope_preview_records
    ) == (
        ("current_requested_scope", 0, 20, False),
        ("compatibility_artifact_source_only", 1, 19, False),
        ("compatibility_wrapper_only", 8, 12, False),
        ("legacy_release_workflow_only", 11, 9, False),
        ("all_reviewed_release_prefixed_sources", 20, 0, True),
    )
    assert tuple(
        (record.batch_name, record.batch_order, record.module_count, record.classifications)
        for record in snapshot.batch_plan_records
    ) == (
        ("artifact_source_probe", 1, 1, ("compatibility_artifact_source",)),
        ("compatibility_wrapper_category", 2, 8, ("compatibility_wrapper",)),
        ("legacy_release_workflow_category", 3, 11, ("legacy_release_workflow",)),
    )
    assert tuple(
        (record.batch_name, record.prerequisite_batches, record.prerequisite_count, record.prerequisite_free)
        for record in snapshot.batch_dependency_records
    ) == (
        ("artifact_source_probe", (), 0, True),
        ("compatibility_wrapper_category", ("artifact_source_probe",), 1, False),
        ("legacy_release_workflow_category", ("artifact_source_probe", "compatibility_wrapper_category"), 2, False),
    )
    assert tuple(
        (
            record.batch_name,
            record.batch_order,
            record.prerequisites_satisfied,
            record.approved_count,
            record.blocked_count,
            record.executable_now,
        )
        for record in snapshot.batch_readiness_records
    ) == (
        ("artifact_source_probe", 1, True, 0, 1, False),
        ("compatibility_wrapper_category", 2, False, 0, 8, False),
        ("legacy_release_workflow_category", 3, False, 0, 11, False),
    )
    assert tuple(
        (
            record.batch_name,
            record.blocking_reasons,
            record.missing_prerequisite_batches,
            record.blocked_module_count,
            record.blocked,
        )
        for record in snapshot.batch_blocker_records
    ) == (
        ("artifact_source_probe", ("missing_batch_module_approval",), (), 1, True),
        (
            "compatibility_wrapper_category",
            ("missing_prerequisite_batch_approval", "missing_batch_module_approval"),
            ("artifact_source_probe",),
            8,
            True,
        ),
        (
            "legacy_release_workflow_category",
            ("missing_prerequisite_batch_approval", "missing_batch_module_approval"),
            ("artifact_source_probe", "compatibility_wrapper_category"),
            11,
            True,
        ),
    )
    assert tuple(
        (
            record.batch_name,
            record.decision_status,
            record.next_decision_candidate,
            record.approval_target_classifications,
            record.approval_target_module_count,
        )
        for record in snapshot.batch_decision_guidance_records
    ) == (
        (
            "artifact_source_probe",
            "request_module_or_classification_approval",
            True,
            ("compatibility_artifact_source",),
            1,
        ),
        (
            "compatibility_wrapper_category",
            "blocked_until_prerequisite_batch_is_resolved",
            False,
            ("compatibility_wrapper",),
            8,
        ),
        (
            "legacy_release_workflow_category",
            "blocked_until_prerequisite_batch_is_resolved",
            False,
            ("legacy_release_workflow",),
            11,
        ),
    )
    assert tuple(
        (record.batch_name, record.command_status, record.actionable_now, record.recommended_flags)
        for record in snapshot.batch_approval_command_records
    ) == (
        ("artifact_source_probe", "preview_next_decision", True, ("--approve-release-source-category compatibility_artifact_source",)),
        ("compatibility_wrapper_category", "wait_for_prerequisite", False, ()),
        ("legacy_release_workflow_category", "wait_for_prerequisite", False, ()),
    )
    assert tuple(
        (
            record.batch_name,
            record.sequence_position,
            record.cumulative_planned_removal_count,
            record.cumulative_planned_retention_count,
            record.reaches_full_scope,
            record.cumulative_category_flags,
        )
        for record in snapshot.batch_approval_sequence_records
    ) == (
        ("artifact_source_probe", 1, 1, 19, False, ("--approve-release-source-category compatibility_artifact_source",)),
        (
            "compatibility_wrapper_category",
            2,
            9,
            11,
            False,
            (
                "--approve-release-source-category compatibility_artifact_source",
                "--approve-release-source-category compatibility_wrapper",
            ),
        ),
        (
            "legacy_release_workflow_category",
            3,
            20,
            0,
            True,
            (
                "--approve-release-source-category compatibility_artifact_source",
                "--approve-release-source-category compatibility_wrapper",
                "--approve-release-source-category legacy_release_workflow",
            ),
        ),
    )
    assert len(snapshot.legacy_ready_modules) == 11
    assert len(snapshot.wrapper_ready_modules) == 8
    assert snapshot.artifact_source_ready_modules == ("release_reports",)
    assert "release_reports" in snapshot.technical_candidate_modules
    assert "release_disposition" in snapshot.technical_candidate_modules
    assert "release_hygiene" in snapshot.technical_candidate_modules


def test_release_prefixed_source_removal_gate_supports_non_destructive_approval_preview():
    audit_module = _load_package_audit_module()

    wrapper_preview = audit_module.collect_release_prefixed_source_removal_gate(
        ROOT,
        approved_classifications=("compatibility_wrapper",),
    )
    assert wrapper_preview.approved_classifications == ("compatibility_wrapper",)
    assert wrapper_preview.technical_candidate_classification_count == 3
    assert wrapper_preview.approved_module_count == 8
    assert wrapper_preview.approval_required_count == 12
    assert wrapper_preview.planned_removal_count == 8
    assert wrapper_preview.planned_retention_count == 12
    assert wrapper_preview.executable_batch_count == 0
    assert wrapper_preview.blocked_batch_count == 3
    assert wrapper_preview.blocked_batch_blocker_count == 3
    assert wrapper_preview.batch_blocker_reason_count == 4
    assert wrapper_preview.batch_decision_guidance_count == 3
    assert wrapper_preview.batch_approval_command_count == 3
    assert wrapper_preview.actionable_approval_command_count == 1
    assert wrapper_preview.recommended_approval_flag_count == 1
    assert wrapper_preview.batch_approval_sequence_count == 3
    assert wrapper_preview.approval_sequence_flag_count == 6
    assert wrapper_preview.full_scope_approval_sequence_count == 1
    assert wrapper_preview.next_decision_candidate_count == 1
    assert wrapper_preview.approved_executable_decision_count == 0
    assert wrapper_preview.prerequisite_blocked_decision_count == 2
    assert tuple(
        (record.batch_name, record.prerequisites_satisfied, record.approved_count, record.blocked_count, record.executable_now)
        for record in wrapper_preview.batch_readiness_records
    ) == (
        ("artifact_source_probe", True, 0, 1, False),
        ("compatibility_wrapper_category", False, 8, 0, False),
        ("legacy_release_workflow_category", False, 0, 11, False),
    )
    assert tuple(
        (record.batch_name, record.blocking_reasons, record.missing_prerequisite_batches, record.blocked_module_count)
        for record in wrapper_preview.batch_blocker_records
    ) == (
        ("artifact_source_probe", ("missing_batch_module_approval",), (), 1),
        ("compatibility_wrapper_category", ("missing_prerequisite_batch_approval",), ("artifact_source_probe",), 0),
        (
            "legacy_release_workflow_category",
            ("missing_prerequisite_batch_approval", "missing_batch_module_approval"),
            ("artifact_source_probe",),
            11,
        ),
    )
    assert tuple(
        (record.batch_name, record.decision_status, record.next_decision_candidate)
        for record in wrapper_preview.batch_decision_guidance_records
    ) == (
        ("artifact_source_probe", "request_module_or_classification_approval", True),
        ("compatibility_wrapper_category", "blocked_until_prerequisite_batch_is_resolved", False),
        ("legacy_release_workflow_category", "blocked_until_prerequisite_batch_is_resolved", False),
    )
    assert wrapper_preview.scope_preview_records[0].scope_name == "current_requested_scope"
    assert wrapper_preview.scope_preview_records[0].planned_removal_count == 8
    assert wrapper_preview.scope_preview_records[0].planned_retention_count == 12
    assert wrapper_preview.removal_allowed_now is False
    assert set(wrapper_preview.approved_modules) == set(wrapper_preview.wrapper_ready_modules)
    assert tuple(
        (record.classification, record.approved_count, record.blocked_count, record.fully_approved)
        for record in wrapper_preview.classification_approval_records
    ) == (
        ("compatibility_artifact_source", 0, 1, False),
        ("compatibility_wrapper", 8, 0, True),
        ("legacy_release_workflow", 0, 11, False),
    )

    full_preview = audit_module.collect_release_prefixed_source_removal_gate(
        ROOT,
        approved_classifications=(
            "compatibility_artifact_source",
            "compatibility_wrapper",
            "legacy_release_workflow",
        ),
    )
    assert full_preview.approved_module_count == 20
    assert full_preview.approval_required_count == 0
    assert full_preview.planned_removal_count == 20
    assert full_preview.planned_retention_count == 0
    assert full_preview.scope_preview_records[0].planned_removal_count == 20
    assert full_preview.scope_preview_records[0].planned_retention_count == 0
    assert full_preview.removal_allowed_now is True
    assert full_preview.executable_batch_count == 3
    assert full_preview.blocked_batch_count == 0
    assert full_preview.blocked_batch_blocker_count == 0
    assert full_preview.batch_blocker_reason_count == 0
    assert full_preview.batch_blocker_blocked_module_count == 0
    assert full_preview.next_decision_candidate_count == 0
    assert full_preview.batch_approval_command_count == 3
    assert full_preview.actionable_approval_command_count == 0
    assert full_preview.recommended_approval_flag_count == 0
    assert full_preview.batch_approval_sequence_count == 3
    assert full_preview.full_scope_approval_sequence_count == 1
    assert full_preview.batch_approval_sequence_records[-1].cumulative_planned_removal_count == 20
    assert full_preview.batch_approval_sequence_records[-1].cumulative_planned_retention_count == 0
    assert full_preview.approved_executable_decision_count == 3
    assert full_preview.prerequisite_blocked_decision_count == 0
    assert tuple(
        (record.batch_name, record.prerequisites_satisfied, record.approved_count, record.blocked_count, record.executable_now)
        for record in full_preview.batch_readiness_records
    ) == (
        ("artifact_source_probe", True, 1, 0, True),
        ("compatibility_wrapper_category", True, 8, 0, True),
        ("legacy_release_workflow_category", True, 11, 0, True),
    )
    assert all(record.blocking_reasons == () for record in full_preview.batch_blocker_records)
    assert all(record.decision_status == "approved_executable" for record in full_preview.batch_decision_guidance_records)
    assert all(record.fully_approved for record in full_preview.classification_approval_records)

    single_module_preview = audit_module.collect_release_prefixed_source_removal_gate(
        ROOT,
        approved_modules=("release_reports",),
    )
    assert single_module_preview.approved_module_count == 1
    assert single_module_preview.approval_required_count == 19
    assert single_module_preview.planned_removal_count == 1
    assert single_module_preview.planned_retention_count == 19
    assert single_module_preview.scope_preview_records[0].planned_removal_count == 1
    assert single_module_preview.scope_preview_records[0].planned_retention_count == 19
    assert single_module_preview.action_plan_records[0].module_name == "release_reports"
    assert single_module_preview.action_plan_records[0].planned_action == "remove_if_packager_executes_approved_scope"
    assert single_module_preview.module_approval_records[0].module_name == "release_reports"
    assert single_module_preview.module_approval_records[0].approved is True
    assert single_module_preview.module_approval_records[0].blocked is False
    assert single_module_preview.executable_batch_count == 1
    assert single_module_preview.blocked_batch_count == 2
    assert single_module_preview.blocked_batch_blocker_count == 2
    assert single_module_preview.batch_blocker_reason_count == 3
    assert single_module_preview.next_decision_candidate_count == 1
    assert single_module_preview.actionable_approval_command_count == 1
    assert single_module_preview.recommended_approval_flag_count == 1
    assert single_module_preview.batch_approval_sequence_count == 3
    assert single_module_preview.batch_approval_sequence_records[1].cumulative_planned_removal_count == 9
    assert single_module_preview.approved_executable_decision_count == 1
    assert single_module_preview.prerequisite_blocked_decision_count == 1
    assert single_module_preview.batch_blocker_records[0].blocking_reasons == ()
    assert single_module_preview.batch_readiness_records[0].executable_now is True
    assert single_module_preview.batch_readiness_records[1].prerequisites_satisfied is True
    assert single_module_preview.batch_readiness_records[1].executable_now is False
    assert tuple(
        (record.batch_name, record.decision_status, record.next_decision_candidate)
        for record in single_module_preview.batch_decision_guidance_records
    ) == (
        ("artifact_source_probe", "approved_executable", False),
        ("compatibility_wrapper_category", "request_module_or_classification_approval", True),
        ("legacy_release_workflow_category", "blocked_until_prerequisite_batch_is_resolved", False),
    )
    assert tuple(
        (record.batch_name, record.command_status, record.recommended_flags)
        for record in single_module_preview.batch_approval_command_records
    ) == (
        ("artifact_source_probe", "already_approved", ()),
        ("compatibility_wrapper_category", "preview_next_decision", ("--approve-release-source-category compatibility_wrapper",)),
        ("legacy_release_workflow_category", "wait_for_prerequisite", ()),
    )

    invalid_preview = audit_module.collect_release_prefixed_source_removal_gate(
        ROOT,
        approved_modules=("release_missing",),
    )
    assert invalid_preview.approved_module_count == 0
    assert invalid_preview.invalid_approval_modules == ("release_missing",)

def test_experimental_research_path_wrapper_imports():
    from pytop_experimental.research_path_registry import (
        ResearchPathProfile,
        get_named_research_path_profiles,
        research_path_chapter_index,
        research_path_layer_summary,
        research_path_route_index,
    )

    assert ResearchPathProfile is not None
    assert get_named_research_path_profiles()
    assert isinstance(research_path_chapter_index(), dict)
    assert isinstance(research_path_layer_summary(), dict)
    assert isinstance(research_path_route_index(), dict)



def test_pytop_publish_public_surface_excludes_legacy_release_exports():
    sys.path.insert(0, str(ROOT / "src"))
    import pytop_publish

    exported = set(getattr(pytop_publish, "__all__", ()))
    legacy_prefixes = (
        "build_release_",
        "collect_release_",
        "render_release_",
        "write_release_",
    )
    legacy_names = sorted(
        name
        for name in exported
        if name.startswith(legacy_prefixes)
        or name in {
            "REQUIRED_THRESHOLD_PATH_TEMPLATES",
            "collect_release_surface_metrics",
        }
    )
    assert legacy_names == []
    assert "build_teaching_material_bundle" in exported
    assert "build_finite_space_example_catalog" in exported
    assert "collect_package_hygiene_snapshot" in exported
    assert "scan_package_hygiene" in exported
    assert "collect_package_reliability_snapshot" in exported
    assert "PackageReliabilitySnapshot" in exported
    assert "build_research_bridge_inventory_artifact" in exported
    assert "build_research_notebook_index_artifact" in exported
    assert "build_material_chain_inventory_artifact" in exported
    assert "build_objective_alignment_status_artifact" in exported
    assert "build_volume_3_scored_assessment_artifact" in exported
    assert "build_exception_protocol_status_artifact" in exported


def test_legacy_release_shell_and_test_surfaces_are_retired():
    assert not list((ROOT / "tools").glob("release_*.sh"))
    assert not (ROOT / "tools" / "check_release_hygiene.sh").exists()
    assert not (ROOT / "tools" / "clean_release_artifacts.sh").exists()
    assert not list((ROOT / "tests" / "publishing").glob("test_release_*.py"))

def test_durable_artifact_builder_facade_exists():
    sys.path.insert(0, str(ROOT / "src"))
    import pytop_publish.artifact_builders as artifact_builders

    assert "build_three_volume_chapter_dependency_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert callable(artifact_builders.build_three_volume_chapter_dependency_artifact)
    assert callable(artifact_builders.build_bridge_route_map_artifact)
    assert callable(artifact_builders.build_volume_surface_status_artifact)
    assert "build_research_bridge_inventory_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert "build_research_notebook_index_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert callable(artifact_builders.build_research_bridge_inventory_artifact)
    assert callable(artifact_builders.build_special_example_inventory_artifact)
    assert "build_material_chain_inventory_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert "build_objective_alignment_status_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert callable(artifact_builders.build_material_chain_inventory_artifact)
    assert callable(artifact_builders.build_objective_alignment_status_artifact)
    assert "build_volume_3_scored_assessment_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert "build_exception_protocol_status_artifact" in artifact_builders.DURABLE_ARTIFACT_BUILDER_NAMES
    assert callable(artifact_builders.build_volume_3_scored_assessment_artifact)
    assert callable(artifact_builders.build_volume_3_exception_protocols_artifact)
    assert callable(artifact_builders.build_exception_protocol_status_artifact)


def test_publishing_surface_registry_classifies_reviewed_release_modules():
    sys.path.insert(0, str(ROOT / "src"))
    from pytop_publish import (
        build_publishing_surface_registry,
        classify_publishing_surface,
        legacy_pending_publishing_modules,
        publishing_surface_summary,
    )

    registry = build_publishing_surface_registry()
    reviewed_names = {profile.module_name for profile in registry}
    assert "release_hygiene" in reviewed_names
    assert "release_reports" in reviewed_names
    assert "release_preflight_gate" in reviewed_names

    hygiene = classify_publishing_surface("release_hygiene.py")
    assert hygiene is not None
    assert hygiene.classification == "compatibility_wrapper"
    assert hygiene.action == "keep_as_import_alias_only"
    assert hygiene.replacement_import == "pytop_publish.package_hygiene"

    reports = classify_publishing_surface("release_reports")
    assert reports is not None
    assert reports.classification == "compatibility_artifact_source"
    assert reports.replacement_import == (
        "pytop_publish.artifact_builders for reusable material-chain, objective-alignment, "
        "dependency, bridge, research, and volume-3 pedagogy artifact builders"
    )

    preflight = classify_publishing_surface("release_preflight_gate")
    assert preflight is not None
    assert preflight.classification == "legacy_release_workflow"

    summary = publishing_surface_summary(registry)
    assert summary == {
        "compatibility_artifact_source": 1,
        "compatibility_wrapper": 8,
        "legacy_release_workflow": 11,
    }
    assert legacy_pending_publishing_modules() == ()

    release_modules = sorted(p.stem for p in (ROOT / "src" / "pytop_publish").glob("release_*.py"))
    assert len(release_modules) == 20
    assert reviewed_names == set(release_modules)

    reliability = classify_publishing_surface("release_reliability")
    assert reliability is not None
    assert reliability.classification == "compatibility_wrapper"
    assert reliability.replacement_import == "pytop_publish.package_reliability"

    disposition = classify_publishing_surface("release_disposition")
    assert disposition is not None
    assert disposition.classification == "legacy_release_workflow"


def test_package_hygiene_replaces_release_hygiene_public_policy_name():
    sys.path.insert(0, str(ROOT / "src"))
    from pytop_publish import (
        PackageHygieneSnapshot,
        collect_package_hygiene_snapshot,
        scan_package_hygiene,
    )

    release_hygiene = importlib.import_module("pytop_publish.release_hygiene")

    assert release_hygiene.ReleaseHygieneSnapshot is PackageHygieneSnapshot
    assert (
        release_hygiene.collect_release_hygiene_snapshot(ROOT).detected_paths
        == collect_package_hygiene_snapshot(ROOT).detected_paths
    )
    assert release_hygiene.scan_release_hygiene(
        ROOT,
        ignore_runtime_test_artifacts=True,
    ) == scan_package_hygiene(
        ROOT,
        ignore_runtime_test_artifacts=True,
    )


def test_package_reliability_replaces_release_reliability_policy_name():
    sys.path.insert(0, str(ROOT / "src"))
    from pytop_publish import PackageReliabilitySnapshot
    from pytop_publish.package_reliability import PACKAGE_STAGE_ENTRIES

    release_reliability = importlib.import_module("pytop_publish.release_reliability")

    assert release_reliability.ReleaseReliabilitySnapshot is PackageReliabilitySnapshot
    assert release_reliability.RELEASE_STAGE_ENTRIES is PACKAGE_STAGE_ENTRIES
    assert callable(release_reliability.collect_release_reliability_snapshot)
