# Journal of Geodesy final submission package

## Status

**SUBMISSION READY AFTER METADATA ONLY.**

The scientific analysis, reproducibility bundle, editable files, PDF files,
checksums, and archive integrity checks are complete. Before portal upload,
the author must complete only the items listed in
`FINAL_USER_INPUT_REQUIRED.md`.

## Primary upload files

- `manuscript_inline.docx` — manuscript with five inline main figures and
  three inline main tables
- `manuscript.pdf` — rendered manuscript for final visual checking
- `title_page.docx`
- `cover_letter.docx`
- `declarations.docx`
- `DATA_CODE_AVAILABILITY.txt`
- `AI_DISCLOSURE.txt`
- `supplement.docx` and `supplement.pdf`
- `figures_editable.pptx` and `tables_editable.docx`
- `figures/` and `tables/` — separate generated display files
- `dtrs_reproducibility.zip`
- `MANIFEST.csv`

## Reproduction

From the project root:

```bash
make setup
make reproduce
```

The first command creates the pinned environment. The second verifies raw
checksums, regenerates analyses and documents, runs compilation and all tests,
and validates the final manifest and ZIP archive.

## Scope

The central result is a conditional residual-invariance hierarchy for Euclidean chord
distance under explicitly stated origin, scale, axis, physical-chirality, and
meridian assumptions. The incomplete-network calculation establishes local
rigidity rank only; it is not a claim of global rigidity. The ITRF2020 result
is an epoch-sensitivity and computational-symmetry demonstration, not a
physical reflected realization or a geological propagation experiment.
