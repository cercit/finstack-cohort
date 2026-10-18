# DealerFinance: product requirements document (PRD)

**Status:** draft for review, written 18 Oct 2026 from the work done in the FinStack cohort (9 to 13 Oct 2026).
**Team 6:** Sameer S Mittimani and Aditya Sharan.
**Format:** the execution-ready PRD template from Class 9, trimmed to the sections that apply. Evidence tags: **[Built]** works in the FinStack journey today; **[Planned]** designed, not built; **[Assumption]** our guess, not tested; **[Test value]** a demo number, not a lender's real term. No research is claimed beyond what the team saw and did.

The earlier decisions log (F1 to F26) is kept in `prd-decisions-log.md`. That log was written for a bigger design. This PRD describes what was built and what comes next.

---

## 1. Overview

DealerFinance is a loan journey for a new-car buyer, run by a dealership sales executive or by the customer. It collects consent, verifies identity, works out the price and loan amount, checks which lenders are likely to accept the case, sends it to one lender, follows the lender's answer and settles the dealer's trade advance and commission. It is built on FinStack's no-code journey builder. Scope for the hackathon: Kia cars in Bengaluru, four lenders (sbi, hdfc, bajaj, chola).

## 2. Background

- A dealership sells the car and also arranges the loan. The executive talks to several lenders by phone or app, one after another. [Assumption, from the team's finance experience]
- The dealer is paid a commission by the lender and often holds a trade advance (stock funding) with some lenders. Those limits and commissions are tracked outside the sales process, in accounts. [Assumption]
- A rejected loan costs the dealer a sale unless the case is quickly moved to another lender. [Assumption]
- Why now: FinStack gives credit report, KYC, DigiLocker, vehicle and bank-statement APIs behind a no-code builder, so a dealer-side tool can be built without a lending system of our own. [Built, cohort learning]

## 3. Problem

| Part | Statement |
|---|---|
| User | The dealership executive, and the buyer sitting in front of them |
| Task | Find a lender who will fund this customer and this car, and close the sale |
| Cause | Lender fit is checked by calling around; price, tax, insurance and exchange value are worked out by hand; the customer's data is typed again for each lender |
| Consequence | Slow answers, wrong loan amounts, repeat typing, cases dropped after a rejection |
| Business effect | Lost car sales, and commission and trade advance that are not tracked case by case |

## 4. Users

| User | Role | Job to be done |
|---|---|---|
| Sales or finance executive (primary) | Fills the journey for the customer | "When a buyer says they want finance, I want a lender and an exact cash figure in minutes, so the sale does not stall." |
| Customer (secondary) | Gives consent, completes KYC | "I want to know what I need to pay, without sharing my documents with five people." |
| Dealer principal (buyer of the tool) | Pays for it | "I want to see which lenders approve, how fast, and what commission and trade advance I have left." [Planned] |
| Lender (outside the journey) | Receives the case, answers approved or rejected | Not a user of this product yet. [Planned] |

Evidence: the personas come from the team's own working knowledge, not from interviews. Interviews with dealers are an open item (section 21).

## 5. Goals and non-goals

**Goals**
1. A customer or executive can finish the journey with minimal typing. Most fields pre-fill from APIs, rules or the dealer's quote. [Built, partly]
2. The executive sees which lenders are open for this case, and can reroute after a rejection. [Built]
3. The exact cash the customer needs (down payment plus any gap to the approved amount) is shown before the sale is closed. [Built]
4. The dealer's trade advance balance and commission are shown per case. [Built with demo values]

**Non-goals (deliberately out for now)**
- No credit decision, sanction promise or approved amount from DealerFinance itself. The lender decides.
- No loan servicing or collections.
- No database or lending system of our own. FinStack's journey, listing and back office are used as they are.
- No brands other than Kia in the demo.
- No dealer login or separate dealer portal. One journey serves the customer and the executive.

## 6. Principles

- Consent first: no credit report is pulled before the customer agrees and confirms by OTP on their own phone.
- Ask for less: every field that can be filled from an API, a rule or the dealer's quote should be.
- A "not available" answer is a valid answer: every outside call has a path that shows a plain label and moves on (lesson from the live demo).
- Show the dealer's money next to the customer's: commission and trade advance are visible, but never change the customer's choice silently.

## 7. Journey: before and after

**Before:** enquiry in a CRM or notebook > call lenders > collect documents > wait > repeat if rejected.

**After (as built):** Enquiry with OTP > DigiLocker > Verification > Customer_Inputs > Routing-1 > Routing-2 > Settlement. A rejected case goes from Routing-2 back to Routing-1. [Built]

## 8. Proposed solution: the six steps

| Step | What happens | Typed or filled |
|---|---|---|
| 1 Enquiry | Customer name, mobile, terms tick, then a 6-digit code to the customer's phone | Typed |
| DigiLocker | Aadhaar OTP through DigiLocker; PAN name, number and date of birth come back | Filled |
| 2 Verification | PAN (pre-filled), employment, monthly income, monthly EMI commitment, down payment, income proof yes or no, Kia model, exchange yes or no, vehicle number only if exchange is yes | Mostly typed |
| 3 Customer_Inputs | Ex-showroom price, road tax, insurance, TCS, on-road price, loan value, exchange value | All pre-filled |
| 4 Routing-1 | Loan requirement, credit score (or NTC), LTV, choice of lender | Filled, one pick |
| 5 Routing-2 | What the lender sees; status approved or rejected; approved amount when approved | Status picked by hand today |
| 6 Settlement | Additional down payment, trade advance limit and used, balance, commission | All pre-filled |

## 9. Functional requirements

Priority: **P1** must work for the journey to complete; **P2** needed for launch; **P3** later.

| ID | Behaviour | Priority | Why | Acceptance | Status |
|---|---|---|---|---|---|
| FR-01 | Collect name, mobile, terms tick; send a 6-digit code to the customer's phone; continue only on a correct code | P1 | Consent before any check | Wrong code blocks; correct code opens DigiLocker | [Built] |
| FR-02 | Validate mobile as 10 digits starting 6 to 9 | P1 | Stop bad data early | `^[6-9]\d{9}$` | [Built] |
| FR-03 | DigiLocker redirect and return; store PAN name, PAN number, date of birth | P1 | KYC and pre-fill | Return lands on Step 2 with PAN filled | [Built] |
| FR-04 | Compare typed name with the PAN name; compare typed PAN with the PAN from DigiLocker | P2 | Catch wrong identity | Name match score and PAN 100 or 0 shown; mismatch rule: name below 90% and PAN below 100% | [Built as expressions; not tied to a screen] |
| FR-05 | Work out age from date of birth | P2 | Age rule for lenders | Whole years, birthday-aware | [Built as expression] |
| FR-06 | Price, road tax, insurance, TCS and on-road price for the chosen Kia variant | P1 | Loan base | See section 11 | [Built] |
| FR-07 | Loan value = on-road price less TCS, down payment and exchange value | P1 | Loan amount | Matches section 11 | [Built; a defect found, see section 13] |
| FR-08 | Exchange value from vehicle number: brand, engine size and age | P2 | Fill the exchange field | Rule in section 11 | [Rule built; asset API pending] |
| FR-09 | Credit score from the bureau; show "NTC" when no score returns | P1 | Lender fit | NTC case carries on to NTC-accepting lenders only | [Score built; NTC path built after the demo] |
| FR-10 | Credit health Bad, Good or Best from suit-filed balance, defaults and total outstanding | P2 | Lender fit | Section 11 | [Built as expression; hidden on screen] |
| FR-11 | Fit label per lender: likely, possible, not a fit | P1 | Pick a lender | Section 11 | [Built as one formula] |
| FR-12 | Send to one lender; record status approved or rejected | P1 | Core flow | Rejected returns to Routing-1 | [Built; status by hand] |
| FR-13 | Approved amount replaces the requested loan when above 1 | P1 | Right settlement | Section 11 | [Built] |
| FR-14 | Additional down payment = loan requirement less approved amount | P1 | Exact cash needed | Never below 0 | [Built] |
| FR-15 | Trade advance limit, used, balance and commission per lender | P2 | Dealer value | Section 11 | [Built, test values] |
| FR-16 | Skip the vehicle-number check when exchange is No | P1 | Avoid a dead end and a paid call | Journey moves on with no exchange car | [Built after the demo] |
| FR-17 | "My cases" list and back-office review queue | P2 | Resume and oversee cases | Case list by status | [Planned, FinStack listing page] |
| FR-18 | Lender status and trade advance used from the lender | P3 | Real decisions and balances | API or callback | [Planned] |
| FR-19 | Bank statement analysis for lenders that need income proof | P3 | Verified income | Salary credits and average balance | [Planned] |

## 10. Detailed flows

**Happy path:** Step 1 consent > DigiLocker > Step 2 > Step 3 (all filled) > Step 4 choose a fitting lender > Step 5 lender says approved with an amount > Step 6 settlement.

**Rejected:** Step 5 status rejected > back to Step 4 > pick another lender > repeat. The rejected lender should not be offered again. [Planned: today it still is]

**No score (NTC):** Step 4 shows NTC > only lenders that accept NTC are offered. [Built after the demo; the NTC lender list is still to confirm with each lender]

**No exchange car:** Step 2 exchange No > no vehicle number asked > Step 3 exchange value 0. [Built after the demo]

**Approved for less than asked:** Step 6 shows the gap as additional down payment. Example from the demo: asked 15,17,728, approved 15,00,000, additional down payment 17,728. [Built]

## 11. Business rules (all amounts in rupees; lender terms are test values)

| Rule | Statement |
|---|---|
| Insurance | 4% of the ex-showroom price (approximate) |
| TCS | 1% of the ex-showroom price when it is above 10,00,000; otherwise 0 |
| Road tax | Karnataka slabs plus a fixed 3,000 for other charges; looked up per Kia variant (182 variants) |
| On-road price | Ex-showroom + insurance + road tax. TCS is not included |
| Loan value | On-road price − TCS − down payment − exchange value, never below 0 |
| LTV | Loan value ÷ ex-showroom price, as a percentage |
| Credit health | Bad if any suit-filed balance, any default account, or outstanding above 25,00,000. Best if outstanding is 10,00,000 or less. Otherwise Good |
| Finance amount | Approved amount if above 1, otherwise the loan requirement |
| Additional down payment | Loan requirement − approved amount |
| Balance trade advance | Lender limit − used so far − this case's finance amount |
| Commission | Lender rate × finance amount: sbi 1.4%, hdfc 1.8%, bajaj 2.5%, chola 3% [Test value] |
| Trade advance limits | sbi 2 Cr, hdfc 1 Cr, bajaj 75 L, chola 50 L [Test value] |
| Exchange value | Base price by engine-size band × make weight × age factor, rounded to 500. Make weights: Toyota 1.08, Maruti 1.05, Hyundai, Kia and Mahindra 1.00, Tata 0.93, other 0.85. Age factor falls from 0.90 in year 0 to 0.20 from year 10. [Assumption, not a dealer quote] |
| Route | Status rejected goes back to Routing-1; approved goes to Settlement |

**Lender fit (illustrative thresholds, not the lenders' real policies) [Assumption]**

| | sbi | hdfc | bajaj | chola |
|---|---|---|---|---|
| Not a fit if score is below | 750 | 700 | 650 | 650 |
| Likely needs a score of at least | 770 | 720 | 670 | 670 |
| Not a fit if monthly commitment is above | 25,000 | 30,000 | 40,000 | 40,000 |
| Likely needs commitment at most | 15,000 | 20,000 | 30,000 | 30,000 |
| Not a fit if loan is above | 30 L | 30 L | 25 L | 25 L |
| Likely needs credit health Best | yes | yes | no | no |

Credit health Bad is not a fit everywhere. Chola is assumed to follow Bajaj's rules.

## 12. Edge cases

| Case | Expected | Status |
|---|---|---|
| Customer new to credit, no score | Show NTC, offer NTC-accepting lenders | [Built after demo] |
| No exchange car | Skip vehicle-number check | [Built after demo] |
| Bureau or other API returns nothing | Plain label, move on, no dead end | [Principle; test each call before launch] |
| Wrong OTP | Block and allow resend | [Built] |
| Name or PAN does not match DigiLocker | Show score; send to manual review | [Expressions built; review queue planned] |
| Page refreshed mid-journey | Values may arrive as text; formulas must convert them | [Bug found and fixed once: TCS dropped to 0] |
| Car not in the price table | Price shows −1; let the executive type the price | [Planned] |
| Approved amount blank on a rejection | Must default to 0 | [Defect, see section 13] |
| Exchange value filled after the loan was worked out | Loan must recompute | [Defect, see section 13] |

## 13. Known defects at the end of the hackathon

1. Loan value ignored the exchange value (showed 15,17,728 with an exchange value of 3,13,000; it should have been 12,04,728).
2. Submitting "rejected" gave "Missing key approved_finance_amount".
3. "Income p.a" on Routing-2 is net of EMI, not gross.
4. Credit health is no longer visible on Steps 4 and 5.
5. Routing-2 shows the car code, not the car name.
6. The rejected lender is still offered again on Step 4.
7. Formulas that need today's date use a fixed date, because FinStack rejected the date calls we tried.

## 14. UX

- Labels in English with Kannada beside them; a language switch in the header. [Built]
- Each form shows Incomplete or Verified, then "Update form"; Continue turns on after Verified. [Built]
- Customer name shows under the step title. [Built]
- To improve: labels say "you" while the executive is typing; show readable names for coded values.

## 15. Analytics and measures

| Measure | Definition | Direction |
|---|---|---|
| Completion (primary) | Cases reaching Settlement ÷ cases started | Up |
| Time to decision | Minutes from consent to lender status | Down |
| Approval share | Approved ÷ sent | Up |
| Reroute rate | Cases that needed more than one lender | Watch |
| Commission matched | Commission shown ÷ commission received | Close to 1 |
| Guardrail | Cases where the customer was quoted a wrong loan | Zero |

Targets are set after a pilot baseline, not now. No numbers are claimed.

## 16. Validation

- **Hypothesis:** an executive can take a buyer from enquiry to a lender decision in one sitting with minimal typing.
- **Test done:** a live demo where about 15 to 16 people used the journey, some with edge cases. [Built, observed]
- **What it showed:** NTC customers and customers with no exchange car hit dead ends. Both were fixed after the demo.
- **Next test:** a pilot with real dealership staff (section 21).

## 17. Non-functional needs

- Slow or failing APIs must not stop the journey.
- Values must survive a page refresh.
- Personal data stays with FinStack and DigiLocker. The dealer side keeps only status and amounts.

## 18. MVP and scope

**In the MVP [Built]:** one linear journey, consent by OTP, DigiLocker, price and loan, fit rules, one lender send with reroute, settlement figures. **Later:** lender API for status and trade advance, bank statement analysis, review queue, dealer login and dashboard, brands beyond Kia, used cars.

## 19. Dependencies

- FinStack: journey builder, bureau, DigiLocker, vehicle and asset APIs. Some were not live at the time (PAN autofill and asset value waited on setup).
- A dealer's quote or DMS feed for prices (we used a Kia price table as the fallback).
- Lenders: status and trade advance data, and the list of lenders that accept NTC.

## 20. Privacy and safety

- Consent with time and purpose before any bureau pull, confirmed by OTP on the customer's phone. [Built: terms tick plus OTP; whether FinStack stores the time of the tick is to confirm]
- Soft credit check only. The report is used for routing and is not shared with the lender. [Design rule from F23]
- Aadhaar goes through DigiLocker only. The dealer side never stores it.
- All figures in the demo are test values. Names, mobiles, PAN and Aadhaar are masked in this repository.
- Regulation to check before launch: RBI digital lending guidelines and the DPDP Act. [Assumption: reading only, not legal advice]

## 21. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Wrong loan shown (defect 1) | High until fixed | High | Fix the formula, re-test every path |
| Lender status still set by hand | Certain | Medium | Lender API or callback |
| API slow or empty at the counter | Medium | High | A "not available" path for each call |
| Lender rules in the demo are our guesses | Certain | Medium | Replace with each lender's real policy before pilot |
| Dealers do not pay | Unknown | High | Test the fee idea with dealers (we assumed Rs 10,000 per outlet per month) |
| Whether FinStack's bureau access can serve a dealer client | Unknown | High | Ask FinStack |

## 22. Rollout and launch readiness

Rollout phases are in `../launch/production-launch-plan.md` (hypothetical, to refine with pilot data). Readiness checklist: defects 1 and 2 fixed; every outside call tested with an empty answer; real lender terms; consent record confirmed; a date variable or API for today's date; a dealer interview round.

## 23. Open questions and assumptions

| Question | Working answer | Confidence |
|---|---|---|
| Which lenders accept NTC? | Unknown, to confirm per lender | Low |
| Is Chola's rule the same as Bajaj's? | Assumed yes | Low |
| Who sets the lender status in production? | A lender API or callback | Medium |
| Does FinStack save the time of the consent tick? | To confirm | Low |
| What will a dealer pay? | Rs 10,000 per outlet per month, assumed | Low |
| Do dealers want one tool for finance and trade advance? | Believed yes, untested | Low |

## 24. Recommendation

Fix the loan formula and the rejected path first, since they affect the customer's money and the reroute. Then run a pilot in one or two Kia outlets with real lender terms, measure completion and time to decision, and only then decide on dealer fees and a lender API.
