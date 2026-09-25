import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "submission_final"
ARCHIVE = ROOT / "submission" / "journal_of_geodesy_submission_FINAL.zip"


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
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(rows)} final files and ZIP integrity.")


if __name__ == "__main__":
    main()
