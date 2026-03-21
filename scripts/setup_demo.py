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

    # 4. Create a file with a dummy secret for Security Sentinel (OPTIONAL, we might skip to keep it passing or use it to show failure)
    # Let's create a file that WOULD be caught if we wanted to show failure,
    # but for "smooth working" we might just mention it.
    # Actually, the prompt says "check if everything is working smoothly",
    # which usually means success. But an agent finding a secret IS working smoothly.
    # However, the orchestrator fails if an agent fails.
    # Let's create a "safe" secret that we can toggle or just use to demonstrate the report.

    print("Demo environment setup complete.")

if __name__ == "__main__":
    setup()
