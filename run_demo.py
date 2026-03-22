import subprocess
import sys
import shutil
from pathlib import Path

def run_demo():
    print("=== Starting Demo Workflow ===")

    # 1. Setup the demo environment
    print("\n--- Step 1: Setting up demo environment ---")
    setup_result = subprocess.run([sys.executable, "scripts/setup_demo.py"])
    if setup_result.returncode != 0:
        print("[ERROR] Setup failed.")
        sys.exit(1)

    # 2. Run the Orchestrator
    print("\n--- Step 2: Running Orchestrator Agent ---")
    print("(Note: Orchestrator will exit with non-zero if agents find issues)")
    orch_result = subprocess.run([sys.executable, "agents/orchestrator_agent.py"])

    if orch_result.returncode != 0:
        print("\n[INFO] Orchestrator correctly reported agent findings as failures.")
    else:
        print("\n[WARNING] Orchestrator did not report any findings as failures.")

    # 3. Verify reports
    print("\n--- Step 3: Verifying and displaying agent findings ---")
    reports_dir = Path("reports")
    expected_reports = [
        "security-report.md",
        "compliance-report.md",
        "issue-triage-report.md"
    ]

    for report in expected_reports:
        report_path = reports_dir / report
        if report_path.exists():
            print(f"\n[OK] Findings from {report}:")
            with open(report_path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print(f"[MISSING] Report not found: {report}")

    # 4. Cleanup
    print("\n--- Step 4: Cleaning up demo environment ---")
    demo_src = Path("demo_src")
    if demo_src.exists():
        shutil.rmtree(demo_src)

    # Also clean up generated tests for demo files
    demo_tests = Path("tests/unit/HelloWorld.spec.js")
    if demo_tests.exists():
        demo_tests.unlink()

    print("\n=== Demo Workflow Completed ===")

if __name__ == "__main__":
    run_demo()
