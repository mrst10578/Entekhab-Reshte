# Experimental 1401 Kanoon Completion Report

Source: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3

Filters: year=1401; group=تجربی; quota regions 1, 2, and 3.

## Status

**PASS**. All three TSVs remained intact and passed representative public QA. No mismatch, missing record, duplicate problem, wrong filter, wrong-region row, gap, or blocking/transfer issue was found.

Combined unique records: **13694**.

## Dataset Summary

| Region | File | Unique records | Quota range | Gaps | Tail confirmation |
|---:|---|---:|---:|---|---|
| 1 | experimental-1401-region-1.tsv | 1972 | [1, 52464] | none | q56661 ended at 52464; q65161 and q81452 returned zero |
| 2 | experimental-1401-region-2.tsv | 6430 | [2, 131596] | none | q140807 ended at 131596; q161929 and q202412 returned zero |
| 3 | experimental-1401-region-3.tsv | 5292 | [2, 129559] | none | q138628 ended at 129559; q159423 and q199279 returned zero |

## Representative QA

| Region | Check | Query rank | Returned rows | Returned interval | TSV membership | Filters |
|---:|---|---:|---:|---:|---|---|
| 1 | low | 100 | 110 | [1, 198] | all present | year=1401, تجربی, region 1 |
| 1 | low-mid | 5000 | 104 | [4510, 5475] | all present | year=1401, تجربی, region 1 |
| 1 | mid | 20000 | 79 | [18016, 21850] | all present | year=1401, تجربی, region 1 |
| 1 | high | 50000 | 6 | [45621, 52464] | all present | year=1401, تجربی, region 1 |
| 1 | near-tail | 56661 | 2 | [51542, 52464] | all present | year=1401, تجربی, region 1 |
| 2 | low | 100 | 134 | [2, 199] | all present | year=1401, تجربی, region 2 |
| 2 | low-mid | 5000 | 298 | [4508, 5499] | all present | year=1401, تجربی, region 2 |
| 2 | mid | 30000 | 351 | [27006, 32978] | all present | year=1401, تجربی, region 2 |
| 2 | high | 100000 | 14 | [91045, 108444] | all present | year=1401, تجربی, region 2 |
| 2 | near-tail | 140807 | 1 | [131596, 131596] | all present | year=1401, تجربی, region 2 |
| 3 | low | 100 | 112 | [2, 200] | all present | year=1401, تجربی, region 3 |
| 3 | low-mid | 5000 | 235 | [4503, 5499] | all present | year=1401, تجربی, region 3 |
| 3 | mid | 30000 | 281 | [27087, 32990] | all present | year=1401, تجربی, region 3 |
| 3 | high | 100000 | 10 | [93797, 109387] | all present | year=1401, تجربی, region 3 |
| 3 | near-tail | 138628 | 3 | [125673, 129559] | all present | year=1401, تجربی, region 3 |

## Tail Evidence

Each region has a final nonzero query followed by two higher public queries returning zero rows:

- Region 1: q56661 [51542, 52464]; zeros at 65161 and 81452.
- Region 2: q140807 [131596, 131596]; zeros at 161929 and 202412.
- Region 3: q138628 [125673, 129559]; zeros at 159423 and 199279.

## Files

- `experimental-1401-region-1.tsv`
- `experimental-1401-region-2.tsv`
- `experimental-1401-region-3.tsv`
- `experimental-1401-summary.json`
- `EXPERIMENTAL_1401_COMPLETION_REPORT.md`
- `experimental-1401-kanoon.zip`
