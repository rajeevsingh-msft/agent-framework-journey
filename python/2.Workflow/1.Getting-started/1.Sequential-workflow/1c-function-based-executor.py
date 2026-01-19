"""
Sequential Workflow using FUNCTION-BASED EXECUTORS

This example demonstrates the Function-based approach for creating executors.
Use this approach when you need:
- Simple, stateless operations
- Quick prototyping
- Clean, minimal code
- No complex initialization required

Flow:
    Input: "hello world"
           ↓
    [upper_case] → "HELLO WORLD"
           ↓
    [reverse_text] → "DLROW OLLEH"
           ↓
    Output
"""

import asyncio
from typing_extensions import Never
from agent_framework import WorkflowBuilder, WorkflowContext, WorkflowOutputEvent, WorkflowViz, executor


# ============================================================================
# EXECUTOR 1: upper_case (Function-based)
# ============================================================================

@executor(id="upper_case_executor")
async def upper_case(text: str, ctx: WorkflowContext[str]) -> None:
    """
    Converts input text to uppercase.
    
    Function-based executors use the @executor decorator.
    Much simpler than class-based - just define an async function!
    
    Args:
        text: Input string from previous executor or workflow start
        ctx: WorkflowContext[str] - context to send string output to next executor
    """
    result = text.upper()
    print(f"[upper_case] '{text}' → '{result}'")
    
    # Send result to next executor in the chain
    await ctx.send_message(result)


# ============================================================================
# EXECUTOR 2: reverse_text (Function-based)
# ============================================================================

@executor(id="reverse_text_executor")
async def reverse_text(text: str, ctx: WorkflowContext[Never, str]) -> None:
    """
    Reverses the input text and yields final output.
    
    This is the terminal executor - it uses yield_output() instead of send_message()
    to return the final workflow result.
    
    Args:
        text: Input string from previous executor
        ctx: WorkflowContext[Never, str]
             - Never: this executor doesn't send to downstream nodes
             - str: this executor yields string as final output
    """
    result = text[::-1]
    print(f"[reverse_text] '{text}' → '{result}'")
    
    # Yield final output (terminal executor)
    await ctx.yield_output(result)


# ============================================================================
# MAIN: Build and run the workflow
# ============================================================================

async def main():
    # Build the workflow: upper_case → reverse_text
    # Note: No need to instantiate - functions are already executors!
    workflow = (
        WorkflowBuilder()
        .add_edge(upper_case, reverse_text)
        .set_start_executor(upper_case)
        .build()
    )
    
    print("=" * 50)
    print("FUNCTION-BASED EXECUTOR EXAMPLE")
    print("=" * 50)
    print()
    
    # Visualization
    print("📊 Workflow Visualization:")
    viz = WorkflowViz(workflow)
    print(viz.to_mermaid())
    try:
        viz.save_svg("function_based_workflow.svg")
        viz.save_png("function_based_workflow.png")
        print("✅ Diagrams saved: function_based_workflow.svg/.png\n")
    except ImportError as e:
        print(f"⚠️ Image export skipped: {e}\n")
    
    # Run workflow with streaming
    async for event in workflow.run_stream("hello world"):
        if isinstance(event, WorkflowOutputEvent):
            print()
            print(f"✅ Final Result: {event.data}")

    """
    Expected Output:
    
    ==================================================
    FUNCTION-BASED EXECUTOR EXAMPLE
    ==================================================

    [upper_case] 'hello world' → 'HELLO WORLD'
    [reverse_text] 'HELLO WORLD' → 'DLROW OLLEH'

    ✅ Final Result: DLROW OLLEH
    """


if __name__ == "__main__":
    asyncio.run(main())
