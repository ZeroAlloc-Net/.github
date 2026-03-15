<p align="center">
  <img src="banner.svg" alt="ZeroAlloc-Net" width="860"/>
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
| [ZeroAlloc.Inject](https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject) | Compile-time dependency injection via Roslyn source generator | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Inject.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Inject) |

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

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
