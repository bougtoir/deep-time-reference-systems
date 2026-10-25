# Pre-adversarial-audit state

Audit date: 2026-10-17 (UTC)
Branch at snapshot: `devin/1792230689-jog-final-audit` (created from `master` before any audit edit)

- Commit hash: `71ddbb22d7901295e5959b5345a254e3b253292e`
- Git status at snapshot: clean (no modified or untracked files under `deep_time_reference_systems/`)
- Project files in manifest: 159 (all tracked files under this directory, excluding `.venv`, `.git`, `__pycache__`)

## Canonical artifacts

- Manuscript title: Identifiability of spatial relations under geodetic datum and reference-frame loss
- Canonical manuscript: `submission_final/manuscript_inline.docx` (+ `submission_final/manuscript.pdf`)
- Canonical supplement: `submission_final/supplement.docx` (+ `submission_final/supplement.pdf`)
- Canonical figures: `figures/*.png` (7 used in package); packaged copies under `submission_final/figures/`
- Canonical tables: `tables/*.csv` (4 files); packaged under `submission_final/tables/`
- Canonical result registry: `results/manuscript_values.csv`
- Traceability: `result_traceability.csv`
- Reproducibility archive: `submission_final/dtrs_reproducibility.zip`
- Submission package: `submission/journal_of_geodesy_submission_FINAL.zip`
- Package SHA-256 at snapshot: `72c3f4a315817b55048e18957ad17f3ee6ba3c70cad5898045d4d5d8ef032429`

## Key packaged file hashes at snapshot

- manuscript_inline.docx `fe033f1dab24d071a98e470bb14f0684c7e8a4a945da451937f11e6d73dacedd`
- manuscript.pdf `ee02235b07f6c9dbb18f9c1802c6b5024be2cdefc20306488e87df30221be5ed`
- supplement.docx `6d0204c92c46d7c25a151e14b4a30e678afd7ac095d502001086d144e80c6a28`
- dtrs_reproducibility.zip `f563dd215e3b2736439a2e42dfec609e6df43584caf0afda32b9de9e7d63b910`

## Protected (frozen) results

- n=16 rigidity: 0.9465 at p=0.5 (Wilson 0.9358–0.9555); 0.996 at p=0.6 (0.9921–0.9980); first tested p>=0.95 = 0.6
- Proper-only mirror RMSE 6.136173e6 m; reflection-permitting RMSE 2.97e-9 m (synthetic), 3.61e-9 m (ITRF2020)
- Ellipsoid sensitivity: max chord-difference 0.000225 m; 100% directional agreement
- ITRF2020: 16 sites; max pairwise change 0.6906 m, median 0.0907 m; epochs 2015.0->2025.0
- Config: seed 20260924; 2000 trials/cell; 250 frame trials; 4000 MC trials/condition

## Known unresolved user metadata

- Affiliation/postal address: `[Affiliation to be confirmed]` (title page, manuscript header, cover letter)
- ORCID: `[to be confirmed]`
- Funding and competing interests: `[To be completed locally before submission.]`
- These are isolated in `submission_final/FINAL_USER_INPUT_REQUIRED.md`; no scientific result depends on them.
