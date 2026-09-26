# Kanoon MATHEMATICS / ریاضی 1401 Completion Report

- Source rendered page: https://www.kanoon.ir/Public/SuperiorsRankBased?type=3
- Source POST endpoint: https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors
- Workflow: LoPRax RankLab adaptive overlapping quota-rank sweep via the public rendered page POST behavior
- Filters: exam group mathematics / ریاضی (`dept=1`), year 1401 (`year=101`), type 3.
- Canonical fields: `kanoon_score`, `national_rank`, `quota_rank`, `quota_region`, `gender`, `city`, `accepted_raw`.
- Exact dedupe key: UTF-8 JSON serialization of those seven fields in that order.
- Sort order: national rank ascending, quota rank ascending, Kanoon score descending, then remaining canonical fields lexicographically.

## Results

| Region | Exact rows | National-rank range | Quota-rank range | Sweep queries | Tail zero probes |
|---:|---:|---:|---:|---:|---|
| 1 | 1362 | 1-107843 | 1-36267 | 136 | 40367, 40467 |
| 2 | 3825 | 3-127544 | 1-49965 | 160 | 55565, 55665 |
| 3 | 2279 | 24-113848 | 1-31275 | 127 | 34875, 34975 |
| **Combined** | **7466** | | | | |

## Completion evidence

Each region reached the tail rule: two strictly higher query ranks returned zero rows. All sweep requests were HTTP 200 with no parser failures.

## Confirmed source-empty bands

Bands below contain at least 100 missing quota-rank values. Each was probed at three internal points; every probe returned HTTP 200 and zero rows inside the band. Smaller gaps are not classified by this audit.

### Region 1
- (7839, 7967) exclusive; 127 missing ranks; probes 7871, 7903, 7935
- (9016, 9137) exclusive; 120 missing ranks; probes 9047, 9077, 9107
- (14686, 14788) exclusive; 101 missing ranks; probes 14712, 14737, 14763
- (15610, 15766) exclusive; 155 missing ranks; probes 15649, 15688, 15727
- (15838, 15942) exclusive; 103 missing ranks; probes 15864, 15890, 15916
- (16628, 16751) exclusive; 122 missing ranks; probes 16659, 16690, 16721
- (17774, 17877) exclusive; 102 missing ranks; probes 17800, 17826, 17852
- (18087, 18190) exclusive; 102 missing ranks; probes 18113, 18139, 18165
- (18190, 18302) exclusive; 111 missing ranks; probes 18218, 18246, 18274
- (18604, 18761) exclusive; 156 missing ranks; probes 18644, 18683, 18722
- (18839, 18995) exclusive; 155 missing ranks; probes 18878, 18917, 18956
- (19012, 19249) exclusive; 236 missing ranks; probes 19072, 19131, 19190
- (19249, 19369) exclusive; 119 missing ranks; probes 19279, 19309, 19339
- (19570, 19755) exclusive; 184 missing ranks; probes 19617, 19663, 19709
- (19755, 20080) exclusive; 324 missing ranks; probes 19837, 19918, 19999
- (20182, 20289) exclusive; 106 missing ranks; probes 20209, 20236, 20263
- (20418, 20725) exclusive; 306 missing ranks; probes 20495, 20572, 20649
- (21432, 21557) exclusive; 124 missing ranks; probes 21464, 21495, 21526
- (21854, 21975) exclusive; 120 missing ranks; probes 21885, 21915, 21945
- (22068, 22249) exclusive; 180 missing ranks; probes 22114, 22159, 22204
- (22454, 22678) exclusive; 223 missing ranks; probes 22510, 22566, 22622
- (22933, 23067) exclusive; 133 missing ranks; probes 22967, 23000, 23034
- (23067, 23201) exclusive; 133 missing ranks; probes 23101, 23134, 23168
- (23512, 23748) exclusive; 235 missing ranks; probes 23571, 23630, 23689
- (23785, 23991) exclusive; 205 missing ranks; probes 23837, 23888, 23940
- (23991, 24111) exclusive; 119 missing ranks; probes 24021, 24051, 24081
- (24122, 24239) exclusive; 116 missing ranks; probes 24152, 24181, 24210
- (24239, 24414) exclusive; 174 missing ranks; probes 24283, 24327, 24371
- (24437, 24556) exclusive; 118 missing ranks; probes 24467, 24497, 24527
- (24756, 24979) exclusive; 222 missing ranks; probes 24812, 24868, 24924
- (25008, 25152) exclusive; 143 missing ranks; probes 25044, 25080, 25116
- (25236, 25443) exclusive; 206 missing ranks; probes 25288, 25340, 25392
- (25465, 25675) exclusive; 209 missing ranks; probes 25518, 25570, 25623
- (25708, 25895) exclusive; 186 missing ranks; probes 25755, 25802, 25849
- (25895, 26056) exclusive; 160 missing ranks; probes 25936, 25976, 26016
- (26056, 26179) exclusive; 122 missing ranks; probes 26087, 26118, 26149
- (26179, 26592) exclusive; 412 missing ranks; probes 26283, 26386, 26489
- (26592, 26719) exclusive; 126 missing ranks; probes 26624, 26656, 26688
- (26719, 27255) exclusive; 535 missing ranks; probes 26853, 26987, 27121
- (27255, 27406) exclusive; 150 missing ranks; probes 27293, 27331, 27369
- (27406, 27598) exclusive; 191 missing ranks; probes 27454, 27502, 27550
- (27684, 28095) exclusive; 410 missing ranks; probes 27787, 27890, 27993
- (28095, 28343) exclusive; 247 missing ranks; probes 28157, 28219, 28281
- (28476, 29302) exclusive; 825 missing ranks; probes 28683, 28889, 29096
- (29302, 29630) exclusive; 327 missing ranks; probes 29384, 29466, 29548
- (29707, 29835) exclusive; 127 missing ranks; probes 29739, 29771, 29803
- (29835, 30347) exclusive; 511 missing ranks; probes 29963, 30091, 30219
- (30347, 31194) exclusive; 846 missing ranks; probes 30559, 30771, 30983
- (31194, 31536) exclusive; 341 missing ranks; probes 31280, 31365, 31451
- (31536, 36267) exclusive; 4730 missing ranks; probes 32719, 33902, 35085

