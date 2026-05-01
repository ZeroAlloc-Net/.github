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
| [ZeroAlloc.ValueObjects](https://github.com/ZeroAlloc-Net/ZeroAlloc.ValueObjects) | Zero-allocation source-generated ValueObject equality for existing domain types | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.ValueObjects.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.ValueObjects) |
| [ZeroAlloc.Inject](https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject) | Compile-time dependency injection via Roslyn source generator | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Inject.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Inject) |
| [ZeroAlloc.Pipeline](https://github.com/ZeroAlloc-Net/ZeroAlloc.Pipeline) | Shared compile-time pipeline infrastructure — `IPipelineBehavior` interface and Roslyn discovery/emission utilities for ZeroAlloc generators | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Pipeline.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Pipeline) |
| [ZeroAlloc.Mediator](https://github.com/ZeroAlloc-Net/ZeroAlloc.Mediator) | Zero-allocation mediator library with source-generated dispatch | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Mediator.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Mediator) |
| [ZeroAlloc.Validation](https://github.com/ZeroAlloc-Net/ZeroAlloc.Validation) | Source-generated validation API — zero allocations, no reflection, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Validation.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Validation) |
| [ZeroAlloc.Results](https://github.com/ZeroAlloc-Net/ZeroAlloc.Results) | Zero-allocation `Result<T, E>` — no boxing, no heap pressure, full combinator API with async and LINQ support | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Results.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Results) |
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
| [ZeroAlloc.Collections](https://github.com/ZeroAlloc-Net/ZeroAlloc.Collections) | Zero-allocation pooled collection types — PooledList, RingBuffer, SpanDictionary, PooledStack, PooledQueue, and FixedSizeList with `ref struct` and heap variants | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Collections.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Collections) |
| [ZeroAlloc.AsyncEvents](https://github.com/ZeroAlloc-Net/ZeroAlloc.AsyncEvents) | Zero-allocation async event primitives — lock-free registration, `ValueTask` invocation, `ArrayPool` parallel dispatch, source-generated `[AsyncEvent]` wiring | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.AsyncEvents.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.AsyncEvents) |
| [ZeroAlloc.Notify](https://github.com/ZeroAlloc-Net/ZeroAlloc.Notify) | Source-generated async INPC — fully awaitable `PropertyChangedAsync`/`CollectionChangedAsync` dispatch, no reflection, compile-time wiring | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Notify.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Notify) |
| [ZeroAlloc.Rest](https://github.com/ZeroAlloc-Net/ZeroAlloc.Rest) | Source-generated Native AOT REST client — define an interface, Roslyn emits a type-safe `HttpClient` implementation at compile time, zero reflection at runtime | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Rest.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Rest) |
| [ZeroAlloc.Serialisation](https://github.com/ZeroAlloc-Net/ZeroAlloc.Serialisation) | Source-generated `ISerializer<T>` — annotate a type, Roslyn emits a sealed serializer and DI extension. Backends for MemoryPack, MessagePack, and System.Text.Json. No reflection, no boxing, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Serialisation.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Serialisation) |
| [ZeroAlloc.EventSourcing](https://github.com/ZeroAlloc-Net/ZeroAlloc.EventSourcing) | Zero-allocation event sourcing — struct-based aggregate state, in-memory and SQL backends, source-generated boilerplate, optional OpenTelemetry instrumentation | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.EventSourcing.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.EventSourcing) |
| [ZeroAlloc.Telemetry](https://github.com/ZeroAlloc-Net/ZeroAlloc.Telemetry) | Source-generated OpenTelemetry proxy — annotate an interface, Roslyn emits a BCL `ActivitySource` + `Meter` decorator. No OTel SDK dependency, Native AOT safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Telemetry.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Telemetry) |
| [ZeroAlloc.Scheduling](https://github.com/ZeroAlloc-Net/ZeroAlloc.Scheduling) | Source-generated background job scheduler — `[Job]` annotation wires up executor, DI registration, and recurring startup at compile time. InMemory, EF Core, and Redis backends | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Scheduling.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Scheduling) |
| [ZeroAlloc.Cache](https://github.com/ZeroAlloc-Net/ZeroAlloc.Cache) | Source-generated caching proxy — annotate an interface with `[Cache]`, Roslyn emits a transparent proxy with zero allocation on the cache-hit path. `IMemoryCache` and `HybridCache` backends | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Cache.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Cache) |
| [ZeroAlloc.Resilience](https://github.com/ZeroAlloc-Net/ZeroAlloc.Resilience) | Source-generated resilience policies — `[Retry]`, `[Timeout]`, `[RateLimit]`, and `[CircuitBreaker]` compose into a generated proxy with zero heap allocation on the happy path | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Resilience.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Resilience) |
| [ZeroAlloc.StateMachine](https://github.com/ZeroAlloc-Net/ZeroAlloc.StateMachine) | Source-generated finite state machines — `[Transition<TState, TTrigger>]` attributes lower to a `switch` expression over tuples. No dictionary, no delegate dispatch, AOT-safe | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.StateMachine.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.StateMachine) |
| [ZeroAlloc.Outbox](https://github.com/ZeroAlloc-Net/ZeroAlloc.Outbox) | Source-generated transactional outbox — `[OutboxMessage]` emits a typed writer and dispatcher bridge. EF Core (production) and InMemory (tests) stores, polling worker, exponential-backoff retry, dead-letter | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Outbox.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Outbox) |
| [ZeroAlloc.Saga](https://github.com/ZeroAlloc-Net/ZeroAlloc.Saga) | Source-generated long-running process orchestration — declare a saga as a `partial class`, the generator emits state machine, notification handlers, and dispatch wiring. Compensation runs in reverse on failure | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Saga.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Saga) |
| [ZeroAlloc.Authorization](https://github.com/ZeroAlloc-Net/ZeroAlloc.Authorization) | Authorization primitives — `[Authorize]` attribute + `IAuthorizationPolicy` contract + `ISecurityContext` for hosts to extend. Source-of-truth contract package consumed by AI.Sentinel and the planned ZeroAlloc.Mediator.Authorization | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Authorization.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Authorization) |

---

## ZeroAlloc.Analyzers

**42+ Roslyn analyzers** that detect allocation-heavy patterns and suggest zero/low-allocation alternatives. Fully aware of target framework version — rules automatically enable/disable based on `TargetFramework`.

Rules cover collections, strings, memory, logging, LINQ, async/await, serialization, and more. Common checks include:

- `ZA0101`: Use `FrozenDictionary` for read-only dictionaries
- `ZA0109`: Avoid zero-length array allocation — use `Array.Empty()`
- `ZA0201`: Avoid string concatenation in loops
- `ZA0603`: Use `.Count`/`.Length` instead of LINQ `.Count()`
- `ZA1001`: Use JSON source generation instead of reflection
- `ZA1401`: Use static lambda when no capture needed

Designed to complement existing analyzers and catch subtle allocation bugs at build time.

---

## ZeroAlloc.ValueObjects

Source-generated `Equals`, `GetHashCode`, `==`/`!=`, and `ToString()` for your existing `partial class` and `partial struct` types — **zero allocations**, no boxing, no iterator state machines.

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

// Generated: Equals, GetHashCode (HashCode.Combine), ==, !=, ToString — zero alloc
```

Fine-grained control via `[EqualityMember]` (opt-in) and `[IgnoreEqualityMember]` (opt-out) attributes.

**Benchmark** (i9-12900HK, .NET 9):

| Method | Mean | Allocated | Speedup vs CFE |
|---|---:|---:|:---:|
| CFE_Equals | 45.2 ns | 96 B | — |
| Record_Equals | 3.1 ns | 0 B | 14.6× |
| **ZeroAlloc_Equals** | **3.1 ns** | **0 B** | **~15×** |
| CFE_GetHashCode | 38.7 ns | 88 B | — |
| Record_GetHashCode | 2.4 ns | 0 B | 16.1× |
| **ZeroAlloc_GetHashCode** | **2.4 ns** | **0 B** | **~16×** |

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

**Benchmark** (i9-12900HK, .NET 9):

| Scenario | ZeroAlloc.Inject | Microsoft DI | Speedup |
|---|---|---|:---:|
| Resolve transient | ~3 ns | ~35 ns | **~12×** |
| Resolve singleton | ~1 ns | ~8 ns | **8×** |
| Open generic (closed at compile time) | ~19 ns | N/A (AOT unsafe) | — |

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

## ZeroAlloc.Mediator

Compile-time wired mediator for request/response, notifications, and streaming with **zero allocations** on all dispatch paths. Pipeline behaviors are inlined as static nested calls with no closure allocation.

```csharp
public readonly record struct Ping(string Message) : IRequest<string>;

public class PingHandler : IRequestHandler<Ping, string>
{
    public ValueTask<string> Handle(Ping request, CancellationToken ct)
        => ValueTask.FromResult($"Pong: {request.Message}");
}

// Generated mediator with strongly-typed Send/Publish/CreateStream overloads
var result = await Mediator.Send(new Ping("Hello"), ct); // ~2 ns, 0 bytes
```

**Benchmark** (i9-12900HK, .NET 10):

| Scenario | ZeroAlloc.Mediator | MediatR | Speedup |
|---|---|---|:---:|
| Send | ~2 ns | ~88 ns | **44×** |
| Publish Single | ~6 ns | ~222 ns | **37×** |
| Publish Multi | ~5 ns | ~299 ns | **~60×** |

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

---

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
| `Match` | 0.37 ns | 0.68 ns | **0 B** both | **1.8×** |
| `Chain` (Map+Bind+Match) | 2.28 ns | 2.45 ns | **0 B** both | **1.1×** |

---

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

## ZeroAlloc.Collections

Six zero-allocation collection types for .NET, each available as a `ref struct` for stack-only scenarios and as a heap class for use in async code and DI. All collections rent their backing storage from `ArrayPool<T>.Shared` and return it on `Dispose()`. Every type exposes `AsSpan()` and `AsReadOnlySpan()` for zero-copy inner loops. An optional source generator can emit additional type-specific collection variants and `ref struct` enumerators at compile time — no reflection, fully Native AOT compatible.

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

**Benchmark** (BenchmarkDotNet v0.14.0, .NET 9, X64 — 10 handlers, invoked once):

| Method | Mean | Ratio | Allocated |
|---|---:|:---:|:---:|
| Sync multicast delegate (baseline) | 22.96 ns | 1.0× | — |
| Naive async (`Task.WhenAll`) | 203.48 ns | 8.96× | 280 B |
| ZeroAlloc Parallel | 70.10 ns | 3.09× | 136 B |
| **ZeroAlloc Sequential** | **16.10 ns** | **0.71×** | **0 B** |

Sequential mode is **30% faster than a sync multicast delegate** at zero allocations. Parallel mode is **3× faster than naive `Task.WhenAll`** with 51% less memory.

---

## ZeroAlloc.Notify

Source-generated async `INotifyPropertyChanged` for .NET 8+. Decorate a `partial` class with `[NotifyPropertyChangedAsync]` and mark backing fields with `[ObservableProperty]` — the Roslyn generator emits `PropertyChangedAsync`, `CollectionChangedAsync`, and strongly-typed `Set*Async` methods at compile time. No reflection, no virtual dispatch, fully awaitable `ValueTask` handlers. The only INPC framework in the .NET ecosystem where `await vm.SetNameAsync(...)` truly awaits all registered handlers.

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

**Benchmark** (i9-12900HK, .NET 10, BenchmarkDotNet):

| Method | Mean | Allocated | vs Baseline |
|---|---:|:---:|:---:|
| Sync `INotifyPropertyChanged` (baseline) | 21.41 ns | 24 B | — |
| CommunityToolkit.Mvvm *(sync only)* | 31.27 ns | 0 B | 1.47× slower |
| PropertyChanged.Fody *(sync only)* | 17.57 ns | 0 B | 1.22× faster |
| **ZeroAlloc.Notify** *(fully awaitable)* | **61.84 ns** | **48 B** | **only async-first** |

CommunityToolkit and Fody dispatch synchronously and cannot await async handlers. ZeroAlloc.Notify trades ~3× overhead for first-class `ValueTask` semantics — the right trade-off when handlers do I/O.

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

// DI registration — AddIUserApi extension generated by the source generator
builder.Services.AddIUserApi(options =>
{
    options.BaseAddress = new Uri("https://api.example.com");
    options.UseSerializer<SystemTextJsonSerializer>();
});

// Inject and use — no reflection, no proxies at runtime
public class UserService(IUserApi api)
{
    public Task<UserDto> GetAsync(int id) => api.GetUserAsync(id);
}
```

**Benchmark** (i9-12900HK, .NET 10.0.4, Windows 11, X64 — in-memory handler, no real network I/O):

| Method | Mean | vs Refit | Allocated |
|---|---:|:---:|---:|
| Raw `HttpClient` (baseline) | 1,648 ns | — | 1.38 KB |
| **ZeroAlloc.Rest GET** | **1,933 ns** | **3.2× faster** | 1.74 KB |
| Refit GET | 6,123 ns | 1× | 3.03 KB |
| **ZeroAlloc.Rest QueryParam** | **2,474 ns** | **5.5× faster** | 1.85 KB |
| Refit QueryParam | 13,509 ns | 1× | 3.67 KB |

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
services.AddSerializerDispatcher();  // covers all [ZeroAllocSerializable] types in the assembly

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

## ZeroAlloc.EventSourcing

Zero-allocation event sourcing for .NET 8+. Struct-based aggregate state keeps the read path off the heap. In-memory and SQL backends (SQL Server / PostgreSQL). Source generator emits aggregate boilerplate. First-class integration with `ZeroAlloc.Serialisation` for AOT-safe event serialization.

```csharp
// Define aggregate state as a struct — zero heap allocation on read
public readonly record struct OrderState(string OrderId, decimal Total, bool Placed);

public sealed class OrderAggregate : Aggregate<OrderState>
{
    public Result<Unit, string> Place(string orderId, decimal total)
    {
        if (State.Placed) return "already placed";
        Raise(new OrderPlacedEvent(orderId, total));
        return Unit.Value;
    }

    protected override OrderState Apply(OrderState state, object @event) => @event switch
    {
        OrderPlacedEvent e => state with { OrderId = e.OrderId, Total = e.Total, Placed = true },
        _ => state,
    };
}

// Wire up DI
services
    .AddEventSourcing()
    .UseInMemoryEventStore();   // swap for .UsePostgreSqlEventStore(cs) in production

// Use
var repo = sp.GetRequiredService<IAggregateRepository<OrderAggregate, string>>();
var order = new OrderAggregate();
order.Place("order-1", 99.99m);
await repo.SaveAsync("order-1", order, CancellationToken.None);
```

Optional `ZeroAlloc.EventSourcing.Telemetry` package adds BCL-based `ActivitySource` + `Meter` instrumentation with no OpenTelemetry SDK dependency.

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

## ZeroAlloc.Scheduling

Source-generated background job scheduler for .NET 8 and .NET 10. Decorate any class with `[Job]` and the generator emits the executor, DI registration, and recurring startup wiring — no reflection, no convention scanning at runtime. InMemory, EF Core, and Redis backends.

```csharp
[Job(Every = Every.Hour)]
public sealed class CleanupExpiredSessionsJob : IJob
{
    public ValueTask ExecuteAsync(JobContext ctx, CancellationToken ct)
        => /* work */ ValueTask.CompletedTask;
}

// Generated DI extension wires executor + recurring schedule
builder.Services.AddZeroAllocScheduling().UseInMemory();
```

---

## ZeroAlloc.Cache

Source-generated zero-allocation caching proxy for .NET. Annotate an interface with `[Cache]`, the Roslyn generator emits a proxy that transparently intercepts every method call — **zero heap allocation on the cache-hit path**. Backed by `IMemoryCache` by default, with optional `HybridCache` (L1 + L2) opt-in per method. AOT-safe.

```csharp
[Cache(TtlMs = 60_000)]
public interface IProductRepository
{
    ValueTask<Product?> GetByIdAsync(int id, CancellationToken ct);

    [Cache(TtlMs = 300_000, MaxEntries = 1_000)]
    ValueTask<IReadOnlyList<Product>> SearchAsync(string query, CancellationToken ct);
}

// One line wires proxy + backing implementation
builder.Services.AddIProductRepositoryCache<ProductRepositoryImpl>();
```

Inject `IProductRepository` anywhere — caching is transparent to the caller.

---

## ZeroAlloc.Resilience

Source-generated, zero-allocation resilience policies for .NET. Add `[Retry]`, `[Timeout]`, `[RateLimit]`, and `[CircuitBreaker]` to an interface — the generator emits a proxy that composes all policies in declaration order with **no heap allocation on the happy path** (beyond the unavoidable `CancellationTokenSource` for timeout). AOT-safe.

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

## ZeroAlloc.Outbox

Source-generated transactional outbox for .NET. Annotate a message type with `[OutboxMessage]` and the Roslyn generator emits a typed writer and dispatcher bridge — no reflection, no boxing, AOT-safe. Backed by EF Core (production) or in-memory (tests), with a built-in polling worker, exponential-backoff retry, and dead-letter support.

```csharp
[OutboxMessage]
public sealed record OrderPlaced(Guid OrderId, decimal Total);

// Inside a transaction — write the row in the same DbContext as your domain change
await _outbox.WriteAsync(new OrderPlaced(orderId, total), ct);
await _db.SaveChangesAsync(ct);

// Polling worker dispatches in the background — at-least-once delivery, retry + DLQ baked in
services.AddZeroAllocOutbox().UseEfCore<MyDbContext>();
```

---

## ZeroAlloc.Saga

Source-generated long-running process orchestration for .NET. Declare a saga as a `partial class` decorated with `[Saga]` — the generator emits state-machine code, notification handlers, and dispatch wiring. Compensation runs in reverse on failure. No reflection, no open-generic resolution at runtime. v1.1 ships durable persistence via `ZeroAlloc.Saga.EfCore` (single shared `SagaInstance` table, row-version OCC, retry-on-conflict). InMemory remains the default; switch to EfCore with one fluent call.

```csharp
[Saga]
public partial class OrderFulfillmentSaga
{
    public OrderId OrderId { get; private set; }

    [StartedBy] public ValueTask Handle(OrderPlaced evt, ISagaContext ctx) { /* ... */ }
    [Step]      public ValueTask Handle(PaymentReceived evt, ISagaContext ctx) { /* ... */ }
    [Compensate(nameof(Handle))] public ValueTask CompensatePayment(ISagaContext ctx) { /* ... */ }
}

// Default in-memory; swap to durable EF Core with one call
services.AddZeroAllocSaga().UseEfCore<MyDbContext>();
```

---

## ZeroAlloc.Authorization

Source-of-truth authorization primitives for .NET. Five contract types — `ISecurityContext`, `IAuthorizationPolicy`, `[Authorize]`, `[AuthorizationPolicy]`, `AnonymousSecurityContext` — designed to be shared across hosts that need a unified policy contract. Pure contracts: no dispatch, no DI registration, no scanning. Hosts (AI.Sentinel for tool-call authz, the planned ZeroAlloc.Mediator.Authorization for handler authz) provide those.

```csharp
[AuthorizationPolicy("AdminOnly")]
public sealed class AdminOnlyPolicy : IAuthorizationPolicy
{
    public bool IsAuthorized(ISecurityContext ctx) => ctx.Roles.Contains("Admin");
}

public sealed class UserService
{
    [Authorize("AdminOnly")]
    public Task DeleteUserAsync(string userId) { /* ... */ }
}
```

For richer deny information, override `Evaluate` to return `UnitResult<AuthorizationFailure>` with a structured `Code` (e.g. `"policy.deny.role"`) and optional `Reason`. Native AOT compatible. Zero allocation on all four hot-path methods (`IsAuthorized`, `IsAuthorizedAsync`, `Evaluate`, `EvaluateAsync` happy path).

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
