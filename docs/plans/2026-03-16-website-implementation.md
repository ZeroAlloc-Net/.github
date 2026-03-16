# ZeroAlloc.net Website Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the `zeroalloc.net` marketing site and per-library Docusaurus documentation sites as a pnpm monorepo hosted on Cloudflare Pages.

**Architecture:** pnpm workspace monorepo with Turborepo orchestration. One Astro app for the marketing site (`zeroalloc.net`), one Docusaurus app per library (e.g. `mediator.zeroalloc.net`). Each library repo owns its `/docs` folder and is pulled into `.website` as a git submodule — docs live with the code, the website just themes and hosts them. Shared theme and UI packages enforce visual consistency across all subdomains. Each app is a separate Cloudflare Pages deployment.

**Tech Stack:** pnpm workspaces, Turborepo, Astro 4, Docusaurus 3, React 18, TypeScript, Cloudflare Pages, git submodules.

---

### Task 1: Create the GitHub repo and clone it locally

**Files:**
- Create: `.website/` (new repo root)

**Step 1: Create repo on GitHub**

```bash
gh repo create ZeroAlloc-Net/.website --public --description "ZeroAlloc.net website and per-library documentation" --clone
cd .website
```

**Step 2: Add a `.gitignore`**

Create `.gitignore`:

```
node_modules/
.turbo/
dist/
.cache/
.docusaurus/
.astro/
.cloudflare/
```

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: initial repo setup"
git push -u origin main
```

---

### Task 2: Initialize pnpm monorepo with Turborepo

**Files:**
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `turbo.json`

**Step 1: Initialize root package.json**

```bash
pnpm init
```

Edit `package.json` to:

```json
{
  "name": "zeroalloc-website",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint"
  },
  "devDependencies": {
    "turbo": "^2.0.0"
  },
  "engines": {
    "node": ">=20",
    "pnpm": ">=9"
  }
}
```

**Step 2: Create pnpm-workspace.yaml**

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

**Step 3: Create turbo.json**

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".astro/**", "build/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {}
  }
}
```

**Step 4: Install turbo**

```bash
pnpm install
```

**Step 5: Create apps and packages directories**

```bash
mkdir -p apps packages
```

**Step 6: Commit**

```bash
git add .
git commit -m "chore: initialize pnpm monorepo with Turborepo"
```

---

### Task 3: Create shared theme package

**Files:**
- Create: `packages/theme/package.json`
- Create: `packages/theme/index.css`
- Create: `packages/theme/tokens.css`
- Create: `packages/theme/docusaurus.config.shared.ts`

**Step 1: Scaffold the package**

```bash
mkdir -p packages/theme
```

Create `packages/theme/package.json`:

```json
{
  "name": "@zeroalloc/theme",
  "version": "0.0.1",
  "private": true,
  "main": "./index.css",
  "exports": {
    ".": "./index.css",
    "./tokens": "./tokens.css",
    "./docusaurus": "./docusaurus.config.shared.ts"
  }
}
```

**Step 2: Create CSS design tokens**

Create `packages/theme/tokens.css`:

```css
:root {
  /* Brand */
  --za-color-primary: #00d4ff;
  --za-color-primary-dark: #00a8cc;
  --za-color-accent: #7c3aed;

  /* Backgrounds */
  --za-bg-base: #0a0a0f;
  --za-bg-surface: #12121a;
  --za-bg-elevated: #1a1a26;

  /* Text */
  --za-text-primary: #f0f0f5;
  --za-text-secondary: #9090a8;
  --za-text-muted: #5a5a72;

  /* Code */
  --za-code-bg: #0d1117;
  --za-code-border: #21262d;

  /* Borders */
  --za-border: #2a2a3a;

  /* Typography */
  --za-font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --za-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

Create `packages/theme/index.css`:

```css
@import './tokens.css';

* {
  box-sizing: border-box;
}

body {
  background: var(--za-bg-base);
  color: var(--za-text-primary);
  font-family: var(--za-font-sans);
}

