# FinStack cohort: learning record and the DealerFinance project

**Status:** private draft, still being written.

A five-day fintech product management cohort (9 to 13 Oct 2026, Bengaluru) where we learned how lending companies and no-code lending platforms work, then planned, built, tested and fixed a product. This repo is the record: what I learned, what I built with it, what went wrong, and what I would do next.

**The product:** DealerFinance, a loan journey for new-car buyers at a dealership. It collects consent by OTP, verifies identity through DigiLocker, works out the price and loan, shows which lenders are likely to accept, sends the case to one lender, reroutes after a rejection, and settles the dealer's trade advance and commission. Kia cars, four lenders, built on FinStack's no-code journey builder. All lender terms and figures are test values.

## Where to look

| Folder | What is in it |
|---|---|
| `cohort/` | What we learned: day 1, day 2, the APIs, the no-code platform, consent and rules |
| `product/` | The PRD, the sprint plan, the decisions log, the journey pages and wireframe, and the formulas |
| `testing/` | The raw build log (failures and fixes are being written up) |
| `launch/` | The production launch plan (markdown and pdf) |
| `tools/` | A scanner that checks files for personal data, and a local viewer |

To browse locally: `python tools/serve.py`, then open http://localhost:8765.

## People

- **Sameer S Mittimani** (cercit): product, build, write-ups.
- **Aditya Sharan** ([github.com/aaDhut](https://github.com/aaDhut)): teammate and colleague on Team 6.

## Privacy

Mobile numbers, PAN, Aadhaar numbers, emails, logins and other people's names are not in this repo. `tools/scan_sensitive.py` checks for them before every commit. FinStack's own course material and platform access details are not included; the notes are in my own words.
