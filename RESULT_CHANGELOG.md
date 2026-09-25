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
