from pathlib import Path
import base64, gzip

root = Path(__file__).resolve().parents[1]
chunk_dir = root / "scripts" / ".health3_payloads" / "chunks"
groups = {
    "1402": ["1402_00.txt","1402_01.txt","1402_02.txt","1402_03.txt"],
    "1403": ["1403_00.txt","1403_01.txt","1403_02.txt","1403_03.txt"],
    "1404": ["1404_00.txt","1404_01.txt","1404_02.txt","1404_03.txt"],
}
for year, parts in groups.items():
    payload = "".join((chunk_dir / p).read_text().strip() for p in parts)
    raw = gzip.decompress(base64.b64decode(payload))
    out = root / "data" / "capacity" / "normalized" / year / "capacities-public-environmental-occupational-health.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print("wrote", out, len(raw))
