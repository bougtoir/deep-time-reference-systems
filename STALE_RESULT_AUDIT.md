# Stale-result / version-crossing audit

## Search targets

- old 100-trial rigidity results: found ONLY in `RESULT_CHANGELOG.md`,
  `PRE_MINOR_REVISION_STATE.md`, `RIGIDITY_REPLICATION_AUDIT.md` — historical audit records,
  intentionally retained outside the package
- old "0.96 at p=0.5" wording: only in the same change-log documents
- old "p=0.5 for >=0.95" threshold: only in the same change-log documents
- old figures: `figures/figure_2_stabilizer_hierarchy.png` — orphaned pre-revision Fig. 2 not
  referenced by any script, table, or document. REMOVED in this audit.
- stale result CSVs: none — `results/*.csv` all regenerated 2026-10-17, identical values to
  committed versions
- duplicate result registries: none — single `results/manuscript_values.csv`; supplement's
  registry table renders it directly
- obsolete supplement values: none — supplement renders registry CSV and config verbatim
- old manuscript drafts referenced by scripts: none — `build_submission.py` is the only
  document builder
- previous-version tables: none — `tables/*.csv` regenerated this run

## Package contents check

`journal_of_geodesy_submission_FINAL.zip` (regenerated) contains only the 26 manifested
artifacts + MANIFEST.csv: current docx/pdf/pptx, figures, tables, the reproducibility zip,
and author-facing readme/checklist/disclosure files. No audit md reports, no old zips, no
cache files. `dtrs_reproducibility.zip` bundles the current code, config, tests, persisted
raw inputs, acquisition ledger, and prior audit documents (as documentation, not as stale
results).

## Current expected rigidity values (verified by regeneration)

- n=16, p=0.5: 0.9465 (0.9358–0.9555) — matches expected ≈0.947
- n=16, p=0.6: 0.996 (0.9921–0.9980) — matches expected ≈0.996
- first tested p with frequency >=0.95: 0.6 — matches expected

## Verdict

PASS — stale results = 0 in the package; one stale orphaned figure removed from the repo.
