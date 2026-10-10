# Design: mark ZeroAlloc libraries AOT-compatible (ZA1706 sweep)

**Date:** 2026-10-10

## Context

ZeroAlloc.Analyzers 1.8.0 added ZA1706. It reports any net8.0-or-later library that never set `IsAotCompatible`. Without that property, the SDK's trim and AOT analyzers (`IL2xxx`, `IL3xxx`) never run on the library. Code that breaks under Native AOT therefore ships unnoticed until an app publishes with it. Native AOT is the point of ZeroAlloc, so the org's own libraries should pass the rule.

A survey on 2026-10-10 covered 27 repos. Each library was built on `origin/main` with `-p:IsAotCompatible=true`. Jev is out of scope, because another agent owns it until 1.0.0.

- ZA1706 would flag 47 projects: libraries plus two test helpers.
- 34 of them build with no trim or AOT warning.
- 13 produce 82 warnings, mostly IL2026 and IL3050.
- No repo sets AOT properties in `Directory.Build.props`. The libraries that already opt in do so in their own csproj, conditioned on a net8+ TFM.

## Decisions

1. **Two waves.** Wave 1 marks the clean projects. Wave 2 does the real work for projects with warnings, one PR per repo.
2. **Reflection-based packages are annotated, not opted out.**
   - These packages set `IsAotCompatible=true` and put `[RequiresUnreferencedCode]` and `[RequiresDynamicCode]` on their public entry points.
   - An AOT app then gets a warning at the exact call it makes.
   - An explicit `false` would leave that app with no warning at all.
3. **Test helpers set `IsAotCompatible=false`.** They build clean only because Roslyn and xunit carry no trim annotations. They never run under AOT, so `false` records a decision rather than a claim.
4. **Serialisation goes back to the maintainer first.** Its MemoryPack and MessagePack implementations need a design choice before any change, described in wave 2.

## Rules for every PR

- **Where the property goes:** in the project's csproj, under the same net8+ condition style the repo already uses for its core package. A repo with no existing example uses `$([MSBuild]::IsTargetFrameworkCompatible('$(TargetFramework)', 'net8.0'))`.
- **What CI must show:** every target framework builds with warnings as errors, and the tests pass. The survey built only the highest net8+ TFM.
- **No suppressions:** no `NoWarn`, `#pragma` or `UnconditionalSuppressMessage` to make a build green. A warning is fixed at its source or the API is annotated.
- **Commit type:** `feat:`. `IsAotCompatible` also sets `IsTrimmable`, so a consumer's trimmed app may trim the assembly further. The PR body states this in a "Behaviour change" section.
- **Releases:** none are cut. Each PR rides the next batched release cycle.

## Wave 1: mark the clean projects

One PR per repo.

| Repo | Projects | Notes |
|---|---|---|
| Collections | ZeroAlloc.Collections | netstandard2.1 is excluded by the condition |
| EventSourcing | Aggregates, InMemory, Kafka, Mediator, Outbox, PostgreSql, Sql, Sqlite, SqlServer | Telemetry waits for wave 2 |
| Inject | ZeroAlloc.Inject, ZeroAlloc.Inject.Container | |
| Mediator | Authorization, Cache, Resilience, Telemetry, Validation | |
| Outbox | Dashboard.Blazor, InMemory, Mediator, Telemetry | The other packages wait for wave 2 |
| Results | ZeroAlloc.Results | |
| Scheduling | InMemory, Mediator, Redis, Telemetry | The other packages wait for wave 2 |
| Specification | ZeroAlloc.Specification | |
| Telemetry | ZeroAlloc.Telemetry | |
| TestHelpers | ZeroAlloc.TestHelpers | `false` |
| Validation | ZeroAlloc.Validation, Validation.AspNetCore, Validation.Options; Validation.Testing | Validation.Testing is a test helper and gets `false` |

