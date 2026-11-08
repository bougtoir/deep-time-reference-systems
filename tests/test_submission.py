import hashlib
import zipfile
from pathlib import Path

import pandas as pd
from docx import Document


ROOT = Path(__file__).resolve().parents[1]


def test_verified_references_have_unique_keys_and_urls() -> None:
    references = pd.read_csv(ROOT / "references_verified.csv")
    assert references["key"].is_unique
    assert references["url"].str.startswith("http").all()
    assert references["verification_source"].notna().all()


def test_manuscript_contains_all_cited_figures_and_tables() -> None:
    document = Document(ROOT / "manuscript/manuscript.docx")
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    assert len(document.inline_shapes) == 6
    assert len(document.tables) == 4
    for number in range(1, 7):
        assert f"Fig. {number}" in text
    for number in range(1, 5):
        assert f"Table {number}" in text
    assert "Earth Science Informatics" in text
    assert "Journal of Geodesy" not in text
    abstract = next(
        document.paragraphs[index + 1].text
        for index, paragraph in enumerate(document.paragraphs)
        if paragraph.text == "Abstract"
    )
    assert 150 <= len(abstract.split()) <= 250
    keywords = next(
        paragraph.text.removeprefix("Keywords: ")
        for paragraph in document.paragraphs
        if paragraph.text.startswith("Keywords: ")
    )
    assert 4 <= len(keywords.split("; ")) <= 6
    for heading in ["Statements and Declarations", "Data availability", "Code availability",
                    "Competing interests", "Funding", "Author contributions"]:
        assert heading in text
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            assert "\n" not in run.text and "\r" not in run.text


def test_submission_archive_and_manifest_exist() -> None:
    archive_path = ROOT / "submission/earth_science_informatics_SUBMISSION_FINAL_AUDITED.zip"
    manifest = pd.read_csv(ROOT / "submission_final/MANIFEST.csv")
    assert manifest["sha256"].str.len().eq(64).all()
    for row in manifest.itertuples():
        path = ROOT / "submission_final" / row.file
        assert path.stat().st_size == row.size_bytes
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row.sha256
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
    assert names == set(manifest["file"]) | {"MANIFEST.csv"}
    for name in ["manuscript_clean.docx", "manuscript_clean.pdf", "ESM_1.pdf", "ESM_2.zip",
                 "cover_letter_final.docx", "declarations.docx", "title_page.docx",
                 "figures_editable.pptx", "tables_editable.docx"]:
        assert name in names, name
    assert {f"figures/Fig{index}.png" for index in range(1, 7)} <= names
    assert not any("ADVERSARIAL" in name or "HOSTILE" in name for name in names)
    with zipfile.ZipFile(ROOT / "submission_final/ESM_2.zip") as archive:
        esm = set(archive.namelist())
    assert "schema/dtrs_relation_record.schema.json" in esm
    assert "examples/records/intact_E.json" in esm
    assert "results/manuscript_values.csv" in esm
    audit = ROOT / "submission/earth_science_informatics_AUDIT_FINAL.zip"
    with zipfile.ZipFile(audit) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
    for name in ["data/raw/itrf2020/ITRF2020_SLR.SSC.txt",
                 "data/raw/literature/crossref_asimow_roth_1978_2026-09-25.json",
                 "scripts/run_pipeline.py", "scripts/build_submission.py",
                 "scripts/verify_submission.py", "src/dtrs/records/decode.py",
                 "result_traceability.csv", "references_verified.csv"]:
        assert name in names, name
