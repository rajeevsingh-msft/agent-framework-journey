"""
Real-World Example: Customer Support Email Processing Pipeline

This workflow demonstrates a practical sequential workflow that processes
customer support emails through 3 stages:

    [Incoming Email] 
           ↓
    ┌─────────────────┐
    │ 1. CLASSIFIER   │  → Categorizes email (billing/technical/general)
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 2. RESPONDER    │  → Generates appropriate response based on category
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 3. FORMATTER    │  → Formats the final email with greeting/signature
    └────────┬────────┘
             ↓
    [Final Response Email]

Why Sequential Workflow?
- Each step MUST complete before the next can start
- Data flows in one direction: Email → Category → Draft → Final Response
- Each executor transforms the data for the next step

No external AI services needed - uses simple rule-based logic for demo purposes.
"""

import asyncio
from dataclasses import dataclass
from typing_extensions import Never
from agent_framework import WorkflowBuilder, WorkflowContext, WorkflowOutputEvent, WorkflowViz, executor, Executor, handler


# ============================================================================
# DATA MODELS - Define the shape of data flowing between executors
# ============================================================================

@dataclass
class CustomerEmail:
    """Input: Raw customer email"""
    customer_name: str
    email_body: str


@dataclass 
class ClassifiedEmail:
    """After Step 1: Email with category assigned"""
    customer_name: str
    email_body: str
    category: str  # "billing", "technical", or "general"


@dataclass
class DraftResponse:
    """After Step 2: Generated response draft"""
    customer_name: str
    category: str
    response_body: str


@dataclass
class FinalResponse:
    """After Step 3: Formatted final email"""
    to: str
    subject: str
    body: str


# ============================================================================
# STEP 1: EMAIL CLASSIFIER
# Analyzes the email content and assigns a category
# ============================================================================

class EmailClassifier(Executor):
    """Classifies incoming emails into categories based on keywords."""
    
    def __init__(self):
        super().__init__(id="email_classifier")
    
    @handler
    async def classify(self, email: CustomerEmail, ctx: WorkflowContext[ClassifiedEmail]) -> None:
        print(f"\n📧 Step 1: Classifying email from {email.customer_name}...")
        
        # Simple keyword-based classification (in real world, use AI/ML)
        body_lower = email.email_body.lower()
        
        if any(word in body_lower for word in ["bill", "payment", "charge", "invoice", "refund"]):
            category = "billing"
        elif any(word in body_lower for word in ["error", "bug", "crash", "not working", "help"]):
            category = "technical"
        else:
            category = "general"
        
        print(f"   ✓ Category assigned: {category.upper()}")
        
        # Pass classified email to next executor
        await ctx.send_message(ClassifiedEmail(
            customer_name=email.customer_name,
            email_body=email.email_body,
            category=category
        ))


# ============================================================================
# STEP 2: RESPONSE GENERATOR
# Creates an appropriate response based on the email category
# ============================================================================

@executor(id="response_generator")
async def generate_response(classified: ClassifiedEmail, ctx: WorkflowContext[DraftResponse]) -> None:
    """Generates a response draft based on the email category."""
    
    print(f"\n💬 Step 2: Generating response for {classified.category} inquiry...")
    
    # Category-specific response templates
    responses = {
        "billing": (
            f"Thank you for contacting us about your billing concern. "
            f"I've reviewed your account and will help resolve this. "
            f"Our billing team will process your request within 24 hours."
        ),
        "technical": (
            f"I understand you're experiencing a technical issue. "
            f"Let me help troubleshoot this problem. "
            f"Please try restarting the application. If the issue persists, "
            f"our technical team will investigate further."
        ),
        "general": (
            f"Thank you for reaching out to us! "
            f"We appreciate your message and are happy to assist. "
            f"A team member will follow up with more details soon."
        )
    }
    
    response_body = responses.get(classified.category, responses["general"])
    print(f"   ✓ Response draft created ({len(response_body)} characters)")
    
    # Pass draft to formatter
    await ctx.send_message(DraftResponse(
        customer_name=classified.customer_name,
        category=classified.category,
        response_body=response_body
    ))


