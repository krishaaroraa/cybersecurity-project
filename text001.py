# dirty.py

import os
import sys
import subprocess

# HARDCODED SECRET (security issue)
API_KEY = "sk-1234567890-SECRET-KEY"
PASSWORD = "admin123"

# TODO: remove debug prints before production
print("Starting application...")

# UNUSED VARIABLE
unused_var = 42

def run_command(cmd):
    # SECURITY RISK: shell=True (command injection)
    return subprocess.check_output(cmd, shell=True)

def insecure_eval(user_input):
    # VERY BAD: arbitrary code execution
    return eval(user_input)

def read_file(filename):
    # NO ERROR HANDLING
    f = open(filename, "r")
    data = f.read()
    return data  # file not closed

def write_file(filename, content):
    # NO CONTEXT MANAGER
    f = open(filename, "w")
    f.write(content)

def login(user, password):
    # HARDCODED AUTH CHECK
    if user == "admin" and password == PASSWORD:
        return True
    return False

def process_data(data):
    # BAD STYLE + NO VALIDATION
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result

# DEBUG CODE LEFT IN
if __name__ == "__main__":
    user_input = input("Enter command: ")
    
    # POTENTIAL INJECTION
    output = run_command(user_input)
    print("Command output:", output)

    # UNSAFE EVAL
    expr = input("Enter expression: ")
    print("Eval result:", insecure_eval(expr))

    # FILE READ WITHOUT CHECK
    content = read_file("sample.txt")
    print("File content:", content)

    # HARDCODED LOGIN TEST
    if login("admin", "admin123"):
        print("Logged in!")

    # RANDOM CRASH POSSIBILITY
    numbers = [1, 2, 3]
    print(numbers[5])  # IndexError

# FIXME: handle exceptions properly
# FIXME: remove hardcoded credentials
# FIXME: sanitize user input
# FIXME: add logging instead of print
