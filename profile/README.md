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
| ZeroAlloc.Options *(coming soon)* | Source-generated options validation — replaces data annotation reflection with compile-time generated validators | — |
| ZeroAlloc.Mapping *(coming soon)* | Source-generated object mapping — zero-allocation compile-time type mappings, no reflection | — |

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

| Scenario | ZeroAlloc.Inject | Microsoft DI |
|---|---|---|
| Resolve transient | ~3 ns | ~35 ns |
| Resolve singleton | ~1 ns | ~8 ns |
| Open generic (closed at compile time) | ~19 ns | N/A (AOT unsafe) |

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

| Scenario | ZeroAlloc.Mediator | MediatR |
|---|---|---|
| Send | ~2 ns | ~88 ns |
| Publish Single | ~6 ns | ~222 ns |
| Publish Multi | ~5 ns | ~299 ns |

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

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
