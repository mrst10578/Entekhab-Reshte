# EXPERIMENTAL 1404 Kanoon Admissions Completion Report

## Scope

- Source page: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3
- Public result endpoint used by the page: https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors
- Year: 1404 (source value 104)
- Group: experimental / تجربی (source value 2)
- Regions: 1, 2 and 3 independently
- Requested fields: kanoon_score, national_rank, quota_rank, quota_region, gender, city, accepted_raw
- CAPTCHA or anti-bot bypass: none; all extraction and QA responses were HTTP 200 and no block was encountered.

## Method

The public page's own JSON POST flow was queried with an adaptive rank sweep. After each non-empty response, the returned quota-rank interval was recorded and the next query used the returned upper endpoint to create deliberate overlap. When the source repeated a stale terminal window behind the query rank, small bridge probes advanced until the response changed; supplemental boundary and midpoint probes closed uncovered intervals. Rows were parsed from the seven table columns and exact-deduplicated by the full seven-field tuple.

## Findings

- Region 1: **853 rows**; quota rank 2-46149; national rank 3-219149; Kanoon score 4022-8059; SHA-256 16701b961bb9c4cd1157a302eeffbb75a47bd531b63bb614f866c74592a62863.
- Region 2: **1861 rows**; quota rank 1-90983; national rank 2-226931; Kanoon score 4012-8069; SHA-256 025c4b992295553c34da7cb57a8374737ef5dc6566fb968eced69c1628ee7ddf.
- Region 3: **1556 rows**; quota rank 1-89774; national rank 5-229529; Kanoon score 4018-8542; SHA-256 61ecdadea6ebb0db97eff004e4e77b67eb2200038316b5a5d4b78b69d797cd2b.

Combined total: **4270 rows**.

## Confirmed Empty Bands

- Region 1, quota ranks 46150-51376: Queries 46150, 47000, 48000, 49000, 50000 and 51000 returned only records at or below quota rank 46149; queries 51377, 51476 and 52376 returned zero.
- Region 2, quota ranks 70525-90982: Queries 70525 and 75000 returned only the prior rank 70524; queries 78525 and 80000 returned zero; the next returned record was rank 90983 at queries 85000 and 90000.
- Region 3, quota ranks 65430-89773: Queries 65430 and 70000 returned only records at or below rank 65429; queries 72789, 75000 and 80000 returned zero; the next returned record was rank 89774 at query 85000.

## Tail Probes

- Region 1: last observed quota rank 46149; higher zero probes: 51377, 51476, 52376, 61376, 151376. The first two higher zero probes confirm the source end; later probes were additional confirmation.
- Region 2: last observed quota rank 90983; higher zero probes: 101184, 101283, 102183, 111183, 201183. The first two higher zero probes confirm the source end; later probes were additional confirmation.
- Region 3: last observed quota rank 89774; higher zero probes: 99875, 99974, 100874, 109874, 199874. The first two higher zero probes confirm the source end; later probes were additional confirmation.

## Sampling QA

Five queries per region were sampled at low, low-mid, mid, high and near-tail ranks. Result: **PASS**. This is sampling QA, not a full independent audit.

## Repo-Ready Tree

`outputs/repo-ready-1404/`
- data/raw/kanoon/experimental/1404/region-1.jsonl (174696 bytes)
- data/raw/kanoon/experimental/1404/region-1.manifest.json (1268 bytes)
- data/raw/kanoon/experimental/1404/region-2.jsonl (381535 bytes)
- data/raw/kanoon/experimental/1404/region-2.manifest.json (1269 bytes)
- data/raw/kanoon/experimental/1404/region-3.jsonl (325219 bytes)
- data/raw/kanoon/experimental/1404/region-3.manifest.json (1269 bytes)
- QA_REPORT.json (4171 bytes)
- stage-summary.json (4515 bytes)
- reports/data-system/EXPERIMENTAL_1404_COMPLETION_REPORT.md (3696 bytes)
