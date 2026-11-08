# Earth Science Informatics (Springer Nature, ISSN 1865-0473 / 1865-0481) — verified requirements

All items were read from official Springer Nature pages captured on 2026-11-06 (UTC) through a
rendered browser session (direct HTTPS returns a JavaScript client challenge). Captures, SHA-256
and sizes are in `data/raw/journal_esi/` and `data/data_acquisition_log.csv` (private audit copy;
not redistributed in the public mirror).

| Source | URL | Accessed (UTC) |
|---|---|---|
| Home | https://link.springer.com/journal/12145 | 2026-11-06T05:55:12Z |
| Aims and scope | https://link.springer.com/journal/12145/aims-and-scope | 2026-11-06T05:55:05Z |
| Submission guidelines | https://link.springer.com/journal/12145/submission-guidelines | 2026-11-06T05:54:59Z |
| Editorial board | https://link.springer.com/journal/12145/editorial-board | 2026-11-06T05:55:25Z |
| Publishing model page | https://link.springer.com/journal/12145/publishing-model | 2026-11-06T05:55:18Z (returned "Page Not Found"; model taken from Home page) |

## Scope

- ESI covers formal and computational methods, computational Earth science, spatial and temporal
  analyses, and computer applications to the acquisition, storage, processing, interchange and
  visualization of Earth-system and space-science data.
- The aims page states that the principal contribution must be to Earth science informatics;
  pure GIS applications or domain studies without an informatics contribution may be out of scope.
- Fit consequence: a manuscript whose novelty is only the geodetic identifiability argument (the
  JoG version) is not in scope. The submission must lead with a data-interchange/preservation
  contribution that is implemented and tested (record model, validator, recoverability decoder,
  benchmark). Verdict: compatible only after that pivot.

## Article type

| Type | Official requirement | Decision |
|---|---|---|
| Research article | Introduction, Methods, Results, Discussion, Conclusions (alternative structure allowed) | — |
| Methodology article | Method detail sufficient to reproduce and apply; computational methods may use Algorithm / Testing / Implementation subsections; theoretical work needs comparison of existing vs new | **Selected** |
| Software article | Mandatory "Software Files", "Design and Implementation", "Availability and Requirements" sections | Not selected (the contribution is a record model plus recoverability semantics, not a stand-alone tool) |

## Formatting and front matter

| Item | Official requirement | Status in package |
|---|---|---|
| Abstract | 150–250 words, no undefined abbreviations or unspecified references | checked by `tests/test_qc.py` |
| Keywords | 4–6 | checked by test |
| Title page | title, author names, affiliations, e-mail of corresponding author, ORCID if available | affiliation/ORCID pending user (`FINAL_USER_INPUT_REQUIRED.md`) |
| Text | Word (.docx), normal plain font (e.g. 10-pt Times Roman), automatic page numbering, equation editor, ≤3 heading levels, footnotes not endnotes | builder output |
| Editable sources | All editable source files must be supplied at every submission; otherwise not reviewed | DOCX + editable figures/tables included |
| Word / figure / table / reference limits | **No numerical limit stated** on the captured pages (only "Comments" are limited to 1000 words) | NOT APPLICABLE |
| Citations | Author–year in text; alphabetical reference list; full DOI links; LTWA abbreviations or full titles | builder output |
| Tables | Arabic numerals, cited consecutively, caption above, footnotes with superscript lower-case letters | builder output |
| Figures | "Fig." + number in bold, no punctuation after number or at end of caption; captions in the text file; figures within the body of the text; separate files named Fig1, Fig2…; EPS/TIFF preferred, MS Office acceptable; combination art ≥600 dpi; ≤174 mm wide, ≤234 mm high; Helvetica/Arial lettering; no titles inside figures; patterns as well as colour; colour free online | builder output |
| Supplementary | Cited as "Online Resource N"; files named ESM_N.ext; text as PDF; each file carries title, journal name, author names, affiliation and e-mail of corresponding author | builder output |
| Statements and Declarations | Under that heading: Funding, Competing interests, Ethics approval, Consent, Data availability, Code availability (as applicable), Author contributions | Funding/competing-interest wording pending user |
| Data availability | Mandatory for original research articles (Springer Nature research data policy); repository deposit strongly encouraged; data citations recommended | public repository + checksummed raw input |
| LLM / AI disclosure | LLMs cannot be authors; LLM use must be documented in the Methods section; AI-assisted copy editing need not be declared | declared in Methods |
| ORCID | recommended | pending user |

## Publication model and fees

- Home page: publishing model **Hybrid**. Subscription publication has no mandatory APC;
  colour online is free.
- Open Choice (optional open access) carries an APC; the captured guideline states that "APCs vary
  by journal" and links to a list. The exact ESI APC amount was **NOT VERIFIED** in this session.

## Metrics (informational only; not used for the decision)

- Home page (Springer): Journal Impact Factor 4.2 (2025); 5-year JIF 3.8 (2025); median 7 days
  submission to first decision.
- JCR category and quartile: **NOT VERIFIED** (Clarivate JCR not accessible). SCImago quartile is
  not used as a substitute.

## Verdict

ESI is compatible with the pivoted contribution (methodology article on an implemented,
tested data model for interchange/preservation of time-indexed spatial relations). It is not
compatible with the JoG manuscript re-titled. No silent journal change.
