# Concurrent Workflow - Getting Started

## Overview

This folder contains sample programs that demonstrate **Concurrent Workflows** (also called Parallel Workflows) using the Microsoft Agent Framework. Concurrent workflows allow multiple executors to run **simultaneously**, enabling faster processing when steps are independent of each other.

| Sample | Description | Complexity |
|--------|-------------|------------|
| [1.create-concurrent-workflow.py](1.create-concurrent-workflow.py) | Fan-out/Fan-in pattern with parallel calculations | Beginner |
| [2.realworld-concurrent-workflow.py](2.realworld-concurrent-workflow.py) | Product price comparison across multiple sources | Intermediate |

---

## Prerequisites

### Required Packages

Install all dependencies from the root `requirements.txt` file:

```bash
pip install -r ../../../requirements.txt
```

### Python Version
- Python 3.10 or later

### No External AI Services Required
The samples use simple calculations and don't require any Azure/OpenAI API keys.

---

## Core Concepts

### What is a Concurrent Workflow?

A concurrent workflow allows **multiple executors to run in parallel** when they don't depend on each other's output. This is faster than sequential execution.

### Sequential vs Concurrent

```
SEQUENTIAL (one after another):
[Input] → [Step A] → [Step B] → [Step C] → [Output]
                Time: ████████████████████████

CONCURRENT (parallel execution):
              ┌→ [Step A] ─┐
[Input] → [Dispatcher] → [Step B] → [Aggregator] → [Output]
              └→ [Step C] ─┘
                Time: ████████████
```

**Concurrent is faster when steps are independent!**

### Fan-Out / Fan-In Pattern

The most common concurrent pattern:

```
┌────────────────────────────────────────────────────────────────────┐
│                     FAN-OUT / FAN-IN PATTERN                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   [Input Data]                                                     │
│        │                                                           │
│        ▼                                                           │
│   ┌────────────┐                                                   │
│   │ DISPATCHER │  ← Sends same input to multiple executors         │
│   └─────┬──────┘                                                   │
│         │                                                          │
│    ─────┼─────  FAN-OUT (split)                                    │
│    │    │    │                                                     │
│    ▼    ▼    ▼                                                     │
│   ┌──┐ ┌──┐ ┌──┐                                                   │
│   │A │ │B │ │C │  ← Run in PARALLEL                                │
│   └┬─┘ └┬─┘ └┬─┘                                                   │
│    │    │    │                                                     │
│    ─────┼─────  FAN-IN (merge)                                     │
│         │                                                          │
│         ▼                                                          │
│   ┌────────────┐                                                   │
│   │ AGGREGATOR │  ← Collects all results                           │
│   └─────┬──────┘                                                   │
│         │                                                          │
│         ▼                                                          │
│   [Combined Output]                                                │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Description |
|-----------|-------------|
| **Dispatcher** | Sends the same input to multiple executors (fan-out) |
| **Parallel Executors** | Independent workers that run simultaneously |
| **Aggregator** | Collects results from all parallel executors (fan-in) |
| `add_fan_out_edges()` | Connect one executor to multiple downstream executors |
| `add_fan_in_edges()` | Connect multiple executors to one downstream executor |

---

## Sample: Concurrent Calculation Workflow

**File:** `1.create-concurrent-workflow.py`

### What It Does

Takes a list of random numbers and calculates **Average** and **Sum** in parallel, then aggregates the results.

### Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│              CONCURRENT CALCULATION WORKFLOW                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Input: [45, 23, 67, 89, 12, 56, 34, 78, 91, 10]                   │
│                          │                                         │
│                          ▼                                         │
│   ┌────────────────────────────────────────┐                       │
│   │           DISPATCHER                   │                       │
│   │   Sends numbers to both calculators    │                       │
│   └──────────────┬─────────────────────────┘                       │
│                  │                                                 │
│         ┌───────┴────────┐   FAN-OUT                               │
│         │                │                                         │
│         ▼                ▼                                         │
│   ┌───────────┐    ┌───────────┐                                   │
│   │  AVERAGE  │    │    SUM    │   ← Run in PARALLEL               │
│   │           │    │           │                                   │
│   │ sum/len   │    │  sum()    │                                   │
│   │  = 50.5   │    │  = 505    │                                   │
│   └─────┬─────┘    └─────┬─────┘                                   │
│         │                │                                         │
│         └───────┬────────┘   FAN-IN                                │
│                 │                                                  │
│                 ▼                                                  │
│   ┌────────────────────────────────────────┐                       │
│   │           AGGREGATOR                   │                       │
│   │   Collects: [50.5, 505]                │                       │
│   └──────────────┬─────────────────────────┘                       │
│                  │                                                 │
│                  ▼                                                 │
│   Output: [50.5, 505]                                              │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Code Breakdown

#### 1. Dispatcher - Sends Input to Parallel Executors

```python
class Dispatcher(Executor):
    @handler
    async def handle(self, numbers: list[int], ctx: WorkflowContext[list[int]]):
        await ctx.send_message(numbers)  # Same input goes to ALL connected executors
