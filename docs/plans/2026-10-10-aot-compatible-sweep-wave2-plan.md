# ZA1706 sweep, wave 2: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the 13 libraries that produced trim or AOT warnings genuinely AOT-safe, or annotate their reflection-based entry points. Each one then sets `IsAotCompatible=true` and builds clean, with one PR per repo.

**Architecture:** Each task fixes warnings at the source, or moves `RequiresUnreferencedCode`/`RequiresDynamicCode` to the public entry point where reflection is unavoidable, and then sets the property. Every PR gets an independent review, because a wrong annotation builds clean.

**Tech Stack:** .NET 8–10, ASP.NET Core minimal APIs with the Request Delegate Generator, System.Text.Json source generation, EF Core, MemoryPack, MessagePack 3, Microsoft.Extensions.DependencyInjection.

**Spec:** `docs/plans/2026-10-10-aot-compatible-sweep-design.md` (this repo), section "Wave 2"

## Global Constraints

- **Worktrees only.** The local clones are on other branches, and some have uncommitted work. Each task runs `git -C <clone> fetch origin` and then `git -C <clone> worktree add <clone>/.worktrees/aot-wave2 -b feat/aot-wave2 origin/main`, and works only there. If `.worktrees/` is not ignored, add it to the clone's `.git/info/exclude`.
- **No suppressions.** Do not add `NoWarn`, `#pragma`, `UnconditionalSuppressMessage`, `DynamicDependency` used to silence a warning, or `WarningsAsErrors` overrides. Fix each warning at its source, or annotate the public entry point and let the requirement flow to the caller.
- **Annotation messages say why and what to do instead.** For example: "EF Core builds its model with reflection and is not trim-safe; see https://aka.ms/efcore-docs-trimming." A message that only says "may require dynamic code" is not enough.
- **Placing `IsAotCompatible`.** Set `<IsAotCompatible>true</IsAotCompatible>` in the first `<PropertyGroup>` of each project the task lists. All of them target net8.0 or later only.
- **What has to pass.**
  - `dotnet build <sln> -c Release` succeeds for every TFM, with no `IL2xxx` or `IL3xxx` output. `TreatWarningsAsErrors` is on in every repo.
  - `dotnet test <sln> -c Release --no-build` passes.
  - If a TFM's tests cannot run locally because a runtime is missing, for example ASP.NET Core 8, CI's run of that TFM is the gate. Confirm it from the CI log and say so in the PR.
- **Public API.** A repo with `PublicAPI.*.txt` files updates `PublicAPI.Unshipped.txt` for every addition. Never add an optional parameter to an existing shipped signature; add a new overload instead.
- **Commit messages.**
  - Headers are conventional and lowercase after the colon. The type is `feat:` for new API or newly AOT-compatible packages, and `fix:` for a behaviour bug.
  - Body lines are 100 characters or fewer, with no nested parentheses. End with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - No `claude.ai/code/session` link anywhere, in commits or PR bodies.
- **PR body.** Fill in the repo's PR template if it has one. Include:
  - a "Behaviour change" section that names every new caller-facing warning, and states that `IsAotCompatible` also sets `IsTrimmable`;
  - a link to the spec;
  - `🤖 Generated with [Claude Code](https://claude.com/claude-code)` at the end.
- **Checks and merging.** Wait for every check (`gh pr checks <n> --watch`). Do not merge, and do not touch release PRs.
- **Local packages.** If a step packs packages, use version `9.9.9-local.<tag>` or a temporary `--packages` folder. Never pack a real release number.

## Standard procedure

Every task follows these steps, using the specifics in its own section.

- [ ] **Step 1: Create the worktree.** See Global Constraints.
- [ ] **Step 2: Reproduce the warnings.** For each project in the task, build its newest TFM with `-p:IsAotCompatible=true -p:TreatWarningsAsErrors=false`, and record the `IL2xxx`/`IL3xxx` list. It should match the task's list. If it differs, report the difference before changing anything.
- [ ] **Step 3: Write the failing tests** the task names, and run them to see them fail.
- [ ] **Step 4: Make the changes** the task describes.
- [ ] **Step 5: Set `IsAotCompatible=true`** on the task's projects.
- [ ] **Step 6: Build and test.** See "What has to pass". The Step 2 build must now show no IL warnings, and the new tests must pass.
- [ ] **Step 7: Commit, push, open the PR and wait for checks.** Report the PR URL and the check results.

---

### Task 1: Serialisation (MemoryPack and MessagePack adapters)

**Repo:** `ZeroAlloc.Serialisation`, solution `ZeroAlloc.Serialisation.slnx`

