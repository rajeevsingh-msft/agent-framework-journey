# Agents in Workflow - Complete Guide

## Overview

This guide explains all the **Agents in Workflow** samples from the Microsoft Agent Framework and helps you choose the right pattern for your use case.

---

## 📋 Quick Reference: All Agent Workflow Samples

| Sample | File | Best For | Complexity |
|--------|------|----------|------------|
| **Azure Chat Agents (Streaming)** | `azure_chat_agents_streaming.py` | Real-time chat responses | Beginner |
| **Azure AI Chat Agents (Streaming)** | `azure_ai_agents_streaming.py` | Azure AI Foundry agents | Beginner |
| **Azure Chat Agents (Function Bridge)** | `azure_chat_agents_function_bridge.py` | Injecting external context between agents | Intermediate |
| **Azure Chat Agents (Tools + HITL)** | `azure_chat_agents_tool_calls_with_feedback.py` | Human-in-the-loop approval | Intermediate |
| **Custom Agent Executors** | `custom_agent_executors.py` | Custom agent run logic | Intermediate |
| **Sequential Workflow as Agent** | `sequential_workflow_as_agent.py` | Exposing workflows as reusable agents | Intermediate |
| **Concurrent Workflow as Agent** | `concurrent_workflow_as_agent.py` | Parallel agents as single agent | Intermediate |
| **Magentic Workflow as Agent** | `magentic_workflow_as_agent.py` | Magentic-One orchestration | Advanced |
| **Workflow as Agent (Reflection)** | `workflow_as_agent_reflection_pattern.py` | Self-improving agents | Advanced |
| **Workflow as Agent + HITL** | `workflow_as_agent_human_in_the_loop.py` | Human approval gates | Intermediate |
| **Workflow as Agent with Thread** | `workflow_as_agent_with_thread.py` | Conversation memory | Intermediate |
| **Workflow as Agent kwargs** | `workflow_as_agent_kwargs.py` | Passing custom context | Intermediate |
| **Handoff Workflow as Agent** | `handoff_workflow_as_agent.py` | Agent-to-agent handoffs | Advanced |

---

## 🔍 Detailed Sample Explanations

### 1. Azure Chat Agents (Streaming)
**File:** `azure_chat_agents_streaming.py`

**What it does:**
- Adds Azure Chat agents as workflow nodes (executors)
- Streams responses in real-time (token by token)

**When to use:**
- You want real-time streaming output (like ChatGPT typing effect)
- Building chatbots with responsive UX

**Pattern:**
```
[User Input] → [Agent A] → [Agent B] → [Streaming Output]
                  ↓            ↓
              (streams)    (streams)
```

---

### 2. Azure AI Chat Agents (Streaming)
**File:** `azure_ai_agents_streaming.py`

**What it does:**
- Uses Azure AI Foundry agents (not just OpenAI)
- Supports streaming responses

**When to use:**
- You're using Azure AI Foundry (not just Azure OpenAI)
- Need access to AI Foundry features (tools, files, etc.)

---

### 3. Azure Chat Agents (Function Bridge)
**File:** `azure_chat_agents_function_bridge.py`

**What it does:**
- Chains two agents with a **function executor** in between
- The function can inject external context (RAG, database lookups, etc.)

**When to use:**
- You need to **enrich data between agents**
- RAG-based systems where you fetch context between steps
- Multi-step pipelines with data transformation

**Pattern:**
```
[User Query] → [Agent 1] → [Function Bridge] → [Agent 2] → [Output]
                              ↓
                     (fetch from DB/API/RAG)
```

**Example Use Case:**
```
User: "What's the status of order #12345?"
         ↓
    [Intent Agent] → understands user wants order status
         ↓
    [Function Bridge] → fetches order from database
         ↓
    [Response Agent] → generates friendly response with order details
```

---

### 4. Azure Chat Agents (Tools + HITL)
**File:** `azure_chat_agents_tool_calls_with_feedback.py`

**What it does:**
- Writer/Editor pipeline with **human feedback gating**
- Human can approve, reject, or modify agent outputs