```

#### 2. Parallel Executors - Run Simultaneously

```python
class Average(Executor):
    @handler
    async def handle(self, numbers: list[int], ctx: WorkflowContext[float]):
        average: float = sum(numbers) / len(numbers)
        await ctx.send_message(average)


class Sum(Executor):
    @handler
    async def handle(self, numbers: list[int], ctx: WorkflowContext[int]):
        total: int = sum(numbers)
        await ctx.send_message(total)
```

#### 3. Aggregator - Collects All Results

```python
class Aggregator(Executor):
    @handler
    async def handle(self, results: list[int | float], ctx: WorkflowContext[Never, list[int | float]]):
        # Framework automatically collects results as a list!
        await ctx.yield_output(results)
```

#### 4. Building the Workflow

```python
workflow = (
    WorkflowBuilder()
    .register_executor(lambda: Dispatcher(id="dispatcher"), name="dispatcher")
    .register_executor(lambda: Average(id="average"), name="average")
    .register_executor(lambda: Sum(id="summation"), name="summation")
    .register_executor(lambda: Aggregator(id="aggregator"), name="aggregator")
    .set_start_executor("dispatcher")
    .add_fan_out_edges("dispatcher", ["average", "summation"])  # Split
    .add_fan_in_edges(["average", "summation"], "aggregator")   # Merge
    .build()
)
```

### Running the Sample

```bash
cd python/2.Workflow/1.Getting-started/2.Concurrent-workflow
py 1.create-concurrent-workflow.py
```

### Expected Output

```
[50.5, 505]
```

*(The exact numbers will vary since random input is generated)*

---

## Sample 2: Real-World Price Comparison Engine

**File:** `2-realworld-concurrent-workflow.py`

### What It Does

A practical example that searches **3 e-commerce sources in PARALLEL** to find the best product price. This demonstrates how concurrent workflows dramatically reduce response time when querying multiple APIs.

### Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│              PRODUCT PRICE COMPARISON ENGINE                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   [ProductQuery]                                                   │
│   ├─ product_name: "Sony WH-1000XM5 Headphones"                    │
│   └─ max_price: $350                                               │
│                          │                                         │
│                          ▼                                         │
│   ┌────────────────────────────────────────┐                       │
│   │         PRICE DISPATCHER               │                       │
│   │   Sends query to all price sources     │                       │
│   └──────────────┬─────────────────────────┘                       │
│                  │                                                 │
│       ┌──────────┼──────────┐   FAN-OUT (parallel)                 │
│       │          │          │                                      │
│       ▼          ▼          ▼                                      │
│   ┌────────┐ ┌────────┐ ┌────────┐                                 │
│   │ AMAZON │ │  EBAY  │ │WALMART │   ← Run SIMULTANEOUSLY          │
│   │ ~2 sec │ │ ~1 sec │ │ ~2 sec │   (simulated API latency)       │
│   └───┬────┘ └───┬────┘ └───┬────┘                                 │
│       │          │          │                                      │
│       ▼          ▼          ▼                                      │
│   [PriceResult] [PriceResult] [PriceResult]                        │
│   ├─ $129.99   ├─ $89.50    ├─ $119.00                             │
│   ├─ FREE ship ├─ $6 ship   ├─ FREE ship                           │
│   └─ In Stock  └─ In Stock  └─ Out Stock                           │
│       │          │          │                                      │
│       └──────────┼──────────┘   FAN-IN (merge)                     │
│                  │                                                 │
│                  ▼                                                 │
│   ┌────────────────────────────────────────┐                       │
│   │         PRICE AGGREGATOR               │                       │
│   │   - Sorts by total price               │                       │
│   │   - Finds best in-stock deal           │                       │
│   │   - Calculates time savings            │                       │
│   └──────────────┬─────────────────────────┘                       │
│                  │                                                 │
│                  ▼                                                 │
│   [AggregatedResults]                                              │
│   ├─ Best Deal: eBay - $95.50                                      │
│   └─ Time: 2.8s (vs 8.4s sequential)                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Data Models (Data Flowing Between Steps)

```python
@dataclass
class ProductQuery:        # Input
    product_name: str
    max_price: float | None = None

