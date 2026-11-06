# FINAL QC MATRIX — Earth Science Informatics package

Scope: `submission/earth_science_informatics_SUBMISSION_FINAL.zip`,
`submission/earth_science_informatics_AUDIT_AND_REPRO_FINAL.zip`, public mirror
`bougtoir/deep-time-reference-systems`. The Journal of Geodesy matrix is preserved as
`JOG_FINAL_QC_MATRIX.md`. Journal-format checks are itemised in `ESI_QC_MATRIX.md`.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Baselines are strong, not strawmen (independent audit) | PASS after fix | BR union reconciliation, B/BR fixity, S13; `NOVELTY_GATE_ESI.md` audit reassessment; tests |
| 2 | Novelty gate still met after fixes | PASS (narrowed) | `NOVELTY_GATE_ESI.md` |
| 3 | Adversarial review + response matrix | PASS (editorial risk remains) | `ADVERSARIAL_REVIEW_ESI.md`, `ADVERSARIAL_RESPONSE_MATRIX_ESI.csv` |
| 4 | Results regenerated from code; changes logged | PASS | `RESULT_CHANGELOG.md`, `results/registry_diff_baseline_audit.csv` |
| 5 | Frozen geometric values unchanged | PASS | registry diff: 0 non-`rec_` changes |
| 6 | Prose numbers from registry, no hard-coding | PASS | `esi_content.py` `v[...]`; `test_headline_results_not_hardcoded` |
| 7 | Schema regenerated, version 1.1.0, examples current | PASS | `schema/dtrs_relation_record.schema.json`, `examples/records/` |
| 8 | References exist and match metadata | PASS | 26 Crossref DOIs title-matched; Crossref "issued" year differs for Chatzinikos & Dermanis, Hogan et al., Shippert & Gaustad because those are online-first dates, and the cited years match `published-print` (2017, 2022, 2017); standards pages HTTP 200 except ISO (403 for scripted fetch; Chrome snapshots in `data/raw/standards/`) |
| 9 | Figures/tables cited, first-citation order, separate figure files | PASS | builder guards; `figures/Fig1–6.png` |
| 10 | Abstract ≤250 words, keywords, declarations, AI disclosure | PASS | `ESI_QC_MATRIX.md` |
| 11 | Required file names | PASS | `manuscript_clean.docx/.pdf`, `FINAL_QC_MATRIX.md`, `PUBLIC_FRESH_CLONE_REPRODUCTION.md` |
| 12 | Private material not in upload ZIP or public mirror | PASS | `verify_submission.py`; `EXCLUDE_MAP` for `data/raw/journal_esi`, `data/raw/standards` (still present in public git history from earlier syncs) |
| 13 | Public fresh-clone reproduction | PASS | `PUBLIC_FRESH_CLONE_REPRODUCTION.md` (51 tests; only wall-clock differences) |
| 14 | Author metadata | OPEN | `FINAL_USER_INPUT_REQUIRED.md` (5 items) |

## Verdict

**READY AFTER USER METADATA ONLY.** The scientific claim is narrower than in #771. The
remaining risks are editorial: novelty relative to ISO 19157, author-designed scenarios, and anchors
whose independence is assumed in each scenario.
