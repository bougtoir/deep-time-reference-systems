# Final adversarial decision

1. Can a hostile reviewer still argue this is only datum-defect repackaging? They can argue
   it; the defense (shifted question + recoverability-conditioned hierarchy + reproducible
   audit) is real but the novelty is framing-level. Accepted risk, honestly scoped.
2. False global-rigidity claim? No — text, captions, and supplement all disclaimed global
   rigidity; only the local 3n−6 diagnostic is used.
3. Datum/frame terminology misuse? No — IERS usage followed (system vs realization; datum,
   CRS, epoch separated).
4. Unexplained number for a reproducibility reviewer? No — every reported value traces to
   `manuscript_values.csv` or a declared config constant; inventory classified all 511
   code literals (0 improper).
5. Manually typed result? None found.
6. Figure/table disagreement? The two display collisions found (Fig. 4 rounding; Fig. 5
   label overlap; supplementary table numbering) are fixed and verified.
7. Old 100-trial result still present? Only in historical changelog/audit docs outside the
   package; one orphaned stale figure removed.
8. Unsupported novelty claim? None — "novel"/"first"/"guarantee" absent or used only
   negatively/conditionally.

## Decision

B. SUBMISSION READY AFTER USER METADATA ONLY

Remaining gate is user metadata (affiliation, ORCID, funding, competing interests —
isolated in `submission_final/FINAL_USER_INPUT_REQUIRED.md`). No scientific or
reproducibility issue remains.
