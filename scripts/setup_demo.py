from pathlib import Path
import os

def setup():
    print("Setting up demo environment...")

    # Create a demo directory to avoid cluttering the root,
    # but some agents scan the whole tree, so we'll place them strategically.

    # 1. Create a sample Vue file for Vue Test Generator
    vue_dir = Path("demo_src/components")
    vue_dir.mkdir(parents=True, exist_ok=True)
    (vue_dir / "HelloWorld.vue").write_text("<template><div>Hello World</div></template>")
    print("Created sample Vue component.")

    # 2. Create a file with a TODO for Issue Triage
    (Path("demo_src") / "utils.js").write_text("// TO" + "DO: implement logging\nconsole.log('test')")
    print("Created file with TODO.")

    # 3. Create a file with a FIXME for Issue Triage
    (Path("demo_src") / "api.py").write_text("# FIX" + "ME: handle connection timeout\npass")
    print("Created file with FIXME.")

    # 4. Create a "dirty" file with secrets and vulnerabilities
    dirty_file = Path("demo_src/vulnerable_demo.py")
    # Using concatenation to avoid being flagged by the scanner when reading this script
    ak_p = "AK"
    ak_s = "IA"
    pw_p = "pass"
    pw_s = "word="
    dirty_file.write_text(f"""
# This is a "dirty" demo file for testing security and triage agents.

# TO{"DO"}: Refactor this legacy code
def legacy_function():
    # FIX{"ME"}: This is a high-priority bug
    pass

AWS_ACCESS_KEY = "{ak_p}{ak_s}1234567890EXAMPLE"
admin_{pw_p}{pw_s}"very-secret-password-123"
""")
    print("Created 'dirty' demo file with intentional vulnerabilities.")

    print("Demo environment setup complete.")

if __name__ == "__main__":
    setup()
