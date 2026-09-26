# Kanoon Mathematics 1403 LoPRax RankLab Completion Report

## Scope
Source rendered page: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3
Source POST endpoint: https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors

Parameters used: `dept=1` (mathematics / گروه ریاضی), `year=103` (admissions year 1403), `type=3`, and each `sahmieh` value 1, 2, and 3 independently.

The extraction used the page's public rendered behavior and same-origin POST response. No CAPTCHA, anti-bot, authentication, or access-control bypass was used. All observed POST responses were HTTP 200.

## Final Findings

| Region | Exact-unique rows | National-rank range | Quota-rank range | Raw returned rows |
|---:|---:|---:|---:|---:|
| 1 | 406 | 1–107937 | 1–37207 | 1917 |
| 2 | 889 | 5–99168 | 1–39994 | 3831 |
| 3 | 516 | 4–98961 | 1–24055 | 2329 |
| **Combined** | **1811** | — | — | **8077** |

Exact deduplication used all seven canonical fields: `kanoon_score`, `national_rank`, `quota_rank`, `quota_region`, `gender`, `city`, and `accepted_raw`.

## Empty Bands and Tail

The sweep was adaptive and overlapping: it used dense low-rank probes and 5% growth at higher query ranks, then targeted the largest apparent quota-rank gaps at three interior points each. All 45 targeted gap probes per region returned rows and produced zero new exact-unique rows. These numeric gaps are therefore treated as sparse source coverage or broad endpoint windows, not extraction gaps.

Region 1: max returned quota rank 37207; required higher zero probes at query ranks 41500, 42000; sampled source-empty tail points 41500, 42000, 42500, 43280, 45444.
Region 2: max returned quota rank 39994; required higher zero probes at query ranks 44500, 45000; sampled source-empty tail points 44500, 45000, 45444, 47717.
Region 3: max returned quota rank 24055; required higher zero probes at query ranks 26800, 27200; sampled source-empty tail points 26800, 27200, 27600, 27896, 29291.

These tail bands are confirmed empty at the listed public query points. The report deliberately does not overclaim that every integer query rank in a band was independently requested.

## Representative QA

Sampling QA, not a full independent audit: five fresh query points per region were checked at low, low-mid, mid, high, and near-tail ranks. Every QA response was HTTP 200, non-empty, canonically mapped, and represented in the final exact-deduped set.

QA result: **PASS**.

## Deterministic Artifacts

JSONL rows are UTF-8, newline-delimited canonical JSON with deterministic ordering. Manifests contain byte counts, SHA-256 hashes, row fingerprints, row-key fingerprints, query-log fingerprints, and extraction statistics.

- Region 1: be43791a2a9d82b64a473c6f9b9a5225abdba2a32efa613fe48f9524501c0a08 (88966 bytes, 406 rows).
- Region 2: 3ce546a2d0fc43d7fe97575ebca7bc0e7c078b75c5914c369a0123f8e64eafbe (193851 bytes, 889 rows).
- Region 3: 8de1e5f81e9ea5e4c9068c90cf0e6d8726ea3ba9cc99f4168eb2ca979a84b35a (113985 bytes, 516 rows).

The repo-ready tree is under `outputs/repo-ready-math-1403/`. TSV exports are under `outputs/math-1403-region-{1,2,3}.tsv`.
