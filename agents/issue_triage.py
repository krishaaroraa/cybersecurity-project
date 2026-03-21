from pathlib import Path
import re

print("Running Issue Triage Agent...")

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

findings = []

# To simulate "triaging issues", we'll scan for TODO comments and FIXMEs
# across the project's Python and JavaScript files.
patterns = [
    (re.compile(r"TODO:\s*(.*)", re.IGNORECASE), "Minor"),
    (re.compile(r"FIXME:\s*(.*)", re.IGNORECASE), "High"),
]

for path in Path(".").rglob("*"):
    if not path.is_file():
        continue
    if any(
        part in {".git", ".github", "__pycache__", "venv", ".venv", "node_modules"}
        for part in path.parts
    ):
        continue
    if path.suffix not in {".py", ".js", ".vue", ".yml", ".yaml"}:
        continue

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    for pattern, priority in patterns:
        for match in pattern.finditer(content):
            findings.append(
                {"file": str(path), "priority": priority, "task": match.group(1).strip()}
            )

with open(report_dir / "issue-triage-report.md", "w", encoding="utf-8") as f:
    f.write("# Issue Triage Report\n\n")
    if findings:
        f.write("## Identified Tasks\n")
        f.write("| File | Priority | Task |\n")
        f.write("| --- | --- | --- |\n")
        for item in findings:
            f.write(f"| `{item['file']}` | {item['priority']} | {item['task']} |\n")
    else:
        f.write("No outstanding TODOs or FIXMEs found. Repository is clean!\n")

print(f"Issue triage report created with {len(findings)} findings")
