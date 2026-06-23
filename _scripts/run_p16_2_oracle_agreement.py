#!/usr/bin/env py -3.14
"""P16.2 Autonomous Oracle Agreement Matrix Runner.

Generates comprehensive oracle agreement reports (JSON + Markdown):
  - All 45 knots × all available oracles
  - Persistent Betti validation
  - K-theory rational group cross-checks (if Sage available)
  - Dehn surgery H₁ (if SnapPy available)

Usage:
  py -3.14 _scripts/run_p16_2_oracle_agreement.py [--output DIR]

Output files:
  - oracle_agreement_report.json (machine-readable)
  - oracle_agreement_report.md (human-readable)
"""

import argparse
import sys
from pathlib import Path

# Ensure pytop is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.validation.oracle_agreement_builder import OracleAgreementBuilder


def main():
    parser = argparse.ArgumentParser(
        description="P16.2 Oracle Agreement Matrix Generator",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Output directory for reports (default: current directory)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Quick mode: sample only, skip full matrix",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[*] P16.2 Oracle Agreement Matrix Builder")
    print("=" * 60)

    builder = OracleAgreementBuilder()
    print(f"\n[+] Available oracles: {', '.join(builder.report.oracle_names) or 'None (install GUDHI/Ripser/SnapPy/Sage)'}")
    print(f"[+] Total knots in table: {len(builder.oracles)}")

    # Build agreement matrix
    print("\n[*] Building oracle agreement matrix...")
    print("    Testing: knot polynomials, persistent Betti, K-theory...")

    if args.fast:
        print("    (fast mode: sample tests only)")
        from tests.validation.fixtures import KnotTable

        builder.test_knot_polynomials(KnotTable.KNOTS[:5])
        builder.test_persistent_betti(sample_circles=1)
        # Ensure report.agreements is updated from builder.comparisons
        builder.report.agreements = builder.comparisons
    else:
        print("    (full mode: all tests)")
        builder.build()

    report = builder.report

    print(f"\n[OK] Matrix built: {report.total_tests} tests, {report.passed_tests} passed")
    print(f"     Agreement rate: {report.agreement_rate():.1%}")

    # Export JSON
    json_path = output_dir / "oracle_agreement_report.json"
    json_path.write_text(report.to_json(), encoding="utf-8")
    print(f"\n[*] JSON report: {json_path}")

    # Export Markdown
    md_path = output_dir / "oracle_agreement_report.md"
    md_path.write_text(report.to_markdown(), encoding="utf-8")
    print(f"[*] Markdown report: {md_path}")

    # Summary
    print("\n" + "=" * 60)
    summary = report.summary_by_oracle()
    if summary:
        print("[SUMMARY] By Oracle:\n")
        for oracle, tests in summary.items():
            print(f"  {oracle}:")
            for test, rate in sorted(tests.items()):
                print(f"    - {test}: {rate}")
    else:
        print("[WARN] No oracles available. Install GUDHI/Ripser/SnapPy/Sage to enable tests.")
        print("       pip install gudhi ripser")

    return 0 if report.passed_tests >= report.total_tests // 2 else 1


if __name__ == "__main__":
    sys.exit(main())
