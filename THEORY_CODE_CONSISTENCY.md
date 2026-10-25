# Theory–code consistency audit

| Manuscript object | Implementation | Consistent? |
|---|---|---|
| Chord distance d_ij = ||x_i−x_j||_2 | `pairwise_distances` (geometry/core.py) | yes |
| Double centering B = −1/2 J(D∘D)J | `classical_mds`, J = I − 11ᵀ/n, 3 largest positive eigenpairs | yes |
| Centered configuration | Procrustes centers both sets before SVD | yes |
| Metric scale known | No scale parameter estimated in alignment | yes |
| Axial latitude asin[(s·x)/(||s||||x||)] | `axial_latitude` with unit normalization, clip to [−1,1] | yes |
| Signed relative longitude atan2[s·(b⊥×a⊥), a⊥·b⊥] on (−π,π] | `directions.py` atan2 of scalar triple product vs projected dot; pairwise, not transitive | yes |
| Degeneracy states | `LongitudeRelationStatus`: AXIS_DEGENERACY, ANTIPODAL, NEAR_ANTIPODAL, SAME_MERIDIAN (explicit tie) | yes |
| Reflection logic | `procrustes_align(allow_reflection=)`; determinant-constrained Kabsch branch | yes |
| Proper/improper transforms | `random_rotation` enforces det>0; reflection path permits det<0 | yes |
| Local rigidity rank 3n−6 | `target_rank = 3*n_points − 6` in rigidity.py; numerical rank via SVD tolerance max(shape)·eps·σ₁ | yes |
| Gauge modes = 6 | `excess_nullity = 3n − ranks − 6` | yes |
| Edge retention | `sample_graph_edges`: independent Bernoulli on all n(n−1)/2 candidate edges | yes |
| Wilson interval | `_wilson_interval` with z=1.959963984540054, standard center/half-width form | yes |
| ITRF propagation x(t)=x(t_ref)+v(t−t_ref) | itrf.py linear propagation to comparison_epoch (2025.0) | yes |
| Chirality det(Q) sign | `oriented_volume` determinant form; reflection flips det | yes |
