# Day 1: how banks work, and what a no-code lending platform does

Friday 9 Oct 2026, 4 to 8 pm. Two parts: a session on banks, RBI and NBFCs, then a demo of FinStack's platform and the hackathon brief.

Written in my own words from my notes of the recording. Items marked **[verify]** were said in class in a simplified way and need checking before I repeat them.

---

## Part 1: how banks, RBI and NBFCs work

**The big idea.** A bank trades money: it buys money (deposits, capital) and sells it (loans) at a higher rate. RBI sets rules so a bank never runs out of cash.

**Assets and liabilities flip for a bank.** My loan is my debt, but it is the bank's asset because it earns interest. My fixed deposit is my asset and the bank's liability, because it pays interest and I may withdraw it.

**Three safety buffers**

| Buffer | What it is | Earns the bank |
|---|---|---|
| CRR | Cash kept with RBI, cash only | Nothing |
| SLR | Government bonds, gold and other very safe assets | Stable, low |
| HQLA | Liquid assets to cover the next 30 days of expected outflow | Some |

About a quarter to 30% of deposits sit in these buffers; the rest can be lent. The reason is to stop a **bank run**, where panic makes everyone withdraw at once even if the bank is fine (Silicon Valley Bank and Yes Bank were the examples).

**Every loan creates a deposit.** When a bank lends, the money lands in an account at the same bank. Nothing physically moves; one balance becomes two entries. That is why banks build ecosystems (apps, salary accounts, no-cost EMIs): to keep the money inside.

**LAF, repo and reverse repo.** Under the liquidity adjustment facility a bank swaps cash and bonds with RBI. The repo rate is what a bank pays to borrow cash from RBI; the reverse repo rate is what RBI pays a bank that parks cash. Lower repo means easier lending; higher repo cools inflation.

**NBFCs.** They lend but, in the deposit-taking case, follow similar ratios and pay a little more on deposits with less insurance cover. A cheaper source of money lets one NBFC serve good borrowers; a dearer one must lend to riskier segments at higher rates. When two lenders chase the same segment they compete on **how easy the onboarding journey is**.

**What I took away:** the lender's cost of money decides which customers it can serve, and when costs are equal the journey itself is the product.

## Part 2: what a no-code lending platform is

**What FinStack is.** Software sold to lenders (banks and NBFCs). It does not lend and does not tell the lender what rules to set. The lender's own customer is the borrower; FinStack's customer is the lender.

**Origination vs servicing.** Origination (sourcing, KYC, underwriting, decision) is where lenders can differ. Servicing (EMIs, reporting, collections) is heavily regulated, so there is little room to differ. The hackathon is about origination.

**Why lenders buy instead of build**
1. Integrations: Aadhaar, PAN, bank statements and bureaus need Indian vendors, and generic no-code tools do not have them.
2. Compliance: an audit trail of every action, masked data, consent records.
3. Speed: a risk team can change a rule in seconds, not months.
4. Data stays with the lender, deployed in the lender's own cloud account.

**The building blocks**

| Block | What it does |
|---|---|
| API hub | Ready verification APIs, each an input and an output; several vendors per check, with fallback |
| Form builder | Forms are the building block of a journey: API forms (PAN, bureau) and custom forms |
| Journey builder | Orders the forms into steps; sets what happens on pass or fail |
| Rules | Verification rules (for example a fuzzy name match at 80%), visibility rules, logic variables |
| Internal workflow | Back-office screens for review and approval |
| Audit trail | Every entry, API response and decision logged |

**Underwriting in one line.** Decide whether to lend, how much and at what rate. Knock-out rules (for example a score under 650 or a name mismatch) reject at once.

**Bureau and Account Aggregator.** The platform cannot make hard credit pulls or Account Aggregator calls on its own; the licensed lender supplies the credentials. PAN and Aadhaar checks work without that.

**Privacy law (DPDP Act).** Take consent and say why the data is collected, encrypt and mask personal data, delete it when the consent period ends.

## The hackathon brief

- Build any fintech product on the form and journey builders.
- KYC is mandatory; put a consent tick in the first form; onboard an individual, not a business; use soft-pull bureau calls only.
- A complete simple product beats a half-built big one.
- Teams of two, one technical and one not.

## What I took away

1. Banks and NBFCs differ by cost of money and by chosen customer segment. The segment decides the rules.
2. In a lending product the **order of checks** is a design choice. Cheap checks go first, costly ones later.
3. A platform like this turns "build an app" into "configure forms, order them and add rules". The thinking moves to the customer, the rules and the data.

## Where I used it in DealerFinance

- Consent tick first, then the checks (Step 1).
- Lender fit rules per lender, as simple thresholds (the knock-out idea).
- A journey of forms in an order, with a rejection sending the case back (journey builder).

## Open or to verify

- Deposit insurance cover as said in class does not match what I know. The current cover is ₹5 lakh per depositor per bank **[verify]**.
- The CRR range said in class was 3 to 5% **[verify the current level]**.
