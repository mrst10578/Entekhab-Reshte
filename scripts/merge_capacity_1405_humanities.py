#!/usr/bin/env python3
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path("data/capacity")
NORM = BASE / "normalized/1405"

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def cap(rows):
    return sum(int(r["capacity"]) for r in rows)

def code(row):
    m = re.search(r"کدرشته[\s\u200c]*محل منبع:\s*(\d+)", row.get("notes", ""))
    return m.group(1) if m else ""

def main():
    exp = read_csv(NORM / "capacities-1405-experimental.csv")
    math = read_csv(NORM / "capacities-math.csv")
    hum = read_csv(NORM / "capacities-humanities.csv")

    assert (len(exp), cap(exp)) == (3900, 56662)
    assert (len(math), cap(math)) == (2003, 52310)
    assert (len(hum), cap(hum)) == (2513, 23226)
    assert len({r["major"] for r in hum}) == 20
    assert not any(any(x in (r["university"] + " " + r["program_type"])
                       for x in ("پیام نور", "غیرانتفاعی", "غیر انتفاعی", "غیردولتی")) for r in hum)

    rows = exp + math + hum
    assert (len(rows), cap(rows)) == (8416, 132198)

    rows.sort(key=lambda r: (
        r["major"], r["province"], r["university"], int(r["source_page"] or 0),
        code(r), r["intake"], r["gender"]
    ))
    header = list(rows[0])
    with (NORM / "capacities-all.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    majors = defaultdict(lambda: {"rows": 0, "capacity": 0})
    for row in rows:
        majors[row["major"]]["rows"] += 1
        majors[row["major"]]["capacity"] += int(row["capacity"])

    summary = {
        "year": 1405,
        "status": "complete_supported_groups_1405",
        "rows": len(rows),
        "capacity": cap(rows),
        "groups": {
            "experimental": {"rows": len(exp), "capacity": cap(exp)},
            "math": {"rows": len(math), "capacity": cap(math)},
            "humanities": {"rows": len(hum), "capacity": cap(hum)}
        },
        "majors": dict(sorted(majors.items())),
        "notes": "1405 covers all experimental, math and humanities major families supported by the capacity explorer."
    }
    (NORM / "SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    root_path = BASE / "SUMMARY.json"
    root = json.loads(root_path.read_text(encoding="utf-8"))
    dataset = root["dataset"]
    dataset["years"]["1405"] = {
        "year": 1405,
        "rows": len(rows),
        "capacity": cap(rows),
        "input_files": [
            {"path": "capacities-1405-experimental.csv", "rows": len(exp), "capacity": cap(exp)},
            {"path": "capacities-math.csv", "rows": len(math), "capacity": cap(math)},
            {"path": "capacities-humanities.csv", "rows": len(hum), "capacity": cap(hum)}
        ],
        "coverage": ["experimental", "math", "humanities"],
        "partial": False
    }
    dataset["rows"] = sum(int(v["rows"]) for v in dataset["years"].values())
    dataset["capacity"] = sum(int(v["capacity"]) for v in dataset["years"].values())
    assert (dataset["rows"], dataset["capacity"]) == (41742, 653043)
    root_path.write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sources_path = BASE / "raw/sources.csv"
    sources = sources_path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^1405-humanities-booklet,", sources):
        if not sources.endswith("\n"):
            sources += "\n"
        sources += "1405-humanities-booklet,1405,Ensani.pdf,booklet,دفترچه انتخاب رشته گروه علوم انسانی ۱۴۰۵,dc53d8c1f61bfd2f9fcb6d8d1cf97ea134c46aa140e0ed7129c3a9f50b5b2d06,https://dl.novinkonkor.com/daftarche_entekhab_reshte/1405/Ensani.pdf,فایل در data/raw/sanjesh/humanities/1405/Ensani.pdf نگهداری می‌شود؛ پیام نور و غیرانتفاعی/غیردولتی طبق سیاست پروژه وارد خروجی ابزار نشده‌اند.\n"
        sources_path.write_text(sources, encoding="utf-8")

    meta_path = BASE / "raw/1405/sources.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["humanities"] = {
        "source_id": "1405-humanities-booklet",
        "teacher_source_id": "1405-humanities-teacher-booklet",
        "original_name": "Ensani.pdf",
        "source_repository_path": "data/raw/sanjesh/humanities/1405/Ensani.pdf",
        "pages": 582,
        "sha256": "dc53d8c1f61bfd2f9fcb6d8d1cf97ea134c46aa140e0ed7129c3a9f50b5b2d06",
        "qa": {
            "rows": len(hum),
            "unique_course_location_codes": 2513,
            "major_families": 20,
            "total_capacity": cap(hum),
            "excluded": ["پیام نور", "غیرانتفاعی", "غیردولتی"]
        }
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    humanities_path = BASE / "HUMANITIES_SUMMARY.json"
    hs = json.loads(humanities_path.read_text(encoding="utf-8"))
    hs["years"]["1405"] = {"rows": len(hum), "capacity": cap(hum)}
    h1405 = json.loads((NORM / "HUMANITIES_SUMMARY.json").read_text(encoding="utf-8"))
    for major, values in h1405["majors"].items():
        entries = hs.setdefault("by_major", {}).setdefault(major, [])
        entries[:] = [e for e in entries if int(e.get("year", 0)) != 1405]
        entries.append({
            "year": 1405, "rows": values["rows"], "capacity": values["capacity"],
            "payam_noor_excluded_codes": None, "nonprofit_excluded_codes": None,
            "amendment_code_operations": 0, "applied_amendments": [],
            "before_capacity_discrepancies_resolved_by_latest_explicit_after": [],
            "unresolved": [], "missing_province_rows": 0,
            "status": "extracted_from_1405_booklet"
        })
        entries.sort(key=lambda e: e["year"])
    humanities_path.write_text(json.dumps(hs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "rows_1405": len(rows),
        "capacity_1405": cap(rows),
        "humanities_rows": len(hum),
        "humanities_capacity": cap(hum),
        "dataset_rows": dataset["rows"],
        "dataset_capacity": dataset["capacity"]
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
