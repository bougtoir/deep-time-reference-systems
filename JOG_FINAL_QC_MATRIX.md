# FINAL QC MATRIX — Journal of Geodesy submission package

Date: 2026-10-25. Scope: `journal_of_geodesy_submission_FINAL_LOCKED.zip` +
public mirror `bougtoir/deep-time-reference-systems` @ `9f833606`.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Adversarial review round 2 (12 challenges) | PASS | ADVERSARIAL_REVIEW_FINAL_2.md + ADVERSARIAL_RESPONSE_MATRIX_FINAL_2.csv — all criticisms resolved or explicitly bounded |
| 2 | No improperly hard-coded scientific results | PASS — no improperly hard-coded scientific results found. | HARDCODE_AUDIT_FINAL.md + hardcode_inventory.csv (A=14,B=358,D=100,E=224,F=0,G=0,H=0) |
| 3 | Fresh-clone reproduction from public main | PASS | PUBLIC_CODE_FRESH_CLONE_REPRODUCTION.md — `make setup && make reproduce` on `9f833606`, 38 tests green; documented 1e-9 m BLAS noise-floor variance only |
| 4 | All references exist (24/24) | PASS | REFERENCE_AND_CITATION_COMPLETENESS_AUDIT.md + references_verified.csv (verified_utc 2026-10-25) |
| 5 | Every reference cited in prose | PASS | REFERENCE_AND_CITATION_COMPLETENESS_AUDIT.md — 24/24 entries cited; every citation resolves |
| 6 | Every figure/table cited in prose | PASS | FIGURE_TABLE_CITATION_AUDIT.md — Fig. 1–5, Table 1–3, Supp Fig S1–S2, Supp Table S1–S3 all cited outside captions |
| 7 | Numbers consistent (data→code→registry→prose→supplement) | PASS | DATA_TEXT_FIGURE_TABLE_CONSISTENCY_FINAL.md — families A–H traced end-to-end |
| 8 | First-citation order monotonic | PASS | FIGURE_TABLE_CITATION_AUDIT.md — Fig 1-5, Table 1-3, SuppTable S1→S2→S3, SuppFig S1→S2 all monotonic (test enforced) |
| 9 | Reference style | PASS | Author–year, alphabetical — "journal-specific author–year/alphabetical style supersedes first-appearance numbering"; ISO 19111 cited as "ISO 2019"; Torsvik & Cocks 2019 |
| 10 | True OMML equations | PASS | WORD_OMML_AUDIT.md — 90 `m:oMath` elements, editable in Word, no image/LaTeX-string equations; supplement inspected |
| 11 | No literal `*` in any DOCX | PASS | WORD_MARKUP_AUDIT.md — 0 literal asterisks in all 6 DOCX |
| 12 | No `w:docGrid` linesAndChars / charSpace | PASS | WORD_GRID_AND_LINEBREAK_AUDIT.md — docGrid removed from all DOCX; code-block/page/table breaks kept |
| 13 | Traceability current (S1/S2/S3) | PASS | result_traceability.csv C6→S2 + C7/C8 rows; `run_pipeline.py` regenerates identical file (fresh-clone verified) |
| 14 | Public repo synchronized | PASS | PUBLIC_REPO_SYNC_AUDIT.md — blob-hash equality on all critical files; canonical commit `9f833606` |
| 15 | Automated tests A–H pass | PASS | `pytest`: 38/38 green in both wip tree and fresh clone |

## Verdict

**B. PASS AFTER USER METADATA ONLY**

The only outstanding items are the author-supplied metadata placeholders
already isolated in `FINAL_USER_INPUT_REQUIRED.md` (affiliations, ORCID,
funding, competing interests). All scientific content, packaging, public
reproducibility, and QC gates pass. The frozen values are unchanged
(`manuscript_values.csv` bit-identical throughout this remediation).
