# Word formatting audit (final)

Inspected the DOCX XML (`word/document.xml`, `word/styles.xml`) of `manuscript.docx`,
`supplement.docx` (ESM_1), `cover_letter.docx` (→ `cover_letter_final.docx`), `title_page.docx`,
`declarations.docx`, `tables.docx` after the final build.

| Check | Result | Evidence |
|---|---|---|
| Equations are Word-native OMML | PASS: 13 `m:oMath` elements in the manuscript; ESM_1 has no display equations | XML count; `tests/test_qc.py` OMML test (arcsin, atan2, det, π, ℝ, ∘ present in `m:t`) |
| No equation images | PASS: no EMF/WMF/equation pictures; the only images are Figs. 1–6 | XML scan |
| No residual Markdown asterisks | PASS: 0 `*` in all six DOCX | XML scan; test |
| No character spacing / grid | PASS: no `w:docGrid`, no `linesAndChars`, no `w:charSpace` | `strip_doc_grid`; `tests/test_qc.py` |
| No hard line breaks inside runs | PASS | `test_manuscript_contains_all_cited_figures_and_tables` |
| Fonts | PASS: Normal, Title, Heading 1–2 = Times New Roman; Equation style Cambria Math (OMML default); ESM configuration listing Courier New 8 pt (code) | styles read back with python-docx |
| Sizes | PASS: body 12 pt; Heading 1 14 pt; Heading 2 12 pt; Title 18 pt; figure/table captions 10 pt; table cells 8 pt (wide tables, e.g. Table 3 with 10 columns, must fit the page) | styles; builder |
| Colour | PASS: used styles black (000000); colours left in unused built-in template styles have no effect | styles |
| Heading levels | PASS: ≤3 (journal limit) | builder |
| Clipped equations/tables | PASS: Table 3 in landscape section; PDF render checked | `manuscript_clean.pdf` |
| Placeholders | OPEN (explained): "[to be confirmed]" for ORCID on the title page and funding/competing-interest placeholders, listed in `FINAL_USER_INPUT_REQUIRED.md` | title page, declarations |

Previously (before this pass) the body was 11 pt and headings were coloured Arial; corrected in
`build_submission.style_document`.
