# Add ZeroAlloc.Results and ZeroAlloc.Specification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update `profile/README.md` to upgrade Results and Specification from "coming soon" to released packages, add full body sections for each, and add speedup ratio columns to the ValueObjects, Inject, and Mediator benchmark tables.

**Architecture:** All changes are to a single markdown file (`profile/README.md`). No code, no tests. Each task is one focused edit followed by a commit.

**Tech Stack:** Markdown, git.

---

### Task 1: Upgrade Results and Specification rows in the packages table

**Files:**
- Modify: `profile/README.md:33-34`

**Step 1: Replace the two "coming soon" rows**

Find (lines 33–34):
```
| ZeroAlloc.Results *(coming soon)* | Zero-allocation source-generated discriminated union for result/error flow — no boxing, no `IEnumerable<Error>` | — |
| ZeroAlloc.Specification *(coming soon)* | Source-generated specifications — compile-time predicate composition, no closure allocations | — |
```

Replace with:
```
| [ZeroAlloc.Results](https://github.com/ZeroAlloc-Net/ZeroAlloc.Results) | Zero-allocation `Result<T, E>` — no boxing, no heap pressure, full combinator API with async and LINQ support | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Results.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Results) |
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
```

**Step 2: Commit**

```bash
git add profile/README.md
git commit -m "docs: upgrade Results and Specification rows in packages table"
```

---

### Task 2: Add speedup column to ValueObjects benchmark table

**Files:**
- Modify: `profile/README.md:85-92`

**Step 1: Replace the benchmark table**

Find (lines 85–92):
```markdown
| Method | Mean | Allocated |
|---|---:|---:|
| CFE_Equals | 45.2 ns | 96 B |
| Record_Equals | 3.1 ns | 0 B |
| **ZeroAlloc_Equals** | **3.1 ns** | **0 B** |
| CFE_GetHashCode | 38.7 ns | 88 B |
| Record_GetHashCode | 2.4 ns | 0 B |
| **ZeroAlloc_GetHashCode** | **2.4 ns** | **0 B** |
```

Replace with:
```markdown
| Method | Mean | Allocated | Speedup vs CFE |
|---|---:|---:|:---:|
| CFE_Equals | 45.2 ns | 96 B | — |
| Record_Equals | 3.1 ns | 0 B | 14.6× |
| **ZeroAlloc_Equals** | **3.1 ns** | **0 B** | **~15×** |
| CFE_GetHashCode | 38.7 ns | 88 B | — |
| Record_GetHashCode | 2.4 ns | 0 B | 16.1× |
| **ZeroAlloc_GetHashCode** | **2.4 ns** | **0 B** | **~16×** |
```

**Step 2: Commit**

```bash
git add profile/README.md
git commit -m "docs: add speedup column to ValueObjects benchmark table"
```

---

### Task 3: Add speedup column to Inject benchmark table

**Files:**
- Modify: `profile/README.md:118-122`

**Step 1: Replace the benchmark table**

Find (lines 118–122):
```markdown
| Scenario | ZeroAlloc.Inject | Microsoft DI |
|---|---|---|
| Resolve transient | ~3 ns | ~35 ns |
| Resolve singleton | ~1 ns | ~8 ns |
| Open generic (closed at compile time) | ~19 ns | N/A (AOT unsafe) |
```

Replace with:
```markdown
| Scenario | ZeroAlloc.Inject | Microsoft DI | Speedup |
|---|---|---|:---:|
| Resolve transient | ~3 ns | ~35 ns | **~12×** |
| Resolve singleton | ~1 ns | ~8 ns | **8×** |
| Open generic (closed at compile time) | ~19 ns | N/A (AOT unsafe) | — |
```

**Step 2: Commit**

```bash
git add profile/README.md
git commit -m "docs: add speedup column to Inject benchmark table"
```

---

### Task 4: Add speedup column to Mediator benchmark table

**Files:**
- Modify: `profile/README.md:181-185`

**Step 1: Replace the benchmark table**

Find (lines 181–185):
```markdown
| Scenario | ZeroAlloc.Mediator | MediatR |
|---|---|---|
| Send | ~2 ns | ~88 ns |
| Publish Single | ~6 ns | ~222 ns |
| Publish Multi | ~5 ns | ~299 ns |
```

Replace with:
```markdown
| Scenario | ZeroAlloc.Mediator | MediatR | Speedup |
|---|---|---|:---:|
| Send | ~2 ns | ~88 ns | **44×** |
| Publish Single | ~6 ns | ~222 ns | **37×** |
| Publish Multi | ~5 ns | ~299 ns | **~60×** |
```

**Step 2: Commit**

```bash
git add profile/README.md
git commit -m "docs: add speedup column to Mediator benchmark table"
```

---

