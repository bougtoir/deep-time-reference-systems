# Novelty audit (final, hostile)

Strongest criticism: "This paper adds a validator and uncertainty flags to existing CRS metadata."

## Capability matrix

Y = provides, P = partial, N = not provided (as specified in the cited standard or work; sources in
`references_verified.csv`, standards snapshots in `data/raw/standards/`).

| Capability | ISO 19111 / OGC Topic 2 | PROJJSON | ISO 19115-1 | ISO 19157-1 | W3C PROV-O | GeoSPARQL 1.1 | OAIS / ESI provenance archives (Barkstrom; Tilmes) | Uncertainty representations (UncertWeb; Heuvelink) | This record |
|---|---|---|---|---|---|---|---|---|---|
| CRS, dynamic frame, coordinate epoch, transformations | Y | Y | P | N | N | P | N | N | Y (reuses ISO 19111 semantics) |
| Lineage / provenance | N | N | Y | P | Y | N | Y | N | P (source ids, hashes) |
| Positional accuracy / data quality | P | P | P | Y | N | N | N | Y | P (σ per distance, coverage factor) |
| Integrity (checksums) | N | N | N | N | N | N | Y (fixity in OAIS) | N | Y (shared with baseline B) |
| Frame-free metric relations stored as data | N | N | N | N | N | N (topology only) | N | N | Y |
| Evidence-type label distinguishing independent physical anchors from digital copies | N | N | N | N | P (generic derivation) | N | N | N | Y |
| Machine-readable statement, per task, of what remains identifiable after loss of a metadata component (residual group / set / probability / none / invalid) | N | N | N | P (conformance result, not per task) | N | N | N | P (probabilistic values, not identifiability) | Y |
| Executable decoder that refuses to coerce ambiguity into a unique coordinate answer, cross-checking coordinates against relations and anchors | N | N | N | N | N | N | N | N | Y |

## Assessment

- What is **not** new: CRS/epoch encoding; provenance; quality metadata; checksums; the group chain
  O(3)→O(2)→SO(2)→{I}; distance-geometry reconstruction; uncertainty encodings. The manuscript says so
  (Sect. 2 and 3).
- What is new in combination: (i) per-task recoverability states computed by a decoder rather than
  declared by a producer; (ii) the evidence-type distinction between independent anchors and digital
  copies, with the demonstration that copies fail with the data; (iii) the coordinate/relation/anchor
  cross-check that turns a silent error into a set- or group-valued answer.
- Is the criticism fair? Partly. The validator and states are the contribution, and states could be
  serialized as ISO 19157 results; the paper does not claim a new standard. The non-trivial part is
  the decoder semantics (which state follows from which surviving evidence) and the benchmark that
  shows where it helps and — after the stress scenarios — where it does not.
- Exact JSON schema novelty is not claimed as a contribution.
- Residual risk: medium-high desk-rejection risk on novelty for an editor who views per-task states
  as an application of existing quality vocabularies. The stress results reduce over-claiming risk
  but also narrow the contribution to "conservative when independent evidence survives".

Verdict: the contribution is distinguishable from existing methods at the level of decoder semantics
and evidence typing; it is incremental rather than foundational, and the manuscript now says the
safety is conditional.
