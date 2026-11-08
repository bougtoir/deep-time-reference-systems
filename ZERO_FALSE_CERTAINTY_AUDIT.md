# Zero-false-certainty audit

Claim under audit: "E produces zero false-certainty answers in the tested scenarios."

## 1. Classification of the claim

| Possibility | Verdict | Evidence |
|---|---|---|
| A. Empirical finding | **No**, not in the sense of an unexpected discovery | the scenarios are deterministic; no sampling of real incidents |
| B. Deterministic consequence of refusal rules | **Yes (partly)** | `decode_recoverability`: coordinate answers for direction tasks are used only if the coordinates agree with the chirality and axis anchors (`coordinate_orientation_ok`); distance answers become `set_valued` when coordinates and relations disagree by more than `k·σ`; hash mismatch disables the coordinate path; duplicate identifiers → `set_valued`; invalid witnesses are flagged and ignored |
| C. Artifact of the selected scenarios | **Yes (partly)** | in every main scenario the corruption leaves at least one independent evidence channel intact (S4, S11, S13: anchors and relations computed from the true configuration) |
| D. Consequence of additional independent information | **Yes (partly)** | ablation: removing relations raises FC to 0.035, removing the chirality anchor to 0.017; a digital-copy witness equals no witness |
| E. Combination | **Verdict: E = B + C + D** | conservative behaviour follows from the refusal rules applied to evidence that the scenario stipulates to be uncorrupted |

The manuscript previously could be read as presenting zero false certainty as an empirical property.
It now states (Results, "Corrupted independent evidence"): "The absence of false certainty in the
deterministic scenarios is therefore a consequence of the decoder's refusal rules together with
evidence that the corruption did not reach, not an empirical property of the record." The abstract
says "This safety is conditional".

## 2. Minimal stress tests (new; `benchmark.STRESS_SCENARIOS`, `results/record_stress.csv`)

Every hash, checksum and declared-recoverability block is re-issued after the corruption, i.e. the
corruption happened upstream of export. Each value is the proportion of 496 task items.

| Requested condition | Scenario | B FC | BR FC | D FC | E FC | E correct unique |
|---|---|---|---|---|---|---|
| Independent anchors corrupted / physical chirality incorrectly labelled together with a handedness flip | X1 handedness flip also reverses chirality anchor | 0.274 | 0.274 | 0.272 | 0.274 | 0.726 |
| Multiple independent sources agree incorrectly; frame metadata and relational constraints jointly corrupted | X2 coordinates and relations share a 5 cm error | 0.137 | 0.137 | 0.137 | 0.137 | 0.863 |
| Entity identifiers incorrectly but consistently assigned | X3 two identifiers swapped in every field | 0.177 | 0.177 | 0.177 | 0.177 | 0.823 |
| Physical chirality incorrectly labelled (data correct) | X4 chirality anchor mislabelled | 0.000 | 0.000 | 0.272 | 0.272 | 0.728 |
| Epoch internally consistent but historically wrong | X5 all fields at wrong epoch, labels consistent | 0.415 | 0.415 | 0.415 | 0.415 | 0.585 |
| Provenance hashes recomputed after corruption | all of X1–X5 (and S4, S11, S13) | — | — | — | — | — |

These scenarios are the smallest modifications of existing ones (S4, S11, S6, S13) that let the error
reach the evidence; none requires an unrealistic mechanism (a reversed handedness convention in the
instrument pipeline, an error in the station position used to compute everything, a label swap in a
station table, a wrong epoch tag at the source).

Tests: `test_hybrid_is_not_protected_when_corruption_reaches_evidence` (X1, X2, X3, X5: E FC > 0),
`test_mislabelled_anchor_induces_false_certainty_in_correct_data` (X4: B FC = 0, E FC > 0).

## 3. When E can and cannot guarantee conservative behaviour

E withholds a unique answer (returns set-valued, group-valued, probabilistic, non-identifiable or
invalid) **if and only if** the record contains, for that task, at least one evidence channel that
(i) survived the corruption, (ii) is used by the decoder for that task and (iii) disagrees with the
corrupted channel beyond the stated tolerance (`k·σ` for distances; exact sign agreement for
chirality; 1e-6 rad for axis latitudes). Specifically:

- **Guaranteed conservative:** silent reflection of the coordinates when an independent chirality or
  axis anchor survives; coordinate errors > `k·σ` when a relation for the pair survives; altered
  values with stale hashes; duplicate identifiers; invalid witnesses (flagged, then ignored).
- **Not guaranteed:** any error common to coordinates and the evidence meant to check them (X1, X2,
  X3, X5); errors smaller than `k·σ`; identity errors other than collisions; tasks for which no
  independent channel exists (e.g. T4 without a meridian anchor gives group-valued, not wrong,
  answers — conservative but uninformative).
- **Can be worse than B:** a wrong independent anchor overrides correct coordinates (X4). The decoder
  trusts an anchor labelled `independent_physical` over the coordinates when they disagree; it has no
  way to decide which channel is wrong. A two-of-three vote would require a third independent channel.

These conditions are now stated in Results, Discussion and Limitations; the Limitations section also states (author addition) that anchor validity cannot be established from the archived record alone, that absence of detected inconsistency is not evidence of correctness, and that conditions for anchor-fault detection and localization (cross-anchor checks, leave-one-anchor-out reconstruction, fault-aware inference) are future work.
