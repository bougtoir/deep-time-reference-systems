# Public fresh-clone reproduction (Earth Science Informatics package)

- Public repository: https://github.com/bougtoir/deep-time-reference-systems, `main` at
  `48eb26ddc288e7142cb8c036bef7d4c9921a3c91`, synced by `sync-to-repos.yml` from
  `bougtoir/wip` commit `bcad6a557e7271d9af6393a18a4fe500e54d09e0` (pointer branch
  `devin/1792230689-jog-final-audit`, fast-forwarded to `devin/1793944467-dtrs-esi-pivot`).
- Tree check before running anything: `diff -rq` between the clone and the wip subdirectory showed
  only `data/raw/journal_esi/` and `data/raw/standards/`, which are excluded on purpose (private
  audit snapshots, see `DATA_PROVENANCE.md`).
- Commands, run in a new clone on a separate directory with a new virtual environment:

  ```bash
  git clone https://github.com/bougtoir/deep-time-reference-systems
  cd deep-time-reference-systems
  make setup && .venv/bin/pip install pytest
  make reproduce
  ```

- Result: exit 0. "Verified 53 raw source snapshots. Skipped 33 non-distributed local or
  private-audit snapshots." Pipeline and manuscript build completed; lint passed; **51 passed**;
  "Verified 20 final files and ZIP integrity."
- Comparison with the wip build:
  - `results/manuscript_values.csv`: 976 metrics in both. The only differences are the six wall-clock
    `rec_cost_*_median_decode_ms` values.
  - Byte-identical: `results/record_scenarios.csv`, `record_missingness.csv`, `record_ablation.csv`,
    `record_calibration.csv`, `tables/table_3_scenario_outcomes.csv`,
    `schema/dtrs_relation_record.schema.json`, `references_verified.csv`, `result_traceability.csv`.
  - DOCX text: `manuscript_clean.docx` differs in one sentence only (median decoding time 3.1 ms vs
    2.7 ms, wall clock); `ESM_1.docx` and `cover_letter.docx` text identical. DOCX/PDF/ZIP binaries
    differ by build timestamps.
- The public raw data plus repository code reproduce every seeded number, figure and table.
