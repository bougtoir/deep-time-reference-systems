# Data–text–figure–table consistency audit

Chain verified: data -> `run_pipeline.py` -> `results/*.csv` -> `manuscript_values.csv` ->
tables -> figures -> manuscript/supplement text.

| Result family | Source | Figure | Table | Text | Status |
|---|---|---|---|---|---|
| A. Local rigidity | results/rigidity_phase_diagram.csv | Fig. 4 (cells now show exact 3-dp values) | Table 3 | §4–5, Abstract | consistent after Fig. 4 fix |
| B. WGS84–GRS80 | results/ellipsoid_sensitivity.csv | — | Table S2 | §4–5, Abstract | consistent |
| C. Complete-distance reconstruction | results/synthetic_summary.csv | — | S3 registry | §5 | consistent |
| D. Proper-only mirror RMSE | results/synthetic_summary.csv | — | S3 registry | §5, S8 | consistent |
| E. Symmetry validation | results/synthetic_summary.csv | Suppl. Fig. S1 | S3 registry | §5 | consistent |
| F. Orientation-label corruption | results/uncertainty_results.csv | Suppl. Fig. S2 | S3 registry | §5 | consistent |
| G. ITRF2020 selection | data/raw/itrf2020 (sha256-verified) -> results/itrf_summary.csv | Fig. 5 left | Suppl. Table S1 | §4–5 | consistent |
| H. Epoch propagation | results/itrf_summary.csv | Fig. 5 right (median = 0.091 m matches text) | — | §4–5, Abstract | consistent |

No branch divergence found: one registry, one builder, one figure generator. Fig. 4's
2-decimal display was the only divergence and is fixed.
