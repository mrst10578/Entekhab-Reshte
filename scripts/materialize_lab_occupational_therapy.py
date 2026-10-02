from pathlib import Path
import base64, gzip

root = Path(__file__).resolve().parents[1]
payload_dir = root / "scripts" / ".lab_ot_payloads"
targets = {
    "1401": "data/capacity/normalized/1401/capacities-lab-occupational-therapy.csv",
    "1402": "data/capacity/normalized/1402/capacities-lab-occupational-therapy.csv",
    "1403": "data/capacity/normalized/1403/capacities-lab-occupational-therapy.csv",
    "1404": "data/capacity/normalized/1404/capacities-lab-occupational-therapy.csv",
    "summary": "data/capacity/LAB_OCCUPATIONAL_THERAPY_SUMMARY.json",
    "report": "data/capacity/LAB_OCCUPATIONAL_THERAPY_REPORT.md",
}
for key, rel in targets.items():
    payload = (payload_dir / f"{key}.txt").read_text().strip()
    out = root / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(gzip.decompress(base64.b64decode(payload)))
    print("wrote", rel)
