#!/usr/bin/env bash
#
# Unlist every published version of one or more NuGet packages.
#
# Use this for packages the org no longer builds — a project that was renamed,
# folded into another package, or deleted, leaving versions on nuget.org that
# nobody can update. ZeroAlloc.Mediator.Authorization.Generator is the case this
# was written for: published up to 4.1.3, no source project remains anywhere in
# the org.
#
# WHAT UNLISTING DOES
#
#   nuget.org has no true delete. `dotnet nuget delete` unlists: the package
#   disappears from search and from the version list, but restore keeps working
#   for anyone who already depends on it. That is exactly what we want — stop new
#   adopters, don't break existing builds. It cannot be undone from the CLI; an
#   owner has to relist via the nuget.org UI.
#
# SAFETY
#
#   * Dry run by default. Nothing is unlisted without --confirm.
#   * Ownership is verified before any package is touched. A typo that resolves
#     to somebody else's package aborts rather than unlisting it. There are
#     unrelated packages on nuget whose names start with "ZeroAlloc" and are
#     owned by other people, so this guard is load-bearing, not decorative.
#   * The API key is read from the environment, never passed as an argument, so
#     it stays out of shell history and the process list.
#
# USAGE
#
#   # See what would happen (no key needed):
#   scripts/unlist-orphaned-packages.sh ZeroAlloc.Mediator.Authorization.Generator
#
#   # Actually unlist:
#   NUGET_API_KEY=... scripts/unlist-orphaned-packages.sh --confirm ZeroAlloc.Mediator.Authorization.Generator
#
# The key needs the "Unlist package" scope for the IDs concerned.

set -euo pipefail

readonly EXPECTED_OWNER="ZeroAlloc.NET"
readonly SOURCE="https://api.nuget.org/v3/index.json"
readonly FLAT="https://api.nuget.org/v3-flatcontainer"
readonly SEARCH="https://azuresearch-usnc.nuget.org/query"

confirm=0
packages=()

for arg in "$@"; do
  case "$arg" in
    --confirm) confirm=1 ;;
    -h|--help) sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "ERROR: unknown option: $arg" >&2; exit 2 ;;
    *) packages+=("$arg") ;;
  esac
done

if [[ ${#packages[@]} -eq 0 ]]; then
  echo "ERROR: no package ids given. See --help." >&2
  exit 2
fi

for tool in curl jq dotnet; do
  command -v "$tool" >/dev/null 2>&1 || { echo "ERROR: $tool is required but not on PATH." >&2; exit 2; }
done

if [[ $confirm -eq 1 && -z "${NUGET_API_KEY:-}" ]]; then
  echo "ERROR: --confirm requires NUGET_API_KEY to be set in the environment." >&2
  exit 2
fi

# Resolve everything before unlisting anything, so a bad id in the list cannot
# leave the org half-unlisted.
declare -a plan_ids=()
declare -a plan_versions=()
failures=0

for id in "${packages[@]}"; do
  echo "==> $id"

  owner=$(curl -fsS --max-time 30 "${SEARCH}?q=packageid:${id}&prerelease=true&semVerLevel=2.0.0" 2>/dev/null \
          | jq -r '.data[0].owners // [] | join(",")' 2>/dev/null || echo "")

  if [[ -z "$owner" ]]; then
    echo "    SKIP: not found on nuget.org (or search unavailable)."
    failures=$((failures + 1))
    continue
  fi

  if [[ "$owner" != *"$EXPECTED_OWNER"* ]]; then
    echo "    ABORT: owned by '${owner}', expected '${EXPECTED_OWNER}'."
    echo "           Refusing to unlist a package this org does not own."
    failures=$((failures + 1))
    continue
  fi

  versions=$(curl -fsS --max-time 30 "${FLAT}/$(echo "$id" | tr '[:upper:]' '[:lower:]')/index.json" 2>/dev/null \
             | jq -r '.versions[]?' 2>/dev/null || echo "")

  if [[ -z "$versions" ]]; then
    echo "    SKIP: no published versions found."
    continue
  fi

  count=$(echo "$versions" | wc -l | tr -d ' ')
  echo "    owner: ${owner}"
  echo "    versions to unlist (${count}): $(echo "$versions" | tr '\n' ' ')"

  while IFS= read -r v; do
    [[ -n "$v" ]] || continue
    plan_ids+=("$id")
    plan_versions+=("$v")
  done <<< "$versions"
done

echo
total=${#plan_ids[@]}

if [[ $failures -gt 0 ]]; then
  echo "$failures package(s) were skipped or refused — see above."
fi

if [[ $total -eq 0 ]]; then
  echo "Nothing to unlist."
  exit $(( failures > 0 ? 1 : 0 ))
fi

if [[ $confirm -eq 0 ]]; then
  echo "DRY RUN — ${total} version(s) would be unlisted. Re-run with --confirm and NUGET_API_KEY set."
  exit 0
fi

echo "Unlisting ${total} version(s)..."
unlisted=0
errors=0

for i in "${!plan_ids[@]}"; do
  id="${plan_ids[$i]}"
  version="${plan_versions[$i]}"
  printf '    %s %s ... ' "$id" "$version"

  if dotnet nuget delete "$id" "$version" \
       --source "$SOURCE" \
       --api-key "$NUGET_API_KEY" \
       --non-interactive >/dev/null 2>&1; then
    echo "unlisted"
    unlisted=$((unlisted + 1))
  else
    echo "FAILED"
    errors=$((errors + 1))
  fi
done

echo
echo "Done: ${unlisted} unlisted, ${errors} failed."
# Unlisting is eventually consistent — search and the version list can take a
# few minutes to reflect it, the same lag that affects publishing.
[[ $errors -eq 0 && $failures -eq 0 ]]
