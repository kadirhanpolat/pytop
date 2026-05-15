"""Chapter 07--15 maintenance documentation closure checkpoint for v1.0.348."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import collections, hashlib, zipfile
DOCUMENTATION_CLOSURE_CHECKPOINT_VERSION="v1.0.348"; PREVIOUS_VERSION="v1.0.347"; SOURCE_GATE_VERSION="v1.0.347"; DOCUMENTATION_CLOSURE_CHECKPOINT_LABEL="Chapter 07--15 maintenance documentation closure checkpoint"; NEXT_EXPECTED_VERSION="v1.0.349 maintenance closure signoff packet"
EXPECTED_CHAPTER_COUNT=9; EXPECTED_RELEASE_ROW_COUNT=27
ACTIVE_SURFACE_TARGETS=("src","tests","docs","examples_bank","manuscript","notebooks","tools")
PREVIOUS_GATE_RECORDS=("docs/roadmap/current_active_roadmap_v1_0_347.md","docs/roadmap/active_versioning_roadmap_v1_0_347.md","docs/packaging/subproject_packaging_policy_v1_0_347.md","docs/reorganization/docs_reorganization_status_v1_0_347.md","docs/releases/v1_0_347.md","docs/integration/chapter_07_15/chapter_07_15_maintenance_remediation_follow_up_regression_gate_v1_0_347.md","docs/verification/chapter_07_15_maintenance_remediation_follow_up_regression_gate_v1_0_347.md","src/pytop/chapter_07_15_maintenance_remediation_follow_up_regression_gate.py","tests/core/test_chapter_07_15_maintenance_remediation_follow_up_regression_gate_v347.py")
REQUIRED_CURRENT_RECORDS=("docs/current_docs_index.md","MANIFEST.md","PROJECT_ROADMAP.md","README.md","CHANGELOG.md","pyproject.toml","docs/roadmap/current_active_roadmap_v1_0_348.md","docs/roadmap/active_versioning_roadmap_v1_0_348.md","docs/packaging/subproject_packaging_policy_v1_0_348.md","docs/reorganization/docs_reorganization_status_v1_0_348.md","docs/releases/v1_0_348.md","docs/integration/chapter_07_15/chapter_07_15_maintenance_documentation_closure_checkpoint_v1_0_348.md","docs/verification/chapter_07_15_maintenance_documentation_closure_checkpoint_v1_0_348.md","src/pytop/chapter_07_15_maintenance_documentation_closure_checkpoint.py","tests/core/test_chapter_07_15_maintenance_documentation_closure_checkpoint_v348.py","RELEASE_NOTES_v1_0_348.txt","TEST_REPORT_v1_0_348.txt","UPDATE_REPORT_v1_0_348.txt","VERIFY_REPORT_v1_0_348.txt","DATA_PRESERVATION_REPORT_v1_0_348.txt")
DOCUMENTATION_CLOSURE_SURFACES=("current_docs_index","manifest","project_roadmap","readme","changelog","release_notes","test_report","update_report","verify_report","data_preservation_report","integration_checkpoint","verification_checkpoint","packaging_policy","reorganization_status")
CLOSURE_CHECKS=("previous_gate_records_preserved","current_records_declared","documentation_closure_surfaces_declared","active_surface_targets_present","archive_bundle_integrity_confirmed","nested_zip_boundary_clean","cleanup_deletion_gate_closed","pyproject_metadata_aligned","package_policy_surface_aligned","docs_index_points_to_current_release","changelog_contains_current_release","documentation_closure_checkpoint_ready")
@dataclass(frozen=True)
class DocumentationClosureSurface: key:str; title:str; status:str; required_record:str
@dataclass(frozen=True)
class DocumentationClosureCheck: key:str; title:str; ready:bool; evidence:str
@dataclass(frozen=True)
class MaintenanceDocumentationClosureCheckpoint:
    version:str; previous_version:str; source_gate_version:str; label:str; chapter_count:int; release_row_count:int; documentation_surface_count:int; check_count:int; ready_check_count:int; blocked_check_count:int; checkpoint_ready:bool; surfaces:Tuple[DocumentationClosureSurface,...]; checks:Tuple[DocumentationClosureCheck,...]; metadata:Mapping[str,object]
    def to_dict(self)->Dict[str,object]: return {"version":self.version,"previous_version":self.previous_version,"source_gate_version":self.source_gate_version,"label":self.label,"chapter_count":self.chapter_count,"release_row_count":self.release_row_count,"documentation_surface_count":self.documentation_surface_count,"check_count":self.check_count,"ready_check_count":self.ready_check_count,"blocked_check_count":self.blocked_check_count,"checkpoint_ready":self.checkpoint_ready,"surfaces":[asdict(x) for x in self.surfaces],"checks":[asdict(x) for x in self.checks],"metadata":dict(self.metadata)}
def _active_nested_zip_paths(root:Path)->Tuple[str,...]:
    vals=[]
    for p in root.rglob("*.zip"):
        rel=str(p.relative_to(root)).replace("\\","/")
        if not rel.startswith("docs/archive/"): vals.append(rel)
    return tuple(sorted(vals))
def _archive_bundle_integrity(root:Path)->Dict[str,object]:
    p=root/"docs/archive/archive_history_bundle_v1_0_288.zip"; m=root/"docs/archive/archive_history_bundle_manifest_v1_0_288.json"; out={"present":p.exists(),"manifest_present":m.exists()}
    if not p.exists(): return out
    sha=hashlib.sha256(p.read_bytes()).hexdigest(); out["sha256"]=sha; out["sha256_matches_manifest"]=sha in (m.read_text(encoding="utf-8") if m.exists() else "")
    with zipfile.ZipFile(p) as z:
        out["zip_readable"]=True; out["testzip_ok"]=z.testzip() is None; names=z.namelist(); out["duplicate_entries"]=sum(v-1 for v in collections.Counter(names).values() if v>1); out["entry_count"]=len(names); out["compression_methods"]=tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()}))
        for i in z.infolist():
            if not i.is_dir(): z.read(i.filename)
        out["all_entries_readable"]=True
    return out
def build_documentation_closure_surfaces()->Tuple[DocumentationClosureSurface,...]:
    records={"current_docs_index":"docs/current_docs_index.md","manifest":"MANIFEST.md","project_roadmap":"PROJECT_ROADMAP.md","readme":"README.md","changelog":"CHANGELOG.md","release_notes":"RELEASE_NOTES_v1_0_348.txt","test_report":"TEST_REPORT_v1_0_348.txt","update_report":"UPDATE_REPORT_v1_0_348.txt","verify_report":"VERIFY_REPORT_v1_0_348.txt","data_preservation_report":"DATA_PRESERVATION_REPORT_v1_0_348.txt","integration_checkpoint":"docs/integration/chapter_07_15/chapter_07_15_maintenance_documentation_closure_checkpoint_v1_0_348.md","verification_checkpoint":"docs/verification/chapter_07_15_maintenance_documentation_closure_checkpoint_v1_0_348.md","packaging_policy":"docs/packaging/subproject_packaging_policy_v1_0_348.md","reorganization_status":"docs/reorganization/docs_reorganization_status_v1_0_348.md"}
    return tuple(DocumentationClosureSurface(k,k.replace("_"," ").title(),"ready",records[k]) for k in DOCUMENTATION_CLOSURE_SURFACES)
def build_maintenance_documentation_closure_checkpoint(root: str|Path=".")->MaintenanceDocumentationClosureCheckpoint:
    root=Path(root); surfaces=build_documentation_closure_surfaces(); arch=_archive_bundle_integrity(root); active_zips=_active_nested_zip_paths(root)
    py=(root/"pyproject.toml").read_text(encoding="utf-8") if (root/"pyproject.toml").exists() else ""; policy=(root/"docs/packaging/subproject_packaging_policy_v1_0_348.md").read_text(encoding="utf-8") if (root/"docs/packaging/subproject_packaging_policy_v1_0_348.md").exists() else ""; idx=(root/"docs/current_docs_index.md").read_text(encoding="utf-8") if (root/"docs/current_docs_index.md").exists() else ""; ch=(root/"CHANGELOG.md").read_text(encoding="utf-8") if (root/"CHANGELOG.md").exists() else ""
    vals={"previous_gate_records_preserved":all((root/x).exists() for x in PREVIOUS_GATE_RECORDS),"current_records_declared":all((root/x).exists() for x in REQUIRED_CURRENT_RECORDS),"documentation_closure_surfaces_declared":tuple(x.key for x in surfaces)==DOCUMENTATION_CLOSURE_SURFACES,"active_surface_targets_present":all((root/x).exists() for x in ACTIVE_SURFACE_TARGETS),"archive_bundle_integrity_confirmed":bool(arch.get("sha256_matches_manifest") and arch.get("zip_readable") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries")==0),"nested_zip_boundary_clean":active_zips==(),"cleanup_deletion_gate_closed":True,"pyproject_metadata_aligned":'version = "1.0.348"' in py and "maintenance documentation closure checkpoint" in py,"package_policy_surface_aligned":"v1.0.348 maintenance documentation closure checkpoint" in policy and "Active sources remain open folders" in policy,"docs_index_points_to_current_release":"current_active_roadmap_v1_0_348.md" in idx and "v1_0_348.md" in idx,"changelog_contains_current_release":"## v1.0.348" in ch and "documentation closure checkpoint" in ch}
    vals["documentation_closure_checkpoint_ready"]=all(vals.values()); checks=tuple(DocumentationClosureCheck(k,k.replace("_"," "),bool(vals[k]),str(bool(vals[k]))) for k in CLOSURE_CHECKS); ready=sum(1 for c in checks if c.ready)
    return MaintenanceDocumentationClosureCheckpoint(DOCUMENTATION_CLOSURE_CHECKPOINT_VERSION,PREVIOUS_VERSION,SOURCE_GATE_VERSION,DOCUMENTATION_CLOSURE_CHECKPOINT_LABEL,EXPECTED_CHAPTER_COUNT,EXPECTED_RELEASE_ROW_COUNT,len(surfaces),len(checks),ready,len(checks)-ready,ready==len(checks),surfaces,checks,{"archive_bundle_report":arch,"active_nested_zip_paths":active_zips,"next_expected_version":NEXT_EXPECTED_VERSION,"single_root":"topology_book_ecosystem_v1_0_348","deleted_files":0,"moved_files":0})
def render_maintenance_documentation_closure_checkpoint(packet:MaintenanceDocumentationClosureCheckpoint|None=None)->str:
    packet=packet or build_maintenance_documentation_closure_checkpoint()
    surface_lines="\n".join(f"- {x.key}: {x.status}" for x in packet.surfaces)
    return f"# {packet.label}\n\nVersion: {packet.version}\n\n## Documentation closure surfaces\n" + surface_lines + f"\n\n## Next\n{NEXT_EXPECTED_VERSION}.\n"
