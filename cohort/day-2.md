# Day 2: underwriting, KYC, credit reports, proof of income, and the platform hands-on

Saturday 10 Oct 2026, about 3 hours 20 minutes. Two halves: underwriting and data sources, then a live hands-on build on the platform.

Written in my own words from my notes of the recording. **[verify]** marks things said in class in a simplified or rough way.

---

## 1. Risk and reward

- No lending segment is evergreen. Money moves between safe bonds, stocks and loans as yields change, and that movement opens new loan markets (gig workers are one: they have income that can be underwritten with alternate data).
- A small default rate can wipe out a lender's margin. With a 6% cost of money, 12% lending and about 3% running cost, a 3% default rate turns a profit into a small loss. That is why high-risk lenders charge very high rates, and why a first small loan matters: it gives a new-to-credit person a credit history.
- The cost of onboarding (KYC, bureau, cloud, API calls) is the same for a small or a large loan, so good products try to raise the ticket size.

## 2. Underwriting: four questions

1. **Contactability:** can we reach the customer later?
2. **Capability:** can they afford it?
3. **Collectability:** can we recover the money if they do not pay? Remote areas cost more to collect from, so banks tag pin codes green, amber or red.
4. **Intent:** will they pay? There is no API for intent. It is checked late, by talking, because it is expensive.

**Funnel thinking.** Every step runs data fetches and rules and decides who goes on. Put cheap checks first and expensive ones later.

## 3. What makes a good fintech product

- **Embed it so it does not feel like finance.** A flight or hotel booking can run KYC and a credit check quietly and then offer EMI at checkout.
- **No-cost EMI** is a discount from the seller paid to the financier, so the customer pays the full price in instalments. It serves people who could already afford the item.
- Everyone has the same tools (DigiLocker, the same bureaus), so the **experience** decides who wins.

## 4. KYC

- Proof of identity and proof of address, from two documents. Most apps use PAN for identity and Aadhaar for address.
- **DigiLocker** returns a signed document from the source, and anyone can use it, but the user is redirected to confirm with an OTP. That breaks the flow, so a reminder notification helps.
- **Names rarely match exactly** (initials, father's name), so use a **fuzzy match**, not an exact one.
- Push any missing-data asks to the end so people do not drop off.
- A selfie or blink test lowers risk but is not real biometrics. For RBI, the proof is the call to the identity authority plus the consent taken before it.

## 5. Credit reports (CCR)

- Under 30% of Indians have credit data **[verify: rough figure]**. A no-hit comes back as -1, new to credit. That is a challenge and also the opportunity.
- Four bureaus: CIBIL, Experian, Equifax, CRIF. Use the score only as a rough gate. A score of 750 can still be a fraud.
- A report gives the score, the enquiries (many means a desperate borrower), loan performance with days past due, and past addresses.
- **Soft pull vs hard pull.** A soft pull leaves no enquiry on the customer's report. A hard pull records an enquiry against the lender.
- **Privacy:** a full name plus a mobile number can be enough to pull someone's PAN, address and date of birth.

## 6. Proof of income

| Route | Who can use it | Problem |
|---|---|---|
| Account Aggregator | Only regulated lenders or their partners | Many smaller banks are not on it |
| Bank statement upload and analysis | Anyone | Friction; tampering risk |
| Tax returns, EPFO, GST | Anyone | Credentials sit with an accountant, or servers are unreliable |

- Salary should arrive by NEFT or IMPS, not UPI. EMIs should stay under about half of income.
- For the hackathon: use statement analysis, not Account Aggregator.

## 7. Platform hands-on

- **Forms:** field types, regex checks (a 10-digit mobile; PAN where the fourth letter is P for an individual), test each form once so the system learns its output.
- **Journey:** steps and actions; what happens on failure; a unique identifier on step 1 (the mobile) to stop duplicates.
- **Auto-submit:** calling an API in the background when a form is submitted. In the demo, name and mobile alone fetched PAN, addresses and date of birth from a basic bureau call, and a second call pulled the full soft-pull report.
- **Pre-fill with a fallback:** use the bureau name first, else what was typed. Lock the pre-filled field.
- **"Force error":** on means an API failure stops the user; off means they carry on (for nice-to-have fills).
- **Consent timestamp:** every bureau call needs it, captured at submit. The platform also stores device and location as an audit trail.
- **Changes on a live journey** do not reach leads already past that step; real teams copy the journey and roll out to a small share first.
- **Back office:** the listing page shows chosen columns, filters and charts; staff can open a stuck lead and fill steps for the customer (assisted onboarding).
- Two people can edit the same journey but may overwrite each other: one on forms, one on the journey.

## 8. How the hackathon was judged, as announced

1. A "subtle" product, where the finance is embedded and the user barely notices, scored highest.
2. Completeness and a clearly targeted customer, with rules that filter to that customer.
3. Screens and charts counted least.
- KYC and a credit report had to be in the journey. No own APIs. No servicing.

## What I took away

1. The best rule order is cheap to costly. Every API call is money, so each step has to earn its place.
2. "No data" is a normal answer, not an error. New-to-credit customers are the market, not an exception.
3. Soft pull for a quiet check; consent first, with a timestamp.
4. A fuzzy name match beats an exact one in India.

## Where I used it in DealerFinance

| From class | In the product |
|---|---|
| Consent with a timestamp before a bureau call | Step 1: terms tick, then a code to the customer's phone |
| Name and mobile can fetch PAN details | Decided early; pre-fill from DigiLocker was built |
| DigiLocker for identity and address | DigiLocker stage between Step 1 and Step 2 |
| Fuzzy name match | A name-match expression comparing typed and PAN names |
| Soft pull, score as a gate | Credit score and credit health on Step 4 |
| Pin code bands | Considered as an extra lender rule; not built |
| Assisted onboarding | The executive fills the journey for the customer |
| Funnel order, cheap first | Skip the vehicle-number check when there is no exchange car |
| "No data is an answer" | NTC path added after the live demo |

## Open or to verify

- Whether the bureau coverage figure and the reporting rules to all four bureaus are current **[verify]**.
- Whether RBI wants a hard pull after a loan is given, as said in class **[verify]**.
