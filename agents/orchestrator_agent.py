import subprocess
import sys
import time
from pathlib import Path
from typing import Tuple


BASE_DIR = Path(__file__).resolve().parent


def run_agent(filename: str) -> Tuple[int, float]:
    agent_path = BASE_DIR / filename
    print(f"\n=== Running {filename} ===", flush=True)

    if not agent_path.exists():
        print(f"[ERROR] Missing file: {agent_path}", flush=True)
        return 1, 0.0

    start_time = time.perf_counter()
    result = subprocess.run([sys.executable, str(agent_path)])
    duration = time.perf_counter() - start_time

    print(f"=== Finished {filename} in {duration:.2f}s with code {result.returncode} ===", flush=True)
    return result.returncode, duration


def main() -> None:
    print("Agent Flow Running", flush=True)

    agents = [
        "security_sentinel.py",
        "compliance_reporter.py",
        "issue_triage.py",
        "vue_test_generator.py",
        "gitops_agent.py",
    ]

    results = []
    total_start = time.perf_counter()
    for agent in agents:
        code, duration = run_agent(agent)
        status = "PASSED" if code == 0 else "FAILED"
        results.append({"agent": agent, "status": status, "duration": duration})

    total_duration = time.perf_counter() - total_start

    print("\n" + "=" * 60, flush=True)
    print(f"{'Agent':<25} | {'Status':<10} | {'Duration (s)':<12}", flush=True)
    print("-" * 60, flush=True)
    failed = False
    for res in results:
        print(f"{res['agent']:<25} | {res['status']:<10} | {res['duration']:>12.2f}", flush=True)
        if res['status'] == "FAILED":
            failed = True
    print("-" * 60, flush=True)
    print(f"{'Total':<25} | {'':<10} | {total_duration:>12.2f}", flush=True)
    print("=" * 60, flush=True)

    # Run the analyst last
    analyst_code, analyst_duration = run_agent("copilot_analyst.py")
    results.append({"agent": "copilot_analyst.py", "status": "PASSED" if analyst_code == 0 else "FAILED", "duration": analyst_duration})

    if failed:
        print("Flow failed", flush=True)
        sys.exit(1)

    print("Done", flush=True)


if __name__ == "__main__":
    main()
