#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "gozine2"
TARGET = ROOT / "data" / "rank_admissions"
REPORT_DIR = ROOT / "reports" / "data-system"
YEARS = [1397, 1398, 1399, 1400, 1402]

FIELDS = ["سال","گروه آزمایشی","رتبه کشوری","رتبه در سهمیه","سهمیه","رشته قبولی","دانشگاه قبولی"]
GROUP_ORDER = {"تجربی":0,"ریاضی":1,"انسانی":2,"هنر":3,"زبان":4}
DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩","01234567890123456789")

def txt(v):
    if v is None:
        return ""
    s = str(v).translate(DIGITS).replace("ي","ی").replace("ك","ک").replace("\u200c"," ")
    return re.sub(r"\s+"," ",s).strip()

def as_int_string(v):
    s = txt(v)
    if not s:
        return ""
    try:
        return str(int(float(s)))
    except Exception:
        return s

def quota_norm(v):
    s = txt(v).lower().replace("٪","%")
    s = s.replace("منطقه یک","منطقه 1").replace("منطقه دو","منطقه 2").replace("منطقه سه","منطقه 3")
    s = re.sub(r"منطقه\s*([123])", r"منطقه \1", s)
    s = s.replace("ایثارگران","ایثارگر")
    s = re.sub(r"\s+"," ",s).strip()
    return s

TYPE_WORDS = [
    "روزانه","شبانه","نوبت دوم","پردیس خودگردان","پردیس","آزاد",
    "غیرانتفاعی","پیام نور","شهریه پرداز","شهریه‌پرداز",
    "نیمسال اول","نیمسال دوم","نیمسال 1","نیمسال 2"
]

def major_core(v):
    s = txt(v)
    for w in TYPE_WORDS:
        s = s.replace(w, " ")
    s = re.sub(r"[-–—_/]+"," ",s)
    s = re.sub(r"\s+"," ",s).strip(" ،,")
    return s

def university_norm(v):
    s = txt(v)
    s = s.replace("شهیدبهشتی","شهید بهشتی")
    s = s.replace("خواجه نصیر الدین","خواجه نصیرالدین")
    s = re.sub(r"[-–—_/،,]+"," ",s)
    s = re.sub(r"\s+"," ",s).strip()
    return s

