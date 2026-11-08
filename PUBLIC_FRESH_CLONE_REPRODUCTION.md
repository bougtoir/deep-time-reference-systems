# Public fresh-clone reproduction (Earth Science Informatics package)

## Run 3 (final QC pass, wip PR #781)

- Public repository `main` at `5a2cd7965d887c26cfd4b03f4cd6803673bcab06`, synced from wip commit
  `95114beae` (pointer branch `devin/1792230689-jog-final-audit`).
- Tree check before running: `diff -rq` against the wip subdirectory showed only
  `data/raw/journal_esi/` and `data/raw/standards/` (private audit snapshots, excluded on purpose by
  the `EXCLUDE_MAP` entry now on `master`).
- Commands in a new empty directory with a new virtual environment (Python 3.10.12):
  `git clone https://github.com/bougtoir/deep-time-reference-systems && cd deep-time-reference-systems && make setup && make reproduce`
  (`make reproduce` = raw-data verification, pipeline, manuscript build, lint, `pytest`, ZIP verification).
- Result: exit 0. "Verified 53 raw source snapshots. Skipped 33 non-distributed local or
  private-audit snapshots." **56 passed.** "Verified 20 final files and ZIP integrity."
- Comparison with the wip build: every file in `data/processed/`, `tables/`, `figures/`, `schema/`,
  `result_traceability.csv`, `references_verified.csv` and every `results/*.csv` except
  `manuscript_values.csv` and `record_cost.csv` is byte-identical; those two differ only in the six
  wall-clock `rec_cost_*_median_decode_ms` values. Paragraph text of `manuscript_clean.docx`,
  `ESM_1.docx` and `cover_letter_final.docx` is identical to the wip build (the decode-time sentence
  happened to round to the same value). DOCX/PDF/ZIP binaries differ by build timestamps.
- An intermediate run on public `e9bcbf0` (before the author's Limitations paragraphs were added)
  also exited 0 with 56 tests; its only differences were the decode times and those two paragraphs.
- Conclusion: the public code and the public raw data reproduce every seeded number, figure, table
  and the manuscript text.

## Run 2 (integrated package, wip PR #774; superseded)

- Public repository: https://github.com/bougtoir/deep-time-reference-systems, `main` at
  `fa7225f26e2eb04f3b998ba1bb3072bc958b885b`, synced from `bougtoir/wip` commit
  `3d8566bcf226ecfc0de372caac6b17cf7128a4be` (pointer branch `devin/1792230689-jog-final-audit`).
- Tree check before running anything: `diff -rq` between the clone and the wip subdirectory showed no
  differences. In particular, `data/raw/journal_esi/` and `data/raw/standards/` were present again:
  the scheduled sync runs the workflow copy on `master`, which does not yet contain the DTRS
  `EXCLUDE_MAP` entry. The exclusion takes effect on scheduled syncs only after this branch is
  merged into `master`. These files also remain in public git history from earlier syncs.
- Commands, run in a new clone in a separate directory with a new virtual environment
  (Python 3.10.12, numpy 2.2.6, scipy 1.15.3):

  ```bash
  git clone https://github.com/bougtoir/deep-time-reference-systems
  cd deep-time-reference-systems
  make setup && make reproduce
  ```

- Result: exit 0. "Verified 79 raw source snapshots. Skipped 7 non-distributed local or
  private-audit snapshots." Pipeline and manuscript build completed; lint passed; **51 passed**;
  "Verified 20 final files and ZIP integrity."
- Comparison with the wip build:
  - Byte-identical: every file in `data/processed/`, `tables/`, `figures/` and `schema/`, and every
    file in `results/` except the two below.
  - `results/manuscript_values.csv`, `results/record_cost.csv`: only the six wall-clock
    `rec_cost_*_median_decode_ms` values differ.
  - DOCX text: `manuscript_clean.docx` differs in one token only (median decoding time 4.0 ms vs
    2.7 ms, wall clock); `ESM_1.docx` and `cover_letter.docx` text identical. DOCX/PDF/ZIP binaries
    differ by build timestamps.
- The public code and the public raw data reproduce every seeded number, figure and table.

## Run 1 (PR #773)

Public `main` at `48eb26ddc288e7142cb8c036bef7d4c9921a3c91`, synced from wip `bcad6a557`: exit 0,
51 passed, 20 final files verified; only the six wall-clock decode-time values differed. At that
time the two private snapshot folders were absent from the public tree.
