# Pre-final-QC state (frozen baseline for the final audit)

Recorded before any change made in the final QC pass.

| Item | State |
|---|---|
| Canonical repository | `bougtoir/wip`, subdirectory `deep_time_reference_systems/` |
| Canonical commit | `b7d6686f5b66e34b75823357d55cac47752e611b` (`master`, merge of PR #774, 2026-11-08) |
| Working branch for this pass | `devin/1794134523-dtrs-esi-final-qc` (from the commit above) |
| Public mirror | https://github.com/bougtoir/deep-time-reference-systems, `main` at `9f8c649` (synced from the commit above; `data/raw/journal_esi/` and `data/raw/standards/` excluded) |
| Manuscript | `submission_final/manuscript_clean.docx` (1,370,806 bytes, sha256 `a538b69b…a3f8`), Methodology article, abstract 248 words, 6 keywords |
| Result registry | `results/manuscript_values.csv`, 976 metrics (+ header); schema version 1.1.0 |
| Figures | main Figs. 1–6 (`figures/figure_1…6_*.png`), Online Resource 1 Figs. S1–S4 |
| Tables | main Tables 1–4; Online Resource 1 Tables S1–S4 |
| Supplementary | ESM_1 (PDF + DOCX, sections S1–S9), ESM_2.zip (schema, examples, registry, benchmark CSVs) |
| Test suite | 51 tests (`tests/`), all passing; `make reproduce` exit 0 |
| Submission ZIPs | `submission/earth_science_informatics_SUBMISSION_FINAL.zip`, `submission/earth_science_informatics_AUDIT_AND_REPRO_FINAL.zip` (20 files in manifest) |
| Verdict carried in | "READY AFTER USER METADATA ONLY" (`FINAL_EDITORIAL_DECISION.md` at the commit above) |

All validated analyses are frozen by default. Changes made in this pass and their reasons are in
`RESULT_CHANGELOG.md` (section "Final QC pass").
