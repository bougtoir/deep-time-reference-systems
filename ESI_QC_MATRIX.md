# ESI QC matrix (generated package, checked by `make reproduce` unless noted)

| # | Check | Requirement source | Evidence | Status |
|---|---|---|---|---|
| 1 | Abstract 150–250 words | ESI guidelines | `build_manuscript` guard; `test_manuscript_contains_all_cited_figures_and_tables` (≤250 words, guard in builder) | PASS |
| 2 | 4–6 keywords | ESI guidelines | test (6 keywords) | PASS |
| 3 | Editable DOCX manuscript + source | ESI guidelines | `manuscript_clean.docx`, `ESM_1.docx`, `tables_editable.docx`, `figures_editable.pptx`, `cover_letter_final.docx` | PASS |
| 4 | Figures cited in order, separate files | ESI guidelines; account rules | builder order guard; `figures/Fig1–6.png` in ZIP | PASS |
| 5 | Tables cited in order, editable | ESI guidelines | builder order guard; 4 Word tables | PASS |
| 6 | Supplements as Online Resource N / ESM_N | ESI guidelines | `ESM_1.pdf`, `ESM_2.zip`; `test_supplementary_items_are_cited`, order test | PASS |
| 7 | Statements and Declarations incl. data/code availability | ESI guidelines | manuscript section + `declarations.docx`; test | PASS (funding/competing interests are author inputs) |
| 8 | LLM use documented in Methods, not as author | ESI AI policy | Sect. 4 "Use of AI tools"; `AI_DISCLOSURE.txt` | PASS |
| 9 | Every reference cited and every citation resolved | Integrity | `test_references_cited_and_resolved` (36) | PASS |
| 10 | Every reference verified against persisted metadata | Integrity | `references_verified.csv` from `build_reference_ledger.py` (26 Crossref, 9 standards snapshots, 1 IERS) | PASS |
| 11 | No hard-coded headline values | account rule | `test_headline_results_not_hardcoded` | PASS |
| 12 | Numbers from registry | account rule | `esi_content.py` reads `manuscript_values.csv`; Table S4 lists cited values | PASS |
| 13 | OMML math, no Markdown artefacts, no doc grid, no hard line breaks in runs | account rules | `test_qc.py`; run-level newline test | PASS |
| 14 | Traceability labels current | Integrity | `test_traceability_numbering_is_current` (C1–C13) | PASS |
| 15 | Schema/validator/decoder tests | Task | `tests/test_records.py` | PASS |
| 16 | ZIP integrity and manifest | Task | `verify_submission.py` | PASS |
| 17 | Private reviews excluded from submission ZIP | Task | `verify_submission.py`, test | PASS |
| 18 | Public mirror reproduces from clean clone | account rule | `PUBLIC_FRESH_CLONE_REPRODUCTION.md` | see file |
| 19 | Journal name absent from public repo name | account rule | `deep-time-reference-systems` | PASS |
| 20 | Scope: principal contribution is informatics | ESI aims | `NOVELTY_GATE_ESI.md` Phase 5; title/abstract/sections | PASS (editorial risk remains) |
