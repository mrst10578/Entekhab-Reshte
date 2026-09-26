# MATH 1404 Kanoon Completion Report

Generated: 2026-09-26T08:33:42.140Z

## Scope

- Exam group: mathematics / ریاضی (`dept=1`).
- Year: 1404 (`year=104`).
- Regions: 1, 2, and 3 independently.
- Source page: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3
- POST endpoint: https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors

## Method

The public rendered page was loaded normally and its own POST behavior was used. The response HTML table was parsed for the seven canonical fields. No CAPTCHA, anti-bot, or access-control bypass was used; all observed responses were public HTTP 200 page responses.

LoPRax RankLab coverage used a conservative 100-target overlap sweep, followed by an adaptive sweep whose step was `max(100, floor(max(100, 10% of target)))`. This is smaller than the empirically observed response half-window and therefore overlaps the returned windows. Every returned row from both sweeps and the gap/far-empty probes was aggregated and exact-deduplicated.

The endpoint’s rank window expands with the requested target: approximately `max(100, 10% of target)` on each side. Consequently, an apparent gap between returned quota ranks is not called source-empty unless a zero-row response window fully covers it.

## Findings

| Region | Exact rows | National-rank range | Quota-rank range | Adaptive tail-zero probes |
|---:|---:|---:|---:|---|
| 1 | 497 | 1–88307 | 1–32978 | 37321, 41053 |
| 2 | 793 | 2–86862 | 1–34356 | 41053, 45158 |
| 3 | 603 | 43–86084 | 1–19649 | 23175, 25492 |
| **Combined** | **1893** | | | |

### Confirmed source-empty bands

These are direct zero-response windows inferred using the observed endpoint window rule. They are not claims that every rank between adjacent returned rows is independently queried.

- Region 1: 33031–45158 (zero targets 36701, 36801, 37321, 40000, 41053).
- Region 1: 437 internal observed gaps remain unconfirmed as source-empty because no zero response window fully covered them.
- Region 2: 34471–49673 (zero targets 38301, 38401, 40000, 41053, 45158).
- Region 2: 654 internal observed gaps remain unconfirmed as source-empty because no zero response window fully covered them.
- Region 3: 19711–33000 (zero targets 21901, 22001, 23175, 25000, 25492, 30000); 36000–44000 (zero targets 40000).
- Region 3: 500 internal observed gaps remain unconfirmed as source-empty because no zero response window fully covered them.

### Representative QA

Sampling QA only, not a full independent audit. Five adaptive queries per region were checked at low, low-mid, mid, high, and near-tail positions. All five returned rows and every unique row in each sampled response was present in the final aggregate.

- Region 1: low=1 (64 rows), low-mid=3449 (18 rows), mid=13083 (17 rows), high=25492 (10 rows), near-tail=33929 (2 rows).
- Region 2: low=1 (99 rows), low-mid=3793 (26 rows), mid=14391 (17 rows), high=28041 (14 rows), near-tail=37321 (1 rows).
- Region 3: low=1 (89 rows), low-mid=2143 (27 rows), mid=8125 (28 rows), high=15830 (10 rows), near-tail=21069 (1 rows).

## Repo-ready files

The repo-ready tree is under `outputs/repo-ready-math-1404/`. Data and manifest byte sizes and SHA-256 values:

- `data/raw/kanoon/math/1404/region-1.jsonl`: 103833 bytes, SHA-256 `493e5a486a03560f4cb0e859f9abc3d1cf3de493273c0b7edc9b9e21880c17d2`.
- `data/raw/kanoon/math/1404/region-1.manifest.json`: 11412 bytes, SHA-256 `2d82cff55b4b53fbd0161d58781e898eb20910dfa25af4f6a41b79bfcdc31b7a`.
- `data/raw/kanoon/math/1404/region-2.jsonl`: 164832 bytes, SHA-256 `9ca11b039959b1b759cab00dbbd96bc4f83033f7618c11ad6a0d1aa4176645cc`.
- `data/raw/kanoon/math/1404/region-2.manifest.json`: 11726 bytes, SHA-256 `ff8693d371652dfef8443bbad328a5418ca56a32a5612258ffcb65228bd714e0`.
- `data/raw/kanoon/math/1404/region-3.jsonl`: 127403 bytes, SHA-256 `85a6b220686ec5dfe2f2d05b600250f0a6680071a5c6940c42a58d45ffc8489d`.
- `data/raw/kanoon/math/1404/region-3.manifest.json`: 8161 bytes, SHA-256 `e1b3467163722c8fc0f6d50ab694fdf57a4686a77b71319758c5fa8e32606265`.
- `data/raw/kanoon/math/1404/QA_REPORT.json`: 10808 bytes, SHA-256 `7be3391975e991c7f88298c4080708c4b1ba4bb5edc9ca550763c32b5b187177`.

Root TSVs and `math-1404-summary.json` are also emitted under `outputs/`; the requested completion report is duplicated at `reports/data-system/MATH_1404_COMPLETION_REPORT.md` inside the repo-ready tree.

## Validation status

- JSONL was generated with one deterministic JSON object per line and a final newline.
- Canonical-field parsing, exact dedupe, numeric rank validation, region validation, deterministic sort, per-file SHA-256, manifest consistency, summary consistency, and representative sampling QA are validated by the companion build/validation pass.
