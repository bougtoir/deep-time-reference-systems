import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = ROOT / "data" / "data_acquisition_log.csv"
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    errors = []
    skipped = []
    for row in rows:
        path = ROOT / row["saved_path"]
        if not path.exists():
            if row["repository_distribution"] == "local snapshot only":
                skipped.append(str(path))
                continue
            errors.append(f"missing: {path}")
            continue
        if str(path.stat().st_size) != row["file_size_bytes"]:
            errors.append(f"size mismatch: {path}")
        if sha256(path) != row["sha256"]:
            errors.append(f"checksum mismatch: {path}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(rows) - len(skipped)} raw source snapshots.")
    if skipped:
        print(f"Skipped {len(skipped)} non-distributed local snapshots.")


if __name__ == "__main__":
    main()
