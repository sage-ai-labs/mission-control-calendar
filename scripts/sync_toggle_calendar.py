#!/usr/bin/env python3
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1evS-9IlR-v94UIVd7J3KcwSxfXo-g6LDnEHJnwqEYBc/export?format=csv&gid=0"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "mission-control.json"


def clean(value):
    return (value or "").strip()


def normalize_row(row):
    return {
        "name": clean(row.get("Feature / Initiative") or row.get("Feature Name")),
        "cat": clean(row.get("Category")),
        "owner": clean(row.get("Owner")),
        "spec": clean(row.get("Spec or Design")),
        "expStart": clean(row.get("Experiment Start")) or None,
        "expEnd": clean(row.get("Experiment End")) or None,
        "launch": clean(row.get("Launch Date")) or None,
        "status": clean(row.get("Status")),
        "pct": clean(row.get("Experiment %")),
        "result": clean(row.get("Results")),
    }


def fetch_rows():
    with urlopen(SHEET_CSV_URL) as response:
        text = response.read().decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    return [normalize_row(row) for row in reader if clean(row.get("Feature / Initiative") or row.get("Feature Name"))]


def write_json(features):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": SHEET_CSV_URL,
        "features": features,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main():
    try:
        features = fetch_rows()
        write_json(features)
        print(f"Wrote {len(features)} features to {OUTPUT_PATH}")
    except Exception as exc:
        print(f"Failed to sync calendar data: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
