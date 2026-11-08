# Journal compliance (Earth Science Informatics), final

Source of requirements: official Springer pages captured 2026-11-06 (`ESI_JOURNAL_REQUIREMENTS.md`;
snapshots in the private audit copy `data/raw/journal_esi/`). Nothing below is inferred beyond those
pages; items the pages do not state are marked "not stated".

| Requirement | Official statement | Package | Status |
|---|---|---|---|
| Article type | research, methodology (experimental/computational/simulation/theoretical), software … | Methodology article; Method section with algorithm (ESM S2), testing and implementation details | PASS |
| Abstract | 150–250 words | 246 words after this pass (builder guard; `test_manuscript_contains_all_cited_figures_and_tables`) | PASS |
| Keywords | 4–6 | 6 | PASS |
| Main text length | not stated (only Comments ≤1000 words) | — | N/A |
| Text format | Word, plain font (e.g. 10-pt Times Roman), page numbering, equation editor, ≤3 heading levels | DOCX, Times New Roman 12 pt (default rule; "e.g." allows it), black, OMML equations, 2 heading levels | PASS |
| Figures | separate files Fig1…; captions in text file; no titles inside figures; Helvetica/Arial lettering; ≤174 mm wide | `figures/Fig1–6.png` in ZIP; editable PPTX; figure-level titles removed in this pass; matplotlib DejaVu Sans lettering (sans-serif, not Arial) | PASS with note (lettering font) |
| Tables | Arabic numerals, cited consecutively, caption above | Tables 1–4, captions above, order test | PASS |
| Supplementary material | "Online Resource N", ESM_N files, text as PDF, title/author/e-mail in each file | ESM_1.pdf (+ editable .docx), ESM_2.zip; Online Resource 1/2 cited in order | PASS |
| Data availability | mandatory statement | Statements and Declarations + `DATA_CODE_AVAILABILITY.txt` (public repository, checksummed raw ITRF2020 input) | PASS |
| Code availability | as applicable | public repository URL | PASS |
| AI disclosure | LLM use documented in Methods; LLMs not authors | Methods paragraph + `AI_DISCLOSURE.txt` | PASS |
| Author contributions | required statement (CRediT style shown) | single-author statement | PASS |
| Funding | statement required | placeholder pending author | OPEN (user metadata) |
| Competing interests | statement required | placeholder pending author | OPEN (user metadata) |
| Title page | title, author, affiliation, e-mail, ORCID if available | affiliation and ORCID pending | OPEN (user metadata) |
| Ethics / consent | as applicable | "not applicable" (no human/animal data) | PASS |
| Submission files | editable sources at every submission | manuscript DOCX, tables DOCX, figures PPTX, ESM_1 DOCX | PASS |
| Publication model / APC | Hybrid; subscription route without mandatory APC; Open Choice APC "varies by journal" | APC amount NOT VERIFIED; the route is an author decision | OPEN (author choice) |
| Reference style | author–year; alphabetical list; full DOI links | as required | PASS |
