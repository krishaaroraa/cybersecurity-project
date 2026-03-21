import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run_agent(filename: str) -> int:
    agent_path = BASE_DIR / filename
    print(f"\n=== Running {filename} ===", flush=True)

    if not agent_path.exists():
        print(f"[ERROR] Missing file: {agent_path}", flush=True)
        return 1

    result = subprocess.run([sys.executable, str(agent_path)])
    print(f"=== Finished {filename} with code {result.returncode} ===", flush=True)
    return result.returncode


def main() -> None:
    print("Agent Flow Running", flush=True)

    agents = [
        "security_sentinel.py",
        "compliance_reporter.py",
        "issue_triage.py",
        "vue_test_generator.py",
        "gitops_agent.py",
    ]

    results = {}
    for agent in agents:
        code = run_agent(agent)
        results[agent] = "PASSED" if code == 0 else "FAILED"

    print("\n" + "=" * 30, flush=True)
    print("Execution Summary:", flush=True)
    print("=" * 30, flush=True)
    failed = False
    for agent, status in results.items():
        print(f"{agent:25} : {status}", flush=True)
        if status == "FAILED":
            failed = True
    print("=" * 30, flush=True)

    if failed:
        print("Flow failed", flush=True)
        sys.exit(1)

    print("Done", flush=True)


if __name__ == "__main__":
    main()
