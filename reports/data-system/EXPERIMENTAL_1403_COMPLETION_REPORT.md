# Experimental 1403 Kanoon Completion Report

Source: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3

Filters: year=1403; group=experimental / تجربی; quota regions 1, 2, and 3.

## QA Result

**PASS: representative QA only**. This is not a full independent audit. All 15 representative queries returned rows that were present in the deduplicated TSVs, with no wrong-region rows, duplicate records, extra records, missing records, unresolved extraction gaps, or blocking responses.

Combined unique records: **4265**.

## Dataset Summary

| Region | Records | Quota range | Confirmed source-empty bands | Tail confirmation |
|---:|---:|---:|---|---|
| 1 | 815 | [1, 48164] | [[20792, 22020], [23624, 25194], [26049, 27188], [27567, 29111], [29774, 31044], [31730, 33099], [33101, 35357], [35359, 38055], [38057, 39357], [39359, 42044], [42952, 48163]] | q52000 ended at [48164, 48164]; zeros at [54000, 56000] |
| 2 | 1864 | [1, 109638] | [[41310, 42351], [43641, 44721], [44982, 47012], [49744, 51483], [52477, 54575], [54724, 56990], [56992, 58355], [58357, 63573], [63575, 75394], [75396, 98328], [98330, 105887], [105889, 108895]] | q120000 ended at [108896, 109638]; zeros at [125000, 130000] |
| 3 | 1586 | [1, 164973] | [[40570, 41833], [45422, 48488], [48798, 51603], [51605, 59667], [59669, 66671], [66673, 72322], [72324, 78420], [78422, 102523], [102525, 108809], [108811, 136998], [137000, 164972]] | q180000 ended at [164973, 164973]; zeros at [185000, 190000] |

## Method

- Adaptive overlapping rank sweep against `/Public/SuperiorsRankBasedShowSuperiors` with year=103, dept=2, type=3, and each quota region independently.
- All returned rows were aggregated and exact-deduplicated across overlapping responses.
- Large apparent gaps were probed at their boundaries and midpoint. No rows appeared inside the declared bands, so they are classified as confirmed source-empty bands rather than extraction gaps.
- Each region continued through the tail. Two higher query ranks returned zero rows after the final nonzero query.
- No CAPTCHA, anti-bot circumvention, login, or private data was used.

## Representative QA

| Region | Label | Query rank | Returned rows | Interval | TSV membership | Filters |
|---:|---|---:|---:|---|---|---|
| 1 | low | 100 | 120 | [1, 198] | all present; no extras | PASS |
| 1 | low-mid | 5000 | 35 | [4505, 5357] | all present; no extras | PASS |
| 1 | mid | 26000 | 7 | [23623, 27566] | all present; no extras | PASS |
| 1 | high | 41600 | 4 | [38056, 42951] | all present; no extras | PASS |
| 1 | near-tail | 52000 | 1 | [48164, 48164] | all present; no extras | PASS |
| 2 | low | 100 | 142 | [1, 199] | all present; no extras | PASS |
| 2 | low-mid | 5000 | 80 | [4540, 5494] | all present; no extras | PASS |
| 2 | mid | 60000 | 5 | [54576, 63574] | all present; no extras | PASS |
| 2 | high | 96000 | 1 | [98329, 98329] | all present; no extras | PASS |
| 2 | near-tail | 120000 | 2 | [108896, 109638] | all present; no extras | PASS |
| 3 | low | 100 | 135 | [1, 199] | all present; no extras | PASS |
| 3 | low-mid | 5000 | 76 | [4507, 5498] | all present; no extras | PASS |
| 3 | mid | 90000 | 0 | None | all present; no extras | PASS |
| 3 | high | 144000 | 1 | [136999, 136999] | all present; no extras | PASS |
| 3 | near-tail | 180000 | 1 | [164973, 164973] | all present; no extras | PASS |

## QA Findings

- Representative QA queries: 15.
- Missing records: 0.
- Unexpected extra rows: 0.
- Duplicate problems after exact dedupe: 0.
- Wrong-region rows: 0.
- Unresolved extraction gaps: 0.
- Blocking issues: 0.
- Scope note: representative QA only; not a full independent audit.

## Files

- `experimental-1403-region-1.tsv`
- `experimental-1403-region-2.tsv`
- `experimental-1403-region-3.tsv`
- `experimental-1403-summary.json`
- `EXPERIMENTAL_1403_COMPLETION_REPORT.md`
- `experimental-1403-kanoon.zip`