code, pre {
  font-family: var(--za-font-mono);
}
```

**Step 3: Create shared Docusaurus config fragment**

Create `packages/theme/docusaurus.config.shared.ts`:

```ts
export const sharedNavbar = {
  logo: {
    alt: 'ZeroAlloc',
    src: 'img/logo.svg',
    href: 'https://zeroalloc.net',
  },
  items: [
    {
      href: 'https://zeroalloc.net',
      label: 'Home',
      position: 'left' as const,
    },
    {
      href: 'https://github.com/ZeroAlloc-Net',
      label: 'GitHub',
      position: 'right' as const,
    },
    {
      href: 'https://www.nuget.org/profiles/ZeroAlloc',
      label: 'NuGet',
      position: 'right' as const,
    },
  ],
};

export const sharedFooter = {
  style: 'dark' as const,
  links: [
    {
      title: 'Libraries',
      items: [
        { label: 'Analyzers', href: 'https://analyzers.zeroalloc.net' },
        { label: 'Inject', href: 'https://inject.zeroalloc.net' },
        { label: 'Mediator', href: 'https://mediator.zeroalloc.net' },
        { label: 'ValueObjects', href: 'https://valueobjects.zeroalloc.net' },
      ],
    },
    {
      title: 'Community',
      items: [
        { label: 'GitHub', href: 'https://github.com/ZeroAlloc-Net' },
        { label: 'NuGet', href: 'https://www.nuget.org/profiles/ZeroAlloc' },
      ],
    },
  ],
  copyright: `© ${new Date().getFullYear()} ZeroAlloc-Net`,
};

export const sharedThemeConfig = {
  colorMode: {
    defaultMode: 'dark' as const,
    disableSwitch: false,
    respectPrefersColorScheme: false,
  },
  prism: {
    additionalLanguages: ['csharp', 'bash'],
  },
};
```

**Step 4: Commit**

```bash
git add packages/theme
git commit -m "chore: add shared theme package with design tokens"
```

---

### Task 4: Scaffold the Astro marketing site

**Files:**
- Create: `apps/web/` (Astro app)

**Step 1: Create Astro app**

```bash
cd apps
pnpm create astro@latest web -- --template minimal --typescript strict --no-git --install
cd web
```

**Step 2: Update apps/web/package.json name**

Edit `apps/web/package.json`:
- Set `"name": "@zeroalloc/web"`
- Add to dependencies: `"@zeroalloc/theme": "workspace:*"`

**Step 3: Add Astro config for Cloudflare**

```bash
pnpm astro add cloudflare
```

Edit `apps/web/astro.config.mjs`:

```js
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'static',
  adapter: cloudflare(),
});
```

**Step 4: Import shared theme in global CSS**

Create `apps/web/src/styles/global.css`:

```css
@import '@zeroalloc/theme';

/* Page-specific overrides */
html {
  scroll-behavior: smooth;
}
```

**Step 5: Create the base layout**

Create `apps/web/src/layouts/Base.astro`:

```astro
---
interface Props {
  title?: string;
  description?: string;
}
const {
  title = 'ZeroAlloc — Zero allocations for .NET',
  description = 'A family of high-performance .NET libraries. Zero allocations. Native AOT. Compile-time correctness.',
} = Astro.props;
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles/global.css" />
  </head>
  <body>
    <slot />
  </body>
</html>
```

**Step 6: Verify dev server starts**

```bash
cd apps/web
pnpm dev
```

Expected: Astro dev server starts at `http://localhost:4321`

**Step 7: Commit**

```bash
cd ../..
git add apps/web
git commit -m "feat: scaffold Astro marketing site"
```

---

### Task 5: Build the marketing site sections

**Files:**
- Create: `apps/web/src/pages/index.astro`
- Create: `apps/web/src/components/Hero.astro`
- Create: `apps/web/src/components/Principles.astro`
- Create: `apps/web/src/components/PackagesGrid.astro`
- Create: `apps/web/src/components/Benchmarks.astro`
- Create: `apps/web/src/components/Footer.astro`

**Step 1: Create the data file for packages**

Create `apps/web/src/data/packages.ts`:

