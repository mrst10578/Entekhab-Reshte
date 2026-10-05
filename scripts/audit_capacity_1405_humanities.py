#!/usr/bin/env python3
# rerun marker after parser cleanup
import csv, json, re, subprocess, tempfile
from collections import Counter, defaultdict
from pathlib import Path

PDF = Path("data/raw/sanjesh/humanities/1405/Ensani.pdf")
CSV = Path("data/capacity/normalized/1405/capacities-humanities.csv")
OUT = Path("data/capacity/audit/humanities-1405-audit.json")
TRANS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
BIDI = ("\u202b","\u202c","\u202a","\u202d","\u202e","\u200f","\u200e","\ufeff","\u2066","\u2067","\u2068","\u2069")
ALIASES = {
"حقوق":["حقوق"],"روان‌شناسی":["روانشناسی","روان شناسی"],"مشاوره":["مشاوره"],"علوم تربیتی":["علوم تربیتی"],
"آموزش ابتدایی":["آموزش ابتدایی"],"حسابداری":["حسابداری"],"اقتصاد":["اقتصاد"],"مدیریت بازرگانی":["مدیریت بازرگانی"],
"مدیریت دولتی":["مدیریت دولتی"],"مدیریت صنعتی":["مدیریت صنعتی"],"مدیریت مالی":["مدیریت مالی"],"علوم سیاسی":["علوم سیاسی"],
"جامعه‌شناسی":["جامعهشناسی","جامعه شناسی"],"مددکاری اجتماعی":["مددکاری اجتماعی"],"علوم ورزشی":["علوم ورزشی"],
"زبان و ادبیات فارسی":["زبان و ادبیات فارسی"],"جغرافیا":["جغرافیا"],"تاریخ":["تاریخ"],"گردشگری":["گردشگری"],
"علم اطلاعات و دانش‌شناسی":["علم اطلاعات و دانششناسی","علم اطلاعات و دانش شناسی","علم اطالعات و دانششناسی","علم اطالعات و دانش شناسی"],
}
PROGRAMS = ["پردیس خودگردان","پردیسخودگردان","شهریه پرداز","شهریه‌پرداز","روزانه - غیردولتی","روزانه- غیردولتی","روزانه -غیردولتی","روزانه-غیردولتی","نوبت دوم","روزانه","مجازی","پیام نور","غیرانتفاعی"]
ADMISSIONS = ["صرفا با سوابق تحصیلی","صرفاً با سوابق تحصیلی","با آزمون"]

def clean(s):
    for ch in BIDI: s=s.replace(ch,"")
    s=s.translate(TRANS).replace("ي","ی").replace("ك","ک").replace("ۀ","ه").replace("ة","ه").replace("‌"," ")
    return re.sub(r"\s+"," ",s).strip()

def norm(s): return clean(s).replace("ـ","").strip(" .،؛:-")

with tempfile.NamedTemporaryFile(suffix=".txt") as temp:
    subprocess.run(["pdftotext","-layout",str(PDF),temp.name],check=True)
    pages=Path(temp.name).read_text(encoding="utf-8",errors="ignore").split("\f")

source_by_code={}
independent_codes={}
for pno in range(42,401):
    for raw in pages[pno-1].splitlines():
        line=clean(raw)
        m=re.search(r"(?<!\d)(\d{5})(?!\d)",line)
        if not m: continue
        code=m.group(1)
        source_by_code.setdefault(code,[]).append({"page":pno,"line":line})
        left,right=line[:m.start()].strip(),line[m.end():].strip()
        # Strict independent exact-title recognizer.
        for major, aliases in ALIASES.items():
            if pno>=147 and major not in ("آموزش ابتدایی","علوم ورزشی"):
                continue
            matched=False
            for alias in aliases:
                a=norm(alias)
                rr=norm(right)
                if rr==a or rr.startswith(a+" ") or rr.startswith(a+"("):
                    matched=True
                # Some PDF rows reorder title to the left of the code.
                ll=norm(left)
                if ll==a or ll.endswith(" "+a):
                    matched=True
            if matched:
                independent_codes[code]={"major":major,"page":pno,"line":line}
                break

with CSV.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))

current={}
duplicates=[]
for row in rows:
    m=re.search(r"کدرشته[\s\u200c]*محل منبع:\s*(\d+)",row.get("notes",""))
    code=m.group(1) if m else None
    if not code: continue
    if code in current: duplicates.append(code)
    current[code]=row

extra=sorted(set(current)-set(independent_codes))
missing=sorted(set(independent_codes)-set(current))

def row_summary(code):
    row=current.get(code,{})
    src=source_by_code.get(code,[])
    return {
        "code":code,"major":row.get("major"),"university":row.get("university"),"campus":row.get("campus"),
        "province":row.get("province"),"program_type":row.get("program_type"),"capacity":row.get("capacity"),
        "gender":row.get("gender"),"intake":row.get("intake"),"admission_conditions":row.get("admission_conditions"),
        "source_page":row.get("source_page"),"source_lines":src[:3],
    }

digit_only_conditions=[row_summary(code) for code,row in current.items() if re.fullmatch(r"[\d\s\-]+", row.get("admission_conditions","").strip() or "X")]
unbalanced=[]
for code,row in current.items():
    for field in ("university","campus"):
        v=row.get(field,"")
        if v.count("(")!=v.count(")") or v.count("[")!=v.count("]"):
            unbalanced.append({"code":code,"field":field,"value":v,"major":row.get("major"),"page":row.get("source_page")})
            break

weird_university=[]
for code,row in current.items():
    u=row.get("university","")
    if len(u)>140 or re.search(r"\b(ظرفیت|کدرشته|نحوه پذیرش|عنوان رشته)\b",u) or re.search(r"\d{3,}",u):
        weird_university.append(row_summary(code))

major_counts=Counter(r["major"] for r in rows)
program_counts=Counter(r["program_type"] for r in rows)
source_counts=Counter(r["source_id"] for r in rows)

report={
    "rows":len(rows),"unique_codes":len(current),"duplicate_codes":sorted(set(duplicates)),
    "independent_exact_target_codes":len(independent_codes),
    "extra_vs_independent":[row_summary(c) for c in extra],
    "missing_vs_independent":[{"code":c,**independent_codes[c]} for c in missing],
    "digit_only_admission_conditions_count":len(digit_only_conditions),
    "digit_only_admission_conditions_sample":digit_only_conditions[:50],
    "unbalanced_name_count":len(unbalanced),"unbalanced_name_sample":unbalanced[:100],
    "weird_university_count":len(weird_university),"weird_university_sample":weird_university[:100],
    "major_counts":dict(major_counts),"program_counts":dict(program_counts),"source_counts":dict(source_counts),
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({
 "rows":report["rows"],"unique_codes":report["unique_codes"],"independent":report["independent_exact_target_codes"],
 "extra":len(extra),"missing":len(missing),"digit_conditions":len(digit_only_conditions),
 "unbalanced":len(unbalanced),"weird_university":len(weird_university)
},ensure_ascii=False))
