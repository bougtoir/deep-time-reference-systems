# Figure/table citation audit

Audit date: 2026-10-25 (against rebuilt `manuscript/manuscript.docx`)

First prose-citation positions (character offset in body text):

| Item | First prose citation (offset) | Order |
|---|---|---|
| Fig. 1 | 3041 | 1st figure |
| Fig. 2 | 7841 | 2nd |
| Fig. 3 | 8892 | 3rd |
| Fig. 4 | 14199 | 4th |
| Fig. 5 | 16227 | 5th |
| Table 1 | 7852 | 1st table |
| Table 2 | 11431 | 2nd |
| Table 3 | 12041 | 3rd |
| Supplementary Table S1 | 13130 | 1st supp. table |
| Supplementary Table S2 | ~13500 | 2nd |
| Supplementary Table S3 | ~13900 | 3rd |
| Supplementary Fig. S1 | 15794 | 1st supp. figure |
| Supplementary Fig. S2 | 16150 | 2nd |

Monotonic within every family; no skipped, duplicated, or orphan numbers.
Supplementary Tables S1 and S3 are now cited in Methods prose ("listed in
Supplementary Table S1"; "reproduced as Supplementary Table S3"); S2 is cited
in Methods and again in Results. Guarded by
`tests/test_qc.py::test_supplementary_items_are_cited` and
`test_first_citation_order_is_monotonic`.

PASS — all main and supplementary figures/tables are explicitly cited in
prose, in first-citation numbering order.
