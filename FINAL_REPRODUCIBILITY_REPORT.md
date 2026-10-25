# Final reproducibility report

Audit date: 2026-10-17 (UTC)

## Environment

- Linux (Ubuntu), x86_64; Python venv at `.venv/`
- Pinned deps: numpy 2.2.6, pandas 2.3.3, matplotlib 3.10.9, scipy 1.15.3,
  PyYAML 6.0.2, python-docx 1.2.0, python-pptx 1.0.2, pytest 8.4.2

## Commands executed

1. `make reproduce` (= `make data` + `make manuscript` + `lint` + `test` +
   `verify-submission`):
   - verified 23 persisted raw source snapshots by size and SHA-256 (7 non-distributed
     local snapshots skipped by design);
   - ran `scripts/run_pipeline.py --config configs/default.yml` — regenerated
     `results/*.csv`, `figures/*.png`, `tables/*.csv`; all `manuscript_values.csv`
     entries identical to the committed registry;
   - rebuilt all docx/pdf/pptx and `submission/journal_of_geodesy_submission_FINAL.zip`;
   - `pytest`: 29 tests passed;
   - `verify_submission.py`: 26 manifested final files and ZIP integrity verified.
2. `make manuscript` (after the figure/table-numbering fixes): pipeline + builder rerun,
   36 s wall time; registry values again identical.
3. `pytest` rerun: 29 passed in ~1.1 s. `verify_submission.py` rerun: PASS.

## Failures / warnings

None. Runtime ~36–50 s per full pipeline. No network access required at build time
(raw inputs persisted and checksum-verified).

## Update — fresh-clone reproduction from public `main` (2026-10-25)

After the FINAL QC remediation pass, the reproduction was repeated from a
new empty directory against the PUBLIC repository only (no private content):
`git clone bougtoir/deep-time-reference-systems` at `main` =
`9f833606a906c4b4e5a85ed0e982de989b96b1ba`, then `make setup && make reproduce`.

- `pytest`: 38 passed (9 QC tests added since this report's first version).
- `verify_submission.py`: 26 files + ZIP integrity verified.
- `result_traceability.csv`, all figure PNGs and all table CSVs: bit-identical
  to the canonical package.
- Two noise-floor RMSE metrics (~1e-9 m) and one last-bit value regenerated
  differently — identified cause: OpenBLAS `DYNAMIC_ARCH` CPU dispatch; no
  claim-level value changed. Full account in
  `PUBLIC_CODE_FRESH_CLONE_REPRODUCTION.md` and `RESULT_CHANGELOG.md`.
