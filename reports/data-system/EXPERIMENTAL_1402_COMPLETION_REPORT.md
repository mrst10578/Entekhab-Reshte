# Experimental 1402 Kanoon Completion Report

Source: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3

Filters: year=1402; group=تجربی; regions 1, 2, and 3.

## QA Result

**PASS with formatting note**. All three TSVs passed 15 representative public queries. All 631 returned rows matched the corresponding TSV after canonical whitespace comparison. Three region-2 `accepted_raw` cells had an HTML-only double-space difference from the TSV's single-space text; these were the only raw-text differences and were not substantive record mismatches. No missing, unexpected extra, duplicate, wrong-filter, wrong-region, unresolved-gap, or blocking issue was found.

Combined unique records: **3381**.

## Dataset Summary

| Region | File | Unique records | Quota range | Empty source band | Tail confirmation |
|---:|---|---:|---:|---|---|
| 1 | experimental-1402-region-1.tsv | 620 | [1, 28976] | none | q31004 ended at 28976; zeros at 35655 and q44569 |
| 2 | experimental-1402-region-2.tsv | 1598 | [3, 78608] | [62406, 76213] | q85000 ended at 78608; zeros at 90000 and q95000 |
| 3 | experimental-1402-region-3.tsv | 1163 | [1, 83482] | [57611, 76069] | q90000 ended at 83482; zeros at 100000 and q110000 |

## Representative QA

| Region | Check | Query | Rows | Interval | TSV comparison | Filters |
|---:|---|---:|---:|---:|---|---|
| 1 | low | 100 | 133 | [1, 200] | all present; no duplicates | PASS |
| 1 | low-mid | 4751 | 11 | [4247, 5170] | all present; no duplicates | PASS |
| 1 | mid | 15568 | 7 | [14220, 16820] | all present; no duplicates | PASS |
| 1 | high | 26117 | 4 | [23524, 26595] | all present; no duplicates | PASS |
| 1 | near-tail | 31004 | 1 | [28976, 28976] | all present; no duplicates | PASS |
| 2 | low | 100 | 158 | [3, 200] | all present; no duplicates | PASS |
| 2 | low-mid | 5398 | 58 | [4811, 5880] | all present; no duplicates | PASS |
| 2 | mid | 19565 | 30 | [17611, 21442] | all present; no duplicates | PASS |
| 2 | high | 51370 | 5 | [47565, 53075] | all present; no duplicates | PASS |
| 2 | near-tail | 85000 | 1 | [78608, 78608] | all present; no duplicates | PASS |
| 3 | low | 100 | 130 | [1, 199] | all present; no duplicates | PASS |
| 3 | low-mid | 5393 | 36 | [4815, 5856] | all present; no duplicates | PASS |
| 3 | mid | 18902 | 24 | [17121, 20699] | all present; no duplicates | PASS |
| 3 | high | 54025 | 3 | [50024, 57610] | all present; no duplicates | PASS |
| 3 | near-tail | 90000 | 1 | [83482, 83482] | all present; no duplicates | PASS |

## Formatting-Only Differences

- Region 2, query q19565: quota ranks 20029 and 20557 rendered one extra space inside `accepted_raw` in the public HTML.
- Region 2, query q51370: quota rank 52170 rendered one extra space inside `accepted_raw` in the public HTML.
- After collapsing repeated whitespace, all three rows match their TSV records exactly.

## Empty-Band Probes

No returned row fell inside either declared band. Boundary rows jump across each band, so both are classified as empty source bands rather than extraction gaps.

| Region | Declared band | Probe query ranks | Rows inside band | Conclusion |
|---:|---:|---|---:|---|
| 2 | [62406, 76213] | 62405, 63000, 65000, 68000, 70000, 76213, 76214 | 0 | empty source band |
| 3 | [57611, 76069] | 57610, 60000, 63000, 65000, 70000, 74000, 76069, 76070 | 0 | empty source band |

## Tail Confirmation

- Region 1: last nonzero q31004 reached 28976; q35655 and q44569 returned zero.
- Region 2: last nonzero q85000 reached 78608; q90000 and q95000 returned zero.
- Region 3: last nonzero q90000 reached 83482; q100000 and q110000 returned zero.

## QA Findings

- Raw text differences: 3, all whitespace-only.
- Substantive mismatches: 0.
- Missing rows: 0.
- Unexpected extra rows: 0.
- Duplicate problems: 0.
- Wrong-region rows: 0.
- Source gaps: 0 unresolved; declared empty bands were confirmed.
- Blocking issues: 0.

## Files

- `experimental-1402-region-1.tsv`
- `experimental-1402-region-2.tsv`
- `experimental-1402-region-3.tsv`
- `experimental-1402-summary.json`
- `EXPERIMENTAL_1402_COMPLETION_REPORT.md`
- `experimental-1402-kanoon.zip`
