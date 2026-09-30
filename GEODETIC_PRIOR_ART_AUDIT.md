# Geodetic prior-art audit

## Scope and conclusion

This audit tests whether the manuscript's contribution is distinct from established
geodetic datum theory, free-network adjustment, Helmert alignment, time-dependent
reference frames, and plate-reconstruction practice. The close prior art already
contains rigorous treatments of datum defect, rank deficiency, algebraic and inner
constraints, minimum-constraint realization, nonlinear deformation, and terrestrial
frame alignment. The manuscript therefore must not claim to introduce gauge freedom,
datum constraints, Helmert alignment, coordinate invariance, or station-trajectory
models.

The defensible contribution is narrower: a residual-invariance sufficiency audit for which
*relational observables* remain identifiable when a stored three-dimensional coordinate
realization loses some or all reference metadata. The hierarchy connects complete or
incomplete Euclidean distance data to a directed axis, a physically recoverable chiral
witness, a meridian direction, and epoch/entity metadata. Its value is an explicit
archival-identifiability test and reproducible demonstration, not a new terrestrial
reference frame or a replacement for geodetic datum realization.

## Claim-by-claim comparison

| Domain | Established result | Verified sources | Consequence for this manuscript |
|---|---|---|---|
| Free networks and datum defect | A geodetic normal system can be rank deficient because the observations do not determine all datum degrees of freedom. Datum realization requires appropriate constraints. | Papo (1985); Sillard and Boucher (2001); Kotsakis and Chatzinikos (2017) | Treat Euclidean gauge freedom as established geodesy. Use it to motivate, not claim, novelty. |
| Algebraic, inner, and minimum constraints | Different constraint strategies select realizations of an otherwise deficient network and may affect distortion and stability. | Sillard and Boucher (2001); Kotsakis (2012, 2013); Glaser et al. (2015) | Distinguish selecting a conventional realization from identifying an invariant relation. Do not equate a chosen constraint with recovered physical metadata. |
| Coordinate-invariant deformation models | Rank deficiencies, non-estimability, and minimal-constraint effects can be formulated without privileging a coordinate parameterization. | Chatzinikos and Dermanis (2017) | State explicitly that the residual-invariance analysis is compatible with coordinate-invariant datum theory and addresses a different archival question. |
| Helmert transformation and ITRF realization | Translation, rotation, and scale alignment are standard tools for combining or comparing terrestrial frames; origin, scale, and orientation are physically/conventionally realized by specified techniques and constraints. | Altamimi et al. (2002, 2023); Sillard and Boucher (2001); IERS Conventions (2010) | Present Procrustes alignment as the rigid, unit-scale special case used for diagnostics. It is not a substitute for operational ITRF realization. |
| No-net-translation/no-net-rotation | NNT/NNR conditions realize a datum relative to a selected station set or plate-motion model and can change interpretation. | Altamimi et al. (2003); Glaser et al. (2015); Zajdel et al. (2019) | Do not describe the reflected ITRF network as a plausible alternative realization. It is a mathematical witness to distance invariance only. |
| Datum-station selection | Network geometry and the selected datum stations affect station repeatability, Earth-rotation parameters, and geocenter estimates. | Zajdel et al. (2019) | The incomplete-network experiment should be described as a local rank/identifiability experiment, not operational evidence about ITRF accuracy. |
| Time-dependent frames and trajectories | Coordinates depend on epoch; secular, seasonal, discontinuity, post-seismic, and other nonlinear trajectory terms are required for modern reference frames. | Bevis and Brown (2014); Altamimi et al. (2023) | Retain epoch and entity identity as indispensable metadata. The present linear propagation is a limited demonstration, not a full station-motion model. |
| Earth orientation and celestial-terrestrial linkage | Earth orientation parameters connect terrestrial and celestial reference systems and make direction conventions time dependent. | IERS Conventions (2010) | A stored axis must include physical interpretation and epoch; an unlabeled vector does not recover geodetic north. |
| Paleogeographic frames | Paleomagnetism constrains latitude more directly than longitude; longitude estimates require additional model assumptions and geological/geodynamic information. | Torsvik et al. (2008, 2012); Torsvik and Cocks (2019) | Avoid categorical impossibility claims. Describe paleolongitude as more model dependent, not unrecoverable in all scientific settings. |

## Novelty boundary

The manuscript may claim:

1. an explicit residual-invariance sequence for the archival observables considered here;
2. a separation between an algebraic handedness label and a physically interpretable
   chiral witness;
3. precise definitions and degeneracy handling for axial ordering and signed relative
   longitude;
4. a reproducible local-rigidity experiment showing when incomplete distance graphs
   acquire null modes beyond Euclidean gauge freedom;
5. a preservation checklist linking observables to the metadata required for later
   interpretation.

The manuscript may not claim:

1. discovery of datum defect, rank deficiency, free-network adjustment, minimum
   constraints, Helmert transformations, NNT/NNR, or time-dependent terrestrial frames;
2. that a binary orientation field is necessarily a durable physical chiral witness;
3. that pairwise distances alone determine geodetic north, east/west, longitude, epoch,
   or entity identity;
4. that local rigidity-matrix rank establishes global rigidity;
5. that a reflected ITRF coordinate set is an operationally valid terrestrial frame;
6. that paleolongitude is universally impossible.

## Bibliographic decisions

- Journal issue years are used in the reference list. Chatzinikos and Dermanis is cited
  as 2017 (volume 91, issue 4), although Crossref records 2016 online publication.
- Torsvik and Cocks is cited as 2019 (volume 156, issue 2), while noting its 2017 online
  publication. The earlier mixed “2017” convention is removed.
- Every DOI used for substantive prior-art claims is listed in
  `references_verified.csv`; the raw Crossref work records are preserved under
  `data/raw/literature/` and registered in `data/data_acquisition_log.csv`.

## Submission relevance

The revised paper fits *Journal of Geodesy* only if it leads with reference-system/frame
dependence, datum defect, realization constraints, epoch dependence, and the limited
identifiability question. “Deep time” is an application motivation, not the primary
scientific claim. The cover letter and abstract must maintain this boundary.
