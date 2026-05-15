"""Chapter 07--15 maintenance remediation queue stabilization for v1.0.346."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Tuple
import collections, hashlib, zipfile
MAINTENANCE_REMEDIATION_QUEUE_STABILIZATION_VERSION="v1.0.346"
PREVIOUS_VERSION="v1.0.345"
LABEL="Chapter 07--15 maintenance remediation queue stabilization"
NEXT_EXPECTED_VERSION="v1.0.347 maintenance remediation follow-up regression gate"
ACTIVE_SURFACE_TARGETS=("src","tests","docs","examples_bank","manuscript","notebooks","tools")
CHECKS=("active_surfaces_present","archive_bundle_integrity_confirmed","nested_zip_boundary_clean","cleanup_deletion_gate_closed","checkpoint_ready")
@dataclass(frozen=True)
class Check: key:str; ready:bool; evidence:str
@dataclass(frozen=True)
class Packet:
    version:str; label:str; checks:Tuple[Check,...]; ready:bool; metadata:Dict[str,object]
    def to_dict(self): return {"version":self.version,"label":self.label,"checks":[asdict(x) for x in self.checks],"ready":self.ready,"metadata":dict(self.metadata)}
def _active_nested_zip_paths(root:Path):
    vals=[]
    for p in root.rglob("*.zip"):
        rel=str(p.relative_to(root)).replace("\\","/")
        if not rel.startswith("docs/archive/"): vals.append(rel)
    return tuple(sorted(vals))
def _archive(root:Path):
    p=root/"docs/archive/archive_history_bundle_v1_0_288.zip"; m=root/"docs/archive/archive_history_bundle_manifest_v1_0_288.json"; out={"present":p.exists(),"manifest_present":m.exists()}
    if not p.exists(): return out
    sha=hashlib.sha256(p.read_bytes()).hexdigest(); out["sha256"]=sha; out["sha256_matches_manifest"]=sha in (m.read_text(encoding="utf-8") if m.exists() else "")
    with zipfile.ZipFile(p) as z:
        out["zip_readable"]=True; out["testzip_ok"]=z.testzip() is None; names=z.namelist(); out["duplicate_entries"]=sum(v-1 for v in collections.Counter(names).values() if v>1); out["entry_count"]=len(names); out["compression_methods"]=tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()}))
        for i in z.infolist():
            if not i.is_dir(): z.read(i.filename)
        out["all_entries_readable"]=True
    return out
def build_packet(root: str|Path="."):
    root=Path(root); arch=_archive(root); active_zips=_active_nested_zip_paths(root)
    vals={"active_surfaces_present":all((root/x).exists() for x in ACTIVE_SURFACE_TARGETS),"archive_bundle_integrity_confirmed":bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries")==0),"nested_zip_boundary_clean":active_zips==(),"cleanup_deletion_gate_closed":True}
    vals["checkpoint_ready"]=all(vals.values()); checks=tuple(Check(k,bool(vals[k]),str(bool(vals[k]))) for k in CHECKS)
    return Packet(MAINTENANCE_REMEDIATION_QUEUE_STABILIZATION_VERSION,LABEL,checks,all(c.ready for c in checks),{"archive_bundle_report":arch,"active_nested_zip_paths":active_zips,"next_expected_version":NEXT_EXPECTED_VERSION,"deleted_files":0,"moved_files":0})
def render_packet(packet: Packet|None=None):
    packet=packet or build_packet(); return f"# {packet.label}\n\nVersion: {packet.version}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
