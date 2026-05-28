# Advanced Workflow Samples

## Overview

This folder contains **advanced workflow samples** for the Microsoft Agent Framework, showcasing sophisticated patterns beyond the getting-started examples. These samples demonstrate real-world patterns including conditional branching logic and agent handoff between workflows.

| Sample | Description | Complexity |
|--------|-------------|------------|
| [4.workflow-with-branching-logic.py](4.workflow-with-branching-logic.py) | Workflow with conditional branching — routes execution based on runtime decisions | Advanced |
| [5.workflow-handoff.py](5.workflow-handoff.py) | Agent handoff pattern — transfers control between agents within a workflow | Advanced |

---

## Prerequisites

### Required Packages

Install all dependencies from the root `requirements.txt` file:

```bash
pip install -r ../../../requirements.txt
```

### Python Version
- Python 3.10 or later

### Azure AI Foundry Setup
These samples integrate AI agents and require Azure AI Foundry credentials. See the [Setup Guide](../../../documents/Microsoft%20Foundry-setup-guide.md) for configuration details.

---

## 🔀 Sample 4: Workflow with Branching Logic

### File: `4.workflow-with-branching-logic.py`

**Purpose**: Demonstrates conditional branching within a workflow, where the execution path is determined at runtime based on the output of an executor or agent.

**Key Concepts:**
- Conditional edge routing between executors
- Dynamic decision-making within a workflow
- Multiple execution paths in a single workflow

**Use Cases:**
- Content moderation pipelines with approve/reject paths
- Multi-step data processing with error handling branches
- Agent responses that route to different follow-up actions

---

## 🤝 Sample 5: Workflow Handoff

### File: `5.workflow-handoff.py`

**Purpose**: Demonstrates the agent handoff pattern, where one agent transfers control to another agent within a workflow for specialized task handling.

**Key Concepts:**
- Agent-to-agent handoff within workflows
- Specialized agent delegation
- Seamless context passing between agents

**Use Cases:**
- Customer support escalation (general → specialist agent)
- Multi-domain Q&A (routing to domain-specific agents)
- Task decomposition with specialized sub-agents

---

## 📚 How to Run

```bash
# Navigate to this directory
cd python/2.Workflow/2.Advance-samples

# Run a sample
python 4.workflow-with-branching-logic.py
python 5.workflow-handoff.py
```

---

## 📚 Resources

- [Getting Started Workflows](../1.Getting-started/Workflow-Readme.md)
- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Part 2 Blog Post: Workflows Deep Dive](https://singhrajeev.com/2026/01/18/microsoft-agent-framework-workflows-the-next-step-in-building-intelligent-multi-agent-ai-systems/)

---

**Built with ❤️ using Microsoft Agent Framework**