@dataclass
class PriceResult:         # From each price source
    source: str            # "Amazon", "eBay", "Walmart"
    product_name: str
    price: float
    in_stock: bool
    shipping: float
    url: str

@dataclass
class AggregatedResults:   # Final Output
    query: str
    results: list[PriceResult]
    best_deal: PriceResult | None
    search_time_ms: int
```

### Code Breakdown

#### 1. Dispatcher - Sends Query to All Sources

```python
class PriceDispatcher(Executor):
    @handler
    async def dispatch(self, query: ProductQuery, ctx: WorkflowContext[ProductQuery]) -> None:
        print(f"🔍 Searching for: '{query.product_name}'")
        # Send the same query to all connected executors (fan-out)
        await ctx.send_message(query)
```

#### 2. Price Source Executors - Run in PARALLEL

Each source simulates an API call with random latency:

```python
class AmazonPriceSource(Executor):
    @handler
    async def fetch_price(self, query: ProductQuery, ctx: WorkflowContext[PriceResult]) -> None:
        # Simulate API latency (1-3 seconds)
        delay = random.uniform(1.0, 3.0)
        await asyncio.sleep(delay)
        
        # Create price result
        result = PriceResult(
            source="Amazon",
            product_name=query.product_name,
            price=round(random.uniform(80, 150), 2),
            in_stock=random.choice([True, True, True, False]),
            shipping=0.0 if price > 35 else 5.99,
            url=f"https://amazon.com/dp/{random.randint(1000000, 9999999)}"
        )
        await ctx.send_message(result)
```

*(Similar executors for eBay and Walmart)*

#### 3. Aggregator - Collects and Ranks Results

```python
class PriceAggregator(Executor):
    @handler
    async def aggregate(
        self, 
        results: list[PriceResult],  # Framework collects all results automatically!
        ctx: WorkflowContext[Never, AggregatedResults]
    ) -> None:
        # Sort by total price
        sorted_results = sorted(results, key=lambda r: r.total_price)
        
        # Find best in-stock deal
        in_stock = [r for r in sorted_results if r.in_stock]
        best_deal = in_stock[0] if in_stock else None
        
        await ctx.yield_output(AggregatedResults(
            query=results[0].product_name,
            results=sorted_results,
            best_deal=best_deal,
            search_time_ms=0
        ))
```

#### 4. Building the Workflow

```python
workflow = (
    WorkflowBuilder()
    .register_executor(lambda: dispatcher, name="dispatcher")
    .register_executor(lambda: amazon, name="amazon")
    .register_executor(lambda: ebay, name="ebay")
    .register_executor(lambda: walmart, name="walmart")
    .register_executor(lambda: aggregator, name="aggregator")
    .set_start_executor("dispatcher")
    # Fan-out: dispatcher sends to all price sources
    .add_fan_out_edges("dispatcher", ["amazon", "ebay", "walmart"])
    # Fan-in: all price sources feed into aggregator
    .add_fan_in_edges(["amazon", "ebay", "walmart"], "aggregator")
    .build()
)
```

### Running the Sample

```bash
cd python/2.Workflow/1.Getting-started/2.Concurrent-workflow
py 2a-realworld-concurrent-workflow.py
```

### Expected Output

```
======================================================================
🛒 PRODUCT PRICE COMPARISON
======================================================================

🔍 Searching for: 'Sony WH-1000XM5 Headphones'
   Max price filter: $350

   Querying all sources in PARALLEL...
   ✓ eBay responded in 1.2s - $95.50
   ✓ Amazon responded in 2.1s - $129.99
   ✓ Walmart responded in 2.8s - $119.00

----------------------------------------------------------------------
💰 PRICE COMPARISON RESULTS
----------------------------------------------------------------------
Product: Sony WH-1000XM5 Headphones
Total search time: 2.82 seconds (PARALLEL!)

All prices (sorted by total):
--------------------------------------------------
1. eBay       $  89.50 +  $6.00 shipping = $  95.50  ✅ In Stock
2. Walmart    $ 119.00 +   FREE shipping = $ 119.00  ✅ In Stock
3. Amazon     $ 129.99 +   FREE shipping = $ 129.99  ❌ Out of Stock

🏆 BEST DEAL:
   eBay - $95.50
   URL: https://ebay.com/itm/123456789

⏱️ Time Analysis:
   - Concurrent (actual): 2.82 seconds
   - Sequential (would be): ~8.46 seconds
   - Time saved: ~5.64 seconds (66% faster!)
