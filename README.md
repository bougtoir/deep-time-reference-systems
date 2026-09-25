# Deep-Time Reference Systems

This project studies the minimum information required to preserve and later
reconstruct time-indexed spatial relations when the original coordinates,
datum, frame realization, software, or naming infrastructure is unavailable.
The work is framed as geodetic reference-system theory and distance geometry;
deep-time scenarios are boundary-condition stress tests rather than forecasts.

## Reproduce

```bash
make setup
make reproduce
```

`make setup` creates the pinned local environment once. `make reproduce`
verifies raw-input checksums, runs all seeded analyses, regenerates figures,
tables, manuscript values, manuscript and supplement files, runs compilation
and the complete test suite, then checks the final manifest and ZIP byte for
byte.

## Main outputs

- `submission_final/manuscript_inline.docx` and
  `submission_final/manuscript.pdf`
- `submission_final/title_page.docx` and
  `submission_final/cover_letter.docx`
- `manuscript/figures.pptx` and `manuscript/tables.docx`
- `supplement/supplement.docx` and `supplement/supplement.pdf`
- `submission_final/figures/` and `submission_final/tables/`
- `submission_final/dtrs_reproducibility.zip`
- `submission/journal_of_geodesy_submission_FINAL.zip`
- `results/manuscript_values.csv`
- `result_traceability.csv`
- `references_verified.csv`
- `INTEGRITY_AUDIT.md`, `CONSISTENCY_AUDIT.md`, and `ADVERSARIAL_REVIEW.md`

## Method summary

With origin fixed or removed and metric scale known, complete labeled
Euclidean chord distances leave an \(O(3)\) ambiguity. A directed axis reduces
the residual invariance group to \(O(2)\); a physically recoverable chiral witness
reduces it to \(SO(2)\); and an independently recoverable directed meridian
removes the remaining rotation. Epoch, uncertainty, entity identity, and
provenance remain separate necessary metadata.

## Data

The real-data example uses the official ITRF2020 SLR station coordinate and
velocity file. Acquisition metadata and checksums are in
`data/data_acquisition_log.csv`. Copyrighted journal web-page snapshots used
for requirement checking are retained locally but intentionally excluded from
repository distribution.
