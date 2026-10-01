# Sajjad admission data

Source: Telegram channel `@Sajadxyz` / Dr. Sajad Gheibi.

This source is stored independently from Kanoon data. No Kanoon files are overwritten or modified.

## Experimental group

- 1402: 174 usable admission records
- 1403: 203 usable admission records
- 1404: 146 usable admission records

Total: 523 records.

Each year contains:
- `admissions.csv`: normalized rank-to-admission records
- `source-audit.csv`: provenance/audit data with Telegram message identifiers and raw admission labels

Fields in admissions:
`سال, گروه آزمایشی, رتبه کشوری, رتبه در سهمیه, سهمیه, رشته قبولی, دانشگاه قبولی, نوع دوره قبولی`

Notes:
- National rank may be blank when the source post did not provide it.
- Missing course type is preserved as `نامشخص` rather than inferred.
- This dataset is a separate source and should be deduplicated carefully before any future merge with Kanoon or other sources.
