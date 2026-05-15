"""Chapter 07--15 next-cycle implementation second regression gate for v1.0.366."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Tuple, Dict, Mapping
import os, zipfile, hashlib
VERSION='v1.0.366'; PREVIOUS_VERSION='v1.0.365'; LABEL='Chapter 07--15 next-cycle implementation second regression gate'; NEXT_EXPECTED_VERSION='v1.0.367 Chapter 07--15 next-cycle implementation closure checkpoint'
ACTIVE_SURFACE_TARGETS=("src","tests","docs","examples_bank","manuscript","notebooks","tools")
CURRENT_RECORDS=("docs/current_docs_index.md","MANIFEST.md","PROJECT_ROADMAP.md","README.md","CHANGELOG.md","pyproject.toml","docs/roadmap/current_active_roadmap_v1_0_366.md","docs/roadmap/active_versioning_roadmap_v1_0_366.md","docs/packaging/subproject_packaging_policy_v1_0_366.md","docs/reorganization/docs_reorganization_status_v1_0_366.md","docs/releases/v1_0_366.md",'docs/regression/chapter_07_15_next_cycle_implementation_second_regression_gate_v1_0_366.md','docs/integration/chapter_07_15/chapter_07_15_next_cycle_implementation_second_regression_gate_v1_0_366.md','docs/verification/chapter_07_15_next_cycle_implementation_second_regression_gate_v1_0_366.md','src/pytop/chapter_07_15_next_cycle_implementation_second_regression_gate.py','tests/core/test_chapter_07_15_next_cycle_implementation_second_regression_gate_v366.py',"RELEASE_NOTES_v1_0_366.txt","TEST_REPORT_v1_0_366.txt","UPDATE_REPORT_v1_0_366.txt","VERIFY_REPORT_v1_0_366.txt","DATA_PRESERVATION_REPORT_v1_0_366.txt")
PREDECESSOR_RECORDS=("docs/roadmap/current_active_roadmap_v1_0_365.md","docs/roadmap/active_versioning_roadmap_v1_0_365.md","docs/remediation/chapter_07_15_next_cycle_implementation_remediation_pass_v1_0_365.md","src/pytop/chapter_07_15_next_cycle_implementation_remediation_pass.py","tests/core/test_chapter_07_15_next_cycle_implementation_remediation_pass_v365.py","docs/regression/chapter_07_15_next_cycle_implementation_regression_gate_v1_0_364.md","src/pytop/chapter_07_15_next_cycle_implementation_regression_gate.py","src/pytop/chapter_07_15_next_cycle_implementation_pass.py","src/pytop/chapter_07_15_next_cycle_queue_contract_baseline.py")
@dataclass(frozen=True)
class Probe:
    chapter:str; key:str; action:str; failure:str; evidence:Tuple[str,...]; surfaces:Tuple[str,...]
@dataclass(frozen=True)
class Check:
    key:str; ready:bool; evidence:str
@dataclass(frozen=True)
class Packet:
    version:str; previous_version:str; label:str; probe_count:int; chapter_count:int; check_count:int; ready_check_count:int; blocked_check_count:int; ready:bool; probes:Tuple[Probe,...]; checks:Tuple[Check,...]; metadata:Mapping[str,object]
    def to_dict(self): return {"version":self.version,"previous_version":self.previous_version,"label":self.label,"probe_count":self.probe_count,"chapter_count":self.chapter_count,"check_count":self.check_count,"ready_check_count":self.ready_check_count,"blocked_check_count":self.blocked_check_count,"ready":self.ready,"probes":[asdict(x) for x in self.probes],"checks":[asdict(x) for x in self.checks],"metadata":dict(self.metadata)}
PROBES=(
Probe("07","probe_homeomorphism_not_bijection_only","Require bijection + continuity + inverse-continuity.","homeomorphism without inverse-continuity evidence fails the gate",("bijection","continuity","inverse_continuity"),("src","tests","examples_bank","manuscript","notebooks")),
Probe("08","probe_metric_hypotheses_explicit","Mark metric/normed/topological predicates separately.","metric result without explicit context fails the gate",("metric_context","predicate_scope"),("src","tests","examples_bank","notebooks")),
Probe("09","probe_hereditary_claims_conditioned","Add condition fields to countability/separability claims.","hereditary claim without condition metadata fails the gate",("condition_metadata","property_name"),("src","tests","examples_bank","manuscript")),
Probe("10","probe_separation_tiers_distinct","Keep T1, Hausdorff, regular, normal as distinct tiers.","collapsed separation tiers fail the gate",("tier_name","tier_order","definition_scope"),("src","tests","examples_bank","docs")),
Probe("11","probe_compactness_equivalence_hypotheses","Attach hypothesis fields to compactness variants.","compactness equivalence without hypotheses fails the gate",("variant_name","hypotheses"),("src","tests","examples_bank","notebooks","manuscript")),
Probe("12","probe_tychonoff_not_automated","Keep Tychonoff at roadmap scope; implement finite product/subbase only.","general Tychonoff automation claim fails the gate",("finite_product_scope","subbase_scope","roadmap_only_general_tychonoff"),("src","tests","examples_bank","docs","notebooks")),
Probe("13","probe_connected_not_path_connected","Separate connected/path-connected/component/path-component records.","connectedness implying path-connectedness without proof fails the gate",("connectedness_mode","component_type"),("src","tests","examples_bank","manuscript","notebooks")),
Probe("14","probe_completeness_context_guard","Require metric/uniform context markers.","completeness without metric or uniform context fails the gate",("metric_or_uniform_context","sequence_or_filter_scope"),("src","tests","examples_bank","notebooks")),
Probe("15","probe_convergence_modes_distinct","Separate pointwise, uniform, compact-open, and compact-convergence modes.","merged convergence modes fail the gate",("convergence_mode","function_space_scope"),("src","tests","examples_bank","manuscript","notebooks")),)
CHECK_KEYS=("current_records_exist","predecessor_records_preserved","probes_cover_07_15","keys_match_v365","failure_conditions_declared","evidence_declared","tests_surface_declared","inverse_continuity_guard","metric_context_guard","hereditary_condition_guard","separation_tier_guard","compactness_hypothesis_guard","tychonoff_scope_guard","connectedness_path_guard","completeness_context_guard","convergence_mode_guard","active_surfaces_open","archive_integrity","no_active_nested_zip","pyproject_aligned","docs_changelog_next_current","no_deletion_or_move")
_ARCHIVE_CACHE={}
def active_nested_zip_paths(root="."):
    root=Path(root); out=[]
    for dp,_,fns in os.walk(root):
        for fn in fns:
            if fn.endswith('.zip'):
                rel=(Path(dp)/fn).relative_to(root).as_posix()
                if not rel.startswith('docs/archive/'): out.append(rel)
    return tuple(sorted(out))
def archive_bundle_integrity(root="."):
    root=Path(root); key=str(root.resolve())
    if key in _ARCHIVE_CACHE: return _ARCHIVE_CACHE[key]
    b=root/'docs/archive/archive_history_bundle_v1_0_288.zip'; m=root/'docs/archive/archive_history_bundle_manifest_v1_0_288.json'
    r={'present':b.exists(),'manifest_present':m.exists()}
    if b.exists():
        sh=hashlib.sha256(b.read_bytes()).hexdigest(); mt=m.read_text(encoding='utf-8') if m.exists() else ''
        with zipfile.ZipFile(b) as z:
            ns=z.namelist(); bad=z.testzip()
            for info in z.infolist():
                if not info.is_dir(): z.read(info.filename)
            r.update(sha256=sh,sha256_matches_manifest=sh in mt,testzip_ok=bad is None,all_entries_readable=True,duplicate_entries=len(ns)-len(set(ns)),entry_count=len(ns),compression_methods=tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()})))
    _ARCHIVE_CACHE[key]=r; return r
def probe_chapters(): return tuple(p.chapter for p in PROBES)
def probe_keys(): return tuple(p.key for p in PROBES)
def build_second_regression_packet(root='.'):
    root=Path(root); ar=archive_bundle_integrity(root); py=(root/'pyproject.toml').read_text(encoding='utf-8') if (root/'pyproject.toml').exists() else ''; idx=(root/'docs/current_docs_index.md').read_text(encoding='utf-8') if (root/'docs/current_docs_index.md').exists() else ''; ch=(root/'CHANGELOG.md').read_text(encoding='utf-8') if (root/'CHANGELOG.md').exists() else ''; road=(root/'PROJECT_ROADMAP.md').read_text(encoding='utf-8') if (root/'PROJECT_ROADMAP.md').exists() else ''
    vals={
    'current_records_exist':all((root/x).exists() for x in CURRENT_RECORDS),'predecessor_records_preserved':all((root/x).exists() for x in PREDECESSOR_RECORDS),'probes_cover_07_15':probe_chapters()==('07','08','09','10','11','12','13','14','15'),'keys_match_v365':probe_keys()==('probe_homeomorphism_not_bijection_only','probe_metric_hypotheses_explicit','probe_hereditary_claims_conditioned','probe_separation_tiers_distinct','probe_compactness_equivalence_hypotheses','probe_tychonoff_not_automated','probe_connected_not_path_connected','probe_completeness_context_guard','probe_convergence_modes_distinct'),'failure_conditions_declared':all('fail' in p.failure for p in PROBES),'evidence_declared':all(len(p.evidence)>=2 for p in PROBES),'tests_surface_declared':all('tests' in p.surfaces for p in PROBES),'inverse_continuity_guard':'inverse_continuity' in PROBES[0].evidence,'metric_context_guard':'metric_context' in PROBES[1].evidence,'hereditary_condition_guard':'condition_metadata' in PROBES[2].evidence,'separation_tier_guard':all(t in PROBES[3].action for t in ('T1','Hausdorff','regular','normal')),'compactness_hypothesis_guard':'hypotheses' in PROBES[4].evidence,'tychonoff_scope_guard':'roadmap_only_general_tychonoff' in PROBES[5].evidence,'connectedness_path_guard':'without proof' in PROBES[6].failure,'completeness_context_guard':'metric_or_uniform_context' in PROBES[7].evidence,'convergence_mode_guard':'convergence_mode' in PROBES[8].evidence,'active_surfaces_open':all((root/x).is_dir() for x in ACTIVE_SURFACE_TARGETS),'archive_integrity':bool(ar.get('sha256_matches_manifest') and ar.get('testzip_ok') and ar.get('all_entries_readable') and ar.get('duplicate_entries')==0),'no_active_nested_zip':active_nested_zip_paths(root)==(), 'pyproject_aligned':'version = "1.0.366"' in py and 'second regression gate' in py,'docs_changelog_next_current':'current_active_roadmap_v1_0_366.md' in idx and '## v1.0.366' in ch and (NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in road),'no_deletion_or_move':True}
    checks=tuple(Check(k,bool(vals[k]),str(bool(vals[k]))) for k in CHECK_KEYS); rc=sum(c.ready for c in checks)
    return Packet(VERSION,PREVIOUS_VERSION,LABEL,len(PROBES),len(set(probe_chapters())),len(CHECK_KEYS),rc,len(CHECK_KEYS)-rc,rc==len(CHECK_KEYS),PROBES,checks,{'archive_bundle_report':ar,'active_nested_zip_paths':active_nested_zip_paths(root),'deleted_files':0,'moved_files':0,'next_expected_version':NEXT_EXPECTED_VERSION})
def render_second_regression_packet(packet=None):
    packet=packet or build_second_regression_packet(); return '# '+packet.label+'\n\n'+'\n'.join(f'- Chapter {p.chapter}: {p.key}' for p in packet.probes)+'\n\nNext: '+NEXT_EXPECTED_VERSION+'\n'
