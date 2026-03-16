# ZeroAlloc.net Website Design

**Date:** 2026-03-16
**Status:** Approved

---

## Overview

A full marketing website for `zeroalloc.net` with per-library Docusaurus documentation sites on subdomains. Hosted on Cloudflare Pages.

---

## Repository

**Repo:** `ZeroAlloc-Net/.website`

Leading dot mirrors the `.github` convention — signals infrastructure, not a package.

pnpm monorepo with Turborepo for build orchestration.

```
.website/
  apps/
    web/               → zeroalloc.net              (Astro)
    docs-analyzers/    → analyzers.zeroalloc.net    (Docusaurus)
    docs-inject/       → inject.zeroalloc.net        (Docusaurus)
    docs-mediator/     → mediator.zeroalloc.net      (Docusaurus)
    docs-valueobjects/ → valueobjects.zeroalloc.net  (Docusaurus)
    docs-validation/   → validation.zeroalloc.net    (Docusaurus, when ready)
  packages/
    theme/             → shared colors, fonts, CSS tokens
    ui/                → shared React components (used by Docusaurus swizzle)
  pnpm-workspace.yaml
  turbo.json
```

---

## Hosting & Deployments

Each `apps/*` is a separate **Cloudflare Pages** project. One push to `main` triggers all builds in parallel via Turborepo's dependency graph.

| Cloudflare project | Root directory       | Domain                        |
|--------------------|----------------------|-------------------------------|
| `za-web`           | `apps/web`           | `zeroalloc.net`               |
| `za-docs-analyzers`| `apps/docs-analyzers`| `analyzers.zeroalloc.net`     |
| `za-docs-inject`   | `apps/docs-inject`   | `inject.zeroalloc.net`        |
| `za-docs-mediator` | `apps/docs-mediator` | `mediator.zeroalloc.net`      |
| `za-docs-valueobjects` | `apps/docs-valueobjects` | `valueobjects.zeroalloc.net` |

DNS managed via Cloudflare. Each subdomain is a CNAME to its Cloudflare Pages deployment.

---

## Marketing Site (`zeroalloc.net`)

**Framework:** Astro — fully static output, zero JS by default.

**Theme:** Dark by default. Matches the .NET performance/systems aesthetic.

### Sections

1. **Hero** — tagline, three principles (zero allocations · native AOT · compile-time correctness), CTA to browse packages
2. **Why ZeroAlloc** — the three principles expanded with icons
3. **Packages grid** — one card per library: name, short description, NuGet badge, link to subdomain docs
4. **Benchmarks** — headline benchmark number per library (e.g. "2 ns vs 88 ns")
5. **Footer** — GitHub org, NuGet org

### Content source

Content mirrors the org profile README. The packages grid and benchmark numbers are the canonical source of truth — the README can reference the site going forward.

---

## Per-Library Docs (`*.zeroalloc.net`)

**Framework:** Docusaurus with shared theme from `packages/theme`.

### Shared theme package

- Color tokens, typography, dark mode config
- Navbar config (links back to `zeroalloc.net`, GitHub, NuGet)
- Footer config
- Shared CSS overrides

All doc sites import from `packages/theme` so visual consistency is enforced across all subdomains.

### Per-library doc structure (standard Docusaurus)

```
docs-mediator/
  docs/
    intro.md
    installation.md
    getting-started.md
    api-reference.md
    benchmarks.md
    migration.md        (from MediatR)
  src/
  docusaurus.config.ts
  package.json          (extends packages/theme)
```

---

## Tech Stack Summary

| Concern | Choice |
|---|---|
| Marketing site | Astro (static) |
| Docs sites | Docusaurus |
| Monorepo tooling | pnpm workspaces + Turborepo |
| Hosting | Cloudflare Pages (one project per app) |
| DNS | Cloudflare |
| Shared theme | Internal `packages/theme` |
| Shared UI components | Internal `packages/ui` |
