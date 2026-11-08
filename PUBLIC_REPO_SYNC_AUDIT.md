# Public Repository Synchronization Audit — Journal of Geodesy package

Date: 2026-10-25. Scope: confirm the public mirror
`bougtoir/deep-time-reference-systems` (`main`) carries the exact code and
registries that produced the locked submission package.

## Canonical reference

- Private monorepo: `bougtoir/wip`, branch `devin/1792230689-jog-final-audit`,
  subdirectory `deep_time_reference_systems/`.
- Public repo: https://github.com/bougtoir/deep-time-reference-systems
- Public `main` HEAD at audit time: `9f833606a906c4b4e5a85ed0e982de989b96b1ba`
  (sync commit produced by `sync-to-repos`; see CANONICAL_COMMIT.txt).
- Sync mechanism: `.github/workflows/sync-to-repos.yml` maps the working
  branch to the public repo and exports `deep_time_reference_systems/` as the
  repo root.

## Incident found and remediated during this audit

A stale sibling branch (`devin/1790229434-deep-time-spatial-relations`) was
still mapped to the same target repo in the workflow on `master`; its
scheduled re-sync overwrote the public `main` after this branch's content had
already landed (public HEAD was left at `be99dc8d…`). Remediation:

1. Removed that branch's push-trigger and `BRANCH_MAP`/`SUBDIR_MAP` entries on
   this branch (commit `3b5dd6d`).
2. Brought the stale branch's `deep_time_reference_systems/` subdir to this
   branch's exact tree (plumbing commits `51ca63a`, `f553101`), so whichever
   branch a scheduled run exports, the public tree is identical.
3. Re-verified public `main` blob-by-blob afterward (table below).

Note: the mapping change becomes permanent only once the working branch is
merged to `master`; until then the two subdir trees are kept identical, which
makes the sync order-independent.

## Blob-hash verification (git object SHA, local vs public `main`)

| File | Blob SHA | Match |
|---|---|---|
| `scripts/build_submission.py` | `99c4a27667469f5922ebff1af8cf3c8c3e4e9337` | yes |
| `scripts/run_pipeline.py` | `feb79c90cfe8af2117588709676eca3966a9da71` | yes |
| `configs/default.yml` | `f6fceab5370b9ad2337d64d94622043e8b994f73` | yes |
| `results/manuscript_values.csv` | `ae55227fba9313edce94dc917ce529986e341273` | yes |
| `result_traceability.csv` | `d3472348342966a31f12827de99f24433380cf3a` | yes |
| `references_verified.csv` | `56cd20bf77b47b361b4c96412be2e6037492f9d4` | yes |
| `Makefile` | `59471a4824692d00d6ea1b633292d6148a649757` | yes |
| `pyproject.toml` | `6f05508d7074fdd9b09e543b09a3fba1b19024d7` | yes |
| `README.md` | `cffcddb55485cfde42f2a93f16bc97f41850f08f` | yes |
| `src/dtrs/**` (all tracked files) | per-file `git hash-object` vs API `.sha` | all match |

Verification command per file: `git hash-object <f>` locally vs
`gh api repos/bougtoir/deep-time-reference-systems/contents/<f> --jq .sha`.

## Verdict

PASS — the public `main` tree contains the same code, configs, registries,
traceability table and verified-reference table as the package that produced
`journal_of_geodesy_submission_FINAL_LOCKED.zip`. Fresh-clone reproduction
from this exact tree is documented in `PUBLIC_CODE_FRESH_CLONE_REPRODUCTION.md`.
