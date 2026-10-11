# ZeroAlloc-Net: guidance for agents and contributors

Every ZeroAlloc-Net library makes two promises: it works under NativeAOT and trimming, and its hot path
allocates nothing. This file records what the 2026-10-11 org-wide sweep found when it checked those
promises, so the same mistakes are not made again. The sweep found no AOT breaks, but 16 of 28 repos
allocated on the hot path, and most of them had docs claiming 0 B. Search GitHub issues for "Found in the
2026-10-11 org-wide" to see every finding.

## 1. Know your hot path

The hot path is the operation a consumer runs repeatedly: `Send`, a cache hit, `Validate`, `Map`,
`Serialize`, a resilience call, building a REST request, a state transition, appending an event, a worker
poll. Startup, registration and configuration code are not hot path.

For a source generator, the hot path is the code it **emits**. Judge the snapshots and the generated output,
not the generator.

A worker or poll loop is hot path too, including the idle poll. A poll that allocates while doing nothing
costs memory all day.

## 2. Allocation patterns the sweep kept finding

None of these show up in a review unless you look for them. Each one shipped in at least one repo.

| Pattern | Where it hid | Instead |
|---|---|---|
| `async ValueTask` that only awaits and returns | AdoNet.Async adapters | `return new ValueTask<T>(inner.XAsync(ct));` when the method only forwards |
| `Task.WhenAll` when every task already completed | AsyncEvents, Mediator `[ParallelNotification]` | check `IsCompletedSuccessfully` first; only await what is pending |
| `TagList` / log `params object[]` built before checking `Enabled` or `IsEnabled` | Scheduling, Saga | check first, or use `LoggerMessage.Define` |
| allocating event args before checking for subscribers | Notify | copy the handler to a local, check, then allocate |
| `new Serializer()` / `new Utf8JsonWriter()` per call | Serialisation dispatcher and adapters | cache stateless instances; reuse writers with `Reset` |
| `GetString()` / `ToString()` round-trips in JSON converters | ValueObjects, Serialisation | parse and format through spans |
| `ToArray()` / `ToList()` copies between layers | EventSourcing append path, Outbox, MessagePack | pass `ReadOnlyMemory<T>` or spans through; copy once at most |
| LINQ in emitted code | Mapping nested collections | emit `for` loops |
| `yield` iterators returned from a public `GetEnumerator` | Collections Heap* types | a public struct enumerator; this is a breaking change once shipped, so do it first time |
| `Enum.IsDefined(typeof(E), value)`, `decimal.GetBits(value)` | Validation | `Enum.IsDefined<E>`, `value.Scale` |
| re-parsing or re-reading configuration per call | Scheduling cron, Snowflake env var | parse once and cache |
| an `AsyncLocal` write per call | Mediator 6.4.2 | pass state explicitly; write only when a consumer needs it |
| a capturing lambda or method-group delegate per call | Flux `InvokeAsync(StateHasChanged)`, Mediator DI chain | cache the delegate in a field, or use a static lambda |
| a per-key object that is never removed | Saga lock manager, InMemory job store | remove on release, or keep it off the scan path; this is a leak, not only an allocation |

Inherent allocations are fine when documented: the consumer's own result object, an exception on a failure
path, a one-time cache fill.

## 3. Prove it with tests, not benchmarks run by hand

- **Every hot path has an allocation gate test.** Use `AllocationGate` from ZeroAlloc.TestHelpers and
  measure the **whole** public call. The Mediator 72 B regression shipped because its gate set the state
  outside the measured region.
- **Budgets are exact, not generous.** A 512 B budget around a 32 B cost hides the next regression. If a
  path legitimately allocates, assert that number, and comment what it is.
- **Test the generated code**, not a hand-written stand-in. Templates benchmarked a `FakeMediator`; Flux and
  Saga had no allocation test for what they emit.
- **Cover every shape.** Validation tested many rules but not `[PrecisionScale]` or `[IsInEnum]`; Mapping
  tested flat members but not nested collections. Both allocated.
- **A test that measures async code must also cover the asynchronous case.** Synchronous in-memory SQLite
  never shows the cost of an `async` forwarder; use a fake that returns pending tasks.

## 4. Benchmarks

- Every repo runs its benchmarks in CI through the shared `benchmark-smoke.yml` workflow. Two Resilience
  benchmarks had crashed for months, and four AdoNet.Async XML benchmarks had never worked.
- Measure the library, not the harness: no allocation inside the benchmark body except what the library
  does. Allocating a new buffer, writer or machine per operation in the benchmark hides the real number.
- Target the library's LTS frameworks, so every code path that differs per framework is measured.
- Locally, run BenchmarkDotNet with `--inProcess`; deep worktree paths exceed MAX_PATH otherwise.

## 5. NativeAOT

- Every packable runtime project sets `IsAotCompatible=true` on its modern target frameworks, so the trim and
  AOT analyzers run. Projects that consumers publish, such as template projects, set it too.
- No reflection or runtime code generation on any supported path. An opt-in reflection fallback carries
  honest `[RequiresUnreferencedCode]` / `[RequiresDynamicCode]`.
- A suppression must be true. Remove dead ones; the sweep found suppressions justified by "no runtime code
  generation" on a path that does exactly that.
- The AOT smoke sample:
  - publishes with `TreatWarningsAsErrors=true`, not a list of six IL codes. If a third-party rollup warning
    really blocks it, name the assembly and exclude only that code with `WarningsNotAsErrors`.
  - exercises the hot path of **every** package in the repo, not only the core one. Adapter packages that
    need a live service are at least AOT-published in CI.
  - for apps and templates, makes real authenticated requests, not only an anonymous `/healthz`.

## 6. Docs must match measurements

Most failing repos claimed zero allocation somewhere they did not have it. When you change a hot path,
re-measure and update `docs/performance.md` and the README with the numbers you measured. Never write
"0 B" without a test that asserts it.

## 7. Wiring lessons from the templates

The templates are what adopters copy, so wiring mistakes there spread.

- Pin current package versions. Mediator 6.0.0 dropped behaviors from referenced packages, so validation
  and authorization silently never ran.
- `UseAccessor<T>()` resolves `T` from DI; it does not register it.
- The mediator validation behavior skips requests without a registered `ValidatorFor<T>`. Register
  validators with `AddZeroAllocValidators()` from ZeroAlloc.Validation.Inject.
- The validation and authorization behaviors return a failed `Result` only when the error type is
  `ValidationError` or `AuthorizationFailure`. For any other error type they throw, so the app needs an
  `IExceptionHandler` that maps the exceptions to 400 and 403.
- CI must send an invalid request and assert the 400. Nothing did, which is how this stayed hidden.

## 8. Shipping changes

- Fix review findings in the change under review; file an issue only for what genuinely cannot go in it.
- A change that adds public API is `feat:`, even when its purpose is performance.
- Public API changes are additive. Never add an optional parameter to a shipped signature; api-compat
  guards it. A breaking end state goes in an issue labelled `next-major`.
- A behaviour change gets a `## Behaviour change` section in the PR body; the release notes collect it.
- Commit subjects start lowercase, body lines stay within 100 characters, and commit bodies never contain
  nested parentheses: release-please drops the whole commit if they do.
- Local packs use `9.9.9-local.<sha>`, never a real version, so the shared NuGet cache is not poisoned.
- A green release pipeline proves nothing shipped; verify the package on NuGet.
