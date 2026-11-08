# Novelty gate for Earth Science Informatics (pre-experiment, 2026-11-06)

Question: after the JoG desk rejection ("does not add sufficient methodological or topical
innovation"), is there an Earth-science-informatics contribution that is not (i) the rejected
geodetic identifiability argument re-titled, (ii) a restatement of ISO/OGC metadata, or
(iii) relabelled mathematics?

All sources below were verified against Crossref metadata (`data/raw/literature_esi/`) or the
official standards page (`data/raw/standards/`), accessed 2026-11-06.

## Comparison matrix

Columns: C1 coordinates + CRS + epoch; C2 transformation provenance; C3 metric relations stored
as data; C4 per-relation statement of what is still recoverable after metadata loss (residual
invariance group / recoverability state); C5 separation of independent physical anchors from
storage redundancy; C6 uncertainty attached to relations; C7 executable validator/decoder that
refuses to emit single coordinates when the state is ambiguous. Y = provides, P = partial, N = no.

| Source | Class | C1 | C2 | C3 | C4 | C5 | C6 | C7 |
|---|---|---|---|---|---|---|---|---|
| ISO 19111:2019 / OGC 18-005r5 (referencing by coordinates; dynamic CRS, coordinate epoch, frame reference epoch, point-motion operations) | direct precedent (C1–C2) | Y | Y | N | N | N | P (operation accuracy) | N |
| PROJJSON (PROJ 9 specification; datum_epoch, CoordinateMetadata) | direct precedent, implementation | Y | Y | N | N | N | P | N |
| ISO 19115-1:2014 (metadata) | partial precedent | P | P (lineage) | N | N | N | P | N |
| ISO 19157-1:2023 (data quality) | partial precedent | N | N | N | N | N | Y (positional accuracy) | P (conformance) |
| ISO 19108:2002 (temporal schema) / W3C–OGC OWL-Time | enabling | N | N | N | N | N | N | N |
| W3C PROV-O (2013) | enabling (provenance) | N | Y (generic) | N | N | N | N | N |
| Barkstrom 2010 ESI; Tilmes et al. 2010 ESI (Earth-science provenance) | partial precedent (C2) | N | Y | N | N | N | N | P |
| OGC GeoSPARQL 1.1 (Car and Homburg 2022) | partial precedent (C3, topological only) | Y | N | P | N | N | N | N |
| Egenhofer and Franzosa 1991; Cohn and Renz 2008; Galton 2009 ESI (qualitative/topological relations) | partial precedent (C3) | N | N | P | P (invariance of topology) | N | N | N |
| Freksa 1992 (orientation calculus) | analogy; presupposes a shared handedness | N | N | P | N | N | N | N |
| Hogan et al. 2021; Janowicz et al. 2022 KnowWhereGraph (knowledge graphs) | enabling | P | P | P | N | N | N | N |
| Heuvelink et al. 1989; Bastin et al. 2013 UncertWeb (uncertainty propagation / encoding) | partial precedent (C6) | N | N | N | N | N | Y | N |
| Nativi et al. 2008 ESI; Shippert and Gaustad 2016 ESI; Fugazza et al. 2021 ESI; Lakani et al. 2026 ESI (data models / metadata / semantic interoperability) | partial precedent (interchange framing) | P | P | N | N | N | N | N |
| Wilkinson et al. 2016 (FAIR); Klump and Huber 2017 (persistent identifiers); CCSDS 650.0-M-3 OAIS (2024) | enabling (preservation framing) | N | P | N | N | N | N | N |
| Müller et al. 2018 GPlates; Torsvik et al. (palaeomagnetic frames) | analogy / domain (frame-dependent reconstructions) | Y | Y | N | N | N | P | N |
| Kotsakis 2012/2013; Chatzinikos and Dermanis 2017 (datum defect, gauge) | enabling method (invariance) | Y | N | N | P (datum defect) | N | Y | N |
| Asimow and Roth 1978/1979; Liberti et al. 2014; Dokmanić et al. 2015 (rigidity, distance geometry) | enabling method | N | N | Y | P (congruence class) | N | N | N |

## What survives

1. **Not new (cite as foundations):** distance-geometry congruence modulo O(3), datum defect /
   gauge freedom, the chain O(3)→O(2)→SO(2)→{I}, rigidity thresholds. These are not claimed as
   theorems.
2. **Not new (cite as direct precedent):** encoding CRS, epoch and transformations (ISO 19111,
   PROJJSON), lineage (ISO 19115, PROV-O), accuracy (ISO 19157), topological relations (GeoSPARQL).
3. **Candidate contribution (no precedent found for C4 + C5 + C7 together):** a versioned,
   machine-readable record for a time-indexed spatial relation that (a) stores the relation
   alongside, not instead of, ISO 19111-style referencing; (b) declares, per task, the residual
   invariance group / recoverability state that survives loss of each metadata component;
   (c) distinguishes physically independent orientation evidence from redundant copies of the same
   digital convention; and (d) is executed by a validator/decoder that returns
   unique / unique-up-to-group / set-valued / probabilistic / non-identifiable / invalid rather
   than coercing to coordinates.

## Gate rule (fixed before experiments)

GO only if the benchmark (Phase 3–4) shows, against the strong baseline B (coordinates + complete
CRS/frame/epoch metadata), a reduction of false-certainty under at least the specified loss modes,
with no loss of correct-unique recovery when metadata are intact, and an ablation showing that the
gain requires C4/C5 fields rather than storage redundancy. If B is equally safe under every loss
mode, issue SCIENTIFIC NO-GO and recommend a software/data-descriptor pivot.

Expected limitation recorded in advance: under intact metadata B fully recovers every task;
the claim is restricted to robustness and honest ambiguity under specified metadata loss.

Pre-experiment verdict: **CONDITIONAL GO** (to be reassessed in `NOVELTY_GATE_ESI.md` §Reassessment).

## Reassessment after the benchmark (Phase 5)

Source: `results/record_scenarios.csv`, `record_missingness.csv`, `record_ablation.csv`,
`record_calibration.csv`, `record_cost.csv` (all generated by `make analysis`; values registered
in `results/manuscript_values.csv` with `source = record_benchmark`).

- **Intact metadata:** baseline B (coordinates + complete CRS/frame/epoch) recovers every task
  (correct-unique 1.000). So does E. There is no gain over B when metadata are intact; this is
  reported as such.
- **Silent common-mode corruption** (left-handed export with metadata unchanged): B and the
  storage-redundant BR both give false certainty on 0.274 of items; E gives 0 and recovers all
  items, because its chirality witness is independent physical evidence. When the same witness is
  a digital copy, E's ablation false-certainty rises from 0 to 0.0183 (equal to removing the
  witness). Storage redundancy does not substitute for independent evidence.