**When to use:**
- Content moderation workflows
- Approval processes before final output
- Quality control with human oversight

**Pattern:**
```
[Writer Agent] → [Human Review] → [Editor Agent] → [Output]
                      ↓
              (approve/reject/modify)
```

---

### 5. Custom Agent Executors
**File:** `custom_agent_executors.py`

**What it does:**
- Create custom executors to handle agent `run` methods
- Full control over how agents are invoked

**When to use:**
- Need custom pre/post processing around agent calls
- Want to modify agent behavior dynamically

---

### 6. Sequential Workflow as Agent ⭐
**File:** `sequential_workflow_as_agent.py`

**What it does:**
- Builds a sequential workflow with multiple agents
- **Exposes the entire workflow as a single reusable agent**

**When to use:**
- You have a multi-step agent pipeline
- Want to reuse the pipeline as a single "super agent"
- Building modular, composable agent systems

**Pattern:**
```
┌─────────────────────────────────────────────┐
│         WORKFLOW (exposed as Agent)         │
│                                             │
│  [Agent A] → [Agent B] → [Agent C]          │
│                                             │
└─────────────────────────────────────────────┘
                    ↓
         Can be used like a single agent!
```

---

### 7. Concurrent Workflow as Agent ⭐
**File:** `concurrent_workflow_as_agent.py`

**What it does:**
- Builds a concurrent (parallel) workflow
- **Exposes it as a single reusable agent**

**When to use:**
- Multiple agents can run in parallel
- Want to wrap parallel execution as a single agent

**Pattern:**
```
┌─────────────────────────────────────────────┐
│         WORKFLOW (exposed as Agent)         │
│                                             │
│      ┌→ [Agent A] ─┐                        │
│  [D] → [Agent B] → [Aggregator]             │
│      └→ [Agent C] ─┘                        │
│                                             │
└─────────────────────────────────────────────┘
```

---

### 8. Workflow as Agent (Reflection Pattern) ⭐
**File:** `workflow_as_agent_reflection_pattern.py`

**What it does:**
- Agent generates output, then **reflects on its own output**
- Self-improvement loop

**When to use:**
- Self-correcting agents
- Quality improvement through reflection
- Research/writing agents that revise their work

**Pattern:**
```
[Generate] → [Reflect] → [Improve] → [Final Output]
     ↑______________|
         (loop until satisfied)
```

---

### 9. Workflow as Agent + HITL (Human-in-the-Loop)
**File:** `workflow_as_agent_human_in_the_loop.py`

**What it does:**
- Extends workflow-as-agent with human approval gates
- Humans can intervene at key decision points

**When to use:**
- High-stakes decisions requiring human approval
- Compliance workflows
- Risk assessment with human oversight

---

### 10. Workflow as Agent with Thread
**File:** `workflow_as_agent_with_thread.py`

**What it does:**
- Uses `AgentThread` to maintain **conversation history**
- Agents remember previous interactions

**When to use:**
- Multi-turn conversations
- Chatbots that need context across messages
- Agents that build on previous outputs

---

### 11. Workflow as Agent kwargs
**File:** `workflow_as_agent_kwargs.py`

**What it does:**
- Pass custom context (data, user tokens, etc.) via kwargs
- Context flows through `workflow.as_agent()` to `@ai_function` tools

**When to use:**
- Need to pass user-specific data to tools
- Authentication tokens, session data, etc.

---

### 12. Handoff Workflow as Agent ⭐
**File:** `handoff_workflow_as_agent.py`

**What it does:**
- Uses `HandoffBuilder` for agent-to-agent handoffs
- Includes Human-in-the-Loop via `FunctionCallContent`/`FunctionResultContent`

**When to use:**
- Complex multi-agent systems with dynamic routing
- Agents that need to "hand off" to specialists
- Customer service escalation workflows

**Pattern:**
```
[Triage Agent] → Decision: What type of request?
       │
       ├→ Billing Issue → [Billing Agent]
       ├→ Technical Issue → [Tech Support Agent]
       └→ General Query → [General Agent]
```

