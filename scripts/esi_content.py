"""Earth Science Informatics manuscript text; every number is read from the result registry."""

from __future__ import annotations

from dtrs.records import SCHEMA_VERSION

TITLE = (
    "Recoverability-aware records for spatial relations under incomplete "
    "reference-frame metadata"
)
SHORT_TITLE = "Recoverability-aware spatial-relation records"
ARTICLE_TYPE = "Methodology"
KEYWORDS = [
    "coordinate reference system metadata",
    "data provenance",
    "uncertainty",
    "identifiability",
    "geodetic reference frame",
    "data validation",
]
RATES = ("0p05", "0p1", "0p2", "0p3", "0p5")
NOISES = ("0p01", "0p03", "0p1")


def _p(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def abstract(v: dict[str, float]) -> str:
    if any(v[f"rec_field_mcar_r{r}_E_records_with_false_certainty"] > 0 for r in RATES):
        raise ValueError("E produced false certainty under field MCAR; revise the abstract")
    return (
        "Coordinates are interpretable only with their coordinate reference system, frame "
        "realization, epoch and transformation; when this metadata is lost or silently "
        "corrupted, software still returns a unique answer. I present a versioned, "
        "machine-readable record for time-indexed spatial relations, a validator and a "
        "decoder that report, per task, whether a relation is unique, unique up to a "
        "residual group, set-valued, probabilistic, non-identifiable or invalid. The "
        "record stores coordinates with complete metadata, labelled distances, origin, "
        "axis, chirality and meridian anchors whose evidence type is explicit, "
        "uncertainty and SHA-256 provenance. I benchmarked six representations on "
        f"{int(v['n_selected_sites'])} ITRF2020 satellite-laser-ranging stations, "
        f"{int(v['rec_n_scenarios'])} intact, loss and corruption scenarios and random field "
        "deletion, against a strong baseline (complete metadata, fixity checksum, "
        "repaired redundant copy). With intact metadata both recovered "
        "every task. Under a silent handedness flip the baseline gave false certainty on "
        f"{_p(v['rec_S4_silent_left_handed_export_B_false_certainty'])} of task items, "
        "and on "
        f"{_p(v['rec_S13_epoch_mislabelled_at_export_B_false_certainty'])} when "
        "wrong-epoch values were exported with a re-issued checksum; the proposed record "
        "gave none, but in the latter case returned "
        f"{_p(v['rec_S13_epoch_mislabelled_at_export_E_informative_ambiguity'])} of items "
        "as set-valued, whereas a coordinate-free relations-and-anchors record recovered "
        "all. Under independent field deletion no proposed record produced false "
        f"certainty (0/{int(v['rec_field_mcar_r0p5_E_n_records'])} records per rate; "
        "95% upper bound "
        f"{_p(v['rec_field_mcar_r0p5_E_records_with_false_certainty_95ci_high'], 4)}); the "
        "redundant baseline did so in at most "
        f"{_p(max(v[f'rec_field_mcar_r{r}_BR_records_with_false_certainty'] for r in RATES))} "
        "of records but retained equal or greater coverage. This safety is conditional: "
        "corruption that also reached relations or anchors defeated it, and a "
        "mislabelled chirality anchor induced false certainty ("
        f"{_p(v['rec_stress_X4_chirality_anchor_mislabelled_E_false_certainty'])} of "
        "items). The contribution is safety under specified metadata loss, not "
        "superiority with complete metadata."
    )


def captions(v: dict[str, float]) -> list[str]:
    return [
        "Residual invariance group of the retained observables after successive "
        "independent physical anchors (known results; Sect. 3). Complete centred chord "
        "distances leave O(3); a directed axis leaves O(2); an independently recoverable "
        "chiral witness leaves SO(2); a directed meridian removes the final rotation. "
        "Metric scale is assumed known.",
        "Data flow of the recoverability-aware relation record. The validator rejects "
        "structurally invalid records and flags invalid components; the decoder combines "
        "a coordinate path and a relational path, cross-checks them against anchors, "
        "uncertainty and provenance hashes, and emits a per-task recoverability state.",
        "ITRF2020 test network. Left: the "
        f"{int(v['n_selected_sites'])} selected SLR stations and published velocity "
        "magnitudes. Right: absolute pairwise chord-distance changes after linear "
        f"propagation from {v['reference_epoch']:.1f} to {v['comparison_epoch']:.1f}.",
        "Outcome of each deterministic loss or corruption scenario for representations A "
        "(coordinates only), B (coordinates and complete metadata), BR (B with a "
        "redundant metadata copy and digital chirality bit), C (relations only), D "
        "(relations and physical anchors) and E (proposed hybrid). Each cell is the "
        f"proportion of {int(v['rec_n_items_per_scenario'])} task items.",
        "Random metadata loss. Rows: independent deletion of individual fields and "
        "correlated loss of the whole metadata block. Left: proportion of records with at "
        "least one false-certainty answer with 95% Wilson intervals (symmetric-log axis). "
        "Right: mean correct-unique coverage with 95% intervals. "
        f"{int(v['rec_missingness_replicates'])} replicates per convention, three "
        "storage conventions. Where fewer lines are visible, series coincide.",
        "Left: field ablation of representation E aggregated over all deterministic "
        "scenarios; numbers give the false-certainty proportion. Right: reliability of "
        "probabilistic north/south states under noisy axis anchors; marker area scales "
        "with the number of items per bin.",
    ]


def _same_as_b(v: dict[str, float], scenario: str) -> float:
    e = v[f"rec_stress_{scenario}_E_false_certainty"]
    if abs(e - v[f"rec_stress_{scenario}_B_false_certainty"]) > 1e-12:
        raise ValueError(f"stress scenario {scenario}: E and B differ; revise the prose")
    return e


def sections(v: dict[str, float], rigidity_sizes: str, rigidity_probabilities: str):
    fc_b_mcar = [v[f"rec_field_mcar_r{r}_B_records_with_false_certainty"] for r in RATES]
    fc_br_mcar = [v[f"rec_field_mcar_r{r}_BR_records_with_false_certainty"] for r in RATES]
    return [
        ("1 Introduction", [
            "A coordinate tuple is not a location by itself. Its meaning depends on a "
            "coordinate reference system (CRS), a datum or reference-frame realization, a "
            "coordinate epoch and the coordinate operations applied to it (ISO 2019; Petit "
            "and Luzum 2010). Terrestrial reference frames such as ITRF2020 realize origin, "
            "scale, orientation and time evolution from observations (Altamimi et al. 2023), "
            "and station positions are epoch-dependent (Bevis and Brown 2014). In data "
            "systems the numeric values routinely outlive this context: sidecar files are "
            "dropped in format conversion, axis-order conventions are misread, epochs are "
            "left implicit and provenance is not updated when values are edited.",
            "The usual informatics answer is complete metadata: ISO 19111 and its OGC "
            "abstract specification define dynamic CRSs, coordinate epochs and point-motion "
            "operations, and PROJJSON serializes them (ISO 2019; OGC 2019; PROJ 2023). When "
            "that metadata is present and correct it is sufficient, and I show this "
            "explicitly. The failure addressed here is different: when metadata is missing "
            "or silently wrong, a consumer that reads coordinates still returns a single, "
            "precise-looking answer. Nothing in the data tells it that a signed east–west "
            "relation or an absolute longitude has become non-identifiable.",
            "This paper contributes (i) a versioned JSON record for time-indexed spatial "
            "relations that stores, alongside coordinates and complete reference-system "
            "metadata, frame-free relational evidence and independent physical anchors "
            "whose evidence type is explicit; (ii) a validator and a decoder that return a "
            "per-task recoverability state instead of coercing ambiguity into one "
            "coordinate; and (iii) a reproducible benchmark against a strong "
            "coordinate-plus-metadata baseline under specified loss and corruption modes, "
            "with ablations, calibration and cost. The mathematics in Sect. 3 is used as a "
            "foundation and is not claimed as new.",
        ]),
        ("2 Related work", [
            "Standards. ISO 19111 and OGC Topic 2 model CRSs, datum ensembles, dynamic "
            "frames, coordinate epochs and transformations (ISO 2019; OGC 2019); PROJJSON "
            "encodes them (PROJ 2023). ISO 19115-1 and ISO 19157-1 describe lineage and "
            "positional accuracy (ISO 2014, 2023). W3C PROV-O and OWL-Time express "
            "provenance and temporal entities (W3C 2013, 2022), GeoSPARQL 1.1 standardizes "
            "topological relations and their querying (OGC 2024; Car and Homburg 2022), and "
            "OAIS defines preservation of representation information (CCSDS 2024). These "
            "specify how to describe a CRS or lineage; none returns a machine-readable "
            "statement of which relations remain identifiable when parts of that "
            "description are lost.",
            "Earth science informatics. Provenance tracing (Barkstrom 2010; Tilmes et al. "
            "2010), common data models (Nativi et al. 2008), spatio-temporal knowledge "
            "representation (Galton 2009), regridding architectures (Shippert and Gaustad "
            "2017), decentralized metadata management (Fugazza et al. 2021) and semantic "
            "interoperability (Lakani et al. 2026) address description and exchange. "
            "Uncertainty propagation in GIS and model chains (Heuvelink et al. 1989; Bastin "
            "et al. 2013), FAIR principles (Wilkinson et al. 2016), persistent identifiers "
            "(Klump and Huber 2017) and geospatial knowledge graphs (Hogan et al. 2022; "
            "Janowicz et al. 2022) complement them. Qualitative spatial reasoning "
            "formalizes topology and orientation relations (Egenhofer and Franzosa 1991; "
            "Freksa 1992) but assumes a shared orientation frame. Plate-reconstruction "
            "software makes deep-time frames explicit through models (Müller et al. 2018).",
            "Geodesy and geometry. Datum defects, free-network adjustment and minimum "
            "constraints are mature topics (Sillard and Boucher 2001; Kotsakis and "
            "Chatzinikos 2017; Chatzinikos and Dermanis 2017). Distance geometry and "
            "Procrustes alignment give recovery up to Euclidean motions (Kabsch 1976; "
            "Liberti et al. 2014; Dokmanić et al. 2015), and rigidity theory characterizes "
            "incomplete distance graphs (Asimow and Roth 1978). The present work reuses "
            "these results to define what a data record must carry and what a consumer "
            "may claim.",
        ]),
        ("3 Foundations: observables and residual invariance", [
            "Let $X = \\left[x_1, \\dots, x_n\\right]^{\\mathsf{T}}$ be labelled points in "
            "$\\mathbb{R}^3$ with chord distances $d_{ij} = \\|x_i - x_j\\|$. Double "
            "centring, $B = -\\tfrac{1}{2}\\,J(D\\circ D)J$ with "
            "$J = I - \\mathbf{1}\\mathbf{1}^{\\mathsf{T}}/n$, recovers a configuration "
            "unique up to translation and an orthogonal transformation (Dokmanić et al. "
            "2015). An independent origin removes translation, a directed axis $s$ leaves "
            "$O(2)$, a physically recoverable chiral witness leaves $SO(2)$ and a directed "
            "meridian leaves the identity (Fig. 1). Axial latitude "
            "$\\phi_s(x) = \\arcsin\\frac{s\\cdot x}{\\|s\\|\\,\\|x\\|}$ is invariant under "
            "the whole group, whereas the signed relative longitude "
            "$\\operatorname{atan2}[s\\cdot(b_\\perp\\times a_\\perp),\\; a_\\perp\\cdot "
            "b_\\perp]$ on $-\\pi < \\lambda \\leq \\pi$ is multiplied in sign by "
            "$\\det(Q)$. Table 1 lists the resulting task-level identifiability.",
            "__FIGURE_1__",
            "__TABLE_1__",
            "Two consequences shape the data model. First, a stored orientation bit or a "
            "second copy of the CRS is not independent evidence: if it is recomputed from "
            "the same corrupted values it agrees with them. The record therefore labels "
            "each anchor as independent physical evidence, a digital copy or a conventional "
            "definition. Second, identifiability is task-specific: distances can be "
            "unique while signed longitude is unique only up to $O(2)$, so a single "
            "record-level quality flag is insufficient.",
        ]),
        ("4 Method: the recoverability-aware relation record", [
            f"Record model. A record (schema dtrs-relation-record, version {SCHEMA_VERSION}) contains "
            "entities, optional coordinates and velocities, a reference-system block, "
            "labelled relations with epoch and rates, anchors, uncertainty, provenance "
            "and a declared recoverability block (Fig. 2; Table 2). Hashes of the "
            "coordinate and relation components are computed at export, so they detect "
            "alteration after export but not errors committed before the hash was "
            "issued; the declared "
            "residual group and per-task states are recomputed by the validator and a "
            "stale declaration is an error.",
            "__FIGURE_2__",
            "__TABLE_2__",
            "Validation. The validator checks the JSON structure against the schema and "
            "then semantic constraints: identifier collisions, array lengths, degenerate or "
            "non-orthogonal axes, relation edges referring to absent entities, collinear or "
            "out-of-range chirality triples, invalid meridian entities, provenance hash "
            "mismatches and stale declarations. Issues are fatal (record unusable), "
            "component (one anchor or path unusable) or warnings.",
            "Decoding. Six states are defined: unique; unique up to a named group; "
            "set-valued (conflicting candidates retained); probabilistic (with a "
            "probability); non-identifiable; and invalid record. The decoder evaluates a "
            "coordinate path only when the reference system is usable and the coordinate "
            "hash verifies, and a relational path by classical multidimensional scaling of "
            "the distances augmented by origin radii, followed by axis fitting, chirality "
            "selection and meridian rotation when the corresponding anchors are valid. "
            "The paths are cross-checked: distances are compared at the stated coverage "
            "factor, and coordinate-derived latitudes and chirality are compared with "
            "independent anchors. A disagreement withdraws the coordinate path for "
            "orientation tasks or yields a set-valued distance; a missing anchor yields "
            "the corresponding residual group. North–south ordering from noisy axis "
            "anchors is reported as probabilistic when the sign probability is below "
            "0.975. The step-by-step algorithm is given in Online Resource 1 (Sect. S2).",
            "Implementation. The schema, validator, decoders and benchmark are a Python "
            "package (dtrs.records) with a JSON Schema export, worked examples for every "
            "representation and damaged-record examples (Online Resource 2). Unit tests "
            "cover schema validity, intact recovery, refusal to claim orientation from "
            "relations alone, group-valued states, invalid-witness detection and the "
            "baseline comparisons. The full pipeline is executed by make reproduce.",
            "Use of AI tools. The Devin web service (Cognition) was used in September "
            "and November 2026 to assist with Python implementation, test writing, simulation "
            "execution, document generation and language revision. It did not supply "
            "source data. All numerical values are regenerated by the disclosed code from "
            "persisted inputs; the author reviewed the code, outputs, references and text "
            "and is responsible for the content.",
        ]),
        ("5 Testing", [
            "Data. The official ITRF2020 SLR station solution was persisted with its "
            "checksum (Altamimi et al. 2023). Stations with maximum coordinate standard "
            "uncertainty no greater than "
            f"{v['maximum_coordinate_standard_uncertainty_m']:.2f} m were binned by "
            f"longitude to select {int(v['n_selected_sites'])} sites (Fig. 3; Online "
            f"Resource 1, Table S1). Reference epoch {v['reference_epoch']:.1f} and "
            f"comparison epoch {v['comparison_epoch']:.1f} were used with published "
            "linear velocities.",
            "__FIGURE_3__",
            "Representations and tasks. Representation A stores coordinates only; B adds "
            "complete CRS, axis, unit, frame and epoch metadata, velocities and a SHA-256 "
            "fixity checksum of the coordinate values, and is the strong baseline; its "
            "decoder rejects the record when the checksum fails. BR adds a redundant "
            "metadata copy, reconciled over the union of keys so that a field missing "
            "from either copy is repaired from the other and a contradiction is an error, "
            "and a digital chirality bit; C stores labelled distances and rates only; D adds origin, axis, "
            "chirality and meridian anchors; E combines B and D with uncertainty and "
            "provenance. Tasks are metric distance (T1), north–south ordering (T2), "
            "signed east–west relation (T3), absolute longitude (T4) and distance at the "
            "comparison epoch (T5) for all pairs and sites; entity identity (T6) is "
            "evaluated through identifier collisions. An answer is correct when distances "
            f"agree within {v['rec_distance_tolerance_m']:.2f} m, signs agree, or longitude "
            f"agrees within {v['rec_longitude_tolerance_degrees']:.0e} degrees.",
            "Metrics. Each answer is classified as correct unique, false certainty (a "
            "unique answer that is wrong), honest ambiguity (group-valued, set-valued or "
            "probabilistic), non-identifiable or flagged invalid. Coverage is the "
            "correct-unique proportion. A deterministic scenario yields one record, so its "
            f"proportions describe all {int(v['rec_n_items_per_scenario'])} task items of that "
            "record exhaustively; they are not sampled estimates and carry no interval. Under "
            "random loss the unit is the record: record-level false certainty (at least one "
            "false answer) is summarized with Wilson intervals over independent records.",
            f"Scenarios. The {int(v['rec_n_scenarios'])} deterministic scenarios cover loss of the CRS block under "
            "three storage conventions, loss of the CRS identifier with parameters "
            "retained, loss of the coordinate epoch, a silent left-handed export in which "
            "all digitally derived fields are recomputed after the error, a correctly "
            "labelled axis swap, an identifier collision, absent and invalid chirality "
            "witnesses, joint loss of CRS and witness, coordinates replaced by values at "
            "the comparison epoch without updating hashes, the same error committed before "
            "the hashes were issued, an unflagged "
            f"{v['rec_perturbation_m']:.2f} m error at three sites, and sparse relations "
            f"(edge retention {v['rec_sparse_edge_probability']:.1f}) with the CRS lost "
            "(Table 3). Five stress scenarios (X1–X5) additionally corrupt the relations, "
            "anchors or identifiers consistently with the coordinates and re-issue every "
            "hash; they are reported separately because they break the independence "
            "assumption on which the deterministic scenarios rest. Random loss deletes each of fourteen metadata fields independently "
            "(MCAR) or the whole metadata block, including its copy, as a correlated "
            "failure. Ablations remove one component of E at a time or replace the "
            "physical chirality witness by a digital copy. Calibration perturbs axis "
            "anchors with Gaussian noise of "
            f"{v['rec_calibration_noise0p01_axis_noise_radians']:g}, "
            f"{v['rec_calibration_noise0p03_axis_noise_radians']:g} and "
            f"{v['rec_calibration_noise0p1_axis_noise_radians']:g} rad.",
            "__TABLE_3__",
            "Geometric foundations. The frozen geometric experiments are retained as "
            "checks of the decoder's foundations: complete-distance reconstruction with "
            "and without reflection, direction invariance under proper and improper "
            "transformations, WGS84–GRS80 sensitivity, and the local rigidity of random "
            f"three-dimensional frameworks for n = {rigidity_sizes} and edge-retention "
            f"probabilities {{{rigidity_probabilities}}} with "
            f"{int(v['rigidity_trials_per_cell'])} trials per cell (Table 4). All "
            f"calculations use seed {int(v['random_seed'])}; the record benchmark uses "
            f"seed {int(v['rec_seed'])}. Direction asymmetry, the rigidity phase diagram, the "
            "synthetic benchmark and anchor sensitivity are shown in Online Resource 1 "
            "(Figs. S1–S4), with ellipsoid sensitivity, the reference-frame taxonomy and "
            "the full numerical registry in Tables S2–S4.",
            "__TABLE_4__",
        ]),
        ("6 Results", [
            "Intact metadata. B and E recovered every task "
            f"(correct-unique {_p(v['rec_S0_intact_B_correct_unique'])} and "
            f"{_p(v['rec_S0_intact_E_correct_unique'])}); there is no gain from the "
            "proposed record when metadata are complete and correct (Fig. 4). "
            "Representation A gave false certainty on "
            f"{_p(v['rec_S0_intact_A_false_certainty'])} of items even when intact, "
            "because it cannot propagate distances to another epoch. C was correct on "
            f"{_p(v['rec_S0_intact_C_correct_unique'])} of items and returned "
            "non-identifiable for every orientation task, as required.",
            "__FIGURE_4__",
            "Silent corruption. Under the silent left-handed export B and BR gave false "
            f"certainty on {_p(v['rec_S4_silent_left_handed_export_B_false_certainty'])} "
            "of items, all in the east–west and longitude tasks, because the redundant "
            "copy and digital bit were recomputed from the corrupted values. E detected "
            "the contradiction with its independent chirality and axis anchors and "
            f"recovered {_p(v['rec_S4_silent_left_handed_export_E_correct_unique'])} of "
            "items from the relational path. When epoch-mislabelled values were written "
            "after the hashes had been issued, B and BR rejected the record through their "
            f"fixity checksum ({_p(v['rec_S10_epoch_mislabelled_coordinates_B_flagged_invalid'])} "
            "flagged invalid) and E fell back to the relational path. When the same error "
            "was committed before the hashes were issued, the checksum verified and B "
            "gave false certainty on "
            f"{_p(v['rec_S13_epoch_mislabelled_at_export_B_false_certainty'])} of items; "
            "E gave none but returned "
            f"{_p(v['rec_S13_epoch_mislabelled_at_export_E_informative_ambiguity'])} as "
            "set-valued because its coordinates contradicted its relations, whereas D was "
            f"correct on {_p(v['rec_S13_epoch_mislabelled_at_export_D_correct_unique'])}. "
            "Carrying coordinates therefore costs coverage when they are wrong in a way "
            "no hash can reveal. With an "
            "unflagged coordinate error B gave false certainty on "
            f"{_p(v['rec_S11_unflagged_coordinate_error_B_false_certainty'])}; E reported "
            f"{_p(v['rec_S11_unflagged_coordinate_error_E_informative_ambiguity'])} of "
            "items as set-valued and none falsely, whereas D, which has no coordinates to "
            "conflict with, was correct on "
            f"{_p(v['rec_S11_unflagged_coordinate_error_D_correct_unique'])}.",
            "Explicit loss. When the CRS block was deleted, B became non-identifiable on "
            f"{_p(v['rec_S1_crs_block_deleted_left_handed_B_non_identifiable'])} of items "
            "without error, BR recovered through its copy, and E recovered "
            f"{_p(v['rec_S1_crs_block_deleted_left_handed_E_correct_unique'])} through the "
            "relational path. When the chirality witness was also lost, E returned the "
            "east–west and longitude tasks as unique up to a group "
            f"({_p(v['rec_S9_crs_and_witness_lost_E_informative_ambiguity'])} of items). "
            "An identifier collision was handled identically by B, D and E "
            f"(set-valued {_p(v['rec_S6_entity_collision_E_informative_ambiguity'])}), so "
            "it is not an advantage of the proposal. Sparse relations reduced E's "
            f"coverage to {_p(v['rec_S12_sparse_relations_crs_lost_E_correct_unique'])}, "
            "with the remainder non-identifiable.",
            "Random loss. Under independent field deletion B produced at least one false "
            f"answer in {_p(min(fc_b_mcar))}–{_p(max(fc_b_mcar))} of records, when "
            "transformation parameters were lost while the axis labels remained (Fig. 5); "
            "BR, which repairs the primary from its copy, did so in "
            f"{_p(min(fc_br_mcar))}–{_p(max(fc_br_mcar))}, only when both copies had lost "
            "them. "
            "No E record produced false certainty at any rate (95% upper bound "
            f"{_p(max(v[f'rec_field_mcar_r{r}_E_records_with_false_certainty_95ci_high'] for r in RATES), 4)}; "
            f"0/{int(v['rec_field_mcar_r0p5_E_n_records'])} records at each rate). "
            "Coverage favoured repaired redundancy at every rate: at rate 0.1 BR retained "
            f"{_p(v['rec_field_mcar_r0p1_BR_mean_coverage'])} and E "
            f"{_p(v['rec_field_mcar_r0p1_E_mean_coverage'])}, at rate 0.5 "
            f"{_p(v['rec_field_mcar_r0p5_BR_mean_coverage'])} and "
            f"{_p(v['rec_field_mcar_r0p5_E_mean_coverage'])}; D, which has no coordinates "
            f"to withdraw, retained {_p(v['rec_field_mcar_r0p5_D_mean_coverage'])} at rate "
            "0.5. Under correlated block loss "
            f"E kept coverage {_p(v['rec_metadata_block_r0p5_E_mean_coverage'])} at rate "
            f"0.5, B and BR {_p(v['rec_metadata_block_r0p5_B_mean_coverage'])}.",
            "__FIGURE_5__",
            "Ablation and calibration. Over all scenarios the full record had false "
            f"certainty {_p(v['rec_ablation_full_false_certainty'], 4)}; removing relations "
            f"raised it to {_p(v['rec_ablation_no_relations_false_certainty'], 4)}, "
            "removing the chirality witness to "
            f"{_p(v['rec_ablation_no_chirality_anchor_false_certainty'], 4)}, and "
            "replacing the physical witness by a digital copy to "
            f"{_p(v['rec_ablation_chirality_digital_copy_false_certainty'], 4)} (Fig. 6). "
            "Probabilistic north–south states had Brier scores of "
            f"{_p(v['rec_calibration_noise0p01_brier_score'], 4)}, "
            f"{_p(v['rec_calibration_noise0p03_brier_score'], 4)} and "
            f"{_p(v['rec_calibration_noise0p1_brier_score'], 4)} at the three noise "
            "levels, and unique claims were wrong in at most "
            f"{_p(v['rec_calibration_noise0p1_unique_error_rate'], 4)} of items.",
            "__FIGURE_6__",
            "Corrupted independent evidence. When the corruption reached the evidence on "
            "which E relies and every hash was re-issued, E lost its protection (Online "
            "Resource 1, Table S5). A handedness flip that also reversed the chirality "
            "anchor, coordinates and relations sharing the same "
            f"{v['rec_perturbation_m']:.2f} m error, two identifiers swapped consistently "
            "in every field, and all fields written at the wrong epoch with matching labels "
            "gave E false certainty on "
            f"{_p(_same_as_b(v, 'X1_handedness_flip_including_anchor'))}, "
            f"{_p(_same_as_b(v, 'X2_agreeing_wrong_coordinates_and_relations'))}, "
            f"{_p(_same_as_b(v, 'X3_consistent_identifier_swap'))} and "
            f"{_p(_same_as_b(v, 'X5_consistent_wrong_epoch'))} of items, the same "
            "proportions as B. A mislabelled chirality anchor on otherwise correct data "
            "made E wrong on "
            f"{_p(v['rec_stress_X4_chirality_anchor_mislabelled_E_false_certainty'])} of "
            "items, where B, which has no such anchor, gave "
            f"{_p(v['rec_stress_X4_chirality_anchor_mislabelled_B_false_certainty'])}. The "
            "absence of false certainty in the deterministic scenarios is therefore a "
            "consequence of the decoder's refusal rules together with evidence that the "
            "corruption did not reach, not an empirical property of the record.",
            "Cost. The E record for the test network occupied "
            f"{int(v['rec_cost_E_json_bytes'])} bytes of compact JSON, "
            f"{v['rec_cost_E_size_ratio_to_A']:.2f} times representation A and "
            f"{v['rec_cost_E_size_ratio_to_A'] / v['rec_cost_B_size_ratio_to_A']:.2f} "
            "times B; median decoding time was "
            f"{v['rec_cost_E_median_decode_ms']:.1f} ms.",
            "Geometric checks. Complete distances reconstructed the synthetic "
            "configuration with reflection-permitting RMSE "
            f"{v['distance_reconstruction_rmse_allow_reflection_m']:.0e} m, whereas a "
            "proper-only alignment left "
            f"{v['distance_reconstruction_rmse_proper_only_m'] / 1e6:.3f} million m. "
            "Replacing WGS84 by GRS80 changed chord distances by at most "
            f"{v['ellipsoid_maximum_chord_distance_difference_m']:.6f} m without changing "
            "any directional classification. For "
            f"{int(v['rigidity_largest_network_n_points'])}-point frameworks full local "
            f"rigidity occurred in {v['rigidity_probability_before_95pct_threshold']:.4f} "
            f"of trials at edge retention {v['rigidity_edge_probability_before_95pct_threshold']:.1f} "
            f"(95% interval {v['rigidity_probability_before_95pct_threshold_95ci_lower']:.4f}–"
            f"{v['rigidity_probability_before_95pct_threshold_95ci_upper']:.4f}) and "
            f"{v['rigidity_probability_at_95pct_threshold']:.3f} at "
            f"{v['rigidity_95pct_threshold_edge_probability']:.1f} "
            f"({v['rigidity_95pct_threshold_95ci_lower']:.4f}–"
            f"{v['rigidity_95pct_threshold_95ci_upper']:.4f}). In the ITRF2020 network "
            "the maximum and median pairwise distance changes over the ten-year interval "
            f"were {v['maximum_pairwise_distance_change_m']:.3f} m and "
            f"{v['median_pairwise_distance_change_m']:.3f} m, so distance relations are "
            "epoch-specific at the centimetre level.",
        ]),
        ("7 Discussion", [
            "Complete CRS metadata is the right operational answer and remains so: the "
            "benchmark shows no advantage of the proposed record when it is intact. The "
            "record is useful when the metadata cannot be trusted or has been partly "
            "lost, which is the normal condition of long-lived and repeatedly converted "
            "data. Its safety comes from three design choices that existing metadata "
            "standards do not combine: per-task recoverability states, frame-free "
            "relational evidence cross-checked against coordinates, and an explicit "
            "distinction between independent physical anchors and digital copies. The "
            "safety is conditional rather than intrinsic: the decoder withholds a unique "
            "answer only when evidence that survived the corruption contradicts the "
            "coordinates. Where the same error reaches every channel, as in the stress "
            "scenarios, no record-level check can detect it, and an incorrectly labelled "
            "anchor can introduce error into correct data.",
            "The ablations make the last point quantitative. A second copy of the CRS or "
            "a stored chirality bit increases coverage under independent deletion but "
            "fails together with the values under common-mode corruption, and a fixity "
            "checksum detects alteration after export but not an error committed before "
            "it. A strong baseline that reconciles its copies and verifies a checksum "
            "removes most, but not all, of the false certainty that a naive consumer "
            "shows; the remaining advantage of the proposed record is the absence of "
            "false certainty, paid for in coverage. That advantage comes from the "
            "relations, anchors and conflict checks, not from the coordinates: profile D, "
            "the same record without coordinates, also gave no false certainty in any "
            "scenario and was correct more often than E when coordinates were wrong "
            f"(unflagged error: {_p(v['rec_S11_unflagged_coordinate_error_D_correct_unique'])} "
            f"versus {_p(v['rec_S11_unflagged_coordinate_error_E_correct_unique'])}), whereas "
            "E kept coverage when the chirality witness was absent "
            f"({_p(v['rec_S7_chirality_witness_absent_E_correct_unique'])} versus "
            f"{_p(v['rec_S7_chirality_witness_absent_D_correct_unique'])}). Carrying "
            "coordinates is therefore a coverage choice that an archive can make per "
            "dataset, not a safety mechanism. Redundancy "
            "therefore has to be designed around independent failure modes, a point that "
            "applies equally to plate-reconstruction outputs whose frames are model "
            "choices (Müller et al. 2018).",
            "The states map naturally onto existing vocabularies: the declared "
            "recoverability block can be expressed as a PROV-O derivation with a "
            "data-quality result in the sense of ISO 19157-1, and the relations as "
            "GeoSPARQL-style statements with OWL-Time epochs. I did not implement these "
            "mappings; the JSON Schema is the normative form in this version.",
        ]),
        ("8 Limitations", [
            "The benchmark uses one realized network of "
            f"{int(v['n_selected_sites'])} stations and synthetic corruption; the "
            "scenarios are specified failure modes, not a sample of real data incidents, "
            "so the proportions are conditional on them. The Euclidean chord model, known "
            "metric scale, linear velocities and generic configurations are assumed; "
            "deformation, nonlinear station motion, surface-geodesic distances and "
            "identity inference beyond collision detection are not treated. In the "
            "benchmark the anchors are computed from the true configuration and their "
            "independence is a stipulation of each scenario (the corruption does not "
            "reach them); the results test how the decoder uses independent evidence, "
            "not whether such evidence is available in practice. The axis anchor stores "
            "geocentric latitudes and is therefore a second, differently failing encoding "
            "of the coordinates rather than a new observation. Independent "
            "physical anchors are assumed to exist and to be correctly labelled; the "
            "record can describe but not create them. A digital chirality bit is never "
            "treated as a recovered physical handedness anchor. The relational path needs "
            "complete or rigid distance graphs, and coverage falls with sparsity. The "
            "stress scenarios show that the record gives false certainty whenever an error "
            "is common to the coordinates and to the evidence meant to check them.",
            "A more fundamental limitation concerns the validity of the physical anchors "
            "themselves. In the absence of independent verification evidence, the "
            "correctness of an anchor cannot generally be established from the archived "
            "record alone. Internal consistency, provenance hashes, and agreement among "
            "digitally derived copies do not guarantee physical validity; a corrupted or "
            "incorrectly labelled anchor may remain internally consistent and lead to false "
            "certainty. Accordingly, the absence of detected inconsistency must not be "
            "interpreted as evidence that the recovered spatial relation is necessarily "
            "correct.",
            "Nevertheless, complete loss of all information is not required for "
            "recoverability to fail, nor does partial information loss necessarily preclude "
            "fault detection. Where multiple sufficiently independent anchors or other "
            "physical constraints survive, cross-anchor consistency checks, "
            "leave-one-anchor-out reconstruction, and fault-aware inference may help detect "
            "inconsistencies, identify suspect anchors, or recover relations under explicit "
            "assumptions about the number, independence, and structure of faults. Such "
            "methods cannot guarantee identification of the correct anchor when the "
            "surviving evidence is insufficient, mutually dependent, or affected by "
            "common-mode corruption. Establishing the necessary and sufficient conditions "
            "for anchor-fault detection, fault localization, and reliable recovery—including "
            "the minimum independent evidence required—remains an important direction for "
            "future research.",
        ]),
        ("9 Conclusions", [
            "A recoverability-aware record that keeps coordinates with full metadata, "
            "labelled relations, independent anchors, uncertainty and provenance, "
            "together with a validator and decoder that report per-task states, removed "
            "false certainty in every specified loss and corruption scenario in which the "
            "relations and anchors were not themselves corrupted, while matching the strong "
            "baseline when metadata were intact; when they were corrupted consistently with "
            "the coordinates, it failed like the baseline. It costs storage, "
            "coverage relative to repaired redundancy under independent deletion, "
            "and coverage relative to a coordinate-free record when coordinates are wrong "
            "before export. The "
            "schema, code, data and benchmark are openly available for reuse and "
            "extension.",
        ]),
    ]


REFERENCES = [
    "Altamimi Z, Rebischung P, Collilieux X, Métivier L, Chanard K (2023) ITRF2020: an augmented reference frame refining the modeling of nonlinear station motions. J Geod 97:47. https://doi.org/10.1007/s00190-023-01738-w",
    "Asimow L, Roth B (1978) The rigidity of graphs. Trans Am Math Soc 245:279–289. https://doi.org/10.1090/S0002-9947-1978-0511410-9",
    "Barkstrom BR (2010) A mathematical framework for earth science data provenance tracing. Earth Sci Inform 3:167–196. https://doi.org/10.1007/s12145-010-0057-0",
    "Bastin L, Cornford D, Jones R, Heuvelink GBM, Pebesma E, Stasch C, Nativi S, Mazzetti P, Williams M (2013) Managing uncertainty in integrated environmental modelling: the UncertWeb framework. Environ Model Softw 39:116–134. https://doi.org/10.1016/j.envsoft.2012.02.008",
    "Bevis M, Brown A (2014) Trajectory models and reference frames for crustal motion geodesy. J Geod 88:283–311. https://doi.org/10.1007/s00190-013-0685-5",
    "Car NJ, Homburg T (2022) GeoSPARQL 1.1: motivations, details and applications of the decadal update to the most important geospatial LOD standard. ISPRS Int J Geo-Inf 11:117. https://doi.org/10.3390/ijgi11020117",
    "CCSDS (2024) Reference model for an Open Archival Information System (OAIS). CCSDS 650.0-M-3, Magenta Book. Consultative Committee for Space Data Systems, Washington DC. https://public.ccsds.org/Pubs/650x0m3.pdf",
    "Chatzinikos M, Dermanis A (2017) A coordinate-invariant model for deforming geodetic networks: understanding rank deficiencies, non-estimability of parameters, and the effect of the choice of minimal constraints. J Geod 91:375–396. https://doi.org/10.1007/s00190-016-0970-1",
    "Dokmanić I, Parhizkar R, Ranieri J, Vetterli M (2015) Euclidean distance matrices: essential theory, algorithms, and applications. IEEE Signal Process Mag 32(6):12–30. https://doi.org/10.1109/MSP.2015.2398954",
    "Egenhofer MJ, Franzosa RD (1991) Point-set topological spatial relations. Int J Geogr Inf Syst 5:161–174. https://doi.org/10.1080/02693799108927841",
    "Freksa C (1992) Using orientation information for qualitative spatial reasoning. In: Frank AU, Campari I, Formentini U (eds) Theories and methods of spatio-temporal reasoning in geographic space. Lecture Notes in Computer Science 639. Springer, Berlin, pp 162–178. https://doi.org/10.1007/3-540-55966-3_10",
    "Fugazza C, Tagliolato Acquaviva d’Aragona P, Oggioni A, Carrara P (2021) Decentralized geospatial metadata management. Earth Sci Inform 14:1579–1596. https://doi.org/10.1007/s12145-020-00559-1",
    "Galton A (2009) Spatial and temporal knowledge representation. Earth Sci Inform 2:169–187. https://doi.org/10.1007/s12145-009-0027-6",
    "Heuvelink GBM, Burrough PA, Stein A (1989) Propagation of errors in spatial modelling with GIS. Int J Geogr Inf Syst 3:303–322. https://doi.org/10.1080/02693798908941518",
    "Hogan A, Blomqvist E, Cochez M et al (2022) Knowledge graphs. ACM Comput Surv 54(4):71. https://doi.org/10.1145/3447772",
    "ISO (2014) ISO 19115-1:2014 Geographic information—Metadata—Part 1: Fundamentals. International Organization for Standardization, Geneva. https://www.iso.org/standard/53798.html",
    "ISO (2019) ISO 19111:2019 Geographic information—Referencing by coordinates. International Organization for Standardization, Geneva. https://www.iso.org/standard/74039.html",
    "ISO (2023) ISO 19157-1:2023 Geographic information—Data quality—Part 1: General requirements. International Organization for Standardization, Geneva. https://www.iso.org/standard/78900.html",
    "Janowicz K, Hitzler P, Li W et al (2022) Know, know where, KnowWhereGraph: a densely connected, cross-domain knowledge graph and geo-enrichment service stack for applications in environmental intelligence. AI Mag 43:30–39. https://doi.org/10.1002/aaai.12043",
    "Kabsch W (1976) A solution for the best rotation to relate two sets of vectors. Acta Crystallogr A 32:922–923. https://doi.org/10.1107/S0567739476001873",
    "Klump J, Huber R (2017) 20 years of persistent identifiers—which systems are here to stay? Data Sci J 16:9. https://doi.org/10.5334/dsj-2017-009",
    "Kotsakis C, Chatzinikos M (2017) Rank defect analysis and the realization of proper singularity in normal equations of geodetic networks. J Geod 91:627–652. https://doi.org/10.1007/s00190-016-0989-3",
    "Lakani E, Louge T, Karray MH (2026) Geoscience semantic interoperability: systematic review of semantic resources. Earth Sci Inform 19:111. https://doi.org/10.1007/s12145-026-02159-x",
    "Liberti L, Lavor C, Maculan N, Mucherino A (2014) Euclidean distance geometry and applications. SIAM Rev 56:3–69. https://doi.org/10.1137/120875909",
    "Müller RD, Cannon J, Qin X et al (2018) GPlates: building a virtual Earth through deep time. Geochem Geophys Geosyst 19:2243–2261. https://doi.org/10.1029/2018GC007584",
    "Nativi S, Caron J, Domenico B, Bigagli L (2008) Unidata’s Common Data Model mapping to the ISO 19123 data model. Earth Sci Inform 1:59–78. https://doi.org/10.1007/s12145-008-0011-6",
    "OGC (2019) Topic 2—Referencing by coordinates. OGC Abstract Specification 18-005r5. Open Geospatial Consortium. https://docs.ogc.org/as/18-005r5/18-005r5.html",
    "OGC (2024) OGC GeoSPARQL—a geographic query language for RDF data, version 1.1. OGC 22-047r1. Open Geospatial Consortium. https://docs.ogc.org/is/22-047r1/22-047r1.html",
    "Petit G, Luzum B (eds) (2010) IERS Conventions (2010). IERS Technical Note 36. Verlag des Bundesamts für Kartographie und Geodäsie, Frankfurt am Main. https://iers-conventions.obspm.fr/content/tn36.pdf",
    "PROJ (2023) PROJJSON specification. PROJ contributors. https://proj.org/en/latest/specifications/projjson.html",
    "Shippert T, Gaustad K (2017) An architecture for consolidating multidimensional time-series data onto a common coordinate grid. Earth Sci Inform 10:247–256. https://doi.org/10.1007/s12145-016-0285-z",
    "Sillard P, Boucher C (2001) A review of algebraic constraints in terrestrial reference frame datum definition. J Geod 75:63–73. https://doi.org/10.1007/s001900100166",
    "Tilmes C, Yesha Y, Halem M (2010) Tracking provenance of earth science data. Earth Sci Inform 3:59–65. https://doi.org/10.1007/s12145-010-0046-3",
    "W3C (2013) PROV-O: the PROV ontology. W3C Recommendation 30 April 2013. https://www.w3.org/TR/prov-o/",
    "W3C (2022) Time ontology in OWL. W3C Candidate Recommendation Draft 15 November 2022. https://www.w3.org/TR/owl-time/",
    "Wilkinson MD, Dumontier M, Aalbersberg IJ et al (2016) The FAIR Guiding Principles for scientific data management and stewardship. Sci Data 3:160018. https://doi.org/10.1038/sdata.2016.18",
]

def cover_letter(v: dict[str, float]) -> list[str]:
    return [
        "Editor-in-Chief",
        "Earth Science Informatics",
        "",
        "Dear Editor,",
        f"I submit the Methodology article “{TITLE}” for consideration in Earth Science Informatics.",
        "The manuscript addresses an information-management failure that metadata standards describe but do not detect: when coordinate reference system, epoch or transformation metadata is lost or silently corrupted, software still returns unique answers. I contribute a versioned, machine-readable record for time-indexed spatial relations, a validator, and a decoder that reports per-task recoverability states (unique, unique up to a group, set-valued, probabilistic, non-identifiable or invalid), together with a reproducible benchmark against a strong coordinates-plus-complete-metadata baseline on ITRF2020 stations.",
        "With intact metadata the baseline and the proposed record both recovered every task. Under a silent handedness flip the baseline gave false certainty on "
        f"{_p(v['rec_S4_silent_left_handed_export_B_false_certainty'])} of task items and, when wrong-epoch values were exported with a re-issued checksum, on "
        f"{_p(v['rec_S13_epoch_mislabelled_at_export_B_false_certainty'])}; the proposed record gave none in these and the other specified scenarios.",
        "The limits are reported with equal weight. The baseline carries a fixity checksum and, in its redundant variant, repairs fields missing from either copy; repaired redundancy retains equal or greater coverage at every independent deletion rate; when coordinates are wrong before any checksum is issued, the proposed record avoids false certainty but loses coverage relative to a record without coordinates. The protection is conditional: when the corruption also reaches the relations or anchors, the proposed record gives false certainty like the baseline, and a mislabelled chirality anchor introduced it on "
        f"{_p(v['rec_stress_X4_chirality_anchor_mislabelled_E_false_certainty'])} of items of otherwise correct data. The method does not guarantee correctness under arbitrary corruption; it makes explicit which answers remain identifiable from evidence whose failure modes are independent of the coordinates.",
        "This version follows a desk decision at Journal of Geodesy (JOGE-D-26-00489), which judged that an earlier, geodesy-oriented version did not add sufficient methodological or topical innovation to be within the scope of that journal. I rebuilt the manuscript around the informatics contribution; the geometric results are retained only as foundations. It is not under consideration elsewhere.",
        "The schema, code, persisted input data, tests and generated results are openly available, and the full pipeline is reproducible with a single command.",
        "Sincerely,",
    ]
