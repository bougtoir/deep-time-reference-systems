# Word document grid / line-break audit

Audit date: 2026-10-25

All generated DOCX files previously inherited `w:docGrid w:linePitch="360"`
from the python-docx default template (a harmless line-grid hint, but
ambiguous under the no-character-grid requirement; Journal of Geodesy does
not require a document grid).

Action: `strip_doc_grid()` in `scripts/build_submission.py` now removes every
`w:docGrid` element from all sections of every generated DOCX before save.

Post-rebuild verification over the six DOCX files:

- `w:docGrid` count: 0 in all files
- `w:type="linesAndChars"`: 0
- `w:charSpace`: 0
- no manual line breaks forcing prose wrapping (the supplement config block
  intentionally uses a monospace preformatted run — code-like content, kept)

Guarded by `tests/test_qc.py::test_no_character_grid`.

PASS — no character-count line wrapping or document grid remains.
