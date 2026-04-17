# Microsoft Agent Framework - Workflows

## Overview

Hands-on examples demonstrating **Microsoft Agent Framework Workflows** - orchestrating AI agent operations through sequential, concurrent, and branching execution patterns.

---

## 📁 Folder Structure

```
2.Workflow/
└── 1.Getting-started/
    ├── 📁 1.Sequential-workflow/     → Linear step-by-step execution
    ├── 📁 2.Concurrent-workflow/     → Parallel fan-out/fan-in execution  
    ├── 📁 3.Agents-in-Workflow/      → AI Agents within workflows 
    ├── 📁 4.DevUI-Workflow/          → Interactive DevUI for workflows
```

Each folder contains its own **Readme.md** with detailed documentation.

---

## 🛠️ Quick Setup

```bash
# Install required packages from the root folder
pip install -r requirements.txt

# Optional: For workflow visualization as images (SVG/PNG)
pip install graphviz
# + Install Graphviz binaries from https://graphviz.org/download/
```

---

## 🚀 How to Run

Navigate to the folder and run the Python file:

```bash
cd <folder>
python <file.py>
```

### 📋 Sample Files

| Folder | File | Description | Docs |
|--------|------|-------------|------|
| **1.Sequential-workflow/** | [`1.create-sequential-workflow.py`](./1.Sequential-workflow/1.create-sequential-workflow.py) | Basic sequential flow: UpperCase → ReverseText | [📖 Readme](./1.Sequential-workflow/Readme.md) |
| | [`1b-class-based-executor.py`](./1.Sequential-workflow/1b-class-based-executor.py) | Sequential workflow using class-based executors | |
| | [`1c-function-based-executor.py`](./1.Sequential-workflow/1c-function-based-executor.py) | Sequential workflow using function-based executors | |
| | [`2.realworld-sequential-workflow.py`](./1.Sequential-workflow/2.realworld-sequential-workflow.py) | Real-world example: Customer email processing pipeline | |
| **2.Concurrent-workflow/** | [`2.create-concurrent-workflow.py`](./2.Concurrent-workflow/2.create-concurrent-workflow.py) | Basic concurrent flow: fan-out to Average & Sum, fan-in | [📖 Readme](./2.Concurrent-workflow/Readme.md) |
| | [`2a-realworld-concurrent-workflow.py`](./2.Concurrent-workflow/2a-realworld-concurrent-workflow.py) | Real-world example: Price comparison engine with parallel API calls | |
| **3.Agents-in-Workflow/** | [`3.agents-in-workflow.py`](./3.Agents-in-Workflow/3.agents-in-workflow.py) | AI Agents orchestrated within workflows | [📖 Readme](./3.Agents-in-Workflow/Readme.md) |
| **4.DevUI-Workflow/** | [`1.workflow-agents-devui.py`](./4.DevUI-Workflow/1.workflow-agents-devui.py) | Content Review Workflow with Quality-Based Routing | [📖 Readme](./4.DevUI-Workflow/Readme.md) |

📖 See each folder's **Readme.md** for detailed documentation.

---

## 📚 Resources

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Mermaid Live Editor](https://mermaid.live) - Visualize diagrams online

---

**Built with ❤️ using Microsoft Agent Framework**
