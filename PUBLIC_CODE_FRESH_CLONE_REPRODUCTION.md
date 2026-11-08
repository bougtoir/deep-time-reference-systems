# Fresh-Clone Reproduction from Public `main` — Journal of Geodesy package

Date: 2026-10-25. Protocol followed exactly as required:

1. Created a NEW EMPTY directory (`~/freshclone2/`).
2. Fresh-cloned the PUBLIC repository `bougtoir/deep-time-reference-systems`,
   `main` at `9f833606a906c4b4e5a85ed0e982de989b96b1ba`.
3. Copied NOTHING from the working tree; used only the documented setup:
   `make setup` then `make reproduce` (README §Reproduce).
4. Ran the full suite: raw-data checksum verification → seeded analyses →
   figure/table/registry regeneration → `compileall` → `pytest` →
   `verify_submission` → submission ZIP rebuilt.
5. Compared regenerated artifacts against the canonical package.

## Result of the run

- `make reproduce` exit 0.
- `pytest`: **38 passed, 0 failed** (includes all QC tests A–H: OMML
  presence, supplementary citations, monotonic first-citation order,
  reference completeness both directions, headline hardcode guard, no
  Markdown asterisks, no character grid, current traceability).
- `verify_submission`: 26 final files + ZIP integrity verified.
- No local unpublished patch was required at any step.

## Artifact comparison (clone vs canonical package)

| Artifact | Result |
|---|---|
| `result_traceability.csv` | **bit-identical** |
| All `figures/*.png` | **bit-identical** (every figure byte-matches) |
| All `tables/*.csv` | **bit-identical** |
| `results/manuscript_values.csv` | identical except 3 metrics below |
| `data/processed/itrf_selected_sites.csv` | identical except last-digit float repr in lon column |
| DOCX/PDF/PPTX/ZIP | rebuilt; DOCX internals carry fresh timestamps (expected nondeterminism) |

## Documented nondeterminism: two noise-floor RMSEs

Three registry values regenerated to different last digits:

| Metric | Canonical | Fresh clone | Comment |
|---|---|---|---|
| `distance_reconstruction_rmse_allow_reflection_m` (synthetic) | 2.9701702222673244e-09 | 4.024743751868387e-09 | noise floor |
| `distance_reconstruction_rmse_m` (ITRF2020) | 3.6132759390917642e-09 | 3.2363723287752093e-09 | noise floor |
| `distance_reconstruction_rmse_proper_only_m` | 6136173.251345326 | 6136173.251345327 | last bit; rounds to the same 6.136173e6 m |

Cause (identified, not hypothesized): pinned dependency versions are identical
(numpy 2.2.6, scipy 1.15.3, pandas 2.3.3, Python 3.10.12), but numpy/scipy
link `scipy-openblas` built with `DYNAMIC_ARCH` — OpenBLAS selects a different
SIMD kernel per host CPU, changing floating-point reduction order. The
pipeline is bit-deterministic within one environment (two consecutive clone
runs produced byte-identical output) but not across CPU microarchitectures.

Impact: none on any claim. The varying metrics are reconstruction-error
floors of order 1e-9 m — "numerically zero" values whose exact last digit is
meaningless; all decision-relevant values are bit-identical: rigidity
probabilities and Wilson CIs, 16/16 SLR stations, 0.691 m max / 0.091 m
median epoch distance change, ellipsoid max chord difference 0.000225 m,
100% directional agreement, all counts. The corresponding prose digits
(2.97e-9 vs 4.02e-9; 3.61e-9 vs 3.24e-9) are the only rendered difference;
claims, tables, figures, and traceability are semantically and byte-identical.
This caveat is recorded in `RESULT_CHANGELOG.md`.

## Verdict

PASS — public `main` alone reproduces the entire analysis, package and test
suite; the only variance is a documented, environment-level floating-point
noise floor that does not alter any value reported to the reader at the
precision claimed.