```ts
export interface Package {
  name: string;
  slug: string;
  description: string;
  docsUrl: string;
  githubUrl: string;
  nugetPackage: string;
  headline: string; // benchmark headline
  available: boolean;
}

export const packages: Package[] = [
  {
    name: 'ZeroAlloc.Analyzers',
    slug: 'analyzers',
    description: '42+ Roslyn analyzers that detect allocation-heavy patterns at build time.',
    docsUrl: 'https://analyzers.zeroalloc.net',
    githubUrl: 'https://github.com/ZeroAlloc-Net/ZeroAlloc.Analyzers',
    nugetPackage: 'ZeroAlloc.Analyzers',
    headline: 'Build-time allocation detection',
    available: true,
  },
  {
    name: 'ZeroAlloc.Inject',
    slug: 'inject',
    description: 'Compile-time dependency injection via Roslyn source generator. No reflection, fully Native AOT safe.',
    docsUrl: 'https://inject.zeroalloc.net',
    githubUrl: 'https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject',
    nugetPackage: 'ZeroAlloc.Inject',
    headline: '~3 ns vs ~35 ns (Microsoft DI)',
    available: true,
  },
  {
    name: 'ZeroAlloc.Mediator',
    slug: 'mediator',
    description: 'Zero-allocation source-generated mediator for request/response and notifications.',
    docsUrl: 'https://mediator.zeroalloc.net',
    githubUrl: 'https://github.com/ZeroAlloc-Net/ZeroAlloc.Mediator',
    nugetPackage: 'ZeroAlloc.Mediator',
    headline: '~2 ns vs ~88 ns (MediatR)',
    available: true,
  },
  {
    name: 'ZeroAlloc.ValueObjects',
    slug: 'valueobjects',
    description: 'Source-generated Equals, GetHashCode, == and ToString for existing partial class/struct types.',
    docsUrl: 'https://valueobjects.zeroalloc.net',
    githubUrl: 'https://github.com/ZeroAlloc-Net/ZeroAlloc.ValueObjects',
    nugetPackage: 'ZeroAlloc.ValueObjects',
    headline: '3.1 ns vs 45.2 ns (CFE)',
    available: true,
  },
  {
    name: 'ZeroAlloc.Validation',
    slug: 'validation',
    description: 'Source-generated validation API — zero allocations, no reflection, Native AOT safe.',
    docsUrl: 'https://validation.zeroalloc.net',
    githubUrl: 'https://github.com/ZeroAlloc-Net/ZeroAlloc.Validation',
    nugetPackage: 'ZeroAlloc.Validation',
    headline: 'Coming soon',
    available: false,
  },
];
```

**Step 2: Build the Hero component**

Create `apps/web/src/components/Hero.astro`:

```astro
---
---
<section class="hero">
  <div class="hero__inner">
    <p class="hero__eyebrow">High-performance .NET libraries</p>
    <h1 class="hero__title">
      Zero allocations.<br />
      Native AOT.<br />
      Compile-time correctness.
    </h1>
    <p class="hero__subtitle">
      A family of source-generated .NET libraries that eliminate runtime allocations,
      reflection, and dynamic dispatch from your hot paths.
    </p>
    <div class="hero__cta">
      <a href="#packages" class="btn btn--primary">Browse packages</a>
      <a href="https://github.com/ZeroAlloc-Net" class="btn btn--ghost">GitHub</a>
    </div>
  </div>
</section>

<style>
  .hero {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 1.5rem;
    text-align: center;
    background: radial-gradient(ellipse at 50% 0%, rgba(0, 212, 255, 0.08) 0%, transparent 60%);
  }
  .hero__inner { max-width: 760px; }
  .hero__eyebrow {
    font-size: 0.875rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--za-color-primary);
    margin-bottom: 1rem;
  }
  .hero__title {
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 700;
    line-height: 1.1;
    margin: 0 0 1.5rem;
    color: var(--za-text-primary);
  }
  .hero__subtitle {
    font-size: 1.125rem;
    color: var(--za-text-secondary);
    max-width: 560px;
    margin: 0 auto 2.5rem;
    line-height: 1.6;
  }
  .hero__cta { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
  .btn {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.75rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.9375rem;
    text-decoration: none;
    transition: opacity 0.15s;
  }
  .btn:hover { opacity: 0.85; }
  .btn--primary { background: var(--za-color-primary); color: #000; }
  .btn--ghost { border: 1px solid var(--za-border); color: var(--za-text-primary); }
</style>
```

**Step 3: Build the Packages grid**

Create `apps/web/src/components/PackagesGrid.astro`:

