from pathlib import Path
import json

print("Running Security Sentinel...")

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

findings = []

for path in Path(".").rglob("*"):
    if not path.is_file():
        continue
    if any(
        part in {".git", ".github", "__pycache__", "venv", ".venv", "node_modules", "reports", "scripts", "tests", "agents", "demo"}
        for part in path.parts
    ) or path.name in {"security_sentinel.py", "issue_triage.py", "run_demo.py", "README.md", "orchestrator_agent.py", "dirty_demo.py"}:
        continue

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    # Patterns for secrets and threats
    # We use string concatenation/fragmentation to avoid self-matches
    text_lower = text.lower()
    patterns = {
        "Secret Key": "secret_" + "key",
        "API Key": "api_" + "key",
        "Password": "password=",
        "GitHub Token": "ghp_",
        "AWS Key": "akia",
        "Bearer Token": "bearer ",
        "Keylogger": "keylogger",
        "Keyboard Listener": "keyboard_listener",
        "Hidden File Access": "/.",
        "Hidden File Logging": 'open(".',
        "Continuous Loop": "while true:",
        "Dynamic Execution (eval)": "eval(",
        "Dynamic Execution (exec)": "exec(",
        "Exfiltration": "exfiltration",
        "Suspicious Encoding": "base64.b64decode",
        "Backdoor": "backdoor",
        "Reverse Shell": "reverse_shell",
        "Generic Secret": "secret",
        "Credential": "credential",
        "Private Key": "private_" + "key",
        "Auth Token": "auth_" + "token",
        "System Command": "os.system(",
        "Subprocess Call": "subprocess.",
        "Network POST": "requests.post(",
        "Socket Connection": "socket.socket",
    }

    for label, pattern in patterns.items():
        if pattern in text_lower:
            # Extract line context for LLM/Analyst
            lines = text.splitlines()
            context = ""
            for i, line in enumerate(lines):
                if pattern in line.lower():
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = "\n".join(lines[start:end])
                    break
            findings.append({"file": str(path), "issue": label, "pattern": pattern, "context": context})

with open(report_dir / "security-report.json", "w", encoding="utf-8") as f:
    json.dump(findings, f, indent=2)

with open(report_dir / "security-report.md", "w", encoding="utf-8") as f:
    f.write("# Security Report\n\n")
    if findings:
        f.write("## Findings\n")
        f.write("| File | Issue | Detected Pattern |\n")
        f.write("| --- | --- | --- |\n")
        for item in findings:
            f.write(f"| `{item['file']}` | {item['issue']} | `{item['pattern']}` |\n")
    else:
        f.write("No obvious security issues found.\n")

print("Security report created")

if findings:
    print(f"Found {len(findings)} security issues.")
    import sys
    sys.exit(1)
