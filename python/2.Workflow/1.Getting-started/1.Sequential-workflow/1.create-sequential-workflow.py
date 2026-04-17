import asyncio
from typing_extensions import Never
from agent_framework import WorkflowBuilder, WorkflowContext, WorkflowOutputEvent, WorkflowViz, executor, Executor, handler


"""
Step 1: Foundational patterns: Executors and edges

What this example shows
- Two ways to define a unit of work (an Executor node):
    1) Custom class that subclasses Executor with an async method marked by @handler.
         Possible handler signatures:
            - (text: str, ctx: WorkflowContext) -> None,
            - (text: str, ctx: WorkflowContext[str]) -> None, or
            - (text: str, ctx: WorkflowContext[Never, str]) -> None.
         The first parameter is the typed input to this node, the input type is str here.
         The second parameter is a WorkflowContext[T_Out, T_W_Out].
         WorkflowContext[T_Out] is used for nodes that send messages to downstream nodes with ctx.send_message(T_Out).
         WorkflowContext[T_Out, T_W_Out] is used for nodes that also yield workflow
            output with ctx.yield_output(T_W_Out).
         WorkflowContext without type parameters is equivalent to WorkflowContext[Never, Never], meaning this node
            neither sends messages to downstream nodes nor yields workflow output.

    2) Standalone async function decorated with @executor using the same signature.
         Simple steps can use this form; a terminal step can yield output
         using ctx.yield_output() to provide workflow results.

- Fluent WorkflowBuilder API:
    add_edge(A, B) to connect nodes, set_start_executor(A), then build() -> Workflow.

- Running and results:
    workflow.run(initial_input) executes the graph. Terminal nodes yield
    outputs using ctx.yield_output(). The workflow runs until idle.

Prerequisites
- No external services required.
"""


# Example 1: A custom Executor subclass
# ------------------------------------
#
# Subclassing Executor lets you define a named node with lifecycle hooks if needed.
# The work itself is implemented in an async method decorated with @handler.
#
# Handler signature contract:
# - First parameter is the typed input to this node (here: text: str)
# - Second parameter is a WorkflowContext[T_Out], where T_Out is the type of data this
#   node will emit via ctx.send_message (here: T_Out is str)
#
# Within a handler you typically:
# - Compute a result
# - Forward that result to downstream node(s) using ctx.send_message(result)
class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert the input to uppercase and forward it to the next node.

        Note: The WorkflowContext is parameterized with the type this handler will
        emit. Here WorkflowContext[str] means downstream nodes should expect str.
        """
        result = text.upper()

        # Send the result to the next executor in the workflow.
        await ctx.send_message(result)


# Example 2: A standalone function-based executor
# -----------------------------------------------
#
# For simple steps you can skip subclassing and define an async function with the
# same signature pattern (typed input + WorkflowContext[T_Out, T_W_Out]) and decorate it with
# @executor. This creates a fully functional node that can be wired into a flow.


@executor(id="reverse_text_executor")
async def reverse_text(text: str, ctx: WorkflowContext[Never, str]) -> None:
    """Reverse the input string and yield the workflow output.

    This node yields the final output using ctx.yield_output(result).
    The workflow will complete when it becomes idle (no more work to do).

    The WorkflowContext is parameterized with two types:
    - T_Out = Never: this node does not send messages to downstream nodes.
    - T_W_Out = str: this node yields workflow output of type str.
    """
    result = text[::-1]

    # Yield the output - the workflow will complete when idle
    await ctx.yield_output(result)


async def main():
    """Build and run a simple 2-step workflow using the fluent builder API."""

    upper_case = UpperCase(id="upper_case_executor")

    # Build the workflow using a fluent pattern:
    # 1) add_edge(from_node, to_node) defines a directed edge upper_case -> reverse_text
    # 2) set_start_executor(node) declares the entry point
    # 3) build() finalizes and returns an immutable Workflow object
    workflow = (
        WorkflowBuilder()
        .add_edge(upper_case, reverse_text)
        .set_start_executor(upper_case)
        .build()
    )

    # ========================================================================
    # WORKFLOW VISUALIZATION
    # ========================================================================
    print("="*70)
    print("📊 WORKFLOW VISUALIZATION")
    print("="*70)
    
    viz = WorkflowViz(workflow)
    
    # Option 1: Print Mermaid diagram (paste into mermaid.live or GitHub markdown)
    print("\n📌 Mermaid Diagram (copy/paste to https://mermaid.live):")
    print("-"*50)
    print(viz.to_mermaid())
    print("-"*50)
    
    # Option 2: Export as image files (requires graphviz binaries installed)
    print("\n📄 Exporting workflow diagrams...")
    try:
        svg_path = viz.save_svg("sequential_workflow.svg")
        print(f"   ✅ SVG saved: {svg_path}")
        
        png_path = viz.save_png("sequential_workflow.png")
        print(f"   ✅ PNG saved: {png_path}")
        
        print("\n🖼️  Open the files to see your workflow diagram!")
    except ImportError as e:
        print(f"   ⚠️ Could not export images: {e}")
        print("   Install Graphviz from https://graphviz.org/download/")
    
    print("\n" + "="*70)

    # Run the workflow with streaming to observe events in real-time
    async for event in workflow.run_stream("hello world"):
        print(f"Event: {event}")
        if isinstance(event, WorkflowOutputEvent):
            print(f"Workflow completed with result: {event.data}")

    """
    Sample Output:

    Event: ExecutorInvokedEvent(executor_id=upper_case_executor)
    Event: ExecutorCompletedEvent(executor_id=upper_case_executor)
    Event: ExecutorInvokedEvent(executor_id=reverse_text_executor)
    Event: ExecutorCompletedEvent(executor_id=reverse_text_executor)
    Event: WorkflowOutputEvent(data='DLROW OLLEH', source_executor_id=reverse_text_executor)
    Workflow completed with result: DLROW OLLEH
    """


if __name__ == "__main__":
    asyncio.run(main())