"""Regenerate references_verified.csv from the cited reference list and persisted metadata."""

import csv
import json
import re
import unicodedata
from pathlib import Path

import esi_content as esi

ROOT = Path(__file__).resolve().parents[1]
CROSSREF_DIRECTORIES = [ROOT / "data/raw/literature", ROOT / "data/raw/literature_esi"]
STANDARD_SNAPSHOTS = {
    "ISO (2014)": "data/raw/standards/iso_19115-1_2014.html",
    "ISO (2019)": "data/raw/standards/iso_19111_2019.html",
    "ISO (2023)": "data/raw/standards/iso_19157-1_2023.html",
    "OGC (2019)": "data/raw/standards/ogc_18-005r5_topic2.html",
    "OGC (2024)": "data/raw/standards/ogc_geosparql_1.1.html",
    "W3C (2013)": "data/raw/standards/w3c_prov-o.html",
    "W3C (2022)": "data/raw/standards/w3c_owl-time.html",
    "PROJ (2023)": "data/raw/standards/projjson_spec.html",
    "CCSDS (2024)": "data/raw/standards/ccsds_650.0-m-3.pdf",
}
PREVIOUS = ROOT / "references_verified.csv"


def crossref_index() -> dict[str, tuple[Path, dict]]:
    index = {}
    for directory in CROSSREF_DIRECTORIES:
        for path in sorted(directory.glob("crossref_*.json")):
            try:
                message = json.loads(path.read_text(encoding="utf-8"))["message"]
            except (ValueError, KeyError):
                continue
            index[message["DOI"].lower()] = (path, message)
    return index


def main() -> None:
    index = crossref_index()
    previous = {}
    if PREVIOUS.exists():
        with PREVIOUS.open(encoding="utf-8") as handle:
            previous = {row["url"]: row for row in csv.DictReader(handle)}
    rows = []
    for reference in esi.REFERENCES:
        head = reference.split(")")[0] + ")"
        year = re.search(r"\((\d{4})\)", reference).group(1)
        first = unicodedata.normalize("NFKD", head.split(" ")[0]).encode("ascii", "ignore").decode()
        key = re.sub(r"[^a-z0-9]", "", first.lower()) + year
        url = reference.rsplit(" ", 1)[-1]
        doi = url.removeprefix("https://doi.org/").lower() if "doi.org" in url else ""
        row = {"key": key, "year": year, "doi": doi, "url": url, "cited_for": "", "reference": reference}
        if doi and doi in index:
            path, message = index[doi]
            row["title"] = message["title"][0]
            row["container"] = (message.get("container-title") or [""])[0]
            row["verification_source"] = f"Crossref metadata {path.relative_to(ROOT)}"
            row["verified_utc"] = re.search(r"(\d{4}-\d{2}-\d{2})", path.name).group(1) if re.search(r"(\d{4}-\d{2}-\d{2})", path.name) else ""
        elif head in STANDARD_SNAPSHOTS:
            row["verification_source"] = f"Official page snapshot {STANDARD_SNAPSHOTS[head]}"
        elif url in previous:
            row["verification_source"] = previous[url]["verification_source"]
            row["verified_utc"] = previous[url]["verified_utc"]
        else:
            raise SystemExit(f"Unverified reference: {reference}")
        rows.append(row)
    keys = [row["key"] for row in rows]
    for row in rows:
        if keys.count(row["key"]) > 1:
            row["key"] += re.sub(r"[^a-z]", "", row["reference"].split("(")[0].split(",")[1].lower())[:4] if "," in row["reference"].split("(")[0] else ""
    columns = ["key", "year", "title", "container", "doi", "url", "verification_source", "verified_utc", "reference"]
    with PREVIOUS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} verified references")


if __name__ == "__main__":
    main()
