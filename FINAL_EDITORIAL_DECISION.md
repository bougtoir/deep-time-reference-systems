# Final editorial decision

**Decision: B. READY AFTER USER METADATA ONLY — Earth Science Informatics, Methodology article.**

This decision follows the final QC pass recorded in `PRE_FINAL_QC_STATE.md` → `FINAL_QC_MATRIX.md`.
A scientific revision of the claim was required during this pass and has been implemented; the
classification refers to the revised manuscript.

## What the audit found

1. **Zero false certainty was a conditional, largely deterministic property** presented in a way that
   could be read as an empirical finding (`ZERO_FALSE_CERTAINTY_AUDIT.md`). Five minimal stress
   scenarios (X1–X5) show that when the corruption also reaches the relations, anchors or identifiers,
   E gives false certainty exactly like the baseline (0.274, 0.137, 0.177, 0.415 of items), and a
   mislabelled chirality anchor makes E wrong on 0.272 of items of correct data where B is correct.
   → Implemented: abstract, Methods, Results, Discussion, Limitations, Conclusions, cover letter and
   ESM Table S5 now state that the safety is conditional on evidence whose failure modes are
   independent of the coordinates.
2. **The baseline is fair** for what it represents (ISO 19111/PROJJSON-style strict consumer with
   fixity and repaired redundancy); no standards-only validator can detect self-consistent corruption
   (`BASELINE_FAIRNESS_AUDIT.md`). E's advantage comes from independent evidence plus refusal rules.
3. **Statistics:** the 95% upper bound for zero events was rounded down (0.006 vs 0.00636); now
   printed as 0.0064 with the record denominator (`STATISTICAL_VALIDITY_AUDIT.md`).
4. **Presentation defects fixed:** titles inside figures (ESI artwork rule), Word styling, two
   generated-but-typed values, cover-letter description of the JoG decision.
5. **Reproducibility:** public fresh clone reproduces every seeded value
   (`PUBLIC_FRESH_CLONE_REPRODUCTION.md`).

## Claims made

Per-task recoverability states, frame-free relations cross-checked against coordinates, and typed
independent anchors remove false certainty in the specified scenarios in which that evidence is not
itself corrupted, without loss when metadata are intact.

## Claims not made

Superiority with intact metadata; coverage superiority (repaired BR is better under independent
deletion); safety under arbitrary corruption; that coordinates make E safe (D is equally safe); a new
theorem; that a digital chirality bit or a benchmark anchor is real independent physical evidence.

## Remaining risks

- Editorial novelty judgement: medium-high (incremental relative to ISO 19157-style quality
  reporting; `NOVELTY_AUDIT_FINAL.md`).
- Author-designed scenarios, no real incident corpus: medium-high.
- Practical availability of independent anchors: high for impact; the paper now quantifies the
  failure when they share the error or are wrong.

## Blocking before upload

The author inputs in `FINAL_USER_INPUT_REQUIRED.md` (affiliation/address, ORCID, funding, competing
interests, publishing route).
