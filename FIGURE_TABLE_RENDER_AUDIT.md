# Figure/table render audit (visual inspection of regenerated outputs)

- Fig. 1: layers readable, no clipping. OK.
- Fig. 2: hierarchy nodes/annotations readable; scale note legible. OK.
- Fig. 3: both panels, labels and footnote legible. OK.
- Fig. 4: cell values now at 3 decimals — (16, 0.5)=0.947 and (16, 0.6)=0.996 match the
  manuscript exactly; no stale "0.95"/"1.00" rounding. Fixed this pass.
- Fig. 5: right-panel "Station pairs" label no longer collides with the colorbar label
  (moved to right side). Station id clusters (7840/7810/7845/7941, 1879/1890) slightly
  crowded but legible. Fixed this pass.
- Suppl. Fig. S1: bar values correct (1.000/1.000/1.000/0.000); labels crowd the top edge
  slightly — cosmetic, retained.
- Suppl. Fig. S2: curves and error bars correct; legend readable; values consistent with
  registry (0.895/0.602 at corruption 0.1/0.4 under 0° noise).
- Table 1 (M0–M7 + metadata row): content verified against §3 text.
- Table 2 (frame taxonomy): 8 frame classes; N/S and E/W support columns consistent with
  §2/§6 discussion.
- Table 3: matches rigidity CSV first-tested thresholds (0.8/1.0; 0.7/0.9; 0.6/0.7;
  0.5/0.7; 0.4/0.6; complete-graph=1.0).
- Suppl. Table S1 (16 stations), S2 (ellipsoid), S3 (registry): regenerated, values equal
  to `manuscript_values.csv`. Table numbering unified (S1/S2/S3) this pass.

No clipped labels, no stale embedded text, correct units and trial counts, no old p=0.5
threshold text, no impossible legend entries.
