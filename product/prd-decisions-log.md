# DealerFinance: PRD decisions log

One feature at a time. Each entry: Sameer's decision, what goes in the PRD, and what stays out.

---

## F1. Users and access (10 Oct 2026)

**Decision:** The **Dealer Principal** owns the dealer account and gives logins to their team: the **finance coordinator**, the **sales executives** and **CRM entry staff**. Leads can also come in from **other sources such as the dealer's CRM**. For those, **customer consent is critical**.

**In the PRD (do):**
- Dealer Principal is the account admin: adds and removes users and assigns roles.
- Three staff roles: finance coordinator, sales executive, CRM entry.
- Two ways a lead arrives: typed in manually, or imported from the dealer CRM (file upload or API).
- **Every lead, however it arrives, needs fresh customer consent (SMS link + OTP) before any KYC or bureau check.** An imported lead sits at "Waiting for consent" until the customer agrees.
- Each action is logged with who did it (user + role + time).

**Out of the PRD (don't):**
- No KYC or bureau pull on CRM-imported data without fresh consent, even if the CRM says the customer "agreed" earlier.
- No shared logins; every staff member has their own.
- No lender staff accounts inside the dealer workspace (lenders have their own inbox).

---

## F2. Who can send a case to a lender (10 Oct 2026)

**Decision:** The **finance coordinator** sends cases. If a dealer has no finance coordinator, **whoever handles that function** does.

**In the PRD (do):**
- "Send to lender" is a **permission**, not a fixed role. The Dealer Principal gives it to the finance coordinator by default, or to any user who does that job (small dealers may have one person doing sales and finance).
- Users without the permission can create leads, add details and see match results, but the Send button is hidden for them.
- The Dealer Principal always has every permission.
- The case record shows who sent it.

**Out of the PRD (don't):**
- No hard-coded "only finance coordinator" rule; it would break for small dealers.
- No send without the permission, even for the top-fit lender.

---

## F3. How leads come in + consent mode (10 Oct 2026)

**Decision:** Three ways in:
1. **Excel/CSV upload** from the CRM with customer name, mobile and PAN (PAN only if available). Each uploaded lead gets a **simple consent SMS**.
2. **Walk-in, customer present:** the dealer or sales person enters the lead and the **customer gets an OTP on their phone and enters it** on the dealer's screen.
3. **Walk-in, customer not present:** send the customer a **link to fill in their own details** (name, mobile, car, etc.) and consent there.

**In the PRD (do):**
- CSV template: name, mobile (required), PAN (optional). Invalid rows (bad mobile, duplicate mobile) are shown before upload, not silently dropped.
- Uploaded leads start at **"Waiting for consent"**; nothing runs until the customer agrees.
- If PAN is missing from the CSV, it's collected when the customer opens the link or at the showroom.
- Consent modes, chosen per lead:
  - **In person (assisted):** OTP to the customer's phone, entered on the dealer screen.
  - **Remote (self-serve link):** the customer fills basic details + consents on their own phone.
- This makes onboarding **hybrid** (assisted + self-serve), which the brief rewards.
- Consent record stores mode, time, OTP/link reference, and the lenders named.

**Out of the PRD (don't):**
- No KYC or bureau on uploaded rows until consent (same as F1).
- No bulk "consent on behalf of customer" button for dealers.
- No long forms in the consent SMS; it's one short message + link.

---

## F4. Customer doesn't give consent (10 Oct 2026)

**Decision:** The lead is **kept on hold** and does not proceed. RBI guidelines are strict: **without consent, the customer's details can't be used to pull a CCR (consumer credit report)**.

**In the PRD (do):**
- Status **"On hold: no consent"**. KYC, CCR and matching are all locked.
- The dealer can re-send the consent SMS/link.
- The hold is visible on the dealer's lead list and in the funnel ("consent pending" stage).

**Out of the PRD (don't):**
- No CCR, KYC or any bureau call without recorded consent. No exceptions, no override, not even for the Dealer Principal.
- No sharing the lead with any lender while on hold.

**Open item:** how long an on-hold lead's data is kept before deletion (DPDP Act asks us not to keep personal data longer than needed). Suggest 30 days.

---

## F5. Identity check at the dealer stage (10 Oct 2026)

**Decision:** The dealer stage stays light. With consent, we pull the **CCR using a fuzzy match on name + mobile**. If the bureau can't find the customer that way, we **ask for PAN**. After consent, **PAN is pre-filled** if a lookup returns it; if not, the customer has to give it.

**In the PRD (do):**
- Order: consent → CCR lookup on name + mobile (fuzzy) → if found, continue; if no hit, ask for PAN → retry the CCR with PAN.
- PAN field: pre-filled after consent when available; otherwise required from the customer (in person or through the link).
- **PAN verification API** checks the PAN is valid and returns the name; this is the "KYC through API" the hackathon brief requires.
- Name match (PAN name vs entered name) is shown to the finance coordinator as a score, as a warning rather than a stop.
- Full KYC (Aadhaar / DigiLocker, documents) is **done by the lender** after the case is sent, not by the dealer.

**Out of the PRD (don't):**
- No Aadhaar collection at the dealer stage. Less sensitive data held by the dealer = less DPDP risk.
- No hard stop on name mismatch; the lender's own KYC decides.

**Note for the pitch:** say clearly that the dealer stage does "KYC-lite" (consent + PAN verify), and the lender does full KYC. That satisfies "don't skip KYC" without the dealer handling Aadhaar.

---

## F6. Income (10 Oct 2026)

**Decision:** DealerFinance **doesn't verify income**. It uses the **customer's self-declaration**: either their monthly income, or **the EMI they say they can pay** ("I can pay this much a month").

**In the PRD (do):**
- Two input options, at least one required:
  - **Declared monthly income** → used for FOIR: (existing EMIs from CCR + new EMI) ÷ income.
  - **Comfortable EMI** → used to work out the loan the customer can afford, and to suggest down payment, tenure or variant ("At ₹18,000/month you can borrow ₹8.7 lakh over 60 months").
- Both are labelled **"Declared, not verified"** on the match screen and in the file sent to the lender.
- If only the comfortable EMI is given, the lender's FOIR rule shows **"Not checked: income not declared"** instead of pass/fail; the lender verifies.
- The lender does real income verification (payslips, bank statement, ITR) after receiving the case.

**Out of the PRD (don't):**
- No bank statement, Account Aggregator or payslip upload at the dealer stage.
- Declared income is never shown as verified.

---

## F7. Lender-fit rules (10 Oct 2026)

**Decision:** The dealer **doesn't underwrite**; the dealer's aim is to **sell more cars**. DealerFinance only checks a few **standard points** each tied-up lender is known for, as simple dealer-level rules. Examples: salaried with a score above 650 → Bank A; above 700 → Bank B; below 650 with no income proof → NBFC C.

**In the PRD (do):**
- Rules are set at **dealer level** (by the Dealer Principal or whoever they allow) for each lender they're tied up with.
- Each lender rule is a short checklist:
  - employment type accepted (salaried / self-employed / both)
  - minimum CCR score
  - income proof needed? (yes / no)
  - optional: maximum loan or LTV
- New dealer input: **"Income proof available?" (yes / no)**, which drives lenders like NBFC C.
- Output is a **fit label, not a decision**: "Likely fit / Possible fit / Not a fit", with the reason. The lender still underwrites.
- Rules screen is plain: one card per lender with these fields and an on/off switch.

**Out of the PRD (don't):**
- No credit decision, approval promise or sanction amount at the dealer stage.
- No complex scorecards or ML at the dealer level.
- Don't show real bank names with made-up policies in the demo; use Bank A / Bank B / NBFC C (the dealer types the real names in their own setup).

**Changes to make in the wireframe:** replace FOIR/LTV-heavy rules with the simple checklist, add "Income proof available?", and change "Strong / Eligible" to "Likely / Possible / Not a fit".

---

## F8. Lender access + case stages (10 Oct 2026)

**Decision:** Give logins to the lender's **servicing branch staff**, or to the **sales officer / manager who visits the dealership**. They see all live cases sent to their lender and update the stage.

**In the PRD (do):**
- Lender user roles: branch servicing staff, sales officer / manager. Each sees only their own lender's cases, and only for dealers they're mapped to.
- Case stages (lender updates, dealer sees live):
  1. Sent to lender
  2. Under credit approval
  3. Approved / Rejected (with reason)
  4. Sanctioned
  5. Disbursed
- Reject → the dealer is prompted to send to the next fitting lender.
- Each stage change is time-stamped, so the dashboard can show **turnaround time per lender**.

**Out of the PRD (don't):**
- Lender users can't see other lenders' cases or the match ranking.
- Lender users can't edit customer data; only stage, reason and notes.

---

## F9. Dealer commission after disbursement (10 Oct 2026)

**Decision:** After disbursement, the same platform **calculates the dealer's commission** from the loan amount and keeps it on the dealer's side. The dealer **claims it through their own process** (GST invoice, TDS). Once paid, their **accounting team ticks "commission received"**, which **closes the case**. Later, data can also come from the **CRM API or accounting systems like Tally**.

**In the PRD (do):**
- Commission ledger per case: loan amount × lender's payout rate = commission due.
- Claim flow: commission due → claim raised (GST invoice number, TDS) → received (ticked by accounts) → **case closed**.
- GST and TDS rates are **settings, not hard-coded** (rates change; e.g. TDS on commission falls under section 194H).
- Dealer dashboard: commission due, claimed, received, and overdue by lender.
- Phase 2: sync with CRM (API) and accounting software (Tally export/API).

**Out of the PRD (don't):**
- DealerFinance doesn't move money or pay commission; it only tracks it.
- No invoice generation in Phase 1; the dealer enters their own invoice number.

**Why it matters:** this gives the dealer a reason to use DealerFinance every day, not just to find a lender. Tracking commission and lender turnaround are real dealer pains.

**For the hackathon:** show it as one back-office screen (commission ledger); keep the full claim flow for the PRD.

### F9b. Commission rate (10 Oct 2026)

**Decision:** The dealer **enters the commission when the loan is sent**, mostly as a **% of the loan amount**. Rates **differ from financier to financier**. If a financier later pays **less** on some cases, the dealer records the gap as a **discount / short payment** at their end.

**In the PRD (do):**
- Default % per lender in settings, pre-filled on each case; the dealer can change it per case.
- Commission due = loan amount × % (shown when the case is disbursed, based on the actual disbursed amount).
- On receipt, accounts enter the **amount received**; any difference is saved as **"Short paid / discount"** with a reason.
- Report: expected vs received by lender, total short-paid.

**Out of the PRD (don't):**
- No single platform-wide rate.
- No auto-dispute with the lender; it's a record for the dealer's own follow-up.

---

## F10. Dealer Principal dashboard (10 Oct 2026)

**Decision:** The home screen shows the **funnel + conversion**, a **lender scorecard**, the **commission tracker**, and a **reroute view** that shows how rejected cases moved from lender to lender. Examples of a case's path:
- Sent to Bank A → rejected → sent to NBFC C → disbursed
- Sent to Bank B → rejected → Bank A → rejected → NBFC C → rejected → NBFC D → approved

**In the PRD (do):**
- **Funnel:** leads → consent → sent → approved → sanctioned → disbursed, with drop-off at each step.
- **Reroute funnel:** of disbursed cases, how many were approved by the 1st, 2nd, 3rd, or 4th+ lender tried. Shows how much rerouting saves sales.
- **Case path:** each case shows its lender trail as a timeline (lender, result, reason, date).
- **Lender scorecard:** per lender: sent, approval %, rejection reasons, average turnaround (sent → sanction), and how often they're the 1st vs a later choice.
- **Commission tracker:** due, claimed, received, short-paid, overdue, by lender.

**Out of the PRD (don't):**
- No staff-performance leaderboard on the home screen (not picked; could be a later report).
- Demo uses sample lender names (Bank A, Bank B, NBFC C, NBFC D), not real ones.

---

## F11. Reroute limit (11 Oct 2026)

**Decision:** **Up to 3 lenders** automatically; a **4th needs Dealer Principal approval** with a reason. The customer gets an SMS each time their file goes to a new lender.

**In the PRD (do):**
- Counter on each case: "Lender 2 of 3".
- 4th lender onward: DP approval + reason, logged.
- Customer SMS on every send: "Your loan file has been sent to [lender]".

**Out of the PRD (don't):**
- No sending to several lenders at once.
- No silent rerouting without the customer being told.

---

## F12. Trade advance lenders get priority (11 Oct 2026)

**Decision:** Some financiers give the dealer a **trade advance** (inventory funding) with an **interest-free period (IFTA)** and interest after that. The dealer wants those financiers **prioritised, based on the amount available** under the arrangement.

**In the PRD (do):**
- Per lender, in dealer settings: trade advance yes/no, limit, amount used, **amount available**, interest-free days, interest rate after.
- Among lenders that fit the customer, ones with an active trade advance and enough available amount get a **"Trade advance" tag and move up the list**.
- The match screen still shows each lender's EMI, so the dealer and customer can see the cost difference.
- Dashboard tile: trade advance used vs available per lender, and stock nearing the end of its interest-free period.

**Out of the PRD (don't):**
- No trade advance priority for a lender the customer doesn't fit.
- DealerFinance doesn't manage the trade advance account itself; it reads the numbers the dealer enters (or later from accounting/Tally).

**Watch out:** if trade advance pushes a costlier lender to the top, the customer pays more. Keeping the EMI visible and logging the reason keeps it fair (see the ranking question next).

---

## F13. Ranking order on the match screen (11 Oct 2026)

**Decision:** It depends on the customer.
- **Customer is flexible** → **trade advance lenders first** (among those that fit).
- **Customer has a preference** → their **chosen lender first**. If they prefer a bank, send to that bank first; the dealer still earns commission, even if smaller.
- Otherwise → **fit order**.

The dealer may gently shift a customer's preference at the showroom; that happens in real life.

**In the PRD (do):**
- New input on the lead: **"Lender preference": Flexible / Prefers [lender]** (dropdown of tied-up lenders, or "own bank").
- Ranking logic:
  1. Remove lenders that don't fit.
  2. If "Prefers X" and X fits → X first.
  3. If "Flexible" → trade advance lenders with available amount first.
  4. Then by fit strength, then lowest EMI.
- If the preferred lender doesn't fit, show "Customer's choice not a fit: [reason]" and fall back to step 3/4.
- EMI is always visible for every lender; the customer's stated preference is saved on the case.

**Out of the PRD (don't):**
- Never override a customer's stated preference silently. If the dealer changes it, the new preference is recorded on the case.
- No sending to a preferred lender the customer clearly doesn't fit (it would waste a credit check).

---

## F14. Hackathon build scope (11 Oct 2026)

**Decision:** **Include everything for now.** The final scope will be decided later, once scoring is clear.

All four blocks are in for now:
1. Lead + consent + CCR + match
2. Send + lender stage updates + reroute (3-lender cap)
3. Commission ledger
4. CSV upload + DP dashboard

**Suggested cut order if the 2-hour build runs short** (cut from the bottom): CSV upload → commission claim details (keep only "due") → reroute funnel chart → trade advance tile. Never cut: consent, PAN verify, CCR, match, send, lender stage, reject → reroute.

---

## F15–F21. Changes after reviewing Day 1 + Day 2 class info (11 Oct 2026, all decided)

**F15. Consent sits inside the car enquiry / booking form (the "subtle" fix).** The customer is buying a car; the dealer already has name, mobile and often PAN. One line on the enquiry or booking form: *"I agree to a soft credit check to see my finance options (no impact on my score)"*, with OTP in the showroom or ticked on the online enquiry link. The separate "agree to loan checks" SMS is dropped. Everything after runs in the background, and the dealer calls the customer already knowing who will finance them. *Why:* Day 2 judging gives the highest points to subtle, embedded finance. Bureau calls still need consent + timestamp (Day 2 demo), so this keeps it subtle and compliant. Replaces the separate consent SMS in F3/F4; the F4 "no consent = on hold" rule stays.

**F16. DigiLocker KYC before the case is sent.** The customer is in the showroom when the case is sent, so a DigiLocker OTP is easy. It gives verified name, address and masked Aadhaar = proof of identity + proof of address (Day 2: KYC needs two documents). The dealer never stores Aadhaar copies. PAN verify stays at the start. *Why:* "don't skip KYC" is in the brief; PAN-only KYC-lite risked being read as skipped. Updates F5 (Aadhaar is no longer left only to the lender).

**F17. Bank statement step for lenders that need income proof.** Declared income or comfortable EMI stays for the quick match (F6). For "Possible fit" cases, or lenders whose rule says "proof needed", the customer uploads a bank statement → bank statement analysis (salary credited by NEFT/IMPS, average balance) → verified income replaces declared. **Upload + analysis, not Account Aggregator** (Day 2: AA is only for regulated entities). Updates F6.

**F18. One manual review queue in the back office.** One listing, filtered to: name match below 80% (PAN vs DigiLocker), credit report no-hit even with PAN, "Possible" fit, dealer override of the top fit, 4th-lender request. The finance coordinator (or Dealer Principal for the 4th lender) approves or rejects each one, with a reason. *Why:* the brief asks for "manual approval for edge cases in the back office".

**F19. More credit report data in the lender-fit rules.**
- More than 5 enquiries in the last 3 months → "Possible" at most (desperate borrower).
- 30+ days late in the last 12 months → not a fit for banks, "Possible" for NBFCs.
- Pin code band (green / amber / red) per lender.

**F20. Build scope vs Phase 2.** *Build (2-hour slot):* enquiry form + consent → credit report + PAN pre-fill → customer inputs → lender-fit rules + ranking → DigiLocker → bank statement (if needed) → review queue → send; back-office listing with stage column; funnel. *Phase 2 (PRD and pitch only):* commission ledger, trade advance, lender stage portal, CSV upload from the CRM, reroute funnel chart. *Why:* FinStack's builder is for onboarding journeys + back-office listing; Day 2 said focus on onboarding, not servicing. Replaces the "include all" note in F14.

**F21. Who runs it.** FinStack only sells to banks and NBFCs ("my client is never the borrower"). DealerFinance is deployed by **one lead NBFC at its partner dealers**. The NBFC's bureau membership covers the credit pulls; cases it can't take go to partner lenders. Real lender and dealer names are used in the demo; rule thresholds are labelled as illustrative assumptions, not the lenders' actual policies.

---

## F22–F25. Answers to the critic review (11 Oct 2026)

**F22. Dealers are the paying customer** (replaces the "lead NBFC deploys it" part of F21). DealerFinance is a SaaS tool the dealer pays for. *Gap to close in the pitch:* a dealer isn't a bureau member, so the soft credit check must run through a **regulated partner's bureau access** (or a consumer-consented bureau API). In the hackathon, FinStack's platform plays the software role.

**F23. The credit report is only for routing.** The soft-pull CCR is used **only to decide which lender to send the case to**. It is **not shared** with lenders: the case sent to a lender carries KYC, customer inputs, car details and the fit reasons. Each lender runs its own credit check. This keeps the dealer stage compliant; the 3-lender cap (F11) limits enquiries piling up on the customer's report.

**F24. How we differ from OEM finance portals (e.g. Maruti Suzuki Smart Finance).** In those, the **customer** picks the dealer and financier, and they cover **one brand** only. DealerFinance is **dealer-side and multi-brand**, and shows what OEM portals don't: the dealer's **trade advance limit, commission, and each lender's speed**.

**F25. Ranking: drop "trade advance first"** (replaces step 3 of F13). Order: **fit → customer's preferred lender → lowest EMI**. Dealer factors (**lender turnaround: how fast the dealer gets the money and can redeploy it**, trade advance room, commission) are shown as **tags and tie-breakers**, not as the main sort, so the customer isn't pushed to a costlier lender. Any dealer pick below the top fit still needs a reason (F13/F18).

**F26. Differentiators go into the build, as tags on the match screen** (updates F20). Trade advance, commission and lender speed are what set us apart from OEM portals, so they can't be only Phase 2.
- **Build:** one simple **dealer settings** form per lender: trade advance room available (₹), default commission %, average turnaround (hours to sanction / days to disbursal payout). These are stored as data in FinStack.
- **Match screen:** each lender card shows tags next to fit and EMI: **"Trade advance ₹38 L free" · "Commission 1.0%" · "Pays out in ~1 day"**. Tags break ties per F25; they never override fit or the customer's preference.
- **Back-office listing:** columns for lender, commission % and expected payout days, so the funnel shows dealer value.
- **Also Phase 1 (Sameer, 11 Oct):** the full commission ledger (claim → GST/TDS → received → closed), trade advance utilisation tracking, and the lender stage portal. **Nothing from this list is Phase 2.**
- **Build order so the core is never at risk:** (1) onboarding journey + match + tags + send → (2) lender stage updates → (3) commission ledger → (4) trade advance tracking. If time runs out, later items are shown as screens in the pitch.

---

## Open items
- F4: how long on-hold (no consent) lead data is kept. Suggest 30 days.
- **Monday (FinStack):** whose bureau access do FinStack's Experian / Equifax APIs use for a non-lender client such as a dealer? Is the vendor a specified user? (F22)
- (Done 12 Oct: the wireframe now reflects F5–F26.)
