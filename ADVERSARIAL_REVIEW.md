# Role-based adversarial review

Audit date: 2026-09-24

This is an internal role-based review, not a claim of external independent peer
review. Each perspective was applied separately and concrete findings were
implemented before this verdict.

## Priority register

### Highest priority — required before submission

| Domain | Risk | Fatality | Improvement | Feasibility | Required action |
|---|---|---:|---:|---:|---|
| Manuscript | Author affiliation and ORCID are unresolved | desk-reject/administrative return | high | immediate | Replace placeholders and verify title-page metadata |
| Reproducibility | Public release has no immutable DOI | major revision risk | high | immediate after release | Create a versioned archive and insert its DOI |
| Claims | Human declarations have not been confirmed | submission-integrity risk | high | immediate | Confirm funding, interests, contribution, and AI wording |

### High priority — implemented in this review

| Domain | Risk | Fatality | Improvement | Feasibility | Action taken |
|---|---|---:|---:|---:|---|
| Manuscript | Central result read as intuition rather than a formal result | major revision | high | feasible with current work | Added four propositions and proof sketches |
| Statistical design | Monte Carlo proportions lacked finite-run uncertainty | reviewer concern | medium | feasible with current data | Added 95% Wilson intervals and error bars |
| Claims | Modern ITRF result could be mistaken for geological validation | major revision | high | feasible | Bounded the demonstration explicitly |
| Reproducibility | Configurable epochs were exposed through fixed labels | major revision | high | completed | Replaced fixed-year fields and added tests |

### Medium priority — acceptable limitation if stated

| Domain | Risk | Fatality | Improvement | Feasibility | Disposition |
|---|---|---:|---:|---:|---|
| Statistical design | Complete distances avoid sparse-network nonuniqueness | normal review request | medium | additional analysis | State limitation and global-rigidity requirement |
| Figure design | Frame taxonomy is qualitative | normal review request | medium | additional empirical study | Retain as conceptual comparison |
| Reproducibility | Linear ITRF propagation omits nonlinear station motion | normal review request | medium | new modeling/data | State scope and do not infer geophysics |

### Optional

- Add a geological plate-circuit case study with full covariance.
- Add sparse distance-graph completion and outlier experiments.
- Provide a formal machine-readable schema implementation beyond the tabular
  event definition.

## Five-domain review

1. **Manuscript:** novelty is bounded to the integrated sufficiency hierarchy;
   four propositions now carry the central logic; conclusions do not exceed the
   rigid-model results.
2. **Statistical design:** the analysis unit is a simulated directional
   classification trial conditional on a fixed point pair and model.
   Monte Carlo intervals quantify only finite-run uncertainty; no population or
   geophysical inference is claimed. There are no null-hypothesis tests or
   multiple-comparison claims.
3. **Figures and tables:** each display supports a distinct claim; the frame
   taxonomy is placed on a landscape page; no display duplicates a primary
   result solely for decoration.
4. **Reproducibility:** public raw data are persisted with version, URL,
   retrieval time, byte count, SHA-256, and usage notes; dependencies and seeds
   are pinned; generated claims are traced to code and configuration.
5. **Claim strength:** synthetic, modern realized-network, and geological
   statements are separated. Paleolongitude and future survivability are
   model-dependent questions, not conclusions established by the ITRF example.

## 1. Reference-frame geodesist

**Challenge:** A spin axis alone does not define a complete terrestrial frame,
and a coordinate reference system must not be conflated with its realization.

**Action implemented:** The event schema separates origin/directed axis,
handedness, and meridian anchor. The manuscript follows IERS
system-versus-frame terminology and explicitly states that absolute longitude
still requires a meridian anchor.

**Residual concern:** Long-term scale preservation and nonrigid deformation
would require extensions beyond the rigid hierarchy.

## 2. Earth-rotation specialist

**Challenge:** “North” cannot be tied to an unspecified timeless axis; polar
motion, precession-nutation, length-of-day variation, and true polar wander
make axis definition and epoch material.

**Action implemented:** The axis is directed and time-indexed, and the frame
taxonomy lists polar motion and true polar wander as failure modes. Observation
and reference epochs are distinct fields. The ITRF demonstration is explicitly
limited to a secular ten-year propagation.

**Residual concern:** A future extension should specify which instantaneous,
mean, or angular-momentum axis is archived for each application.

## 3. Geodetic mathematician

**Challenge:** Reflection-permitting and proper-only errors must be computed
from the same unaligned realization; otherwise mirror ambiguity can be erased
by preprocessing. Degenerate directional cases must not receive arbitrary
signs.

**Action implemented:** Independent Procrustes fits now start from the same
classical-MDS output. Regression tests expose the proper-only mirror error.
Pole and projected-antipode east/west relations return undefined. The
manuscript distinguishes identifiability from numerical conditioning.

**Residual concern:** Formal theorem statements for sparse globally rigid
graphs are outside the current complete-distance analysis.

## 4. Paleomagnetist and plate-reconstruction scientist

**Challenge:** The paper must not claim that paleolongitude is simply
impossible, nor imply that a modern ITRF experiment validates geological
frames.

**Action implemented:** Paleolongitude is described as model- and
additional-constraint-dependent. Paleomagnetic, hotspot, mantle, and plate
frames are compared by assumptions and failure modes. The ITRF example is
restricted to symmetry and epoch sensitivity.

**Residual concern:** A future geological case study should propagate full
plate-circuit and anchor covariance, including entity-identity alternatives.

## 5. Computational geometer

**Challenge:** Complete distance matrices hide sparse-graph flexibility and
can be numerically ill-conditioned near degeneracy. A binary anchor-present
flag is insufficient.

**Action implemented:** The discussion now separates complete-matrix
identifiability from sparse global rigidity and requires uncertainty/quality
metadata for oriented simplices and anchors. Seeded tests cover proper and
improper transformations and degeneracies.

**Residual concern:** No graph-completion or robust outlier estimator is
implemented in this version.

## 6. Skeptical Journal of Geodesy editor

**Challenge:** The manuscript could appear speculative, overstate novelty, or
fall outside geodesy if framed around distant-future scenarios.

**Action implemented:** The title and abstract foreground reference frames,
identifiability, orientation, epoch, and ITRF2020. Deep time appears only as a
stress condition. `NOVELTY_AUDIT.md` identifies established components and
bounds the contribution to their integrated sufficiency hierarchy and
validation.

**Residual concern:** The author should further evaluate whether the concise
manuscript needs an additional applied archival example before submission.

## Software review findings implemented

Automated PR review identified and the code now corrects:

1. reflection-aligned data reused for proper-only RMSE;
2. fewer ITRF stations than configured when longitude bins were empty;
3. output labels hard-coded to 2025 despite configurable epochs;
4. manuscript-value extraction failing for nondefault uncertainty grids; and
5. antipodal points receiving the same east/west sign in both directions.

## Editorial verdict

**Technically submission-ready after author metadata confirmation.** The
scientific claims are appropriately bounded, the central symmetry result is
reproducible, and the real-data example is relevant to reference-frame
practice. The main likely reviewer request is expansion to incomplete networks
or a geological case study; this is a defensible future-work item rather than
a validity defect in the present theorem and experiments.
