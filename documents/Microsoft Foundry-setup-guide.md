# Setup Guide

This comprehensive guide walks you through the essential configuration steps needed to get started with the Agent Framework Journey repository.


This guide covers two critical setup components:

1. **Azure AI Foundry Project Configuration** - Understanding the setup approach and requirements
2. **Step-by-Step Implementation** - Detailed instructions for creating and configuring your AI Foundry project



# 1.  Azure AI Foundry set  Guide: Choosing Between Direct OpenAI and AI Foundry Project Approaches

When building AI applications with Azure, developers often face a choice between two distinct approaches: **Azure OpenAI Direct** and **Azure AI Foundry Projects**. Understanding these differences is crucial for selecting the right architecture for your use case.

## 🎯 The Two Approaches

### Azure OpenAI Direct Approach
This is the straightforward path where you connect directly to an Azure OpenAI resource. Think of it as having a direct conversation with a specific AI model.

```python
# Direct Azure OpenAI approach
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

client = AzureOpenAIChatClient(credential=AzureCliCredential())
agent = client.create_agent(instructions="You are a helpful assistant")
```

**Environment Variables:**
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01
```

### Azure AI Studio Project Approach
This leverages Azure AI Studio's comprehensive project ecosystem, providing enhanced capabilities and enterprise-grade features.

```python
# Azure AI Project approach
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async with AzureAIAgentClient(async_credential=credential) as client:
    agent = ChatAgent(chat_client=client, instructions="Advanced agent")
```

**Environment Variables:**
```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.westus.aiprojects.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

## 🔍 Key Differences at a Glance

| Feature | Azure OpenAI Direct | Azure AI Studio Project |
|---------|-------------------|-------------------------|
| **Complexity** | Simple, minimal setup | Enterprise-grade, feature-rich |
| **Use Case** | Chat apps, basic AI integration | Complex workflows, multi-service apps |
| **Endpoint** | `*.openai.azure.com` | `*.aiprojects.azure.com` |
| **Management** | Azure OpenAI Studio | Azure AI Studio |
| **Team Features** | Limited | Collaboration, versioning, monitoring |
| **Service Integration** | Single OpenAI service | Multiple AI services ecosystem |

## 🚀 When to Choose What?

### Choose **Azure OpenAI Direct** when:
- Building simple chatbots or Q&A systems
- Need quick prototyping and minimal configuration
- Working on personal projects or small teams
- Primarily need text generation capabilities
- Want straightforward API access without additional overhead

### Choose **Azure AI Studio Project** when:
- Building enterprise applications with complex workflows
- Need integration with multiple Azure AI services
- Require team collaboration and project management features
- Want advanced monitoring, logging, and governance
- Planning to scale across multiple AI capabilities (vision, speech, etc.)
- Need built-in tools and pre-configured connections

## 💡 Developer Tip

If you're just starting with Azure AI or building a proof-of-concept, begin with the **Azure OpenAI Direct** approach. It's easier to understand, faster to set up, and covers most basic AI integration needs. You can always migrate to Azure AI Studio Projects later when your requirements grow more complex.

The choice ultimately depends on your project's complexity, team size, and long-term scalability requirements. Both approaches are valid and serve different segments of the AI development spectrum.

---

## 🏭 **2. Creating an AI Foundry Project - Microsoft's Current Recommendation**

Since you need to use `AZURE_AI_PROJECT_ENDPOINT` for the Agent Framework, here's how to create an **AI Foundry Project** - Microsoft's latest unified platform for building AI applications.

### **AI Foundry Project Overview**

**AI Foundry** is Microsoft's evolution of Azure AI Studio with enhanced capabilities for:

- 🤖 **Multi-modal AI agents** (text, vision, speech)
- 🔧 **Built-in tools and integrations** 
- 📊 **Advanced monitoring and evaluation**
- 🔄 **MLOps workflows**
- 👥 **Team collaboration features**
- 🛡️ **Enterprise-grade security and governance**

### **Azure AI Resource Types Explained**

When you visit AI Foundry, you'll see different resource types:

| Resource Type | Purpose | When to Use |
|---------------|---------|-------------|
| **Azure OpenAI** | Direct model access | Simple chat apps, basic integration |
| **Hub** | Enterprise foundation | Shared governance, multiple teams |
| **Project** | Individual workspace | Organized AI development |
| **AI Foundry** | Latest project interface | New projects (recommended) |

### **Step-by-Step Project Creation**

#### **Step 1: Access AI Foundry**
1. Go to **[https://ai.azure.com](https://ai.azure.com)**
2. Sign in with your Azure credentials

#### **Step 2: Create New Project**
1. Click **"+ New project"** or **"Create project"**
2. Fill in project details:
   - **Project name:** `agent-framework-demo` (or your preferred name)
   - **Subscription:** Select your Azure subscription
   - **Resource group:** Create new or select existing
   - **Region:** Choose a region (e.g., `East US`, `West US 2`)

#### **Step 3: Configure Project Settings**
1. **Hub selection:** 
   - Create new Hub (recommended for first project)
   - Or select existing Hub if available
2. **Connected services:**
   - Link your existing Azure OpenAI resource (e.g., `rks-rag-openai`)
   - This allows you to use your existing `gpt-4o` deployment

#### **Step 4: Get Your Project Endpoint**
Once created, your project endpoint will follow this format:
```
https://your-project-name.your-region.aiprojects.azure.com
```

**How to find it in AI Foundry:**
- **Option A:** Project Overview → "Project details" → "Project endpoint"
- **Option B:** Settings → General → "Project endpoint" 
- **Option C:** Check browser URL when in project: `https://ai.azure.com/projects/your-project-name/`

#### **Step 5: Update Your Environment Configuration**
Replace the placeholder in your `.env` file (located in the root directory):

```env
#Azure AI Project Configuration Approach
AZURE_AI_PROJECT_ENDPOINT=https://your-actual-project-name.your-region.aiprojects.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

**File Location**: `AgentFramework/.env`

#### **Step 6: Verify Configuration**
Test your setup with this code:

```python
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
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

### **Troubleshooting Common Issues**

| Issue | Solution |
|-------|----------|
| "Project endpoint required" | Ensure `AZURE_AI_PROJECT_ENDPOINT` is set correctly |
| "Authentication failed" | Run `az login` to refresh credentials |
| "Deployment not found" | Verify `AZURE_AI_MODEL_DEPLOYMENT_NAME` matches your model |
| "Connection timeout" | Check network connectivity and firewall settings |

---

*This guide helps you set up AI Foundry Projects for advanced Agent Framework development with Microsoft's latest AI platform.*