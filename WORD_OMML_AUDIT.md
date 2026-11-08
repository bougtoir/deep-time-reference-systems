# Word OMML audit

Audit date: 2026-10-25

## Result

`manuscript_inline.docx` (built as `manuscript/manuscript.docx`, copied into the
submission): **90 `<m:oMath>` elements** — previously 0. All equations are true
OMML (editable in Microsoft Word), produced by `scripts/docx_math.py` from
LaTeX spans embedded in the builder prose and converted via
`latex2mathml` + `docx-equation` (both pinned in `pyproject.toml`).

## Expression coverage

| Required expression | Status |
|---|---|
| d_ij = ‖x_i − x_j‖₂ | OMML (`d_{ij}=\|x_i-x_j\|_2`) |
| φ_s(x) = asin[(s·x)/(‖s‖‖x‖)] | OMML (`\phi_s(x)=\arcsin\frac{s\cdot x}{\|s\|\|x\|}`) |
| signed-relative-longitude atan2 | OMML (`\operatorname{atan2}[s·(b_⊥×a_⊥), a_⊥·b_⊥]`) |
| principal branch (−π, π] | OMML, restated as `−π < λ ≤ π` (see note) |
| E = {I, t_obs, t_ref, G, O, C, M, U, P} | OMML |
| X = [x_1,…,x_n]^T | OMML (`\left[…\right]^{\mathsf{T}}`) |
| d_ij = ‖x_i − x_j‖ | OMML |
| B = −½J(D∘D)J, J = I − 11^T/n | OMML |
| XQ + 1c^T | OMML |
| F(QX) = F(X) | OMML |
| O(3)→O(2)→SO(2)→{I} | OMML (`\to`) |
| O(3), O(2), SO(2), {I} in formal relations | OMML in theory section + abstract |
| det(Q) | OMML (`\det(Q)`); `O(3)\setminus SO(3)` OMML |
| (Qs)·(Qx) = s·x | OMML |
| rank 3n − 6 | OMML |
| x(t) = x(t_ref) + v(t − t_ref) + d(t) | OMML |

Ordinary prose numbers, years, units and abbreviations were left as text.
The supplement contains no display equations — its mathematical content is
descriptive prose and was deliberately not converted.

## Rendering check

LibreOffice PDF export re-checked page by page; all equations render.
Note: two constructs initially exported as a placeholder glyph under
LibreOffice's OMML import (mismatched `(` … `]` delimiters and `[]^{T}`
superscript). They were rewritten to renderer-safe equivalents
(`−π < λ ≤ π`; `\left[…\right]^{\mathsf{T}}`) — mathematically identical.

PASS — Word-native OMML present; every identified expression is OMML or
explicitly prose.
