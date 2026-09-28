# Humanities Offline Audit — 2026-09-28

Scope: static audit of the committed Kanoon humanities dataset on this branch. No Browser Use scraping and no GitHub Actions/runner execution were used for this audit.

## Dataset totals

| Year | Region 1 | Region 2 | Region 3 | Total |
|---|---:|---:|---:|---:|
| 1401 | 814 | 3015 | 4334 | 8163 |
| 1402 | 250 | 1035 | 1387 | 2672 |
| 1403 | 269 | 731 | 684 | 1684 |
| 1404 | 233 | 739 | 647 | 1619 |
| **Grand total** | **1566** | **5520** | **7052** | **14138** |

## Internal QA state

All four yearly QA reports currently return PASS.

Validated checks recorded in every QA report:
- JSONL parsing
- exact deduplication
- sorted output
- region labels
- tail probing
- large-gap probing
- source type = 3
- no recorded sweep failures

## Important finding

1402 / Region 1 contains one explicitly recorded source-empty quota-rank band:
- exclusive quota rank interval: 9553..15625
- missing quota-rank span: 6071
- probes recorded at 11071, 12589, 14107

The extraction metadata labels this as a confirmed source-empty band rather than an extraction gap.

## Coverage observations

- 1401 is much larger than later years: 8163 rows vs 2672 / 1684 / 1619.
- The sharp drop after 1401 should be treated as a source-behavior/data-availability characteristic until independently rechecked.
- Region 3 is the largest component overall: 7052 rows.
- Internal PASS means the committed files are structurally consistent with the extractor's QA rules. It does not by itself prove complete parity with every row currently visible on Kanoon's website.

## Safe next checks

1. Browser-only spot checks at low / mid / high quota-rank windows for each year-region.
2. Recheck the 1402 Region 1 empty band through normal browser interaction.
3. Compare a small sample of accepted_raw strings with the rendered site.
4. Do not run extraction workflows or scraping jobs from GitHub Actions for these checks.

## Audit execution note

This report was created directly through repository file operations on branch `audit/humanities-offline-20260928`. No workflow was dispatched.
