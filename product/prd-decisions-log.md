# DealerFinance: decisions log

The design decisions we made, one line each, and what happened to them. The full original log (F1 to F26, with the "do" and "don't" lists) is in [archive/prd-decisions-full.md](archive/prd-decisions-full.md).

## How the logic was built without a database

FinStack gave us forms and journeys but no database or lending system. So every calculation and rule sits in a **logic variable**: a short Python expression that FinStack runs inside the journey. These did most of the work:

- **Auto-fill calculations:** price, road tax, insurance, TCS, on-road price, loan value, LTV and the finance amount follow from the car and the down payment.
- **Complex drop-downs and lookups:** the Kia model list, price and road-tax tables, trade advance limits and commission rates are dictionaries inside expressions.
- **Locked fields:** pre-filled values (PAN, prices, loan) are read-only, so the executive cannot overwrite them.
- **Conditional fields:** the vehicle number appears only when the customer has an exchange car; the approved amount appears only when the lender approves.
- **Rules:** credit health, the fit label for each lender, the name and PAN checks, age from date of birth, and the exchange-value estimate.

The limits: each variable is one expression, with no libraries and restricted imports, so some ideas (a fuzzy-match library, today's date) had to be rebuilt from plain functions. The expressions themselves are in `product/formulas/formulas.md` in the repository.

## Decisions

| ID | Decision | Why | What happened |
|---|---|---|---|
| F1 | The dealer principal owns the account and gives logins to the finance coordinator, sales executives and CRM staff. Every action is logged | Clear ownership and a trail | Not built (no login on the platform) |
| F2 | "Send to lender" is a permission, by default the finance coordinator's, or whoever does that job | Small dealers combine roles | Not built |
| F3 | Leads arrive three ways: CRM file, walk-in with a code on the customer's phone, or a self-fill link | Assisted and self-serve | One journey for both, built |
| F4 | No consent, no credit check: the lead waits | RBI rules on credit reports | Built (terms tick plus code). Open: how long to keep on-hold data (30 days suggested) |
| F5 | Light identity check at the dealer stage: lookup on name and mobile, PAN only if no hit, name match as a warning | Keep KYC light | Replaced by F16 |
| F6 | Income is declared by the customer (monthly income or comfortable EMI) and labelled "declared, not verified" | The dealer does not verify income | Built |
| F7 | Lender fit is a simple checklist per lender, giving "likely, possible or not a fit", never a decision | The dealer does not underwrite | Built as one formula |
| F8 | Lender staff update the case stages: sent, under approval, approved or rejected, sanctioned, disbursed | Live status for the dealer | Not built; status set by hand |
| F9 | Commission is worked out per case from the lender's rate, then claimed with GST and TDS and ticked as received | Gives the dealer a daily reason to use the tool | The commission figure is built; the ledger is not |
| F10 | The principal's home screen shows funnel, lender scorecard, commission tracker and reroute view | See what lenders really do | Not built |
| F11 | Up to three lenders automatically; a fourth needs the principal's approval; the customer is told each time | Limits enquiries on the customer's report | Reroute built; the cap is not |
| F12 | Track each lender's trade advance room and show it as a tag | Dealers want funded lenders used | Built with demo limits |
| F13 | Rank by customer preference, then trade advance | Superseded by F25 | Replaced |
| F14 | Include everything in the first build | Scope to be cut later | Replaced by F20, then by the one-journey change |
| F15 | Consent is one line on the enquiry form, confirmed by a code; no separate consent message | "Subtle" finance scores highest and stays compliant | Built |
| F16 | DigiLocker KYC before the case is sent | Identity and address without document copies | Built |
| F17 | A bank statement step for lenders that need income proof (upload and analysis, not Account Aggregator) | Verified income where needed | Planned |
| F18 | One manual review queue for edge cases (weak name match, no credit hit, possible fit, overrides, a fourth lender) | The brief asked for manual approval of edge cases | Planned |
| F19 | More credit data in the fit rules: recent enquiries, late payments, pin code band | Better fit | Credit health built; the rest not |
| F20 | Build onboarding, match and send first; the commission ledger and lender portal later | Platform is built for onboarding | Superseded by F26 |
| F21 | A lead lender deploys it at its partner dealers | First idea of who runs it | Replaced by F22 |
| F22 | Dealers are the paying customer (a software fee) | The dealer has the pain and the budget | Fee is an assumption |
| F23 | The credit report is used only to route; it is not passed to lenders | Keeps the dealer stage compliant | Built |
| F24 | We differ from carmaker finance portals: dealer-side, multi-brand, and showing trade advance, commission and lender speed | A real gap | Pitch point |
| F25 | Rank by fit, then the customer's choice, then lowest EMI. Dealer factors are tags and tie-breakers only | Do not push the customer to a costlier lender | Fit and tags built |
| F26 | Trade advance, commission and lender speed go into the build as tags | They are what set us apart | Trade advance and commission built; speed not |

## What changed on 13 October

The platform had no dealer login, database or menu setup, so the design became **one linear journey** used by the customer or a dealer executive. Cars are Kia only and there are four lenders. One-time-code consent and DigiLocker were built. The review queue, lender portal, ledger and dashboard were not. See the [PRD](prd.md) for what was built and the [launch plan](../launch/production-launch-plan.md) for what comes next.

## Still open

- How long to keep the data of a lead that gave no consent.
- Whether FinStack's bureau access can serve a dealer, who is not a lender.
