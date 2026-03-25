import json
import os
import sys
from pathlib import Path
from openai import OpenAI

class AgenticArchitect:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.together.ai/v1",
        )
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)
        self.findings = []
        self.repo_map = {}

    def map_repository(self):
        print("Mapping repository structure...")
        for path in Path(".").rglob("*"):
            if not path.is_file():
                continue
            if any(part in {".git", ".github", "__pycache__", "venv", ".venv", "node_modules", "reports", "agents"} for part in path.parts):
                continue
            self.repo_map[str(path)] = path.stat().st_size

    def select_relevant_files(self):
        # Intelligent selection based on size and extension
        return [f for f in self.repo_map.keys() if f.endswith(('.py', '.js', '.vue', '.yml', '.yaml'))]

    def intelligent_chunk(self, content, max_lines=100, overlap=10):
        lines = content.splitlines()
        chunks = []
        for i in range(0, len(lines), max_lines - overlap):
            chunk = "\n".join(lines[i:i + max_lines])
            chunks.append(chunk)
            if i + max_lines >= len(lines):
                break
        return chunks

    def phase_project_understanding(self):
        print("Phase 0: Project Understanding...")
        self.map_repository()
        readme = ""
        if Path("README.md").exists():
            readme = Path("README.md").read_text()[:2000]

        tree = "\n".join(list(self.repo_map.keys())[:100])
        prompt = f"Given this repository structure and README, identify the most CRITICAL files for security and bug analysis.\nREADME:\n{readme}\nFILES:\n{tree}\nOutput a comma-separated list of filenames."
        try:
            response = self.client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[{"role": "user", "content": prompt}],
            )
            return [f.strip() for f in response.choices[0].message.content.split(",")]
        except:
            return []

    def phase_contextual_discovery(self):
        print("Phase 1: Contextual Discovery & Selection...")
        critical_files = self.phase_project_understanding()
        changed_files = os.environ.get("CHANGED_FILES", "").split(",")
        all_relevant = list(set([f for f in critical_files + changed_files if f in self.repo_map]))

        if not all_relevant:
            all_relevant = self.select_relevant_files()

        return all_relevant

    def phase_selection_deep_dive(self, files):
        print(f"Phase 2: Selection & Deep Dive on {len(files)} files...")
        findings = []
        for file_path in files:
            content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
            chunks = self.intelligent_chunk(content)
            for i, chunk in enumerate(chunks):
                print(f"  Analyzing `{file_path}` (chunk {i+1}/{len(chunks)})...")
                prompt = f"""You are an Agentic Security Architect performing a DEEP DIVE.
Analyze this code chunk for security threats, bugs, or architectural flaws.
File: `{file_path}`
Context: Chunk {i+1} of {len(chunks)}

Content:
```
{chunk}
```
If you find an issue, explain your logic and provide a structured JSON response:
{{
  "file": "{file_path}",
  "issue": "Specific threat/bug",
  "reasoning": "Step-by-step logic detailing the flow and impact",
  "fix": "Specific code snippet to resolve the issue",
  "priority": "High/Minor"
}}
If no issues are found, respond with 'NONE'."""
                try:
                    response = self.client.chat.completions.create(
                        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    analysis = response.choices[0].message.content
                    if "{" in analysis:
                        try:
                            json_str = analysis[analysis.find("{"):analysis.rfind("}")+1]
                            finding = json.loads(json_str)
                            findings.append(finding)
                        except json.JSONDecodeError:
                            print(f"  Warning: Failed to parse JSON from analysis in `{file_path}`")
                except Exception as e:
                    print(f"  Error in deep dive: {e}")
        return findings

    def phase_fix_synthesis(self, findings):
        print("Phase 3: Fix Synthesis & Verification...")
        # Reason across findings to ensure fixes are consistent
        synthesized = []
        for fnd in findings:
            prompt = f"""Review this proposed fix for a {fnd.get('issue')} in `{fnd.get('file')}`.
Reasoning: {fnd.get('reasoning')}
Proposed Fix: {fnd.get('fix')}

Is this fix complete and secure? If yes, output 'APPROVED'. If no, output 'FIX:' followed by the improved code."""
            try:
                response = self.client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=[{"role": "user", "content": prompt}],
                )
                if "APPROVED" in response.choices[0].message.content.upper():
                    synthesized.append(fnd)
                elif "FIX:" in response.choices[0].message.content:
                    fnd['fix'] = response.choices[0].message.content.split("FIX:")[1].strip()
                    synthesized.append(fnd)
            except:
                synthesized.append(fnd)
        return synthesized

    def run(self):
        relevant_files = self.phase_contextual_discovery()
        initial_findings = self.phase_selection_deep_dive(relevant_files)
        self.findings = self.phase_fix_synthesis(initial_findings)
        self.generate_reports()

    def generate_reports(self):
        with open(self.report_dir / "agentic-architect-findings.json", "w") as f:
            json.dump(self.findings, f, indent=2)

        with open(self.report_dir / "agentic-architect-report.md", "w") as f:
            f.write("# Agentic Architect Analysis Report\n\n")
            if not self.findings:
                f.write("No issues detected across the repository.")
            else:
                for i, fnd in enumerate(self.findings):
                    f.write(f"## Finding {i+1}: {fnd.get('issue')}\n")
                    f.write(f"**File:** `{fnd.get('file')}`\n")
                    f.write(f"**Priority:** {fnd.get('priority')}\n")
                    f.write(f"### Reasoning:\n{fnd.get('reasoning')}\n")
                    f.write(f"### Proposed Fix:\n```python\n{fnd.get('fix')}\n```\n\n---\n")

        print(f"Architect reports generated with {len(self.findings)} findings.")

if __name__ == "__main__":
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        print("Missing TOGETHER_API_KEY environment variable. Skipping Agentic Architect.")
        sys.exit(0)
    architect = AgenticArchitect(api_key)
    architect.run()
