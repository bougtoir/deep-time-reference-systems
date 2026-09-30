# Data provenance

## ITRF2020 demonstration

- Provider: Institut national de l'information géographique et forestière,
  ITRF product center.
- Product: ITRF2020 SLR station positions and velocities.
- Source:
  https://itrf.ign.fr/ftp/pub/itrf/itrf2020/ITRF2020_SLR.SSC.txt
- Reference epoch: 2015.0.
- Analysis comparison epoch: 2025.0.
- Local raw snapshot:
  `data/raw/itrf2020/ITRF2020_SLR.SSC.txt`.
- Integrity: SHA-256 and byte count are in
  `data/data_acquisition_log.csv`.
- Processing: the parser joins position and velocity records by DOMES number,
  filters maximum coordinate standard uncertainty at 0.02 m, chooses
  longitude-distributed representatives, then supplements from remaining
  eligible sites to the requested total.
- Limitations: linear velocity propagation is a transparent epoch-sensitivity
  illustration, not a full station-discontinuity or nonlinear-motion model.

## Synthetic data

- Generator: `src/dtrs/simulations/benchmark.py`.
- Seed: `20260924`.
- Geometry: 24 points sampled on a WGS84-shaped ellipsoid away from polar
  singularities.
- Transformations: proper rotations and determinant-negative reflections.
- Uncertainty: directed-axis perturbation and handedness corruption.
- Configuration: `configs/default.yml`.

## Literature and policy snapshots

Crossref work records for all 22 DOI-bearing references and the official IERS
Conventions (2010) Technical Note 36 PDF were saved locally without
overwriting earlier source files. ISO 19111:2019 was checked against the
official ISO catalogue. Verification outcomes are in
`references_verified.csv`.

The official Journal of Geodesy aims-and-scope and submission-guidelines pages
and the Springer Nature AI guidance were also saved locally with checksums.
Web-page and official-PDF snapshots are not distributed in the public
repository where redistribution rights are not granted. Their URLs, access
times, sizes, hashes, completeness, and distribution status remain in
`data/data_acquisition_log.csv`.

## Reproduction boundary

The distributed ITRF file plus repository code are sufficient to reproduce all
reported numerical results. Internet access is not required by `make all`.
