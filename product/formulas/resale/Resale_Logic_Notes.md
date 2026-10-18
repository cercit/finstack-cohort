# Used-car resale estimate: notes

Written 12 Oct 2026. Gives an approximate resale value in Rs from three RC fields. Same folder style as `kia_prices`.

---

## 1. What it does

Inputs, all from the RC response:

| Field | Example | Used for |
|---|---|---|
| `vehicle_manufacturer_name` | `MARUTI SUZUKI INDIA LTD` | brand (matched on a word inside the name) |
| `vehicle_cubic_capacity` | `998` | cc band |
| `vehicle_manufacturing_month_year` | `2-2018` (month-year) | age in completed years |

```
value = base[brand][cc band] x retention[completed years]      rounded to the nearest Rs 500
```

- Brands: Maruti Suzuki, Hyundai, Tata, Mahindra, Toyota, Kia. Anything else returns nothing.
- Cars up to 10 years old. Older, or a future date, returns nothing.
- Petrol, diesel, CNG and hybrid. Electric cars have no cc and are left out.
- Show a range of plus or minus 10%. Dealers quote a band, not one number.

## 2. The numbers

**cc bands:** up to 1000, 1001-1300, 1301-1600, 1601-2000, over 2000.

**Retention by completed years (0 to 10):** 90, 80, 70, 60, 50, 44, 38, 32, 26, 22, 20 per cent. Years 0 to 4 follow the insurance depreciation schedule used for insured value. Years 5 to 10 are my assumption of dealer practice. Calibrate them against real listings.

**Brand factor (already inside the base price):** Toyota 1.08, Maruti 1.05, Hyundai 1.00, Kia 1.00, Mahindra 1.00, Tata 0.93.

**Base price:** the median of each model's median current Bengaluru ex-showroom price (each model counts once), for non-electric variants in that brand and cc band. The cc comes from the `Displacement` field in the source pages.

The full table (30 rows, age 0 to 10) is in `resale_table.csv`.

## 3. Two versions

| | Library version | FinStack version |
|---|---|---|
| File | `resale_value.py` | `resale_expression.txt` |
| Libraries | `datetime`, `json`, `re`, `pathlib` | none (Logic variables allow no libraries) |
| Use for | scripts, tests, back end | pasting into a Logic variable |
| Data | `resale_base.json` | dictionary written inside the expression |

The FinStack expression uses the same dictionary-in-both-branches wrapper as the Kia lookup. It has four placeholders to replace with real variable names:
`{#vehicle_manufacturer_name#}`, `{#vehicle_cubic_capacity#}`, `{#vehicle_manufacturing_month_year#}`, and today's year and month (`{#current_year#}`, `{#current_month#}`). I don't know what FinStack calls today's date, so confirm that one first. The expression is 3,567 characters.

## 4. Use it

```python
from resale_value import estimate
estimate("MARUTI SUZUKI INDIA LTD", "998", "2-2018")
# {'value': 161000, 'low': 145000, 'high': 177000, 'oem': 'maruti', 'cc_band': '<=1000', 'age_years': 8, ...}
```

When `value` is `None`, `reason` says why (brand not supported, over 10 years, future date).

Rebuild after changing prices or factors: `python -I build_resale.py`. It rewrites `resale_table.csv`, `resale_expression.txt` and `resale_base.json`. Run the tests with `python test_resale_value.py`.

## 5. Checks done

- 6 tests pass: brand names, cc band edges, age maths, a known value, cases that return nothing, and value falling with age.
- The FinStack expression and the Python version give the same answer on 9 sample cars.
- Sample: Maruti, 998 cc, Feb 2018 gives Rs 1,61,000 (range 1,45,000 to 1,77,000).

## 6. Limits

1. **Today's price as the base.** An old car's base is today's price, higher than what it cost new. Old-car values are probably high.
2. **Small-cc band includes turbo cars** (Venue, Sonet, Taisor), so Hyundai, Kia and Toyota show a higher base there than Maruti.
3. **Copied bands.** Where a brand has no car in a cc band, the base is copied from the nearest band. `resale_table.csv` marks these as "copied".
4. **Not tested inside FinStack.**
5. **Not a quote.** Check against 5 to 10 real listings (Cars24, Spinny, OLX) before it goes in front of a customer.
6. **RC data is personal.** The RC response carries the owner's name, father's name, address and insurance policy number. Use only the three fields above and the owner count. Do not store or pass on the rest.

## 7. Files

| File | What it is |
|---|---|
| `build_resale.py` | builds the table, the JSON and the FinStack expression from the source pages |
| `resale_base.json` | base prices, retention and factors, read by `resale_value.py` |
| `resale_table.csv` | brand x cc band x age 0 to 10 |
| `resale_expression.txt` | the expression for a FinStack Logic variable |
| `resale_value.py` | library version with `estimate()` |
| `test_resale_value.py` | tests |
