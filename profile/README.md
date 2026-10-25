<p align="center">
  <img src="https://raw.githubusercontent.com/ZeroAlloc-Net/.github/main/profile/banner.svg" alt="ZeroAlloc-Net" width="860"/>
</p>

## About

**ZeroAlloc-Net** is home to a family of high-performance .NET libraries built around three principles:

- **Zero allocations** — no heap pressure at steady state
- **Native AOT compatible** — no reflection, no runtime code generation
- **Compile-time correctness** — errors and wiring validated by Roslyn at build time, not at startup

Everything here targets .NET 8+ and is designed to work end-to-end with `PublishAot=true`.

### Design Philosophy

> If it needs reflection at runtime, it doesn't belong here.

All libraries in this org follow the same contract: the heavy work happens at compile time via Roslyn source generators or compile-time analysis. The runtime path is a straight line — no dictionaries, no `Type.GetMethod`, no dynamic dispatch.

---

## Packages

| Package | Description | NuGet |
|---|---|---|
| [ZeroAlloc.Analyzers](https://github.com/ZeroAlloc-Net/ZeroAlloc.Analyzers) | Roslyn analyzers for modern .NET performance patterns | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Analyzers.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Analyzers) |
| [ZeroAlloc.AsyncEvents](https://github.com/ZeroAlloc-Net/ZeroAlloc.AsyncEvents) | Zero-allocation async event primitives — lock-free registration, `ValueTask` invocation, `ArrayPool` parallel dispatch, source-generated `[AsyncEvent]` wiring | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.AsyncEvents.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.AsyncEvents) |
| [ZeroAlloc.Authorization](https://github.com/ZeroAlloc-Net/ZeroAlloc.Authorization) | Authorization primitives — `[Policy]` / `[RequirePolicy]` attributes + `IAuthorizationPolicy` contract + `ISecurityContext` for hosts to extend, with a bundled generator emitting `AuthorizerFor<TRequest>`. Source-of-truth contract package consumed by AI.Sentinel and ZeroAlloc.Mediator.Authorization | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Authorization.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Authorization) |
| [ZeroAlloc.Cache](https://github.com/ZeroAlloc-Net/ZeroAlloc.Cache) | Source-generated caching proxy — annotate an interface with `[Cache]`, Roslyn emits a transparent proxy with no heap allocation on a cache hit (`ValueTask<T>`, `MemoryCache`, .NET 9+). `IMemoryCache` and `HybridCache` backends | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Cache.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Cache) |
| [ZeroAlloc.Collections](https://github.com/ZeroAlloc-Net/ZeroAlloc.Collections) | Zero-allocation pooled collection types — PooledList, RingBuffer, SpanDictionary, PooledStack, PooledQueue, and FixedSizeList with `ref struct` and heap variants | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Collections.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Collections) |
| [ZeroAlloc.EventSourcing](https://github.com/ZeroAlloc-Net/ZeroAlloc.EventSourcing) | Zero-allocation event sourcing — struct-based aggregate state, in-memory and SQL backends, source-generated boilerplate, optional OpenTelemetry instrumentation | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.EventSourcing.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.EventSourcing) |
| [ZeroAlloc.Flux](https://github.com/ZeroAlloc-Net/ZeroAlloc.Flux) | Source-generated Flux/Redux state management — `[Feature]` state, `[Reducer]` statics, compile-time action dispatch. Zero allocation per dispatch when handlers complete synchronously. Blazor integration via `ZeroAlloc.Flux.Blazor` | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Flux.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Flux) |
| [ZeroAlloc.Inject](https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject) | Compile-time dependency injection via Roslyn source generator | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Inject.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Inject) |
| [ZeroAlloc.Mapping](https://github.com/ZeroAlloc-Net/ZeroAlloc.Mapping) | Source-generated Command→Domain→DTO mapper — `[Map<,>]` / `[TryMap<,>]` on a static partial class emits direct property assignments. No reflection, no expression trees, `Result<T, MappingError>` on the fallible path | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Mapping.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Mapping) |
| [ZeroAlloc.Mediator](https://github.com/ZeroAlloc-Net/ZeroAlloc.Mediator) | Zero-allocation mediator library with source-generated dispatch | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Mediator.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Mediator) |
| [ZeroAlloc.Notify](https://github.com/ZeroAlloc-Net/ZeroAlloc.Notify) | Source-generated async INPC — fully awaitable `PropertyChangedAsync`/`CollectionChangedAsync` dispatch, no reflection, compile-time wiring | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Notify.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Notify) |
| [ZeroAlloc.ORM](https://github.com/ZeroAlloc-Net/ZeroAlloc.ORM) | Source-generated raw-SQL data access — `[Query]` / `[Command]` / `[StoredProcedure]` on partial methods emit typed parameter binding and materialization against AdoNet.Async. NativeAOT-clean, zero runtime reflection | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.ORM.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.ORM) |
| [ZeroAlloc.Outbox](https://github.com/ZeroAlloc-Net/ZeroAlloc.Outbox) | Source-generated transactional outbox — `[OutboxMessage]` emits a typed writer and dispatcher bridge. EF Core and ZeroAlloc.ORM (production) and InMemory (tests) stores, polling worker, exponential-backoff retry, dead-letter | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Outbox.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Outbox) |
| [ZeroAlloc.Pipeline](https://github.com/ZeroAlloc-Net/ZeroAlloc.Pipeline) | Shared compile-time pipeline infrastructure — `IPipelineBehavior` interface and Roslyn discovery/emission utilities for ZeroAlloc generators | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Pipeline.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Pipeline) |
| [ZeroAlloc.Resilience](https://github.com/ZeroAlloc-Net/ZeroAlloc.Resilience) | Source-generated resilience policies — `[Retry]`, `[Timeout]`, `[RateLimit]`, and `[CircuitBreaker]` compose into a generated proxy with zero heap allocation on the happy path | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Resilience.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Resilience) |
| [ZeroAlloc.Rest](https://github.com/ZeroAlloc-Net/ZeroAlloc.Rest) | Source-generated Native AOT REST client — define an interface, Roslyn emits a type-safe `HttpClient` implementation at compile time, zero reflection at runtime | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Rest.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Rest) |
| [ZeroAlloc.Results](https://github.com/ZeroAlloc-Net/ZeroAlloc.Results) | Zero-allocation `Result<T, E>` — no boxing, no heap pressure, full combinator API with async and LINQ support | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Results.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Results) |
| [ZeroAlloc.Saga](https://github.com/ZeroAlloc-Net/ZeroAlloc.Saga) | Source-generated long-running process orchestration — declare a saga as a `partial class`, the generator emits state machine, notification handlers, and dispatch wiring. Compensation runs in reverse on failure | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Saga.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Saga) |
| [ZeroAlloc.Scheduling](https://github.com/ZeroAlloc-Net/ZeroAlloc.Scheduling) | Source-generated background job scheduler — `[Job]` annotation wires up executor, DI registration, and recurring startup at compile time. InMemory, EF Core, ZeroAlloc.ORM and Redis backends | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Scheduling.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Scheduling) |
| [ZeroAlloc.Serialisation](https://github.com/ZeroAlloc-Net/ZeroAlloc.Serialisation) | Source-generated `ISerializer<T>` — annotate a type, Roslyn emits a sealed serializer and DI extension. Backends for MemoryPack, MessagePack, and System.Text.Json. No reflection, no boxing, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Serialisation.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Serialisation) |
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
| [ZeroAlloc.StateMachine](https://github.com/ZeroAlloc-Net/ZeroAlloc.StateMachine) | Source-generated finite state machines — `[Transition<TState, TTrigger>]` attributes lower to a `switch` expression over tuples. No dictionary, no delegate dispatch, AOT-safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.StateMachine.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.StateMachine) |
| [ZeroAlloc.Telemetry](https://github.com/ZeroAlloc-Net/ZeroAlloc.Telemetry) | Source-generated OpenTelemetry proxy — annotate an interface, Roslyn emits a BCL `ActivitySource` + `Meter` decorator. No OTel SDK dependency, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Telemetry.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Telemetry) |
| [ZeroAlloc.Templates](https://github.com/ZeroAlloc-Net/ZeroAlloc.Templates) | `dotnet new` Web API templates — `za-clean` (Clean Architecture) and `za-vertical-slice`, both built on 11 ZeroAlloc libraries, plus Telemetry in `za-vertical-slice`, with SQLite, JWT, OpenTelemetry, NetArchTest boundary rules and BenchmarkDotNet/NBomber harnesses | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Templates.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Templates) |
| [ZeroAlloc.TestHelpers](https://github.com/ZeroAlloc-Net/ZeroAlloc.TestHelpers) | Source-distributed test helpers — `AllocationGate` asserts an allocation budget over a warmed, GC-settled loop; `TextSnapshot` and `GeneratorSnapshot` do snapshot testing. Compiles into the consumer assembly as `internal`, so it never reaches a package's public surface | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.TestHelpers.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.TestHelpers) |
| [ZeroAlloc.Validation](https://github.com/ZeroAlloc-Net/ZeroAlloc.Validation) | Source-generated validation API — zero allocations, no reflection, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Validation.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Validation) |
| [ZeroAlloc.ValueObjects](https://github.com/ZeroAlloc-Net/ZeroAlloc.ValueObjects) | Zero-allocation source-generated ValueObject equality for existing domain types, plus `[TypedId]` strongly-typed IDs | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.ValueObjects.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.ValueObjects) |

---

## ZeroAlloc.Analyzers

**64 Roslyn analyzers** across 15 categories that detect allocation-heavy patterns and suggest zero/low-allocation alternatives. Fully aware of target framework version — rules automatically enable/disable based on `TargetFramework`.

Rules cover collections, strings, memory, logging, LINQ, async/await, serialization, and more. Common checks include:

- `ZA0101`: Use `FrozenDictionary` for read-only dictionaries
- `ZA0109`: Avoid zero-length array allocation — use `Array.Empty()`
- `ZA0201`: Avoid string concatenation in loops
- `ZA0603`: Use `.Count`/`.Length` instead of LINQ `.Count()`
- `ZA1001`: Use JSON source generation instead of reflection
- `ZA1401`: Use static lambda when no capture needed

Designed to complement existing analyzers and catch subtle allocation bugs at build time.

---

## ZeroAlloc.AsyncEvents

Zero-allocation async event primitives for .NET. `AsyncEventHandler<TArgs>` uses a CAS-loop for lock-free handler registration, `ValueTask` throughout for zero `Task` allocation on hot paths, and rents from `ArrayPool` for parallel fan-out dispatch. A source generator handles the `event` property boilerplate: annotate a field with `[AsyncEvent]` and the generator emits the `add`/`remove` accessors.

```csharp
// Manual — declare backing field, expose event, invoke
private AsyncEventHandler<OrderPlacedArgs> _orderPlaced = new(InvokeMode.Parallel);

public event AsyncEvent<OrderPlacedArgs> OrderPlaced
{
    add    => _orderPlaced.Register(value);
    remove => _orderPlaced.Unregister(value);
}

await _orderPlaced.InvokeAsync(new OrderPlacedArgs(orderId), cancellationToken);

// Source generator — [AsyncEvent] generates the event property automatically
public partial class OrderService
{
    [AsyncEvent(InvokeMode.Parallel)]
    private AsyncEventHandler<OrderPlacedArgs> _orderPlaced = new(InvokeMode.Parallel);
    // Generated: public event AsyncEvent<OrderPlacedArgs> OrderPlaced { add => ...; remove => ...; }
}
```

**Benchmark** (BenchmarkDotNet v0.15.8, .NET 10, i9-12900HK — 10 handlers, invoked once):

| Method | Mean | Ratio | Allocated |
|---|---:|:---:|:---:|
| Sync multicast delegate (baseline) | 40.69 ns | 1.0× | — |
| Naive async (`Task.WhenAll`) | 440.47 ns | 10.83× | 280 B |
| **ZeroAlloc Parallel** | **18.31 ns** | **0.45×** | **0 B** |
| **ZeroAlloc Sequential** | **29.60 ns** | **0.73×** | **0 B** |

Both modes are **faster than a sync multicast delegate** and allocate nothing when handlers complete synchronously. Parallel mode is **more than 10× faster than naive `Task.WhenAll`**, which allocates 280–288 B per call.

---

## ZeroAlloc.Authorization

Source-of-truth authorization primitives for .NET: `ISecurityContext`, `IAuthorizationPolicy`, `[Policy]`, `[RequirePolicy]` and `AnonymousSecurityContext`. A bundled source generator emits one `AuthorizerFor<TRequest>` per `[RequirePolicy]`-decorated type, plus an `AddZeroAllocAuthorization()` DI extension. Hosts (AI.Sentinel for tool-call authz, `ZeroAlloc.Mediator.Authorization` for handler authz) resolve `AuthorizerFor<T>` and map the result to their own outcome.

```csharp
[Policy("AdminOnly")]
public sealed class AdminOnlyPolicy : IAuthorizationPolicy
{
    public ValueTask<UnitResult<AuthorizationFailure>> EvaluateAsync(
        ISecurityContext ctx, CancellationToken ct = default)
        => new(ctx.Roles.Contains("Admin")
            ? UnitResult<AuthorizationFailure>.Success()
            : new AuthorizationFailure(AuthorizationFailure.DefaultDenyCode, "Admin role required"));
}

[RequirePolicy("AdminOnly")]
public sealed record DeleteUserCommand(string UserId);

// using ZeroAlloc.Authorization.Generated;
builder.Services.AddZeroAllocAuthorization();   // generated
```

A denial carries a structured `Code` (default `"policy.deny"`) and an optional `Reason`. `ZAUTH` generator diagnostics catch unknown, duplicate or misdeclared policies at build time. Native AOT compatible; a synchronously completing `EvaluateAsync` allocates 0 B.

---

## ZeroAlloc.Cache

Source-generated zero-allocation caching proxy for .NET. Annotate an interface with `[Cache]`, the Roslyn generator emits a proxy that transparently intercepts every method call — **zero heap allocation on the cache-hit path** for `ValueTask<T>` methods on the default `MemoryCache` on .NET 9+. Backed by `IMemoryCache` by default, with optional `HybridCache` (L1 + L2) opt-in per method. AOT-safe.

```csharp
[Cache(TtlMs = 60_000)]
public interface IProductRepository
{
    ValueTask<Product?> GetByIdAsync(int id, CancellationToken ct);

    [Cache(TtlMs = 300_000, MaxEntries = 1_000)]
    ValueTask<IReadOnlyList<Product>> SearchAsync(string query, CancellationToken ct);
}

// One line wires proxy + backing implementation
builder.Services.AddProductRepositoryCache<ProductRepositoryImpl>();
```

Inject `IProductRepository` anywhere — caching is transparent to the caller.

---

## ZeroAlloc.Collections

Six zero-allocation collection types for .NET, each available as a `ref struct` for stack-only scenarios and as a heap class for use in async code and DI. The pooled collections rent their backing storage from `ArrayPool<T>.Shared` and return it on `Dispose()`; `FixedSizeList<T>` wraps a caller-supplied (typically `stackalloc`) span and `HeapFixedSizeList<T>` a plain array. `PooledList`, `HeapPooledList`, `FixedSizeList` and `PooledStack` expose `AsSpan()` for zero-copy inner loops. The `ref struct` variants add, look up and enumerate with 0 B allocated; the `Heap*` variants allocate one enumerator per `foreach`. An optional source generator can emit additional type-specific collection variants and `ref struct` enumerators at compile time — no reflection, fully Native AOT compatible.

```csharp
using ZeroAlloc.Collections;

// PooledList — growable, ArrayPool-backed; zero heap allocation for the backing array
using var list = new PooledList<int>(capacity: 64);
list.Add(1);
list.Add(2);
list.Add(3);
foreach (var item in list)
    Console.WriteLine(item);

// RingBuffer — fixed-capacity circular buffer for producer/consumer queues
using var ring = new RingBuffer<string>(capacity: 4);
ring.TryWrite("alpha");
ring.TryWrite("beta");
ring.TryWrite("gamma");
while (ring.TryRead(out var item))
    Console.WriteLine(item); // alpha, beta, gamma
```

| Type | Ref Struct | Heap Variant | Description |
|---|---|---|---|
| `PooledList<T>` | Yes | `HeapPooledList<T>` | Pool-backed growable list |
| `RingBuffer<T>` | Yes | `HeapRingBuffer<T>` | Fixed-capacity circular buffer |
| `SpanDictionary<TKey, TValue>` | Yes | `HeapSpanDictionary<TKey, TValue>` | Open-addressing hash map |
| `PooledStack<T>` | Yes | `HeapPooledStack<T>` | Pool-backed LIFO stack |
| `PooledQueue<T>` | Yes | `HeapPooledQueue<T>` | Pool-backed FIFO queue |
| `FixedSizeList<T>` | Yes | `HeapFixedSizeList<T>` | Stack-allocated fixed-capacity list |

---

## ZeroAlloc.EventSourcing

Zero-allocation event sourcing for .NET 8+. Struct-based aggregate state keeps the read path off the heap. In-memory, SQL Server, PostgreSQL and SQLite backends. Source generator emits aggregate boilerplate. First-class integration with `ZeroAlloc.Serialisation` for AOT-safe event serialization.

```csharp
public readonly record struct OrderId(Guid Value);
public sealed record OrderPlacedEvent(string OrderNumber, decimal Total);

// State is a struct — replaying events allocates no state objects
public partial struct OrderState : IAggregateState<OrderState>
{
    public static OrderState Initial => default;
    public bool IsPlaced { get; private set; }
    public decimal Total { get; private set; }

    internal OrderState Apply(OrderPlacedEvent e) => this with { IsPlaced = true, Total = e.Total };
}

// The generator emits ApplyEvent dispatch and OrderEventTypeRegistry for partial aggregates
public sealed partial class Order : Aggregate<OrderId, OrderState>
{
    public void Place(string orderNumber, decimal total)
    {
        if (State.IsPlaced) throw new InvalidOperationException("already placed");
        Raise(new OrderPlacedEvent(orderNumber, total));
    }
}

// Wire up DI
services
    .AddSingleton<IEventTypeRegistry, OrderEventTypeRegistry>()
    .AddEventSourcing()
    .UseInMemoryEventStore()   // swap for .UsePostgreSqlEventStore(cs) in production
    .UseAggregateRepository<Order, OrderId>(() => new Order(), id => new StreamId($"order-{id.Value}"));

// Use
var repo = sp.GetRequiredService<IAggregateRepository<Order, OrderId>>();
using var order = new Order();
order.Place("ORD-001", 99.99m);
await repo.SaveAsync(order, new OrderId(Guid.NewGuid()), CancellationToken.None);
```

Optional `ZeroAlloc.EventSourcing.Telemetry` package adds BCL-based `ActivitySource` + `Meter` instrumentation with no OpenTelemetry SDK dependency.

**Integration packages**

- `ZeroAlloc.EventSourcing.Aggregates`: aggregate base with generator-emitted `Apply` dispatch
- `ZeroAlloc.EventSourcing.InMemory`: in-process event store for tests and prototypes
- `ZeroAlloc.EventSourcing.PostgreSql`: PostgreSQL event store
- `ZeroAlloc.EventSourcing.SqlServer`: SQL Server event store
- `ZeroAlloc.EventSourcing.Sqlite`: SQLite event store, AOT-clean via Microsoft.Data.Sqlite
- `ZeroAlloc.EventSourcing.Kafka`: consumes events from Kafka topics with checkpointed position tracking
- `ZeroAlloc.EventSourcing.Mediator`: republishes live committed events through ZeroAlloc.Mediator notifications
- `ZeroAlloc.EventSourcing.Outbox`: at-least-once cross-aggregate event dispatch from the event store

---

## ZeroAlloc.Flux

Source-generated Flux/Redux state management for .NET 8 and .NET 10. The Roslyn generator wires every action to its reducer at compile time — no reflection, no runtime dictionaries, no virtual dispatch. The dispatch hot path allocates **0 bytes** per call when handlers complete synchronously.

```csharp
using ZeroAlloc.Flux;

// 1. State — record struct (recommended) or record class
[Feature]
public readonly partial record struct CounterState(int Count);

// 2. Actions — plain record structs, no marker interface
public readonly record struct IncrementAction(int Amount);
public readonly record struct ResetAction;

// 3. Reducers — static methods, discovered at compile time
public static partial class CounterReducers
{
    [Reducer]
    public static CounterState On(CounterState state, IncrementAction action)
        => state with { Count = state.Count + action.Amount };

    [Reducer]
    public static CounterState On(CounterState state, ResetAction _) => new(0);
}

// 4. Register and dispatch
services.AddZeroAllocFlux();
```

The generator ships inside the `ZeroAlloc.Flux` package, so one `PackageReference` gives you both the runtime contracts and the emitter. Blazor apps add `ZeroAlloc.Flux.Blazor`.

---

## ZeroAlloc.Inject

Attribute-driven DI registration that generates `IServiceCollection` extensions and a fully **Native AOT-safe** `IServiceProvider` at compile time — no `MakeGenericType`, no reflection scanning, no startup overhead.

```csharp
[assembly: ZeroAllocInject("AddMyServices")]

[Transient(As = typeof(IOrderService))]
public class OrderService : IOrderService { ... }

[Singleton(As = typeof(ICache))]
public class RedisCache : ICache { ... }
```

```csharp
// Generated at compile time — resolved without any reflection
services.AddMyServices();
var provider = services.BuildZeroAllocInjectServiceProvider();
```

`AddMyServices()` needs `ZeroAlloc.Inject` + `ZeroAlloc.Inject.Generator`; `BuildZeroAllocInjectServiceProvider()` (hybrid/standalone container) comes from `ZeroAlloc.Inject.Container`, which bundles both.

**Benchmark** (i9-12900HK, .NET 9 runtime, BenchmarkDotNet v0.15.8):

| Scenario | ZeroAlloc.Inject (Standalone) | Microsoft DI | Speedup |
|---|---:|---:|:---:|
| Transient (1 property dep) | 21.9 ns | 43.7 ns | **2×** |
| Decorated transient | 22.3 ns | 44.5 ns | **2×** |
| Open generic (closed type) | 7.7 ns | 13.5 ns | **1.8×** |
| Singleton | 5.4 ns | 6.3 ns | **1.2×** |

---

## ZeroAlloc.Mapping

Compile-time Command→Domain→DTO mapping. No reflection, no expression trees, no runtime configuration — the generator emits a direct constructor call, and the success path allocates nothing beyond the destination instance itself.

```csharp
using ZeroAlloc.Mapping;

public sealed record OrderRequest(int Id, string Notes);
public sealed record Order(int Id, string Notes);

// Declare the mapper — the generator fills in the partial
[Map<OrderRequest, Order>]
public static partial class AppMappings { }

var order = AppMappings.Map(new OrderRequest(42, "rush"));
```

What gets emitted is exactly what you would have written by hand:

```csharp
public static Order Map(OrderRequest src)
    => new Order(Id: src.Id, Notes: src.Notes);
```

`[TryMap<,>]` returns `Result<T, MappingError>` instead of throwing, and integrates with ZeroAlloc.Results and the smart constructors in ZeroAlloc.ValueObjects.

**Benchmark** (i9-12900HK, .NET 10.0.7, BenchmarkDotNet v0.15.8):

| Scenario | ZeroAlloc | Mapperly | AutoMapper | HandWritten |
|---|---:|---:|---:|---:|
| FlatIdentity (record copy) | 30.8 ns | 26.3 ns | 76.4 ns | 32.4 ns |
| Flattening (`a.b.c → d`) | 22.9 ns | 23.0 ns | 70.8 ns | 29.2 ns |
| Polymorphic dispatch | 11.4 ns | 11.0 ns | 48.8 ns | 11.3 ns |
| UpdateInPlace | 6.1 ns | 6.0 ns | **83.9 ns (~18×)** | 4.7 ns |

Level with Mapperly, the other source-generator mapper, and 2–18× faster than AutoMapper with allocation parity.

---

## ZeroAlloc.Mediator

Compile-time wired mediator for request/response, notifications, and streaming with **zero allocations** on every non-streaming dispatch path. Pipeline behaviors are inlined as static nested calls with no closure allocation.

```csharp
public readonly record struct Ping(string Message) : IRequest<string>;

public class PingHandler : IRequestHandler<Ping, string>
{
    public ValueTask<string> Handle(Ping request, CancellationToken ct)
        => ValueTask.FromResult($"Pong: {request.Message}");
}

// Generated mediator with strongly-typed Send/Publish/CreateStream overloads
var result = await Mediator.Send(new Ping("Hello"), ct); // ~0.5 ns, 0 bytes
```

**Benchmark** (i9-12900HK, .NET 10.0.4):

| Scenario | ZeroAlloc.Mediator | MediatR | Speedup |
|---|---|---|:---:|
| Send | 0.5 ns | 78.3 ns | **~160×** |
| Publish Single | 6.1 ns | 243.8 ns | **~40×** |
| Publish Multi | 6.6 ns | 332.4 ns | **~51×** |

**Integration packages**

- `ZeroAlloc.Mediator.Authorization`: authorizes requests via ZeroAlloc.Authorization before dispatch
- `ZeroAlloc.Mediator.Cache`: caches responses for request types marked `[Cache]`
- `ZeroAlloc.Mediator.Resilience`: retry, circuit breaker and timeout declared on request types
- `ZeroAlloc.Mediator.Telemetry`: OpenTelemetry request counter and duration histogram per `Send` (the generated dispatch already opens the spans)
- `ZeroAlloc.Mediator.Validation`: validates requests via ZeroAlloc.Validation; failures come back as `Result`, not exceptions

---

## ZeroAlloc.Notify

Source-generated async `INotifyPropertyChanged` for .NET 8+. Decorate a `partial` class with `[NotifyPropertyChangedAsync]` and mark backing fields with `[ObservableProperty]` — the Roslyn generator emits `PropertyChangedAsync` and strongly-typed `Set*Async` methods at compile time (add `[NotifyCollectionChangedAsync]` for `CollectionChangedAsync`). No reflection, no virtual dispatch, fully awaitable `ValueTask` handlers. The only INPC framework in the .NET ecosystem where `await vm.SetNameAsync(...)` truly awaits all registered handlers.

```csharp
[NotifyPropertyChangedAsync]
public partial class UserViewModel
{
    [ObservableProperty] private string _name = "";
    [ObservableProperty] private int    _age;
}

var vm = new UserViewModel();
vm.PropertyChangedAsync += async (args, ct) =>
{
    Console.WriteLine($"'{args.PropertyName}' changed: {args.OldValue} → {args.NewValue}");
    await SaveAuditLogAsync(args, ct);
};

await vm.SetNameAsync("Alice");
await vm.SetAgeAsync(30);
```

**Benchmark** (i9-12900HK, .NET 10.0.12, BenchmarkDotNet v0.15.8, 5 handlers):

| Method | Mean | Allocated | vs Baseline |
|---|---:|:---:|:---:|
| Sync `INotifyPropertyChanged` (baseline) | 35.2 ns | 24 B | — |
| CommunityToolkit.Mvvm *(sync only)* | 50.2 ns | 0 B | 1.43× slower |
| PropertyChanged.Fody *(sync only)* | 29.0 ns | 0 B | 1.21× faster |
| **ZeroAlloc.Notify** *(fully awaitable)* | **112.8 ns** | **40 B** | **only async-first** |

CommunityToolkit and Fody dispatch synchronously and cannot await async handlers. ZeroAlloc.Notify trades ~3× overhead for first-class `ValueTask` semantics — the right trade-off when handlers do I/O.

---

## ZeroAlloc.ORM

Raw SQL without the hand-shaped ADO.NET tower. Annotate a `partial` method with the query; the generator emits the parameter binding, execution and materialization against [AdoNet.Async](https://github.com/MarcelRoozekrans/AdoNet.Async). Zero runtime reflection, and NativeAOT-clean — which is the gap it exists to fill, since EF Core's precompiled-query pipeline collides with co-resident source generators.

```csharp
[Query("SELECT id, name FROM customers WHERE id = @id")]
public partial Task<Customer?> GetCustomerAsync(int id, CancellationToken ct);

public sealed record Customer(int Id, string Name);
```

A positional record whose order matches the `SELECT` needs no mapping configuration, and a nullable return type turns an empty result set into `null`. `[Command]` and `[StoredProcedure]` cover writes and procs, `IAsyncEnumerable<T>` returns stream without buffering, and `MigrationRunner` applies embedded SQL migrations on SQLite, Postgres and SQL Server.

Ships as four packages: the runtime extensions, the `Abstractions` attributes, the `Generator` itself, and `ZeroAlloc.TypeConversions` — a convention catalog shared with ZeroAlloc.Mapping.

---

## ZeroAlloc.Outbox

Source-generated transactional outbox for .NET. Annotate a message type with `[OutboxMessage]` and the Roslyn generator emits a typed writer and dispatcher bridge — no reflection, no boxing, AOT-safe. Backed by EF Core or ZeroAlloc.ORM (production) or in-memory (tests), with a built-in polling worker, exponential-backoff retry, and dead-letter support.

```csharp
[OutboxMessage]
public sealed record OrderPlaced(Guid OrderId, decimal Total);

// Enlist the outbox write in the same transaction as your domain change
await using var tx = await _db.Database.BeginTransactionAsync(ct);
await _db.SaveChangesAsync(ct);
await _outbox.WriteAsync(new OrderPlaced(orderId, total), tx.GetDbTransaction(), ct);
await tx.CommitAsync(ct);

// Polling worker dispatches in the background — at-least-once delivery, retry + DLQ baked in
services.AddOutbox().WithEfCore<MyDbContext>().AddOrderPlacedOutbox();
services.AddSerializerDispatcher(); // AOT-safe serializer, required since 4.0
```

**Integration packages**

- `ZeroAlloc.Outbox.EfCore`: EF Core store
- `ZeroAlloc.Outbox.Orm`: ZeroAlloc.ORM store with transactional enqueue on the caller's transaction
- `ZeroAlloc.Outbox.InMemory`: in-memory store for tests
- `ZeroAlloc.Outbox.Mediator`: dispatches outbox messages via `IMediator.Publish`
- `ZeroAlloc.Outbox.Resilience`: wraps dispatchers in a ZeroAlloc.Resilience proxy
- `ZeroAlloc.Outbox.Telemetry`: source-generated OpenTelemetry proxy around dispatch
- `ZeroAlloc.Outbox.Dashboard`: operations dashboard: Minimal API, SSE and embedded HTML
- `ZeroAlloc.Outbox.Dashboard.Blazor`: `<OutboxDashboard />` Blazor component

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

---

## ZeroAlloc.Resilience

Source-generated, zero-allocation resilience policies for .NET. Add `[Retry]`, `[Timeout]`, `[RateLimit]`, and `[CircuitBreaker]` to an interface — the generator emits a proxy that composes all policies in a fixed order (RateLimit → CircuitBreaker → Timeout → Retry) with **no heap allocation on the happy path** (beyond the unavoidable `CancellationTokenSource` for timeout). AOT-safe.

```csharp
[Retry(MaxAttempts = 3, BackoffMs = 200, Jitter = true, PerAttemptTimeoutMs = 1_000)]
[Timeout(Ms = 5_000)]
[RateLimit(MaxPerSecond = 100, BurstSize = 10)]
[CircuitBreaker(MaxFailures = 5, ResetMs = 1_000, HalfOpenProbes = 1, Fallback = nameof(FetchFallback))]
public interface IExternalService
{
    ValueTask<string> FetchAsync(string id, CancellationToken ct);
    ValueTask<string> FetchFallback(string id, CancellationToken ct);
}
```

---

## ZeroAlloc.Rest

Source-generated, Native AOT-compatible REST client for .NET 10+. Decorate an interface with `[ZeroAllocRestClient]` and annotate methods with `[Get]`, `[Post]`, `[Delete]`, etc. — the Roslyn generator emits a sealed `*Client` class at compile time. No runtime reflection, no dynamic proxies, no `DynamicMethod`. Path, query, body, and header parameters are handled via attributes. Returns integrate with `ZeroAlloc.Results` (`Result<T, HttpError>`) for typed error handling without exceptions on 4xx/5xx responses.

```csharp
[ZeroAllocRestClient]
public interface IUserApi
{
    [Get("/users/{id}")]
    Task<UserDto> GetUserAsync(int id, CancellationToken ct = default);

    [Get("/users")]
    Task<List<UserDto>> ListUsersAsync([Query] string? name = null, CancellationToken ct = default);

    [Post("/users")]
    Task<UserDto> CreateUserAsync([Body] CreateUserRequest request, CancellationToken ct = default);

    [Delete("/users/{id}")]
    Task DeleteUserAsync(int id, CancellationToken ct = default);
}

[JsonSerializable(typeof(UserDto))]
[JsonSerializable(typeof(List<UserDto>))]
[JsonSerializable(typeof(CreateUserRequest))]
internal partial class AppJsonContext : JsonSerializerContext { }

// DI registration — AddIUserApi extension generated by the source generator
builder.Services.AddIUserApi(options =>
{
    options.BaseAddress = new Uri("https://api.example.com");
    options.UseSerializer(new SystemTextJsonSerializer(AppJsonContext.Default));
});

// Inject and use — no reflection, no proxies at runtime
public class UserService(IUserApi api)
{
    public Task<UserDto> GetAsync(int id) => api.GetUserAsync(id);
}
```

**Benchmark** (i9-12900HK, .NET 10.0.7, BenchmarkDotNet v0.15.8 — in-memory handler, no real network I/O):

| Method | Mean | vs Refit | Allocated |
|---|---:|:---:|---:|
| Raw `HttpClient` (baseline) | 2.09 μs | — | 1.38 KB |
| **ZeroAlloc.Rest GET** | **3.52 μs** | **3.6× faster** | 1.88 KB |
| Refit GET | 12.70 μs | 1× | 2.88 KB |
| **ZeroAlloc.Rest QueryParam** | **4.28 μs** | **3.6× faster** | 1.99 KB |
| Refit QueryParam | 15.51 μs | 1× | 3.55 KB |

**Integration packages**

- `ZeroAlloc.Rest.DependencyInjection`: DI and `IHttpClientFactory` registration for generated clients
- `ZeroAlloc.Rest.SystemTextJson`: System.Text.Json serializer
- `ZeroAlloc.Rest.MessagePack`: MessagePack serializer
- `ZeroAlloc.Rest.MemoryPack`: MemoryPack serializer
- `ZeroAlloc.Rest.Resilience`: `[Retry]`, `[Timeout]`, `[CircuitBreaker]` and `[RateLimit]` on client interfaces
- `ZeroAlloc.Rest.Tools.MSBuild`: generates a client interface from an OpenAPI 3.x spec at build time
- `ZeroAlloc.Rest.Tools`: `zeroalloc generate` .NET tool that generates a client interface from an OpenAPI 3.x spec on the command line

---

## ZeroAlloc.Results

Zero-allocation, no-boxing `Result<T, E>` for .NET 8, 9 and 10. All five types — `Result`, `Result<T>`, `Result<T,E>`, `UnitResult<E>`, and `Maybe<T>` — are `readonly struct` values. No heap allocation, no boxing, no GC pressure. Full combinator API: `Map`, `Bind`, `Match`, `Tap`, `Ensure`, `Combine`, with `ValueTask`-based `MapAsync`, `BindAsync`, `TapAsync` and `MatchAsync`, plus LINQ query syntax via `Select` and `SelectMany`.

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
var permissions = await GetUser(id).MapAsync(async u => await LoadPermissions(u));
var response    = await permissions.BindAsync(async p => await BuildToken(p));
```

**Benchmark** (.NET 10.0.7, i9-12900HK, BenchmarkDotNet v0.15.4):

| Scenario | ZeroAlloc.Results | OneOf | ErrorOr | FluentResults |
|---|---:|---:|---:|---:|
| Success construct | 0.4 ns / 0 B | 0.5 ns / 0 B | 0.0 ns / 0 B | 87 ns / **112 B** |
| Failure construct | 0.3 ns / 0 B | 0.9 ns / 0 B | 63 ns / **184 B** | 87 ns / **272 B** |
| Failure consume | 0.4 ns / 0 B | 0.9 ns / 0 B | 2.6 ns / 0 B | 214 ns / **240 B** |
| Hot loop (100 iter, 1-in-3 fail) | **183 ns / 0 B** | 202 ns / 0 B | 7,693 ns / 6,256 B | 39,450 ns / 25,968 B |

Head-to-head vs [CSharpFunctionalExtensions](https://github.com/vkhorikov/CSharpFunctionalExtensions): **1.1–8.7× faster** depending on operation; 0 B both.

---

## ZeroAlloc.Saga

Source-generated long-running process orchestration for .NET. Declare a saga as a `partial class` decorated with `[Saga]` — the generator emits state-machine code, notification handlers, and dispatch wiring. Compensation runs in reverse on failure. No reflection, no open-generic resolution at runtime. Durable persistence comes from `ZeroAlloc.Saga.EfCore` (single shared `SagaInstance` table, row-version OCC, retry-on-conflict), `ZeroAlloc.Saga.Orm` or `ZeroAlloc.Saga.Redis`. InMemory remains the default; switch store with one fluent call.

```csharp
[Saga]
public partial class OrderFulfillmentSaga
{
    public OrderId OrderId { get; private set; }

    [CorrelationKey] public OrderId Correlation(OrderPlaced e)    => e.OrderId;
    [CorrelationKey] public OrderId Correlation(PaymentCharged e) => e.OrderId;
    [CorrelationKey] public OrderId Correlation(PaymentDeclined e) => e.OrderId;

    [Step(Order = 1, Compensate = nameof(CancelReservation), CompensateOn = typeof(PaymentDeclined))]
    public ReserveStockCommand ReserveStock(OrderPlaced e)
    {
        OrderId = e.OrderId;
        return new ReserveStockCommand(e.OrderId);
    }

    [Step(Order = 2)]
    public ShipOrderCommand ShipOrder(PaymentCharged e) => new(OrderId);

    public CancelReservationCommand CancelReservation() => new(OrderId);
}

// In-memory by default; swap to a durable store with one call
services.AddSaga()
    .WithEfCoreStore<MyDbContext>()
    .WithOrderFulfillmentSaga();   // generated per saga
```

**Integration packages**

- `ZeroAlloc.Saga.EfCore`: EF Core persistence with row-version optimistic concurrency
- `ZeroAlloc.Saga.Orm`: ZeroAlloc.ORM persistence
- `ZeroAlloc.Saga.Redis`: Redis persistence with WATCH/MULTI/EXEC concurrency
- `ZeroAlloc.Saga.Outbox`: transactional outbox: commands commit atomically with the saga state
- `ZeroAlloc.Saga.Outbox.Orm`: outbox unit of work for the ZeroAlloc.ORM backend
- `ZeroAlloc.Saga.Outbox.Redis`: outbox storage and unit of work for the Redis backend
- `ZeroAlloc.Saga.Resilience`: retry, timeout, circuit-breaker and rate-limit policies on step-command dispatch

---

## ZeroAlloc.Scheduling

Source-generated background job scheduler for .NET 8, 9 and 10. Decorate any class with `[Job]` and the generator emits the executor, DI registration, and recurring startup wiring — no reflection, no convention scanning at runtime. InMemory, EF Core, ZeroAlloc.ORM and Redis backends.

```csharp
[Job(Every = Every.Hour)]
public sealed class CleanupExpiredSessionsJob : IJob
{
    public ValueTask ExecuteAsync(JobContext ctx, CancellationToken ct)
        => /* work */ ValueTask.CompletedTask;
}

// Generated AddCleanupExpiredSessionsJob() wires executor + recurring schedule
builder.Services.AddSerializerDispatcher();   // AOT-safe job serializer, required since 2.0
builder.Services.AddScheduling()
    .WithInMemoryStore()
    .AddCleanupExpiredSessionsJob();
```

**Integration packages**

- `ZeroAlloc.Scheduling.InMemory`: in-memory job store for tests
- `ZeroAlloc.Scheduling.EfCore`: EF Core job store
- `ZeroAlloc.Scheduling.Orm`: ZeroAlloc.ORM job store with an atomic claim, on SQLite, PostgreSQL and SQL Server
- `ZeroAlloc.Scheduling.Redis`: Redis job store
- `ZeroAlloc.Scheduling.Mediator`: dispatches jobs via `IMediator.Send`
- `ZeroAlloc.Scheduling.Resilience`: wraps job executors in a ZeroAlloc.Resilience proxy
- `ZeroAlloc.Scheduling.Telemetry`: source-generated OpenTelemetry proxy around job execution
- `ZeroAlloc.Scheduling.Dashboard`: Minimal API dashboard with JSON endpoints and an embedded UI
- `ZeroAlloc.Scheduling.Dashboard.Blazor`: Blazor dashboard components

---

## ZeroAlloc.Serialisation

Source-generated, zero-allocation serialization for .NET 8+. Annotate a type with `[ZeroAllocSerializable]` — the Roslyn generator emits a sealed `{TypeName}Serializer : ISerializer<T>` and a per-type DI extension method. A `SerializerDispatcher` covering all annotated types in the assembly is also generated. No reflection, no `byte[]` intermediate allocation, fully Native AOT safe.

```csharp
[MemoryPackable]
[ZeroAllocSerializable(SerializationFormat.MemoryPack)]
public partial class OrderPlacedEvent
{
    public Guid OrderId { get; set; }
    public decimal Total { get; set; }
}

// Generated: OrderPlacedEventSerializer + AddOrderPlacedEventSerializer()
services.AddOrderPlacedEventSerializer();  // registers ISerializer<OrderPlacedEvent>
services.AddSerializerDispatcher();        // optional: ISerializerDispatcher over all [ZeroAllocSerializable] types

public class OrderStore(ISerializer<OrderPlacedEvent> serializer)
{
    public void Write(IBufferWriter<byte> writer, OrderPlacedEvent evt)
        => serializer.Serialize(writer, evt);         // writes directly to IBufferWriter<byte> — zero intermediate byte[]

    public OrderPlacedEvent? Read(ReadOnlySpan<byte> bytes)
        => serializer.Deserialize(bytes);
}
```

Backends: `ZeroAlloc.Serialisation.MemoryPack`, `ZeroAlloc.Serialisation.MessagePack`, `ZeroAlloc.Serialisation.SystemTextJson`.

---

## ZeroAlloc.Specification

Source-generated specification pattern for .NET 8+. Decorate a `readonly partial struct` with `[Specification]` — the Roslyn generator emits `And<TOther>()`, `Or<TOther>()`, and `Not()` fluent combinators. Composed specs stay `readonly struct` values: zero heap allocation, no closures. Every spec exposes `ToExpression()` returning `Expression<Func<T, bool>>` for direct use with EF Core `Where()`. `ZeroAlloc.Specification` bundles its source generator, so it is the only package to install. Compile-time diagnostics ZA001–ZA005 enforce correct usage.

```bash
dotnet add package ZeroAlloc.Specification
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

## ZeroAlloc.StateMachine

Source-generated, zero-allocation finite state machines for .NET. Add `[StateMachine]` and `[Transition<TState, TTrigger>]` attributes to a `partial` class or struct — the generator emits a `TryFire(TTrigger)` method as a `switch` expression over `(TState, TTrigger)` tuples. No dictionary, no delegate dispatch, no heap allocation on the transition path. AOT-safe.

```csharp
public enum State   { Idle, Pending, Done }
public enum Trigger { Submit, Pay }

[StateMachine(InitialState = nameof(State.Idle))]
[Transition<State, Trigger>(From = State.Idle,    On = Trigger.Submit, To = State.Pending)]
[Transition<State, Trigger>(From = State.Pending, On = Trigger.Pay,    To = State.Done)]
[Terminal<State>(State = State.Done)]
public partial class OrderMachine { }

var machine = new OrderMachine();
machine.TryFire(Trigger.Submit);   // → State.Pending
machine.TryFire(Trigger.Pay);      // → State.Done (terminal)
```

---

## ZeroAlloc.Telemetry

Source-generated OpenTelemetry proxy for .NET 8+. Annotate an interface with `[Instrument]` — the Roslyn generator emits a sealed decorator class that wraps an inner implementation and records `ActivitySource` spans, `Counter<long>` increments, and `Histogram<double>` timings per method. No OpenTelemetry SDK dependency, no reflection, fully Native AOT safe.

```csharp
[Instrument("MyApp.Orders")]
public interface IOrderService
{
    [Trace("order.create")]
    [Count("orders.created")]
    ValueTask<OrderId> CreateOrderAsync(CreateOrderCommand cmd, CancellationToken ct);

    [Trace("order.get")]
    [Histogram("order.get_ms")]
    ValueTask<Order> GetOrderAsync(OrderId id, CancellationToken ct);
}

// Generated: OrderServiceInstrumented — wire up as a DI decorator
services.AddSingleton<OrderServiceImpl>();
services.AddSingleton<IOrderService>(sp =>
    new OrderServiceInstrumented(sp.GetRequiredService<OrderServiceImpl>()));

// Add any exporter — the library emits standard BCL ActivitySource and Meter
builder.Services.AddOpenTelemetry()
    .WithTracing(t => t.AddSource("MyApp.Orders").AddOtlpExporter())
    .WithMetrics(m => m.AddMeter("MyApp.Orders").AddOtlpExporter());
```

| Call outcome | `[Trace]` span | `[Count]` counter | `[Histogram]` |
|---|---|---|---|
| Success | Started + stopped | Incremented by 1 | Records elapsed ms |
| Exception | Started + Error status set | Not incremented | Records elapsed ms |

---

## ZeroAlloc.Templates

`dotnet new` Web API templates that wire the ecosystem together, so a new service starts AOT-safe rather than being retrofitted later.

```bash
dotnet new install ZeroAlloc.Templates

dotnet new za-clean -o MyApp              # Clean Architecture, four layered projects
dotnet new za-vertical-slice -o MyApp     # one project, one folder per use case
```

| Short name | Architecture | When to pick it |
|---|---|---|
| `za-clean` | Four layered projects (Domain / Application / Infrastructure / Api) with NetArchTest boundary rules | Familiar to teams already running layered architectures; horizontal boundaries lock concerns in place |
| `za-vertical-slice` | One src project, one file per slice — request, validator, handler, endpoint and entity co-located | Lower ceremony; each feature reads top to bottom in ~50–100 lines |

Both reference the same 11 ZeroAlloc libraries (Mediator, Validation, Authorization, Mapping, ValueObjects, Inject, Resilience, Rest, Results, ORM, Serialisation), and `za-vertical-slice` adds ZeroAlloc.Telemetry. They share the same SQLite persistence through ZeroAlloc.ORM with no `DbContext`, and the same xUnit + BenchmarkDotNet + NBomber fan-out. Otherwise they differ in arrangement, not capability — pick on team comfort.

---

## ZeroAlloc.TestHelpers

Test helpers distributed as source rather than as a runtime dependency. `AllocationGate` asserts an allocation budget over a warmed, GC-settled loop, which is how the libraries here keep their zero-allocation claims honest instead of asserting them once and hoping.

```csharp
AllocationGate.AssertBudget(
    budgetBytes: 0,
    iterations: 1000,
    action: () => validator.Validate(model),
    label: "valid path");
```

`AssertBudgetValueTask<T>` covers `ValueTask<T>`-returning APIs and fails if the task did not complete synchronously, since the awaiter machinery would otherwise pollute the measurement. For calls that really complete on another thread, `AssertBudgetAsync` and `AssertNoMoreThanAsync` count allocations on every thread.

`TextSnapshot` and `GeneratorSnapshot` add snapshot testing for strings and source-generator output; `GeneratorSnapshot` is compiled only when the consuming project references Roslyn.

The package contributes three source files that compile into the consuming assembly as `internal`, so test infrastructure never reaches a package's public API surface and costs nothing at consumer runtime.

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

**Integration packages**

- `ZeroAlloc.Validation.AspNetCore`: source-generated action filter that validates request models
- `ZeroAlloc.Validation.Inject`: generates `AddZeroAllocValidators()` for reflection-free DI registration
- `ZeroAlloc.Validation.Options`: plugs validators into Microsoft.Extensions.Options
- `ZeroAlloc.Validation.Testing`: assertion helpers for validation results

---

## ZeroAlloc.ValueObjects

Source-generated `Equals`, `GetHashCode`, `==`/`!=` and `ToString()` for your existing `partial class` and `partial struct` types. The equality members make **zero allocations**, with no boxing and no iterator state machines; `ToString()` returns a new string.

Targets users of `CSharpFunctionalExtensions.ValueObject` where `GetEqualityComponents()` allocates on every equality check, but works equally well as a lightweight alternative to `record` when you can't or don't want to change the type keyword.

```csharp
// Drop onto any existing partial class — no keyword changes required
[ValueObject]
public partial class Money
{
    public decimal Amount { get; }
    public string Currency { get; }
}

[ValueObject]
public partial struct CustomerId
{
    public Guid Value { get; }
}

// Generated: Equals, GetHashCode (HashCode.Combine), ==, != — zero alloc — plus ToString
```

Fine-grained control via `[EqualityMember]` (opt-in) and `[IgnoreEqualityMember]` (opt-out) attributes.

`[TypedId]` generates strongly-typed IDs on a `readonly partial record struct`: ULID, UUIDv7, Snowflake or sequential values, with `New()`, `Parse`, `IParsable`/`ISpanParsable`, an AOT-safe JSON converter and EF Core conventions.

```csharp
[TypedId(Strategy = IdStrategy.Ulid)]
public readonly partial record struct OrderId;

OrderId id = OrderId.New();          // monotonic ULID, 26-char base32 string form
OrderId parsed = OrderId.Parse(id.ToString());
```

**Benchmark** (i9-12900HK, .NET 9):

| Method | Mean | Allocated | Speedup vs CFE |
|---|---:|---:|:---:|
| CFE_Equals | 45.2 ns | 96 B | — |
| Record_Equals | 3.1 ns | 0 B | 14.6× |
| **ZeroAlloc_Equals** | **3.1 ns** | **0 B** | **~15×** |
| CFE_GetHashCode | 38.7 ns | 88 B | — |
| Record_GetHashCode | 2.4 ns | 0 B | 16.1× |
| **ZeroAlloc_GetHashCode** | **2.4 ns** | **0 B** | **~16×** |

**Integration packages**

- `ZeroAlloc.ValueObjects.EfCore`: EF Core value converters and conventions for `[TypedId]` structs
- `ZeroAlloc.ValueObjects.Hosting`: host-integrated Snowflake worker-id registration

---

## Built on ZeroAlloc

Projects that use these libraries in practice:

- [AI.Sentinel](https://github.com/MarcelRoozekrans/AI.Sentinel): security monitoring middleware for `IChatClient`, using ZeroAlloc.Analyzers and ZeroAlloc.Authorization.
- [Minos.NET](https://github.com/MarcelRoozekrans/Minos.NET): typed, source-generated decision questions, using Analyzers, Resilience, Rest, Results, Telemetry and Validation.
- [Rag.NET](https://github.com/MarcelRoozekrans/Rag.NET): a modular retrieval-augmented generation pipeline, using Analyzers, Mediator, Inject, Pipeline, Rest, Results, Specification, Validation and ValueObjects.
- [Roslyn CodeLens MCP](https://github.com/MarcelRoozekrans/roslyn-codelens-mcp): semantic .NET code intelligence for AI agents, using Analyzers.
- [MemoryLens MCP](https://github.com/MarcelRoozekrans/memorylens-mcp): on-demand .NET memory profiling for AI agents, using Analyzers.

---

## Sponsor

ZeroAlloc-Net is maintained in spare time. If these libraries save you allocations, GC pauses, or migration effort, consider sponsoring to keep the work going.

[![Sponsor ZeroAlloc-Net](https://img.shields.io/badge/Sponsor_ZeroAlloc--Net-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/ZeroAlloc-Net)
[![Sponsor Marcel Roozekrans](https://img.shields.io/badge/Sponsor_Marcel-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/MarcelRoozekrans)

**What sponsorship funds:**
- Continued maintenance and .NET version upgrades across all packages
- New packages and source generator improvements
- Keeping everything Native AOT-compatible as the ecosystem evolves

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
