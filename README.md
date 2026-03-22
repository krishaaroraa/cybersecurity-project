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

To run a full demo that sets up a "dirty" environment with sample files (Vue components, TODOs, FIXMEs, and dummy secrets) and executes the orchestrator to show its detection capabilities:

```bash
python3 run_demo.py
```

## Docker Integration

To run the agentic workflow using Docker, you can build and run the container:

```bash
docker-compose build
docker-compose up agentic-workflow
```

Or run the full demo in Docker:

```bash
docker-compose up demo-run
```

## Projects Directory

The `projects/` directory is where sample projects managed by the workflow can be stored (e.g., `projects/sample-app/`).
