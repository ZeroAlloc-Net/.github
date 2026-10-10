# ZA1706 sweep, wave 1: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set `IsAotCompatible` on every library that builds clean under the trim and AOT analyzers, and set `false` on the two test helpers, with one PR per repo.

**Architecture:** Each task touches one repo. It works in a git worktree created from `origin/main`, edits the listed csproj files, proves that the analyzers are on and the build is clean, and then opens a PR. No source code changes in this wave.

**Tech Stack:** MSBuild/.NET SDK 10, `dotnet build`, `dotnet test`, `gh`.

**Spec:** `docs/plans/2026-10-10-aot-compatible-sweep-design.md` (this repo)

## Global Constraints

- **Worktrees only.** The local clones under `C:\Projects\Prive\ZeroAlloc\ZeroAlloc.<Repo>` are on other branches, and some have uncommitted work. Never switch branches, reset, stash or commit in them. Each task runs `git -C <clone> fetch origin` and then `git -C <clone> worktree add <clone>/.worktrees/aot-compatible -b feat/aot-compatible origin/main`, and works only in that worktree.
- **Where the property goes:**
  - A project whose target frameworks are all net8.0 or later gets `<IsAotCompatible>true</IsAotCompatible>` in its first `<PropertyGroup>`. That matches how `ZeroAlloc.Outbox.csproj` and `ZeroAlloc.Mediator.csproj` already do it.
  - A project that also targets an older framework gets this group instead, placed right after its first `<PropertyGroup>`:
    ```xml
      <PropertyGroup Condition="$([MSBuild]::IsTargetFrameworkCompatible('$(TargetFramework)', 'net8.0'))">
        <IsAotCompatible>true</IsAotCompatible>
      </PropertyGroup>
    ```
  - Test helpers get `<IsAotCompatible>false</IsAotCompatible>` in their first `<PropertyGroup>`.
- **No suppressions.** Do not add `NoWarn`, `#pragma`, `UnconditionalSuppressMessage` or `WarningsAsErrors` overrides. If a build reports an `IL2xxx` or `IL3xxx` warning, stop. Report the project, the TFM and the warning, and remove that project from the task. It moves to wave 2.
- **What has to pass.** Every repo already sets `TreatWarningsAsErrors` in `Directory.Build.props`. `dotnet build <sln> -c Release` must succeed for every target framework, and `dotnet test <sln> -c Release --no-build` must pass.
- **Commit message.**
  - The header is `feat: mark <packages> as AOT-compatible`, lowercase after the colon.
  - Body lines are 100 characters or fewer, with no nested parentheses.
  - End the body with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - No `claude.ai/code/session` link anywhere.
- **PR body.** Fill in the repo's PR template. Include a "Behaviour change" section with exactly this text:
  > Setting `IsAotCompatible` also sets `IsTrimmable`, so these assemblies carry trimmable metadata. An app that publishes with trimming may now trim them further. The trim and AOT analyzers run on them in our builds, which reported no warnings.

  For TestHelpers and Validation.Testing, use this instead:
  > These test helpers now declare `IsAotCompatible=false`. They run only in test projects, which never publish with Native AOT. Nothing changes at run time.

  End the body with `🤖 Generated with [Claude Code](https://claude.com/claude-code)` and no session link. Link the spec: `ZeroAlloc-Net/.github` `docs/plans/2026-10-10-aot-compatible-sweep-design.md`.
- **Checks before reporting the PR.** Wait for every check to finish (`gh pr checks <n> --watch`), and report red checks with their logs. Do not merge.
- **No releases.** Do not touch release-please PRs or cut a release.

## Standard procedure

Every task follows these steps, using the values in its own table.

- [ ] **Step 1: Create the worktree**

```bash
git -C C:/Projects/Prive/ZeroAlloc/ZeroAlloc.<Repo> fetch origin
git -C C:/Projects/Prive/ZeroAlloc/ZeroAlloc.<Repo> worktree add .worktrees/aot-compatible -b feat/aot-compatible origin/main
cd C:/Projects/Prive/ZeroAlloc/ZeroAlloc.<Repo>/.worktrees/aot-compatible
```

