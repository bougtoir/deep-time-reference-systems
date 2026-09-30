# Consistency audit

Audit date: 2026-09-25

## Cross-product checks

| Check | Result |
|---|---|
| Manuscript title matches cover letter and supplement | Pass |
| Five main figures exist, are embedded, and are cited in sequential order | Pass |
| Three main tables exist, are embedded, and are cited in sequential order | Pass |
| Two supplementary figures and one supplementary sensitivity table exist | Pass |
| Figure/table labels are English throughout | Pass |
| Abstract is 150–250 words | Pass (210 words) |
| Keyword count is four to six | Pass (six) |
| References use author–year citations and alphabetized list | Pass |
| All manuscript references appear in `references_verified.csv` | Pass |
| Main numerical values match `results/manuscript_values.csv` | Pass |
| ITRF site count matches configuration | Pass (16) |
| Reference and comparison epochs match configuration | Pass (2015.0, 2025.0) |
| Final manifest matches all packaged SHA-256 values | Pass (24 files) |
| Final archive members exactly match manifest plus manifest file | Pass |
| Submission archive passes ZIP integrity test | Pass |
| Distributed raw-data checksum verification | Pass (21 snapshots) |
| Automated tests | Pass (28 tests at audit run) |

## Terminology checks

- “Reference system” is used for a theoretical specification and “reference
  frame” for its realization.
- Geocentric axial latitude ordering is not described as geodetic latitude.
- Generic axial latitude is distinguished from geocentric, geodetic,
  astronomical, and magnetic latitude.
- Relative east/west is distinguished from absolute longitude.
- A directed axis is distinguished from an undirected axial line.
- A coordinate-handedness convention is distinguished from a physically
  recoverable chiral witness.
- Signed relative longitude is identified as a pairwise principal-branch
  relation, not a transitive total order.
- Euclidean chord distance is distinguished from surface-geodesic distance.
- Local rigidity is distinguished from global rigidity.
- Paleolongitude is described as model- and additional-constraint-dependent,
  not categorically impossible.
- Observation epoch, coordinate reference epoch, geological age, and
  reconstructed epoch are distinguished.

## Known submission metadata gaps

1. Replace `[Affiliation to be confirmed]`.
2. Add or explicitly omit an ORCID.
3. Confirm funding, competing-interest, and CRediT statements.
4. Add the final public repository release URL and archival DOI.

## Verdict

The generated scientific products, final directory, reproducibility archive,
manifest, and clean final ZIP are internally consistent. The remaining gaps
are author-controlled metadata, not analytical inconsistencies.
