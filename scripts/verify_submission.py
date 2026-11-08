import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "submission_final"
ARCHIVE = ROOT / "submission" / "earth_science_informatics_SUBMISSION_FINAL_AUDITED.zip"
AUDIT = ROOT / "submission" / "earth_science_informatics_AUDIT_FINAL.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest_path = FINAL / "MANIFEST.csv"
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    errors = []
    for row in rows:
        path = FINAL / row["file"]
        if not path.is_file():
            errors.append(f"missing: {path}")
            continue
        if path.stat().st_size != int(row["size_bytes"]):
            errors.append(f"size mismatch: {path}")
        if sha256(path) != row["sha256"]:
            errors.append(f"checksum mismatch: {path}")
    expected = {row["file"] for row in rows} | {"MANIFEST.csv"}
    with zipfile.ZipFile(ARCHIVE) as archive:
        corrupt = archive.testzip()
        names = set(archive.namelist())
    if corrupt:
        errors.append(f"corrupt ZIP member: {corrupt}")
    if names != expected:
        errors.append("ZIP members do not match the final manifest")
    with zipfile.ZipFile(AUDIT) as archive:
        if archive.testzip():
            errors.append("corrupt audit ZIP member")
        audit_names = set(archive.namelist())
    for required in ("result_traceability.csv", "results/manuscript_values.csv",
                     "schema/dtrs_relation_record.schema.json", "data/raw/itrf2020/ITRF2020_SLR.SSC.txt"):
        if required not in audit_names:
            errors.append(f"audit ZIP lacks {required}")
    private = {"ADVERSARIAL_REVIEW_ESI.md", "HOSTILE_REVIEW_NOTES.md"}
    if names & private:
        errors.append("private review notes in submission ZIP")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(rows)} final files and ZIP integrity.")


if __name__ == "__main__":
    main()
