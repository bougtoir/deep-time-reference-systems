# Pre-pivot baseline (Journal of Geodesy version, frozen)

Snapshot taken 2026-11-06 before the Earth Science Informatics pivot.

## Canonical state

- Private source: `bougtoir/wip` master `d2f0dbc84`, subdirectory `deep_time_reference_systems/`
  (tree `d5a2917f4654d243d4a3a8b00d15e088c1883e26`).
- Public mirror `bougtoir/deep-time-reference-systems` main `d0a03e8ab9605681f301b83f754c845ddc5b150e`
  has the identical tree `d5a2917f…` (verified with `git rev-parse`).
- Read-only historical tag in `bougtoir/wip`: `dtrs-jog-final-pre-esi-pivot`.
- Journal of Geodesy decision: manuscript JOGE-D-26-00489, editorial desk rejection
  ("does not add sufficient methodological or topical innovation to be within the scope of
  our journal"). Treated as a novelty/scope signal, not as evidence of a mathematical error.

## Baseline reproduction (this VM)

`make setup && make reproduce`: exit 0; 38 tests passed; `verify_submission.py` verified 26
final files and ZIP integrity. Only noise-floor digits changed relative to the committed
outputs (reflection-permitting synthetic RMSE 2.97e-09 → 4.02e-09 m; ITRF RMSE 3.61e-09 →
3.24e-09 m; proper-only RMSE identical to 1e-6 m). This is the documented OpenBLAS
DYNAMIC_ARCH cross-VM variance; the committed values were restored.

## Inventory

- Manuscript builder: `scripts/build_submission.py` (all prose numbers from
  `results/manuscript_values.csv`); OMML via `scripts/docx_math.py`.
- Analysis: `scripts/run_pipeline.py` → `results/*.csv`, `tables/*.csv`, `figures/*.png`,
  `result_traceability.csv`.
- Main display items: Figs. 1–5, Tables 1–3. Supplement S1–S8 with Supplementary Figs. S1–S2
  and Supplementary Tables S1–S3.
- References: 24 entries in `references_verified.csv`; Crossref JSON in `data/raw/literature/`.
- Raw data: `data/raw/itrf2020/ITRF2020_SLR.SSC.txt` (SHA-256 `d0f7afc0…09b4d`), ledger
  `data/data_acquisition_log.csv`.
- Tests: 7 files, 38 tests (`tests/test_qc.py` 9 QC tests).
- Author metadata pending: affiliation, ORCID, funding, competing interests.
- `manuscript_author(6).docx` (possible human edits referencing S1–S3, S7, S8) was not
  provided to this session and is not present in either repository; it could not be
  reconciled (see `FINAL_USER_INPUT_REQUIRED.md`).

## Frozen values (must not change)

rigidity p=0.5 → 0.9465 (0.9358–0.9555); p=0.6 → 0.996 (0.9921–0.9980); n=16; 2000
trials/cell; seed 20260924; proper-only RMSE 6.136173e6 m; reflection RMSE ~1e-9 m noise
floor; ellipsoid max chord difference 0.000225 m, 100% agreement; ITRF2020 16 SLR sites,
maximum/median pairwise change 0.691/0.091 m; residual chain O(3)→O(2)→SO(2)→{I}.
