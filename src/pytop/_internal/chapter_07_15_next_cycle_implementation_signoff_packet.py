"""Chapter 07--15 next-cycle implementation signoff packet for v1.0.368."""
from pathlib import Path
import hashlib, os, zipfile
VERSION = "v1.0.368"
PREVIOUS_VERSION = "v1.0.367"
LABEL = "Chapter 07--15 next-cycle implementation signoff packet"
NEXT_EXPECTED_VERSION = "v1.0.369 Chapter 07--15 next-cycle post-signoff roadmap refresh"
CHAPTERS = ("07","08","09","10","11","12","13","14","15")
SIGNOFF_ITEMS = (('07', 'Continuity and homeomorphism', 'continuity/homeomorphism API, examples, notebook, and crosswalk records closed and signed off'), ('08', 'Metric and normed topology', 'metric/normed examples and questionbank bridge closed and signed off'), ('09', 'Countability and separability', 'countability hierarchy and separability theorem-profile records closed and signed off'), ('10', 'Separation axioms', 'T1/Hausdorff/regular/normal guardrails closed and signed off'), ('11', 'Compactness variants', 'FIP/local/sequential/metric compactness bridge closed and signed off'), ('12', 'Product topology and subbases', 'finite product/subbase/Cantor learning-path queue closed and signed off'), ('13', 'Connectedness and paths', 'connectedness/path-component/homotopy learning-path records closed and signed off'), ('14', 'Complete metric spaces', 'Cauchy/completeness/Baire learning-path records closed and signed off'), ('15', 'Function spaces and convergence', 'pointwise/uniform/compact-open/convergence records closed and signed off'))
EXPECTED_CHAIN = ("v1.0.361 queue selection","v1.0.362 contract baseline","v1.0.363 implementation pass","v1.0.364 regression gate","v1.0.365 remediation pass","v1.0.366 second regression gate","v1.0.367 closure checkpoint","v1.0.368 signoff packet")
CURRENT_RECORDS = ("docs/current_docs_index.md","MANIFEST.md","PROJECT_ROADMAP.md","README.md","CHANGELOG.md","pyproject.toml","docs/roadmap/current_active_roadmap_v1_0_368.md","docs/roadmap/active_versioning_roadmap_v1_0_368.md","docs/releases/v1_0_368.md","src/pytop/chapter_07_15_next_cycle_implementation_signoff_packet.py","tests/core/test_chapter_07_15_next_cycle_implementation_signoff_packet_v368.py")
PREDECESSOR_RECORDS = ("docs/roadmap/current_active_roadmap_v1_0_361.md","docs/roadmap/current_active_roadmap_v1_0_362.md","docs/roadmap/current_active_roadmap_v1_0_363.md","docs/roadmap/current_active_roadmap_v1_0_364.md","docs/roadmap/current_active_roadmap_v1_0_365.md","docs/roadmap/current_active_roadmap_v1_0_366.md","docs/roadmap/current_active_roadmap_v1_0_367.md")
def active_nested_zip_paths(root="."):
    root=Path(root); out=[]
    for dp,_,fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".zip"):
                rel=str((Path(dp)/fn).relative_to(root)).replace("\\","/")
                if not rel.startswith("docs/archive/"): out.append(rel)
    return tuple(sorted(out))
def archive_bundle_integrity(root="."):
    root=Path(root); bundle=root/"docs/archive/archive_history_bundle_v1_0_288.zip"; manifest=root/"docs/archive/archive_history_bundle_manifest_v1_0_288.json"
    data=bundle.read_bytes(); sha=hashlib.sha256(data).hexdigest(); mt=manifest.read_text(encoding="utf-8")
    with zipfile.ZipFile(bundle) as z:
        names=z.namelist(); bad=z.testzip()
    return {"sha256":sha,"sha256_matches_manifest":sha in mt,"testzip_ok":bad is None,"duplicate_entries":len(names)-len(set(names)),"entry_count":len(names)}
def build_signoff_packet(root="."):
    root=Path(root); archive=archive_bundle_integrity(root)
    checks={
      "current_records_exist": all((root/r).exists() for r in CURRENT_RECORDS),
      "predecessor_records_preserved": all((root/r).exists() for r in PREDECESSOR_RECORDS),
      "chapter_coverage": tuple(x[0] for x in SIGNOFF_ITEMS)==CHAPTERS,
      "no_active_nested_zip_files": active_nested_zip_paths(root)==(),
      "archive_bundle_integrity": archive["sha256_matches_manifest"] and archive["testzip_ok"] and archive["duplicate_entries"]==0,
      "next_pointer_declared": "v1.0.369" in (root/"README.md").read_text(encoding="utf-8"),
    }
    ready=sum(bool(v) for v in checks.values())
    return {"version":VERSION,"previous_version":PREVIOUS_VERSION,"label":LABEL,"ready":ready==len(checks),"ready_check_count":ready,"check_count":len(checks),"blocked_check_count":len(checks)-ready,"checks":checks,"metadata":{"archive_bundle_report":archive,"active_nested_zip_paths":active_nested_zip_paths(root),"deleted_files":0,"moved_files":0}}