```astro
---
import { packages } from '../data/packages';
---
<section id="packages" class="section">
  <div class="container">
    <h2 class="section__title">Packages</h2>
    <div class="grid">
      {packages.map((pkg) => (
        <div class={`card ${!pkg.available ? 'card--soon' : ''}`}>
          <div class="card__header">
            <h3 class="card__name">{pkg.name}</h3>
            {pkg.available && (
              <a
                href={`https://www.nuget.org/packages/${pkg.nugetPackage}`}
                class="badge"
                target="_blank"
              >
                <img
                  src={`https://img.shields.io/nuget/v/${pkg.nugetPackage}.svg?style=flat-square`}
                  alt={`${pkg.name} NuGet version`}
                />
              </a>
            )}
            {!pkg.available && <span class="badge badge--soon">coming soon</span>}
          </div>
          <p class="card__desc">{pkg.description}</p>
          <p class="card__headline">{pkg.headline}</p>
          {pkg.available && (
            <div class="card__links">
              <a href={pkg.docsUrl} class="link">Docs →</a>
              <a href={pkg.githubUrl} class="link link--muted" target="_blank">GitHub</a>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
</section>

<style>
  .section { padding: 5rem 1.5rem; }
  .container { max-width: 1100px; margin: 0 auto; }
  .section__title {
    font-size: 2rem; font-weight: 700; margin-bottom: 2.5rem;
    color: var(--za-text-primary);
  }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }
  .card {
    background: var(--za-bg-surface);
    border: 1px solid var(--za-border);
    border-radius: 10px;
    padding: 1.5rem;
    display: flex; flex-direction: column; gap: 0.75rem;
  }
  .card--soon { opacity: 0.6; }
  .card__header { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; flex-wrap: wrap; }
  .card__name { font-size: 1rem; font-weight: 600; color: var(--za-text-primary); margin: 0; font-family: var(--za-font-mono); }
  .card__desc { font-size: 0.875rem; color: var(--za-text-secondary); margin: 0; line-height: 1.5; }
  .card__headline { font-size: 0.8125rem; color: var(--za-color-primary); font-family: var(--za-font-mono); margin: 0; }
  .card__links { display: flex; gap: 1rem; margin-top: auto; }
  .link { font-size: 0.875rem; color: var(--za-color-primary); text-decoration: none; font-weight: 500; }
  .link--muted { color: var(--za-text-secondary); }
  .badge { display: inline-flex; }
  .badge--soon {
    font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem;
    border-radius: 999px; background: var(--za-bg-elevated);
    color: var(--za-text-muted); border: 1px solid var(--za-border);
  }
</style>
```

**Step 4: Build the Footer**

Create `apps/web/src/components/Footer.astro`:

```astro
---
---
<footer class="footer">
  <div class="footer__inner">
    <p class="footer__copy">© {new Date().getFullYear()} ZeroAlloc-Net</p>
    <nav class="footer__links">
      <a href="https://github.com/ZeroAlloc-Net" target="_blank">GitHub</a>
      <a href="https://www.nuget.org/profiles/ZeroAlloc" target="_blank">NuGet</a>
    </nav>
  </div>
</footer>

<style>
  .footer {
    border-top: 1px solid var(--za-border);
    padding: 2rem 1.5rem;
  }
  .footer__inner {
    max-width: 1100px; margin: 0 auto;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 1rem;
  }
  .footer__copy { color: var(--za-text-muted); font-size: 0.875rem; margin: 0; }
  .footer__links { display: flex; gap: 1.5rem; }
  .footer__links a { color: var(--za-text-secondary); font-size: 0.875rem; text-decoration: none; }
  .footer__links a:hover { color: var(--za-text-primary); }
</style>
```

**Step 5: Wire up the index page**

Create `apps/web/src/pages/index.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import Hero from '../components/Hero.astro';
import PackagesGrid from '../components/PackagesGrid.astro';
import Footer from '../components/Footer.astro';
---
<Base>
  <main>
    <Hero />
    <PackagesGrid />
  </main>
  <Footer />
</Base>
```

**Step 6: Verify it builds**

```bash
cd apps/web
pnpm build
```

Expected: `dist/` folder created with no errors.

**Step 7: Commit**

```bash
cd ../..
git add apps/web/src
git commit -m "feat: build marketing site sections (hero, packages, footer)"
```

---

### Task 6: Add library repos as git submodules

**Files:**
- Create: `repos/` directory with one submodule per library

**Step 1: Add each library repo as a submodule**

```bash
git submodule add https://github.com/ZeroAlloc-Net/ZeroAlloc.Analyzers repos/analyzers
git submodule add https://github.com/ZeroAlloc-Net/ZeroAlloc.Inject repos/inject
git submodule add https://github.com/ZeroAlloc-Net/ZeroAlloc.Mediator repos/mediator
git submodule add https://github.com/ZeroAlloc-Net/ZeroAlloc.ValueObjects repos/valueobjects
```

**Step 2: Add a `/docs` folder to each library repo**

For each library repo (do this in each library's own local clone), create:

```
ZeroAlloc.Mediator/
  docs/
    index.md          ← intro / getting started
    installation.md
    api-reference.md
    benchmarks.md
    migration.md      ← migration from MediatR
```

Minimum `docs/index.md` for each repo (example for Mediator):

```md
---
slug: /
sidebar_position: 1
---

# ZeroAlloc.Mediator

Zero-allocation source-generated mediator for request/response and notifications.

## Install

```bash
dotnet add package ZeroAlloc.Mediator
```

## Quick start

Coming soon.
```

Commit and push the `/docs` folder in each library repo before proceeding.

**Step 3: Verify submodule content is accessible**

```bash
ls repos/mediator/docs/
```

Expected: `index.md` and other doc files from the library repo.

**Step 4: Commit submodules**

```bash
git add .gitmodules repos/
git commit -m "chore: add library repos as git submodules"
```

---

### Task 7: Scaffold Docusaurus docs sites pointing to submodule docs

**Files:**
- Create: `apps/docs-mediator/` (and repeat for each library)

**Step 1: Create first Docusaurus app**

```bash
cd apps
pnpm create docusaurus@latest docs-mediator classic --typescript
cd ..
```

**Step 2: Update package.json**

Edit `apps/docs-mediator/package.json`:
- Set `"name": "@zeroalloc/docs-mediator"`
- Add `"@zeroalloc/theme": "workspace:*"` to dependencies

**Step 3: Configure Docusaurus to read docs from the submodule**

Replace `apps/docs-mediator/docusaurus.config.ts`:

```ts
import type { Config } from '@docusaurus/types';
import { sharedNavbar, sharedFooter, sharedThemeConfig } from '@zeroalloc/theme/docusaurus';

const config: Config = {
  title: 'ZeroAlloc.Mediator',
  tagline: 'Zero-allocation source-generated mediator for .NET',
  url: 'https://mediator.zeroalloc.net',
  baseUrl: '/',
  organizationName: 'ZeroAlloc-Net',
  projectName: 'ZeroAlloc.Mediator',
  trailingSlash: false,

  themeConfig: {
    ...sharedThemeConfig,
    navbar: { ...sharedNavbar, title: 'ZeroAlloc.Mediator' },
    footer: sharedFooter,
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          // Read docs from the library repo submodule — not from this app folder
          path: '../../repos/mediator/docs',
          sidebarPath: './sidebars.ts',
        },
        blog: false,
        theme: {
          customCss: ['@zeroalloc/theme/index.css', './src/css/custom.css'],
        },
      },
    ],
  ],
};

