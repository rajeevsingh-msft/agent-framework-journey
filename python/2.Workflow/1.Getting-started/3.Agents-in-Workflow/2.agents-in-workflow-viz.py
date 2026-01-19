#https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/_start-here/step2_agents_in_a_workflow.py
#https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/agents-in-workflows?pivots=programming-language-python

# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file (override system env vars)
load_dotenv(dotenv_path="../../../../.env", override=True)

# Remove API key from environment to force credential-only authentication
if "AZURE_OPENAI_API_KEY" in os.environ:
    del os.environ["AZURE_OPENAI_API_KEY"]

# Enable Azure SDK logging for debugging authentication
os.environ["AZURE_LOG_LEVEL"] = "INFO"

print(f"🔍 AZURE_OPENAI_ENDPOINT: {os.environ.get('AZURE_OPENAI_ENDPOINT', 'NOT SET')}")
print(f"🔍 AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: {os.environ.get('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME', 'NOT SET')}")
print(f"🔍 AZURE_OPENAI_API_KEY present: {'AZURE_OPENAI_API_KEY' in os.environ}")
print("=" * 60)

from agent_framework import AgentRunEvent, WorkflowBuilder, WorkflowViz
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential, AzureCliCredential

"""
Step 2: Agents in a Workflow non-streaming

This sample uses two custom executors. A Writer agent creates or edits content,
then hands the conversation to a Reviewer agent which evaluates and finalizes the result.

Purpose:
Show how to wrap chat agents created by AzureOpenAIChatClient inside workflow executors. Demonstrate how agents
automatically yield outputs when they complete, removing the need for explicit completion events.
The workflow completes when it becomes idle.

Prerequisites:
- Azure OpenAI configured for AzureOpenAIChatClient with required environment variables.
- Authentication via azure-identity. Use AzureCliCredential and run az login before executing the sample.
- Basic familiarity with WorkflowBuilder, executors, edges, events, and streaming or non streaming runs.
"""


async def main():
    """Build and run a simple two node agent workflow: Writer then Reviewer."""
    # Create the Azure chat client using Azure credentials (since API key auth is disabled)
    print("🔐 Creating AzureOpenAIChatClient with AzureCliCredential...")
    
    # Use AzureCliCredential since API key authentication is disabled for this resource
    credential = AzureCliCredential()
    
    chat_client = AzureOpenAIChatClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        credential=credential,
        deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )
    writer_agent = chat_client.as_agent(
        instructions=(
            "You are an excellent content writer. You create new content and edit contents based on the feedback."
        ),
        name="writer",
    )
    reviewer_agent = chat_client.as_agent(
        instructions=(
            "You are an excellent content reviewer."
            "Provide actionable feedback to the writer about the provided content."
            "Provide the feedback in the most concise manner possible."
        ),
        name="reviewer",
    )
    # Build the workflow using the fluent builder.
    # Set the start node and connect an edge from writer to reviewer.
    workflow = (
        WorkflowBuilder()
        .set_start_executor(writer_agent)
        .add_edge(writer_agent, reviewer_agent)
        .build()
    )

    # ========================================================================
    # WORKFLOW VISUALIZATION
    # ========================================================================
    print("="*60)
    print("📊 WORKFLOW VISUALIZATION")
    print("="*60)
    
    viz = WorkflowViz(workflow)
    
    # Print Mermaid diagram
    print("\n📌 Mermaid Diagram (copy/paste to https://mermaid.live):")
    print("-"*50)
    print(viz.to_mermaid())
    print("-"*50)
    
    # Export as image files
    print("\n📄 Exporting workflow diagrams...")
    try:
        svg_path = viz.save_svg("agents_workflow.svg")
        print(f"   ✅ SVG saved: {svg_path}")
        png_path = viz.save_png("agents_workflow.png")
        print(f"   ✅ PNG saved: {png_path}")
    except ImportError as e:
        print(f"   ⚠️ Could not export images: {e}")
    
    print()
    
    # Run the workflow with the user's initial message.
    # For foundational clarity, use run (non streaming) and print the terminal event.
    events = await workflow.run("Create a slogan for a new electric SUV that is affordable and fun to drive.")
    # Print agent run events and final outputs
    for event in events:
        if isinstance(event, AgentRunEvent):
            print(f"{event.executor_id}: {event.data}")

    print(f"{'=' * 60}\nWorkflow Outputs: {events.get_outputs()}")
    # Summarize the final run state (e.g., COMPLETED)
    print("Final state:", events.get_final_state())

    """
    Sample Output:

    writer: "Charge Up Your Adventure—Affordable Fun, Electrified!"
    reviewer: Slogan: "Plug Into Fun—Affordable Adventure, Electrified."

    **Feedback:**
    - Clear focus on affordability and enjoyment.
    - "Plug into fun" connects emotionally and highlights electric nature.
    - Consider specifying "SUV" for clarity in some uses.
    - Strong, upbeat tone suitable for marketing.
    ============================================================
    Workflow Outputs: ['Slogan: "Plug Into Fun—Affordable Adventure, Electrified."

    **Feedback:**
    - Clear focus on affordability and enjoyment.
    - "Plug into fun" connects emotionally and highlights electric nature.
    - Consider specifying "SUV" for clarity in some uses.
    - Strong, upbeat tone suitable for marketing.']
    """


if __name__ == "__main__":
    asyncio.run(main())