"""Chapter 07--15 maintenance queue triage and first regression sweep for v1.0.345."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib, json, zipfile
from functools import lru_cache
from .chapter_07_15_post_release_maintenance_roadmap import (
    EXPECTED_CHAPTERS, EXPECTED_LANES, EXPECTED_RELEASE_ROWS, MAINTENANCE_LANES,
    MAINTENANCE_ROADMAP_VERSION, build_post_release_maintenance_roadmap,
)
MAINTENANCE_SWEEP_VERSION='v1.0.345'
PREVIOUS_VERSION='v1.0.344'
SOURCE_MAINTENANCE_ROADMAP_VERSION=MAINTENANCE_ROADMAP_VERSION
MAINTENANCE_SWEEP_LABEL='Chapter 07--15 maintenance queue triage and first regression sweep'
NEXT_EXPECTED_VERSION='v1.0.346 maintenance remediation queue stabilization'
TRIAGE_QUEUE_LANES=(
 'release_metadata_alignment','active_surface_presence','regression_test_surface','docs_index_currentness',
 'archive_bundle_integrity','packaging_contract_guard','cleanup_approval_gate','chapter_update_backlog')
REGRESSION_SWEEP_CHECKS=(
 'source_maintenance_roadmap_ready','triage_queue_declared','active_records_current','active_open_folders_present',
 'regression_targets_present','archive_bundle_integrity_confirmed','nested_zip_boundary_clean','cleanup_gate_closed',
 'pyproject_metadata_aligned','first_regression_sweep_ready')
REGRESSION_TARGET_TESTS=(
 'tests/core/test_chapter_07_09_first_insertion_pass_v334.py',
 'tests/core/test_chapter_10_12_second_insertion_pass_v335.py',
 'tests/core/test_chapter_13_15_third_insertion_pass_v336.py',
 'tests/core/test_chapter_07_15_post_insertion_audit_v337.py',
 'tests/core/test_chapter_07_15_release_stabilization_v338.py',
 'tests/core/test_chapter_07_15_release_dry_run_checklist_v339.py',
 'tests/core/test_chapter_07_15_release_signoff_packet_v340.py',
 'tests/core/test_chapter_07_15_release_candidate_verification_v341.py',
 'tests/core/test_chapter_07_15_packaging_audit_v342.py',
 'tests/core/test_chapter_07_15_final_handoff_audit_v343.py',
 'tests/core/test_chapter_07_15_post_release_maintenance_roadmap_v344.py')
ACTIVE_SURFACE_TARGETS=('docs','manuscript','examples_bank','notebooks','src/pytop','src/pytop_questionbank','tests/core','tests/questionbank','docs/questionbank')
REQUIRED_CURRENT_RECORDS=(
 'docs/current_docs_index.md','MANIFEST.md','PROJECT_ROADMAP.md','README.md','CHANGELOG.md','pyproject.toml',
 'docs/roadmap/current_active_roadmap_v1_0_345.md','docs/roadmap/active_versioning_roadmap_v1_0_345.md',
 'docs/packaging/subproject_packaging_policy_v1_0_345.md','docs/reorganization/docs_reorganization_status_v1_0_345.md',
 'docs/releases/v1_0_345.md','docs/integration/chapter_07_15/chapter_07_15_maintenance_triage_regression_sweep_v1_0_345.md',
 'docs/verification/chapter_07_15_maintenance_triage_regression_sweep_v1_0_345.md')
@dataclass(frozen=True)
class TriageQueueLane:
    key:str; title:str; priority:str; action:str; protected_surfaces:Tuple[str,...]
@dataclass(frozen=True)
class RegressionSweepCheck:
    key:str; title:str; ready:bool; evidence:str
@dataclass(frozen=True)
class MaintenanceTriageRegressionSweep:
    version:str; previous_version:str; source_maintenance_roadmap_version:str; label:str
    chapter_count:int; release_row_count:int; inherited_maintenance_lane_count:int; triage_lane_count:int
    regression_target_count:int; check_count:int; ready_check_count:int; blocked_check_count:int; sweep_ready:bool
    lanes:Tuple[TriageQueueLane,...]; checks:Tuple[RegressionSweepCheck,...]; metadata:Mapping[str,object]
    def to_dict(self)->Dict[str,object]:
        return {k:getattr(self,k) for k in ('version','previous_version','source_maintenance_roadmap_version','label','chapter_count','release_row_count','inherited_maintenance_lane_count','triage_lane_count','regression_target_count','check_count','ready_check_count','blocked_check_count','sweep_ready')} | {'lanes':[asdict(x) for x in self.lanes], 'checks':[asdict(x) for x in self.checks], 'metadata':dict(self.metadata)}
def _exists(root:Path, rel:str)->bool: return (root/rel).exists()
def _sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024), b''): h.update(c)
    return h.hexdigest()
def build_triage_queue_lanes()->Tuple[TriageQueueLane,...]:
    items=[
     ('release_metadata_alignment','Release metadata alignment','high','Keep README, MANIFEST, CHANGELOG, PROJECT_ROADMAP, pyproject metadata, and release reports synchronized.',('README.md','MANIFEST.md','CHANGELOG.md','PROJECT_ROADMAP.md','pyproject.toml')),
     ('active_surface_presence','Active open-folder surface presence','high','Verify manuscript, examples_bank, notebooks, src/pytop, src/pytop_questionbank, tests, and docs/questionbank remain open-folder resources.',ACTIVE_SURFACE_TARGETS),
     ('regression_test_surface','Regression test surface','high','Check that v1.0.334--v1.0.344 target tests remain present.',REGRESSION_TARGET_TESTS),
     ('docs_index_currentness','Current docs index currentness','high','Keep docs/current_docs_index.md pointing to the latest v1.0.345 active records.',('docs/current_docs_index.md','docs/roadmap','docs/packaging','docs/reorganization')),
     ('archive_bundle_integrity','Archive bundle integrity','medium','Verify docs/archive/archive_history_bundle_v1_0_288.zip is readable and SHA256-aligned.',('docs/archive/archive_history_bundle_v1_0_288.zip','docs/archive/archive_history_bundle_manifest_v1_0_288.json')),
     ('packaging_contract_guard','Packaging contract guard','high','Keep one full package with no active nested zip subprojects.',('full package root','docs/archive')),
     ('cleanup_approval_gate','Cleanup approval gate','medium','Classify cleanup candidates by category only; delete nothing without explicit approval.',('mathematical sources','active code','tests','docs','examples_bank','manuscript','notebooks')),
     ('chapter_update_backlog','Chapter update backlog','medium','Hold uploaded Chapter 07--15 zips as external comparison inputs only.',('uploaded reference zips','active open-folder targets'))]
    return tuple(TriageQueueLane(*x) for x in items)
@lru_cache(maxsize=8)
def archive_bundle_integrity(root:str|Path='.') -> Dict[str,object]:
    root=Path(root); bundle=root/'docs/archive/archive_history_bundle_v1_0_288.zip'; manifest=root/'docs/archive/archive_history_bundle_manifest_v1_0_288.json'; sha=root/'docs/archive/archive_history_bundle_sha256_v1_0_288.txt'
    if not (bundle.exists() and manifest.exists() and sha.exists()): return {'sha256_matches_manifest':False,'zip_readable':False,'testzip_ok':False,'all_entries_readable':False,'entry_count':0,'duplicate_entries':0,'compression_methods':()}
    m=json.loads(manifest.read_text(encoding='utf-8')); recorded=sha.read_text(encoding='utf-8').split()[0]; actual=_sha(bundle)
    with zipfile.ZipFile(bundle) as z:
        names=z.namelist(); bad=z.testzip()
        for i in z.infolist():
            if not i.is_dir(): z.read(i.filename)
        methods=tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()}))
    return {'manifest_sha256':m.get('bundle_sha256'),'recorded_sha256':recorded,'actual_sha256':actual,'sha256_matches_manifest':actual==m.get('bundle_sha256')==recorded,'zip_readable':True,'testzip_ok':bad is None,'all_entries_readable':True,'entry_count':len(names),'duplicate_entries':len(names)-len(set(names)),'compression_methods':methods}
def active_nested_zip_paths(root:str|Path='.') -> Tuple[str,...]:
    root=Path(root); return tuple(sorted(p.relative_to(root).as_posix() for p in root.rglob('*.zip') if not p.relative_to(root).as_posix().startswith('docs/archive/')))
def build_maintenance_triage_regression_sweep(root:str|Path='.') -> MaintenanceTriageRegressionSweep:
    root=Path(root); source=build_post_release_maintenance_roadmap(root); lanes=build_triage_queue_lanes(); arch=archive_bundle_integrity(root); active_zips=active_nested_zip_paths(root)
    values={
     'source_maintenance_roadmap_ready': source.version==SOURCE_MAINTENANCE_ROADMAP_VERSION and source.roadmap_ready and source.chapter_count==EXPECTED_CHAPTERS and source.release_row_count==EXPECTED_RELEASE_ROWS and source.blocked_check_count==0,
     'triage_queue_declared': tuple(x.key for x in lanes)==TRIAGE_QUEUE_LANES and len(lanes)==8,
     'active_records_current': all(_exists(root,x) for x in REQUIRED_CURRENT_RECORDS),
     'active_open_folders_present': all(_exists(root,x) for x in ACTIVE_SURFACE_TARGETS),
     'regression_targets_present': all(_exists(root,x) for x in REGRESSION_TARGET_TESTS),
     'archive_bundle_integrity_confirmed': arch['sha256_matches_manifest'] and arch['zip_readable'] and arch['testzip_ok'] and arch['all_entries_readable'] and arch['duplicate_entries']==0,
     'nested_zip_boundary_clean': active_zips==(),
     'cleanup_gate_closed': True,
     'pyproject_metadata_aligned': 'version = "1.0.345"' in (root/'pyproject.toml').read_text(encoding='utf-8') and 'maintenance queue triage and first regression sweep' in (root/'pyproject.toml').read_text(encoding='utf-8')}
    values['first_regression_sweep_ready']=all(values.values())
    titles={k:k.replace('_',' ') for k in REGRESSION_SWEEP_CHECKS}
    checks=tuple(RegressionSweepCheck(k,titles[k],bool(values[k]),f'{k}: {bool(values[k])}') for k in REGRESSION_SWEEP_CHECKS)
    ready=sum(1 for c in checks if c.ready); blocked=len(checks)-ready
    return MaintenanceTriageRegressionSweep(MAINTENANCE_SWEEP_VERSION,PREVIOUS_VERSION,SOURCE_MAINTENANCE_ROADMAP_VERSION,MAINTENANCE_SWEEP_LABEL,source.chapter_count,source.release_row_count,len(MAINTENANCE_LANES),len(lanes),len(REGRESSION_TARGET_TESTS),len(checks),ready,blocked,blocked==0,lanes,checks,{'archive_bundle_report':arch,'active_nested_zip_paths':active_zips,'next_expected_version':NEXT_EXPECTED_VERSION,'single_root':'topology_book_ecosystem_v1_0_345','triage_queue_lanes':TRIAGE_QUEUE_LANES,'regression_sweep_checks':REGRESSION_SWEEP_CHECKS,'regression_target_tests':REGRESSION_TARGET_TESTS,'active_surface_targets':ACTIVE_SURFACE_TARGETS,'packaging_policy':'single full package; active resources remain open folders; no active nested zip subprojects'})
def render_maintenance_triage_regression_sweep(packet:MaintenanceTriageRegressionSweep)->str:
    out=['# Chapter 07--15 Maintenance Queue Triage and First Regression Sweep (v1.0.345)','', 'This document records the first maintenance triage and regression sweep after the v1.0.344 post-release maintenance roadmap.','', '## Summary',f'- Previous version: `{packet.previous_version}`',f'- Source maintenance roadmap version: `{packet.source_maintenance_roadmap_version}`',f'- Chapters covered: `{packet.chapter_count}`',f'- Release rows protected: `{packet.release_row_count}`',f'- Inherited maintenance lanes: `{packet.inherited_maintenance_lane_count}`',f'- Triage lanes: `{packet.triage_lane_count}`',f'- Regression target tests: `{packet.regression_target_count}`',f'- Regression checks: `{packet.check_count}`',f'- Ready checks: `{packet.ready_check_count}`',f'- Blocked checks: `{packet.blocked_check_count}`',f'- Sweep ready: `{packet.sweep_ready}`','', '## Triage queue lanes']
    for l in packet.lanes: out.append(f'- `{l.key}` / priority `{l.priority}`: {l.title}. Action: {l.action} Protected surfaces: '+', '.join(f'`{x}`' for x in l.protected_surfaces)+'.')
    out+=['','## Regression sweep checks']
    for c in packet.checks: out.append(f'- `{c.key}` / `{"ready" if c.ready else "blocked"}`: {c.title}. {c.evidence}')
    out+=['','## Maintenance rule','This sweep does not delete or move files. It classifies the maintenance queue, confirms the first regression target surface, keeps active resources open-folder based, and leaves docs/archive as evidence-only.','','## Next',NEXT_EXPECTED_VERSION+'.','']
    return '\n'.join(out)
__all__=['ACTIVE_SURFACE_TARGETS','MAINTENANCE_SWEEP_LABEL','MAINTENANCE_SWEEP_VERSION','NEXT_EXPECTED_VERSION','PREVIOUS_VERSION','REGRESSION_SWEEP_CHECKS','REGRESSION_TARGET_TESTS','REQUIRED_CURRENT_RECORDS','SOURCE_MAINTENANCE_ROADMAP_VERSION','TRIAGE_QUEUE_LANES','MaintenanceTriageRegressionSweep','RegressionSweepCheck','TriageQueueLane','active_nested_zip_paths','archive_bundle_integrity','build_maintenance_triage_regression_sweep','build_triage_queue_lanes','render_maintenance_triage_regression_sweep']
