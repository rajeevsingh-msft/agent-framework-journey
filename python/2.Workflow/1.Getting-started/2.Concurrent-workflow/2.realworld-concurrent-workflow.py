"""
Real-World Example: Product Price Comparison Engine

This workflow demonstrates a practical concurrent workflow that searches
multiple e-commerce sources in PARALLEL and aggregates the best prices.

    [Product Search Query]
              │
              ▼
    ┌─────────────────┐
    │   DISPATCHER    │  → Sends query to all price sources
    └────────┬────────┘
             │
    ─────────┼─────────  FAN-OUT (parallel)
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│ AMAZON │ │ EBAY   │ │ WALMART│  ← Run SIMULTANEOUSLY
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    ─────────┬─────────  FAN-IN (merge)
             │
             ▼
    ┌─────────────────┐
    │   AGGREGATOR    │  → Combines & ranks all results
    └────────┬────────┘
             │
             ▼
    [Best Price Results]

Why Concurrent Workflow?
- All price sources can be queried at the SAME TIME
- Total time = slowest source (not sum of all sources)
- Example: 3 sources × 2 sec each = 2 sec total (not 6 sec!)

No external services - uses simulated API responses for demo purposes.
"""

import asyncio
import random
import time
from dataclasses import dataclass
from typing_extensions import Never
from agent_framework import Executor, WorkflowBuilder, WorkflowContext, WorkflowOutputEvent, WorkflowViz, handler


# ============================================================================
# DATA MODELS - Define the shape of data flowing between executors
# ============================================================================

@dataclass
class ProductQuery:
    """Input: What product to search for"""
    product_name: str
    max_price: float | None = None


@dataclass
class PriceResult:
    """Result from a single price source"""
    source: str          # "Amazon", "eBay", "Walmart"
    product_name: str
    price: float
    in_stock: bool
    shipping: float
    url: str
    
    @property
    def total_price(self) -> float:
        return self.price + self.shipping


@dataclass
class AggregatedResults:
    """Final output: All prices sorted by best deal"""
    query: str
    results: list[PriceResult]
    best_deal: PriceResult | None
    search_time_ms: int


# ============================================================================
# DISPATCHER - Sends query to all price sources
# ============================================================================

class PriceDispatcher(Executor):
    """Dispatches the product query to all price source executors."""
    
    def __init__(self):
        super().__init__(id="price_dispatcher")
    
    @handler
    async def dispatch(self, query: ProductQuery, ctx: WorkflowContext[ProductQuery]) -> None:
        print(f"\n🔍 Searching for: '{query.product_name}'")
        print(f"   Max price filter: ${query.max_price}" if query.max_price else "   No price filter")
        print("\n   Querying all sources in PARALLEL...")
        
        # Send the same query to all connected executors (fan-out)
        await ctx.send_message(query)


# ============================================================================
# PRICE SOURCE EXECUTORS - Run in PARALLEL
# Each simulates an API call to a different e-commerce site
# ============================================================================

class AmazonPriceSource(Executor):
    """Fetches prices from Amazon (simulated)."""
    
    def __init__(self):
        super().__init__(id="amazon_source")
    
    @handler
    async def fetch_price(self, query: ProductQuery, ctx: WorkflowContext[PriceResult]) -> None:
        # Simulate API latency (1-3 seconds)
        delay = random.uniform(1.0, 3.0)
        await asyncio.sleep(delay)
        
        # Simulate price result
        base_price = random.uniform(80, 150)
        result = PriceResult(
            source="Amazon",
            product_name=query.product_name,
            price=round(base_price, 2),
            in_stock=random.choice([True, True, True, False]),  # 75% in stock
            shipping=0.0 if base_price > 35 else 5.99,  # Free shipping over $35
            url=f"https://amazon.com/dp/{random.randint(1000000, 9999999)}"
        )
        
        print(f"   ✓ Amazon responded in {delay:.1f}s - ${result.total_price:.2f}")
        await ctx.send_message(result)


class EbayPriceSource(Executor):
    """Fetches prices from eBay (simulated)."""
    
    def __init__(self):
        super().__init__(id="ebay_source")
    
    @handler
    async def fetch_price(self, query: ProductQuery, ctx: WorkflowContext[PriceResult]) -> None:
        # Simulate API latency
        delay = random.uniform(0.5, 2.5)
        await asyncio.sleep(delay)
        
        # Simulate price result (eBay often has lower base prices)
        base_price = random.uniform(60, 130)
        result = PriceResult(
            source="eBay",
            product_name=query.product_name,
            price=round(base_price, 2),
            in_stock=True,  # eBay always has something
            shipping=round(random.uniform(0, 12), 2),
            url=f"https://ebay.com/itm/{random.randint(100000000, 999999999)}"
        )
        
        print(f"   ✓ eBay responded in {delay:.1f}s - ${result.total_price:.2f}")
        await ctx.send_message(result)