The survey's per-project results decide which Outbox and Scheduling packages are clean. If a wave-1 build finds a warning on a lower TFM that the survey missed, that project moves to wave 2.

## Wave 2: real fixes

One PR per repo. Each gets an independent review, because a wrong annotation does not fail the build.

### Outbox and Scheduling

Both repos have the same shape, so the same fixes apply to each.

- **Dashboard.** `MapGet(string, Delegate)` raises IL2026/IL3050, and so does reflection-based `JsonSerializer.Serialize(object, Type, options)`.
  - Set `EnableRequestDelegateGenerator`, so ASP.NET's generator binds the endpoints at compile time.
  - Serialize through a source-generated `JsonSerializerContext`.
- **Dashboard.Blazor (Scheduling only; Outbox's is clean).** Call `ReadFromJsonAsync` with a `JsonTypeInfo<T>` from a source-generated context.
- **Resilience.** Annotate `AddTransient<TService>`'s type parameter with `[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)]` (IL2091).
- **EfCore.** EF Core is not trim-safe, which shows up as IL2026 on the `DbContext` constructor and `[MaxLength]`. Annotate the public entry points with `RequiresUnreferencedCode` and `RequiresDynamicCode`.

### EventSourcing.Telemetry

- `WithTelemetry()` decorates every registered `IAggregateRepository<TAggregate, TId>` at run time. It closes `InstrumentedAggregateRepository<,>` over the registration's type arguments with `MakeGenericType` (IL2055, IL3050) and creates it with `Activator`.
- `TId` is often a value type such as `Guid`, so under Native AOT the closed type may not exist and the call can fail at run time. That makes this a bug for AOT users, not only a warning.
- Fix: capture the types where they are statically known. When a repository is registered with its generic arguments, also register a typed decorator factory for that pair. `WithTelemetry()` then applies those factories instead of building types at run time.
- Design the registration change in the PR, and keep `WithTelemetry()` source-compatible.

### AdoNet.Async

- **DataSet.**
  - Replace `Type.GetType(name)` on serialized column types (IL2057) with a closed switch over the supported column types.
  - Annotate the code paths that set `DataTable.DisplayExpression` and `DataColumn.Expression`. System.Data evaluates those by reflection.
- **Serialization.NewtonsoftJson.** Newtonsoft is reflection-based, so annotate the entry points.
- **Serialization.SystemTextJson.** Fix with source-generated `JsonTypeInfo` where the serialized types are known. Annotate where they are user types.

### ValueObjects.EfCore

- The package scans an assembly and closes generics over user ID types. That raises IL2026, IL2060, IL2070, IL2075, IL2076 and IL3050.
- Annotate the scanning entry point, and add `[DynamicallyAccessedMembers]` on `TId` wherever that covers the rest.
- File a feature issue to have ValueObjects.Generator emit the converter registration. That removes the scan entirely.

### Serialisation (decision first)

`MemoryPackSerializer<T>` and `MessagePackSerializer<T>` carry `RequiresUnreferencedCode`/`RequiresDynamicCode`, but the `ISerializer<T>` members they implement do not (IL2046, IL3051). The options:

1. **Make them AOT-safe.** Use MemoryPack's generated formatters and MessagePack's source-generated resolver, and drop the attributes. This only works if both libraries' generic APIs are AOT-safe with their generators.
2. **Annotate `ISerializer<T>`.** This pushes the warning to every caller, including callers of the already AOT-safe System.Text.Json implementation.
3. **Stop implementing `ISerializer<T>`** in the reflection-based types, or split the interface. This is a breaking change.

Read the code, recommend an option, and get the maintainer's decision before changing anything.

## Done when

- ZA1706 reports nothing for any repo in scope.
- Every library either builds clean with `IsAotCompatible=true`, or annotates its reflection-based entry points. Test helpers set `false`.
- The ValueObjects.EfCore generator issue is filed, and the Serialisation decision is made and carried out.
