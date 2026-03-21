from pathlib import Path

print("Running Compliance Reporter...")

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

required = [
    "README.md",
    ".github/workflows/agent-flow.yml",
    "agents/orchestrator_agent.py",
    "LICENSE",
    ".gitignore",
]

missing = [item for item in required if not Path(item).exists()]

with open(report_dir / "compliance-report.md", "w", encoding="utf-8") as f:
    f.write("# Compliance Report\n\n")
    if missing:
        f.write("## Missing Files\n")
        for item in missing:
            f.write(f"- `{item}`\n")
    else:
        f.write("All required baseline files are present.\n")

print("Compliance report created")

if missing:
    import sys

    sys.exit(1)
