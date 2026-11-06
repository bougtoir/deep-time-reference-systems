# Journal of Geodesy requirements audit

Current official snapshots were retrieved on 2026-09-25 and preserved under
`data/raw/journal/`. The applicable requirements are:

| Requirement | Verified policy | Required package action |
|---|---|---|
| Editable source | Manuscript text must be supplied as DOCX or LaTeX, with relevant editable sources at submission and revision. | Include manuscript DOCX, editable figure PPTX, table DOCX, and supplement DOCX. PDF files are viewing companions, not substitutes. |
| Title page | Concise title and complete author information are required; acknowledgments and full funder names belong on the title page. | Keep a separate editable title page. Leave affiliation, ORCID, funding, and corresponding-author details as explicit placeholders for local completion; do not invent them. |
| Abstract | 150–250 words; no undefined abbreviations or unspecified references. | Enforce word count in the build checks. |
| Keywords | Four to six indexing keywords. | Generate five or six keywords. |
| Declarations | Relevant statements must appear under “Statements and Declarations”; incomplete declarations may be returned. | Include funding, competing interests, author contributions, data availability, code availability, and AI disclosure. |
| Data availability | All original research requires a data availability statement describing access to supporting input and generated data. | Cite the official ITRF source, repository/reproducibility bundle, checksums, and generated result files. |
| Author contribution | Journal policy requires an author contribution statement. | Include a single-author CRediT-style statement, subject to local author approval. |
| Figures and tables | Follow artwork/table instructions and supply editable/high-quality files. | Provide separate figure files and editable PPTX; provide tables as editable DOCX/CSV. Cite every figure and table in text. |
| Supplementary information | Supplementary files may accompany the article and must be identified consistently. | Supply editable and PDF supplement with a manifest. |
| References | Reference list includes only cited published/accepted works, is alphabetical by first author, and uses full DOI links where available. | Use author–year citations and an alphabetical list; do not impose Vancouver numbering on this journal style. |
| AI use | LLMs cannot be authors. Generative-AI use must be transparently disclosed with the tool/version, usage dates, prompts, extent of contribution, human review, and accountability. | Disclose Devin as a versionless web service, the 24–25 September 2026 usage dates, prompt purposes, the assisted tasks, deterministic code-based figures and results, and the author's verification and responsibility. |
| Early-career award | The cover letter should indicate whether the first author meets the journal's early-career criterion if the author seeks consideration. | Leave an optional explicit placeholder; do not infer age or status. |

The official sources used are the Journal of Geodesy submission guidelines, journal
aims and scope, the journal editorial-policy article describing author-contribution and
data-availability requirements, the journal submission guidelines, and the Springer
Nature AI guidance for researchers. Checksums and retrieval details are in
`data/data_acquisition_log.csv`.