export default config;
```

**Step 4: Verify dev server loads docs from submodule**

```bash
cd apps/docs-mediator
pnpm start
```

Expected: Docusaurus serves the docs from `repos/mediator/docs/` with dark theme applied.

**Step 5: Scaffold remaining docs sites**

```bash
cd apps
pnpm create docusaurus@latest docs-analyzers classic --typescript
pnpm create docusaurus@latest docs-inject classic --typescript
pnpm create docusaurus@latest docs-valueobjects classic --typescript
cd ..
```

For each, repeat steps 2–3 with the appropriate values:

| App | name | title | url | submodule path |
|---|---|---|---|---|
| docs-analyzers | `@zeroalloc/docs-analyzers` | `ZeroAlloc.Analyzers` | `https://analyzers.zeroalloc.net` | `../../repos/analyzers/docs` |
| docs-inject | `@zeroalloc/docs-inject` | `ZeroAlloc.Inject` | `https://inject.zeroalloc.net` | `../../repos/inject/docs` |
| docs-valueobjects | `@zeroalloc/docs-valueobjects` | `ZeroAlloc.ValueObjects` | `https://valueobjects.zeroalloc.net` | `../../repos/valueobjects/docs` |

**Step 6: Install and verify full build**

```bash
pnpm install
pnpm build
```

Expected: All apps build successfully. Each docs site renders content from its library submodule.