**Warnings:** IL2046 and IL3051 on `src/ZeroAlloc.Serialisation.MemoryPack/MemoryPackSerializer.cs` and `src/ZeroAlloc.Serialisation.MessagePack/MessagePackSerializer.cs`. `Serialize` and `Deserialize` carry the trim and AOT attributes, but the `ISerializer<T>` members they implement do not.

**Decision (maintainer, 2026-10-10):** follow ZeroAlloc.Rest's `MemoryPackRestSerializer` and `MessagePackRestSerializer` pattern. Annotate the constructors that choose a reflection path, not the interface methods, and add AOT-safe constructors.

**Changes:**
- **`MessagePackSerializer<T>`:**
  - Remove the attributes from `Serialize` and `Deserialize`.
  - Put `[RequiresUnreferencedCode]` and `[RequiresDynamicCode]` on the existing `MessagePackSerializer()` and `MessagePackSerializer(MessagePackSerializerOptions options)` constructors. Reuse the message text of Rest's `ReflectionMessage`, naming this type.
  - Add `public MessagePackSerializer(IFormatterResolver resolver, MessagePackSerializerOptions? options = null)`, unannotated. It throws `ArgumentNullException` for a null resolver, and stores `(options ?? MessagePackSerializerOptions.Standard).WithResolver(resolver)`. Its XML doc says the resolver should be built from a `[GeneratedMessagePackResolver]` class and `BuiltinResolver.Instance` for Native AOT.
- **`MemoryPackSerializer<T>`:**
  - Remove the attributes from `Serialize` and `Deserialize`.
  - Add an explicit `public MemoryPackSerializer()` that carries `[RequiresUnreferencedCode]` and `[RequiresDynamicCode]`. Its message says MemoryPack finds a type's formatter through reflection unless the formatter is registered, and points to `MemoryPackableSerializer<T>`.
  - Add a `protected MemoryPackSerializer(bool formatterRegistered)` constructor, unannotated, for subclasses that have registered the formatter themselves.
- **New `MemoryPackableSerializer<T>`:** `public sealed class MemoryPackableSerializer<T> : MemoryPackSerializer<T> where T : IMemoryPackable<T>`. Its constructor calls the protected base constructor and runs `T.RegisterFormatter()`. Its XML doc explains that this is the Native AOT path.
- **`IsAotCompatible=true`** on both adapter projects.
- **Next-major issue.** File one in ZeroAlloc.Serialisation, labelled `next-major`: in the next major, remove the reflection-based constructors, so `MessagePackSerializer<T>` requires a resolver and `MemoryPackSerializer<T>` is replaced by `MemoryPackableSerializer<T>`. Link it from the PR.

**Tests:** add them to the repo's existing adapter tests, or create `tests/ZeroAlloc.Serialisation.Tests/AotSafeAdapterTests.cs` if there are none.
- `MemoryPackableSerializer<T>` round-trips a `[MemoryPackable]` record.
- `new MessagePackSerializer<T>(resolver)` round-trips a `[MessagePackObject]` type through a resolver built from `BuiltinResolver.Instance` and the type's formatter.
- A null resolver throws `ArgumentNullException`.
- In `samples/ZeroAlloc.Serialisation.AotSmoke`, round-trip one value through each AOT-safe path, so the AOT smoke check runs them under Native AOT.

**Commit:** `feat: add AOT-safe constructors to the MemoryPack and MessagePack serializers`

### Task 2: Outbox (Dashboard, EfCore and Resilience)

**Repo:** `ZeroAlloc.Outbox`, solution `ZeroAlloc.Outbox.slnx`

**Warnings:**
- **Dashboard** (`OutboxDashboardEndpointRouteBuilderExtensions.cs`): IL2026 and IL3050 at lines 91–94, from `MapGet(string, Delegate)`. IL2026 and IL3050 at line 218, from `JsonSerializer.Serialize(object, Type, JsonSerializerOptions)`.
- **EfCore** (`OutboxMessageEntity.cs:14`): IL2026, from `[MaxLength]`.
- **Resilience** (`OutboxResilienceServiceCollectionExtensions.cs:48`): IL2091 on `TService`.

**Changes:**
- **Dashboard:**
  - Set `<EnableRequestDelegateGenerator>true</EnableRequestDelegateGenerator>` in the csproj, so ASP.NET's generator binds the `MapGet` handlers at compile time.
  - Replace the line-218 call with a source-generated `JsonSerializerContext` declared in the project, using `[JsonSerializable]` for every type the dashboard writes, and serialize through its `JsonTypeInfo`.
  - If the generator cannot bind a handler, rewrite that handler as a typed lambda or a `RequestDelegate`. Do not annotate it.
- **EfCore:**
  - Remove `[MaxLength]` from `OutboxMessageEntity`.
  - Configure the same lengths with `HasMaxLength` in the entity's existing EF Core configuration.
  - Add a test that the model's max lengths are unchanged. Build the model, read `GetMaxLength()` for each property, and compare with the old values.
