# Figure and table audit (final)

All items were regenerated in this pass and rendered for visual inspection (contact sheet of the ten
PNG files; tables read back from the DOCX).

| Item | Cited in text | First-citation order | Caption matches content | Values match Results | Axes / units | Clipping | Stale embedded values |
|---|---|---|---|---|---|---|---|
| Fig. 1 residual invariance chain | yes | 1 | yes | n/a (schematic) | n/a | none | none |
| Fig. 2 record data flow | yes | 2 | yes | n/a | n/a | none | none |
| Fig. 3 ITRF2020 network | yes | 3 | yes | median 0.091 m = `median_pairwise_distance_change_m` | degrees; mm yr⁻¹; m | none | epoch label now generated from data |
| Fig. 4 scenario heat maps (A–E × S0–S13) | yes | 4 | yes ("proportion of 496 task items") | cell values = `rec_S*` (e.g. B S4 0.27, B S13 0.42, E S13 0.61) | proportion | small cell font but legible at 600 dpi | none |
| Fig. 5 random loss | yes | 5 | yes (Wilson intervals over records; 200 replicates × 3 conventions) | E zero line; BR/B coverage as in text | proportion; deletion probability | none | none |
| Fig. 6 ablation and calibration | yes | 6 | yes | FC labels 0.0345, 0.0171 = registry | proportion; probability | none | none |
| Table 1 representations | yes | 1 | yes | n/a | n/a | none | none |
| Table 2 record fields (schema 1.1.0) | yes | 2 | version read from `SCHEMA_VERSION` | n/a | n/a | none | none |
| Table 3 scenario outcomes | yes | 3 | yes | from `results/record_scenarios.csv` via `scenario_outcome_table` | proportion | landscape section | none |
| Table 4 geometric foundations / rigidity | yes | 4 | yes | 0.9465, 0.996 = frozen registry | proportion | none | none |
| Figs. S1–S4 | "Figs. S1–S4" | after Table S1 family as tested | yes | S3 1.000/0.000 = registry; S4 accuracy curves = `uncertainty_benchmark` | labelled | none | none |
| Table S1 stations | yes | S1 | yes | `itrf_selected_sites.csv` | degrees, epochs | none | none |
| Tables S2–S4 | "Tables S2–S4" | S2–S4 | yes | registry | units column | none | none |
| Table S5 stress scenarios (new) | "Online Resource 1, Table S5" | S5 (after S2–S4) | yes | `results/record_stress.csv`; text values 0.274, 0.137, 0.177, 0.415, 0.272 | proportion | none | none |

Changes in this pass: figure-level titles removed from Figs. 1, 2, 3, 6 (panel labels kept) and
Figs. S1–S4, following the ESI artwork instruction "no titles inside figures"; Table S5 added;
captions set to 10 pt. No obsolete numbering remains (`tests/test_qc.py` order and traceability
tests; labels limited to Table S1–S5). Note: figure lettering uses the matplotlib default sans-serif
(DejaVu Sans) rather than Helvetica/Arial.
