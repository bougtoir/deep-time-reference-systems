# Reference verification audit

## Scope

All 24 references cited by the manuscript generator were rechecked on
2026-09-25 for existence, author order, issue-year, title, container, volume,
issue, pagination or article number, and DOI where applicable.

## Result

- 22 DOI-bearing references match persisted Crossref work-record snapshots in
  `data/raw/literature/`.
- The IERS Conventions (2010) entry matches the persisted official Technical
  Note 36 PDF.
- ISO 19111:2019 matches the official ISO catalogue entry. The catalogue
  reports edition 3, publication in January 2019, and current confirmed status.
- Every citation in the manuscript generator has a row in
  `references_verified.csv`; there are no unmatched or extra DOI entries.
- Chatzinikos and Dermanis is cited as 2017, matching the print issue year
  rather than the 2016 online-first year.
- Torsvik and Cocks is cited as 2019, matching Geological Magazine volume 156,
  issue 2, rather than the 2017 online-first year.

The verification timestamps and sources in `references_verified.csv` were
updated. Newly acquired snapshots were added without overwriting earlier raw
files, and their sizes and SHA-256 values were recorded in
`data/data_acquisition_log.csv`.
