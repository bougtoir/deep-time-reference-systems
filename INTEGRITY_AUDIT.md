# Integrity audit

Audit date: 2026-09-25

## Data and provenance

- **Pass:** The real-data demonstration uses the persisted official ITRF2020
  SLR product, not invented or manually transcribed station data.
- **Pass:** Source URL, version, retrieval time, byte count, SHA-256, usage
  condition, completeness, and repository-distribution status are recorded in
  `data/data_acquisition_log.csv`.
- **Pass:** `scripts/verify_raw_data.py` verifies every distributed raw input
  and every locally available non-distributed snapshot.
- **Pass:** Synthetic points are explicitly labeled synthetic and are generated
  from a fixed configuration and seed.
- **Pass:** Journal web pages are retained locally for verification but are not
  redistributed without a clear license.

## Results and reporting

- **Pass:** Manuscript numbers are read from
  `results/manuscript_values.csv`; the document builder does not contain
  hard-coded calculated estimates.
- **Pass:** `result_traceability.csv` links each principal claim to source
  data, source field, generating script, configuration, and display product.
- **Pass:** The corrected proper-only Procrustes result is computed
  independently from the unaligned MDS configuration; it is not recomputed
  from a reflection-aligned result.
- **Pass:** Pole and antipodal longitude relations are reported as undefined
  rather than forced into an east/west class.
- **Pass:** Exact and near-antipodal states, branch wrapping, same-meridian
  ties, and axial degeneracy are represented explicitly.
- **Pass:** The residual hierarchy is reported as
  \(O(3)\rightarrow O(2)\rightarrow SO(2)\rightarrow\{I\}\) under explicit
  origin, scale, directed-axis, physical-chirality, and meridian assumptions.
- **Pass:** A stored orientation label is not treated as a physical chiral
  witness unless its interpretation is independently recoverable.
- **Pass:** Rigidity-matrix rank is described as local rigidity only and is not
  used to claim global uniqueness.
- **Pass:** The theoretical metric is Euclidean chord distance, not a surface
  geodesic.
- **Pass:** The ITRF example is described as a modern symmetry and
  epoch-sensitivity demonstration, not evidence for geological propagation.

## Citations and novelty

- **Pass:** Every manuscript source is present in
  `references_verified.csv`.
- **Pass:** DOI metadata were checked through Crossref and official
  non-DOI sources through the responsible organization.
- **Pass:** Established distance-geometry, reference-frame, Kabsch-alignment,
  graph-rigidity, and plate-frame results are attributed and not claimed as
  new.
- **Pass:** The novelty statement is limited to the integrated
  minimal-sufficiency hierarchy and its reproducible demonstration.

## Authorship and disclosure

- **Conditional pass:** The named human author will complete and confirm
  affiliation, contributions, funding, competing interests, and the
  generative-AI disclosure locally.
- **Open item:** Affiliation and ORCID remain explicit placeholders. The
  package must not be uploaded to the journal until these are replaced.

## Verdict

No fabricated empirical data, unverifiable calculated value, or hidden
provenance substitution was identified. All distributed raw snapshots pass
size and SHA-256 verification, including the added graph-rigidity metadata
records. Technical integrity passes; final submission remains conditional
only on human author metadata and declaration confirmation.
