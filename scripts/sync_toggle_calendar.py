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


def first_field(row, *aliases):
    for alias in aliases:
        value = clean(row.get(alias))
        if value:
            return value
    return ""


def normalize_row(row):
    return {
        "name": first_field(row, "Feature / Initiative", "Feature Name", "Initiative", "Feature"),
        "cat": first_field(row, "Category", "Type"),
        "owner": first_field(row, "Owner"),
        "builders": first_field(row, "Builders", "Builder", "Engineer", "Engineers"),
        "spec": first_field(row, "Spec or Design", "Spec", "Design"),
        "notes": first_field(row, "Notes", "Note"),
        "expStart": first_field(row, "Experiment Start", "Exp Start") or None,
        "expEnd": first_field(row, "Experiment End", "Exp End") or None,
        "launch": first_field(row, "Launch Date", "Launch") or None,
        "status": first_field(row, "Status"),
        "pct": first_field(row, "Experiment %", "Exp %"),
        "result": first_field(row, "Results", "Result"),
    }


def fetch_rows():
    with urlopen(SHEET_CSV_URL) as response:
        text = response.read().decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    rows = [normalize_row(row) for row in reader]
    return [
        row for row in rows
        if row["name"] and (
            row["status"]
            or row["launch"]
            or row["expStart"]
            or row["expEnd"]
            or row["spec"]
            or row["owner"]
            or row["builders"]
            or row["notes"]
        )
    ]


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
