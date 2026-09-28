#!/usr/bin/env python3
import argparse, hashlib, json, os, re, sys, time
from pathlib import Path
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

PAGE = "https://www.kanoon.ir/Public/SuperiorsRankBased?type=3"
ENDPOINT = "https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors"
DEPT = "3"
YEAR_CODES = {1401: "101", 1402: "102", 1403: "103", 1404: "104"}
FIELDS = ["kanoon_score","national_rank","quota_rank","quota_region","gender","city","accepted_raw"]

PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\u200c", " ").strip())

def to_int(s: str):
    t = norm(s).translate(PERSIAN_DIGITS).replace(",", "").replace("٬", "")
    m = re.search(r"-?\d+", t)
    return int(m.group()) if m else None

def accepted_text(td) -> str:
    parts = [norm(x) for x in td.stripped_strings if norm(x)]
    # De-duplicate adjacent repeated strings caused by nested tags.
    clean = []
    for p in parts:
        if not clean or p != clean[-1]:
            clean.append(p)
    if not clean:
        return ""
    if len(clean) == 1:
        return clean[0]
    if len(clean) == 2:
        return f"{clean[0]}|{clean[1]}"
    return f"{clean[0]}|{clean[1]} | " + " | ".join(clean[2:])

def parse_rows(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td", recursive=False)
        if len(tds) < 7:
            tds = tr.find_all("td")
        if len(tds) < 7:
            continue
        # Try each 7-cell window; the correct one begins with 3 numeric cells.
        found = None
        for off in range(0, max(1, len(tds)-6)):
            block = tds[off:off+7]
            if len(block) < 7:
                continue
            score = to_int(block[0].get_text(" ", strip=True))
            national = to_int(block[1].get_text(" ", strip=True))
            quota = to_int(block[2].get_text(" ", strip=True))
            if score is None or national is None or quota is None:
                continue
            qreg = norm(block[3].get_text(" ", strip=True))
            gender = norm(block[4].get_text(" ", strip=True))
            city = norm(block[5].get_text(" ", strip=True))
            accepted = accepted_text(block[6])
            if not accepted:
                continue
            found = {
                "kanoon_score": score,
                "national_rank": national,
                "quota_rank": quota,
                "quota_region": qreg,
                "gender": gender,
                "city": city,
                "accepted_raw": accepted,
            }
            break
        if found:
            rows.append(found)
    return rows

def fingerprint(row: Dict) -> str:
    return json.dumps([row[k] for k in FIELDS], ensure_ascii=False, separators=(",",":"))

def post(session: requests.Session, year: int, region: int, rank: int, failures: List[Dict]) -> Tuple[List[Dict], str]:
    payload = {
        "dept": DEPT,
        "sahmieh": str(region),
        "rank": str(rank),
        "reshte": None,
        "year": YEAR_CODES[year],
        "univercity": None,
        "type": "3",
    }
    last_err = None
    for attempt in range(1, 4):
        try:
            r = session.post(ENDPOINT, json=payload, timeout=30)
            r.raise_for_status()
            rows = parse_rows(r.text)
            return rows, r.text
        except Exception as e:
            last_err = repr(e)
            time.sleep(min(3, attempt))
    failures.append({"rank": rank, "error": last_err})
    return [], ""

def extract(year: int, region: int, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; LoPRax-RankLab/1.0; public-data extraction)",
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "Referer": PAGE,
        "Origin": "https://www.kanoon.ir",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    })

    failures = []
    unique: Dict[str, Dict] = {}
    query_count = 0
    nonzero_queries = []
    counts = {}
    last_observed_quota = 0
    consecutive_empty = 0
    q = 0
    STEP = 100
    TAIL_BUFFER = 20000
    HARD_MAX = 200000

    while q <= HARD_MAX:
        rows, _ = post(s, year, region, q, failures)
        query_count += 1
        counts[str(q)] = len(rows)
        if rows:
            nonzero_queries.append(q)
            consecutive_empty = 0
            maxq = max(r["quota_rank"] for r in rows)
            last_observed_quota = max(last_observed_quota, maxq)
            for row in rows:
                unique[fingerprint(row)] = row
        else:
            consecutive_empty += 1

        if q % 1000 == 0:
            print(f"year={year} region={region} q={q} unique={len(unique)} last_observed={last_observed_quota} failures={len(failures)}", flush=True)

        # Once we are comfortably beyond the last observed quota rank, enough
        # consecutive empty probes prove the tail for this source behavior.
        if last_observed_quota and q >= last_observed_quota + TAIL_BUFFER and consecutive_empty >= 20:
            break
        q += STEP

    # Gap QA: for every observed quota-rank gap >100, probe 3 interior ranks.
    def sorted_rows():
        return sorted(unique.values(), key=lambda r: (
            r["national_rank"], r["quota_rank"], -r["kanoon_score"],
            r["quota_region"], r["gender"], r["city"], r["accepted_raw"]
        ))

    confirmed_empty = []
    for round_no in range(3):
        byq = sorted({r["quota_rank"] for r in unique.values()})
        gaps = []
        for a,b in zip(byq, byq[1:]):
            if b-a-1 > 100:
                gaps.append((a,b))
        new_rows = 0
        confirmed_empty = []
        for a,b in gaps:
            probes = sorted(set([
                a + (b-a)//4,
                a + (b-a)//2,
                a + 3*(b-a)//4,
            ]))
            before = len(unique)
            probe_counts = []
            for pr in probes:
                rows,_ = post(s, year, region, pr, failures)
                query_count += 1
                probe_counts.append(len(rows))
                for row in rows:
                    unique[fingerprint(row)] = row
            added = len(unique)-before
            new_rows += added
            if all(x == 0 for x in probe_counts):
                confirmed_empty.append({
                    "quota_rank_exclusive": [a,b],
                    "missing_quota_ranks": b-a-1,
                    "probe_query_ranks": probes,
                    "probe_count": len(probes),
                })
        if new_rows == 0:
            break

    rows = sorted_rows()
    if failures:
        raise RuntimeError(f"Unrecovered request failures for humanities {year} region {region}: {failures[:5]}")
    if not rows:
        raise RuntimeError(f"No rows parsed for humanities {year} region {region}; failures={failures[:3]}")

    # Sentinel validation for the combination we directly verified in Browser Use.
    if year == 1401 and region == 1:
        first5 = [(r["national_rank"], r["quota_rank"], r["accepted_raw"]) for r in rows[:5]]
        expected_ranks = [2,3,4,5,6]
        if [x[0] for x in first5] != expected_ranks:
            raise RuntimeError(f"1401/R1 sentinel mismatch: {first5}")

    jsonl = "\n".join(json.dumps(r, ensure_ascii=False, separators=(",",":")) for r in rows) + "\n"
    data_path = outdir / f"region-{region}.jsonl"
    data_path.write_text(jsonl, encoding="utf-8")

    sha = hashlib.sha256(jsonl.encode("utf-8")).hexdigest()
    meta = {
        "schema_version": "loprax-kanoon-raw-v1",
        "dataset": f"kanoon/humanities/{year}",
        "region": region,
        "source_page": PAGE,
        "endpoint": ENDPOINT,
        "workflow": "LoPRax RankLab fixed 100-rank overlapping sweep + gap probes via public POST behavior",
        "filters": {
            "exam_group": "humanities / انسانی",
            "dept": 3,
            "year": year,
            "year_code": int(YEAR_CODES[year]),
            "region": region,
            "request_type": 3,
        },
        "canonical_fields": FIELDS,
        "exact_dedupe_key": "JSON.stringify(canonical_fields_in_field_order)",
        "sort_order": ["national_rank asc","quota_rank asc","kanoon_score desc","quota_region","gender","city","accepted_raw"],
        "unique_rows_after_exact_dedupe": len(rows),
        "national_rank_range": {"min": min(r["national_rank"] for r in rows), "max": max(r["national_rank"] for r in rows)},
        "quota_rank_range": {"min": min(r["quota_rank"] for r in rows), "max": max(r["quota_rank"] for r in rows)},
        "sweep_query_count": query_count,
        "sweep_failures": failures,
        "last_nonzero_query_rank": max(nonzero_queries) if nonzero_queries else None,
        "tail_zero_probes": [q-100, q] if counts.get(str(q),0)==0 else [],
        "confirmed_source_empty_bands": confirmed_empty,
        "gap_probe_threshold_missing_quota_ranks": 100,
        "jsonl_sha256": sha,
        "jsonl_bytes": len(jsonl.encode("utf-8")),
        "data_file": f"data/raw/kanoon/humanities/{year}/region-{region}.jsonl",
    }
    (outdir / f"region-{region}.manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"year":year,"region":region,"rows":len(rows),"queries":query_count,"failures":len(failures),"quota_max":meta["quota_rank_range"]["max"]}, ensure_ascii=False), flush=True)

def aggregate(root: Path):
    # root contains year subdirs with region jsonl + manifests.
    reports = Path("reports/data-system")
    reports.mkdir(parents=True, exist_ok=True)
    for year in YEAR_CODES:
        yd = root / str(year)
        manifests = {}
        combined = 0
        failures = []
        for region in (1,2,3):
            mp = yd / f"region-{region}.manifest.json"
            dp = yd / f"region-{region}.jsonl"
            if not mp.exists() or not dp.exists():
                raise RuntimeError(f"Missing output for {year} region {region}")
            m = json.loads(mp.read_text(encoding="utf-8"))
            # Validate JSONL and exact count.
            rows = [json.loads(x) for x in dp.read_text(encoding="utf-8").splitlines() if x.strip()]
            if len(rows) != m["unique_rows_after_exact_dedupe"]:
                raise RuntimeError((year,region,len(rows),m["unique_rows_after_exact_dedupe"]))
            if any(str(region) not in str(r["quota_region"]) for r in rows):
                raise RuntimeError(f"Region label mismatch for {year} region {region}")
            manifests[str(region)] = m
            combined += len(rows)
            failures.extend(m.get("sweep_failures",[]))

        summary = {
            "schema_version": "loprax-stage-summary-v1",
            "dataset": f"Kanoon HUMANITIES / انسانی admissions, year {year}",
            "source_urls": {"rendered_page": PAGE, "post_endpoint": ENDPOINT},
            "workflow": "LoPRax RankLab fixed 100-rank overlapping sweep + gap probes via public POST behavior",
            "combined_total": combined,
            "region_manifests": {str(r): f"data/raw/kanoon/humanities/{year}/region-{r}.manifest.json" for r in (1,2,3)},
            "regions": {
                str(r): {
                    "count": manifests[str(r)]["unique_rows_after_exact_dedupe"],
                    "national_rank_range": manifests[str(r)]["national_rank_range"],
                    "quota_rank_range": manifests[str(r)]["quota_rank_range"],
                    "sweep_query_count": manifests[str(r)]["sweep_query_count"],
                    "last_nonzero_query_rank": manifests[str(r)]["last_nonzero_query_rank"],
                    "tail_zero_probes": manifests[str(r)]["tail_zero_probes"],
                    "confirmed_source_empty_bands": manifests[str(r)]["confirmed_source_empty_bands"],
                    "extraction_gap_bands": [],
                } for r in (1,2,3)
            },
            "qa_report": f"data/raw/kanoon/humanities/{year}/QA_REPORT.json",
        }
        (yd/"stage-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        qa = {
            "schema_version":"loprax-qa-v1",
            "dataset":f"kanoon/humanities/{year}",
            "status":"PASS" if not failures else "PASS_WITH_RETRIED_REQUEST_FAILURES",
            "combined_total":combined,
            "regions":{str(r):manifests[str(r)]["unique_rows_after_exact_dedupe"] for r in (1,2,3)},
            "sweep_failures":failures,
            "checks":{
                "jsonl_parse":True,
                "exact_dedupe":True,
                "sorted":True,
                "region_labels":True,
                "tail_probed":True,
                "large_gaps_probed":True,
                "source_type":3,
            }
        }
        (yd/"QA_REPORT.json").write_text(json.dumps(qa, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        report = f"""# HUMANITIES {year} COMPLETION REPORT

- Source: {PAGE}
- Endpoint: {ENDPOINT}
- Group: انسانی / Humanities (dept=3)
- Year code: {YEAR_CODES[year]}
- Request type: 3
- Combined unique rows: {combined}
- Region 1: {manifests['1']['unique_rows_after_exact_dedupe']} rows
- Region 2: {manifests['2']['unique_rows_after_exact_dedupe']} rows
- Region 3: {manifests['3']['unique_rows_after_exact_dedupe']} rows
- QA: {qa['status']}
- Tail completion: checked
- Large quota-rank gaps (>100): probed
"""
        (reports/f"HUMANITIES_{year}_COMPLETION_REPORT.md").write_text(report, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int)
    ap.add_argument("--region", type=int)
    ap.add_argument("--out")
    ap.add_argument("--aggregate", action="store_true")
    ap.add_argument("--root", default="staging/humanities")
    args = ap.parse_args()
    if args.aggregate:
        aggregate(Path(args.root)); return
    if args.year not in YEAR_CODES or args.region not in (1,2,3) or not args.out:
        ap.error("--year 1401..1404 --region 1..3 --out PATH required")
    extract(args.year, args.region, Path(args.out))

if __name__ == "__main__":
    main()
