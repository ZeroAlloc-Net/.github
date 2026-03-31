---
date: 2026-03-31
topic: Add new packages to GitHub landing page
status: approved
---

# Design: Add New Packages to GitHub Landing Page

## Goal

Update `profile/README.md` to include the four new ZeroAlloc-Net packages:
`ZeroAlloc.Collections`, `ZeroAlloc.AsyncEvents`, `ZeroAlloc.Notify`, and `ZeroAlloc.Rest`.

## Approach

Option A: Full sections — add table rows + a complete section per package (description, code snippet, benchmark table), matching the existing style for all eight packages.

## Packages Table

Add 4 new rows after the existing `ZeroAlloc.Specification` row, in this order:

| Package | Description |
|---|---|
| ZeroAlloc.Collections | Zero-alloc pooled collection types |
| ZeroAlloc.AsyncEvents | Zero-alloc async event primitives |
| ZeroAlloc.Notify | Source-generated async INPC |
| ZeroAlloc.Rest | Source-generated Native AOT REST client |

Each row: GitHub link, one-line description, NuGet badge (same markup as existing rows).

## New Sections

Appended after `## ZeroAlloc.Specification`, before the footer `<p align="center">` tag.

### ZeroAlloc.Collections

- **Description:** 6 collection types (PooledList, RingBuffer, SpanDictionary, PooledStack, PooledQueue, FixedSizeList); each available as `ref struct` (stack-only) and heap class variant; ArrayPool-backed; `AsSpan()` accessors; source generators; Native AOT safe.
- **Code snippet:** `PooledList<T>` construction + Add/iterate, and `RingBuffer<T>` TryWrite/TryRead.
- **Table:** 6-row collections summary (Type, Ref Struct, Heap Variant, Description).
- **No benchmark numbers** — none exist in the upstream README.

### ZeroAlloc.AsyncEvents

- **Description:** Lock-free CAS registration, ValueTask throughout, ArrayPool parallel dispatch, `[AsyncEvent]` source generator for boilerplate-free event wiring.
- **Code snippet:** Field declaration + event property + `InvokeAsync` call; source generator `[AsyncEvent]` usage.
- **Benchmark table:** 4 rows — Sync multicast, NaiveAsync TaskWhenAll, ZeroAlloc Parallel, ZeroAlloc Sequential (Mean / Ratio / Allocated). Key callout: sequential mode 30% faster than sync multicast at 0 B; parallel mode 3× faster than naive async with 51% less memory.

### ZeroAlloc.Notify

- **Description:** `[NotifyPropertyChangedAsync]` + `[ObservableProperty]` on `partial` classes; source generator wires PropertyChangedAsync / CollectionChangedAsync at compile time; fully awaitable ValueTask dispatch; only framework in class with async-first handlers.
- **Code snippet:** ViewModel with `[ObservableProperty]` fields + subscriber + `await vm.SetNameAsync(...)`.
- **Benchmark table:** 4 rows — Sync INPC baseline, CommunityToolkit, Fody, ZeroAlloc (Mean / Alloc / vs Baseline). Note that CommunityToolkit and Fody are sync-only; ZeroAlloc is the only fully-awaitable option.

### ZeroAlloc.Rest

- **Description:** `[ZeroAllocRestClient]` interface → Roslyn generator emits sealed `*Client` at compile time; no reflection, no proxies, no IL emit; path/query/body/header params; `Result<T, HttpError>` returns; pluggable serializers (STJ, MemoryPack, MessagePack); OpenAPI codegen via MSBuild task.
- **Code snippet:** Interface definition with `[Get]`/`[Post]`/`[Delete]` + DI registration + injection usage.
- **Benchmark table:** 5 rows — Raw HttpClient baseline, ZeroAlloc GET, Refit GET, ZeroAlloc QueryParam, Refit QueryParam (Mean / vs Refit / Allocated). Key callout: 3.2× faster on GET, 5.5× on query params.

## Section Order in README

```
## Packages  (table — 12 rows total)
## ZeroAlloc.Analyzers
## ZeroAlloc.ValueObjects
## ZeroAlloc.Inject
## ZeroAlloc.Pipeline
## ZeroAlloc.Mediator
## ZeroAlloc.Validation
## ZeroAlloc.Results
## ZeroAlloc.Specification
## ZeroAlloc.Collections      ← new
## ZeroAlloc.AsyncEvents       ← new
## ZeroAlloc.Notify            ← new
## ZeroAlloc.Rest              ← new
<footer>
```

## Delivery

Single commit on a feature branch `docs/add-new-packages-landing-page`, then a PR against `main`.