**Step 7: Commit**

```bash
git add apps/
git commit -m "feat: scaffold Docusaurus docs sites reading from library submodules"
```

---

### Task 7b: Set up GitHub Actions to auto-update submodules on library changes

**Files:**
- Create: `.github/workflows/update-submodules.yml` in `.website` repo
- Create: `.github/workflows/trigger-website.yml` in each library repo

**Step 1: Add dispatch workflow to `.website`**

Create `.website/.github/workflows/update-submodules.yml`:

```yaml
name: Update submodules

on:
  repository_dispatch:
    types: [submodule-update]
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Update all submodules to latest
        run: git submodule update --remote --merge

      - name: Commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git diff --quiet && git diff --staged --quiet || \
            git commit -am "chore: update submodules" && git push
```

**Step 2: Add trigger workflow to each library repo**

Create `.github/workflows/trigger-website.yml` in each library repo (e.g. `ZeroAlloc.Mediator`):

```yaml
name: Trigger website rebuild

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Dispatch to .website repo
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.WEBSITE_DISPATCH_TOKEN }}
          repository: ZeroAlloc-Net/.website
          event-type: submodule-update
```

**Step 3: Create the dispatch token**

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Create a fine-grained token with `Actions: write` permission on `ZeroAlloc-Net/.website`
3. Add it as a secret named `WEBSITE_DISPATCH_TOKEN` in each library repo

**Step 4: Commit workflows**

In `.website`:
```bash
git add .github/
git commit -m "ci: add submodule auto-update workflow"
git push
```

In each library repo, commit the trigger workflow.

---

### Task 8: Configure Cloudflare Pages deployments

> This task is performed in the Cloudflare dashboard, not in code.

**Step 1: Create Cloudflare Pages project for the marketing site**

1. Go to Cloudflare Dashboard → Pages → Create a project
2. Connect to `ZeroAlloc-Net/.website` GitHub repo
3. Set:
   - Project name: `za-web`
   - Build command: `pnpm build --filter @zeroalloc/web`
   - Build output directory: `apps/web/dist`
   - Root directory: `/` (monorepo root)
4. Add environment variable: `NODE_VERSION=20`
5. Deploy

**Step 2: Add custom domain for marketing site**

In `za-web` → Custom domains → Add `zeroalloc.net` and `www.zeroalloc.net`

**Step 3: Repeat for each docs site**

Create one Cloudflare Pages project per docs app:

| Project name | Build command | Output dir | Domain |
|---|---|---|---|
| `za-docs-analyzers` | `pnpm build --filter @zeroalloc/docs-analyzers` | `apps/docs-analyzers/build` | `analyzers.zeroalloc.net` |
| `za-docs-inject` | `pnpm build --filter @zeroalloc/docs-inject` | `apps/docs-inject/build` | `inject.zeroalloc.net` |
| `za-docs-mediator` | `pnpm build --filter @zeroalloc/docs-mediator` | `apps/docs-mediator/build` | `mediator.zeroalloc.net` |
| `za-docs-valueobjects` | `pnpm build --filter @zeroalloc/docs-valueobjects` | `apps/docs-valueobjects/build` | `valueobjects.zeroalloc.net` |

**Step 4: Verify all deployments are live**

Visit each URL and confirm the correct site loads with dark theme.

---

### Task 9: Final polish and README

**Step 1: Add a root README**

Create `.website/README.md`:

```md
# ZeroAlloc.net — Website & Docs

Monorepo for [zeroalloc.net](https://zeroalloc.net) and all per-library documentation sites.

## Structure

| App | URL |
|---|---|
| `apps/web` | zeroalloc.net |
| `apps/docs-analyzers` | analyzers.zeroalloc.net |
| `apps/docs-inject` | inject.zeroalloc.net |
| `apps/docs-mediator` | mediator.zeroalloc.net |
| `apps/docs-valueobjects` | valueobjects.zeroalloc.net |

## Dev

```bash
pnpm install
pnpm dev                                    # all apps in parallel
pnpm dev --filter @zeroalloc/web            # marketing site only
pnpm dev --filter @zeroalloc/docs-mediator  # mediator docs only
```

## Build

```bash
pnpm build         # all apps
```
```

**Step 2: Commit and push**

```bash
git add README.md
git commit -m "docs: add monorepo README"
git push
```
