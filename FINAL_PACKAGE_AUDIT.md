# Final package audit

Inspected regenerated `submission/journal_of_geodesy_submission_FINAL.zip`
(and identical content in `journal_of_geodesy_submission_FINAL_AUDITED.zip`).

Contents (27 entries = 26 manifest files + MANIFEST.csv):

- manuscript_inline.docx, manuscript.pdf
- figures_editable.pptx, tables_editable.docx
- supplement.docx, supplement.pdf
- cover_letter.docx, title_page.docx, declarations.docx
- dtrs_reproducibility.zip (code, config, tests, persisted raw inputs, acquisition ledger,
  prior audit docs)
- FINAL_SUBMISSION_README.md, AUTHOR_CHECKLIST.md, FINAL_USER_INPUT_REQUIRED.md,
  DATA_CODE_AVAILABILITY.txt, AI_DISCLOSURE.txt
- figures/ (7 PNGs: Fig 1–5, S1, S2)
- tables/ (4 CSVs)
- MANIFEST.csv (name,size,sha256 — regenerated with current hashes)

## Exclusion check

- No old manuscript versions, no stale figures (orphan stabilizer figure removed),
  no internal audit md files, no temp/cache/OS files (no .DS_Store, __pycache__, .venv),
  no previous submission zips, no obsolete result CSVs.
- Internal audit reports from this pass remain in the repo root, outside the ZIP.
- `verify_submission.py` re-verified manifest membership and CRC after regeneration.