- **Resilience:** annotate the method's `TService` type parameter, and `TImplementation` if there is one, with `[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)]`, so the requirement flows to callers.
- **`IsAotCompatible=true`** on Dashboard, EfCore and Resilience.

**Tests:**
- The EfCore max-length test above.
- A Dashboard test that each endpoint still returns its JSON. Use the existing Dashboard tests if they cover this; otherwise add one per endpoint with `WebApplicationFactory` or `TestServer`.

**Commit:** `feat: make the Outbox dashboard, EfCore and Resilience packages AOT-compatible`

### Task 3: Scheduling (Dashboard, Dashboard.Blazor, EfCore and Resilience)

**Repo:** `ZeroAlloc.Scheduling`, solution `ZeroAlloc.Scheduling.slnx`. The local clone has uncommitted work, so use the worktree only.

**Warnings:**
- **Dashboard** (`JobsDashboardExtensions.cs`): IL2026 and IL3050 at lines 43, 44, 49, 54 and 57, from `MapGet(string, Delegate)`.
- **Dashboard.Blazor** (`JobsDashboardClient.cs`): IL2026 and IL3050 at lines 16, 23, 30, 37 and 44, from `ReadFromJsonAsync<T>(HttpContent, CancellationToken)`.
- **EfCore** (`SchedulingDbContext.cs:9`): IL2026 and IL3050, from the `DbContext(DbContextOptions)` constructor.
- **Resilience** (`SchedulingResilienceServiceCollectionExtensions.cs:44`): IL2091 on `TService`.

**Changes:**
- **Dashboard:**
  - Set `<EnableRequestDelegateGenerator>true</EnableRequestDelegateGenerator>`.
  - Serialize the responses through a source-generated `JsonSerializerContext`.
  - Rewrite any handler the generator cannot bind, as in Task 2.
- **Dashboard.Blazor:** add a source-generated `JsonSerializerContext` covering every response type, and call `ReadFromJsonAsync(JsonTypeInfo<T>, CancellationToken)`.
- **EfCore:**
  - EF Core itself is not trim-safe, so annotate.
  - Put `[RequiresUnreferencedCode]` and `[RequiresDynamicCode]`, with the EF Core message from Global Constraints, on the `SchedulingDbContext` constructor.
  - Put the same attributes on every public method that registers or creates it, such as the `AddScheduling...EfCore` extension methods. Follow each call chain to the public API until the build is clean.
- **Resilience:** add `[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)]` on `TService`, as in Task 2.
- **`IsAotCompatible=true`** on all four projects.

**Tests:**
- A Blazor client test that each method still deserializes a sample response.
- A Dashboard test per endpoint, as in Task 2.

**Commit:** `feat: make the Scheduling dashboard, EfCore and Resilience packages AOT-compatible`

### Task 4: EventSourcing.Telemetry (typed repository decorator)

**Repo:** `ZeroAlloc.EventSourcing`, solution `ZeroAlloc.EventSourcing.slnx`

**Warnings:** IL2055 and IL3050 at `src/ZeroAlloc.EventSourcing.Telemetry/EventSourcingBuilderExtensions.cs:41`. `typeof(InstrumentedAggregateRepository<,>).MakeGenericType(typeArgs)` closes the decorator at run time, and `Activator.CreateInstance` creates it.

**Problem:** `TId` is often a value type, such as `Guid`. Under Native AOT the closed generic may not exist, so the behaviour can fail at run time, not just warn.

**Changes:**
- Capture the types where they are statically known. Find where `IAggregateRepository<TAggregate, TId>` registrations are made in this repo. Search for the generic registration methods on `EventSourcingBuilder` and the generator output in `ZeroAlloc.EventSourcing.Generators`.
- At each such registration, also register a typed decorator factory for that pair. For example, `services.AddSingleton<IRepositoryDecoratorFactory>(new RepositoryDecoratorFactory<TAggregate, TId>())`, whose method wraps an `IAggregateRepository<TAggregate, TId>` in `InstrumentedAggregateRepository<TAggregate, TId>` without reflection.
- `WithTelemetry()` keeps its signature. It replaces each repository descriptor using the matching factory, and never calls `MakeGenericType` or `Activator`.
- **Repositories registered without a factory.** First find out whether any supported path, documented or tested, registers a repository without going through a method that can add the factory. A hand-written `ServiceDescriptor` is one example.
  - If there are none, `WithTelemetry()` decorates through factories only. The XML doc says it decorates repositories registered through the builder.
  - If such paths exist, stop and report NEEDS_CONTEXT with the options and their behaviour changes. The controller decides. A silent behaviour change is not acceptable.
