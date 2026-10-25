# Result changelog

## 2026-09-25 final scientific revision

The protected numerical results from the validated pre-revision pipeline are
unchanged. The revision changes their interpretation and presentation by
correcting the residual-invariance hierarchy, qualifying chirality as a physical
witness, and moving the synthetic reflection and corruption experiments to
theorem validation.

New generated results were added for:

- WGS84 versus GRS80 coordinate, chord-distance, and directional sensitivity;
- incomplete-network local rigidity from numerical rigidity-matrix rank; and
- threshold summaries for the seeded framework sizes.

All manuscript numbers are read from `results/manuscript_values.csv`. No
protected value was manually replaced or rounded in source text.

## 2026-09-25 final minor revision

The incomplete-network replication increased from 100 to 2,000 independent
point-and-edge trials per \((n,p)\) cell. The point-count grid,
edge-retention-probability grid, rank criterion, seed and seed offset, Wilson
interval method, and local-rigidity interpretation were unchanged.

| Manuscript location | Old value | New value | Source | Cause | Interpretation impact |
|---|---|---|---|---|---|
| Abstract, \(n=16\) local rigidity | 0.96 at \(p=0.5\) | 0.996 at \(p=0.6\) | `src/dtrs/simulations/rigidity.py`; `scripts/run_pipeline.py` | 20-fold replication | First tested \(p\) with observed frequency >=0.95 moves from 0.5 to 0.6; no universal-threshold claim |
| Methods and Fig. 4 caption | 100 trials per cell | 2,000 trials per cell | `configs/default.yml`; `scripts/run_pipeline.py` | Requested replication increase | Monte Carlo uncertainty is narrower |
| Results, \(n=16,p=0.4\) | 0.630 (0.532–0.718) | 0.608 (0.586–0.629) | `results/rigidity_phase_diagram.csv` | Larger seeded sample | No change to first tested \(p\) with observed frequency >=0.50 |
| Results, \(n=16,p=0.5\) | 0.960 (0.902–0.984) | 0.9465 (0.9358–0.9555) | `results/rigidity_phase_diagram.csv` | Larger seeded sample | Observed frequency is below 0.95 despite the interval spanning 0.95 |
| Results, \(n=16,p=0.6\) | 1.000 (0.963–1.000) | 0.996 (0.992–0.998) | `results/rigidity_phase_diagram.csv` | Larger seeded sample | Becomes first tested \(p\) with observed frequency >=0.95 |
| Table 3, \(n=8\), observed frequency >=0.95 | \(p=0.8\) | \(p=0.9\) | `scripts/run_pipeline.py` | 0.948 observed at \(p=0.8\) after replication | Grid summary changes; qualitative pattern does not |
| Table 3, \(n=16\), observed frequency >=0.95 | \(p=0.5\) | \(p=0.6\) | `scripts/run_pipeline.py` | 0.9465 observed at \(p=0.5\) after replication | Grid summary changes; qualitative pattern does not |
| Figure 4 heatmap | 100-trial cell estimates | 2,000-trial cell estimates | `src/dtrs/plotting/figures.py` | Full regeneration | Visual uncertainty from finite replication is reduced |

All protected WGS84–GRS80, complete-distance reconstruction, mirror
reconstruction, ITRF epoch, and theorem-validation values remained unchanged.

## Final adversarial audit pass (2026-10-17)

| Artifact | Old | New | Source files | Reason | Consequence |
|---|---|---|---|---|---|
| Fig. 4 cell annotations | 2 decimals (showed 0.95 / 1.00) | 3 decimals (0.947 / 0.996) | `src/dtrs/plotting/figures.py` | Hostile-review find: displayed rounding contradicted headline values | Figure and text now identical values; no analysis change |
| Fig. 5 right panel | y-label overlapped colorbar label | y-label moved to right side | `src/dtrs/plotting/figures.py` | Render audit: label collision | Cosmetic fix; no analysis change |
| Supplementary table numbering | station table numbered "Table 1"; ellipsoid "S1"; registry "S2" | S1 (stations), S2 (ellipsoid), S3 (registry); main text ref updated to S2 | `scripts/build_submission.py` | Numbering collision with main-text Table 1 | Consistent supplementary numbering |
| `figures/figure_2_stabilizer_hierarchy.png` | orphaned pre-revision figure | removed | repo tree | Stale artifact | No package content affected (was already excluded) |

## Final QC remediation pass (2026-10-25)

| Artifact | Old | New | Source files | Reason | Consequence |
|---|---|---|---|---|---|
| manuscript equations | plain text (0 OMML) | 90 native m:oMath elements | `scripts/docx_math.py`, `scripts/build_submission.py` prose | QC defect A: Word-native math required | Equations editable in Word; no meaning change; `(-π,π]` restated as `−π < λ ≤ π` and `[x₁,…,xₙ]^T` uses `\left[…\right]` for renderer compatibility |
| Supplementary Table S1, S3 | uncited in prose | cited in Methods | `scripts/build_submission.py` | QC defect B: all tables must be cited | Citation completeness |
| result_traceability.csv | ellipsoid → "Supplementary Table S1" | → "Supplementary Table S2"; added S1/S3 rows | `result_traceability.csv` | QC defect D: stale label | Traceability matches supplement |
| all DOCX | `w:docGrid linePitch=360` | removed | `scripts/build_submission.py::strip_doc_grid` | Character-grid ambiguity | No document grid remains |
| No scientific values changed | — | — | — | Science freeze | `manuscript_values.csv` bit-identical |

## Fresh-clone verification pass (2026-10-25)

| Artifact | Old | New | Source files | Reason | Consequence |
|---|---|---|---|---|---|
| `result_traceability.csv` regeneration | regenerated C6 → "Supplementary Table S1", no C7/C8 | emits S2 + C7 + C8 matching committed CSV | `scripts/run_pipeline.py` | Fresh-clone `make reproduce` revealed generator emitted stale numbering | Traceability is now reproducible end-to-end |
| `distance_reconstruction_rmse_allow_reflection_m` (synthetic) | 2.9701702222673244e-09 | 4.024743751868387e-09 (fresh clone only) | OpenBLAS `DYNAMIC_ARCH` CPU dispatch | Machine-precision noise floor (~1e-9 m); pinned numpy/scipy/pandas identical | Frozen registry value kept; documented in PUBLIC_CODE_FRESH_CLONE_REPRODUCTION.md |
| `distance_reconstruction_rmse_m` (ITRF2020) | 3.6132759390917642e-09 | 3.2363723287752093e-09 (fresh clone only) | same as above | same | same |
| `distance_reconstruction_rmse_proper_only_m` | 6136173.251345326 | 6136173.251345327 (last digit) | same as above | same | same; rounded value 6.136173e6 unchanged |
| All decision-relevant values | — | bit-identical | — | Rigidity probabilities/CIs, 16 sites, 0.691/0.091 m, ellipsoid 0.000225, 100% agreement | Science freeze holds |
