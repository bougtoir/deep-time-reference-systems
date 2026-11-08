# FINAL QC MATRIX — Earth Science Informatics package (final QC pass)

Scope: `submission/earth_science_informatics_SUBMISSION_FINAL_AUDITED.zip`,
`submission/earth_science_informatics_AUDIT_FINAL.zip`, public mirror
`bougtoir/deep-time-reference-systems`. Baseline: `PRE_FINAL_QC_STATE.md`. JoG matrix preserved as
`JOG_FINAL_QC_MATRIX.md`; journal-format items itemised in `ESI_QC_MATRIX.md`.

| # | Requirement | Status | Evidence (file / test) |
|---|---|---|---|
| 1 | Baseline freeze recorded | PASS | `PRE_FINAL_QC_STATE.md` |
| 2 | Strong, fair baseline (five levels distinguished; no weakening) | PASS | `BASELINE_FAIRNESS_AUDIT.md`; `test_baseline_fixity_flags_post_export_corruption`, `test_redundant_copy_repairs_field_missing_from_primary` |
| 3 | Information-budget separation (information, redundancy, independent evidence, validation, states) | PASS | `BASELINE_FAIRNESS_AUDIT.md` §3; `results/record_ablation.csv`; `results/record_cost.csv` |
| 4 | Failure-model specification per scenario | PASS | `BASELINE_FAIRNESS_AUDIT.md` §4 |
| 5 | Zero-false-certainty claim correctly characterised (deterministic + conditional) | PASS after revision | `ZERO_FALSE_CERTAINTY_AUDIT.md`; stress X1–X5 (`results/record_stress.csv`, Table S5); `test_hybrid_is_not_protected_when_corruption_reaches_evidence`, `test_mislabelled_anchor_induces_false_certainty_in_correct_data`; abstract/Results/Discussion/Limitations/Conclusions |
| 6 | Statistical validity (units, Wilson, zero events, correlation, Brier) | PASS after fix (bound 0.0064) | `STATISTICAL_VALIDITY_AUDIT.md` |
| 7 | Novelty distinguishable from ISO 19111/19115/19157, OGC, PROJJSON, PROV-O, GeoSPARQL | PASS (incremental; editorial risk) | `NOVELTY_AUDIT_FINAL.md` |
| 8 | Zero improperly hard-coded scientific results | PASS | `HARDCODE_AUDIT_FINAL.md`; `test_headline_results_not_hardcoded`; prose guards in `esi_content.py` |
| 9 | Data–text–figure–table consistency | PASS | `DATA_TEXT_FIGURE_TABLE_CONSISTENCY_FINAL.md` |
| 10 | Public fresh-clone reproduction (`make reproduce`, `pytest`) | PASS (public `5a2cd79`, 56 tests, only wall-clock differences) | `PUBLIC_FRESH_CLONE_REPRODUCTION.md` |
| 11 | References exist, metadata match, all cited, all resolve, style | PASS | `REFERENCE_AUDIT_FINAL.md`; `test_references_cited_and_resolved` |
| 12 | Figures/tables cited, ordered, captions, values, no titles in figures | PASS | `FIGURE_TABLE_AUDIT_FINAL.md`; order tests |
| 13 | Supplement necessary and cited; essential content in main text | PASS | `SUPPLEMENT_AUDIT_FINAL.md` |
| 14 | Word format (OMML, no `*`, no docGrid/charSpace, TNR 12 black, captions 10) | PASS | `WORD_FORMAT_AUDIT_FINAL.md`; `tests/test_qc.py` |
| 15 | Journal requirements | PASS except author items | `JOURNAL_COMPLIANCE_FINAL.md` |
| 16 | Five hostile reviews; valid points implemented | PASS | `ADVERSARIAL_REVIEW_FINAL.md`, `ADVERSARIAL_RESPONSE_MATRIX.csv` |
| 17 | Cover letter (problem, record/validator, benchmark, measured reduction, limits, fit; no universal claims; first person) | PASS | `submission_final/cover_letter_final.docx` |
| 18 | Two ZIPs; internal reviews excluded from submission ZIP; manifest + integrity | PASS | `scripts/verify_submission.py`; `test_submission_archive_and_manifest_exist` |
| 19 | Full pipeline and tests | PASS | `make reproduce` exit 0; 56 tests |
| 20 | Private snapshots absent from public mirror | PASS (current tree; still in public history from earlier syncs) | master `EXCLUDE_MAP`; fresh-clone `diff -rq` |
| 21 | Author metadata (affiliation, ORCID, funding, competing interests, route) | NOT VERIFIED (user input) | `FINAL_USER_INPUT_REQUIRED.md` |

## Verdict

No scientific requirement fails after the revisions implemented in this pass. Overall:
**READY AFTER USER METADATA ONLY** (`FINAL_EDITORIAL_DECISION.md`).