---

## 🎯 Which Sample Should You Use?

### For RAG-based Chatbots

**Recommended:** `azure_chat_agents_function_bridge.py`

```
User Query → [Intent/Query Agent] → [RAG Function Bridge] → [Response Agent]
                                           ↓
                                    (fetch from vector DB)
```

**Why:**
- Function bridge lets you inject RAG context between agents
- First agent understands intent, function fetches relevant docs, second agent responds

---

### For Multi-Agent Systems with LLM

**Recommended:** 
- Simple: `sequential_workflow_as_agent.py`
- With handoffs: `handoff_workflow_as_agent.py`
- With human approval: `workflow_as_agent_human_in_the_loop.py`

---

### For Any Approval related Workflow


```
Mail Received → Digitization → Content Analysis → Risk Assessment
                                                        │
                                    ┌───────────────────┼───────────────────┐
                                    ↓                                       ↓
                              High Risk                                Low Risk
                                    ↓                                       ↓
                           Compliance Agent                          Workflow Agent
                                    ↓                                       │
                         Security Officer Review                            │
                                    ↓                                       │
                           Approval Decision                                │
                              │         │                                   │
                        Approved    Rejected                                │
                              │         │                                   │
                              ↓         ↓                                   │
                              │    Return to Sender                         │
                              │                                             │
                              └──────────→ Mail Database ←──────────────────┘
                                               ↓
                                       Notification System
```

**Recommended Samples:**

| Stage | Sample to Use |
|-------|---------------|
| **Overall Architecture** | `handoff_workflow_as_agent.py` - for dynamic routing between agents |
| **Risk Assessment Branching** | Use `workflow_with_branching_logic` pattern |
| **High Risk Path (Human Approval)** | `workflow_as_agent_human_in_the_loop.py` |
| **Agent Chaining** | `sequential_workflow_as_agent.py` |
| **External System Calls** | `azure_chat_agents_function_bridge.py` - for DB/API calls |

**Implementation Approach:**

```python
# Your workflow would combine multiple patterns:

# 1. Digitization Agent
digitization_agent = chat_client.as_agent(
    instructions="Extract text and metadata from incoming mail...",
    name="digitization"
)

# 2. Content Analysis Agent  
analysis_agent = chat_client.as_agent(
    instructions="Analyze mail content, categorize, extract key entities...",
    name="content_analysis"
)

# 3. Risk Assessment Agent (with branching)
risk_agent = chat_client.as_agent(
    instructions="Assess risk level: HIGH or LOW based on content...",
    name="risk_assessment"
)

# 4. Compliance Agent (for high-risk)
compliance_agent = chat_client.as_agent(
    instructions="Review for compliance issues, flag concerns...",
    name="compliance"
)

# 5. Build with HandoffBuilder for dynamic routing
workflow = (
    HandoffBuilder()
    .add_agent(digitization_agent)
    .add_agent(analysis_agent)
    .add_agent(risk_agent)
    .add_agent(compliance_agent)
    # ... add routing logic
    .build()
)
```

---

## 📊 Decision Matrix

| Your Need | Use This Sample |
|-----------|-----------------|
| Simple agent chain | `3.agents-in-workflow.py` (what you have) |
| Add RAG/external data | `function_bridge.py` |
| Human approval gates | `human_in_the_loop.py` |
| Conversation memory | `with_thread.py` |
| Self-improving agents | `reflection_pattern.py` |
| Dynamic agent routing | `handoff_workflow_as_agent.py` |
| Parallel agents | `concurrent_workflow_as_agent.py` |
| Reuse workflow as agent | `sequential_workflow_as_agent.py` |
| Real-time streaming | `streaming.py` variants |

---


## 📚 Resources

- [GitHub: Agent Framework Workflow Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/workflows#agents)
- [Microsoft Docs: Agents in Workflows](https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/agents-in-workflows)

---

**Built with ❤️ using Microsoft Agent Framework**