```

### Understanding the Output

| Step | What Happens | Time |
|------|--------------|------|
| Dispatcher | Sends query to 3 sources | Instant |
| Amazon, eBay, Walmart | All query **simultaneously** | ~1-3 sec each |
| Total parallel time | Equals **slowest** source | ~2.8 sec |
| Sequential would be | Sum of all sources | ~8.4 sec |
| **Time saved** | 66% faster! | ~5.6 sec |

### Why This Example Matters

This is exactly how real price comparison sites (Google Shopping, PriceGrabber) work:
- They query multiple sources **in parallel**
- User gets results in ~2-3 seconds instead of ~10+ seconds
- The pattern scales: add more sources without increasing wait time

---

## Key Differences: Sequential vs Concurrent

| Aspect | Sequential | Concurrent |
|--------|------------|------------|
| **Execution** | One step at a time | Multiple steps at once |
| **Speed** | Slower (sum of all step times) | Faster (max of parallel step times) |
| **Dependencies** | Each step needs previous output | Parallel steps are independent |
| **Edge Type** | `add_edge(A, B)` | `add_fan_out_edges()` / `add_fan_in_edges()` |
| **Use Case** | Pipeline processing | Parallel data fetching/processing |

### Time Comparison Example

```
Scenario: 3 API calls, each takes 2 seconds

SEQUENTIAL:
  API 1 ──────> API 2 ──────> API 3
  [  2s  ]     [  2s  ]     [  2s  ]
  Total: 6 seconds

CONCURRENT:
  API 1 ──────>
  API 2 ──────>  (all at same time)
  API 3 ──────>
  [     2s     ]
  Total: 2 seconds (3x faster!)
```

---

## Real-World Use Cases for Concurrent Workflows

### 1. Multi-Source Data Aggregation

```
[User Query] → [Dispatcher]
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   [Database]  [Cache API]  [External API]
        │           │           │
        └───────────┼───────────┘
                    ▼
              [Aggregator] → [Combined Response]
```

**Example:** Dashboard loading multiple data sources simultaneously

### 2. Parallel AI Model Inference

```
[Image] → [Dispatcher]
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
[Object     [Face      [Text
Detection]  Recognition] Extraction]
    │          │          │
    └──────────┼──────────┘
               ▼
         [Aggregator] → [Combined Analysis]
```

**Example:** Image analysis with multiple AI models

### 3. Multi-Language Translation

```
[Source Text] → [Dispatcher]
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   [Translate    [Translate   [Translate
    to French]    to Spanish]  to German]
        │            │            │
        └────────────┼────────────┘
                     ▼
               [Aggregator] → [All Translations]
```

**Example:** Translate content to multiple languages at once

### 4. Parallel Document Processing

```
[Document Batch] → [Dispatcher]
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
    [Process       [Process       [Process
     Doc 1]         Doc 2]         Doc 3]
         │              │              │
         └──────────────┼──────────────┘
                        ▼
                  [Aggregator] → [All Results]
```

**Example:** Processing multiple documents in parallel

### 5. Multi-Region Health Check

```
[Health Check] → [Dispatcher]
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
  [US East]      [EU West]     [Asia Pacific]
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                [Aggregator] → [Status Report]
```

**Example:** Check service health across multiple regions

---

## When to Use Concurrent vs Other Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| **Sequential** | Steps depend on previous output | Document processing pipeline |
| **Concurrent** | Steps are independent, can run in parallel | Multi-API data fetching |
| **Branching** | Different paths based on conditions | Approval routing |
| **Hybrid** | Mix of sequential and concurrent | Complex data pipelines |

---

## Key Takeaways

1. **Concurrent = Parallel Execution**: Multiple executors run at the same time
2. **Fan-Out/Fan-In Pattern**: Dispatcher splits work, Aggregator collects results
3. **Faster Processing**: When steps are independent, concurrent is much faster
4. **Automatic Result Collection**: Framework collects parallel results as a list
5. **Use `add_fan_out_edges()`/`add_fan_in_edges()`**: Special methods for parallel connections

---

## Next Steps

- [3. Agents in Workflow](../3.Agents-in-Workflow/Readme.md) - Add AI agents to workflows

---

## References

- [Agent Framework - Concurrent Workflow Tutorial](https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/simple-concurrent-workflow)
- [Agent Framework - Workflow Core Concepts](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/workflows)
- [Agent Framework - Edges](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges)
- [Azure Durable Functions - Fan-out/Fan-in](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-cloud-backup)
- [Parallel Processing Patterns](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/task-parallel-library-tpl)
