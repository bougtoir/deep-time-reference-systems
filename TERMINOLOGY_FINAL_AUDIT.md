# Final terminology audit

Audit date: 2026-09-25

## Decision

The manuscript now uses **residual invariance group** for the transformations
that preserve the retained observable values. At first use, the group is
defined for an observable map \(F\) as the transformations \(Q\) satisfying
\(F(QX)=F(X)\).

The previous term **stabilizer** was potentially ambiguous because a reader
could interpret it as the pointwise stabilizer of a generic realized
configuration, which would normally be trivial. The intended object is instead
the observational-equivalence group induced by the retained information.

The word *stabilizer* remains only in the explicit sentence distinguishing the
chosen term from a pointwise stabilizer.

## Terms retained for distinct purposes

- **Gauge class / gauge freedom** remains where the text discusses geodetic
  datum defect or coordinate representations related by unobservable
  transformations.
- **Six infinitesimal Euclidean gauge modes** remains in the rigidity
  experiment because it denotes the three translational and three rotational
  null modes removed from the rigidity-matrix rank criterion.
- **Symmetry check** remains for reflection experiments used to verify
  invariance or sign reversal. It is not used as a competing name for the
  hierarchy.

## Locations reconciled

- Abstract and Introduction: `scripts/build_submission.py`
- First-use mathematical definition and theory: `scripts/build_submission.py`
  and `THEOREM_AUDIT.md`
- Figure 1 and Figure 2 labels/captions:
  `src/dtrs/plotting/figures.py`
- Table 1: `scripts/run_pipeline.py` and
  `tables/table_1_identifiability_hierarchy.csv`
- Discussion, Conclusions, and cover letter: `scripts/build_submission.py`
- Prior-art, revision, submission, and changelog documentation:
  `GEODETIC_PRIOR_ART_AUDIT.md`, `FINAL_REVISION_REPORT.md`,
  `FINAL_SUBMISSION_README.md`, `RESULT_CHANGELOG.md`, and `README.md`
- Figure 2 artifact name:
  `figure_2_residual_invariance_hierarchy.png`

## Final chain

\[
O(3)\longrightarrow O(2)\longrightarrow SO(2)\longrightarrow\{I\}.
\]

This revision changes terminology, not the protected mathematical hierarchy.
