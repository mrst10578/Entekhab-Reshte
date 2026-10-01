# Sajjad admission data

Source: Telegram channel `@Sajadxyz` / Dr. Sajad Gheibi.

This source is stored independently from Kanoon data. No Kanoon files are overwritten or modified.

## Experimental group

- 1401: 43 admission-source records (3 with quota/region rank explicitly present in Telegram text; 40 preserved with blank rank because the rank is not written in the message text)
- 1402: 174 usable admission records
- 1403: 203 usable admission records
- 1404: 147 usable admission records

Total source records: 567.

Each year contains:
- `admissions.csv`: normalized admission records
- `source-audit.csv`: provenance/audit data with Telegram message identifiers and raw admission labels
- `rank-outcomes.csv`: paired accepted/rejected outcomes for candidates where the source explicitly reports failed choices. Rows sharing the same `شناسه داوطلب` belong to one candidate; the accepted row is followed by one or more `عدم قبولی` rows.

Fields in admissions:
`سال, گروه آزمایشی, رتبه کشوری, رتبه در سهمیه, سهمیه, رشته قبولی, دانشگاه قبولی, نوع دوره قبولی`

Notes:
- National rank may be blank when the source post did not provide it.
- For 1401, many Telegram captions identify quota/region and admission but leave the numeric rank inside the image; these records are retained with blank rank rather than discarded or inferred.
- Missing course type is preserved as `نامشخص` rather than inferred.
- This dataset is a separate source and should be deduplicated carefully before any future merge with Kanoon or other sources.


## Help-pack image extraction

The 14 "کمک‌یار انتخاب رشته" image slides supplied from the Sajjad channel have been transcribed separately under `data/raw/sajad/help-pack/`.

- `image-rank-outcomes.csv`: expanded outcome rows. Each candidate has a `قبولی` row and an `عدم قبولی` row tied to the same candidate ID, rank, quota and score.
- `candidates-with-rejections.csv`: one row per candidate with accepted and rejected choices side by side.
- `index.csv`: Telegram message/slide inventory and extraction status.

Current image-pack extraction:
- 158 candidates with an explicit rejected choice
- 145 candidates from 1404
- 13 candidates from 1403
- 316 expanded outcome rows

Image text is preserved as a source transcription rather than silently normalizing ambiguous multi-choice rejection cells. Group phrases such as "کل ...", "همه ..." or multiple universities in one cell remain grouped for later normalization/audit.


## Help Pack

The 14 supplied Help Pack slides were visually extracted and linked to rank outcomes.

- 1404: medicine, medicine 5%/25%, dentistry, pharmacy, physiotherapy, veterinary medicine, nursing, operating room/anesthesia, nutrition/radiology
- 1403: nutrition/radiology
- Extracted rows are also collected in `data/raw/sajad/help-pack/extracted-outcomes.csv`.
- Grouped rejection phrases from the source image are preserved verbatim when splitting them into individual universities would require guessing.
