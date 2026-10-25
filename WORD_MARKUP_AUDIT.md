# Word markup / asterisk audit

Audit date: 2026-10-25

Inspected `word/document.xml` and extracted visible text of all submission
DOCX files:

- manuscript_inline.docx — 0 `*` characters in visible text
- supplement.docx — 0
- tables_editable.docx — 0
- cover_letter.docx — 0
- title_page.docx — 0
- declarations.docx — 0

No `**bold**`, `*italic*`, backticks, or Markdown headings survive; emphasis
uses Word run properties. Equations are OMML elements, not literal markup.
Guarded by `tests/test_qc.py::test_no_markdown_asterisks`.

PASS — visible-text Markdown-asterisk count = 0.