- Keep `WithTelemetry()`'s idempotency and its documented ordering rule.
- **`IsAotCompatible=true`** on `ZeroAlloc.EventSourcing.Telemetry`.

**Tests:**
- The existing telemetry tests still pass.
- New test: a repository with a value-type `TId`, such as `Guid`, is decorated and records its spans.
- New test: `WithTelemetry()` called twice decorates once.
- The AOT smoke sample, if it exists in this repo, runs a decorated `Guid`-keyed repository.

**Commit:** `fix: decorate aggregate repositories for telemetry without runtime generic construction`

**Model:** this task needs design judgment, so dispatch it on the most capable model.

### Task 5: AdoNet.Async (JSON converters)

**Repo:** `AdoNet.Async` at `C:\Projects\Prive\ZeroAlloc\AdoNet.Async` (remote `MarcelRoozekrans/AdoNet.Async`), solution `System.Data.Async.slnx`

**Warnings:**
- **NewtonsoftJson** (`AsyncDataTableConverter.cs`): IL2026 at lines 36, 172 and 330, from the `DataTable.DisplayExpression` and `DataColumn.Expression` setters. IL2057 at lines 317 and 778, from `Type.GetType(string)`.
- **NewtonsoftJson** (`AsyncDataSetConverter.cs:481`): IL2057.
- **SystemTextJson** (`AsyncDataTableJsonConverter.cs`): IL2026 at lines 75 and 164. IL2057 at lines 155 and 531.
- **DataSet:** Step 2 decides whether `System.Data.Async.DataSet` has warnings of its own. If it has none, it only gets the property.

**Changes:**
- System.Data evaluates `Expression` and `DisplayExpression` by reflection, and .NET marks those setters as reflection-dependent. Restoring a column's runtime type from its serialized name needs `Type.GetType`. Both are part of what these converters do.
- So annotate the public entry points with `[RequiresUnreferencedCode]` and, where IL3050 applies, `[RequiresDynamicCode]`. Explain why in the message: "DataTable column expressions and column types are restored by reflection, which trimming can break". Those entry points are the converter constructors and any public registration methods, such as `AddAsyncDataSetConverters` or options extensions.
- Follow each call chain from the warning to the public API.
- Do not hide `Type.GetType` behind a helper that loses the warning.
- **`IsAotCompatible=true`** on `System.Data.Async.DataSet`, `System.Data.Async.Serialization.NewtonsoftJson` and `System.Data.Async.Serialization.SystemTextJson`.

**Tests:** the existing converter tests pass unchanged. Annotations do not change behaviour.

**Commit:** `feat: mark the DataSet and JSON converter packages AOT-compatible with annotated entry points`

### Task 6: ValueObjects.EfCore

**Repo:** `ZeroAlloc.ValueObjects`, solution `ZeroAlloc.ValueObjects.slnx`

**Warnings:**
- **`TypedIdModelConfigurationExtensions.cs`:** IL2026 at :33 (`Assembly.GetTypes`), IL2075 at :48, IL2060 and IL3050 at :56 and :64 (`MakeGenericMethod`), IL2076 and IL3050 at :60 (`MakeGenericType`), and IL2070 at :88.
- **`TypedIdValueConverter.cs`:** IL2090 at :26 and :42.

**Changes:**
- **`TypedIdValueConverter<TId, TBacking>`:** annotate `TId` with exactly the `DynamicallyAccessedMembers` the code uses: `PublicProperties`, `PublicConstructors` and `PublicParameterlessConstructor`, as the warnings name them. That clears IL2090 and IL2076 at the source, where the generic argument is static.
- **`AddTypedIdConventions` (line 16), the public scanning entry point:** add `[RequiresUnreferencedCode]` and `[RequiresDynamicCode]`, with a message that it scans the assembly and closes generics over the discovered ID types. The remaining warnings in the method body are then covered.
- **`IsAotCompatible=true`** on `ZeroAlloc.ValueObjects.EfCore`. It targets net8.0 and net9.0.
- **Feature issue.** File one in ZeroAlloc.ValueObjects: "Generate typed-ID EF Core converter registration, so no assembly scanning is needed". Ask for ValueObjects.Generator to emit a per-ID registration method that calls `TypedIdValueConverter<TId, TBacking>` statically. Link it from the PR.

**Tests:** the existing EfCore tests pass unchanged. Add one test that `AddTypedIdConventions` still configures a typed-ID property.

**Commit:** `feat: mark ZeroAlloc.ValueObjects.EfCore AOT-compatible with an annotated scanning entry point`

## After wave 2

- **ZA1706:** it reports nothing in any repo in scope.
- **Worktrees:** remove them after the PRs merge.
- **Release-please:** confirm that each commit appears in its repo's release-please PR.