If `.worktrees/` is not in the repo's `.gitignore`, add it to `.git/info/exclude` in the clone, not to the repo.

- [ ] **Step 2: Show that the property is unset (the failing check)**

For each project in the task, run this with its newest TFM:

```bash
dotnet msbuild <project.csproj> -getProperty:IsAotCompatible -getProperty:EnableTrimAnalyzer -getProperty:EnableAotAnalyzer -p:TargetFramework=<tfm>
```

Expected: `IsAotCompatible` is empty, and both analyzer properties are empty or `false`.

- [ ] **Step 3: Edit each csproj** as Global Constraints describes, using the value in the task table.

- [ ] **Step 4: Show that the property is set (the passing check)**

Run the Step 2 command again. For `true` projects, expect `IsAotCompatible=true`, `EnableTrimAnalyzer=true` and `EnableAotAnalyzer=true`; for test helpers, expect `IsAotCompatible=false`. For a conditional project, also run it with the older TFM and expect `IsAotCompatible` to be empty.

- [ ] **Step 5: Build and test**

```bash
dotnet build <sln> -c Release
dotnet test <sln> -c Release --no-build
```

Expected: the build succeeds with 0 warnings and no `IL2xxx` or `IL3xxx` output, and every test passes.

- [ ] **Step 6: Commit, push and open the PR**

```bash
git add <the csproj files>
git commit -F <message file>
git push -u origin feat/aot-compatible
gh pr create --title "<commit header>" --body-file <body file>
gh pr checks <n> --watch
```

- [ ] **Step 7: Report** the PR URL, the check results and any project that moved to wave 2. Leave the worktree in place until the PR merges.

---

### Task 1: Collections

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Collections/ZeroAlloc.Collections.csproj` | netstandard2.1;net8.0;net9.0 | `true`, conditional group |

Solution: `ZeroAlloc.Collections.slnx`. Commit header: `feat: mark ZeroAlloc.Collections as AOT-compatible`. Step 4 also checks the netstandard2.1 TFM.

### Task 2: EventSourcing

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.EventSourcing.Aggregates/ZeroAlloc.EventSourcing.Aggregates.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.InMemory/ZeroAlloc.EventSourcing.InMemory.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.Kafka/ZeroAlloc.EventSourcing.Kafka.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.Mediator/ZeroAlloc.EventSourcing.Mediator.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.Outbox/ZeroAlloc.EventSourcing.Outbox.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.PostgreSql/ZeroAlloc.EventSourcing.PostgreSql.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.Sql/ZeroAlloc.EventSourcing.Sql.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.Sqlite/ZeroAlloc.EventSourcing.Sqlite.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.EventSourcing.SqlServer/ZeroAlloc.EventSourcing.SqlServer.csproj` | net8.0;net9.0;net10.0 | `true` |

Solution: `ZeroAlloc.EventSourcing.slnx`. Commit header: `feat: mark the EventSourcing packages as AOT-compatible`. Do not touch `ZeroAlloc.EventSourcing.Telemetry`, which is wave 2.

### Task 3: Inject

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Inject/ZeroAlloc.Inject.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Inject.Container/ZeroAlloc.Inject.Container.csproj` | net8.0;net9.0;net10.0 | `true` |

Solution: `ZeroAlloc.Inject.slnx`. Commit header: `feat: mark ZeroAlloc.Inject and Inject.Container as AOT-compatible`.

### Task 4: Mediator

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Mediator.Authorization/ZeroAlloc.Mediator.Authorization.csproj` | net8.0;net10.0 | `true` |
| `src/ZeroAlloc.Mediator.Cache/ZeroAlloc.Mediator.Cache.csproj` | net8.0;net10.0 | `true` |
| `src/ZeroAlloc.Mediator.Resilience/ZeroAlloc.Mediator.Resilience.csproj` | net8.0;net10.0 | `true` |
| `src/ZeroAlloc.Mediator.Telemetry/ZeroAlloc.Mediator.Telemetry.csproj` | net8.0;net10.0 | `true` |
| `src/ZeroAlloc.Mediator.Validation/ZeroAlloc.Mediator.Validation.csproj` | net8.0;net10.0 | `true` |

