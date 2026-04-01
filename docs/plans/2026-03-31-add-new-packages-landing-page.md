# Add New Packages to GitHub Landing Page — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add ZeroAlloc.Collections, ZeroAlloc.AsyncEvents, ZeroAlloc.Notify, and ZeroAlloc.Rest to `profile/README.md` — packages table rows + full sections with description, code snippet, and benchmark table for each.

**Architecture:** Pure docs change. Edit a single file (`profile/README.md`). No tests. One commit per package section addition, plus one for the table rows. PR against `main` at the end.

**Tech Stack:** Markdown, GitHub-flavored markdown tables, NuGet badge shields.io format matching the rest of the file.

---

### Task 1: Create feature branch

**Files:**
- No file changes — branch setup only

**Step 1: Create and switch to feature branch**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" checkout -b docs/add-new-packages-landing-page
```

Expected: `Switched to a new branch 'docs/add-new-packages-landing-page'`

---

### Task 2: Add 4 new rows to the packages table

**Files:**
- Modify: `profile/README.md` (packages table, after the `ZeroAlloc.Specification` row)

**Step 1: Locate the insertion point**

In `profile/README.md`, find this line (currently the last row in the table):

```
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
```

**Step 2: Insert 4 new rows immediately after it**

The `old_string` to match (the Specification row):

```
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
```

Replace with:

```
| [ZeroAlloc.Specification](https://github.com/ZeroAlloc-Net/ZeroAlloc.Specification) | Source-generated specifications — compile-time `And`/`Or`/`Not` composition, zero closure allocations, EF Core compatible | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Specification.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Specification) |
| [ZeroAlloc.Collections](https://github.com/ZeroAlloc-Net/ZeroAlloc.Collections) | Zero-allocation pooled collection types — PooledList, RingBuffer, SpanDictionary, PooledStack, PooledQueue, and FixedSizeList with `ref struct` and heap variants | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Collections.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Collections) |
| [ZeroAlloc.AsyncEvents](https://github.com/ZeroAlloc-Net/ZeroAlloc.AsyncEvents) | Zero-allocation async event primitives — lock-free registration, `ValueTask` invocation, `ArrayPool` parallel dispatch, source-generated `[AsyncEvent]` wiring | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.AsyncEvents.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.AsyncEvents) |
| [ZeroAlloc.Notify](https://github.com/ZeroAlloc-Net/ZeroAlloc.Notify) | Source-generated async INPC — fully awaitable `PropertyChangedAsync`/`CollectionChangedAsync` dispatch, no reflection, compile-time wiring | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Notify.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Notify) |
| [ZeroAlloc.Rest](https://github.com/ZeroAlloc-Net/ZeroAlloc.Rest) | Source-generated Native AOT REST client — define an interface, Roslyn emits a type-safe `HttpClient` implementation at compile time, zero reflection at runtime | [![NuGet](https://img.shields.io/nuget/v/ZeroAlloc.Rest.svg?style=flat-square)](https://www.nuget.org/packages/ZeroAlloc.Rest) |
```

**Step 3: Commit**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" add profile/README.md
git -C "c:/Projects/Prive/ZeroAlloc.github" commit -m "docs: add Collections, AsyncEvents, Notify, Rest to packages table"
```

---

### Task 3: Add ZeroAlloc.Collections section

**Files:**
- Modify: `profile/README.md` (after `## ZeroAlloc.Specification` section, before the footer `<p align="center">`)

**Step 1: Locate the insertion point**

Find this block at the bottom of the file (the footer):

```
<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 2: Insert the Collections section before the footer**

The `old_string`:

```
<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

The `new_string`:

```
## ZeroAlloc.Collections

Six zero-allocation collection types for .NET, each available as a `ref struct` for stack-only scenarios and as a heap class for use in async code and DI. All collections rent their backing storage from `ArrayPool<T>.Shared` and return it on `Dispose()`. Every type exposes `AsSpan()` and `AsReadOnlySpan()` for zero-copy inner loops. Source generators emit type-specific collections and `ref struct` enumerators at compile time — no reflection, fully Native AOT compatible.

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
| `PooledList<T>` | Yes | `HeapPooledList<T>` | Pooled-backed growable list |
| `RingBuffer<T>` | Yes | `HeapRingBuffer<T>` | Fixed-capacity circular buffer |
| `SpanDictionary<TKey, TValue>` | Yes | `HeapSpanDictionary<TKey, TValue>` | Open-addressing hash map |
| `PooledStack<T>` | Yes | `HeapPooledStack<T>` | Pooled-backed LIFO stack |
| `PooledQueue<T>` | Yes | `HeapPooledQueue<T>` | Pooled-backed FIFO queue |
| `FixedSizeList<T>` | Yes | `HeapFixedSizeList<T>` | Stack-allocated fixed-capacity list |

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 3: Commit**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" add profile/README.md
git -C "c:/Projects/Prive/ZeroAlloc.github" commit -m "docs: add ZeroAlloc.Collections section to landing page"
```

---

### Task 4: Add ZeroAlloc.AsyncEvents section

**Files:**
- Modify: `profile/README.md` (after Collections section, before footer)

**Step 1: Locate the insertion point**

Find this line (end of the Collections section, just before the footer):

```
| `FixedSizeList<T>` | Yes | `HeapFixedSizeList<T>` | Stack-allocated fixed-capacity list |

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 2: Insert AsyncEvents section**

`old_string`:

```
| `FixedSizeList<T>` | Yes | `HeapFixedSizeList<T>` | Stack-allocated fixed-capacity list |

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

`new_string`:

```
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

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 3: Commit**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" add profile/README.md
git -C "c:/Projects/Prive/ZeroAlloc.github" commit -m "docs: add ZeroAlloc.AsyncEvents section to landing page"
```

---

### Task 5: Add ZeroAlloc.Notify section

**Files:**
- Modify: `profile/README.md` (after AsyncEvents section, before footer)

**Step 1: Locate the insertion point**

Find this block (end of the AsyncEvents section benchmark callout, just before the footer):

```
Sequential mode is **30% faster than a sync multicast delegate** at zero allocations. Parallel mode is **3× faster than naive `Task.WhenAll`** with 51% less memory.

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 2: Insert Notify section**

`old_string`:

```
Sequential mode is **30% faster than a sync multicast delegate** at zero allocations. Parallel mode is **3× faster than naive `Task.WhenAll`** with 51% less memory.

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

`new_string`:

```
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

**Benchmark** (.NET 10, i9-12900HK, BenchmarkDotNet):

| Method | Mean | Allocated | vs Baseline |
|---|---:|:---:|:---:|
| Sync `INotifyPropertyChanged` (baseline) | 21.41 ns | 24 B | — |
| CommunityToolkit.Mvvm *(sync only)* | 31.27 ns | 0 B | 1.47× slower |
| PropertyChanged.Fody *(sync only)* | 17.57 ns | 0 B | 1.22× faster |
| **ZeroAlloc.Notify** *(fully awaitable)* | **61.84 ns** | **48 B** | **only async-first** |

CommunityToolkit and Fody dispatch synchronously and cannot await async handlers. ZeroAlloc.Notify trades ~3× overhead for first-class `ValueTask` semantics — the right trade-off when handlers do I/O.

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 3: Commit**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" add profile/README.md
git -C "c:/Projects/Prive/ZeroAlloc.github" commit -m "docs: add ZeroAlloc.Notify section to landing page"
```

---

### Task 6: Add ZeroAlloc.Rest section

**Files:**
- Modify: `profile/README.md` (after Notify section, before footer)

**Step 1: Locate the insertion point**

Find this block (end of the Notify section, just before the footer):

```
CommunityToolkit and Fody dispatch synchronously and cannot await async handlers. ZeroAlloc.Notify trades ~3× overhead for first-class `ValueTask` semantics — the right trade-off when handlers do I/O.

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 2: Insert Rest section**

`old_string`:

```
CommunityToolkit and Fody dispatch synchronously and cannot await async handlers. ZeroAlloc.Notify trades ~3× overhead for first-class `ValueTask` semantics — the right trade-off when handlers do I/O.

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

`new_string`:

```
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

// DI registration — AddIUserApi generated by the source generator
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

**Benchmark** (.NET 10.0.4, Windows 11, X64 — in-memory handler, no real network I/O):

| Method | Mean | vs Refit | Allocated |
|---|---:|:---:|---:|
| Raw `HttpClient` (baseline) | 1,648 ns | — | 1.38 KB |
| **ZeroAlloc.Rest GET** | **1,933 ns** | **3.2× faster** | 1.74 KB |
| Refit GET | 6,123 ns | 1× | 3.03 KB |
| **ZeroAlloc.Rest QueryParam** | **2,474 ns** | **5.5× faster** | 1.85 KB |
| Refit QueryParam | 13,509 ns | 1× | 3.67 KB |

---

<p align="center">
  <sub>Built with ❤️ for the Native AOT era of .NET</sub>
</p>
```

**Step 3: Commit**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" add profile/README.md
git -C "c:/Projects/Prive/ZeroAlloc.github" commit -m "docs: add ZeroAlloc.Rest section to landing page"
```

---

### Task 7: Create pull request

**Step 1: Push the branch**

```bash
git -C "c:/Projects/Prive/ZeroAlloc.github" push -u origin docs/add-new-packages-landing-page
```

**Step 2: Create PR**

```bash
gh pr create \
  --repo ZeroAlloc-Net/.github \
  --base main \
  --head docs/add-new-packages-landing-page \
  --title "docs: add Collections, AsyncEvents, Notify, and Rest to landing page" \
  --body "$(cat <<'EOF'
## Summary

- Adds `ZeroAlloc.Collections`, `ZeroAlloc.AsyncEvents`, `ZeroAlloc.Notify`, and `ZeroAlloc.Rest` to the packages table in `profile/README.md`
- Adds a full section for each new package (description, code snippet, benchmark table) matching the style of existing sections
- Section order: …Specification → Collections → AsyncEvents → Notify → Rest → footer

## Test plan

- [ ] Verify the packages table renders correctly on GitHub (12 rows, badges resolve)
- [ ] Verify all 4 new sections render: headings, code blocks, benchmark tables
- [ ] Verify NuGet badge URLs are correct for each new package
- [ ] Verify GitHub repo links in the table point to the correct repos

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: PR URL printed to terminal. Return the URL to the user.
