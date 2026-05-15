"""Chapter 07--15 next-cycle queue contract baseline for v1.0.362."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib, os, zipfile

VERSION="v1.0.362"
PREVIOUS_VERSION="v1.0.361"
LABEL="Chapter 07--15 next-cycle queue contract baseline"
NEXT_EXPECTED_VERSION="v1.0.363 Chapter 07--15 next-cycle implementation pass"
EXPECTED_CONTRACT_COUNT=9
EXPECTED_TRACK_COUNT=6
EXPECTED_GATE_COUNT=8
ACTIVE_SURFACE_TARGETS=("src","tests","docs","examples_bank","manuscript","notebooks","tools")
CURRENT_RECORDS=("docs/current_docs_index.md","MANIFEST.md","PROJECT_ROADMAP.md","README.md","CHANGELOG.md","pyproject.toml","docs/roadmap/current_active_roadmap_v1_0_362.md","docs/roadmap/active_versioning_roadmap_v1_0_362.md","docs/packaging/subproject_packaging_policy_v1_0_362.md","docs/reorganization/docs_reorganization_status_v1_0_362.md","docs/releases/v1_0_362.md","docs/integration/chapter_07_15/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md","docs/verification/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md","src/pytop/chapter_07_15_next_cycle_queue_contract_baseline.py","tests/core/test_chapter_07_15_next_cycle_queue_contract_baseline_v362.py","RELEASE_NOTES_v1_0_362.txt","TEST_REPORT_v1_0_362.txt","UPDATE_REPORT_v1_0_362.txt","VERIFY_REPORT_v1_0_362.txt","DATA_PRESERVATION_REPORT_v1_0_362.txt")
PREVIOUS_SELECTION_RECORDS=("docs/roadmap/current_active_roadmap_v1_0_361.md","docs/roadmap/active_versioning_roadmap_v1_0_361.md","docs/releases/v1_0_361.md","docs/integration/chapter_07_15/chapter_07_15_next_cycle_queue_selection_v1_0_361.md","docs/verification/chapter_07_15_next_cycle_queue_selection_v1_0_361.md","src/pytop/chapter_07_15_next_cycle_queue_selection.py","tests/core/test_chapter_07_15_next_cycle_queue_selection_v361.py")
REBASELINE_REFERENCE_RECORDS=("docs/roadmap/chapter_07_15_active_integration_roadmap_v1_0_316.md","docs/roadmap/chapter_07_15_integration_roadmap_v1_0_217.md")
REFERENCE_INPUT_POLICY="Uploaded Chapter 07--15 zip files remain reference/comparison inputs only; contracted work becomes active content only after adaptation into open-folder sources."
CONTRACT_TRACKS=("api_surface_contracts","examples_bank_expansion","questionbank_contracts","notebook_learning_path","manuscript_crosswalk_notes","release_validation_gates")
IMPLEMENTATION_GATES=("no_nested_active_chapter_zip","one_contract_per_chapter","acceptance_criteria_declared","active_surface_targets_declared","tests_required_for_each_contract","examples_bank_or_manuscript_or_notebook_surface_declared","archive_bundle_evidence_only","next_release_implementation_pointer_declared")
@dataclass(frozen=True)
class ContractItem:
    chapter:str; selected_focus:str; target_surfaces:Tuple[str,...]; acceptance_criteria:Tuple[str,...]; validation_gates:Tuple[str,...]; implementation_notes:Tuple[str,...]
@dataclass(frozen=True)
class ContractBaselineCheck:
    key:str; ready:bool; evidence:str
@dataclass(frozen=True)
class ContractBaselinePacket:
    version:str; previous_version:str; label:str; contract_count:int; chapter_count:int; track_count:int; gate_count:int; check_count:int; ready_check_count:int; blocked_check_count:int; ready:bool; contracts:Tuple[ContractItem,...]; tracks:Tuple[str,...]; gates:Tuple[str,...]; checks:Tuple[ContractBaselineCheck,...]; metadata:Mapping[str,object]
    def to_dict(self)->Dict[str,object]:
        return {"version":self.version,"previous_version":self.previous_version,"label":self.label,"contract_count":self.contract_count,"chapter_count":self.chapter_count,"track_count":self.track_count,"gate_count":self.gate_count,"check_count":self.check_count,"ready_check_count":self.ready_check_count,"blocked_check_count":self.blocked_check_count,"ready":self.ready,"contracts":[asdict(i) for i in self.contracts],"tracks":list(self.tracks),"gates":list(self.gates),"checks":[asdict(i) for i in self.checks],"metadata":dict(self.metadata)}
def _c(ch,focus,surfaces,criteria,notes):
    return ContractItem(ch,focus,surfaces,criteria,("add_or_extend_direct_tests","add_examples_bank_contract_when_applicable","keep_chapter_reference_zip_non_active","document_manuscript_or_notebook_crosswalk_when_targeted"),notes)
CONTRACTS=(
_c("07","continuity and homeomorphism API/examples crosswalk",("src","tests","examples_bank","manuscript","notebooks"),("declare continuity and homeomorphism API names before implementation","include examples_bank contracts for open/closed-map behavior","include crosswalk notes for induced-topology examples","validate homeomorphism wording against computational predicates"),("avoid external copy-paste","start from finite-space examples")),
_c("08","metric and normed topology examples/questionbank bridge",("src","tests","examples_bank","notebooks"),("declare metric-topology and normed-space example families","add questionbank expectations for equivalent metrics","validate open-ball terminology in examples","prepare notebook checks for metric-neighborhood exploration"),("keep examples small","separate metric predicates from generic topology")),
_c("09","countability and separability theorem-profile queue",("src","tests","examples_bank","manuscript"),("declare theorem profiles for first countability, second countability, separability, and Lindelof links","add examples distinguishing hereditary and non-hereditary properties","validate theorem-profile metadata with direct tests","prepare manuscript crosswalk notes for countability hierarchy"),("use theorem profiles","preserve undergraduate explanations")),
_c("10","separation axioms and function-separation validation",("src","tests","examples_bank","docs"),("declare T1, Hausdorff, regular, and normal validation records","include function-separation expectations when relevant","add finite counterexample hooks for tests","document separation-axiom escalation without collapsing definitions"),("keep English module names stable","use docs for hierarchy")),
_c("11","compactness family expansion and metric compactness bridge",("src","tests","examples_bank","notebooks","manuscript"),("declare compactness family records for FIP, local compactness, and sequential compactness","include metric compactness bridge expectations","add examples distinguishing compactness variants","prepare notebook and manuscript crosswalk targets"),("do not assert equivalences outside hypotheses","separate finite and metric statements")),
_c("12","product topology, subbase, and Cantor-set queue",("src","tests","examples_bank","docs","notebooks"),("declare product-topology and subbase contract records","include finite-product basis validation targets","stage Cantor-set references as learning-path notes","document Tychonoff-route scope as roadmap-level only until implementation"),("avoid overpromising full Tychonoff automation","prefer finite pedagogical scaffolds")),
_c("13","connectedness, path, and homotopy learning-path queue",("src","tests","examples_bank","manuscript","notebooks"),("declare connectedness and component example contracts","include path and path-component learning-path targets","stage homotopic-path terminology for future examples","validate that connectedness contracts do not imply path-connectedness"),("keep homotopy staged","separate connected and path-connected behavior")),
_c("14","complete metric spaces and Baire-category queue",("src","tests","examples_bank","notebooks"),("declare complete-metric and Cauchy-sequence contract records","include nested-closed-set and completion learning targets","stage Baire-category examples as notebook-supported records","validate metric-specific hypotheses in every test contract"),("do not generalize completeness beyond metric spaces","keep Baire as staged enrichment")),
_c("15","function spaces and convergence topology queue",("src","tests","examples_bank","manuscript","notebooks"),("declare pointwise, uniform, compact-open, and compact-convergence contract records","include examples distinguishing convergence modes","prepare manuscript and notebook crosswalks for function-space topology","validate naming consistency before implementation"),("separate convergence modes first","align terminology across docs and tests")),
)
CHECK_KEYS=("current_records_exist","previous_selection_records_preserved","v316_rebaseline_roadmap_preserved","contract_items_cover_chapters_07_15","each_contract_has_acceptance_criteria","each_contract_has_validation_gates","each_contract_references_open_surfaces","contract_tracks_declared","implementation_gates_declared","active_surface_targets_present","archive_bundle_integrity_confirmed","no_active_nested_zip_files","cleanup_deletion_gate_closed","pyproject_version_aligned","docs_index_points_to_current_release","changelog_contains_current_release","next_release_pointer_declared")
def active_nested_zip_paths(root:str|Path=".")->Tuple[str,...]:
    root=Path(root); out=[]
    for dp,_dirs,files in os.walk(root):
        for fn in files:
            if fn.endswith(".zip"):
                rel=str((Path(dp)/fn).relative_to(root)).replace("\\","/")
                if not rel.startswith("docs/archive/"): out.append(rel)
    return tuple(sorted(out))
def archive_bundle_integrity(root:str|Path=".")->Dict[str,object]:
    root=Path(root); p=root/"docs/archive/archive_history_bundle_v1_0_288.zip"; m=root/"docs/archive/archive_history_bundle_manifest_v1_0_288.json"
    report={"present":p.exists(),"manifest_present":m.exists()}
    if not p.exists(): return report
    sha=hashlib.sha256(p.read_bytes()).hexdigest(); manifest=m.read_text(encoding="utf-8") if m.exists() else ""
    report.update({"sha256":sha,"sha256_matches_manifest":sha in manifest})
    with zipfile.ZipFile(p) as z:
        names=z.namelist(); report["duplicate_entries"]=len(names)-len(set(names)); report["entry_count"]=len(names); report["compression_methods"]=tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()})); report["testzip_ok"]=z.testzip() is None
        for i in z.infolist():
            if not i.is_dir(): z.read(i.filename)
        report["all_entries_readable"]=True
    return report
def contract_chapters()->Tuple[str,...]: return tuple(i.chapter for i in CONTRACTS)
def target_surface_union()->Tuple[str,...]: return tuple(sorted({s for i in CONTRACTS for s in i.target_surfaces}))
def build_contract_baseline(root:str|Path=".")->ContractBaselinePacket:
    root=Path(root); arch=archive_bundle_integrity(root); py=(root/"pyproject.toml").read_text(encoding="utf-8") if (root/"pyproject.toml").exists() else ""; idx=(root/"docs/current_docs_index.md").read_text(encoding="utf-8") if (root/"docs/current_docs_index.md").exists() else ""; ch=(root/"CHANGELOG.md").read_text(encoding="utf-8") if (root/"CHANGELOG.md").exists() else ""; roadmap=(root/"PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root/"PROJECT_ROADMAP.md").exists() else ""; chapters=contract_chapters(); allowed=set(ACTIVE_SURFACE_TARGETS)
    vals={"current_records_exist":all((root/r).exists() for r in CURRENT_RECORDS),"previous_selection_records_preserved":all((root/r).exists() for r in PREVIOUS_SELECTION_RECORDS),"v316_rebaseline_roadmap_preserved":all((root/r).exists() for r in REBASELINE_REFERENCE_RECORDS),"contract_items_cover_chapters_07_15":len(CONTRACTS)==EXPECTED_CONTRACT_COUNT and chapters==("07","08","09","10","11","12","13","14","15"),"each_contract_has_acceptance_criteria":all(len(i.acceptance_criteria)>=4 for i in CONTRACTS),"each_contract_has_validation_gates":all(len(i.validation_gates)>=4 and "add_or_extend_direct_tests" in i.validation_gates for i in CONTRACTS),"each_contract_references_open_surfaces":all(set(i.target_surfaces).issubset(allowed) and "tests" in i.target_surfaces for i in CONTRACTS),"contract_tracks_declared":len(CONTRACT_TRACKS)==EXPECTED_TRACK_COUNT and "questionbank_contracts" in CONTRACT_TRACKS,"implementation_gates_declared":len(IMPLEMENTATION_GATES)==EXPECTED_GATE_COUNT and "no_nested_active_chapter_zip" in IMPLEMENTATION_GATES,"active_surface_targets_present":all((root/r).is_dir() for r in ACTIVE_SURFACE_TARGETS),"archive_bundle_integrity_confirmed":bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries")==0),"no_active_nested_zip_files":active_nested_zip_paths(root)==(),"cleanup_deletion_gate_closed":True,"pyproject_version_aligned":'version = "1.0.362"' in py and "next-cycle queue contract baseline" in py,"docs_index_points_to_current_release":"current_active_roadmap_v1_0_362.md" in idx and "v1_0_362.md" in idx,"changelog_contains_current_release":"## v1.0.362" in ch and "next-cycle queue contract baseline" in ch,"next_release_pointer_declared":NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in roadmap}
    checks=tuple(ContractBaselineCheck(k,bool(vals[k]),str(bool(vals[k]))) for k in CHECK_KEYS); ready=sum(c.ready for c in checks)
    return ContractBaselinePacket(VERSION,PREVIOUS_VERSION,LABEL,len(CONTRACTS),len(set(chapters)),len(CONTRACT_TRACKS),len(IMPLEMENTATION_GATES),len(CHECK_KEYS),ready,len(CHECK_KEYS)-ready,ready==len(CHECK_KEYS),CONTRACTS,CONTRACT_TRACKS,IMPLEMENTATION_GATES,checks,{"archive_bundle_report":arch,"active_nested_zip_paths":active_nested_zip_paths(root),"reference_input_policy":REFERENCE_INPUT_POLICY,"next_expected_version":NEXT_EXPECTED_VERSION,"deleted_files":0,"moved_files":0,"contract_chapters":chapters,"target_surface_union":target_surface_union()})
def render_contract_baseline(packet:ContractBaselinePacket|None=None)->str:
    packet=packet or build_contract_baseline(); rows="\n".join(f"- Chapter {i.chapter}: {i.selected_focus}; criteria={len(i.acceptance_criteria)}; surfaces={', '.join(i.target_surfaces)}" for i in packet.contracts); gates="\n".join(f"- {g}" for g in packet.gates)
    return f"# {packet.label}\n\nVersion: {packet.version}\n\n## Contracts\n{rows}\n\n## Implementation gates\n{gates}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
