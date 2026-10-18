# FinStack Logic Variables: Notes

Written 12 Oct 2026. Covers the Kia price lookup, the rules for writing Logic variables in the FinStack tool, and the vehicle-number regex.

---

## 1. Rules for FinStack Logic variables

1. **The library feature does not work inside Logic variables.** Put the data directly in the variable.
2. **Everything is one expression.** No separate statements, no `import` lines, no library calls (`re`, `json`, `math`). Use plain operators, `x if condition else y`, and Python built-ins only.
3. **This applies to calculations too**, not only lookups.
4. **A dictionary pasted as text is a string, not a dict.** The tool shows `... is not of type 'dict'`. The fix is the single-expression form in section 2, where the dictionary is written inside the expression itself.
5. **Test with sample values before pasting.**

---

## 2. Kia ex-showroom price lookup (Bengaluru)

182 variants. Value = ex-showroom price in INR as a plain integer.

### Expression shape

```
{ "snake_case_key": price, ... } if {#common/lead/count#} is not None else { ...same dictionary... }
```

Both branches hold the same dictionary, so the condition does not change the result.

### Key rule (snake_case)

- Lowercase everything.
- Every run of spaces, brackets, dots or hyphens becomes one `_`.
- `+` becomes `plus`, so `HTK+` and `HTK` stay different keys.

| Source name | Key |
|---|---|
| Carens Premium (O) Petrol 1.5L Manual 7 STR | `carens_premium_o_petrol_1_5l_manual_7_str` |
| Seltos HTE Petrol 1.5L Manual | `seltos_hte_petrol_1_5l_manual` |
| Syros EV HTX+ ER 51.4 kWh | `syros_ev_htx_plus_er_51_4_kwh` |

The key is the model and variant joined together, for example `Seltos` + `HTE Petrol 1.5L Manual`.

### Converting a car name to a key, with no library

One expression, tested against all 182 names (every one gave the matching key and price):

```python
"_".join("".join(c if c.isalnum() else " " for c in name.replace("+", " plus ").lower()).split())
```

Example: `Syros EV HTX+ ER  51.4 kWh` gives `syros_ev_htx_plus_er_51_4_kwh`.

### Getting the price

```python
price = prices.get(key)        # returns None if the key is not found
price = prices[key]            # raises an error if the key is not found
```

`syros_ev_htx_plus_er_51_4_kwh` returns `1949900`.

### Files in this folder

| File | What it is |
|---|---|
| `raw.txt` | the pasted list: name, tab, Indian-format price |
| `build.py` | builds the long-name JSON and the Python dictionary from `raw.txt` |
| `kia_prices_bengaluru.json` | long-name keys, 182 entries |
| `kia_prices_bengaluru.py` | the same data as a Python dictionary |
| `snake.py` | converts the long-name keys to snake_case and checks for key clashes |
| `kia_prices_snake.json` | snake_case keys, 182 entries |
| `expr.py` | builds the full if/else expression |
| `kia_prices_expression.txt` | the full expression to paste into the variable (23,449 characters) |

### Checks done

- 182 entries, no duplicate keys, no key clashes after the snake_case conversion.
- `kia_prices_snake.json` loads as a dict in Python.
- Prices were parsed from Indian grouping (`1,29,91,312` becomes `12991312`).

---

## 3. Vehicle number regex

The tool message: `Enter a valid vehicle number (e.g., KA22A0001)`.

The first regex, `^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$`, needs exactly two letters in the series. It rejects `KA01N6576` and the tool's own example `KA22A0001`.

Corrected, series of 1 to 3 letters:

```
^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}$
```

Tested results: `KA01N6576` yes, `KA22A0001` yes, `KA01AB1234` yes, `KA01ABCD1234` no.

Wider version (also allows older plates with fewer digits):

```
^[A-Z]{2}[0-9]{1,2}[A-Z]{0,3}[0-9]{1,4}$
```

Both are case-sensitive, so `ka01n6576` fails unless the input is converted to uppercase first. Neither accepts spaces or dashes, or BH-series plates such as `22BH1234AA`.

| Part | Meaning |
|---|---|
| `[A-Z]{2}` | state code, for example `KA` |
| `[0-9]{2}` | RTO code, for example `01` |
| `[A-Z]{1,3}` | series letters |
| `[0-9]{4}` | number |

---

## 4. Kia total road tax + other charges (Bengaluru)

Same lookup as section 2, but the value is **total road tax + other charges**. It leaves out insurance and TCS.

- Value = `total_road_tax_inr` (base tax + 11% cess on that tax + Rs 1,000 fixed cess) + `registration_other_allowance_inr` (Rs 3,000).
- Key = snake_case of `Car_Type` (model and variant), the same rule and the same 182 keys as the price lookup.
- Example: `carens_premium_o_petrol_1_5l_manual_7_str` gives `213816` (210,816 + 3,000).
- Source: `Desktop\kia_before_insurance_correction.xlsx`, Sheet1 (checked: for every row base tax + cess + fixed cess equals the sheet's total).
- Expression shape, the dummy condition and the dictionary-in-both-branches rule are the same as section 2. The file is one line, about 15,000 characters.

| File | What it is |
|---|---|
| `build_roadtax.py` | reads the xlsx, checks the totals, writes the two files below |
| `kia_roadtax_others_snake.json` | snake_case key to value, 182 entries |
| `kia_roadtax_others_expression.txt` | the expression to paste into the variable |

Use it with the price lookup: the same key gives both the ex-showroom price and the road tax + others. The on-road estimate is price + this value + insurance + TCS.

Limits: the Rs 3,000 is an assumed allowance for registration, plates and similar charges, not an official fee schedule. The tax uses the Karnataka slabs in the workbook, and the EV rates need the commencement notification confirmed.
