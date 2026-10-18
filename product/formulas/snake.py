import json
import re

with open("kia_prices_bengaluru.json", encoding="utf-8") as f:
    src = json.load(f)

out, clash = {}, []
for name, price in src.items():
    key = re.sub(r"[^a-z0-9]+", "_", name.replace("+", " plus ").lower()).strip("_")
    if key in out:
        clash.append((key, name))
    out[key] = price

with open("kia_prices_snake.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=4)

print(len(out), "keys; clashes:", clash)
print(json.dumps(out, indent=4))
