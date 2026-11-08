# Adversarial review, final (internal; not part of the journal upload)

Five independent hostile reviews of the package at `PRE_FINAL_QC_STATE.md`. Each criticism is
classified as Valid-material (VM), Valid-minor (Vm), Already addressed (AA) or Invalid (INV). Valid
points were implemented in this pass; the point-by-point record is `ADVERSARIAL_RESPONSE_MATRIX.csv`.
The JoG-era review is preserved as `JOG_ADVERSARIAL_REVIEW_FINAL.md`.

## Reviewer 1 — ESI editor (novelty, fit, significance, desk risk)

- R1.1 (VM) "Zero false certainty reads as a headline discovery, but it is built into the decoder."
  → Stress scenarios X1–X5 added; abstract, Results, Discussion and Conclusions now say the safety is
  conditional and a consequence of refusal rules plus surviving evidence.
- R1.2 (AA) "Fit: is this informatics or geodesy?" → record model, validator, decoder and benchmark
  lead; geometry is foundation only.
- R1.3 (Vm) "Practical significance: where do independent anchors come from?" → Limitations state
  anchors are computed from truth and independence is stipulated; X4 shows the cost of a wrong anchor.
- R1.4 (VM, residual) "Incremental relative to ISO 19157." → `NOVELTY_AUDIT_FINAL.md`; claim limited
  to decoder semantics and evidence typing. Desk-rejection risk remains medium-high.

## Reviewer 2 — geospatial standards specialist

- R2.1 (AA) "B is a strawman." → B has epoch, dynamic frame, transformations, accuracy, fixity,
  strict missing-metadata handling; BR reconciles copies over the union of keys
  (`BASELINE_FAIRNESS_AUDIT.md`).
- R2.2 (Vm) "An ISO 19157 + PROV-O baseline would do the same." → Argued and documented: any
  validator whose inputs are functions of the corrupted values accepts a self-consistent corrupted
  record; adding independent evidence makes it D/E. Mapping to ISO 19157/PROV-O stated as not
  implemented.
- R2.3 (AA) "PROJJSON already carries coordinate epochs." → cited; B emulates it.
- R2.4 (INV) "Checksums would catch S13." → a checksum issued after the error verifies; S10 vs S13
  demonstrates this.

## Reviewer 3 — statistician

- R3.1 (VM) "The 95% upper bound 0.006 is rounded down from 0.00636." → now printed as 0.0064 with
  "0/600 records per rate" (`STATISTICAL_VALIDITY_AUDIT.md`).
- R3.2 (Vm) "Task items within a record are correlated; are they treated as Bernoulli trials?" → No
  interval is attached to item proportions; Methods now state that deterministic-scenario proportions
  are exhaustive descriptions of one record and that the random-loss unit is the record.
- R3.3 (AA) "Unit of the Wilson interval." → records, 600 per rate, independent draws.
- R3.4 (Vm) "Brier scores over correlated items without intervals." → descriptive only; stated in the
  audit; no inferential claim made.

## Reviewer 4 — computational geometer

- R4.1 (AA) "Group chain is classical." → labelled as known (Sect. 3).
- R4.2 (Vm) "The axis anchor (geocentric latitudes) is a re-encoding of coordinates." → stated in
  Limitations; X1/X2/X5 show the consequence when it shares the error.
- R4.3 (AA) "Rigidity and reflection results depend on generic configurations." → stated in
  Limitations and ESM S1.
- R4.4 (Vm) "A wrong chirality anchor will reflect a correct reconstruction." → confirmed (X4: E and D
  false certainty 0.272 where B has 0.000) and reported in Results, Discussion and abstract.

## Reviewer 5 — reproducibility auditor

- R5.1 (Vm) "Two configuration values are typed into prose/figure titles." → calibration noise levels
  and Fig. 3 epoch label now generated (`HARDCODE_AUDIT_FINAL.md`).
- R5.2 (Vm) "Figures contain titles, contrary to ESI artwork instructions." → figure-level titles
  removed from Figs. 1–3, 6 and S1–S4; panel labels retained.
- R5.3 (Vm) "Word styling: 11-pt body, coloured Arial headings, captions not 10 pt." → body 12-pt Times
  New Roman, black headings, 10-pt captions.
- R5.4 (AA) "Public clone reproduces?" → fresh-clone run documented in
  `PUBLIC_FRESH_CLONE_REPRODUCTION.md` (rerun after this pass).
- R5.5 (Vm) "Cover letter mis-states the JoG reason as scope only." → now quotes the editorial reason
  (insufficient methodological or topical innovation for that journal).
- R5.6 (AA) "Private snapshots in the public mirror." → excluded via master `EXCLUDE_MAP` (verified
  after merge of #774); remain in public history from earlier syncs.

## Overall

No criticism invalidates the computations. Two material points (R1.1/R4.4 conditional safety; R3.1
bound rounding) required manuscript revision, which was implemented. The scientific claim is narrower
than at the start of this pass.