def read_csv(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def strict_key(r):
    return (
        as_int_string(r.get("سال")),
        txt(r.get("گروه آزمایشی")),
        as_int_string(r.get("رتبه در سهمیه")),
        quota_norm(r.get("سهمیه")),
        major_core(r.get("رشته قبولی")),
        university_norm(r.get("دانشگاه قبولی")),
    )

def loose_key(r):
    return (
        as_int_string(r.get("سال")),
        txt(r.get("گروه آزمایشی")),
        as_int_string(r.get("رتبه در سهمیه")),
        major_core(r.get("رشته قبولی")),
        university_norm(r.get("دانشگاه قبولی")),
    )

def sort_key(r):
    rank = as_int_string(r.get("رتبه در سهمیه"))
    country = as_int_string(r.get("رتبه کشوری"))
    q = quota_norm(r.get("سهمیه"))
    qorder = {"منطقه 1":0,"منطقه 2":1,"منطقه 3":2,"ایثارگر-5%":3,"ایثارگر-25%":4}.get(q,9)
    return (
        GROUP_ORDER.get(txt(r.get("گروه آزمایشی")), 9),
        int(rank) if rank.isdigit() else 10**12,
        qorder,
        int(country) if country.isdigit() else 10**12,
        major_core(r.get("رشته قبولی")),
        university_norm(r.get("دانشگاه قبولی")),
    )

def main():
    report = {
        "source": "Gozine2 public historical report-card archive",
        "years": {},
        "totals": defaultdict(int),
        "notes": [
            "Target rank_admissions schema is preserved at seven columns.",
            "Admission type and full Telegram provenance remain in data/raw/gozine2/<year>/admissions.csv.",
            "Existing records are never deleted by this merge.",
            "A matching source row may only fill a blank national rank or blank quota.",
        ],
    }

    for year in YEARS:
        raw_path = RAW / str(year) / "admissions.csv"
        target_path = TARGET / f"rank_to_admission_{year}.csv"

        source = read_csv(raw_path)
        existing = read_csv(target_path)
        rows = [{k: txt(r.get(k,"")) for k in FIELDS} for r in existing]

        strict_map = defaultdict(list)
        loose_map = defaultdict(list)
        for i, r in enumerate(rows):
            strict_map[strict_key(r)].append(i)
            loose_map[loose_key(r)].append(i)

        matched = enriched_country = enriched_quota = added = ambiguous_loose = 0

        for src in source:
            candidate = {
                "سال": as_int_string(src.get("سال")) or str(year),
                "گروه آزمایشی": txt(src.get("گروه آزمایشی")),
                "رتبه کشوری": as_int_string(src.get("رتبه کشوری")),
                "رتبه در سهمیه": as_int_string(src.get("رتبه در سهمیه")),
                "سهمیه": quota_norm(src.get("سهمیه")),
                "رشته قبولی": txt(src.get("رشته قبولی")),
                "دانشگاه قبولی": txt(src.get("دانشگاه قبولی")),
            }

            sk = strict_key(candidate)
            lk = loose_key(candidate)
            matches = strict_map.get(sk, [])

            if not matches:
                loose_matches = loose_map.get(lk, [])
                if len(loose_matches) == 1:
                    idx = loose_matches[0]
                    if not candidate["سهمیه"] or not rows[idx].get("سهمیه"):
                        matches = [idx]
                elif len(loose_matches) > 1 and not candidate["سهمیه"]:
                    ambiguous_loose += 1

            if matches:
                matched += 1
                idx = matches[0]
                old = rows[idx]
                changed = False
                if not as_int_string(old.get("رتبه کشوری")) and candidate["رتبه کشوری"]:
                    old["رتبه کشوری"] = candidate["رتبه کشوری"]
                    enriched_country += 1
                    changed = True
                if not quota_norm(old.get("سهمیه")) and candidate["سهمیه"]:
                    old["سهمیه"] = candidate["سهمیه"]
                    enriched_quota += 1
                    changed = True
                if changed:
                    strict_map[strict_key(old)].append(idx)
                    loose_map[loose_key(old)].append(idx)
                continue

            idx = len(rows)
            rows.append(candidate)
            strict_map[strict_key(candidate)].append(idx)
            loose_map[loose_key(candidate)].append(idx)
            added += 1

        rows.sort(key=sort_key)
        write_csv(target_path, rows)

        yr = {
            "existing_before": len(existing),
            "gozine2_source_rows": len(source),
            "matched_existing": matched,
            "added_new": added,
            "enriched_national_rank": enriched_country,
            "enriched_quota": enriched_quota,
            "ambiguous_loose_matches_not_forced": ambiguous_loose,
            "final_rows": len(rows),
        }
        report["years"][str(year)] = yr
        for k, v in yr.items():
            if isinstance(v, int):
                report["totals"][k] += v

    report["totals"] = dict(report["totals"])
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "GOZINE2_642_MERGE_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# Gozine2 642 merge report",
        "",
        "Public historical Gozine2 report-card records were merged into data/rank_admissions.",
        "The existing seven-column schema was preserved. Full source provenance and admission type remain under data/raw/gozine2/.",
        "",
        "| Year | Existing | Source | Matched | Added | Final |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for y in YEARS:
        r = report["years"][str(y)]
        md.append(f"| {y} | {r['existing_before']} | {r['gozine2_source_rows']} | {r['matched_existing']} | {r['added_new']} | {r['final_rows']} |")
    md += [
        "",
        f"Total source rows: **{report['totals']['gozine2_source_rows']}**",
        f"Matched existing rows: **{report['totals']['matched_existing']}**",
        f"New rows added: **{report['totals']['added_new']}**",
        f"National ranks filled on existing rows: **{report['totals']['enriched_national_rank']}**",
        "",
        "No existing record is deleted by the merge.",
    ]
    (REPORT_DIR / "GOZINE2_642_MERGE_REPORT.md").write_text("\n".join(md)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
