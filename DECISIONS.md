# Scientific and submission decisions

## Scope

1. Treat the problem as preservation of **relations and their identifiability
   class**, not preservation of a coordinate tuple.
2. Use deep time only as a stress test for frame loss, anchor failure,
   semantic drift, and model discontinuity.
3. Separate the theoretical reference system from its physical realization,
   following IERS terminology.
4. Use a modern ITRF2020 SLR network as a transparent real geodetic
   demonstration. It validates the symmetry argument in realized coordinates;
   it is not presented as a geological reconstruction.

## Mathematical model

The archived event is represented as

```text
E = {I, t_obs, t_ref, G, O, H, M, U, P}
```

where `I` is entity identity, `t_obs` and `t_ref` are observation and reference
epochs, `G` is relational geometry, `O` is origin/axis information, `H` is
handedness, `M` is a meridian or equivalent longitude anchor, `U` is
uncertainty, and `P` is provenance and reconstruction metadata.

This extends the initial `{A, B, t, G, F, U, P}` notation by decomposing frame
information into independently failing origin/axis, handedness, and meridian
components and by separating observation from reference epoch.

## Direction semantics

- North/south is defined by ordering of normalized axial projections relative
  to a **directed** spin axis.
- Relative east/west is the sign of the shortest axial longitude difference
  in a handed three-dimensional space.
- East/west is undefined at an axis pole and for projected antipodes.
- Absolute longitude is not claimed without an independent meridian anchor.
- Geocentric latitude is used for the coordinate-free axial relation.
  Geodetic latitude remains an ellipsoid-dependent coordinate quantity.

## Submission format

- English-only manuscript and figure/table labels.
- Figures and tables are embedded immediately after first citation.
- Figures are also supplied as editable PPTX and high-resolution PNG.
- Tables are also supplied as editable DOCX and CSV.
- Author–year references follow the journal guideline, overriding generic
  numbered-reference preferences.
