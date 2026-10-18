# DealerFinance: all formulas and codes (13 Oct 2026)

Every FinStack formula we settled, in one place. Variable names in `{#primary/logic_variable/...#}` are the ones used in the journey; the few marked **guess** were never confirmed, so check them against FinStack. All were tested in Python only, not inside FinStack.

Rules that apply to every formula: no libraries, one expression, always bracket a dictionary before `.get(...)`, and after a refresh a value can arrive as text.

---

## 1. Car price and road tax (Kia only)

| Variable | Default value | Where it is saved |
|---|---|---|
| `DUMMY` | Kia price dictionary (182 variants, key = snake_case of model + variant) | `Desktop\Claude\kia_prices\kia_prices_expression.txt` |
| `Roadtax` | Kia road tax + others dictionary | `Desktop\Claude\kia_prices\kia_roadtax_others_expression.txt` |

`exshow`:
```
({#primary/logic_variable/DUMMY#}).get({#primary/custom-externalapi-verification_<id>/car_model#}, -1)
```

`Road_Tax`:
```
({#primary/logic_variable/Roadtax#}).get({#primary/custom-externalapi-verification_<id>/car_model#}, -1)
```

Road tax + others = total road tax (base tax + 11% cess + Rs 1,000) + Rs 3,000. Notes and the name-to-key rule: `kia_prices\FinStack_Logic_Notes.md`.

## 2. Customer_Inputs

`insurance` (4% of ex-showroom):
```
round({#primary/logic_variable/exshow#} * 0.04) if {#primary/logic_variable/exshow#} > 0 else -1
```

`tcs` (1% when ex-showroom is above Rs 10 lakh; no round, no float):
```
{#primary/logic_variable/exshow#} / 100 if {#primary/logic_variable/exshow#} > 1000000 else 0 if {#primary/logic_variable/exshow#} > 0 else -1
```
If TCS drops to 0 after a refresh, the value is arriving as text: use `int({#primary/logic_variable/exshow#})` in both places.

`onroad` (TCS not included; **guess** the variable names `insurance`, `Road_Tax`):
```
{#primary/logic_variable/exshow#} + {#primary/logic_variable/insurance#} + {#primary/logic_variable/Road_Tax#} if {#primary/logic_variable/exshow#} > 0 and {#primary/logic_variable/Road_Tax#} > 0 else -1
```

`loan` (**guess** `downpayment`, `exchange_value`):
```
max({#primary/logic_variable/onroad#} - {#primary/logic_variable/tcs#} - {#primary/logic_variable/downpayment#} - {#primary/logic_variable/exchange_value#}, 0) if {#primary/logic_variable/onroad#} > 0 else -1
```
Wrap in `int(...)` to remove a trailing ".0".

`ltv` (loan against the ex-showroom price):
```
round({#primary/logic_variable/loan#} / {#primary/logic_variable/exshow#} * 100, 1) if {#primary/logic_variable/exshow#} > 0 else -1
```

Exchange value default when the customer says No (**guess** `exchange`):
```
0 if "{#primary/logic_variable/exchange#}" == "No" else ""
```

## 3. Credit health

`credit_health` (Bad: any suit-filed balance, any default account, or outstanding above Rs 25 L. Best: outstanding up to Rs 10 L. Otherwise Good). Needs `suit_filed_current_balance`, `default_account`, `total_outstanding_balance` from the bureau response (**guess** variable names `suit_bal`, `default_acc`, `outstanding`):
```
"Bad" if {#primary/logic_variable/suit_bal#} > 0 or {#primary/logic_variable/default_acc#} > 0 or {#primary/logic_variable/outstanding#} > 2500000 else "Best" if {#primary/logic_variable/outstanding#} <= 1000000 else "Good"
```

## 4. Decision: fit for sbi, hdfc, bajaj, chola (single formula, four inputs)

Variable `decision`. Inputs: `score`, `credit_health`, `net_commit` (net monthly commitment, Rs), `loan`, plus `customer_pick`. Returns six parts joined with `|`: sbi, hdfc, bajaj, chola, customer choice, default card. Read a part with `{#primary/logic_variable/decision#}.split("|")[0]` to `[5]`. Uses the `for x in [value]` trick, tested in Python only.

| | sbi | hdfc | bajaj | chola |
|---|---|---|---|---|
| Not a fit if score below | 750 | 700 | 650 | 650 |
| Likely needs score of at least | 770 | 720 | 670 | 670 |
| Not a fit if commitment above | 25,000 | 30,000 | 40,000 | 40,000 |
| Likely needs commitment of at most | 15,000 | 20,000 | 30,000 | 30,000 |
| Not a fit if loan above | 30 L | 30 L | 25 L | 25 L |
| Likely needs health Best | yes | yes | no | no |