# ============================================================================
# STEP 3: EMAIL FORMATTER
# Formats the final email with proper greeting, body, and signature
# ============================================================================

@executor(id="email_formatter")
async def format_email(draft: DraftResponse, ctx: WorkflowContext[Never, FinalResponse]) -> None:
    """Formats the draft into a professional email response."""
    
    print(f"\n📝 Step 3: Formatting final email...")
    
    # Build the formatted email
    formatted_body = f"""Dear {draft.customer_name},

{draft.response_body}

Best regards,
Customer Support Team
Acme Corporation

---
Category: {draft.category.upper()}
Reference: #CS-{hash(draft.customer_name) % 10000:04d}
"""
    
    subject_prefixes = {
        "billing": "Re: Your Billing Inquiry",
        "technical": "Re: Technical Support Request", 
        "general": "Re: Your Message"
    }
    
    final = FinalResponse(
        to=draft.customer_name,
        subject=subject_prefixes.get(draft.category, "Re: Your Inquiry"),
        body=formatted_body
    )
    
    print(f"   ✓ Email formatted with subject: {final.subject}")
    
    # Yield final output - this ends the workflow
    await ctx.yield_output(final)


# ============================================================================
# MAIN: Build and run the workflow
# ============================================================================

async def main():
    # Create executor instances
    classifier = EmailClassifier()
    
    # Build the sequential workflow pipeline
    # classifier → generate_response → format_email
    workflow = (
        WorkflowBuilder()
        .add_edge(classifier, generate_response)
        .add_edge(generate_response, format_email)
        .set_start_executor(classifier)
        .build()
    )
    
    
    # ========================================================================
    # WORKFLOW VISUALIZATION
    # ========================================================================
    print("="*70)
    print("📊 WORKFLOW VISUALIZATION")
    print("="*70)
    
    viz = WorkflowViz(workflow)
    
    # Print Mermaid diagram
    print("\n📌 Mermaid Diagram (copy/paste to https://mermaid.live):")
    print("-"*50)
    print(viz.to_mermaid())
    print("-"*50)
    
    # Export as image files
    print("\n📄 Exporting workflow diagrams...")
    try:
        svg_path = viz.save_svg("email_processing_workflow.svg")
        print(f"   ✅ SVG saved: {svg_path}")
        png_path = viz.save_png("email_processing_workflow.png")
        print(f"   ✅ PNG saved: {png_path}")
    except ImportError as e:
        print(f"   ⚠️ Could not export images: {e}")
    
    print()
    
    # Sample customer emails to process
    test_emails = [
        CustomerEmail(
            customer_name="John Smith",
            email_body="I was charged twice for my subscription last month. Please help with a refund."
        ),
        CustomerEmail(
            customer_name="Sarah Johnson", 
            email_body="The app keeps crashing when I try to upload files. This is very frustrating!"
        ),
        CustomerEmail(
            customer_name="Mike Wilson",
            email_body="I love your product! Just wanted to say thanks for the great service."
        ),
    ]
    
    # Process each email through the workflow
    for email in test_emails:
        print("\n" + "="*70)
        print(f"📨 PROCESSING EMAIL FROM: {email.customer_name}")
        print(f"   Message: {email.email_body[:50]}...")
        print("="*70)
        
        # Run workflow with streaming to see each step
        async for event in workflow.run_stream(email):
            if isinstance(event, WorkflowOutputEvent):
                final_email: FinalResponse = event.data
                print("\n" + "-"*70)
                print("✅ FINAL OUTPUT:")
                print("-"*70)
                print(f"To: {final_email.to}")
                print(f"Subject: {final_email.subject}")
                print(f"\n{final_email.body}")


if __name__ == "__main__":
    asyncio.run(main())
