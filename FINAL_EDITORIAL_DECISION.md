# Final editorial decision

**Decision: READY AFTER USER METADATA ONLY — Earth Science Informatics, Methodology article.**

Basis (after the independent baseline audit; values from `results/manuscript_values.csv`): against a
baseline with complete metadata, a coordinate fixity checksum and repaired redundancy, the
recoverability-aware record (E, and its coordinate-free profile D) gave no false certainty in any
specified scenario. The baseline gave false certainty under a silent handedness flip (0.274 of items),
an epoch error committed before the checksum was issued (0.415) and an unflagged coordinate error
(0.137). Both recovered every task when metadata were intact.

Claims that are **not** made: superiority with intact metadata; coverage superiority under
independent deletion (repaired BR is better at every rate); that coordinates are what makes E
safe (D is equally safe); a new theorem (the O(3)→O(2)→SO(2)→{I} chain is known); that a digital
chirality bit or a benchmark anchor is real independent physical evidence.

Changes relative to the #771 "GO": the #771 baseline had two defects, which are now fixed
(`NOVELTY_GATE_ESI.md`, `RESULT_CHANGELOG.md`). The claim is narrower; the novelty gate is still met.

Remaining risks: editorial novelty judgement (medium-high), author-designed scenarios
(medium-high), anchors independent only by assumption (high for practical impact), no real incident
corpus (medium).

Blocking items before upload: the five author inputs in `FINAL_USER_INPUT_REQUIRED.md`.
Public reproducibility: `PUBLIC_FRESH_CLONE_REPRODUCTION.md`.
