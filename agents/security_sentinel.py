from pathlib import Path

print("Running Security Sentinel...")

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

findings = []

for path in Path(".").rglob("*"):
    if not path.is_file():
        continue
    if any(
        part in {".git", ".github", "__pycache__", "venv", ".venv", "node_modules"}
        for part in path.parts
    ) or path.name == "security_sentinel.py":
        continue

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    # Patterns for secrets
    # We use string concatenation to avoid the script itself matching these patterns
    if (
        "SECRET_" + "KEY" in text
        or "password=" in text
        or "api_" + "key" in text
        or "ghp_" in text  # GitHub Personal Access Token
        or "AKIA" in text  # AWS Access Key ID
        or "bearer " in text.lower()
    ):
        # Additional heuristic to avoid matching the scanning script itself's pattern list
        if path.name == "security_sentinel.py":
            continue
        findings.append(str(path))

with open(report_dir / "security-report.md", "w", encoding="utf-8") as f:
    f.write("# Security Report\n\n")
    if findings:
        f.write("## Findings\n")
        for item in findings:
            f.write(f"- Potential secret pattern in `{item}`\n")
    else:
        f.write("No obvious security issues found.\n")

print("Security report created")

if findings:
    import sys

    sys.exit(1)
