# 🖥️ DevUI with Workflow Agents - Content Review Workflow

## Overview

This folder demonstrates the **Agent Framework DevUI** - an interactive web-based interface for developing, testing, and debugging multi-agent workflows. DevUI provides real-time visualization of workflow execution, making it easy to understand how agents interact.

| Sample | Description | Complexity |
|--------|-------------|------------|
| [1.workflow-agents-devui.py](1.workflow-agents-devui.py) | Content Review Workflow with Quality-Based Routing | Advanced |

---

## 🎯 What is DevUI?

**DevUI** (Developer UI) is a built-in web interface that allows you to:

- 🔄 **Visualize** workflow execution in real-time
- 💬 **Interact** with agents through a chat interface
- 🔍 **Debug** agent responses and routing decisions
- 📊 **Trace** the path taken through branching workflows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEVUI WEB INTERFACE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  📝 Chat Input                                                      │   │
│   │  ─────────────────────────────────────────────────────────────────  │   │
│   │  "Write a blog post about AI in healthcare"                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  🤖 Agent Responses (Real-time)                                     │   │
│   │  ─────────────────────────────────────────────────────────────────  │   │
│   │  ✅ Writer: [Content created...]                                    │   │
│   │  ✅ Reviewer: {"score": 85, "feedback": "..."}                      │   │
│   │  ✅ Publisher: [Formatted content...]                               │   │
│   │  ✅ Summarizer: [Final report...]                                   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   URL: http://localhost:8093                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### Required Packages
Install packages from requirnments.txt file

### Azure OpenAI Required ⚠️

This demo requires Azure OpenAI access with Azure AD authentication.

#### Environment Variables (.env file)

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

#### Azure CLI Authentication

```bash
az login
```

---

## 🏗️ Workflow Architecture

### Content Review Workflow with Quality Routing

This workflow demonstrates **conditional branching** based on structured outputs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONTENT REVIEW WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [User Prompt]                                                             │
│   "Write a blog post about cloud computing"                                 │
│        │                                                                    │
│        ▼                                                                    │
│   ┌──────────────────────────────────────────┐                              │
│   │           ✍️ WRITER AGENT                │                              │
│   │   Creates content based on user request  │                              │
│   └────────────────┬─────────────────────────┘                              │
│                    │                                                        │
│                    ▼                                                        │
│   ┌──────────────────────────────────────────┐                              │
│   │          🔍 REVIEWER AGENT               │                              │
│   │   Evaluates quality, returns JSON score  │                              │
│   │   { score: 85, clarity: 90, ... }        │                              │
│   └────────────────┬─────────────────────────┘                              │
│                    │                                                        │
│           ┌───────┴───────┐                                                 │
│           │  SCORE CHECK  │                                                 │
│           └───────┬───────┘                                                 │
│                   │                                                         │
│      ┌────────────┴────────────┐                                            │
│      │                         │                                            │
│   score ≥ 80              score < 80                                        │
│   (Approved)              (Needs Work)                                      │
│      │                         │                                            │
│      │                         ▼                                            │
│      │            ┌──────────────────────────────────────────┐              │
│      │            │          ✏️ EDITOR AGENT                 │              │
│      │            │   Improves content based on feedback     │              │
│      │            └────────────────┬─────────────────────────┘              │
│      │                             │                                        │
│      └─────────────┬───────────────┘                                        │
│                    │                                                        │
│                    ▼                                                        │
│   ┌──────────────────────────────────────────┐                              │
│   │          📰 PUBLISHER AGENT              │                              │
│   │   Formats content for publication        │                              │
│   └────────────────┬─────────────────────────┘                              │
│                    │                                                        │
│                    ▼                                                        │
│   ┌──────────────────────────────────────────┐                              │
│   │          📋 SUMMARIZER AGENT             │                              │
│   │   Creates final publication report       │                              │
│   └──────────────────────────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Two Paths

| Path | Condition | Route |
|------|-----------|-------|
| **Direct Approval** | Score ≥ 80 | Writer → Reviewer → Publisher → Summarizer |
| **Needs Editing** | Score < 80 | Writer → Reviewer → **Editor** → Publisher → Summarizer |

---

## 📝 Step-by-Step Code Walkthrough

### Step 1: Setup & Authentication

```python
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables
load_dotenv(override=True)

# Remove API key to force Azure AD authentication
if "AZURE_OPENAI_API_KEY" in os.environ:
    del os.environ["AZURE_OPENAI_API_KEY"]
```

### Step 2: Define Structured Output Schema

