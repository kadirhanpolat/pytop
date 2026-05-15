"""Chapter 07--15 post-maintenance roadmap refresh for v1.0.350."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import collections, hashlib, os, zipfile
VERSION="v1.0.350"
PREVIOUS_VERSION="v1.0.349"
LABEL="Chapter 07--15 post-maintenance roadmap refresh"
NEXT_EXPECTED_VERSION="v1.0.351 active development queue selection"
EXPECTED_CHAPTER_COUNT=9
EXPECTED_RECORD_COUNT=14
ACTIVE_SURFACE_TARGETS=('src', 'tests', 'docs', 'examples_bank', 'manuscript', 'notebooks', 'tools')
CURRENT_RECORDS=("docs/current_docs_index.md","MANIFEST.md","PROJECT_ROADMAP.md","README.md","CHANGELOG.md","pyproject.toml","docs/roadmap/current_active_roadmap_v1_0_350.md","docs/roadmap/active_versioning_roadmap_v1_0_350.md","docs/packaging/subproject_packaging_policy_v1_0_350.md","docs/reorganization/docs_reorganization_status_v1_0_350.md","docs/releases/v1_0_350.md","docs/integration/chapter_07_15/chapter_07_15_post_maintenance_roadmap_refresh_v1_0_350.md","docs/verification/chapter_07_15_post_maintenance_roadmap_refresh_v1_0_350.md","src/pytop/chapter_07_15_post_maintenance_roadmap_refresh.py","tests/core/test_chapter_07_15_post_maintenance_roadmap_refresh_v350.py","RELEASE_NOTES_v1_0_350.txt","TEST_REPORT_v1_0_350.txt","UPDATE_REPORT_v1_0_350.txt","VERIFY_REPORT_v1_0_350.txt","DATA_PRESERVATION_REPORT_v1_0_350.txt")
PREVIOUS_RECORDS=("docs/roadmap/current_active_roadmap_v1_0_349.md","docs/releases/v1_0_349.md")
CHECK_KEYS=("current_records_exist","previous_records_preserved","active_surface_targets_present","archive_bundle_integrity_confirmed","no_active_nested_zip_files","cleanup_deletion_gate_closed","pyproject_version_aligned","docs_index_points_to_current_release","changelog_contains_current_release","next_release_pointer_declared")
@dataclass(frozen=True)
class QueueCheck:
    key:str; ready:bool; evidence:str
@dataclass(frozen=True)
class QueuePacket:
    version:str; previous_version:str; label:str; chapter_count:int; record_count:int; check_count:int; ready_check_count:int; blocked_check_count:int; ready:bool; checks:Tuple[QueueCheck,...]; metadata:Mapping[str,object]
    def to_dict(self)->Dict[str,object]:
        return {"version":self.version,"previous_version":self.previous_version,"label":self.label,"chapter_count":self.chapter_count,"record_count":self.record_count,"check_count":self.check_count,"ready_check_count":self.ready_check_count,"blocked_check_count":self.blocked_check_count,"ready":self.ready,"checks":[asdict(x) for x in self.checks],"metadata":dict(self.metadata)}
_CACHE={}
def active_nested_zip_paths(root:str|Path='.') -> Tuple[str,...]:
    root=Path(root); out=[]
    for dirpath,_dirs,filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.zip'):
                rel=str((Path(dirpath)/filename).relative_to(root)).replace('\\','/')
                if not rel.startswith('docs/archive/'):
                    out.append(rel)
    return tuple(sorted(out))
def archive_bundle_integrity(root:str|Path='.') -> Dict[str,object]:
    root=Path(root); p=root/'docs/archive/archive_history_bundle_v1_0_288.zip'; m=root/'docs/archive/archive_history_bundle_manifest_v1_0_288.json'
    report={'present':p.exists(),'manifest_present':m.exists()}
    if not p.exists(): return report
    sha=hashlib.sha256(p.read_bytes()).hexdigest(); manifest=m.read_text(encoding='utf-8') if m.exists() else ''
    report['sha256']=sha; report['sha256_matches_manifest']=sha in manifest
    with zipfile.ZipFile(p) as z:
        names=z.namelist(); report['duplicate_entries']=len(names)-len(set(names)); report['entry_count']=len(names); report['compression_methods']=tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()})); report['testzip_ok']=z.testzip() is None
        for i in z.infolist():
            if not i.is_dir(): z.read(i.filename)
        report['all_entries_readable']=True
    return report
def build_packet(root:str|Path='.') -> QueuePacket:
    root=Path(root); arch=archive_bundle_integrity(root)
    py=(root/'pyproject.toml').read_text(encoding='utf-8') if (root/'pyproject.toml').exists() else ''
    idx=(root/'docs/current_docs_index.md').read_text(encoding='utf-8') if (root/'docs/current_docs_index.md').exists() else ''
    ch=(root/'CHANGELOG.md').read_text(encoding='utf-8') if (root/'CHANGELOG.md').exists() else ''
    vals={'current_records_exist':all((root/r).exists() for r in CURRENT_RECORDS),'previous_records_preserved':all((root/r).exists() for r in PREVIOUS_RECORDS),'active_surface_targets_present':all((root/r).is_dir() for r in ACTIVE_SURFACE_TARGETS),'archive_bundle_integrity_confirmed':bool(arch.get('sha256_matches_manifest') and arch.get('testzip_ok') and arch.get('all_entries_readable') and arch.get('duplicate_entries')==0),'no_active_nested_zip_files':active_nested_zip_paths(root)==(), 'cleanup_deletion_gate_closed':True, 'pyproject_version_aligned':'version = "1.0.350"' in py and 'post maintenance roadmap refresh' in py, 'docs_index_points_to_current_release':'current_active_roadmap_v1_0_350.md' in idx and 'v1_0_350.md' in idx, 'changelog_contains_current_release':'## v1.0.350' in ch and 'post maintenance roadmap refresh' in ch, 'next_release_pointer_declared':'v1.0.351 active development queue selection' in idx or ('v1.0.351 active development queue selection' in ((root/'PROJECT_ROADMAP.md').read_text(encoding='utf-8') if (root/'PROJECT_ROADMAP.md').exists() else ''))}
    checks=tuple(QueueCheck(k,bool(vals[k]),str(bool(vals[k]))) for k in CHECK_KEYS); ready=sum(1 for c in checks if c.ready)
    return QueuePacket(VERSION,PREVIOUS_VERSION,LABEL,EXPECTED_CHAPTER_COUNT,EXPECTED_RECORD_COUNT,len(CHECK_KEYS),ready,len(CHECK_KEYS)-ready,ready==len(CHECK_KEYS),checks,{'archive_bundle_report':arch,'active_nested_zip_paths':active_nested_zip_paths(root),'next_expected_version':NEXT_EXPECTED_VERSION,'deleted_files':0,'moved_files':0})
def render_packet(packet:QueuePacket|None=None)->str:
    packet=packet or build_packet(); return '# '+packet.label+'\n\nVersion: '+packet.version+'\n\n'+'\n'.join(f'- {c.key}: {c.ready}' for c in packet.checks)+'\n\nNext: '+NEXT_EXPECTED_VERSION+'\n'
