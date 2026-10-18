import json
import re

prices, dupes = {}, []
with open("raw.txt", encoding="utf-8") as src:
    for line in src:
        line = line.strip()
        if not line:
            continue
        name, price = line.rsplit(None, 1)
        key = re.sub(r"\s+", " ", name).strip()
        if key in prices:
            dupes.append(key)
        prices[key] = int(price.replace(",", ""))

with open("kia_prices_bengaluru.json", "w", encoding="utf-8") as out:
    json.dump(prices, out, indent=2, ensure_ascii=False)

with open("kia_prices_bengaluru.py", "w", encoding="utf-8") as out:
    out.write("# Kia ex-showroom prices (INR), Bengaluru. Key = 'Model Variant' with single spaces.\n")
    out.write("KIA_EX_SHOWROOM_BENGALURU = {\n")
    for k, v in prices.items():
        out.write("    %r: %d,\n" % (k, v))
    out.write("}\n")

print(len(prices), "entries; duplicate keys:", dupes)