### Region 2
- (20679, 20782) exclusive; 102 missing ranks; probes 20705, 20731, 20757
- (20825, 20960) exclusive; 134 missing ranks; probes 20859, 20893, 20927
- (24276, 24396) exclusive; 119 missing ranks; probes 24306, 24336, 24366
- (24536, 24640) exclusive; 103 missing ranks; probes 24562, 24588, 24614
- (24792, 24955) exclusive; 162 missing ranks; probes 24833, 24874, 24915
- (25529, 25648) exclusive; 118 missing ranks; probes 25559, 25589, 25619
- (26234, 26345) exclusive; 110 missing ranks; probes 26262, 26290, 26318
- (26345, 26454) exclusive; 108 missing ranks; probes 26373, 26400, 26427
- (26454, 26613) exclusive; 158 missing ranks; probes 26494, 26534, 26574
- (26613, 26806) exclusive; 192 missing ranks; probes 26662, 26710, 26758
- (27752, 27911) exclusive; 158 missing ranks; probes 27792, 27832, 27872
- (28830, 28931) exclusive; 100 missing ranks; probes 28856, 28881, 28906
- (29050, 29166) exclusive; 115 missing ranks; probes 29079, 29108, 29137
- (29477, 29596) exclusive; 118 missing ranks; probes 29507, 29537, 29567
- (29827, 29945) exclusive; 117 missing ranks; probes 29857, 29886, 29916
- (30028, 30192) exclusive; 163 missing ranks; probes 30069, 30110, 30151
- (30474, 30579) exclusive; 104 missing ranks; probes 30501, 30527, 30553
- (30766, 30930) exclusive; 163 missing ranks; probes 30807, 30848, 30889
- (31130, 31254) exclusive; 123 missing ranks; probes 31161, 31192, 31223
- (31254, 31380) exclusive; 125 missing ranks; probes 31286, 31317, 31349
- (31589, 31744) exclusive; 154 missing ranks; probes 31628, 31667, 31706
- (31913, 32098) exclusive; 184 missing ranks; probes 31960, 32006, 32052
- (32197, 32378) exclusive; 180 missing ranks; probes 32243, 32288, 32333
- (32378, 32567) exclusive; 188 missing ranks; probes 32426, 32473, 32520
- (32801, 33071) exclusive; 269 missing ranks; probes 32869, 32936, 33004
- (33124, 33303) exclusive; 178 missing ranks; probes 33169, 33214, 33259
- (33303, 33492) exclusive; 188 missing ranks; probes 33351, 33398, 33445
- (33517, 33659) exclusive; 141 missing ranks; probes 33553, 33588, 33624
- (33659, 34412) exclusive; 752 missing ranks; probes 33848, 34036, 34224
- (34412, 34552) exclusive; 139 missing ranks; probes 34447, 34482, 34517
- (34968, 35292) exclusive; 323 missing ranks; probes 35049, 35130, 35211
- (35437, 35558) exclusive; 120 missing ranks; probes 35468, 35498, 35528
- (35558, 35865) exclusive; 306 missing ranks; probes 35635, 35712, 35789
- (35865, 36017) exclusive; 151 missing ranks; probes 35903, 35941, 35979
- (36017, 36556) exclusive; 538 missing ranks; probes 36152, 36287, 36422
- (36593, 36731) exclusive; 137 missing ranks; probes 36628, 36662, 36697
- (36731, 36865) exclusive; 133 missing ranks; probes 36765, 36798, 36832
- (36914, 37143) exclusive; 228 missing ranks; probes 36972, 37029, 37086
- (37143, 37257) exclusive; 113 missing ranks; probes 37172, 37200, 37229
- (37257, 37764) exclusive; 506 missing ranks; probes 37384, 37511, 37638
- (37764, 38283) exclusive; 518 missing ranks; probes 37894, 38024, 38154
- (38362, 38605) exclusive; 242 missing ranks; probes 38423, 38484, 38545
- (38605, 40168) exclusive; 1562 missing ranks; probes 38996, 39387, 39778
- (40168, 43453) exclusive; 3284 missing ranks; probes 40990, 41811, 42632
- (43453, 49965) exclusive; 6511 missing ranks; probes 45081, 46709, 48337

