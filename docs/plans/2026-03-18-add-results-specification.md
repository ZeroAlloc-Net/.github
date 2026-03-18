# Design: Add ZeroAlloc.Results and ZeroAlloc.Specification to Profile README

## Summary

Update `profile/README.md` to:

1. Upgrade `ZeroAlloc.Results` and `ZeroAlloc.Specification` from "coming soon" to fully released entries (GitHub link + NuGet badge) in the packages table.
2. Add full body sections for each new library (description, code example, benchmark).
3. Add a speedup ratio column to the benchmark tables in the ValueObjects, Inject, and Mediator sections that currently lack one.

---

## Packages Table Changes

Upgrade these two rows from "coming soon" placeholders to released entries:

### ZeroAlloc.Results

```
| [ZeroAlloc.Results](https://github.com/ZeroAlloc-Net/ZeroAlloc.Results) | Zero-allocation `Result<T, E>` — no boxing, no heap pressure, full combinator API with async and LINQ support | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Results.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Results) |
```

### ZeroAlloc.Specification

```
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
```

---

## New Body Sections

Both sections are appended after the existing `ZeroAlloc.Validation` section.

### ZeroAlloc.Results

- **Description**: Zero-allocation, no-boxing `Result<T, E>` for .NET 9. All five types (`Result`, `Result<T>`, `Result<T,E>`, `UnitResult<E>`, `Maybe<T>`) are `readonly struct` — no heap allocation, no boxing, no GC pressure. Full combinator API: `Map`, `Bind`, `Match`, `Tap`, `Ensure`, `Combine`; all with `*Async` / `ValueTask` variants and LINQ query syntax.
- **Code example**: `Map` / `Ensure` / `Bind` / `Match` chain plus LINQ `from … select` form.
- **Benchmark**: Head-to-head vs CSharpFunctionalExtensions — 0 B allocated on both sides, ZeroAlloc up to **8.7× faster** on creation.

### ZeroAlloc.Specification

- **Description**: `[Specification]` attribute on a `readonly partial struct` implementing `ISpecification<T>`. The source generator emits `And<TOther>()`, `Or<TOther>()`, `Not()` fluent combinators — composed specs remain `readonly struct` values, zero heap allocation. Specs expose `ToExpression()` returning `Expression<Func<T, bool>>` for EF Core `Where()` translation. Two packages: `ZeroAlloc.Specification` (runtime) + `ZeroAlloc.Specification.Generator` (build-time generator). Compile-time diagnostics ZA001–ZA004 enforce correct usage.
- **Code example**: `ActiveUserSpec` and `PremiumUserSpec(decimal minSpend)` composed with `.And()`, used in-memory via `IsSatisfiedBy` and in EF Core via `Where(spec.ToExpression())`.
- **Benchmark**: Reference to [docs/performance.md](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification/blob/main/docs/performance.md); no inline numbers in the source README.

---

## Speedup Ratio Column — Existing Sections

Add a `Speedup` column to the three benchmark tables that currently lack one.

### ZeroAlloc.ValueObjects (vs CSharpFunctionalExtensions)

| Method | Mean | Allocated | Speedup vs CFE |
|---|---:|---:|:---:|
| CFE_Equals | 45.2 ns | 96 B | — |
| Record_Equals | 3.1 ns | 0 B | 14.6× |
| **ZeroAlloc_Equals** | **3.1 ns** | **0 B** | **~15×** |
| CFE_GetHashCode | 38.7 ns | 88 B | — |
| Record_GetHashCode | 2.4 ns | 0 B | 16.1× |
| **ZeroAlloc_GetHashCode** | **2.4 ns** | **0 B** | **~16×** |

### ZeroAlloc.Inject (vs Microsoft DI)

| Scenario | ZeroAlloc.Inject | Microsoft DI | Speedup |
|---|---|---|:---:|
| Resolve transient | ~3 ns | ~35 ns | **~12×** |
| Resolve singleton | ~1 ns | ~8 ns | **8×** |
| Open generic (closed at compile time) | ~19 ns | N/A (AOT unsafe) | — |

### ZeroAlloc.Mediator (vs MediatR)

| Scenario | ZeroAlloc.Mediator | MediatR | Speedup |
|---|---|---|:---:|
| Send | ~2 ns | ~88 ns | **44×** |
| Publish Single | ~6 ns | ~222 ns | **37×** |
| Publish Multi | ~5 ns | ~299 ns | **~60×** |

---

## Out of Scope

- No changes to Pipeline or Validation sections (already have Speedup column).
- No changes to Analyzers section (no comparison benchmark).
- "Coming soon" rows for Options and Mapping remain unchanged.
