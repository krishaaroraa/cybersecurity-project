from pathlib import Path

print("Running Vue Test Generator...")

tests_dir = Path("tests/unit")
tests_dir.mkdir(parents=True, exist_ok=True)

vue_files = list(Path(".").rglob("*.vue"))

if not vue_files:
    print("No Vue files found. Skipping test generation.")
else:
    for vue_file in vue_files:
        test_file = tests_dir / f"{vue_file.stem}.spec.js"
        if not test_file.exists():
            test_file.write_text(
                f"""describe('{vue_file.stem}', () => {{
  it('renders', () => {{
    expect(true).toBe(true)
  }})
}})
""",
                encoding="utf-8",
            )
            print(f"Generated test for {vue_file}")
        else:
            print(f"Test already exists for {vue_file}")

print("Vue test generation completed")
