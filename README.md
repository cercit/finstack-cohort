# FinStack cohort: learning record and the DealerFinance project

**Status:** private draft. Core notes, PRD, sprint plan, testing notes and launch plan are written; a few pieces are still being reviewed.

**Please read first:** lender names, rates, limits and thresholds here are invented test values, not any lender's real policy. Car prices are demo listings. See `LICENSE` and `REDACTION.md`.

A five-day fintech product management cohort (9 to 13 Oct 2026, Bengaluru) where I learned how lending companies and no-code lending platforms work, then planned, built, tested and fixed a product. This repo is the record: what I learned, what I built with it, what went wrong, and what I would do next.

**The product:** DealerFinance, a loan journey for new-car buyers at a dealership. It collects consent by OTP, verifies identity through DigiLocker, works out the price and loan, shows which lenders are likely to accept, sends the case to one lender, reroutes after a rejection, and settles the dealer's trade advance and commission. Kia cars, four lenders, built on FinStack's no-code journey builder. All lender terms and figures are test values.

## Where to look

| Folder or file | What is in it |
|---|---|
| `cohort/` | What we learned: day 1, day 2, days 3 to 5, the APIs, the no-code platform, consent and rules |
| `product/` | The PRD, sprint plan, decisions log, journey pages and wireframe, formulas, and a masked demo clip |
| `testing/` | Failures and fixes, and the lessons from the live demo |
| `launch/` | The production launch plan (markdown and pdf) |
| `learned-to-used.md` | Each class topic linked to where we used it in the product |
| `REDACTION.md` | What was removed from the repo and how it was checked |
| `tools/` | A scanner that checks files for personal data, and a local viewer |

To browse locally: `python tools/serve.py`, then open http://localhost:8765.

## People

- **Sameer S Mittimani** (cercit): product, PRD, sprint plan, no-code build, testing and write-ups.
- **Aditya Sharan** ([github.com/aaDhut](https://github.com/aaDhut)): teammate and colleague on Team 6.

## Privacy

Mobile numbers, PAN, Aadhaar numbers, emails, logins and other people's names are not in this repo. `tools/scan_sensitive.py` checks for them before every commit. FinStack's own course material and platform access details are not included; the notes are in my own words.