Solution: `ZeroAlloc.Mediator.slnx`. Commit header: `feat: mark the Mediator bridge packages as AOT-compatible`.

### Task 5: Outbox

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Outbox.Dashboard.Blazor/ZeroAlloc.Outbox.Dashboard.Blazor.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Outbox.InMemory/ZeroAlloc.Outbox.InMemory.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Outbox.Mediator/ZeroAlloc.Outbox.Mediator.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Outbox.Telemetry/ZeroAlloc.Outbox.Telemetry.csproj` | net8.0;net9.0;net10.0 | `true` |

Solution: `ZeroAlloc.Outbox.slnx`. Commit header: `feat: mark the clean Outbox packages as AOT-compatible`. Do not touch Dashboard, EfCore or Resilience, which are wave 2.

### Task 6: Results

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Results/ZeroAlloc.Results.csproj` | net8.0;net9.0;net10.0 | `true` |

Solution: `ZeroAlloc.Results.slnx`. Commit header: `feat: mark ZeroAlloc.Results as AOT-compatible`.

### Task 7: Scheduling

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Scheduling.InMemory/ZeroAlloc.Scheduling.InMemory.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Scheduling.Mediator/ZeroAlloc.Scheduling.Mediator.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Scheduling.Redis/ZeroAlloc.Scheduling.Redis.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Scheduling.Telemetry/ZeroAlloc.Scheduling.Telemetry.csproj` | net8.0;net9.0;net10.0 | `true` |

Solution: `ZeroAlloc.Scheduling.slnx`. Commit header: `feat: mark the clean Scheduling packages as AOT-compatible`. The local clone has uncommitted work, so the worktree rule matters most here. Do not touch Dashboard, Dashboard.Blazor, EfCore or Resilience, which are wave 2.

### Task 8: Specification

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Specification/ZeroAlloc.Specification.csproj` | net8.0 | `true` |

Solution: `ZeroAlloc.Specification.slnx`. Commit header: `feat: mark ZeroAlloc.Specification as AOT-compatible`.

### Task 9: Telemetry

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Telemetry/ZeroAlloc.Telemetry.csproj` | net8.0;net9.0;net10.0 | `true` |

Solution: `ZeroAlloc.Telemetry.slnx`. Commit header: `feat: mark ZeroAlloc.Telemetry as AOT-compatible`.

### Task 10: TestHelpers

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.TestHelpers/ZeroAlloc.TestHelpers.csproj` | net10.0 | `false` |

Solution: `ZeroAlloc.TestHelpers.slnx`. Commit header: `feat: declare ZeroAlloc.TestHelpers as not AOT-compatible`. Use the test-helper "Behaviour change" text.

### Task 11: Validation

| Project | TFMs | Value |
|---|---|---|
| `src/ZeroAlloc.Validation/ZeroAlloc.Validation.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Validation.AspNetCore/ZeroAlloc.Validation.AspNetCore.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Validation.Options/ZeroAlloc.Validation.Options.csproj` | net8.0;net9.0;net10.0 | `true` |
| `src/ZeroAlloc.Validation.Testing/ZeroAlloc.Validation.Testing.csproj` | net8.0;net9.0;net10.0 | `false` |

Solution: `ZeroAlloc.Validation.slnx`. Commit header: `feat: mark the Validation packages as AOT-compatible`. The PR body uses the standard text for the three libraries, and adds the test-helper text for Validation.Testing.

## After wave 1

- When every wave-1 PR has merged, remove its worktree: `git -C <clone> worktree remove .worktrees/aot-compatible`.
- Then confirm each change appears in its repo's release-please PR.
- Wave 2 gets its own plan, starting with the Serialisation decision.
