# suspicious_logger.py (SAFE DEMO — does NOT log real keys)

import time

LOG_FILE = ".hidden_log.txt"

def fake_key_capture():
    # Simulated keystrokes (not real user input)
    fake_keys = ["a", "b", "c", "ENTER", "password123"]

    with open(LOG_FILE, "a") as f:
        for key in fake_keys:
            f.write(key + "\n")
            time.sleep(0.5)

def run_background():
    # Simulating suspicious continuous monitoring
    while True:
        fake_key_capture()

if __name__ == "__main__":
    print("Starting background process...")
    run_background()


