# Microsoft Agent Framework: Preview to GA (v1.0) Migration Guide

> **Microsoft Agent Framework Version 1.0 GA Released**: April 3, 2026  
> **Migration Guide Updated**: April 17, 2026

## Overview

Microsoft Agent Framework has reached **General Availability (GA) with Version 1.0**, bringing production-ready stability, long-term support commitments, and enterprise-grade features. This guide helps you migrate from Preview versions to the stable GA release.

## 📋 Table of Contents

- [1. What's NEW in Version 1.0 (GA)](#1-whats-new-in-version-10-ga)
  - [1.1 Production-Ready Core Features (Stable)](#11-production-ready-core-features-stable)
  - [1.2 Preview Features (APIs May Evolve)](#12-preview-features-apis-may-evolve)
  - [1.3 New GA Capabilities Summary](#13-new-ga-capabilities-summary)
- [2. Side-by-Side Migration Analysis: Preview → GA](#2-side-by-side-migration-analysis-preview--ga)
  - [2.1 Requirements & Dependencies Changes](#21-requirements--dependencies-changes)
  - [2.2 Code Pattern Enhancements](#22-code-pattern-enhancements)
  - [2.3 Import Statement Updates](#23-import-statement-updates)
  - [2.4 API Stability Changes](#24-api-stability-changes)
- [3. Step-by-Step Migration Guide](#3-step-by-step-migration-guide)
  - [3.1 Files & Directories You'll Update](#31-files--directories-youll-update)
  - [3.2 Step 1: Update Dependencies](#32-step-1-update-dependencies)
  - [3.3 Step 2: Update Import Statements](#33-step-2-update-import-statements-required-for-ga)
  - [3.4 Step 3: Code Migration](#34-step-3-code-migration-breaking-changes-required)
  - [3.5 Step 4: Testing Migration](#35-step-4-testing-migration)
- [4. Migration Checklist](#4-migration-checklist)
- [5. Additional Resources](#5-additional-resources)
  - [5.1 Official Microsoft Documentation](#51-official-microsoft-documentation)
  - [5.2 Migration Support](#52-migration-support)

---

## 1. What's NEW in Version 1.0 (GA)

### 1.1 Production-Ready Core Features (Stable)

| Feature | Status | Description |
|---------|--------|-------------|
| **Single Agent & Service Connectors** | ✅ **Stable** | Production-ready agents with connectors for Foundry, Azure OpenAI, OpenAI, Anthropic, Bedrock, Gemini, Ollama |
| **Middleware Hooks** | ✅ **Stable** | Intercept, transform, and extend agent behavior with content safety, logging, compliance |
| **Agent Memory & Context** | ✅ **Stable** | Pluggable memory architecture with Foundry, Mem0, Redis, Neo4j support |
| **Agent Workflows** | ✅ **Stable** | Graph-based workflow engine with checkpointing and hydration |
| **Multi-Agent Orchestration** | ✅ **Stable** | Sequential, concurrent, handoff, group chat patterns with streaming support |
| **Declarative YAML** | ✅ **Stable** | Define agents and workflows in version-controlled YAML files |
| **A2A & MCP Support** | ✅ **Stable** | Cross-runtime agent collaboration and Model Context Protocol |
| **Migration Assistants** | ✅ **Stable** | Automated migration from Semantic Kernel and AutoGen |

### 1.2 Preview Features (APIs May Evolve)

| Feature | Status | Description |
|---------|--------|-------------|
| **DevUI** | 🔄 **Preview** | Browser-based debugger for real-time agent visualization |
| **Foundry Hosted Agents** | 🔄 **Preview** | Run agents as managed services on Foundry/Azure Functions |
| **Foundry Integration Suite** | 🔄 **Preview** | Tools, memory, observability, evaluations deep integration |
| **AG-UI/CopilotKit/ChatKit** | 🔄 **Preview** | Frontend streaming adapters with human-in-the-loop |
| **Skills System** | 🔄 **Preview** | Reusable domain capability packages |
| **GitHub Copilot SDK** | 🔄 **Preview** | Use GitHub Copilot as an agent harness |
| **Claude Code SDK** | 🔄 **Preview** | Claude Code integration for coding agents |
| **Agent Harness** | 🔄 **Preview** | Local runtime with shell, file system access |

### 1.3 New GA Capabilities Summary

| **🆕 Feature** | **Description** | **Implementation** |
|---------|-------------|----------------|
| **🆕 Middleware Pipeline** | Enterprise compliance, logging, monitoring | `agent = Agent(middleware=[...], ...)` |
| **🆕 Named Agents** | Better tracking and debugging | `agent = Agent(name="CustomerService", ...)` |  
| **🆕 Enhanced Clients** | Better Foundry integration | `FoundryChatClient(project_endpoint="...", model="...")` |
| **🆕 Declarative Config** | YAML-based agent definitions | Load agents from `agents.yaml` files |

---

## 2. Side-by-Side Migration Analysis: Preview → GA

### 2.1 Requirements & Dependencies Changes

| Component | **Current (Preview)** | **Recommended (GA)** | **Why This Change Is Needed** |
|-----------|---------------------|---------------------|--------------------------------|
| **Core Framework** | `agent-framework` | `agent-framework>=1.0.0,<2.0.0` | ✅ **Production stability** - Pin to GA version range for predictable behavior and long-term support |
| **Azure Integration** | `agent-framework-azure-ai` | `agent-framework-azure-ai==1.0.0rc6` | ⚠️ **GA pending** - Using latest RC until stable GA available (see [Error Guide](README-AgentFramework-Upgrade-Error-and-Solution.md)) |
| **DevUI (Debug)** | `agent-framework-devui --pre` | `agent-framework-devui --pre # Keep preview` | ⚠️ **Still evolving** - DevUI APIs may change, keep as preview until stable |
| **Visualization** | `agent-framework[viz] --pre` | `agent-framework[viz] --pre # Keep preview` | ⚠️ **Feature preview** - Workflow visualization still in active development |
| **Version Strategy** | No version pinning | Semantic versioning with ranges | 🔒 **Deployment safety** - Prevent accidental breaking changes in production |

### 2.2 Code Pattern Enhancements

| Pattern | **Current (Preview)** | **Recommended (GA)** | **Why This Change Is Needed** |
|---------|---------------------|---------------------|--------------------------------|
| **Foundry Client** | `from agent_framework.azure import AzureAIAgentClient` | `from agent_framework.foundry import FoundryChatClient` | 🚀 **Enhanced features** - New Foundry client has better integration with managed services |
| **Agent Creation** | Basic agent instantiation | Enhanced with middleware support | 🛡️ **Enterprise compliance** - Middleware hooks for logging, monitoring, security |
| **Error Handling** | Basic try/catch patterns | Structured error handling with retries | 🔄 **Production resilience** - Better handling of transient failures |
| **Configuration** | Manual environment setup | Declarative YAML configuration | 📋 **Infrastructure as Code** - Version-controlled agent definitions |

### 2.3 Import Statement Updates

| Current Import | Recommended Import | Benefits |
|----------------|-------------------|----------|
| `from agent_framework.azure import AzureAIAgentClient` | `from agent_framework.foundry import FoundryChatClient` | Better managed service integration |
| Manual client configuration | `from agent_framework.foundry import FoundryChatClient` | Simplified authentication with Azure CLI |
| Basic workflow patterns | Enhanced orchestration imports | Access to new stable orchestration patterns |

### 2.4 API Stability Changes

| API Surface | Preview Status | GA Status | Migration Impact |
|-------------|----------------|-----------|------------------|
| **Agent Creation** | Frequent changes | ✅ **Locked & Stable** | ✅ **No changes needed** |
| **Workflow Builder** | API refinements | ✅ **Locked & Stable** | ✅ **No changes needed** |
| **Service Connectors** | Breaking changes possible | ✅ **Backward Compatible** | ✅ **No changes needed** |
| **DevUI APIs** | Experimental | ⚠️ **Still evolving** | ⚠️ **May need updates** |
| **Foundry Integration** | Limited features | 🎯 **Expanded & Stable** | 🔄 **Review & enhance** |

---

## 3. Step-by-Step Migration Guide

> **⚠️ IMPORTANT NOTE (April 2026)**: While the core `agent-framework` has GA release 1.0.x, the **`agent-framework-azure-ai` package only has Release Candidate versions** (1.0.0rc6 is latest). Use `==1.0.0rc6` until GA is available. See our [**Error Resolution Guide**](README-AgentFramework-Upgrade-Error-and-Solution.md) for details.

### 3.1 Files & Directories You'll Update

This migration affects these specific files in your project:

#### **Core Configuration Files:**
- 📄 [`requirements.txt`](requirements.txt) - Update package versions
- 📄 [`README.md`](README.md) - Update documentation 
- 📄 [`.env`](README.env) - Environment variables (if using GA features)

#### **Python Code Files:**
- 📁 [`python/1.Agents/1.ai-foundry-agents/`](python/1.Agents/1.ai-foundry-agents/) - Agent examples
  - 📄 [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) - Basic agent (GA compatible)
  - 📄 [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) - Multi-agent scenarios (GA compatible)
  - 📄 [`agent-sk.py`](python/1.Agents/1.ai-foundry-agents/agent-sk.py) - Semantic Kernel comparison example
- 📁 [`python/1.Agents/2.DevUI/`](python/1.Agents/2.DevUI/) - DevUI examples (stays Preview)
- 📁 [`python/2.Workflow/`](python/2.Workflow/) - Workflow examples 
  - 📁 [`1.Getting-started/`](python/2.Workflow/1.Getting-started/) - Basic workflows
  - 📁 [`2.Advance-samples/`](python/2.Workflow/2.Advance-samples/) - Advanced patterns

#### **Your Custom Files:**
- 📄 **Your existing agent files** - Minimal/no changes needed (backward compatible)
- 📄 **Your workflow files** - Should work unchanged
- 📄 **Your custom requirements.txt** - Update versions as shown below

#### **Quick Reference: File Changes**

| File Category | Action Required | Specific Files |
|---------------|----------------|----------------|
| **📦 Dependencies** | ⚠️ **MUST Update** | [`requirements.txt`](requirements.txt) |
| **🔧 Basic Agents** | ⚠️ **MUST Update** | [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py), [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) |
| **🚀 GA Enhanced** | ⚠️ **Required Updates** | Use [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) as reference |
| **🔬 DevUI** | ✅ **No Changes Needed** | [`python/1.Agents/2.DevUI/`](python/1.Agents/2.DevUI/) files |
| **⚙️ Workflows** | ✅ **No Changes Needed** | All files in [`python/2.Workflow/`](python/2.Workflow/) |

### 3.2 Step 1: Update Dependencies

**📁 Files to Update:**
- 📄 [`requirements.txt`](requirements.txt) (Root level)

<table>
<tr>
<th>📦 Current Preview Setup</th>
<th>🚀 Updated GA Setup</th>
</tr>
<tr>
<td>

```txt
python-dotenv
azure-identity
agent-framework                     # ← Needs version pinning
agent-framework-azure-ai           # ← Needs version pinning
agent-framework-devui --pre        # ← Stays preview
typing_extensions
agent-framework[viz] --pre         # ← Stays preview
```

</td>
<td>

```txt
# Microsoft Agent Framework - GA Production Requirements
python-dotenv
azure-identity

# Agent Framework GA (Production Ready - Stable APIs)
agent-framework>=1.0.0,<2.0.0                    # 🆕 GA stable with semver
agent-framework-azure-ai==1.0.0rc6               # ⚠️ Latest RC (GA pending)

# Preview features (Keep as preview - APIs may evolve)
agent-framework-devui --pre                       # DevUI debugging interface
agent-framework[viz] --pre                        # Workflow visualization

# Supporting libraries  
typing_extensions                                  # Type hints support
```

</td>
</tr>
</table>

### 3.3 Step 2: Update Import Statements (Required for GA)

**📁 Files to Update:**
- 📄 [`python\1.Agents\1.ai-foundry-agents\demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) *(Updated for GA)*
- 📄 [`python\1.Agents\1.ai-foundry-agents\demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) *(Updated for GA)*
- 📄 Any custom agent files in [`python\1.Agents\`](python/1.Agents/) and [`python\2.Workflow\`](python/2.Workflow/)

<table>
<tr>
<th>📖 Preview Version (Deprecated)</th>
<th>✅ GA Version (Required)</th>
</tr>
<tr>
<td>

```python
from agent_framework.azure import AzureAIAgentClient
```

</td>
<td>

```python
# Backward compatible - old imports still work
from agent_framework.azure import AzureAIAgentClient

# 🆕 Enhanced GA option - recommended for new code
from agent_framework.foundry import FoundryChatClient
```

</td>
</tr>
</table>

### 3.4 Step 3: Code Migration (Breaking Changes Required)

**📁 Example Files Included:**
- 🔧 **Basic Agent**: [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) (GA compatible)
- 🚀 **Multi-Agent**: [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) (GA compatible)

🚨 **Important**: The GA release has **breaking changes** that require code updates. Use the migration guides below.

#### 3.4.1 demo1-agent-framework.py - Basic Agent Migration

**📁 File**: [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) - Basic single agent example

<table>
<tr>
<th>🔧 Preview Version</th>
<th>🚀 GA Version (Required)</th>
</tr>
<tr>
<td>

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are helpful."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

</td>
<td>

```python
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent  # 🆕 GA API: Agent class
from agent_framework.foundry import FoundryChatClient  # 🆕 Enhanced client
from azure.identity.aio import AzureCliCredential

load_dotenv()  # 🆕 Load environment variables

async def main():
    try:  # 🆕 Enhanced error handling
        async with (
            AzureCliCredential() as credential,
            Agent(  # 🆕 GA API: Agent class (not ChatAgent)
                client=FoundryChatClient(  # 🆕 GA API: 'client' parameter
                    model=os.getenv("FOUNDRY_MODEL", "gpt-4o"),  # 🆕 Model config
                    credential=credential
                ),
                instructions="You are helpful.",
                name="MyAgent"  # 🆕 GA feature: named agents
            ) as agent,
        ):
            result = await agent.run("Tell me a joke")
            print(f"Agent: {result.text}")  # 🆕 Enhanced output formatting
    except Exception as e:  # 🆕 Structured error handling
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

</td>
</tr>
</table>

**🔧 Key Changes Summary for demo1:**

| Aspect | Preview | GA Enhancement |
|--------|---------|----------------|
| **Agent Class** | `ChatAgent` | `Agent` (GA production API) |
| **Client Parameter** | `chat_client=` | `client=` (GA parameter name) |
| **Client Import** | `AzureAIAgentClient` | `FoundryChatClient` (enhanced features) |
| **Model Configuration** | Not required | `model=os.getenv("FOUNDRY_MODEL")` (required) |
| **Environment Loading** | Not needed | `load_dotenv()` and `os` import |
| **Error Handling** | Basic | Structured try/catch with logging |
| **Agent Naming** | Not available | `name="MyAgent"` parameter |
| **Output Format** | Simple print | Formatted with agent identification |

#### 3.4.2 demo2-multi-agent.py - Multi-Agent Migration

**📁 File**: [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) - Multi-agent orchestration system

**🔧 Required Changes Summary for demo2:**

| Component | Change | Details |
|-----------|--------|---------|
| **FoundryChatClient** | Add model parameter | `model=os.getenv("FOUNDRY_MODEL", "gpt-4o")` |
| **Credential Parameter** | Update parameter name | `credential=` (not `async_credential=`) |
| **Agent Constructor** | Update parameter name | `client=` (not `chat_client=`) |

**✅ Result**: Multi-agent system now fully compatible with Agent Framework GA v1.0

**💡 Key Considerations for Multi-Agent Systems:**
- Each agent requires its own FoundryChatClient instance
- Model parameter must be specified for each client
- Named agents are essential for debugging multi-agent interactions
- Agent registry and lifecycle management patterns remain unchanged

#### 3.4.3 Environment Configuration Required

🔧 **Important**: Both demos require your `.env` file to contain:
```bash
FOUNDRY_MODEL=gpt-4o
FOUNDRY_PROJECT_ENDPOINT=https://your-foundry-endpoint.services.ai.azure.com/
```

### 3.5 Step 4: Testing Migration

<table>
<tr>
<th>📋 Preview Installation Commands</th>
<th>🎯 GA Installation Commands</th>
</tr>
<tr>
<td>

```bash
# Preview (unpinned versions)
pip install agent-framework
pip install agent-framework-azure-ai
pip install agent-framework-devui --pre
pip install agent-framework[viz] --pre
```

</td>
<td>

```bash
# 🆕 GA Production (version pinned)
pip install agent-framework>=1.0.0
pip install agent-framework-azure-ai==1.0.0rc6  # ⚠️ RC until GA available
pip install agent-framework-devui --pre
pip install agent-framework[viz] --pre

# 🆕 Or install from requirements.txt
pip install -r requirements.txt
```

</td>
</tr>
</table>

#### **Testing Steps**

**📁 Test with Your Code Files:**

1. **Install GA Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test Updated GA Code:**
   ```bash
   # Test GA-compatible agents
   python python\1.Agents\1.ai-foundry-agents\demo1-agent-framework.py
   python python\1.Agents\1.ai-foundry-agents\demo2-multi-agent.py
   
   # Test any workflow files (no changes needed)
   python python\2.Workflow\1.Getting-started\**\*.py
   ```

3. **Verify GA Features:**
   ```bash
   python -c "import agent_framework; print('Version:', agent_framework.__version__)"
   ```

---

## 4. Migration Checklist

- [ ] **Backup current codebase**
- [ ] **🆕 Update [`requirements.txt`](requirements.txt)** with GA versions (use `==1.0.0rc6` for azure-ai)
- [ ] **🆕 Install GA packages**: `pip install -r requirements.txt`
- [ ] **⚠️ Check for version errors** - See [Error Resolution Guide](README-AgentFramework-Upgrade-Error-and-Solution.md)
- [ ] **Test existing functionality** in [`python/1.Agents/`](python/1.Agents/) and [`python/2.Workflow/`](python/2.Workflow/) - should work unchanged
- [ ] **🆕 Optional**: Enhance with new GA features (FoundryClient, middleware, etc.)
  - [ ] Test [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) and [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py)
  - [ ] Update import statements in your custom agent files
- [ ] **Verify DevUI still works** in [`python/1.Agents/2.DevUI/`](python/1.Agents/2.DevUI/) (preview feature)
- [ ] **Update documentation** to reflect GA status

---

## 5. Additional Resources

### 5.1 Official Microsoft Documentation
- [Agent Framework 1.0 GA Announcement](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [Official Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [PyPI Package](https://pypi.org/project/agent-framework/)

### 5.2 Migration Support
- **[🚨 Error Resolution Guide](README-AgentFramework-Upgrade-Error-and-Solution.md)** - Troubleshoot common upgrade issues
- [Semantic Kernel Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel)
- [AutoGen Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen)
- [Discord Community](https://aka.ms/foundry/discord)

---

*This migration guide helps you transition smoothly from Microsoft Agent Framework Preview to the production-ready GA release. The backward compatibility ensures minimal code changes while unlocking enterprise-grade stability and new capabilities.*
- 📄 [`python\1.Agents\1.ai-foundry-agents\demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) *(Updated for GA)*
- 📄 Any custom agent files in [`python\1.Agents\`](python/1.Agents/) and [`python\2.Workflow\`](python/2.Workflow/)

<table>
<tr>
<th>📖 Preview Version (Deprecated)</th>
<th>✅ GA Version (Required)</th>
</tr>
<tr>
<td>

```python
from agent_framework.azure import AzureAIAgentClient
```

</td>
<td>

```python
# Backward compatible - old imports still work
from agent_framework.azure import AzureAIAgentClient

# 🆕 Enhanced GA option - recommended for new code
**from agent_framework.foundry import FoundryChatClient**
```

</td>
</tr>
</table>

### Step 3: Code Migration (Breaking Changes Required)

**📁 Example Files Included:**
- 🔧 **Basic Agent**: [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) (GA compatible)
- 🚀 **Multi-Agent**: [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) (GA compatible)

🚨 **Important**: The GA release has **breaking changes** that require code updates. Use the migration guides below.

---

#### demo1-agent-framework.py - Basic Agent Migration

**📁 File**: [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) - Basic single agent example

<table>
<tr>
<th>🔧 Preview Version</th>
<th>🚀 GA Version (Required)</th>
</tr>
<tr>
<td>

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are helpful."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

</td>
<td>

```python
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent  # 🆕 GA API: Agent class
from agent_framework.foundry import FoundryChatClient  # 🆕 Enhanced client
from azure.identity.aio import AzureCliCredential

load_dotenv()  # 🆕 Load environment variables

async def main():
    try:  # 🆕 Enhanced error handling
        async with (
            AzureCliCredential() as credential,
            Agent(  # 🆕 GA API: Agent class (not ChatAgent)
                client=FoundryChatClient(  # 🆕 GA API: 'client' parameter
                    model=os.getenv("FOUNDRY_MODEL", "gpt-4o"),  # 🆕 Model config
                    credential=credential
                ),
                instructions="You are helpful.",
                name="MyAgent"  # 🆕 GA feature: named agents
            ) as agent,
        ):
            result = await agent.run("Tell me a joke")
            print(f"Agent: {result.text}")  # 🆕 Enhanced output formatting
    except Exception as e:  # 🆕 Structured error handling
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

</td>
</tr>
</table>

**🔧 Key Changes Summary for demo1:**

| Aspect | Preview | GA Enhancement |
|--------|---------|----------------|
| **Agent Class** | `ChatAgent` | `Agent` (GA production API) |
| **Client Parameter** | `chat_client=` | `client=` (GA parameter name) |
| **Client Import** | `AzureAIAgentClient` | `FoundryChatClient` (enhanced features) |
| **Model Configuration** | Not required | `model=os.getenv("FOUNDRY_MODEL")` (required) |
| **Environment Loading** | Not needed | `load_dotenv()` and `os` import |
| **Error Handling** | Basic | Structured try/catch with logging |
| **Agent Naming** | Not available | `name="MyAgent"` parameter |
| **Output Format** | Simple print | Formatted with agent identification |

---

#### demo2-multi-agent.py - Multi-Agent Migration

**📁 File**: [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py) - Multi-agent orchestration system

**🔧 Required Changes Summary for demo2:**

| Component | Change | Details |
|-----------|--------|---------|
| **FoundryChatClient** | Add model parameter | `model=os.getenv("FOUNDRY_MODEL", "gpt-4o")` |
| **Credential Parameter** | Update parameter name | `credential=` (not `async_credential=`) |
| **Agent Constructor** | Update parameter name | `client=` (not `chat_client=`) |

**✅ Result**: Multi-agent system now fully compatible with Agent Framework GA v1.0

**💡 Key Considerations for Multi-Agent Systems:**
- Each agent requires its own FoundryChatClient instance
- Model parameter must be specified for each client
- Named agents are essential for debugging multi-agent interactions
- Agent registry and lifecycle management patterns remain unchanged

---

#### Environment Configuration Required

🔧 **Important**: Both demos require your `.env` file to contain:
```bash
FOUNDRY_MODEL=gpt-4o
FOUNDRY_PROJECT_ENDPOINT=https://your-foundry-endpoint.services.ai.azure.com/
```

### Step 4: Testing Migration

<table>
<tr>
<th>📋 Preview Installation Commands</th>
<th>🎯 GA Installation Commands</th>
</tr>
<tr>
<td>

```bash
# Preview (unpinned versions)
pip install agent-framework
pip install agent-framework-azure-ai
pip install agent-framework-devui --pre
pip install agent-framework[viz] --pre
```

</td>
<td>

```bash
# 🆕 GA Production (version pinned)
**pip install agent-framework>=1.0.0**
**pip install agent-framework-azure-ai==1.0.0rc6**  # ⚠️ RC until GA available
pip install agent-framework-devui --pre
pip install agent-framework[viz] --pre

# 🆕 Or install from requirements.txt
**pip install -r requirements.txt**
```

</td>
</tr>
</table>

#### Testing Steps

**📁 Test with Your Code Files:**

1. **Install GA Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test Updated GA Code:**
   ```bash
   # Test GA-compatible agents
   python python\1.Agents\1.ai-foundry-agents\demo1-agent-framework.py
   python python\1.Agents\1.ai-foundry-agents\demo2-multi-agent.py
   
   # Test any workflow files (no changes needed)
   python python\2.Workflow\1.Getting-started\**\*.py
   ```

3. **Verify GA Features:**
   ```bash
   python -c "import agent_framework; print('Version:', agent_framework.__version__)"
   ```

#### New GA Capabilities Summary

| **🆕 Feature** | **Description** | **Implementation** |
|---------|-------------|----------------|
| **🆕 Middleware Pipeline** | Enterprise compliance, logging, monitoring | `agent = Agent(**middleware=[...]**, ...)` |
| **🆕 Named Agents** | Better tracking and debugging | `agent = Agent(**name="CustomerService"**, ...)` |  
| **🆕 Enhanced Clients** | Better Foundry integration | `**FoundryChatClient**(project_endpoint="...", model="...")` |
| **🆕 Declarative Config** | YAML-based agent definitions | Load agents from `**agents.yaml**` files |

## 📋 Migration Checklist

- [ ] **Backup current codebase**
- [ ] **🆕 Update [`requirements.txt`](requirements.txt)** with GA versions (use `==1.0.0rc6` for azure-ai)
- [ ] **🆕 Install GA packages**: `pip install -r requirements.txt`
- [ ] **⚠️ Check for version errors** - See [Error Resolution Guide](README-AgentFramework-Upgrade-Error-and-Solution.md)
- [ ] **Test existing functionality** in [`python/1.Agents/`](python/1.Agents/) and [`python/2.Workflow/`](python/2.Workflow/) - should work unchanged
- [ ] **🆕 Optional**: Enhance with new GA features (FoundryClient, middleware, etc.)
  - [ ] Test [`demo1-agent-framework.py`](python/1.Agents/1.ai-foundry-agents/demo1-agent-framework.py) and [`demo2-multi-agent.py`](python/1.Agents/1.ai-foundry-agents/demo2-multi-agent.py)
  - [ ] Update import statements in your custom agent files
- [ ] **Verify DevUI still works** in [`python/1.Agents/2.DevUI/`](python/1.Agents/2.DevUI/) (preview feature)
- [ ] **Update documentation** to reflect GA status

## 🔗 Additional Resources

### Official Microsoft Documentation
- [Agent Framework 1.0 GA Announcement](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [Official Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [PyPI Package](https://pypi.org/project/agent-framework/)

### Migration Support
- **[🚨 Error Resolution Guide](README-AgentFramework-Upgrade-Error-and-Solution.md)** - Troubleshoot common upgrade issues
- [Semantic Kernel Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel)
- [AutoGen Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen)
- [Discord Community](https://aka.ms/foundry/discord)

---

*This migration guide helps you transition smoothly from Microsoft Agent Framework Preview to the production-ready GA release. The backward compatibility ensures minimal code changes while unlocking enterprise-grade stability and new capabilities.* 