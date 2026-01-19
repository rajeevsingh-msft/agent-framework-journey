# Sequential Workflow - Getting Started

## Overview

This folder contains sample programs that demonstrate **Sequential Workflows** using the Microsoft Agent Framework. Sequential workflows are the foundation of building complex AI agent systems where steps must execute in a specific order, with each step depending on the output of the previous step.

| Sample | Description | Complexity |
|--------|-------------|------------|
| [1.create-sequential-workflow.py](1.create-sequential-workflow.py) | Basic 2-step text transformation (both executor styles) | Beginner |
| [1b-class-based-executor.py](1b-class-based-executor.py) | Same example using **only class-based** executors | Beginner |
| [1c-function-based-executor.py](1c-function-based-executor.py) | Same example using **only function-based** executors | Beginner |
| [2.realworld-sequential-workflow.py](2.realworld-sequential-workflow.py) | Customer support email processing pipeline | Intermediate |

### Additional Documentation

| File | Description |
|------|-------------|
| [Readme-ref.md](Readme-ref.md) | How Microsoft Copilot works behind the scenes |

---

## Prerequisites

### Required Packages

Install the following packages before running the samples:

```bash
pip install agent-framework typing_extensions
```

Or install all dependencies from the root requirements.txt:

```bash
pip install -r ../../../requirements.txt
```

### Python Version
- Python 3.10 or later

### No External AI Services Required
Both samples use simple rule-based logic and don't require any Azure/OpenAI API keys.

---

## Core Concepts

### What is a Sequential Workflow?

A sequential workflow is a series of **Executors** (processing nodes) connected in a linear chain. Each executor:
1. Receives input from the previous executor
2. Processes/transforms the data
3. Passes the result to the next executor

```
[Input] → [Executor 1] → [Executor 2] → [Executor 3] → [Output]
```

### Key Components

| Component | Description |
|-----------|-------------|
| **Executor** | A unit of work (processing node) in the workflow |
| **WorkflowBuilder** | Fluent API to connect executors and build the workflow |
| **WorkflowContext** | Provides methods to pass data between executors |
| **@handler** | Decorator marking the async method that does the work (class-based) |
| **@executor** | Decorator to create a function-based executor |

### Two Ways to Create Executors

#### 1. Class-based Executor (more control)
```python
class MyExecutor(Executor):
    def __init__(self):
        super().__init__(id="my_executor")
    
    @handler
    async def process(self, input: str, ctx: WorkflowContext[str]) -> None:
        result = input.upper()
        await ctx.send_message(result)  # Pass to next executor
```

#### 2. Function-based Executor (simpler)
```python
@executor(id="my_executor")
async def process(input: str, ctx: WorkflowContext[str]) -> None:
    result = input.upper()
    await ctx.send_message(result)
```

### Passing Data Between Executors

| Method | Purpose |
|--------|---------|
| `ctx.send_message(data)` | Pass data to the next executor in the chain |
| `ctx.yield_output(data)` | Return final workflow output (used by terminal executor) |

---

## Sample 1: Basic Sequential Workflow

**File:** `1.create-sequential-workflow.py`

### What It Does

A simple 2-step workflow that transforms text:

```
Input: "hello world"
         ↓
┌─────────────────────┐
│    UpperCase        │  → Converts to "HELLO WORLD"
│  (Class-based)      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   reverse_text      │  → Reverses to "DLROW OLLEH"
│ (Function-based)    │
└──────────┬──────────┘
           ↓
Output: "DLROW OLLEH"
```

### Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    WORKFLOW EXECUTION                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Input: "hello world"                                           │
│              │                                                   │
│              ▼                                                   │
│   ┌────────────────────┐                                         │
│   │  UpperCase         │  ← Class-based Executor                 │
│   │  ────────────────  │                                         │
│   │  text.upper()      │                                         │
│   │  ctx.send_message()│  → Sends "HELLO WORLD" to next node     │
│   └─────────┬──────────┘                                         │
│             │                                                    │
│             ▼                                                    │
│   ┌────────────────────┐                                         │
│   │  reverse_text      │  ← Function-based Executor              │
│   │  ────────────────  │                                         │
│   │  text[::-1]        │                                         │
│   │  ctx.yield_output()│  → Returns final result                 │
│   └─────────┬──────────┘                                         │
│             │                                                    │
│             ▼                                                    │
│   Output: "DLROW OLLEH"                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Running the Sample

```bash
cd python/2.Workflow/1.Getting-started/1.Sequential-workflow
py 1.create-sequential-workflow.py
```

### Expected Output

```
Event: ExecutorInvokedEvent(executor_id=upper_case_executor)
Event: ExecutorCompletedEvent(executor_id=upper_case_executor)
Event: ExecutorInvokedEvent(executor_id=reverse_text_executor)
Event: ExecutorCompletedEvent(executor_id=reverse_text_executor)
Event: WorkflowOutputEvent(data='DLROW OLLEH', source_executor_id=reverse_text_executor)
Workflow completed with result: DLROW OLLEH
```

### Understanding the Output

| Event | Meaning |
|-------|---------|
| `ExecutorInvokedEvent(executor_id=upper_case_executor)` | UpperCase executor started processing |
| `ExecutorCompletedEvent(executor_id=upper_case_executor)` | UpperCase executor finished |
| `ExecutorInvokedEvent(executor_id=reverse_text_executor)` | reverse_text executor started |
| `ExecutorCompletedEvent(executor_id=reverse_text_executor)` | reverse_text executor finished |
| `WorkflowOutputEvent(data='DLROW OLLEH', ...)` | Final output yielded by terminal executor |

---

## Sample 2: Real-World Sequential Workflow

**File:** `2.realworld-sequential-workflow.py`

### What It Does

A practical 3-step workflow that processes customer support emails:

1. **Classify** the email (billing/technical/general)
2. **Generate** an appropriate response based on category
3. **Format** the final email with greeting, body, and signature

### Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│           CUSTOMER SUPPORT EMAIL PROCESSING PIPELINE             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   [CustomerEmail]                                                │
│   ├─ customer_name: "John Smith"                                 │
│   └─ email_body: "I was charged twice..."                        │
│              │                                                   │
│              ▼                                                   │
│   ┌────────────────────┐                                         │
│   │  EmailClassifier   │  Step 1: CLASSIFY                       │
│   │  ────────────────  │                                         │
│   │  Analyzes keywords │                                         │
│   │  → "billing"       │                                         │
│   └─────────┬──────────┘                                         │
│             │                                                    │
│             ▼                                                    │
│   [ClassifiedEmail]                                              │
│   ├─ customer_name: "John Smith"                                 │
│   ├─ email_body: "I was charged twice..."                        │
│   └─ category: "billing"  ← NEW FIELD                            │
│             │                                                    │
│             ▼                                                    │
│   ┌────────────────────┐                                         │
│   │  generate_response │  Step 2: RESPOND                        │
│   │  ────────────────  │                                         │
│   │  Creates response  │                                         │
│   │  based on category │                                         │
│   └─────────┬──────────┘                                         │
│             │                                                    │
│             ▼                                                    │
│   [DraftResponse]                                                │
│   ├─ customer_name: "John Smith"                                 │
│   ├─ category: "billing"                                         │
│   └─ response_body: "Thank you for contacting us..."             │
│             │                                                    │
│             ▼                                                    │
│   ┌────────────────────┐                                         │
│   │  format_email      │  Step 3: FORMAT                         │
│   │  ────────────────  │                                         │
│   │  Adds greeting,    │                                         │
│   │  signature, ref #  │                                         │
│   └─────────┬──────────┘                                         │
│             │                                                    │
│             ▼                                                    │
│   [FinalResponse]                                                │
│   ├─ to: "John Smith"                                            │
│   ├─ subject: "Re: Your Billing Inquiry"                         │
│   └─ body: "Dear John Smith,\n\nThank you..."                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Data Models (Data Flowing Between Steps)