### Task 5: Add ZeroAlloc.Results body section

**Files:**
- Modify: `profile/README.md` — insert before the closing footer (before line 228 `<p align="center">`)

**Step 1: Insert the Results section**

Find the closing footer block:
```markdown
<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

Insert before it:
```markdown
## ZeroAlloc.Results

Zero-allocation, no-boxing `Result<T, E>` for .NET 9. All five types — `Result`, `Result<T>`, `Result<T,E>`, `UnitResult<E>`, and `Maybe<T>` — are `readonly struct` values. No heap allocation, no boxing, no GC pressure. Full combinator API: `Map`, `Bind`, `Match`, `Tap`, `Ensure`, `Combine`, each with a `*Async` / `ValueTask` variant, plus LINQ query syntax via `Select` and `SelectMany`.

```csharp
using ZeroAlloc.Results;
using ZeroAlloc.Results.Extensions;

// Chain combinators
var result = GetUser(id)
    .Ensure(u => u.IsActive, "user is inactive")
    .Map(u => u.Email)
    .Bind(email => SendWelcome(email));

// Extract with Match
string message = result.Match(
    onSuccess: email => $"Sent to {email}",
    onFailure: err  => $"Failed: {err}");

// LINQ query syntax
var greeting =
    from user    in GetUser(id)
    from profile in GetProfile(user)
    select $"Hello, {profile.Name}";

// Async pipelines
var response = await GetUser(id)
    .MapAsync(async u  => await LoadPermissions(u))
    .BindAsync(async p => await BuildToken(p));
```

**Benchmark** (Windows 11, i9-12900HK, .NET 9 — vs [CSharpFunctionalExtensions](https://github.com/vkhorikov/CSharpFunctionalExtensions) 3.7.0):

| Category | ZeroAlloc.Results | CSharpFunctionalExtensions | Allocated | Speedup |
|---|---:|---:|:---:|:---:|
| `Create_Success` | 0.33 ns | 2.89 ns | **0 B** both | **8.7×** |
| `Create_Failure` | 0.30 ns | 1.44 ns | **0 B** both | **4.8×** |
| `Map` | 1.09 ns | 1.48 ns | **0 B** both | **1.4×** |
| `Match` | 0.37 ns | 0.68 ns | **0 B** both | **1.9×** |
| `Chain` (Map+Bind+Match) | 2.28 ns | 2.45 ns | **0 B** both | **1.1×** |

---

```

**Step 2: Commit**

```bash
git add profile/README.md
git commit -m "docs: add ZeroAlloc.Results section"
```

---

### Task 6: Add ZeroAlloc.Specification body section

**Files:**
- Modify: `profile/README.md` — insert between the Results `---` divider and the closing footer

**Step 1: Insert the Specification section**

Find the closing footer block (now directly after the Results `---`):
```markdown
<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

Insert before it:
```markdown
## ZeroAlloc.Specification

Source-generated specification pattern for .NET 8+. Decorate a `readonly partial struct` with `[Specification]` — the Roslyn generator emits `And<TOther>()`, `Or<TOther>()`, and `Not()` fluent combinators. Composed specs stay `readonly struct` values: zero heap allocation, no closures. Every spec exposes `ToExpression()` returning `Expression<Func<T, bool>>` for direct use with EF Core `Where()`. Two packages: `ZeroAlloc.Specification` (runtime) + `ZeroAlloc.Specification.Generator` (build-time generator). Compile-time diagnostics ZA001–ZA004 enforce correct usage.

```bash
dotnet add package ZeroAlloc.Specification
dotnet add package ZeroAlloc.Specification.Generator
```

```csharp
[Specification]
public readonly partial struct ActiveUserSpec : ISpecification<User>
{
    public bool IsSatisfiedBy(User user) => user.IsActive;
    public Expression<Func<User, bool>> ToExpression() => u => u.IsActive;
}

[Specification]
public readonly partial struct PremiumUserSpec : ISpecification<User>
{
    private readonly decimal _minSpend;
    public PremiumUserSpec(decimal minSpend) => _minSpend = minSpend;

    public bool IsSatisfiedBy(User user) => user.TotalSpend >= _minSpend;
    public Expression<Func<User, bool>> ToExpression()
    {
        var min = _minSpend;
        return u => u.TotalSpend >= min;
    }
}

// Fluent composition — zero allocation, composed type is still a readonly struct
var spec = new ActiveUserSpec().And(new PremiumUserSpec(1000m));

// In-memory
bool qualifies = spec.IsSatisfiedBy(user);

// EF Core — translates to SQL
var users = await dbContext.Users.Where(spec.ToExpression()).ToListAsync();
```

---

```

**Step 2: Commit**

```bash
git add profile/README.md
git commit -m "docs: add ZeroAlloc.Specification section"
```