- **Epoch-mislabelled coordinates** (stale provenance): B false certainty 0.415; E 0 (hash
  mismatch, relational fallback). **Unflagged coordinate error** (0.05 m on three sites): B 0.137;
  E 0 (0.125 set-valued, honest).
- **CRS block deleted:** B becomes non-identifiable (coverage 0); BR recovers via its copy; E and D
  recover all items from the relational path. Under correlated whole-block loss E keeps coverage
  1.000 for all loss rates, B/BR fall to 0.513 at rate 0.5.
- **Independent field deletion (MCAR):** E has no record with false certainty in 600 records per
  cell (95% upper bound 0.006); B and BR have 0.015–0.057 (missing transformation parameters are
  undetectable). BR exceeds E in coverage at rates ≥0.2 (e.g. 0.508 vs 0.290 at 0.5): redundancy
  helps coverage under independent deletion; E's advantage is safety, not coverage.
- **Negative results kept:** entity-identifier collision is handled equally by B, D and E (generic
  uniqueness check); D (relations + anchors without coordinates) is as good as or better than E
  on several cases (S11: D 1.000 vs E 0.875 correct-unique because E reports the conflict as
  set-valued); sparse relations reduce E coverage to 0.234; E is 3.67× larger than A in JSON.
- **Calibration:** with noisy axis anchors (0.01/0.03/0.1 rad) the probabilistic N/S state has
  Brier score 0.0049/0.0168/0.0666; unique claims err in at most 0.28% of items.

**Gate verdict: GO (narrowed).** The surviving contribution is the record + validator + decoder
that (i) never coerces non-identifiable states, (ii) distinguishes independent physical anchors
from digital copies, and (iii) cross-checks coordinates against relations and provenance. The
claim is restricted to "no false certainty under the specified loss and corruption modes, at the
cost of storage and of coverage relative to simple redundancy under independent deletion". No
claim of superiority under intact metadata; no new standard is claimed; the group chain is cited
as a foundation.

## Independent audit reassessment (after strengthening the baseline, 2026-11-06)

The Phase 5 verdict was re-examined in a later session. Two implementation defects inflated the
advantage of E:

1. **BR reconciliation compared only keys present in both copies**, so a field deleted from the
   primary copy (typically `transformation_to_frame`) was neither detected nor repaired from the
   redundant copy. BR now reconciles over the union of keys (missing ⇒ repaired from the other
   copy; different ⇒ conflict).
2. **The epoch-mislabel scenario S10 relied on a stale hash** computed before the corruption, and B
   carried no hash at all. B/BR now carry a SHA-256 fixity checksum of `coordinates.values`
   (schema 1.1.0) and the strict decoder rejects a record whose checksum fails. S10 keeps the
   post-export corruption; the new S13 commits the same error before the hashes are issued.

Re-run results (`results/manuscript_values.csv`):

- S10: B and BR are flagged invalid (1.000); E falls back to relations (1.000 correct-unique).
- S13 (checksum re-issued): B false certainty 0.415; E 0 but only 0.609 correct-unique (0.391
  set-valued); D 1.000.
- MCAR: B 0.015–0.057 of records with false certainty; BR 0–0.018, only when both copies had lost
  the transformation (3000-record stress check: 129/129 false-certainty records satisfied this);
  E 0. BR coverage ≥ E coverage at every rate (0.962 vs 0.908 at 0.1; 0.534 vs 0.290 at 0.5);
  D 0.459 at 0.5.
- D (same record without coordinates) also has zero false certainty in every deterministic
  scenario and is at least as good as E except when the chirality witness is absent or invalid
  (S7/S8: E 1.000, D 0.726).
- Anchors in the benchmark are computed from the true configuration and are independent of each
  corruption by stipulation; this is now stated in Limitations.

The gate rule is still met (false certainty reduced against B under S4, S11, S13 and MCAR; no
loss with intact metadata; digital-copy witness ablation equals no witness), but the advantage is
narrower: against the repaired-redundancy baseline it is the absence of false certainty in S4,
S11, S13 and in ≤1.8% of MCAR records, bought with coverage, and it is carried by the relations,
anchors and conflict checks rather than by the coordinates. **Verdict: GO (further narrowed);**
manuscript claims were rewritten to this scope.
