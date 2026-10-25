# Data–text–figure–table consistency (final)

Audit date: 2026-10-25

Result families traced data → code → canonical output → manuscript_values.csv
→ result_traceability.csv → tables/figures/captions → manuscript prose →
supplement:

A. Rigidity phase diagram: `rigidity_phase_diagram.csv` → Table 3, Fig. 4
   annotations (3-decimal), abstract/Results values (0.9465, Wilson
   0.9358–0.9555 at p=0.5; 0.996, 0.9921–0.9980 at p=0.6; first tested
   p≥0.95 = 0.6; 2000 trials/cell; seed 20260924). Consistent.
B. WGS84–GRS80 sensitivity: `ellipsoid_sensitivity.csv` → Supplementary
   Table S2, Results paragraph, abstract (0.000225 m max; 100% agreement).
   Consistent.
C. Complete-distance reconstruction: `distance_reconstruction.csv` →
   reflection-permitting RMSE 2.97e-09 m (synthetic) in Results. Consistent.
D. Proper-only mirror ambiguity: 6.136173e6 m in Results + supplement S8.
   Consistent.
E. Symmetry validation: reflection accuracies → Fig. 3, Supplementary Fig. S1
   caption (1.000 over seeded trials). Consistent.
F. Orientation-label corruption: Monte Carlo accuracies → Supplementary
   Fig. S2 + prose. Consistent.
G. ITRF station selection: `itrf_selected_sites.csv` → Supplementary Table
   S1, 16 sites in prose, Fig. 5 left panel. Consistent.
H. ITRF epoch propagation: `itrf_distance_changes.csv` → Fig. 5 right panel,
   Results + abstract (max 0.691 m, median 0.091 m, 2015.0→2025.0).
   Consistent.

No mismatches. `manuscript_values.csv` regenerated bit-identical under
`make reproduce`.
