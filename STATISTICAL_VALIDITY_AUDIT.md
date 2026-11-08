# Statistical validity audit

## 1. Units of analysis

| Quantity | Unit | n | Independence | Interval reported | Verdict |
|---|---|---|---|---|---|
| Deterministic scenario proportions (Table 3, Fig. 4, Table S5) | task item within one deterministic record | 496 items per scenario × representation (T1, T2, T3, T5 for 120 pairs; T4 for 16 sites) | items share one record and are **not** independent | none | correct: these are exhaustive descriptions of one deterministic record, not estimates; no interval is attached. Methods now say so explicitly. |
| Record-level false certainty under random loss (Fig. 5) | record (one storage convention × one replicate) | 600 per rate × representation (3 conventions × 200 replicates) | independent: fresh uniform draws per record (`run_missingness`), same draws reused across representations (paired design) | Wilson 95% per rate × representation | correct unit; item-level correlation avoided by the "≥1 false answer per record" indicator |
| Mean coverage under random loss | record mean over its 496 items | 600 | as above | normal approximation on record means (`mean_coverage_95ci_halfwidth`) | correct unit (record means, not items) |
| Ablation proportions (Fig. 6 left) | task item, aggregated over 16 deterministic scenarios | 7936 | not independent | none | descriptive only; no interval claimed |
| Calibration (Fig. 6 right) | T2 item | 24,000 per noise level (200 replicates × 120 pairs) | correlated within a replicate (one noise draw per record) | none | Brier scores are descriptive means; no interval claimed; reliability bins pool items |
| Rigidity probabilities (Table 4) | random framework | 2000 per cell | independent | Wilson 95% | frozen; correct |

## 2. The 95% upper bound "0.006"

- Source: `rec_field_mcar_r0p5_E_records_with_false_certainty_95ci_high` = 0.006361701… from
  `wilson(0, 600)` in `benchmark.summarise_missingness`.
- Closed form for zero events: \(z^2/(n+z^2)\) with \(z=1.95996\), \(n=600\) → 0.0063617. Verified
  independently (matches to machine precision). Rule of three: 3/600 = 0.005.
- Sampling unit: **records**, 600 per deletion rate; the same bound applies at each of the five rates
  (0/600 each). It is not a bound on task items.
- Defect found and fixed: the bound was printed with three decimals as 0.006, i.e. rounded **down**
  from 0.00636. An upper bound must not be rounded down. The manuscript now prints it with four
  decimals (0.0064) and gives the denominator ("0/600 records per rate").
- Interpretation of zero events: absence of observed false certainty in 600 independent records at
  a rate; it does not establish zero probability, and it is conditional on the 14-field deletion
  model and on the independence assumption audited in `ZERO_FALSE_CERTAINTY_AUDIT.md`.

## 3. Other checks

- Wilson implementation (`benchmark.wilson`): standard score interval; returns NaN for n = 0;
  reproduces the textbook value above. PASS.
- Multiple tasks per record: handled by record-level indicator for interval estimates; item-level
  proportions are never given intervals. PASS.
- Multiple comparisons: no hypothesis tests are performed; no p-values are reported. PASS.
- Brier score: mean squared difference between stated probability (1.0 for unique answers) and
  correctness over all T2 items at a noise level; values 0.0049, 0.0168, 0.0666 for 0.01, 0.03,
  0.1 rad. Observed accuracy of probabilistic states (e.g. 0.774 vs mean predicted 0.786 at
  0.1 rad) indicates slight over-confidence; reported as calibration, not tested. PASS (descriptive).
- Correct denominators in the manuscript: "proportion of 496 task items" (captions of Fig. 4,
  Table S5), "0/600 records per rate" (abstract), Wilson intervals over records (Fig. 5 caption). PASS
  after the fix above.
