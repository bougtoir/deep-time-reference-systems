# Numerical hard-code audit (final, ESI package)

Scope: `scripts/esi_content.py`, `scripts/build_submission.py`, `scripts/run_pipeline.py`,
`src/dtrs/**/*.py`, `src/dtrs/plotting/*.py`, `configs/default.yml`, `tests/*.py`. Method: AST scan
of every string constant for numeric tokens (decimals and integers ≥ 10), plus review of every
`v['…']` substitution in the manuscript generator. The JoG-era audit is preserved as
`JOG_HARDCODE_AUDIT_FINAL.md`.

## Classification of numeric literals found in prose-generating code

| Class | Examples (location) | Count | Verdict |
|---|---|---|---|
| Mathematical constants | z = 1.959963984540054 (`benchmark.wilson`, coverage half-width); 2π wrap | 3 | allowed |
| Physical / geodetic constants | WGS84/GRS80 semi-major axes and inverse flattenings (`configs/default.yml`) | 4 | allowed (configuration) |
| Configuration parameters | perturbation 0.05 m, sparse edge probability 0.5, missingness rates, replicates, calibration noise levels (`configs/default.yml`); distance tolerance 0.01 m, longitude tolerance (`benchmark.py`), probabilistic threshold 0.975 (`decode.py`, quoted in ESM S2) | ~20 | allowed; prose reads them from the registry except the rate labels "0.1"/"0.5" that select registry keys `r0p1`/`r0p5` |
| Random seeds | 20260924, seed offsets 3000/1000, +11, +101, +202 | 6 | allowed |
| Test fixtures | `tests/test_records.py` SETTINGS; forbidden-literal list in `tests/test_qc.py` | — | allowed |
| Display parameters | figure sizes, DPI, colours (#374151), font sizes, column widths, table thresholds 0.50 / 0.95 in a caption | many | allowed |
| Bibliographic numbers | years, volumes, pages, DOIs, standard numbers (ISO 19111 …) | ~180 | allowed |
| Generated scientific results | all `v['…']` substitutions (150+), derived ratios (E/B size ratio, RMSE/1e6) | — | generated from `results/manuscript_values.csv` |
| **Improper hard-coded results** | — | **0** | PASS |

Two latent hard-codes were removed in this pass: the calibration noise levels "0.01, 0.03 and 0.1
rad" in the Methods prose (now `v['rec_calibration_noise*_axis_noise_radians']`) and the epoch label
"2015.0 to 2025.0" in the Fig. 3 panel title (now read from `itrf_selected_sites.csv`). Both values
were correct but were not generated.

## Specific values

| Value | Registry key | Generator | Status |
|---|---|---|---|
| 0.274 | `rec_S4_silent_left_handed_export_B_false_certainty` (= BR; also X1 B/E) | `run_scenarios` | generated |
| 0.415 | `rec_S13_epoch_mislabelled_at_export_B_false_certainty` (also X5) | `run_scenarios` | generated |
| 0.137 | `rec_S11_unflagged_coordinate_error_B_false_certainty` (also X2) | `run_scenarios` | generated |
| 0.125 | `rec_S11_unflagged_coordinate_error_E_informative_ambiguity` | `run_scenarios` | generated |
| 0.006 → now 0.0064 | `rec_field_mcar_r*_E_records_with_false_certainty_95ci_high` | `wilson(0, 600)` | generated; display corrected (see `STATISTICAL_VALIDITY_AUDIT.md`) |
| 0.0091 | not present in the current manuscript or registry display (a pre-audit value) | — | not used |
| 0.0183 | not present now; the digital-copy ablation value is 0.0171 after S13 was added (`rec_ablation_chirality_digital_copy_false_certainty`) | `run_ablation` | generated; prompt value is stale |
| 0.0049 / 0.0168 / 0.0666 | `rec_calibration_noise0p01/0p03/0p1_brier_score` | `run_calibration` | generated |
| 8773 bytes | `rec_cost_E_json_bytes` | `run_cost` | generated |
| 2.7 ms (varies) | `rec_cost_E_median_decode_ms` | `run_cost` (wall clock) | generated; non-deterministic by nature, documented |
| All confidence intervals | `*_95ci_low/high`, `*_95ci_halfwidth`, rigidity `*_95ci_*` | `wilson`, normal approx. | generated |

Enforcement: `tests/test_qc.py::test_headline_results_not_hardcoded` fails if headline literals
appear in generator source; `esi_content._same_as_b` and the abstract guard raise if the stress or
MCAR results change so that the prose would become false.
