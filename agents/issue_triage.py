from pathlib import Path
import re

print("Running Issue Triage Agent...")

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

findings = []

# To simulate "triaging issues", we'll scan for TODO comments and FIXMEs
# across the project's Python and JavaScript files.
# Patterns use a [ ]? to avoid matching the regex definitions themselves easily.
patterns = [
    (re.compile(r"TO" + r"DO:\s*(.*)", re.IGNORECASE), "Minor"),
    (re.compile(r"FIX" + r"ME:\s*(.*)", re.IGNORECASE), "High"),
]

for path in Path(".").rglob("*"):
    if not path.is_file():
        continue
    if any(
        part in {".git", ".github", "__pycache__", "venv", ".venv", "node_modules"}
        for part in path.parts
    ) or path.name == "issue_triage.py":
        continue
    if path.suffix not in {".py", ".js", ".vue", ".yml", ".yaml"}:
        continue

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    for pattern, priority in patterns:
        for match in pattern.finditer(content):
            task = match.group(1).strip()
            # Simple heuristic to avoid matching the regex definition line itself if it somehow slips through
            if "re.compile" in task or "patterns =" in task:
                continue
            findings.append(
                {"file": str(path), "priority": priority, "task": task}
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
