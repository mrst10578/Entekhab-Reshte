# Kanoon Mathematics 1402 Admissions Completion Report

Retrieved: `2026-09-26T08:39:16Z`

## Scope

- Exam group: mathematics / ریاضی (`dept=1`).
- Year: 1402 (`year=102`).
- Quota regions: 1, 2, and 3 independently.
- Canonical fields: `kanoon_score`, `national_rank`, `quota_rank`, `quota_region`, `gender`, `city`, `accepted_raw`.

## Sources

- Rendered page: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3
- Public POST endpoint used by `ShowSuperiors()`: https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors
- The page's own same-origin POST behavior was used. No CAPTCHA, anti-bot, or access-control bypass was attempted.

## Completion

The adaptive overlapping sweep used the public rank query with a maximum center step of 150. The observed response window is `max(100, 10% of query rank)`, so adjacent queries overlap. Each region continued until two higher query ranks returned valid 200/source-empty responses whose lower window bound was above the final observed quota rank.

| Region | Exact rows | Quota-rank range | National-rank range | Queries | Tail zero probes | Extraction gaps |
|---:|---:|---:|---:|---:|---|---:|
| 1 | 408 | 1-28341 | 1-76867 | 372 | 31601, 31676 | 0 |
| 2 | 721 | 1-33211 | 2-84201 | 394 | 37026, 37101 | 0 |
| 3 | 409 | 1-29279 | 5-449959 | 381 | 32626, 32701 | 0 |

Combined exact-deduped total: **1538** rows.

## Confirmed Source-Empty Bands

These are the three largest rank gaps per region. The full list of observed gaps is in `math-1402-summary.json`. The selected bands were checked by the complete overlapping sweep and three targeted overlapping probes each; every probe returned zero rows whose `quota_rank` was strictly inside the stated boundaries. Boundary rows may still appear because the public endpoint's query window overlaps the band.

| Region | Empty quota-rank band | Missing ranks | Probe ranks |
|---:|---:|---:|---|
| 1 | 23464-28340 | 4877 | 24500, 26000, 27500 |
| 1 | 19155-21410 | 2256 | 19500, 20250, 21000 |
| 1 | 13654-15719 | 2066 | 13800, 14650, 15550 |
| 2 | 26791-30477 | 3687 | 27000, 28600, 30200 |
| 2 | 12753-14406 | 1654 | 12900, 13550, 14250 |
| 2 | 16414-17988 | 1575 | 16550, 17200, 17850 |
| 3 | 24233-29278 | 5046 | 24500, 26600, 29100 |
| 3 | 19361-21769 | 2409 | 19500, 20550, 21600 |
| 3 | 16816-18879 | 2064 | 17000, 17850, 18750 |

No extraction gap was observed after normalization: HTTP 200 responses with the known 1,347-byte no-row response shell are classified as valid source-empty responses, not parser failures.

## Tail-Zero Probes

Region 1: rank 31601 (HTTP 200, 1347 bytes, 0 rows, lower-bound estimate 28440.9); rank 31676 (HTTP 200, 1347 bytes, 0 rows, lower-bound estimate 28508.4).
Region 2: rank 37026 (HTTP 200, 1347 bytes, 0 rows, lower-bound estimate 33323.4); rank 37101 (HTTP 200, 1347 bytes, 0 rows, lower-bound estimate 33390.9).
Region 3: rank 32626 (HTTP 200, 1347 bytes, 0 rows, lower-bound estimate 29363.4); rank 32701 (HTTP 200, 1347 bytes, 0 rows, lower-bound estimate 29430.9).

## Representative QA

This is sampling QA, not a full independent audit: five queries per region at low, low-mid, mid, high, and near-tail ranks. All 15 queries returned HTTP 200, parsed successfully, had no duplicate sample rows, and every returned canonical row was present in the corresponding full sweep.

| Region | Label | Query rank | Returned rows | HTTP | Subset of sweep |
|---:|---|---:|---:|---:|---|
| 1 | low | 1 | 82 | 200 | yes |
| 1 | low-mid | 5000 | 10 | 200 | yes |
| 1 | mid | 15000 | 5 | 200 | yes |
| 1 | high | 22000 | 2 | 200 | yes |
| 1 | near-tail | 28000 | 1 | 200 | yes |
| 2 | low | 1 | 120 | 200 | yes |
| 2 | low-mid | 5000 | 18 | 200 | yes |
| 2 | mid | 15000 | 12 | 200 | yes |
| 2 | high | 25000 | 6 | 200 | yes |
| 2 | near-tail | 33000 | 3 | 200 | yes |
| 3 | low | 1 | 96 | 200 | yes |
| 3 | low-mid | 5000 | 7 | 200 | yes |
| 3 | mid | 15000 | 6 | 200 | yes |
| 3 | high | 24000 | 2 | 200 | yes |
| 3 | near-tail | 29000 | 1 | 200 | yes |

## Output Files

The repo-ready tree is under `outputs/repo-ready-math-1402/`. JSONL files are UTF-8, one compact canonical JSON object per line, sorted by quota rank and then the documented tie-breakers. Manifests contain exact byte sizes, SHA-256 hashes, row counts, and deterministic row-key fingerprints.

| Path | Bytes | SHA-256 where applicable |
|---|---:|---|
| `data/raw/kanoon/math/1402/region-1.jsonl` | 69874 | `6d03d78cb2947758ac7777c63f4a1c5f4cadbd055d9325961bcc594d79d798fe` |
| `data/raw/kanoon/math/1402/region-1.manifest.json` | 4334 | manifest metadata |
| `data/raw/kanoon/math/1402/region-2.jsonl` | 124266 | `b717a67a3aa966ab1cc3743a3865532db095347dbe34078b4abff56e0d5cc194` |
| `data/raw/kanoon/math/1402/region-2.manifest.json` | 4335 | manifest metadata |
| `data/raw/kanoon/math/1402/region-3.jsonl` | 71145 | `9d76d5602b6a873dc86889a1899f36f081fda3aa9d6f02d9be00c589c3daee10` |
| `data/raw/kanoon/math/1402/region-3.manifest.json` | 4335 | manifest metadata |
| `data/raw/kanoon/math/1402/stage-summary.json` | 8232 | summary metadata |
| `data/raw/kanoon/math/1402/QA_REPORT.json` | 5576 | QA metadata |
| `reports/data-system/MATH_1402_COMPLETION_REPORT.md` | 5249 | this report |

Validation status: **PASS**.
