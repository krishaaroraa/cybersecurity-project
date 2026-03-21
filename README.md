# Agentic Workflow Project

This repository contains several autonomous agents that perform various tasks:

- **Security Sentinel**: Scans for potential secrets in the codebase.
- **Compliance Reporter**: Checks for the existence of required baseline files.
- **Vue Test Generator**: Generates boilerplate tests for Vue components.
- **GitOps Agent**: Validates the environment and prepares for GitOps actions.
- **Orchestrator Agent**: Manages the execution of all other agents.

## Usage

To run the full agent flow, execute:

```bash
python3 agents/orchestrator_agent.py
```
