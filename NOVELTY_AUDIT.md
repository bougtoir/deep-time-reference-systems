# Novelty audit

## Prior art domains checked

| Domain | Established result | Representative verified sources | Consequence for claims |
|---|---|---|---|
| Terrestrial reference systems and frames | A reference system is a conceptual definition; a frame is a realization with origin, orientation, scale, and time evolution. | IERS Conventions 2010; Altamimi et al. (2023); Moritz (2000) | Not novel. The manuscript adopts this terminology. |
| Euclidean distance geometry | A complete Euclidean distance matrix determines a generic configuration up to Euclidean isometry, including reflection. | Liberti et al. (2014); Dokmanić et al. (2015) | Not novel. Used as the mathematical base. |
| Proper alignment and chirality | Orthogonal Procrustes/Kabsch alignment distinguishes proper rotations from reflection-permitting fits. | Kabsch (1976, 1978) | Not novel. Used computationally. |
| Plate and paleogeographic frames | Paleomagnetic and plate-reconstruction constraints are model dependent; paleolatitude is generally better constrained than paleolongitude. | Torsvik et al. (2008, 2012, 2017) | Not novel. Manuscript avoids claiming that paleolongitude is categorically impossible. |
| Long-term coordinate preservation | Coordinates require metadata about CRS, datum/frame, coordinate epoch, and operations. | ISO 19111:2019; IERS Conventions 2010 | Not novel. Motivates the metadata-loss case. |

## Defensible contribution

The contribution is the integration of these established results into a
geodetic **minimal-sufficiency hierarchy** for historical directional
statements. The hierarchy explicitly separates:

1. metric shape from coordinate representation;
2. north/south identifiability from east/west identifiability;
3. handed relative longitude from absolute longitude;
4. geometric ambiguity from epoch, entity-identity, uncertainty, and
   provenance uncertainty; and
5. model storage from storage of independently checkable observations and
   anchors.

The synthetic and ITRF2020 experiments operationalize the hierarchy and expose
failure signatures: distances remain exact under reflection, north/south
classification remains exact under axial reflection, and east/west
classification reverses.

## Claims intentionally not made

- No claim that distance-geometry reconstruction or ITRF2020 is new.
- No claim that a spin axis alone provides east/west or absolute longitude.
- No claim that paleolongitude is impossible; it is described as
  additional-constraint-dependent and model-dependent.
- No claim that a single archival schema is permanently sufficient under all
  physical or semantic changes.
- No claim that the ITRF station example validates geological plate models.

## Remaining novelty risk

The exact phrase “minimal sufficient information for historical directional
relations” may have analogues in spatial databases, geographic information
science, robotics, or archaeological provenancing outside the geodetic
literature sampled here. The manuscript therefore uses “we formulate” and
“we provide” rather than an unqualified “first.”
