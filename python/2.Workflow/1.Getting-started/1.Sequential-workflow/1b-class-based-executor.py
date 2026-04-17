"""
Sequential Workflow using CLASS-BASED EXECUTORS

This example demonstrates the Class-based approach for creating executors.
Use this approach when you need:
- Lifecycle hooks
- Complex state management
- Dependency injection
- More control over initialization

Flow:
    Input: "hello world"
           ↓
    [UpperCase] → "HELLO WORLD"
           ↓
    [ReverseText] → "DLROW OLLEH"
           ↓
    Output
"""

import asyncio
from typing_extensions import Never
from agent_framework import WorkflowBuilder, WorkflowContext, WorkflowOutputEvent, WorkflowViz, Executor, handler


# ============================================================================
# EXECUTOR 1: UpperCase (Class-based)
# ============================================================================

class UpperCase(Executor):
    """Converts input text to uppercase.
    
    Class-based executors inherit from Executor and use @handler decorator
    to mark the method that processes input.
    """
    
    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def process(self, text: str, ctx: WorkflowContext[str]) -> None:
        """
        Handler method that processes input.
        
        Args:
            text: Input string from previous executor or workflow start
            ctx: WorkflowContext[str] - context to send string output to next executor
        """
        result = text.upper()
        print(f"[UpperCase] '{text}' → '{result}'")
        
        # Send result to next executor in the chain
        await ctx.send_message(result)


# ============================================================================
# EXECUTOR 2: ReverseText (Class-based)
# ============================================================================

class ReverseText(Executor):
    """Reverses the input text and yields final output.
    
    This is the terminal executor - it uses yield_output() instead of send_message()
    to return the final workflow result.
    """
    
    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def process(self, text: str, ctx: WorkflowContext[Never, str]) -> None:
        """
        Handler method for terminal executor.
        
        Args:
            text: Input string from previous executor
            ctx: WorkflowContext[Never, str]
                 - Never: this executor doesn't send to downstream nodes
                 - str: this executor yields string as final output
        """
        result = text[::-1]
        print(f"[ReverseText] '{text}' → '{result}'")
        
        # Yield final output (terminal executor)
        await ctx.yield_output(result)


# ============================================================================
# MAIN: Build and run the workflow
# ============================================================================

async def main():
    # Create executor instances
    upper_case = UpperCase(id="upper_case_executor")
    reverse_text = ReverseText(id="reverse_text_executor")
    
    # Build the workflow: upper_case → reverse_text
    workflow = (
        WorkflowBuilder()
        .add_edge(upper_case, reverse_text)
        .set_start_executor(upper_case)
        .build()
    )
    
    print("=" * 50)
    print("CLASS-BASED EXECUTOR EXAMPLE")
    print("=" * 50)
    print()
    
    # Visualization
    print("📊 Workflow Visualization:")
    viz = WorkflowViz(workflow)
    print(viz.to_mermaid())
    try:
        viz.save_svg("class_based_workflow.svg")
        viz.save_png("class_based_workflow.png")
        print("✅ Diagrams saved: class_based_workflow.svg/.png\n")
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
    CLASS-BASED EXECUTOR EXAMPLE
    ==================================================

    [UpperCase] 'hello world' → 'HELLO WORLD'
    [ReverseText] 'HELLO WORLD' → 'DLROW OLLEH'

    ✅ Final Result: DLROW OLLEH
    """


if __name__ == "__main__":
    asyncio.run(main())