### Region 3
- (15971, 16082) exclusive; 110 missing ranks; probes 15999, 16027, 16055
- (17871, 18005) exclusive; 133 missing ranks; probes 17905, 17938, 17972
- (18019, 18146) exclusive; 126 missing ranks; probes 18051, 18083, 18115
- (18722, 18875) exclusive; 152 missing ranks; probes 18761, 18799, 18837
- (19704, 19856) exclusive; 151 missing ranks; probes 19742, 19780, 19818
- (20379, 20509) exclusive; 129 missing ranks; probes 20412, 20444, 20477
- (20564, 20667) exclusive; 102 missing ranks; probes 20590, 20616, 20642
- (20811, 21484) exclusive; 672 missing ranks; probes 20980, 21148, 21316
- (21521, 21645) exclusive; 123 missing ranks; probes 21552, 21583, 21614
- (21773, 21937) exclusive; 163 missing ranks; probes 21814, 21855, 21896
- (21937, 22072) exclusive; 134 missing ranks; probes 21971, 22005, 22039
- (22225, 22343) exclusive; 117 missing ranks; probes 22255, 22284, 22314
- (22418, 22665) exclusive; 246 missing ranks; probes 22480, 22542, 22604
- (22665, 22892) exclusive; 226 missing ranks; probes 22722, 22779, 22836
- (23102, 23260) exclusive; 157 missing ranks; probes 23142, 23181, 23221
- (23260, 23494) exclusive; 233 missing ranks; probes 23319, 23377, 23436
- (23494, 23671) exclusive; 176 missing ranks; probes 23539, 23583, 23627
- (23671, 23774) exclusive; 102 missing ranks; probes 23697, 23723, 23749
- (23774, 23925) exclusive; 150 missing ranks; probes 23812, 23850, 23888
- (23925, 24283) exclusive; 357 missing ranks; probes 24015, 24104, 24194
- (24283, 24467) exclusive; 183 missing ranks; probes 24329, 24375, 24421
- (24507, 24683) exclusive; 175 missing ranks; probes 24551, 24595, 24639
- (24692, 24867) exclusive; 174 missing ranks; probes 24736, 24780, 24824
- (24916, 25057) exclusive; 140 missing ranks; probes 24952, 24987, 25022
- (25148, 25271) exclusive; 122 missing ranks; probes 25179, 25210, 25241
- (25271, 26190) exclusive; 918 missing ranks; probes 25501, 25731, 25961
- (26190, 27075) exclusive; 884 missing ranks; probes 26412, 26633, 26854
- (27075, 31275) exclusive; 4199 missing ranks; probes 28125, 29175, 30225

## Extraction-gap distinction

No audited band was classified as an extraction gap: there were no failed gap probes and no returned rows inside a band classified as source-empty. The unclassified population consists only of gaps with fewer than 100 missing quota-rank values.

## Representative sampling QA

This is sampling QA, not a full independent audit. Five queries per region were re-requested at low, low-mid, mid, high, and near-tail positions.

| Region | Label | Query rank | Endpoint rows | Stored rows present | Unmatched | Result |
|---:|---|---:|---:|---:|---:|---|
| 1 | low | 1 | 78 | 78 | 0 | pass |
| 1 | low-mid | 10066 | 105 | 105 | 0 | pass |
| 1 | mid | 20133 | 61 | 61 | 0 | pass |
| 1 | high | 30200 | 15 | 15 | 0 | pass |
| 1 | near-tail | 40267 | 1 | 1 | 0 | pass |
| 2 | low | 1 | 144 | 144 | 0 | pass |
| 2 | low-mid | 13866 | 305 | 305 | 0 | pass |
| 2 | mid | 27732 | 142 | 142 | 0 | pass |
| 2 | high | 41598 | 6 | 6 | 0 | pass |
| 2 | near-tail | 55465 | 1 | 1 | 0 | pass |
| 3 | low | 1 | 122 | 122 | 0 | pass |
| 3 | low-mid | 8693 | 141 | 141 | 0 | pass |
| 3 | mid | 17387 | 130 | 130 | 0 | pass |
| 3 | high | 26081 | 17 | 17 | 0 | pass |
| 3 | near-tail | 34775 | 1 | 1 | 0 | pass |

All 15 sampling-QA queries passed membership checks.

## Repo-ready tree

```text
repo-ready-math-1401/
└── data/raw/kanoon/math/1401/
    ├── region-1.jsonl
    ├── region-1.manifest.json
    ├── region-2.jsonl
    ├── region-2.manifest.json
    ├── region-3.jsonl
    ├── region-3.manifest.json
    ├── stage-summary.json
    └── QA_REPORT.json
```

Byte sizes and SHA-256 values are in each region manifest. The top-level TSV, summary, and this report are the user-facing copies.

