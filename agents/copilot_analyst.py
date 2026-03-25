import json
import os
import sys
from pathlib import Path
from openai import OpenAI

def main():
    print("Running Copilot Analyst Agent...")

    # User provided Together AI key, which is OpenAI compatible
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        print("Missing TOGETHER_API_KEY environment variable. Skipping analysis.")
        return

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.together.ai/v1",
    )

    report_dir = Path("reports")
    security_json = report_dir / "security-report.json"
    triage_json = report_dir / "issue-triage-report.json"

    all_findings = []

    if security_json.exists():
        with open(security_json, "r") as f:
            all_findings.extend(json.load(f))

    if triage_json.exists():
        with open(triage_json, "r") as f:
            all_findings.extend(json.load(f))

    if not all_findings:
        print("No findings to analyze.")
        with open(report_dir / "copilot-analysis.md", "w") as f:
            f.write("# Copilot Analysis\n\nNo issues were found by the agents. The repository appears clean.")
        return

    # Prepare the prompt for the LLM
    prompt = "You are a senior security researcher and software engineer. " \
             "Analyze the following security and bug findings from our automated scanner. " \
             "Explain EXACTLY what is wrong with each finding, the potential impact, and how to fix it. " \
             "Be concise but thorough. Use Markdown format for your report.\n\n"

    for i, finding in enumerate(all_findings):
        prompt += f"Finding {i+1}:\n"
        prompt += f"File: {finding.get('file')}\n"
        prompt += f"Issue: {finding.get('issue') or finding.get('priority')}\n"
        if finding.get('pattern'):
            prompt += f"Pattern: {finding.get('pattern')}\n"
        if finding.get('task'):
            prompt += f"Task: {finding.get('task')}\n"
        if finding.get('context'):
            prompt += f"Context:\n```\n{finding.get('context')}\n```\n"
        prompt += "-" * 20 + "\n"

    print(f"Analyzing {len(all_findings)} findings with LLM...")

    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are a helpful security analyst."},
                {"role": "user", "content": prompt}
            ],
        )
        analysis = response.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        # Fallback to simulated report if API fails
        analysis = "# Copilot Analyst Report (Fallback)\n\nError calling LLM API. Please check your credentials.\n"

    with open(report_dir / "copilot-analysis.md", "w") as f:
        f.write(analysis)

    print("Copilot analysis report created.")

if __name__ == "__main__":
    main()
