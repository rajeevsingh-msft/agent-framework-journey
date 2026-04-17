import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../../../../.env", override=True)

# Remove API key from environment to force credential-based authentication
if "AZURE_OPENAI_API_KEY" in os.environ:
    del os.environ["AZURE_OPENAI_API_KEY"]

from agent_framework import AgentRunEvent, WorkflowBuilder, WorkflowViz
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

async def main():
    """Build and run a three-agent workflow: Researcher -> Writer -> Reviewer."""
    
    # Create the Azure chat client using credential authentication
    chat_client = AzureOpenAIChatClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        credential=AzureCliCredential(),
        deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )
    
    # Define specialized agents
    researcher_agent = chat_client.as_agent(
        instructions="""You are a research specialist.
        Gather comprehensive, factual information on the given topic.
        Provide sources and key insights.""",
        name="researcher",
    )
    
    writer_agent = chat_client.as_agent(
        instructions="""You are a content writer.
        Based on the research provided, write engaging, 
        well-structured content. Use clear language.""",
        name="writer",
    )
    
    reviewer_agent = chat_client.as_agent(
        instructions="""You are a content reviewer.
        Check for accuracy, clarity, and quality.
        Provide the final polished version.""",
        name="reviewer",
    )
    
    # Build the workflow using the fluent builder
    # Set the start node and connect edges: researcher -> writer -> reviewer
    workflow = (
        WorkflowBuilder()
        .set_start_executor(researcher_agent)
        .add_edge(researcher_agent, writer_agent)
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
        svg_path = viz.save_svg("researcher_writer_reviewer_workflow.svg")
        print(f"   ✅ SVG saved: {svg_path}")
        png_path = viz.save_png("researcher_writer_reviewer_workflow.png")
        print(f"   ✅ PNG saved: {png_path}")
    except ImportError as e:
        print(f"   ⚠️ Could not export images: {e}")
    
    print()
    
    # Run the workflow with the user's initial message
    print("="*60)
    print("🚀 RUNNING WORKFLOW")
    print("="*60)
    events = await workflow.run("Write a blog post about the benefits of AI agents in enterprise")
    
    # Collect and print agent run events with better formatting
    agent_outputs = []
    for event in events:
        if isinstance(event, AgentRunEvent):
            print(f"\n{'='*20} {event.executor_id.upper()} {'='*20}")
            print(event.data)
            agent_outputs.append(f"{event.executor_id}: {event.data}")
    
    print(f"\n{'=' * 60}")
    print("📝 WORKFLOW SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total agents executed: {len(agent_outputs)}")
    print(f"Workflow outputs: {events.get_outputs()}")
    
    # Print final polished content (last agent's output)
    if agent_outputs:
        print(f"\n{'=' * 60}")
        print("🏆 FINAL RESULT (from Reviewer)")
        print(f"{'=' * 60}")
        final_output = agent_outputs[-1].split(": ", 1)[1] if ": " in agent_outputs[-1] else agent_outputs[-1]
        print(final_output)
    
    # Summarize the final run state
    print(f"\n{'=' * 60}")
    print(f"✅ Final state: {events.get_final_state()}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    asyncio.run(main())

    