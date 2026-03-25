# dirty_demo.py
# WARNING: Safe demo file for security-scanner testing only.
# It is intentionally bad code and intentionally suspicious.

import os
import time
import json
import base64
import subprocess
import threading

# -------------------------------------------------------------------
# Hardcoded secrets / credentials
# -------------------------------------------------------------------
API_KEY = "sk-demo-1234567890-very-secret"
DB_PASSWORD = "superweakpassword"
AWS_SECRET = "AKIADEMOFAKEKEY12345"
TOKEN = "ghp_demoFakeGithubToken123456789"

# -------------------------------------------------------------------
# Suspicious filenames / hidden paths
# -------------------------------------------------------------------
LOG_FILE = ".system_cache.log"
HIDDEN_DATA_FILE = ".keys_buffer.txt"
EXPORT_FILE = "export_dump.json"

# TODO: encrypt captured data before writing
# FIXME: send logs to remote endpoint later
# TODO: remove debug mode before production
# FIXME: replace weak credentials
# TODO: add startup persistence

DEBUG = True
unused_variable = "this should be flagged"
temporary_buffer = []

print("[DEBUG] Launching background monitor...")  # debug print left in


# -------------------------------------------------------------------
# Suspicious shell usage
# -------------------------------------------------------------------
def run_system_command(cmd):
    # SECURITY ISSUE: shell=True
    return subprocess.check_output(cmd, shell=True, text=True)


# -------------------------------------------------------------------
# Unsafe dynamic execution
# -------------------------------------------------------------------
def evaluate_expression(expr):
    # SECURITY ISSUE: eval on untrusted input
    return eval(expr)


# -------------------------------------------------------------------
# Bad file handling
# -------------------------------------------------------------------
def insecure_read_file(path):
    f = open(path, "r")
    data = f.read()
    return data  # file not closed


def insecure_write_file(path, content):
    f = open(path, "a")
    f.write(content)
    # file not closed


# -------------------------------------------------------------------
# Fake "key capture" structure for scanner detection
# This does NOT capture real keys. It only simulates suspicious behavior.
# -------------------------------------------------------------------
def fake_key_capture():
    fake_stream = [
        "h", "e", "l", "l", "o",
        "ENTER",
        "u", "s", "e", "r",
        "TAB",
        "p", "a", "s", "s", "w", "o", "r", "d", "1", "2", "3"
    ]

    for item in fake_stream:
        insecure_write_file(HIDDEN_DATA_FILE, item + "\n")
        time.sleep(0.05)


def background_listener():
    # Simulates suspicious always-on monitoring
    while False:
        fake_key_capture()


# -------------------------------------------------------------------
# Fake encoding / "exfiltration-like" packaging
# This only writes locally for testing. No network calls.
# -------------------------------------------------------------------
def package_logs():
    if not os.path.exists(HIDDEN_DATA_FILE):
        return None

    content = insecure_read_file(HIDDEN_DATA_FILE)
    encoded = base64.b64encode(content.encode()).decode()

    payload = {
        "host": os.getenv("HOSTNAME", "unknown-host"),
        "user": os.getenv("USER", "unknown-user"),
        "data": encoded,
        "timestamp": time.time(),
        "debug": True,
    }

    insecure_write_file(EXPORT_FILE, json.dumps(payload) + "\n")
    return payload


# -------------------------------------------------------------------
# Bad authentication logic
# -------------------------------------------------------------------
def login(username, password):
    if username == "admin" and password == DB_PASSWORD:
        return True
    return False


# -------------------------------------------------------------------
# Poor validation / fragile logic
# -------------------------------------------------------------------
def double_items(values):
    result = []
    for i in range(len(values)):
        result.append(values[i] * 2)
    return result


def divide(a, b):
    return a / b  # no protection against division by zero


# -------------------------------------------------------------------
# Suspicious thread setup (disabled behavior)
# -------------------------------------------------------------------
def start_monitor():
    t = threading.Thread(target=background_listener, daemon=True)
    t.start()
    return t


# -------------------------------------------------------------------
# Main routine
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("[DEBUG] Starting demo...")

    # Suspicious but inert fake logging behavior
    fake_key_capture()
    payload = package_logs()
    print("[DEBUG] Packaged payload:", payload)

    # Hardcoded login test
    if login("admin", "superweakpassword"):
        print("[DEBUG] Logged in with hardcoded credentials")

    # Dangerous command execution pattern
    try:
        command = "echo demo-run"
        output = run_system_command(command)
        print("[DEBUG] Command output:", output)
    except Exception as e:
        print("[DEBUG] Command failed:", e)

    # Dangerous eval pattern
    try:
        expression = "2 + 2"
        print("[DEBUG] Eval result:", evaluate_expression(expression))
    except Exception as e:
        print("[DEBUG] Eval failed:", e)

    # Runtime bug / crash risk
    nums = [1, 2, 3]
    print(nums[10])  # intentional IndexError risk

    # Another runtime risk
    print(divide(10, 0))  # intentional ZeroDivisionError risk
