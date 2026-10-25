# Reference existence and citation completeness audit

Audit date: 2026-10-25

## Existence

All 24 bibliography entries re-verified:

- 14 DOIs resolved directly (HTTP 200; IEEE returned 202).
- 7 DOIs blocked by publisher bot-protection on doi.org (403) but resolved
  through the Crossref metadata API with matching container and year:
  10.1029/2001JB000561 (JGR Solid Earth 2002), 10.1029/2002GL016279 (GRL 2003),
  10.1107/S0567739476001873 (Acta Cryst. A 1976),
  10.1107/S0567739478001680 (Acta Cryst. A 1978), 10.1137/120875909
  (SIAM Rev. 2014), 10.1029/2007RG000227 (Rev. Geophys. 2008),
  10.1090/S0002-9947-1978-0511410-9 (Trans. AMS 1978).
- 2 non-DOI official URLs (IERS TN36 PDF, ISO 19111 catalog page).

`references_verified.csv` `verified_utc` updated to 2026-10-25T00:00:00Z.

## Citation completeness (both directions)

- All 24 entries cited at least once in body text.
- Every parenthetical author–year citation resolves to a bibliography entry.
- ISO 19111 cited as "ISO 2019" as specified; Torsvik & Cocks remains 2019.
- No orphan reference; no orphan citation.

Guarded by `tests/test_qc.py::test_references_cited_and_resolved`.

## Style/order

Journal of Geodesy uses author–year citations. In-text citations are
author–year throughout; the bibliography is alphabetized per Springer style;
no numeric-reference remnants.

PASS — journal-specific author–year/alphabetical style supersedes
first-appearance numbering.
