# Gozine2 historical admissions recovery

This directory stores the recovered public Gozine2 report-card dataset before it is merged into the repository-wide rank/admission tables.

## Coverage

- 1397: 165 records
- 1398: 306 records
- 1399: 91 records
- 1400: 52 records
- 1402: 28 records
- Total: 642 records

Each year is stored independently as <year>/admissions.csv.

The raw source table preserves experimental group, national rank when visible, rank in quota, quota/region when visible, accepted major and university, admission type when visible, original Telegram permalink/post, image hash and recovery channel, and rank QA metadata.

The merge into data/rank_admissions deliberately keeps that folder's existing seven-column schema. Source provenance and admission type remain here instead of being discarded.

Recovery used only public historical pages, public Telegram archives and archived public web content. It does not automate Norato login or bypass query limits.
