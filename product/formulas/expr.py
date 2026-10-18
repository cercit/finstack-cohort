import json

with open("kia_prices_snake.json", encoding="utf-8") as f:
    d = json.load(f)

block = json.dumps(d, indent=4)
expr = block + " if {#common/lead/count#} is not None else " + block

with open("kia_prices_expression.txt", "w", encoding="utf-8") as f:
    f.write(expr)

print(len(d), "keys per branch;", len(expr), "characters")
print(expr[:60].replace("\n", " "), "...")
print("...", expr[-40:].replace("\n", " "))