class WalmartPriceSource(Executor):
    """Fetches prices from Walmart (simulated)."""
    
    def __init__(self):
        super().__init__(id="walmart_source")
    
    @handler
    async def fetch_price(self, query: ProductQuery, ctx: WorkflowContext[PriceResult]) -> None:
        # Simulate API latency
        delay = random.uniform(1.5, 3.5)
        await asyncio.sleep(delay)
        
        # Simulate price result (Walmart has competitive prices)
        base_price = random.uniform(70, 140)
        result = PriceResult(
            source="Walmart",
            product_name=query.product_name,
            price=round(base_price, 2),
            in_stock=random.choice([True, True, False]),  # 66% in stock
            shipping=0.0,  # Free shipping
            url=f"https://walmart.com/ip/{random.randint(10000000, 99999999)}"
        )
        
        print(f"   ✓ Walmart responded in {delay:.1f}s - ${result.total_price:.2f}")
        await ctx.send_message(result)


# ============================================================================
# AGGREGATOR - Collects all results and finds the best deal
# ============================================================================

class PriceAggregator(Executor):
    """Aggregates results from all price sources and ranks them."""
    
    def __init__(self):
        super().__init__(id="price_aggregator")
    
    @handler
    async def aggregate(
        self, 
        results: list[PriceResult], 
        ctx: WorkflowContext[Never, AggregatedResults]
    ) -> None:
        print(f"\n📊 Aggregating {len(results)} results...")
        
        # Sort by total price (price + shipping)
        sorted_results = sorted(results, key=lambda r: r.total_price)
        
        # Find best deal (lowest price that's in stock)
        in_stock_results = [r for r in sorted_results if r.in_stock]
        best_deal = in_stock_results[0] if in_stock_results else None
        
        # Create aggregated output
        aggregated = AggregatedResults(
            query=results[0].product_name if results else "Unknown",
            results=sorted_results,
            best_deal=best_deal,
            search_time_ms=0  # Would be calculated in real implementation
        )
        
        await ctx.yield_output(aggregated)


# ============================================================================
# MAIN: Build and run the concurrent workflow
# ============================================================================

async def main():
    # Create executor instances
    dispatcher = PriceDispatcher()
    amazon = AmazonPriceSource()
    ebay = EbayPriceSource()
    walmart = WalmartPriceSource()
    aggregator = PriceAggregator()
    
    # Build the concurrent workflow with fan-out/fan-in pattern
    # Pass executor instances directly (not lambdas)
    workflow = (
        WorkflowBuilder()
        .set_start_executor(dispatcher)
        # Fan-out: dispatcher sends to all price sources in parallel
        .add_fan_out_edges(dispatcher, [amazon, ebay, walmart])
        # Fan-in: all price sources feed into aggregator
        .add_fan_in_edges([amazon, ebay, walmart], aggregator)
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
        svg_path = viz.save_svg("price_comparison_workflow.svg")
        print(f"   ✅ SVG saved: {svg_path}")
        
        png_path = viz.save_png("price_comparison_workflow.png")
        print(f"   ✅ PNG saved: {png_path}")
        
        print("\n🖼️  Open the files to see your workflow diagram!")
    except ImportError as e:
        print(f"   ⚠️ Could not export images: {e}")
        print("   Install Graphviz from https://graphviz.org/download/")
    
    # Sample product searches
    test_queries = [
        ProductQuery(product_name="Sony WH-1000XM5 Headphones", max_price=350),
        ProductQuery(product_name="Apple AirPods Pro 2nd Gen"),
    ]
    
    # Process each search
    for query in test_queries:
        print("\n" + "="*70)
        print("🛒 PRODUCT PRICE COMPARISON")
        print("="*70)
        
        start_time = time.time()
        
        # Run workflow
        async for event in workflow.run_stream(query):
            if isinstance(event, WorkflowOutputEvent):
                result: AggregatedResults = event.data
                elapsed = time.time() - start_time
                
                print("\n" + "-"*70)
                print("💰 PRICE COMPARISON RESULTS")
                print("-"*70)
                print(f"Product: {result.query}")
                print(f"Total search time: {elapsed:.2f} seconds (PARALLEL!)")
                print()
                
                # Display all results
                print("All prices (sorted by total):")
                print("-" * 50)
                for i, r in enumerate(result.results, 1):
                    stock_status = "✅ In Stock" if r.in_stock else "❌ Out of Stock"
                    shipping_text = "FREE" if r.shipping == 0 else f"${r.shipping:.2f}"
                    print(f"{i}. {r.source:10} ${r.price:>7.2f} + {shipping_text:>6} shipping = ${r.total_price:>7.2f}  {stock_status}")
                
                # Display best deal
                if result.best_deal:
                    print()
                    print("🏆 BEST DEAL:")
                    print(f"   {result.best_deal.source} - ${result.best_deal.total_price:.2f}")
                    print(f"   URL: {result.best_deal.url}")
                else:
                    print("\n⚠️ No in-stock items found!")
                
                # Show time savings
                print()
                print(f"⏱️ Time Analysis:")
                print(f"   - Concurrent (actual): {elapsed:.2f} seconds")
                print(f"   - Sequential (would be): ~{elapsed * 3:.2f} seconds")
                print(f"   - Time saved: ~{elapsed * 2:.2f} seconds ({66:.0f}% faster!)")


if __name__ == "__main__":
    asyncio.run(main())
