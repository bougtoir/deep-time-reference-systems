# Rigidity replication audit

Audit date: 2026-09-25

## Design

| Item | Pre-revision | Final replication |
|---|---:|---:|
| Trials per \((n,p)\) cell | 100 | 2,000 |
| Point counts | 6, 8, 10, 12, 16 | unchanged |
| Edge-retention probabilities | 0.1 to 1.0 by 0.1 | unchanged |
| Local-rigidity criterion | rigidity-matrix rank \(3n-6\) | unchanged |
| Confidence interval | Wilson 95% | unchanged |

The deterministic seed strategy is unchanged. The global seed is `20260924`,
the rigidity offset is `1000`, and NumPy's generator is initialized with
`20261924`. Each trial independently samples a generic Gaussian point
configuration and independent Bernoulli edge-retention indicators. The single
seeded stream is consumed in the configured \(n\)-then-\(p\) order.

The isolated 2,000-trial-per-cell rigidity calculation took 16.56 seconds on
the canonical VM. The complete analysis pipeline, which also reran the
synthetic, uncertainty, ellipsoid, and ITRF analyses, took 43.61 seconds.

## Transition summary

The entries are the first probabilities in the tested grid with an observed
full-local-rigidity frequency at or above the stated level. They are not exact
or universal phase-transition thresholds.

| \(n\) | Old first tested \(p\), frequency >= 0.50 | New | Old first tested \(p\), frequency >= 0.95 | New |
|---:|---:|---:|---:|---:|
| 6 | 0.8 | 0.8 | 1.0 | 1.0 |
| 8 | 0.7 | 0.7 | 0.8 | 0.9 |
| 10 | 0.6 | 0.6 | 0.7 | 0.7 |
| 12 | 0.5 | 0.5 | 0.7 | 0.7 |
| 16 | 0.4 | 0.4 | 0.5 | 0.6 |

## Cells controlling changed claims

| \(n\) | \(p\) | Old frequency (95% Wilson interval) | New frequency (95% Wilson interval) |
|---:|---:|---:|---:|
| 8 | 0.8 | 0.960 (0.902–0.984) | 0.948 (0.937–0.957) |
| 8 | 0.9 | 0.970 (0.915–0.990) | 0.9995 (0.9972–0.9999) |
| 16 | 0.4 | 0.630 (0.532–0.718) | 0.608 (0.586–0.629) |
| 16 | 0.5 | 0.960 (0.902–0.984) | 0.9465 (0.9358–0.9555) |
| 16 | 0.6 | 1.000 (0.963–1.000) | 0.996 (0.992–0.998) |

The \(n=16,p=0.5\) Wilson interval includes 0.95, but the predefined summary
uses the observed frequency, not the interval endpoint. Because the observed
frequency is 0.9465, the first tested \(p\) meeting the 0.95-frequency rule is
therefore 0.6. The same distinction moves the \(n=8\) summary from 0.8 to 0.9.

## Interpretation

The increased replication narrows Monte Carlo uncertainty while preserving
the qualitative size-dependent rise in local rigidity. It does not establish
global rigidity, prove a sharp asymptotic threshold, or identify a universal
edge density. Figure 4 and Table 3 report only the configured random-framework
ensemble and tested probability grid.
