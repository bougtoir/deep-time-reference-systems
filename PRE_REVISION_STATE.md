# Pre-revision state

## Checkpoint

- Repository commit: `50417f8c` (`Normalize submission manifest line endings`)
- Annotated tag: `dtrs-pre-final-revision`
- Branch: `devin/1790229434-deep-time-spatial-relations`
- Project files excluding virtual-environment, pytest-cache, and bytecode files: 93
- Full pre-revision SHA-256 inventory: 93 entries; manifest digest
  `58d5b40b923862eb94a9aeac70243e0c8a54d1059113821e234ab15209f6bdf8`

## Canonical products

- Manuscript source: `manuscript/manuscript.docx`
  (`8227fcff5f1316a42ef3c36789d86fd9322041b52f73d33cdb45acf9bb4ec5f3`)
- Manuscript PDF: `manuscript/manuscript.pdf`
  (`4c001348b83eee72bc2bffb3637776e1ffedce0ab7cc60b0ad8fc5eb6b16e417`)
- Submission archive: `submission/journal_of_geodesy_submission.zip`
  (`bc3d52e10240a1d93f0c2cf1409ffe65683d300244c8497ffd14fbb0df917856`)
- Reproducibility archive: `submission/dtrs_reproducibility.zip`
  (`6e288bbe314e06937a631bb445ee823c85bb44e5c638f3b3f07db1cd3dd42d92`)
- Canonical title: “Reference-frame-robust encoding of time-indexed spatial
  relations: identifiability, orientation, and epoch”

## File inventory by function

- Analysis implementation: `src/dtrs/`, `scripts/run_pipeline.py`,
  `configs/default.yml`
- Submission builder: `scripts/build_submission.py`
- Tests: five test modules, 19 passing tests
- Persistent data and provenance: `data/`, `DATA_PROVENANCE.md`
- Generated analytical outputs: `results/`, `tables/`, `figures/`
- Manuscript products: `manuscript/`, `supplement/`
- Journal upload products: `submission/`
- Traceability and reference registries: `result_traceability.csv`,
  `references_verified.csv`
- Internal audits and decisions: `INTEGRITY_AUDIT.md`,
  `CONSISTENCY_AUDIT.md`, `NOVELTY_AUDIT.md`,
  `ADVERSARIAL_REVIEW.md`, `DECISIONS.md`

## Validated results protected from unjustified change

- Selected ITRF2020 SLR sites: 16
- Reference and comparison epochs: 2015.0 and 2025.0
- Maximum pairwise distance change: 0.6906252605840564 m
- Median pairwise distance change: 0.09072410129010677 m
- Reflection-permitting synthetic reconstruction RMSE:
  2.9701702222673244e-09 m
- Proper-only synthetic reconstruction RMSE: 6136173.251345326 m
- ITRF reconstruction RMSE: 3.6132759390917642e-09 m
- Proper-rotation north/south and east/west accuracy: 1.0 and 1.0
- Axial-reflection north/south and east/west accuracy: 1.0 and 0.0

Any change to these values requires an entry in `RESULT_CHANGELOG.md` with the
old value, new value, code cause, and scientific justification.

## Known deficiencies requiring the final revision

1. The directed-axis hierarchy incorrectly reports an `SO(2)` residual where
   an axis-preserving reflection branch remains; the centered residual
   invariance group is
   conceptually `O(2)` until a physically recoverable chiral witness is added.
2. The stored handedness bit is not distinguished from a physically
   recoverable chiral anchor.
3. Axial north/south, signed wrapped longitude, branch-cut behavior, and chord
   versus surface-geodesic distance need exact definitions.
4. The novelty framing does not adequately connect the problem to datum
   defect, free-network, gauge, minimum-constraint, Helmert, and ITRF
   alignment literature.
5. The existing Monte Carlo corruption curve is primarily a validation result;
   at least one non-tautological sparse/noisy identifiability analysis is
   needed.
6. The ITRF demonstration needs a bounded datum/gauge interpretation without
   suggesting that a reflected network is a realistic ITRF realization.
7. Direct reviewer reproduction should be reduced to one documented command.
8. Author affiliation, ORCID choice, final declarations, public release URL,
   and archival DOI remain human-controlled metadata.

## Change-control rule

Raw data, the official ITRF2020 snapshot, provenance records, validated
analyses, and the products listed above must not be overwritten or replaced
without a scientific reason recorded in the audit trail.
