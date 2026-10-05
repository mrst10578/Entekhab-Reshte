import fitz,re,unicodedata,csv,json,os,hashlib,collections
PDF='/mnt/data/Tajrobi.pdf'
OUT='/mnt/data/cap1405'
os.makedirs(OUT,exist_ok=True)
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

def digits_run_for_line(g):
    ws=sorted(g['words'],key=lambda z:z['x0'])
    runs=[]; cur=[]
    for w in ws:
        if 345 <= w['x0'] <= 475 and re.fullmatch(r'\d+',w['text']):
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
    patterns=['شهریه پرداز','نوبت دوم','آزاد تمام وقت','خودگردان آزاد','پردیس خودگردان','روزانه','مجازی','روزانه - غیردولتی']
    for p in patterns:
        if p in s:return p
    return 'در جدول ذکر نشده'

pdf=fitz.open(PDF)
ranges=list(range(46,146))+list(range(146,217))+list(range(217,310))
records=[]; all_candidates=[]; carry_heading=None
for pi in ranges:
    page=pdf[pi]; words_raw=page.get_text('words'); groups=group_lines(words_raw); blocks=page.get_text('blocks',sort=True)
    # code lines
    code_rows=[]
    for gi,g in enumerate(groups):
        hit=digits_run_for_line(g)
        if hit:
            code,x0,x1=hit
            # avoid page header/date codes: only plausible table code positions
            if 355<=x0<=465:
                code_rows.append((gi,g,code,x0,x1))
    for idx,(gi,g,code,cx0,cx1) in enumerate(code_rows):
        cy=g['cy']
        prevcy=code_rows[idx-1][1]['cy'] if idx>0 else cy-40
        nextcy=code_rows[idx+1][1]['cy'] if idx+1<len(code_rows) else cy+40
        top=(prevcy+cy)/2; bottom=(cy+nextcy)/2
        # title region
        title_words=[]
        for gg in groups:
            if top<=gg['cy']<=bottom:
                title_words += [w for w in gg['words'] if cx0-115<=w['x0']<cx0-4]
        title=logical_text(title_words)
        major=map_major(title)
        all_candidates.append((pi+1,code,title,major,cx0))
        if not major: continue
        # capacity/gender on same baseline relative to code x
        male=col_value(g,cx0-185,cx0-162)
        female=col_value(g,cx0-162,cx0-143)
        sem2=col_value(g,cx0-143,cx0-124)
        sem1=col_value(g,cx0-124,cx0-104)
        n1,n2=parse_num(sem1),parse_num(sem2)
        capacity=(n1 or 0)+(n2 or 0) if (n1 is not None or n2 is not None) else None
        if capacity is None or capacity<=0:
            gm,gf=parse_num(male),parse_num(female)
            if gm is not None or gf is not None: capacity=(gm or 0)+(gf or 0)
        if not capacity or capacity<=0:
            continue
        has_m=male not in ('','-')
        has_f=female not in ('','-')
        gender='زن و مرد' if has_m and has_f else ('مرد' if has_m else ('زن' if has_f else ''))
        intake='نیمسال اول و دوم' if n1 is not None and n2 is not None else ('نیمسال اول' if n1 is not None else ('نیمسال دوم' if n2 is not None else 'در جدول ذکر نشده'))
        row_words=[w for gg in groups if top<=gg['cy']<=bottom for w in gg['words']]
        right=logical_text([w for w in row_words if w['x0']>cx1+3])
        ptype=program_type(right)
        if cx0<405:
            uni,prov,carry_heading=regular_institution(blocks,cy,carry_heading)
        else:
            left=[w for w in row_words if w['x1']<cx0-182]
            uni=special_institution(left)
            prov=''
            if not uni:
                # nearest heading as fallback
                uni,prov,carry_heading=regular_institution(blocks,cy,carry_heading)
        if not uni:
            continue
        conditions=logical_text([w for w in row_words if w['x1']<cx0-182]) if cx0<405 else ''
        special = cx0>=405 or any(k in conditions for k in ['مصاحبه','بورس','ویژه','تعهد'])
        records.append({
          'year':1405,'major':major,'university':uni,'campus':'','province':prov,
          'program_type':ptype,'program_type_raw':ptype if ptype!='در جدول ذکر نشده' else '',
          'admission_category':'شرایط خاص' if special else 'عادی','capacity':capacity,'gender':gender,
          'intake':intake,'admission_conditions':conditions if len(conditions)<500 else conditions[:500],
          'source_id':'1405-booklet','source_page':pi+1,'base_source_id':'1405-booklet','base_source_page':pi+1,
          'notes':f'کدرشته‌محل منبع: {code}; عنوان رشته در منبع: {title}'
        })

# dedupe exact code/page identity
seen=set(); ded=[]
for r in records:
    key=(r['source_page'],re.search(r'\d{5}',r['notes']).group(),r['major'])
    if key not in seen: seen.add(key); ded.append(r)
records=ded
fields=['year','major','university','campus','province','program_type','program_type_raw','admission_category','capacity','gender','intake','admission_conditions','source_id','source_page','base_source_id','base_source_page','notes']
for name in ['capacities-1405-experimental.csv','capacities-all.csv']:
    with open(os.path.join(OUT,name),'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
# summary stats
by=collections.Counter(); cap=collections.Counter()
for r in records: by[r['major']]+=1;cap[r['major']]+=r['capacity']
summary={'rows':len(records),'capacity':sum(r['capacity'] for r in records),'majors':{m:{'rows':by[m],'capacity':cap[m]} for m in sorted(by)}}
open(os.path.join(OUT,'summary.json'),'w',encoding='utf8').write(json.dumps(summary,ensure_ascii=False,indent=2))
# diagnostics
unmapped=collections.Counter(t for _,_,t,m,_ in all_candidates if t and not m)
open(os.path.join(OUT,'unmapped_titles.json'),'w',encoding='utf8').write(json.dumps(unmapped,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('unmapped unique',len(unmapped),'top',unmapped.most_common(40))
