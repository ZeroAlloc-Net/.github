# Add Pipeline and Validation to Profile README — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update `profile/README.md` to add `ZeroAlloc.Pipeline` and `ZeroAlloc.Validation` as released packages, reorder the table and body sections, and add full descriptive sections for each new library.

**Architecture:** Pure documentation edit — no code, no tests. All changes are in `profile/README.md`. Tasks are ordered by section position in the file (top-to-bottom) to avoid merge conflicts.

**Tech Stack:** Markdown, GitHub profile README conventions.

---

### Task 1: Reorder and update the packages table

**Files:**
- Modify: `profile/README.md` (packages table only)

**Step 1: Locate the table**

The table starts after `## Packages` and has 9 rows (Analyzers, Inject, Mediator, ValueObjects, then 5 coming-soon entries).

**Step 2: Replace the entire table**

Replace the existing table with this updated version (ValueObjects moved to row 2, Pipeline added after Mediator, Validation upgraded):

```markdown
| Package | Description | NuGet |
|---|---|---|
| [ZeroAlloc.Analyzers](https://github.com/ZeroAlloc-Net/ZeroAlloc.Analyzers) | Roslyn analyzers for modern .NET performance patterns | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Analyzers.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Analyzers) |
| [ZeroAlloc.ValueObjects](https://github.com/ZeroAlloc-Net/ZeroAlloc.ValueObjects) | Zero-allocation source-generated ValueObject equality for existing domain types | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.ValueObjects.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.ValueObjects) |
| [ZeroAlloc.Inject](https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject) | Compile-time dependency injection via Roslyn source generator | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Inject.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Inject) |
| [ZeroAlloc.Mediator](https://github.com/ZeroAlloc-Net/ZeroAlloc.Mediator) | Zero-allocation mediator library with source-generated dispatch | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Mediator.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Mediator) |
| [ZeroAlloc.Pipeline](https://github.com/ZeroAlloc-Net/ZeroAlloc.Pipeline) | Shared compile-time pipeline infrastructure — `IPipelineBehavior` interface and Roslyn discovery/emission utilities for ZeroAlloc generators | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Pipeline.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Pipeline) |
| [ZeroAlloc.Validation](https://github.com/ZeroAlloc-Net/ZeroAlloc.Validation) | Source-generated validation API — zero allocations, no reflection, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Validation.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Validation) |
| ZeroAlloc.Results *(coming soon)* | Zero-allocation source-generated discriminated union for result/error flow — no boxing, no `IEnumerable<Error>` | — |
| ZeroAlloc.Specification *(coming soon)* | Source-generated specifications — compile-time predicate composition, no closure allocations | — |
| ZeroAlloc.Options *(coming soon)* | Source-generated options validation — replaces data annotation reflection with compile-time generated validators | — |
| ZeroAlloc.Mapping *(coming soon)* | Source-generated object mapping — zero-allocation compile-time type mappings, no reflection | — |
```

**Step 3: Commit**

```bash
git add profile/README.md
git commit -m "docs: reorder packages table and add Pipeline + Validation entries"
```

---

### Task 2: Move ZeroAlloc.ValueObjects section before ZeroAlloc.Inject

**Files:**
- Modify: `profile/README.md` (body sections)

**Step 1: Locate the sections**

The body has four `---`-delimited sections in this order: Analyzers, Inject, Mediator, ValueObjects. The ValueObjects section starts at `## ZeroAlloc.ValueObjects` and ends just before the final `<p align="center">` footer.

**Step 2: Cut the ValueObjects section**

Remove the entire `---\n\n## ZeroAlloc.ValueObjects` block (from the `---` separator before it through its last line before the next `---` or footer).

**Step 3: Paste it after the Analyzers section**

Insert the ValueObjects section (with its leading `---`) between the Analyzers section and the Inject section.

The body order should now be: Analyzers → ValueObjects → Inject → Mediator.

**Step 4: Commit**

```bash
git add profile/README.md
git commit -m "docs: move ValueObjects section to after Analyzers"
```

---

### Task 3: Add ZeroAlloc.Pipeline section after Mediator

**Files:**
- Modify: `profile/README.md` (after Mediator section)

**Step 1: Locate the insertion point**

Find the `---` separator that follows the Mediator benchmark table (the one just before `## ZeroAlloc.ValueObjects`, which is now the next section after moving it).

**Step 2: Insert the Pipeline section**

Insert the following block between the Mediator section's closing `---` and the start of the ValueObjects section:

