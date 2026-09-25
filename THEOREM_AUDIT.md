# Theorem and observable audit

## Assumptions

Let \(X=(x_1,\ldots,x_n)\) be a labeled configuration spanning
\(\mathbb{R}^3\). The analyzed distances are Euclidean chord distances
\(d_{ij}=\lVert x_i-x_j\rVert_2\), not ellipsoidal or spherical surface
geodesic distances. Metric units are known. If units are absent, an additional positive
scale factor remains and the relevant group is the similarity group rather than the
Euclidean group.

Complete exact distances determine the centered Gram matrix and therefore a generic
full-dimensional configuration up to a Euclidean isometry. Centering or an independently
fixed origin removes translation. Entity labels are assumed stable; distances do not
recover entity identity. Epoch and motion-model metadata are separate observables and
are not inferred by the static geometry.

## Residual invariance-group chain

For a retained observable map \(F\), the **residual invariance group** is the
set of transformations \(Q\) satisfying \(F(QX)=F(X)\). It describes
observational equivalence and is not the pointwise stabilizer of a generic
realized configuration.

Under those assumptions, the residual orthogonal ambiguity is

\[
O(3)\ \longrightarrow\ O(2)\ \longrightarrow\ SO(2)\
\longrightarrow\ \{I\}.
\]

1. **Distances and a fixed origin: \(O(3)\).**
   If \(Q\in O(3)\), then
   \(\lVert Qx_i-Qx_j\rVert_2=\lVert x_i-x_j\rVert_2\). The complete
   centered distance matrix therefore cannot distinguish proper rotations from
   reflections.

2. **Directed axis: \(O(2)\).**
   Let \(a\) be a unit directed axis. Its residual invariance group is
   \(G_a=\{Q\in O(3):Qa=a\}\). The restriction of each \(Q\in G_a\) to
   \(a^\perp\) is an arbitrary element of \(O(2)\), and every \(O(2)\)
   transformation of \(a^\perp\) extends by fixing \(a\). Thus \(G_a\cong O(2)\).
   A directed axis fixes axial latitude ordering but does not remove reflections through
   planes containing the axis.

3. **Physical chirality: \(SO(2)\).**
   An independently recoverable chiral witness selects the determinant \(+1\) component
   of \(G_a\). The remaining transformations are proper rotations about \(a\), hence
   \(G_a\cap SO(3)\cong SO(2)\). A stored orientation bit has this effect only when the
   physical interpretation of the bit is independently recoverable. A coordinate
   handedness convention alone is not a physical witness.

4. **Directed meridian: identity.**
   Let \(m\) be a nonzero directed vector in \(a^\perp\). The only axial rotation that
   fixes \(m\) is the zero rotation, so the joint residual invariance group of
   \(a\), physical chirality,
   and \(m\) is \(\{I\}\). Without the chirality condition, the reflection through the
   plane spanned by \(a\) and \(m\) fixes both vectors, so axis plus meridian alone does
   not reduce the residual invariance group to the identity.

## Observable definitions

### Axial latitude ordering

For a nonzero point \(x\) and directed unit axis \(a\), define

\[
\phi_a(x)=\arcsin\left(a^\mathsf{T}x/\lVert x\rVert\right).
\]

The sign of \(\phi_a(x_i)-\phi_a(x_j)\) is called **axial latitude ordering**.
It is a geometric order relative to a directed axis. It is not automatically geodetic
latitude, astronomical latitude, or magnetic latitude:

- geocentric latitude is the angle of the geocentric radius from the equatorial plane;
- geodetic latitude is defined by the reference-ellipsoid normal;
- astronomical latitude is defined by the gravity vertical;
- magnetic latitude is defined from a magnetic-field model;
- axial latitude ordering uses only the stored point vectors and directed axis.

“North/south” is used only when the axis has an independently specified terrestrial or
physical interpretation.

### Signed relative longitude

Project two points onto \(a^\perp\), normalize the projections to \(u_i,u_j\), and define

\[
\Delta\lambda_{ij} =
\operatorname{atan2}\!\left(a^\mathsf{T}(u_j\times u_i),
u_i^\mathsf{T}u_j\right)\in(-\pi,\pi].
\]

The sign is a local or pairwise east/west relation under the selected chirality. It is
not a globally transitive order on the circle.

The implementation reports explicit states:

- `same_meridian`: a defined zero difference;
- `axis_degeneracy`: one projected vector is too small, as at a pole/axis;
- `antipodal`: projected vectors are exactly opposite and neither branch is preferred;
- `near_antipodal`: the sign is declared unstable inside a specified angular tolerance;
- `defined`: a nonzero principal-branch difference.

The branch cut lies at the antipodal projected direction. Consequently, arbitrarily small
perturbations near that cut can reverse the reported sign. This is a property of signed
principal angular differences, not a numerical defect.

## Distance-model boundary

The theoretical and computational results apply to Euclidean chord distances in an
embedding. Surface geodesic distances on a sphere or ellipsoid define a different
distance-geometry problem with different isometries, degeneracies, and reconstruction
methods. No theorem in this project transfers to surface geodesic distances without a
separate proof.

## Incomplete networks

For a graph with edge-length observations, rigidity-matrix rank tests local
identifiability. A generic three-dimensional framework with \(n\geq3\) has at most
\(3n-6\) rank after the six infinitesimal Euclidean gauge freedoms are removed.
Rank \(3n-6\) establishes generic local infinitesimal rigidity for the sampled framework;
it does not establish global rigidity or uniqueness among disconnected embeddings.

## Audit outcome

The previous hierarchy incorrectly described the residual group after fixing a directed
axis as only axial rotations. It omitted the axial-reflection component. The corrected
hierarchy uses \(O(2)\), requires a physical chiral witness before signed relative
longitude is identifiable, and requires a directed meridian to remove the final
\(SO(2)\) ambiguity.
