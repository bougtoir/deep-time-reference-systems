# Hostile review — final pre-submission pass (Journal of Geodesy)

Reviewer stance: skeptical JoG referee actively seeking grounds for rejection.

## Major comments

M1. Novelty. A critic can argue this is datum-defect / free-network theory restated. The paper's
defense must rest on the *shift of question*: not "how to estimate coordinates under rank
deficiency" but "which relational claims survive when the realization itself is gone". The
O(3)->O(2)->SO(2)->{I} chain is mathematically elementary (each step is a stabilizer
computation); the contribution is applying it as an archival sufficiency audit with explicit
recoverability conditions (independent physical interpretation) that pure stabilizer algebra
does not capture. This is honest but means the novelty claim is *framing + schema +
audit*, not new mathematics. The manuscript does not overstate this ("a sufficiency audit for
archival observables, not a new datum-adjustment method"). Acceptable if the Abstract is not
read as claiming new theory.

M2. Geodetic significance. The reviewer may say this is information science / archival
metadata, not geodesy. The counter is the ITRF2020 demonstration, the WGS84–GRS80 sensitivity,
and the explicit datum/frame/CRS terminology discipline; roughly half the references are JoG.
Borderline but defensible; fit is real, not inflated.

M3. Fig. 4 display vs text (found in this audit). The heatmap annotated cells at 2 decimals,
displaying "0.95" at (n=16, p=0.5) and "1.00" at (0.6), visually contradicting the text's
headline that 0.9465 < 0.95 and the estimated frequency is 0.996, not 1.000. A hostile
reviewer could cite this as a figure–text inconsistency. FIXED: annotations now render 3
decimals (0.947 / 0.996).

M4. Supplementary table numbering collision (found in this audit). The supplement's ITRF2020
station table was numbered "Table 1", colliding with main-text Table 1 and breaking the S1/S2
supplementary numbering convention. FIXED: supplementary tables renumbered in document order
(S1 stations, S2 ellipsoid sensitivity, S3 value registry); main-text "Supplementary Table S1"
updated to S2.

M5. Fig. 5 axis-label collision (found in this audit). The right-panel y-label overlapped the
colorbar label. FIXED: moved to the right axis side.

## Minor comments

m1. 2000 trials/cell at p=1.0 yields Wilson lower bounds ~0.998 — adequate for the
"first tested p >= 0.95" summary but not for estimating tails near 1. The text already calls
the diagram "a seeded phase diagram, not a universal threshold". Addressed.

m2. Linear propagation 2015->2025 is acknowledged as secular-only; the manuscript explicitly
scopes it ("not a complete nonlinear station-motion model"). Addressed.

m3. Station selection is deterministic (longitude bins + uncertainty cutoff) and disclosed;
the demonstration is illustrative by design. Addressed.

m4. "Residual invariance group" is used as an observational-equivalence group and the text
explicitly disclaims the pointwise-stabilizer reading. Correct usage, verified.

m5. Physical chirality could be called circular (a chiral witness requires a chiral witness).
The manuscript's response — that the witness must be *independently physically recoverable* —
is stated, though a reviewer may still find the operational identification of such a witness
under-specified. Valid-minor; acceptable because the paper's claim is conditional
("sufficient only if its physical interpretation is independently recoverable").

m6. Supplementary Fig. S1 bar labels sit at the axes' top edge; cosmetic crowding against the
title band but no clipping or wrong values. Noted; not a correctness issue.

m7. Cover letter is consistent with the manuscript, uses single-author voice ("my", "I"),
states fit to datum/frame realization topics, contains no numerical claims and no abstract
duplication. Verified.

## Recommendation

Minor revision (as a hypothetical referee report) — the two numbering/display collisions were
the only actionable finds; both fixed in this pass. No grounds for rejection found.

## Exact rationale

Elementary mathematics + genuinely shifted question = borderline novelty that the honest
framing supports. Reproducibility is strong (registry-driven numbers, seeded determinism,
checksum-persisted raw inputs). Remaining weaknesses are scope-acknowledged, not hidden.
