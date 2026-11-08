# Supplementary material audit

| Item | Content | Necessary? | Cited in manuscript | Decision |
|---|---|---|---|---|
| Online Resource 1 (ESM_1.pdf / .docx) | sections S1–S10 below | yes | "Online Resource 1" (Methods) | retained |
| S1 Formal assumptions and degeneracies | assumptions of the relational path | yes (reviewers of Methodology articles need assumptions) | via Online Resource 1 | retained |
| S2 Decoder algorithm | step-by-step algorithm | yes (reproduce and apply) | "Online Resource 1 (Sect. S2)" | retained |
| S3 Schema and examples | pointer to ESM_2 | yes | via Online Resource 2 | retained |
| S4 Configuration | full YAML configuration | useful for reproduction; also in code archive | via Online Resource 1 | retained (short) |
| S5 Table S1 ITRF2020 stations | station list and epochs | yes (data provenance) | "Table S1" | retained |
| S6 Tables S2–S3 | ellipsoid sensitivity; frame taxonomy | supporting | "Tables S2–S4" | retained |
| S7 Figs. S1–S4 | geometric foundations | supporting; foundations, not contribution | "Figs. S1–S4" | retained |
| S8 Table S4 | registry values cited in the manuscript | yes (traceability) | "Tables S2–S4" | retained |
| S9 Table S5 (new) | stress scenarios X1–X5 | yes: essential limitation; key numbers are also in the main Results text | "Online Resource 1, Table S5" | retained; essential content integrated into main text (Results, Discussion, Limitations, abstract) |
| S10 Test coverage | description of the test suite | marginal | via Online Resource 1 | retained (one paragraph); full tests in the code archive |
| Online Resource 2 (ESM_2.zip) | schema, example records, registry, benchmark CSVs (incl. `record_stress.csv`) | yes | "Online Resource 2" | retained |

Execution logs and environment details are not in the supplement; they are in the repository and the
audit archive (`earth_science_informatics_AUDIT_FINAL.zip`). Every retained section, figure and table
is reachable from a manuscript citation; first-citation order is enforced by
`tests/test_qc.py::test_first_citation_order_is_monotonic` (Table S1 → Tables S2–S4 → Table S5).
Each ESM file carries the title, author and correspondence e-mail (journal requirement); journal
name appears in the cover letter and title page.
