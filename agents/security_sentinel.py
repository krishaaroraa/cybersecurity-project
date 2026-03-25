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
    text_lower = text.lower()
    if (
        "secret_" + "key" in text_lower
        or "password=" in text_lower
        or "api_" + "key" in text_lower
        or "ghp_" in text_lower  # GitHub Personal Access Token
        or "akia" in text_lower  # AWS Access Key ID
        or "bearer " in text_lower
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
