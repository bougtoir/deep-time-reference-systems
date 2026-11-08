# Data–text–figure–table consistency (final)

The JoG-era report is preserved as `JOG_DATA_TEXT_FIGURE_TABLE_CONSISTENCY_FINAL.md`.

## Method

1. Every number in the manuscript prose, captions and tables, the cover letter and the editable
   tables was extracted from the built DOCX files (regex over paragraphs and table cells) and matched
   against `results/manuscript_values.csv` at the displayed precision. Excluded: years, citation
   volume/page numbers, DOIs, standard numbers (ISO 19111 …), "95%", "SHA-256", counts ≤ 20.
2. The prose generator substitutes registry values only (`v['…']`); guards raise if the stress or
   MCAR results change in a way that would make fixed wording ("the same proportions as B",
   "no proposed record produced false certainty") false.
3. Figures and Tables 3 and S5 are generated from the same result CSVs as the registry in one
   pipeline run.

## Result

| Document | Numbers checked | Unmatched | Explanation |
|---|---|---|---|
| Manuscript (abstract, body, captions, Tables 1–4) | all | 2 | both derived in code from registry values: 2.72 = `rec_cost_E_size_ratio_to_A / rec_cost_B_size_ratio_to_A`; 6.136 = `distance_reconstruction_rmse_proper_only_m / 1e6` |
| Cover letter | all | 0 | — |
| Editable tables | all | 0 | — |
| ESM_1 | all | site coordinates (Table S1, from `itrf_selected_sites.csv`) and configuration listing (S4, from `configs/default.yml`) | both are data/configuration, not results |

## Labels

- Representations A, B, BR, C, D, E: identical definitions in Methods, Table 1, Fig. 4, Table 3,
  Table S5 and the code (`REPRESENTATIONS`).
- Tasks T1–T5 defined in Methods; T6 (identity) evaluated through collisions (S6) and, now, the
  consistent identifier swap X3.
- Scenarios S0–S13 (16 including S1a–c) and X1–X5: labels in Methods, Table 3, Fig. 4 and Table S5
  come from `SCENARIO_LABELS` / `STRESS_LABELS`.
- Denominators: 496 task items per deterministic scenario (captions of Fig. 4 and Table S5;
  Methods); 600 records per rate under random loss (abstract, Results, Fig. 5 caption).
- Units: m for distances and tolerances, rad for anchor noise, degrees for longitude, bytes and ms
  for cost.

Verdict: PASS (no numerical mismatch).