```python
from pydantic import BaseModel

class ReviewResult(BaseModel):
    """Review evaluation with scores and feedback."""
    score: int          # Overall quality score (0-100)
    feedback: str       # Concise, actionable feedback
    clarity: int        # Clarity score (0-100)
    completeness: int   # Completeness score (0-100)
    accuracy: int       # Accuracy score (0-100)
    structure: int      # Structure score (0-100)
```

This Pydantic model forces the Reviewer agent to return structured JSON.

### Step 3: Create Condition Functions

```python
def needs_editing(message: Any) -> bool:
    """Route to editor if score < 80."""
    if not isinstance(message, AgentExecutorResponse):
        return False
    try:
        review = ReviewResult.model_validate_json(message.agent_response.text)
        return review.score < 80
    except Exception:
        return False

def is_approved(message: Any) -> bool:
    """Route to publisher if score >= 80."""
    # ... similar logic, returns True if score >= 80
```

These functions determine which path the workflow takes.

### Step 4: Create Azure OpenAI Client

```python
chat_client = AzureOpenAIChatClient(
    endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    credential=DefaultAzureCredential(),
    deployment_name=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
)
```

### Step 5: Create Agents

```python
# Writer - Creates content
writer = chat_client.as_agent(
    name="Writer",
    instructions="You are an excellent content writer..."
)

# Reviewer - Evaluates with structured output
reviewer = chat_client.as_agent(
    name="Reviewer",
    instructions="Evaluate content and return JSON scores...",
    default_options={"response_format": ReviewResult}  # Forces JSON output
)

# Editor - Improves content
editor = chat_client.as_agent(
    name="Editor",
    instructions="Improve content based on feedback..."
)

# Publisher - Formats for publication
publisher = chat_client.as_agent(
    name="Publisher",
    instructions="Format content for publication..."
)

# Summarizer - Creates final report
summarizer = chat_client.as_agent(
    name="Summarizer",
    instructions="Create a final publication report..."
)
```

### Step 6: Build Workflow with Branching

```python
from agent_framework import WorkflowBuilder

workflow = (
    WorkflowBuilder(
        name="Content Review Workflow",
        description="Multi-agent content creation with quality-based routing"
    )
    .set_start_executor(writer)
    .add_edge(writer, reviewer)
    # Branch 1: High quality (>= 80) → Publisher
    .add_edge(reviewer, publisher, condition=is_approved)
    # Branch 2: Low quality (< 80) → Editor → Publisher
    .add_edge(reviewer, editor, condition=needs_editing)
    .add_edge(editor, publisher)
    # Convergence: Publisher → Summarizer
    .add_edge(publisher, summarizer)
    .build()
)
```

### Step 7: Launch DevUI

```python
from agent_framework.devui import serve

serve(entities=[workflow], port=8093, auto_open=True)
```

---

## 🚀 Running the Sample

### Run the Script

```powershell
1.workflow-agents-devui.py
```

### Expected Output

```
Starting Agent Workflow (Content Review with Quality Routing)
Available at: http://localhost:8093

This workflow demonstrates:
- Conditional routing based on structured outputs
- Path 1 (score >= 80): Reviewer → Publisher → Summarizer
- Path 2 (score < 80): Reviewer → Editor → Publisher → Summarizer
- Both paths converge at Summarizer for final report
```

The DevUI will automatically open in your browser.

---

## 💬 Sample Prompts to Try

| Prompt Type | Example | Expected Path |
|-------------|---------|---------------|
| **Comprehensive** | "Write a detailed blog post about the benefits of cloud computing with an intro, 3 main points, and conclusion" | Direct Approval (score ≥ 80) |
| **Vague/Short** | "Write about cats" | Needs Editing (score < 80) |
| **Professional** | "Write a professional article about remote work benefits" | Direct Approval |
| **Technical** | "Explain what Kubernetes is" | Depends on quality |

### Example Prompts:

**To test Direct Approval path:**
```
Write a comprehensive article about the future of artificial intelligence 
in healthcare. Include an introduction, 3 main points, and a conclusion.
```

**To test Editor path:**
```
Write something about dogs
```

---

## 🔑 Key Concepts

| Concept | Description |
|---------|-------------|
| **DevUI** | Web interface for testing and debugging workflows |
| **serve()** | Function that launches the DevUI web server |
| **Conditional Routing** | Using condition functions to determine workflow path |
| **Structured Output** | Using Pydantic models to force JSON responses |
| **Workflow Convergence** | Multiple paths merging back to a single executor |
| **response_format** | Agent option that enforces structured output |

---

## 📚 Reference Documentation

| Resource | URL |
|----------|-----|
| DevUI Samples | https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/devui |
| DevUI Documentation | https://learn.microsoft.com/en-us/agent-framework/user-guide/devui/samples |
| Workflow Branching | https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview |

---
