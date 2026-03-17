# Design: Add ZeroAlloc.Pipeline and ZeroAlloc.Validation to Profile README

## Summary

Update `profile/README.md` to add `ZeroAlloc.Pipeline` and `ZeroAlloc.Validation` as fully released packages, reorder the packages table to reflect dependency relationships, and add full sections for each new library.

## Table Order (final)

1. ZeroAlloc.Analyzers
2. ZeroAlloc.ValueObjects *(moved up from position 4)*
3. ZeroAlloc.Inject
4. ZeroAlloc.Mediator
5. ZeroAlloc.Pipeline *(new)*
6. ZeroAlloc.Validation *(upgraded from "coming soon")*
7. ZeroAlloc.Results *(coming soon)*
8. ZeroAlloc.Specification *(coming soon)*
9. ZeroAlloc.Options *(coming soon)*
10. ZeroAlloc.Mapping *(coming soon)*

## Changes to profile/README.md

### 1. Packages table

- Move `ZeroAlloc.ValueObjects` row to position 2 (after Analyzers, before Inject).
- Add `ZeroAlloc.Pipeline` row after Mediator with NuGet badge and description:
  > Shared compile-time pipeline infrastructure — `IPipelineBehavior` interface and Roslyn discovery/emission utilities for ZeroAlloc generators
- Upgrade `ZeroAlloc.Validation` row: remove "*(coming soon)*", add NuGet badge and GitHub link.

### 2. Body sections — reorder

Move the `ZeroAlloc.ValueObjects` section to after `ZeroAlloc.Analyzers` and before `ZeroAlloc.Inject`. All existing section content stays unchanged.

### 3. New section: ZeroAlloc.Pipeline

Insert after the Mediator section.

- **Description**: Shared building block for pipeline-aware source generators in the ZeroAlloc ecosystem. Provides `IPipelineBehavior`, `PipelineBehaviorAttribute`, and Roslyn-based compile-time discovery and static lambda chain emission. Used internally by ZeroAlloc.Mediator and ZeroAlloc.Validation — no reflection, no virtual dispatch, zero heap allocation per call.
- **Code example**: `LoggingBehavior` decorated with `[PipelineBehavior(Order = 1)]` implementing a static `Handle` method.
- **Benchmark**: Static chain vs pre-built delegate chain across 1/3/5 behaviors — 0 B allocated, up to 6.4× faster at 5 behaviors.

### 4. New section: ZeroAlloc.Validation

Insert after the Pipeline section.

- **Description**: Attribute-based validation with a source-generated strongly-typed validator per model. Zero allocations on the valid path, 25+ built-in attributes, nested/collection support, ASP.NET Core auto-validation, conditional rules. No reflection, Native AOT safe.
- **Code example**: `CreateOrderRequest` with `[Validate]`, `[NotEmpty]`, `[MaxLength]`, `[GreaterThan]`, `[EmailAddress]` and calling the generated `CreateOrderRequestValidator`.
- **Benchmark**: Flat model / Nested model / Collection (3×) vs FluentValidation — 0 B allocated, ~49×–143× faster.