```markdown
---

## ZeroAlloc.Pipeline

Shared compile-time pipeline infrastructure for the ZeroAlloc ecosystem. Provides the `IPipelineBehavior` marker interface, `PipelineBehaviorAttribute`, and the Roslyn-based discovery and static-lambda-chain emission utilities that **ZeroAlloc.Mediator** and **ZeroAlloc.Validation** build on. All pipeline wiring is resolved at compile time — no reflection, no virtual dispatch, no heap allocation per call.

```csharp
using ZeroAlloc.Pipeline;

[PipelineBehavior(Order = 1)]
public class LoggingBehavior : IPipelineBehavior
{
    public static async ValueTask<TResponse> Handle<TRequest, TResponse>(
        TRequest request,
        CancellationToken ct,
        Func<TRequest, CancellationToken, ValueTask<TResponse>> next)
    {
        Console.WriteLine($"Handling {typeof(TRequest).Name}");
        var response = await next(request, ct);
        Console.WriteLine($"Handled {typeof(TRequest).Name}");
        return response;
    }
}

// Picked up at compile time by ZeroAlloc.Mediator or ZeroAlloc.Validation
// No registration, no reflection — wired into the generated pipeline automatically
```

**Benchmark** (i9-12900HK, .NET 10):

| Scenario | 1 behavior | 3 behaviors | 5 behaviors | Allocated |
|---|:---:|:---:|:---:|:---:|
| Static chain | 4.1 ns | 2.3 ns | 2.8 ns | **0 B** |
| Pre-built delegate chain | 2.2 ns | 9.9 ns | 17.6 ns | 0 B |
| Speedup | 0.5× | **4.3×** | **6.4×** | — |
```

**Step 3: Commit**

```bash
git add profile/README.md
git commit -m "docs: add ZeroAlloc.Pipeline section"
```

---

### Task 4: Add ZeroAlloc.Validation section after Pipeline

**Files:**
- Modify: `profile/README.md` (after Pipeline section)

**Step 1: Locate the insertion point**

Find the `---` separator at the end of the newly added Pipeline section (just before the ValueObjects section).

**Step 2: Insert the Validation section**

Insert the following block between the Pipeline section's closing `---` and the ValueObjects section:

```markdown
---

## ZeroAlloc.Validation

Attribute-based validation with a **source-generated strongly-typed validator** per model. The generator emits the validator class at build time — no reflection at runtime. On the valid path, the entire validation cycle produces zero heap allocations.

```csharp
using ZeroAlloc.Validation;

[Validate]
public class CreateOrderRequest
{
    [NotEmpty][MaxLength(50)] public string  Reference { get; set; } = "";
    [GreaterThan(0)]          public decimal Amount    { get; set; }
    [NotEmpty][EmailAddress]  public string  Email     { get; set; } = "";
}

// Source generator emits CreateOrderRequestValidator at build time
var validator = new CreateOrderRequestValidator();
var result    = validator.Validate(new CreateOrderRequest
{
    Reference = "ORD-2026-001",
    Amount    = 99.99m,
    Email     = "customer@example.com"
});

if (!result.IsValid)
    foreach (ref readonly var f in result.Failures)
        Console.WriteLine($"{f.PropertyName}: {f.ErrorMessage}");
```

**Benchmark** (i9-12900HK, .NET 10):

| Scenario | ZeroAlloc.Validation | FluentValidation | Speedup | Allocation (valid) |
|---|---:|---:|:---:|:---:|
| Flat model | 6.7 ns | 327 ns | ~49× | **0 B** |
| Nested model | 10.1 ns | 619 ns | ~61× | **0 B** |
| Collection (3×) | 14.3 ns | 2,043 ns | ~143× | **0 B** |
```

**Step 3: Commit**

```bash
git add profile/README.md
git commit -m "docs: add ZeroAlloc.Validation section"
```

---

### Task 5: Verify final README structure

**Step 1: Read the full README and verify section order**

Expected order:
1. Header / About / Design Philosophy
2. Packages table (Analyzers, ValueObjects, Inject, Mediator, Pipeline, Validation, 4× coming soon)
3. `## ZeroAlloc.Analyzers` section
4. `## ZeroAlloc.ValueObjects` section
5. `## ZeroAlloc.Inject` section
6. `## ZeroAlloc.Mediator` section
7. `## ZeroAlloc.Pipeline` section
8. `## ZeroAlloc.Validation` section
9. Footer

**Step 2: Check all NuGet badge URLs**

Confirm each released package row uses `https://img.shields.io/nuget/v/<PackageName>.svg?style=flat-square` and links to `https://www.nuget.org/packages/<PackageName>`.

**Step 3: Commit if any fixes were needed, otherwise note "no changes required"**
