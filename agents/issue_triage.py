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
    (re.compile(r"BUG:\s*(.*)", re.IGNORECASE), "High"),
    (re.compile(r"exfiltration", re.IGNORECASE), "High"),
]

for path in Path(".").rglob("*"):
    if not path.is_file():
        continue
    if any(
        part in {".git", ".github", "__pycache__", "venv", ".venv", "node_modules", "agents"}
        for part in path.parts
    ) or path.name in {"issue_triage.py", "security_sentinel.py"}:
        continue
    if path.suffix not in {".py", ".js", ".vue", ".yml", ".yaml"}:
        continue

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    for pattern, priority in patterns:
        for match in pattern.finditer(content):
            try:
                task = match.group(1).strip()
            except IndexError:
                task = match.group(0).strip()

            # Simple heuristic to avoid matching the regex definition line itself if it somehow slips through
            if "re.compile" in task or "patterns =" in task:
                continue
            # Extract line context for LLM/Analyst
            lines = content.splitlines()
            context = ""
            for i, line in enumerate(lines):
                if task in line or match.group(0) in line:
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = "\n".join(lines[start:end])
                    break
            findings.append(
                {"file": str(path), "priority": priority, "task": task, "context": context}
            )

import json
with open(report_dir / "issue-triage-report.json", "w", encoding="utf-8") as f:
    json.dump(findings, f, indent=2)

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

# If any "High" priority findings are found, exit with error code
if any(item["priority"] == "High" for item in findings):
    print(f"Found {len([f for f in findings if f['priority'] == 'High'])} high-priority issues.")
    import sys
    sys.exit(1)
