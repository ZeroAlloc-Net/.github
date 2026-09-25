# ZeroAlloc-Net / .github

Organization profile and meta-repo for **[ZeroAlloc-Net](https://github.com/ZeroAlloc-Net)**.

## Contents

| Path | Description |
|---|---|
| [`profile/README.md`](profile/README.md) | Org profile shown on the ZeroAlloc-Net GitHub page |
| [`docs/plans/`](docs/plans/) | Design documents and implementation plans |
| [`.github/workflows/api-compat.yml`](.github/workflows/api-compat.yml) | Reusable gate comparing each package's public API with its latest NuGet release |
| [`.github/workflows/ship-release-tracking.yml`](.github/workflows/ship-release-tracking.yml) | Reusable release-please step that moves Unshipped analyzer rules and public API to Shipped on the release PR |
| [`.github/workflows/release-tracking.yml`](.github/workflows/release-tracking.yml) | Reusable CI guard that fails a release PR while anything is left Unshipped |
| [`scripts/ship-release-tracking.py`](scripts/ship-release-tracking.py) | The script both release-tracking workflows run; `--check` runs the guard locally |

## About ZeroAlloc-Net

ZeroAlloc-Net is home to a family of high-performance .NET libraries built around three principles:

- **Zero allocations** — no heap pressure at steady state
- **Native AOT compatible** — no reflection, no runtime code generation
- **Compile-time correctness** — errors and wiring validated by Roslyn at build time, not at startup