```python
@dataclass
class CustomerEmail:        # Input
    customer_name: str
    email_body: str

@dataclass 
class ClassifiedEmail:      # After Step 1
    customer_name: str
    email_body: str
    category: str           # NEW: "billing", "technical", or "general"

@dataclass
class DraftResponse:        # After Step 2
    customer_name: str
    category: str
    response_body: str      # NEW: Generated response text

@dataclass
class FinalResponse:        # After Step 3 (Final Output)
    to: str
    subject: str
    body: str               # Complete formatted email
```

### Running the Sample

```bash
cd python/2.Workflow/1.Getting-started/1.Sequential-workflow
py 1a-realworld-sequential-workflow.py
```

### Expected Output

The sample processes 3 test emails. Here's the output for one:

```
======================================================================
📨 PROCESSING EMAIL FROM: John Smith
   Message: I was charged twice for my subscription last month...
======================================================================

📧 Step 1: Classifying email from John Smith...
   ✓ Category assigned: BILLING

💬 Step 2: Generating response for billing inquiry...
   ✓ Response draft created (170 characters)

📝 Step 3: Formatting final email...
   ✓ Email formatted with subject: Re: Your Billing Inquiry

----------------------------------------------------------------------
✅ FINAL OUTPUT:
----------------------------------------------------------------------
To: John Smith
Subject: Re: Your Billing Inquiry

Dear John Smith,

Thank you for contacting us about your billing concern. I've reviewed your 
account and will help resolve this. Our billing team will process your 
request within 24 hours.

Best regards,
Customer Support Team
Acme Corporation

---
Category: BILLING
Reference: #CS-7819
```

### Understanding the Output

| Step | What Happens | Data Transformation |
|------|--------------|---------------------|
| **Step 1** | Classifier analyzes keywords in email | `CustomerEmail` → `ClassifiedEmail` (adds category) |
| **Step 2** | Response generator creates category-specific reply | `ClassifiedEmail` → `DraftResponse` (adds response_body) |
| **Step 3** | Formatter adds greeting, signature, reference | `DraftResponse` → `FinalResponse` (complete email) |

### Test Cases

The sample includes 3 test emails:

| Customer | Email Content | Detected Category |
|----------|---------------|-------------------|
| John Smith | "I was charged twice...refund" | BILLING |
| Sarah Johnson | "App keeps crashing...frustrating!" | TECHNICAL |
| Mike Wilson | "I love your product!" | GENERAL |

---

## Key Takeaways

1. **Sequential = Linear Flow**: Each step MUST complete before the next starts
2. **Data Transformation**: Each executor can transform the data type for the next step
3. **Two Executor Styles**: Use class-based for complex logic, function-based for simple steps
4. **send_message vs yield_output**: 
   - `send_message()` → passes data to next executor
   - `yield_output()` → returns final workflow result
5. **Streaming Events**: Use `run_stream()` to observe real-time execution events

---

## Real-World Use Cases for Sequential Workflows

Sequential workflows are ideal when **each step depends on the output of the previous step**. Here are production scenarios:

### 1. Document Processing Pipeline

```
[Upload Document] → [Extract Text (OCR)] → [Summarize] → [Translate] → [Store]
```

**Example:** Insurance claim processing
- Step 1: Receive claim document (PDF/image)
- Step 2: OCR to extract text
- Step 3: AI classifies claim type
- Step 4: Extract key entities (dates, amounts, names)
- Step 5: Route to appropriate department

### 2. Content Moderation Pipeline

```
[User Post] → [Text Analysis] → [Image Analysis] → [Policy Check] → [Approve/Flag]
```

