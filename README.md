# Agentic Workflow Project

This repository contains several autonomous agents that perform various tasks:

- **Security Sentinel**: Scans for potential secrets in the codebase.
- **Compliance Reporter**: Checks for the existence of required baseline files.
- **Vue Test Generator**: Generates boilerplate tests for Vue components.
- **GitOps Agent**: Validates the environment and prepares for GitOps actions.
- **Orchestrator Agent**: Manages the execution of all other agents, tracks durations, and generates a summary report.

## Recent Improvements

- **Execution Tracking**: The Orchestrator now tracks the execution time of each agent and provides a detailed summary table.
- **Robustness**: Agents now correctly exclude themselves from their own scans to avoid self-matches (e.g., Security Sentinel, Issue Triage).
- **Security Patterns**: Added common patterns for GitHub tokens and AWS keys in `security_sentinel.py`.
- **Maintainability**: Refactored `compliance_reporter.py` to use a configurable `REQUIRED_FILES` list.

## Usage

To run the full agent flow on the current repository:

```bash
python3 agents/orchestrator_agent.py
```

## Demo

To run a full demo that sets up a temporary environment with sample files (Vue components, TODOs, FIXMEs) and executes the orchestrator:

```bash
python3 run_demo.py
```
