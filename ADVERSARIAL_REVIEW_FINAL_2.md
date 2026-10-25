# Adversarial review — final round 2

Post-remediation hostile Journal of Geodesy review.

## Findings and dispositions

1. Novelty vs datum-defect/free-network theory — valid but bounded: the paper
   explicitly positions itself downstream of that literature; contribution is
   the recoverability-conditioned hierarchy, not a new adjustment method.
   Bounded, honestly scoped.
2. Mathematical rigor — propositions remain correct under stated generic
   assumptions; degeneracies disclosed (S1). Valid only insofar as the claims
   stay limited — text maintains the limited claims.
3. Local vs global rigidity — all results text, Table 3 caption, Fig. 4
   caption and supplement state local-rigidity-only. Resolved in prior round;
   remains resolved.
4. Physical chirality — orientation label vs physical witness distinction
   argued in Prop. 3 and abstract; stored-bit sufficiency is explicitly
   conditional. Remains resolved.
5. ITRF reflection interpretation — Fig. 5 is labelled an epoch-sensitivity
   calculation, not a reflected realization. Remains resolved.
6. Public reproducibility — public main is now the canonical source; see
   PUBLIC_REPO_SYNC_AUDIT.md and PUBLIC_CODE_FRESH_CLONE_REPRODUCTION.md.
   Resolved this round.
7. OMML equation correctness — 90 `<m:oMath>` elements; key equations
   machine-verified and PDF-rendered (WORD_OMML_AUDIT.md). Resolved.
8. Figure/table citation completeness — all 5+3 main and 2+3 supplementary
   items cited in prose, monotonic (FIGURE_TABLE_CITATION_AUDIT.md).
   Resolved.
9. Traceability consistency — result_traceability.csv updated: ellipsoid
   sensitivity S2; S1 stations and S3 registry rows added. Resolved.
10. Numerical hard-coding — 511-literal inventory, F/G classes empty;
    headline-value guard test added (tests/test_qc.py). Remains resolved.
11. Citation ecology — 24/24 references verified and cited bidirectionally;
    author–year/alphabetical style confirmed. Remains resolved.
12. Practical geodetic significance — modest; bounded in journal-fit scoring
    (3/5). No rejection ground.

## Verdict

No unresolved valid criticism of substance remains. Minor-revision-level
issues only (novelty framing, practical impact), both honestly bounded in the
text. No rejection grounds identified.