**Example:** Social media moderation
- Step 1: Receive user-generated content
- Step 2: Analyze text for harmful content
- Step 3: Analyze images for inappropriate content
- Step 4: Check against community guidelines
- Step 5: Auto-approve or flag for human review

### 3. Customer Onboarding

```
[Application] → [Identity Verification] → [Credit Check] → [Account Creation] → [Welcome Email]
```

**Example:** Bank account opening
- Step 1: Collect customer information
- Step 2: Verify identity documents (KYC)
- Step 3: Run credit/background checks
- Step 4: Create account in system
- Step 5: Send onboarding materials

### 4. E-Commerce Order Processing

```
[Order Placed] → [Inventory Check] → [Payment Processing] → [Shipping Label] → [Notification]
```

**Example:** Online retail order fulfillment
- Step 1: Receive order
- Step 2: Verify inventory availability
- Step 3: Process payment
- Step 4: Generate shipping label
- Step 5: Send confirmation + tracking

### 5. AI-Powered Research Assistant

```
[Query] → [Search Documents] → [Extract Relevant Info] → [Synthesize Answer] → [Generate Response]
```

**Example:** Legal research assistant
- Step 1: Receive legal question
- Step 2: Search case law database
- Step 3: Extract relevant precedents
- Step 4: Synthesize findings with AI
- Step 5: Format legal brief

### 6. CI/CD Pipeline (DevOps)

```
[Code Commit] → [Build] → [Test] → [Security Scan] → [Deploy]
```

**Example:** Software deployment
- Step 1: Developer commits code
- Step 2: Build application
- Step 3: Run automated tests
- Step 4: Security vulnerability scan
- Step 5: Deploy to production

### 7. Healthcare Diagnosis Support

```
[Patient Symptoms] → [Initial Triage] → [Test Recommendations] → [Analysis] → [Report]
```

**Example:** Medical imaging analysis
- Step 1: Receive patient symptoms + images
- Step 2: AI triage for urgency
- Step 3: Recommend additional tests
- Step 4: Analyze results with AI
- Step 5: Generate report for physician

### 8. Invoice Processing (Accounts Payable)

```
[Receive Invoice] → [OCR Extract] → [Validate Data] → [Match PO] → [Approve Payment]
```

**Example:** Enterprise AP automation
- Step 1: Receive invoice (email/scan)
- Step 2: Extract data with OCR
- Step 3: Validate vendor and amounts
- Step 4: Match to purchase order
- Step 5: Route for approval

---

## When to Use Sequential vs Other Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| **Sequential** | Steps must happen in order, each depends on previous | Document processing, onboarding |
| **Concurrent** | Independent steps can run in parallel | Fetching data from multiple APIs |
| **Branching** | Different paths based on conditions | Approval routing based on amount |
| **Multi-Agent** | Complex reasoning needs multiple specialists | Research, complex problem solving |

---

## Next Steps

- [2. Concurrent Workflow](../2.Concurrent-workflow/) - Run executors in parallel
- [3. Agents in Workflow](../3.Agents-in-Workflow/) - Integrate AI agents into workflows

---

## References

### Agent Framework Documentation
- [Agent Framework - Sequential Workflow Tutorial](https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/simple-sequential-workflow)
- [Agent Framework - Workflow Core Concepts](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/workflows)
- [Agent Framework - Executors](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/executors)
- [Agent Framework - Events](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/events)

### Related Azure AI Services
- [Azure AI Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/) - For document processing use cases
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) - For content moderation use cases
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/) - For AI-powered workflows

### Other Orchestration Technologies
- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview/) - Microsoft's AI orchestration SDK
- [Azure Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/) - Low-code workflow orchestration
- [Azure Durable Functions](https://learn.microsoft.com/en-us/azure/azure-functions/durable/) - Serverless workflow patterns
- [Microsoft Copilot Architecture](https://learn.microsoft.com/en-us/microsoft-365-copilot/microsoft-365-copilot-overview) - How Copilot uses orchestration
