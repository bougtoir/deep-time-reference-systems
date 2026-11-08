# Baseline fairness audit

Values are from `results/manuscript_values.csv` (seeded run) and `results/record_stress.csv`.

## 1. What B already implements (competent ISO 19111 / PROJJSON-style consumer)

| Capability | B | BR | Where |
|---|---|---|---|
| Coordinate epoch | yes (`reference_system.coordinate_epoch`; velocities propagate to the query epoch) | yes | `encode.build_record`, `decode._coordinate_path` |
| Dynamic reference frame (frame + frame reference epoch) | yes (`frame`, `frame_reference_epoch`) | yes | same |
| Coordinate transformation | yes (`transformation_to_frame`, signed axis permutation + rotation) | yes | `encode.to_frame` |
| Data-quality metadata (positional accuracy) | yes (`coordinates.standard_uncertainty_m`) | yes | `build_record` |
| Provenance / integrity | yes: SHA-256 fixity of `coordinates.values`, strict rejection on mismatch | yes | `validate`, `decode_strict` |
| Validation of missing metadata | yes: never assumes defaults; missing CRS or epoch → `non_identifiable` | yes | `decode_strict` |
| Explicit uncertainty in answers | no (answers are unique or withheld) | no | by design of a strict consumer |
| Detection of contradictory information | n/a (one copy) | yes: union-of-keys reconciliation, differing values → `invalid_record`; digital chirality bit checked | `decode._usable_reference_system` |

B is not weakened: it never guesses, rejects post-export alteration, and with intact metadata recovers
every task (correct-unique 1.000, Table 3).

## 2. Can a standards-aware baseline match E without the proposed schema?

The comparison distinguishes the five levels requested:

| Level | Representation | Silent handedness flip (S4) FC | Epoch error before checksum (S13) FC | Post-export alteration (S10) | Unflagged 5 cm error (S11) FC |
|---|---|---|---|---|---|
| 1 Basic coordinates | A | 0.482 | 0.208 | FC 0.208 | 0.282 |
| 2 Complete CRS metadata | B without fixity (S13 = B with fixity, identical decode) | 0.274 | 0.415 | would be FC 0.415 | 0.137 |
| 3 CRS metadata + integrity validation | B | 0.274 | 0.415 | flagged invalid 1.000 | 0.137 |
| 4 Redundant metadata | BR | 0.274 | 0.415 | flagged invalid 1.000 | 0.137 |
| 5 Recoverability-aware | E | 0.000 | 0.000 | 0.000 (relational fallback) | 0.000 |

(Level-1 and level-2 numbers: `rec_S4_…_A_false_certainty`, `rec_S13_…_B_false_certainty`, etc.)

Argument why levels 2–4 cannot be improved by more validation alone: in S4, S11 and S13 the corrupted
record is a *valid record of a different world*: every field, copy, checksum and digital bit is
consistent with the wrong coordinates because they were derived from them before or during export.
Any validator whose inputs are only these fields therefore accepts it. ISO 19157 quality elements,
PROV-O lineage or a second checksum are further functions of the same corrupted values and add no
discriminating information. Detection needs evidence whose failure mode is independent of the
coordinates, which is what D/E add. An "enhanced standards baseline" that adds such evidence is no
longer a standards-only baseline: it is D or E with another serialization. This is stated in the
Discussion.

## 3. Information budget

| Representation | JSON bytes | Ratio to A | Extra information relative to B |
|---|---|---|---|
| A | 2391 | 1.00 | — |
| B | 3223 | 1.35 | — |
| BR | 3538 | 1.48 | redundant CRS copy, digital chirality bit (same failure mode as the values) |
| C | 5983 | 2.50 | relations and rates, no coordinates or anchors |
| D | 6796 | 2.84 | relations + independent anchors, no coordinates |
| E | 8773 | 3.67 | B + relations + anchors + uncertainty + provenance |

E carries more information than B. The benefit is separated as follows (component ablation over all
deterministic scenarios, `rec_ablation_*`, and stress scenarios):

| Component | Evidence | Effect on false certainty (FC) |
|---|---|---|
| Additional information as such | BR (more bytes than B, same failure mode) | none: BR FC = B FC in S4, S11, S13 |
| Redundancy | BR vs B under field MCAR | reduces record-level FC (B 0.015–0.057 → BR 0.000–0.018 across rates); raises coverage |
| Independent evidence (relations) | ablation `no_relations` | FC 0.000 → 0.035 |
| Independent evidence (chirality anchor) | ablation `no_chirality_anchor`; digital copy | FC 0.000 → 0.017; digital copy 0.017 |
| Validation (fixity) | B in S10 vs S13 | detects post-export alteration only |
| Explicit recoverability states | ablation `no_uncertainty` / `no_provenance`; S9 | do not change FC; convert withheld answers into group-/set-valued answers (coverage of informative answers) |
| Independence assumption itself | stress X1–X5 | when it is violated E's FC equals B's (X1, X2, X3, X5) or exceeds it (X4: 0.272 vs 0.000) |

Conclusion: E's advantage arises from independent evidence plus refusal rules, not from storage
volume or validation alone. The manuscript attributes it accordingly ("not from the coordinates";
"conditional rather than intrinsic").

## 4. Failure-model fairness (per scenario)

| Scenario | Fields corrupted | Fields retained | Checksums/hashes re-issued after corruption? | Physical anchors survive? | Detectable from record alone? | Equivalent evidence for B? |
|---|---|---|---|---|---|---|
| S0 | none | all | — | yes | — | yes |
| S1a–c | CRS block deleted | all else (BR keeps copy) | n/a | yes | yes (missing) | BR: yes (copy) |
| S2 | CRS identifier deleted | parameters | n/a | yes | parameters suffice | yes |
| S3 | coordinate epoch deleted (both copies) | velocities, rest | n/a | yes | yes (missing) | yes |
| S4 | Y negated in values/velocities; digital bit and hashes recomputed | anchors, relations | yes | yes (stipulated) | no for B/BR | no: B has no independent evidence by construction |
| S5 | axis order swapped and labelled | all | yes | yes | n/a (correctly labelled) | yes |
| S6 | one identifier duplicated | all | yes | yes | yes (collision) | yes |
| S7 / S8 | chirality anchor removed / invalid triple | rest | yes | partially | yes | B unaffected |
| S9 | CRS block + chirality anchor removed (left-handed storage) | relations, other anchors | n/a | partially | yes | BR: copy |
| S10 | values replaced by comparison-epoch values after hashes issued | hashes stale | no | yes | yes (fixity) | yes (B fixity) |
| S11 | 5 cm error at 3 sites; hashes re-issued | relations, anchors | yes | yes (stipulated) | no for B | no |
| S12 | 50% of relation edges dropped; CRS lost | rest | yes | yes | yes | BR: copy |
| S13 | as S10 but before hashes issued | relations, anchors | yes | yes (stipulated) | no for B | no |
| X1–X5 | as S4/S11/S13/S6 but also anchors, relations or identifiers | — | yes | **no** | no for any representation | yes (all equally blind) |
| MCAR | each of 14 fields deleted independently | rest | n/a | partially | yes (missing) | yes (same field list for all) |
| Block loss | whole CRS block + copy | rest | n/a | yes | yes | yes |

Unfairness found: S4, S11 and S13 give E evidence that B lacks by construction (anchors stipulated
to survive). This is now explicit in Methods (stress scenarios "break the independence assumption on
which the deterministic scenarios rest"), Results (X1–X5), Discussion and Limitations. With the
stress scenarios added, the comparison covers both the favourable and the unfavourable side of that
assumption. No change to B was needed.
