import argparse
import collections
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import fitz
DIG=str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩','01234567890123456789')

def norm(s):
    s=''.join(ch for ch in str(s) if unicodedata.category(ch)!='Cf')
    s=unicodedata.normalize('NFKC',s).translate(DIG)
    s=s.replace('ي','ی').replace('ى','ی').replace('ك','ک').replace('\u200c',' ')
    s=re.sub(r'[‐‑‒–—−]','-',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

def group_lines(words,tol=2.3):
    arr=[]
    for w in words:
        x0,y0,x1,y1,t,*_=w
        arr.append({'x0':x0,'y0':y0,'x1':x1,'y1':y1,'cy':(y0+y1)/2,'text':norm(t)})
    arr.sort(key=lambda z:(z['cy'],z['x0']))
    groups=[]
    for w in arr:
        if not groups or abs(w['cy']-groups[-1]['cy'])>tol:
            groups.append({'cy':w['cy'],'words':[w]})
        else:
            groups[-1]['words'].append(w)
            groups[-1]['cy']=sum(x['cy'] for x in groups[-1]['words'])/len(groups[-1]['words'])
    return groups

def digits_run_for_line(g, xlo=345, xhi=475):
    ws=sorted(g['words'],key=lambda z:z['x0'])
    runs=[]; cur=[]
    for w in ws:
        if xlo <= w['x0'] <= xhi and re.fullmatch(r'\d+',w['text']):
            if cur and w['x0']-cur[-1]['x1']>2.8:
                runs.append(cur);cur=[]
            cur.append(w)
        else:
            if cur: runs.append(cur);cur=[]
    if cur:runs.append(cur)
    for r in runs:
        s=''.join(x['text'] for x in r)
        if len(s)==5:
            return s,min(x['x0'] for x in r),max(x['x1'] for x in r)
    return None

def logical_text(words):
    if not words:return ''
    # lines top to bottom, words right to left
    gs=[]
    for w in sorted(words,key=lambda z:(z['cy'],z['x0'])):
        if not gs or abs(w['cy']-gs[-1][0])>2.5:
            gs.append([w['cy'],[w]])
        else:gs[-1][1].append(w)
    lines=[]
    for _,ws in gs:
        lines.append(' '.join(x['text'] for x in sorted(ws,key=lambda z:z['x0'],reverse=True)))
    return norm(' '.join(lines))

def map_major(title):
    s=norm(title)
    # normalize spacing variants
    compact=s.replace(' ','')
    rules=[
      ('ارتوز و پروتز (اعضای مصنوعی و وسایل کمکی)', lambda: 'ارتوزوپروتز' in compact or ('اعضایمصنوعی' in compact and 'وسایلکمکی' in compact)),
      ('ساخت پروتزهای دندانی', lambda: 'ساختپروتزهایدندانی' in compact),
      ('تکنولوژی پزشکی هسته‌ای', lambda: 'تکنولوژیپزشکیهسته' in compact),
      ('تکنولوژی پرتودرمانی', lambda: 'تکنولوژیپرتودرمانی' in compact),
      ('تکنولوژی پرتوشناسی', lambda: 'تکنولوژیپرتوشناسی' in compact),
      ('فوریت‌های پزشکی پیش‌بیمارستانی', lambda: 'فوریت' in s and 'پزشکی' in s and 'بیمارستانی' in s),
      ('مهندسی بهداشت حرفه ای و ایمنی کار', lambda: 'مهندسیبهداشتحرفه' in compact and 'ایمنیکار' in compact),
      ('مدیریت خدمات بهداشتی درمانی', lambda: 'مدیریتخدماتبهداشتیدرمانی' in compact),
      ('فناوری اطلاعات سلامت', lambda: 'فناوریاطالعاتسالمت' in compact or 'فناوریاطلاعاتسلامت' in compact),
      ('کتابداری و اطلاع‌رسانی پزشکی', lambda: 'مدیریتاطالعرسانیعلومپزشکی' in compact or 'کتابداری' in s and 'پزشکی' in s),
      ('علوم و صنایع غذایی / علوم و مهندسی صنایع غذایی', lambda: ('علوموصنایعغذایی' in compact or 'علومومهندسیصنایعغذایی' in compact)),
      ('علوم آزمایشگاهی دامپزشکی', lambda: 'علومآزمایشگاهیدامپزشکی' in compact),
      ('دکتری عمومی دامپزشکی', lambda: 'دکتریعمومیدامپزشکی' in compact),
      ('بهداشت و بازرسی گوشت', lambda: 'بهداشتوبازرسیگوشت' in compact),
      ('بهداشت مواد غذایی', lambda: 'بهداشتموادغذایی' in compact),
      ('زیست‌شناسی سلولی و مولکولی', lambda: 'زیستشناسیسلولیومولکولی' in compact),
      ('زیست‌شناسی جانوری', lambda: 'زیستشناسیجانوری' in compact),
      ('زیست‌شناسی گیاهی', lambda: 'زیستشناسیگیاهی' in compact),
      ('زیست‌فناوری', lambda: 'زیستفناوری' in compact),
      ('کاردانی دامپزشکی', lambda: 'کاردانیدامپزشکی' in compact),
      ('میکروبیولوژی', lambda: 'میکروبیولوژی' in s),
      ('شیمی کاربردی', lambda: 'شیمیکاربردی' in compact),
      ('شیمی محض', lambda: 'شیمیمحض' in compact),
      ('بهداشت عمومی', lambda: 'بهداشتعمومی' in compact),
      ('بینایی‌سنجی', lambda: 'بینایی' in s and 'سنجی' in s),
      ('پرستاری', lambda: 'پرستاری' in s),
      ('پزشکی', lambda: 'دکتریعمومیپزشکی' in compact),
      ('داروسازی', lambda: 'دکتریعمومیداروسازی' in compact),
      ('دندانپزشکی', lambda: 'دکتریعمومیدندانپزشکی' in compact),
      ('اتاق عمل', lambda: 'تکنولوژیاتاقعمل' in compact),
      ('شنوایی‌شناسی', lambda: 'شنوایی' in s and 'شناسی' in s),
      ('علوم آزمایشگاهی', lambda: 'علومآزمایشگاهی' in compact and 'دامپزشکی' not in s),
      ('علوم تغذیه', lambda: 'علومتغذیه' in compact),
      ('فیزیوتراپی', lambda: 'فیزیوتراپی' in s),
      ('کاردرمانی', lambda: 'کاردرمانی' in s),
      ('گفتاردرمانی', lambda: 'گفتاردرمانی' in s),
      ('مامایی', lambda: 'مامایی' in s),
      ('مهندسی بهداشت محیط', lambda: 'مهندسیبهداشتمحیط' in compact),
      ('هوشبری', lambda: 'هوشبری' in s),
    ]
    for label,test in rules:
        if test(): return label
    return None

def col_value(g,xlo,xhi):
    ws=[w for w in g['words'] if xlo<=w['x0']<xhi]
    if not ws:return ''
    return norm(''.join(w['text'] for w in sorted(ws,key=lambda z:z['x0'])))

def parse_num(v):
    v=norm(v)
    m=re.search(r'\d+',v)
    return int(m.group()) if m else None

def clean_heading(s):
    s=norm(s).replace('ادامه استان','استان',1)
    s=re.sub(r'\s*-\s*',' - ',s)
    return norm(s)

def regular_institution(blocks,cy,carry):
    cands=[]
    for b in blocks:
        x0,y0,x1,y1,text,*_=b
        s=norm(' '.join(text.split()))
        if y1<=cy+1 and re.match(r'^(?:ادامه\s+)?استان\s+', s) and any(k in s for k in ['دانشگاه','دانشکده','مرکز آموزش','مجتمع آموزش','مؤسسه آموزش','موسسه آموزش']):
            cands.append((y1,clean_heading(s)))
    h=cands[-1][1] if cands else carry
    if not h:return '', '', carry
    h=clean_heading(h)
    m=re.search(r'استان\s+(.+?)\s+-\s+(.+)',h)
    if m:
        prov=norm(m.group(1)); uni=norm(m.group(2)).lstrip(')').strip(); uni = uni + ')' if '(' in uni and ')' not in uni else uni
    else:
        prov=''; uni=h
    return uni,prov,h

COND_WORDS=('خوابگاه','مهمانی','ميهمانی','انتقال','شرایط','دارای','فاقد','محدودیت','عدم','ممنوعیت','معرفی','ویژه','تعهد','پذیرش','بورس','مصاحبه')
def special_institution(words):
    s=logical_text(words)
    # start from first institution keyword in logical text
    m=re.search(r'(دانشگاه|دانشکده|مؤسسه|موسسه|مرکز آموزش عالی|مجتمع آموزش عالی|آموزشکده)',s)
    if not m:return ''
    s=s[m.start():]
    s=re.sub(r'\s*-\s*',' - ',s)
    # cut obvious condition phrase
    cut=len(s)
    for kw in COND_WORDS:
        mm=re.search(r'\s+'+re.escape(kw)+r'\b',s)
        if mm: cut=min(cut,mm.start())
    s=s[:cut].strip(' -')
    parts=[p.strip() for p in s.split(' - ') if p.strip()]
    if len(parts)>1 and not any(k in parts[1] for k in COND_WORDS) and len(parts[1])<=40:
        return norm(parts[0]+' - '+parts[1])
    return norm(parts[0] if parts else s)

def program_type(right_text):
    s=norm(right_text)
    patterns=['شهریه پرداز','نوبت دوم','آزاد تمام وقت','خودگردان آزاد','پردیس خودگردان','روزانه - غیردولتی','روزانه','مجازی']
    for p in patterns:
        if p in s:return p
    return 'در جدول ذکر نشده'

def classify_admission(conditions, context='', special_table=False):
    """Service obligations require service/education context, never a bare تعهد."""
    compact = norm(conditions + ' ' + context).replace(' ', '')
    positive = re.sub(r'(?:عدم|بدون|فاقد)تعهدخدمت', '', compact)
    service = ('تعهدخدمت' in positive
               or bool(re.search(r'تعهد(?:دو|سه|یکونیم|[123])برابر(?:طول)?مدتتحصیل', positive))
               or 'مناطقموردنیازدانشگاه' in positive
               or 'مناطق مورد نیاز دانشکده'.replace(' ', '') in positive)
    if service:
        return 'تعهد خدمت'
    if 'بهیار' in compact:
        return 'سهمیه بهیاران'
    if any(word in compact for word in ('مصاحبه', 'بورس', 'استخدام', 'شرایطخاص')):
        return 'شرایط خاص'
    if 'بومی' in compact:
        return 'بومی'
    return 'شرایط خاص' if special_table else 'عادی'


def table_borders(page):
    # Word's PDF tables draw borders as thin filled rectangles. Using the code
    # cell's real borders avoids stealing multiline text from a neighbouring row.
    return [item[1] for drawing in page.get_drawings() for item in drawing['items']
            if item[0] == 're' and item[1].height < .6 and item[1].width > 15]


def row_bounds(borders, cy, cx0, cx1, fallback):
    ys = sorted({round((rect.y0 + rect.y1) / 2, 3) for rect in borders
                 if rect.x0 <= cx0 and rect.x1 >= cx1})
    before, after = [y for y in ys if y < cy], [y for y in ys if y > cy]
    if before and after:
        return before[-1], after[0], True
    return *fallback, False


def native_context(blocks, top):
    headings = []
    ordered = sorted(blocks, key=lambda block: block[1])
    for index, (x0, y0, x1, y1, text, *_) in enumerate(ordered):
        s = norm(text)
        if y1 <= top + 1 and re.match(r'^(?:ادامه\s+)?(?:مخصوص متقاضیان|پذیرش از تمام|سهمیه مخصوص)', s) and 'بومی' in s:
            # Native headings may be split across PDF text blocks. Keep the
            # covered towns, stopping before table-column headers/next section.
            end = y1
            for following in ordered[index + 1:]:
                more = norm(following[4])
                if not more:
                    continue
                if following[1] - end > 12 or following[3] > top + 1 or any(token in more for token in ('ظرفیت', 'جنس پذیرش', 'عنوان رشته', 'کدرشته', 'توضیحات', 'نحوه پذیرش')):
                    break
                s = norm(s + ' ' + more)
                end = following[3]
            headings.append((y1, s))
    return max(headings, default=(0, ''), key=lambda item: item[0])[1]


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def record_code(row):
    if row.get('code'):
        return str(row['code'])
    match = re.search(r'کدرشته[\s\u200c]*محل منبع:\s*(\d{5})', row.get('notes', ''))
    return match.group(1) if match else ''


def parse_booklet(pdf_paths, pages=None):
    combined = fitz.open()
    for path in pdf_paths:
        with fitz.open(path) as part:
            combined.insert_pdf(part)
    records, candidates, skipped = [], [], []
    carry_heading = None
    # These are the Ministry of Health/Science tables. The following Payam Noor
    # and nonprofit sections are deliberately outside the tool's supported scope.
    pages = range(46, 310) if pages is None else pages
    section = ''
    with combined as pdf:
        for pi in pages:
            page = pdf[pi]
            groups = group_lines(page.get_text('words'))
            blocks = page.get_text('blocks', sort=True)
            borders = table_borders(page)
            # Restrict inherited section context to documented physical ranges;
            # no obligation is carried into subsequent unrelated tables.
            if 146 <= pi < 185:
                section = 'رشته محل های پزشکی و دندان پزشکی دارای تعهد خدمت موضوع مصوبات شورای عالی انقلاب فرهنگی'
            elif 185 <= pi < 194:
                section = 'رشته محل های پزشکی، داروسازی و دندان پزشکی دارای تعهد خدمت موضوع قانون برقراری عدالت آموزشی'
            elif 194 <= pi < 216:
                section = 'رشته محل های سهمیه بومی در رشته های کاردانی و کارشناسی دارای تعهد خدمت مورد نیاز وزارت بهداشت'
            else:
                section = ''
            code_rows = []
            for group in groups:
                # Include shifted 1405 code columns rather than whitelisting
                # numbers or only the older narrow table coordinates.
                hit = digits_run_for_line(group, 320, 510)
                if hit and 320 <= hit[1] <= 485:
                    code_rows.append((group, *hit))
            for index, (g, code, cx0, cx1) in enumerate(code_rows):
                cy = g['cy']
                prevcy = code_rows[index - 1][0]['cy'] if index else cy - 40
                nextcy = code_rows[index + 1][0]['cy'] if index + 1 < len(code_rows) else cy + 40
                top, bottom, geometric = row_bounds(borders, cy, cx0, cx1, ((prevcy + cy) / 2, (cy + nextcy) / 2))
                row_words = [w for gg in groups if top <= gg['cy'] <= bottom for w in gg['words']]
                title = logical_text([w for w in row_words if cx0 - 115 <= w['x0'] < cx0 - 4])
                major = map_major(title)
                candidate = {'code': code, 'source_page': pi + 1, 'title': title, 'major': major or '', 'geometric_bounds': geometric}
                candidates.append(candidate)
                if not major:
                    continue
                if not geometric:
                    skipped.append({**candidate, 'reason': 'Supported title without resolvable code-cell borders'})
                    continue
                male, female = col_value(g, cx0 - 185, cx0 - 162), col_value(g, cx0 - 162, cx0 - 143)
                sem2, sem1 = col_value(g, cx0 - 143, cx0 - 124), col_value(g, cx0 - 124, cx0 - 104)
                n1, n2 = parse_num(sem1), parse_num(sem2)
                if n1 is None and n2 is None:
                    skipped.append({**candidate, 'reason': 'No capacity in semester columns; gender numbers are not a capacity fallback'})
                    continue
                has_m, has_f = male not in ('', '-'), female not in ('', '-')
                gender = 'زن و مرد' if has_m and has_f else ('مرد' if has_m else ('زن' if has_f else ''))
                right = logical_text([w for w in row_words if w['x0'] > cx1 + 3])
                ptype = program_type(right)
                ptype_raw = ptype if ptype != 'در جدول ذکر نشده' else ''
                ptype_source = 'جدول' if ptype_raw else ''
                if 194 <= pi < 216 and not ptype_raw:
                    # Section introduction on PDF p195 explicitly restricts the
                    # new local bachelor/associate quota to daily programmes.
                    ptype = 'روزانه'
                    ptype_source = 'ضوابط سهمیه بومی کاردانی و کارشناسی؛ صفحه PDF 195 (چاپی 194)'
                left_words = [w for w in row_words if w['x1'] < cx0 - 182]
                left = logical_text(left_words)
                if cx0 < 405:
                    uni, prov, carry_heading = regular_institution(blocks, cy, carry_heading)
                    conditions = left
                else:
                    uni, prov = special_institution(left_words), ''
                    conditions = left
                    if not uni:
                        uni, prov, carry_heading = regular_institution(blocks, cy, carry_heading)
                if not uni:
                    skipped.append({**candidate, 'reason': 'University could not be resolved'})
                    continue
                native = native_context(blocks, top)
                context = norm(' '.join(value for value in (section, native) if value))
                category = classify_admission(conditions, context, cx0 >= 405)
                # Retain full row conditions AND native eligibility, even when
                # the primary category is service commitment or interview.
                all_conditions = norm(' | '.join(value for value in (conditions, native, section) if value))
                start = re.search(r'شروع\s*تحصیل\s*(?:مهرماه|مهر|نیمسال اول)?\s*(14\d{2})', conditions)
                start_year = int(start.group(1)) if start else (1406 if 176 <= pi < 185 else 1405)
                for semester, capacity in ((1, n1), (2, n2)):
                    if capacity is None or capacity <= 0:
                        continue
                    records.append({
                        'year': 1405, 'code': code, 'major': major, 'university': uni,
                        'campus': '', 'province': prov, 'program_type': ptype,
                        'program_type_raw': ptype_raw, 'program_type_source': ptype_source,
                        'admission_category': category, 'capacity': capacity, 'gender': gender,
                        'intake': 'نیمسال اول' if semester == 1 else 'نیمسال دوم',
                        'capacity_semester_1': n1 if n1 is not None else '',
                        'capacity_semester_2': n2 if n2 is not None else '',
                        'study_start_year': start_year,
                        'study_start_term': 'مهر' if semester == 1 else 'بهمن',
                        'native_scope': native, 'admission_section': section,
                        'admission_conditions': all_conditions,
                        'source_id': '1405-booklet', 'source_page': pi + 1,
                        'printed_source_page': pi, 'base_source_id': '1405-booklet',
                        'base_source_page': pi + 1,
                        'notes': f'کدرشته‌محل منبع: {code}; عنوان رشته در منبع: {title}'
                    })
    seen = set()
    for row in records:
        identity = (row['code'], row['intake'])
        if identity in seen:
            raise ValueError(f'Duplicate course-location/semester identity: {identity}')
        seen.add(identity)
    return records, candidates, skipped


def statistics(rows):
    categories = collections.Counter(row['admission_category'] for row in rows)
    return {
        'rows': len(rows), 'unique_codes': len({record_code(row) for row in rows}),
        'capacity': sum(int(row['capacity']) for row in rows),
        'major_families': len({row['major'] for row in rows}),
        'categories': dict(categories),
        'native_rows': sum('بومی' in row.get('admission_conditions', '') for row in rows),
        'tuition_rows': sum(any(term in row['program_type'] for term in ('شهریه', 'پردیس', 'خودگردان', 'نوبت دوم')) for row in rows)
    }


def write_csv(path, rows, fields=None):
    fields = fields or list(rows[0])
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def admission_group(row):
    source = row.get('base_source_id') or row.get('source_id', '')
    return next((group for group in ('math', 'humanities') if group in source), 'experimental')


def preserve_other_groups(records, existing):
    """Refresh only experimental rows; a shared code is not a cross-group identity."""
    return records + [row for row in existing if admission_group(row) != 'experimental']


def main():
    root = Path(__file__).resolve().parents[1]
    cli = argparse.ArgumentParser(description='Extract and audit supported experimental capacity tables for admission year 1405')
    cli.add_argument('--pdf', nargs='+', type=Path, default=[root / f'data/raw/sanjesh/experimental/1405/Tajrobi_part_{part}.pdf' for part in (1, 2)])
    cli.add_argument('--output', type=Path, default=root / 'data/capacity/normalized/1405')
    cli.add_argument('--baseline', type=Path)
    cli.add_argument('--historical-root', type=Path, default=root / 'data/capacity/normalized')
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    existing = read_csv(args.output / 'capacities-all.csv')
    before = [row for row in read_csv(args.baseline or args.output / 'capacities-all.csv') if admission_group(row) == 'experimental']
    records, candidates, skipped = parse_booklet(args.pdf)
    if skipped:
        raise ValueError(f'Supported rows were skipped; resolve before publishing: {skipped}')
    old = {(record_code(row), row['intake']): row for row in before}
    current = {(row['code'], row['intake']): row for row in records}
    removed = [key for key in old if key not in current]
    if removed:
        raise ValueError(f'Existing identities disappeared: {removed}')
    audit, extraction_changes = [], []
    semantic_fields = ('major', 'university', 'capacity', 'gender', 'program_type', 'intake')
    for identity, row in current.items():
        previous = old.get(identity)
        if previous and previous['admission_category'] != row['admission_category']:
            audit.append({key: row[key] for key in ('code', 'major', 'university', 'capacity', 'source_page')} | {
                'old_category': previous['admission_category'], 'new_category': row['admission_category'],
                'reason': row['admission_conditions'] or 'No special admission criterion; hostel noncommitment is not service commitment'
            })
        if previous:
            for field in semantic_fields:
                if str(previous[field]) != str(row[field]):
                    extraction_changes.append({'code': row['code'], 'field': field, 'old': previous[field], 'new': row[field], 'source_page': row['source_page'], 'reason': row['program_type_source'] if field == 'program_type' else 'Clipped to actual PDF code-cell borders instead of neighbouring-row midpoints'})
    previous_codes, all_historical_codes, historical_coverage = set(), set(), {}
    for year in range(1401, 1405):
        rows = read_csv(args.historical_root / str(year) / 'capacities-all.csv')
        all_historical_codes.update(record_code(row) for row in rows if record_code(row))
        experimental = [row for row in rows if not any(group in (row.get('base_source_id') or row.get('source_id', '')) for group in ('math', 'humanities'))]
        codes = {record_code(row) for row in experimental if record_code(row)}
        previous_codes.update(codes)
        historical_coverage[year] = {'rows': len(experimental), 'rows_with_code': sum(bool(record_code(row)) for row in experimental), 'unique_codes': len(codes)}
    new_codes = [row for row in records if row['code'] not in previous_codes]
    by, cap = collections.Counter(), collections.Counter()
    for row in records:
        by[row['major']] += 1
        cap[row['major']] += row['capacity']
    summary = {'rows': len(records), 'capacity': sum(row['capacity'] for row in records), 'majors': {major: {'rows': by[major], 'capacity': cap[major]} for major in sorted(by)}}
    after = statistics(records)
    report = {'before': statistics(before), 'after': after, 'classification_changes': len(audit), 'extraction_changes': extraction_changes,
              'new_codes_vs_available_history': len({row['code'] for row in new_codes}), 'history_comparison_group': 'experimental',
              'new_codes_vs_all_groups_history': len({row['code'] for row in records if row['code'] not in all_historical_codes}),
              'historical_code_coverage': historical_coverage,
              'supported_candidates': sum(bool(item['major']) for item in candidates), 'skipped_supported_rows': skipped,
              'pdf_sha256': [hashlib.sha256(path.read_bytes()).hexdigest() for path in args.pdf],
              'page_coverage': {'first_pdf_page': 47, 'last_pdf_page': 310, 'local_service_pages': [195, 216]},
              'delayed_1406_rows': sum(row['study_start_year'] == 1406 for row in records)}
    combined = preserve_other_groups(records, existing)
    fields = list(dict.fromkeys(key for row in combined for key in row))
    write_csv(args.output / 'capacities-all.csv', combined, fields)
    for name in ('capacities-experimental.csv', 'capacities-1405-experimental.csv'):
        write_csv(args.output / name, records)
    write_csv(args.output / 'CLASSIFICATION_AUDIT.csv', audit, ['code', 'major', 'university', 'old_category', 'new_category', 'capacity', 'source_page', 'reason'])
    write_csv(args.output / 'EXTRACTION_AUDIT.csv', extraction_changes, ['code', 'field', 'old', 'new', 'source_page', 'reason'])
    write_csv(args.output / 'NEW_CODES.csv', [{key: row[key] for key in ('code', 'major', 'university', 'intake', 'capacity', 'admission_category', 'source_page')} for row in new_codes], ['code', 'major', 'university', 'intake', 'capacity', 'admission_category', 'source_page'])
    write_csv(args.output / 'CANDIDATE_AUDIT.csv', candidates)
    combined_summary_path = args.output / 'SUMMARY.json'
    combined_summary = json.loads(combined_summary_path.read_text(encoding='utf-8')) if combined_summary_path.exists() else {}
    totals = collections.defaultdict(lambda: {'rows': 0, 'capacity': 0})
    group_totals = collections.defaultdict(lambda: {'rows': 0, 'capacity': 0})
    for row in combined:
        for target, key in ((totals, row['major']), (group_totals, admission_group(row))):
            target[key]['rows'] += 1
            target[key]['capacity'] += int(row['capacity'])
    combined_summary.update(year=1405, rows=len(combined), capacity=sum(int(row['capacity']) for row in combined), majors=dict(sorted(totals.items())))
    combined_summary.setdefault('groups', {}).update(group_totals)
    combined_summary['experimental_audit'] = 'AUDIT_REPORT.md'
    for name, value in (('SUMMARY.json', combined_summary), ('EXPERIMENTAL_SUMMARY.json', summary), ('AUDIT_SUMMARY.json', report), ('unmapped-nontarget-titles.json', collections.Counter(item['title'] for item in candidates if not item['major']))):
        (args.output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
