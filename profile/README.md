<p align="center">
  <img src="https://raw.githubusercontent.com/ZeroAlloc-Net/.github/main/profile/banner.svg" alt="ZeroAlloc-Net" width="860"/>
</p>

## About

**ZeroAlloc-Net** is home to a family of high-performance .NET libraries built around three principles:

- **Zero allocations** — no heap pressure at steady state
- **Native AOT compatible** — no reflection, no runtime code generation
- **Compile-time correctness** — errors and wiring validated by Roslyn at build time, not at startup

Everything here targets .NET 8+ and is designed to work end-to-end with `PublishAot=true`.

---

## Packages

| Package | Description | NuGet |
|---|---|---|
| [ZeroAlloc.Analyzers](https://github.com/ZeroAlloc-Net/ZeroAlloc.Analyzers) | Roslyn analyzers for modern .NET performance patterns | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Analyzers.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Analyzers) |
| [ZeroAlloc.Inject](https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject) | Compile-time dependency injection via Roslyn source generator | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Inject.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Inject) |
| [ZeroAlloc.Mediator](https://github.com/ZeroAlloc-Net/ZeroAlloc.Mediator) | Zero-allocation mediator library with source-generated dispatch | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Mediator.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Mediator) |

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

## Design Philosophy

> If it needs reflection at runtime, it doesn't belong here.

All libraries in this org follow the same contract: the heavy work happens at compile time via Roslyn source generators or compile-time analysis. The runtime path is a straight line — no dictionaries, no `Type.GetMethod`, no dynamic dispatch.

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

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
