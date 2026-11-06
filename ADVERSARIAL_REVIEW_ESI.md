# Adversarial review (internal; not part of the journal upload)

Reviewer stance: hostile ESI referee, applied after the baseline-strengthening audit. Point-by-point
responses with manuscript locations are in `ADVERSARIAL_RESPONSE_MATRIX_ESI.csv`. Numbers are from
`results/manuscript_values.csv`.

1. **The original baseline was weakened by a bug.** BR compared only shared keys; B had no fixity.
   *Response:* fixed (union reconciliation, B/BR SHA-256 fixity, strict rejection); all results
   regenerated; changes listed in `RESULT_CHANGELOG.md`. Residual risk: low.
2. **Unequal information.** E carries anchors and relations that B lacks. *Response:* BR and D
   isolate redundancy and anchors; the digital-copy witness ablation equals no witness. The
   manuscript now states that D, without coordinates, is equally safe. Residual risk: medium.
3. **Author-chosen scenarios.** *Response:* stated as specified failure modes; intact, collision,
   block-loss-with-copy and sparse cases where E has no advantage or loses are reported. No real
   incident corpus. Residual risk: medium-high.
4. **Anchors are generated from truth and independent by stipulation.** *Response:* now explicit in
   Limitations; the axis anchor is described as a second encoding of the coordinates. Residual
   risk: high for practical impact, low for correctness.
5. **S13: coordinates that are wrong before export.** E avoids false certainty but returns 0.391 of
   items as set-valued; D recovers all. *Response:* reported in abstract and Results. Acceptable.
6. **Coverage.** Repaired BR exceeds E at every MCAR rate (0.534 vs 0.290 at 0.5). *Response:*
   abstract, Results, Conclusions. Acceptable.
7. **No comparison with PROJ/pyproj or ISO 19157 tooling.** *Response:* B emulates a
   metadata-complete strict consumer; mapping to PROV-O/ISO 19157 not implemented. Residual risk:
   medium.
8. **Single network, 16 stations.** Limitations. Residual risk: medium.
9. **Novelty of per-task states vs ISO 19157 quality elements.** Positioned in Related work.
   Residual risk: medium-high (desk rejection on novelty remains possible).
10. **Group chain as new theorem?** No; labelled as known.
11. **Timing nondeterminism.** Wall-clock values documented.

Verdict: submittable with the narrowed claims; the main risk is editorial novelty and the
stipulated independence of anchors, not computational correctness.
