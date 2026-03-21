from pathlib import Path

print("Running GitOps Agent...")

reports = Path("reports")
tests = Path("tests")

print(f"reports exists: {reports.exists()}")
print(f"tests exists: {tests.exists()}")

if not reports.exists() or not tests.exists():
    import sys

    print("[ERROR] Required directories are missing.")
    sys.exit(1)

print("GitOps actions completed")
