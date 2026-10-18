# DealerFinance: production launch plan

**Team 6: Aditya Sharan and Sameer S Mittimani** · FinStack FinTech PM Hackathon, Bengaluru
Matches a new-car buyer to the right lender at the dealership counter, and settles the dealer's trade advance and commission. Built on FinStack for Kia cars with four lenders. All figures are test values.

## 1. Where it plugs in

**Platforms where this journey can sit:** a dealership's DMS or CRM (the system the sales executive types the enquiry and quote into); a carmaker's dealer portal; new-car marketplaces that pass leads to dealers; loan aggregator or DSA apps that dealers already use; the enquiry form on a dealer's own website or WhatsApp.

**Chosen platform: the dealership DMS or CRM.** The executive already enters the customer's name, mobile, car, variant, quote, down payment and exchange car, in front of the customer, at the moment the buyer is ready to pay. That is the right moment to ask "do you want finance?". The dealer also earns commission from the lender, so it wants the decision at the counter, not days later. One connection to a DMS can reach every outlet that uses it (to be confirmed with the DMS vendor).

## 2. Fields the platform must give us

| Screen | Fields from the platform | How often |
| --- | --- | --- |
| 1 Enquiry | Customer name, mobile, outlet id, executive id. Consent is taken inside our Step 1 (the terms tick, then a 6-digit code to the customer's own phone), so the platform needs no consent tick of its own. | Once, when the customer says yes to finance |
| DigiLocker | Nothing. The customer does Aadhaar OTP in our SDK. PAN name, PAN number and date of birth come back to us. | Once |
| 2 Verification | Car model and variant code, exchange yes or no, exchange vehicle number, down payment agreed, employment type, monthly income, monthly EMI commitment, income proof yes or no. | Once, and again if any value changes |
| 3 Customer_Inputs | All 7 fields pre-filled from the dealer's quote and our rules. | On quote change |
| 4 Routing-1 | The dealer's lender panel (which of the four lenders this dealer works with). We add credit score (or an NTC label when there is none) and LTV. | Once, as setup |
| 5 Routing-2 | Nothing in. Out to the platform: lender, status (approved or rejected), approved amount. If the status is **rejected**, the case routes back to Routing-1 to pick another lender. In future, Routing-2 becomes a plain submit, and everything after it (lender decision, status, approved amount) runs as backend activities with no screen. | Every decision |
| 6 Settlement | Lender's trade advance limit and amount used so far, commission rate per lender, booking or invoice number once the car is billed. | Every case, plus a daily balance feed |

**In short:**

* **Shared once:** customer name and mobile, and the dealer's lender panel.
* **Shared again on a change:** the quote and the customer's answers (income, EMI, down payment, exchange car).
* **Sent back every time:** the lender, the status and the approved amount, so the executive can quote the exact cash needed.
* **Never asked of the platform:** Aadhaar, bureau data and bank details. These stay with DigiLocker and FinStack.

### Where more can be pre-filled (fewer typed fields)

| Field typed today | Pre-fill source | Status |
| --- | --- | --- |
| PAN, name, date of birth | DigiLocker | Built; match checks written |
| Credit score | Bureau soft pull | Built (Step 4) |
| Monthly EMI commitment | Obligations in the bureau report | Planned |
| Monthly income | Bank statement via Account Aggregator | Planned |
| Exchange car value | Vehicle number, then RC details, then value | Rule built; API pending |
| Customer_Inputs (all 7 fields) | Dealer's quote; our lookup as fallback | Built; DMS feed planned |
| Trade advance used | Live lender data | Demo value today |

## 3. What the platform has to change

1. Add a "Finance" button on the quote screen that opens our journey when the customer says yes to finance, and passes name, mobile, quote id and outlet id. Consent needs no change on the platform, because our Step 1 already holds the terms tick and the code sent to the customer's phone.
2. Send the quote fields in section 2 by API. Send them again on any change, with the quote id, so we update the case and do not make a second one.
3. Take our result back by callback (lender, status, approved amount, extra down payment) and show it on the quote or booking screen, so the executive can tell the customer the exact cash needed.
4. If every lender rejects, hide the finance offer for that customer.
5. Accept a monthly commission file (case, lender, amount) so accounts can match it to lender payouts.
6. Nothing to change for customers new to credit: our journey shows NTC and carries on by itself.
7. Give executives their own logins. FinStack keeps consent, Aadhaar-linked and bureau data. The platform stores only status and amounts.

## 4. Launch plan (hypothetical)

This is our proposed plan. Dates, outlet counts and the fee are assumptions to refine with real pilot data.

| Phase | What happens | Exit check |
| --- | --- | --- |
| 0. Fix and connect (weeks 0 to 2) | Fix the open issues in section 5. Switch on the real PAN, bureau, asset and lender-send connections. Run 20 staff cases through one dealership. | Open issues in section 5 closed and re-tested |
| 1. Pilot (weeks 3 to 8) | One or two Kia outlets in Bengaluru. Executive-assisted only. Review every case each day. | Completion and decision time set as the baseline |
| 2. One dealer group (months 3 to 6) | All its outlets and brands. Customer self-serve link by WhatsApp. First DMS connection. | Commission matches lender payouts for a full month |
| 3. Bengaluru (months 6 to 12) | Up to 178 outlets across six brands, a second DMS, then used cars. | Paying outlets and repeat use |

**What we measure:** cases started versus cases reaching settlement (completion); minutes from enquiry to lender decision; share approved; extra down payment explained at the counter; commission matched to lender payouts; executive minutes saved per case. We set the targets from the pilot baseline, not before.

**Money:** a software fee per outlet per month. We assume Rs 10,000, which gives about Rs 2.1 crore a year across 178 Bengaluru outlets. This is an assumption to test with dealers. Per-call charges for OTP, KYC and bureau are to be confirmed with FinStack.

**Rules and risks:** consent with timestamp and purpose before any bureau pull, confirmed by OTP on the customer's own phone (RBI digital lending guidelines, DPDP Act); keep the minimum data; disclose commission to the customer; lender agreements for each lender before go-live. Main risks: lender status is still set by hand, DMS integrations take time, and API slowness at the counter. Fallback: the executive can save the case and resume it from the My cases list.

## 5. What the live demo taught us, and what we changed

About 15 to 16 people tried the journey at the live demo, and some of them hit edge cases. Two things stopped the journey or cost us a paid call. Both are now handled.

| # | What happened | What we changed | Effect |
| --- | --- | --- | --- |
| 1 | Customers who are new to credit (NTC) get no score from the bureau. The journey had nothing to show, and the next step needs a number. | If no score comes back, the screen shows "NTC" and the case carries on, offering only lenders that accept NTC. The credit report request stops at that point. The platform changes nothing. | No dead end for NTC customers. No repeat requests for a customer who has no file. |
| 2 | The vehicle-number check works only when the customer has a car to exchange. With no exchange car, the journey stopped on that screen. | Skip the vehicle-number check when exchange is No. It runs only when exchange is Yes. | No dead end. One paid lookup fewer for every case without an exchange car. |

**Lessons for production:** every paid call should have a "not available" path that shows a plain label and moves on. Before go-live we list each external call (OTP, DigiLocker, bureau, vehicle lookup, valuation, lender send) with what the journey does when it returns nothing, and we run one case through each. To build: the lender fit rule must read "NTC" as a valid answer, and we need the list of lenders that accept NTC, confirmed with each lender.

### Still open before launch (from our own checks)

| # | Issue | Why it matters | Fix |
| --- | --- | --- | --- |
| 1 | The loan ignored the exchange value. It showed Rs 15,17,728 with an exchange value of Rs 3,13,000. | The customer would be quoted a loan about Rs 3.13 lakh too high (it should be Rs 12,04,728). | Read the exchange value in the loan formula after it fills. Re-test. |
| 2 | Submitting "rejected" gave "Missing key approved_finance_amount". | A rejection cannot be recorded, so the reroute to another lender is blocked. | Default the amount to 0 on a rejection. |
| 3 | Lender status is picked by hand. | No real lender decision. | Lender API or callback. |
| 4 | Trade advance used is a fixed demo value with no running balance. | The balance is wrong after the first case. | Live lender data or a database. |
| 5 | Step 4 still lists the lender that just rejected. | The executive can send it there again. | Remove the rejected lender from the list. |
| 6 | Formulas that need today's date use a fixed date, because FinStack rejected the date and text-compare calls we tried. | Exchange value and age go out of date over time. | A date variable or API from FinStack. |
| 7 | Display polish: "Income p.a" is net of EMI; credit health is hidden on Steps 4 and 5; Step 5 shows the car code, not the name; typo "varifcation". | Readers misread the screen. | Rename labels and show the readable car name and credit health. |