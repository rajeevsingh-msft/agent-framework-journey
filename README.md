# Welcome to the Agent Framework Journey! 🌟

This repository is your comprehensive guide to building, orchestrating, and deploying AI agents and workflows using the Microsoft Agent Framework. Whether you're creating simple chat agents or complex multi-agent workflows, this repository has everything you need to get started.


## 📚 Learn More

For comprehensive insights and detailed tutorials, check out my blog post series:

- **Part 1 - Agent Framework Fundamentals**: [Microsoft Agent Framework: The Open Source Engine for Agentic AI Apps](https://singhrajeev.com/2025/10/05/microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)
- **Part 2 - Workflow Deep Dive**: [Microsoft Agent Framework Workflows: The Next Step in Building Intelligent Multi-Agent AI Systems](https://singhrajeev.com/2026/01/18/microsoft-agent-framework-workflows-the-next-step-in-building-intelligent-multi-agent-ai-systems/)





---

## ✨ Highlights

- 🤖 **Multi-Agent Coordination**: Build intelligent systems with multiple agents working together.
- ⚡ **Workflow Orchestration**: Implement sequential, concurrent, and agent-integrated workflows.
- 🌐 **Azure Integration**: Leverage Azure AI Foundry for scalable and reliable AI solutions.
- 📚 **Comprehensive Documentation**: Each section includes detailed guides and examples.
- 🛠️ **Interactive DevUI**: Develop, test, and debug workflows with an intuitive interface.

---

## 🛠️ Guide to Using This Repository

This repository is designed to help you get started with building and orchestrating AI agents and workflows. Follow the steps below to make the most out of the resources provided:

### Step 1: Run the Examples

- **Agents**: Navigate to `python/1.Agents/` and try running the agent demos.
- **Workflows**: Navigate to `python/2.Workflow/` and explore the sequential and concurrent workflow examples.

### Step 2: Documentation

Each section of Agents and Workflows includes detailed documentation on how to run the code, along with explanations of the code and expected outputs. Below are two tables summarizing the available documentation for agents and workflows:

#### Agent Documentation

| Section               | Description                                      | Documentation Link                                                                 |
|-----------------------|--------------------------------------------------|-----------------------------------------------------------------------------------|
| AI Foundry Agents     | Examples of AI Foundry agents and their usage.   | [AI Foundry Agents Documentation](./python/1.Agents/1.ai-foundry-agents/README.md) |
| DevUI for Agents      | Interactive tools for developing and debugging.  | [DevUI Documentation](./python/1.Agents/2.DevUI/ReadMe.md)                         |

#### Workflow Documentation

| Section                     | Description                                              | Documentation Link                                                                 |
|-----------------------------|----------------------------------------------------------|-----------------------------------------------------------------------------------|
| Sequential Workflows        | Simple sequential workflows with step-by-step execution. | [Sequential Workflow Documentation](./python/2.Workflow/1.Getting-started/1.Sequential-workflow/Readme.md) |
| Concurrent Workflows        | Workflows with concurrent execution of tasks.            | [Concurrent Workflow Documentation](./python/2.Workflow/1.Getting-started/2.Concurrent-workflow/Readme.md) |
| Agents in Workflows         | Integrating agents into workflows.                       | [Agents in Workflow Documentation](./python/2.Workflow/1.Getting-started/3.Agents-in-Workflow/Readme.md) |
| DevUI for Workflows         | Interactive tools for workflow development.              | [DevUI Workflow Documentation](./python/2.Workflow/1.Getting-started/4.DevUI-Workflow/Readme.md) |

### Step 3: Getting Started

Follow the [Getting Started](#getting-started) section below for setup details and to run your first Agents and Workflows.


## 📋 Getting Started

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/agent-framework-journey.git
   cd agent-framework-journey
   ```

2. **Set up your environment:**
   Follow the [Setup Guidelines](#setup-guidelines) to configure your environment and dependencies.


3. **Explore the examples:**
   - Agents: `python/1.Agents/`
   - Workflows: `python/2.Workflow/`

---

## Project Structure

```
agent-framework-journey-main/
├── 📄 README.md                           # Main documentation (this file)
├── 🔒 .env                               # Environment configuration
├── 📁 documents/                          # Documentation and guides
│   ├── Microsoft Foundry-setup-guide.md  # Azure setup instructions
├── 🐍python/                            # Python implementations
│   ├── 1.Agents/                         # Agent demos and examples
│   │   ├── 1.ai-foundry-agents/          # AI Foundry agent demos
│   │   └── 2.DevUI/                      # DevUI for agent development
│   ├── 2.Workflow/                       # Workflow orchestration examples
│       ├── 1.Getting-started/            # Introductory workflows
│       │   ├── 1.Sequential-workflow/    # Simple sequential workflows
│       │   ├── 2.Concurrent-workflow/    # Concurrent execution workflows
│       │   ├── 3.Agents-in-Workflow/     # Workflows integrating agents
│       │   └── 4.DevUI-Workflow/         # Interactive DevUI for workflows
│       └── 2.Advance-samples/            # Advanced workflow patterns
```

---

## Setup Guidelines

### Step 1: Creating Virtual Environment

```bash
# Clone or navigate to the repository
cd AgentFramework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure Environment Files

1. **Create Environment Configuration**
   ```bash
   # Copy the template
   cp README.env .env
   ```

2. **Configure Azure Settings**
   - Edit the `.env` file with your Azure configuration.
   - See [Environment Setup Guide](./README.env) for detailed instructions.

3. **Verify Azure Authentication**
   ```bash
   az login
   az account show  # Verify correct subscription
   ```

### Step 4: Azure AI Foundry Project Setup

Follow the detailed setup instructions in our [Setup Guide](./documents/Microsoft%20Foundry-setup-guide.md) to:
- Create an Azure AI Foundry project
- Configure model deployments
- Get your project endpoint
- Set up authentication

---

## Quickstart

### Agents

1. **Navigate to the Agents directory:**
   ```bash
   cd python/1.Agents/1.ai-foundry-agents
   ```

2. **Run the first agent demo:**
   ```bash
   python demo1-AIFoundryAgents.py
   ```


Here’s an example of how to create and run a simple agent:

```python
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

load_dotenv()

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

**Expected Output:**
```
Why don't pirates ever get lost? Because they always have their "sea" legs!
```

---

### Workflow

1. **Navigate to the Sequential Workflow directory:**
   ```bash
   cd python/2.Workflow/1.Getting-started/1.Sequential-workflow
   ```

2. **Run the first workflow demo:**
   ```bash
   python 1.create-sequential-workflow.py
   ```

Here's the actual sequential workflow from our repository:

```python
import asyncio
from typing_extensions import Never
from agent_framework import WorkflowBuilder, WorkflowContext, WorkflowOutputEvent, Executor, executor, handler

# Custom Executor class
class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        result = text.upper()
        await ctx.send_message(result)

# Function-based executor
@executor(id="reverse_text_executor")
async def reverse_text(text: str, ctx: WorkflowContext[Never, str]) -> None:
    result = text[::-1]
    await ctx.yield_output(result)

async def main():
    upper_case = UpperCase(id="upper_case_executor")
    
    # Build the workflow
    workflow = (
        WorkflowBuilder()
        .add_edge(upper_case, reverse_text)
        .set_start_executor(upper_case)
        .build()
    )
    
    # Run the workflow
    async for event in workflow.run_stream("hello world"):
        if isinstance(event, WorkflowOutputEvent):
            print(f"Workflow completed with result: {event.data}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Expected Output:**
```
Workflow completed with result: DLROW OLLEH
```

---

## License

This project is licensed under the **MIT License**.

For the complete license text, see the [LICENSE](./LICENSE) file.

---

**Built with ❤️ using Microsoft Agent Framework and Azure AI Foundry**