Credit health Bad is "not a fit" everywhere. Chola uses Bajaj's rules (assumed). The full text is saved in `DealerFinance-formulas-decision.txt` (same folder) so it can be copied whole.

## 5. Trade advance, used and commission (Routing-2 and Settlement)

The lender key is `{#primary/custom-externalapi-routing_2_<id>/request_body#sent_to#}`. Use `.lower()` after it if the saved value has capitals.

`trade_advance` (limits: sbi Rs 2 Cr, hdfc Rs 1 Cr, bajaj Rs 75 L, chola Rs 50 L):
```
({"sbi": 20000000, "hdfc": 10000000, "bajaj": 7500000, "chola": 5000000}).get({#primary/custom-externalapi-routing_2_<id>/request_body#sent_to#}.lower(), 0)
```

`trade_used` (demo values: sbi 60 L, hdfc 35 L, bajaj 20 L, chola 10 L; no database, so these are fixed):
```
({"sbi": 6000000, "hdfc": 3500000, "bajaj": 2000000, "chola": 1000000}).get({#primary/custom-externalapi-routing_2_<id>/request_body#sent_to#}.lower(), 0)
```

`fin_amt` (the approved finance amount if it is above 1, otherwise the loan requirement):
```
{#primary/custom-externalapi-routing_2_<id>/approved_finance_amount#} if {#primary/custom-externalapi-routing_2_<id>/approved_finance_amount#} > 1 else {#primary/custom-externalapi-routing_1_<id>/loan_requirement#}
```
Safe version if the amount can be blank or text:
```
int(float("{#primary/custom-externalapi-routing_2_<id>/approved_finance_amount#}" or 0)) if int(float("{#primary/custom-externalapi-routing_2_<id>/approved_finance_amount#}" or 0)) > 1 else {#primary/custom-externalapi-routing_1_<id>/loan_requirement#}
```

`fin_comm` (sbi 1.4%, hdfc 1.8%, bajaj 2.5%, chola 3% of the finance amount; drop `round` for decimals):
```
round(({"sbi": 1.4, "hdfc": 1.8, "bajaj": 2.5, "chola": 3}).get({#primary/custom-externalapi-routing_2_<id>/request_body#sent_to#}.lower(), 0) * {#primary/logic_variable/fin_amt#} / 100)
```

Settlement arithmetic seen on Step 6:
- Additional downpayment = loan requirement - approved amount (never below 0)
- Balance trade advance = trade advance - trade used - approved amount

Routing rule: status `rejected` goes back to Step 4; status `approved` goes on to Step 6.

## 6. Regex

| Field | Pattern |
|---|---|
| Mobile | `^[6-9]\d{9}$` |
| PAN | `^[A-Z]{3}P[A-Z][0-9]{4}[A-Z]$` |
| Vehicle number | `^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}$` (accept "NA" with `^(NA\|[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4})$`) |
| Percentage (string) | `^(100(\.0+)?\|[0-9]{1,2}(\.[0-9]+)?)%$` |

## 7. Vehicle valuation (exchange value) and other code

- Resale estimate from brand, engine size and manufacturing month-year (Maruti Suzuki, Hyundai, Tata, Mahindra, Toyota, Kia, up to 10 years old): `Desktop\Claude\resale_value\` (`resale_value_standalone.py` for scripts, `resale_expression.txt` for a Logic variable, `Resale_Logic_Notes.md`).
- Trade advance, used and commission demo values are not any lender's real terms.

## 8. Pending (API or access)

PAN autofill, credit score (bureau API), exchange value (asset API), the financier send, and the back-office listing page ("My cases").

## 9. Where everything is

| What | Path |
|---|---|
| Build log: screens 1 to 6 as built, learnings, pending items | `Hackathon\DealerFinance-build-log.md` |
| Pitch page for the presentation | `Hackathon\DealerFinance-pitch.html` (rebuild with `_build\build_pitch.py`) |
| Overview page and flow diagram | `Hackathon\DealerFinance-overview.html` |
| Dealer screens design (reference only) | `Hackathon\DealerFinance-dealer-portal.html` |
| Starter data and workbook (Aditya) | `Hackathon\adity_cohort_prod\delivred\` |
| Decisions F1 to F26 | `Hackathon\DealerFinance-PRD-decisions.md` |
| Kia lookups and logic notes | `Desktop\Claude\kia_prices\` |
| Resale code | `Desktop\Claude\resale_value\` |
| Other-brand lookups (not wanted; delete or keep) | `Desktop\Claude\car_lookups\` |
