# Consent, KYC rules and lender rules

What I learned about doing a lending journey legally and sensibly, and how it shaped the product. Written in my own words. **[verify]** marks things I need to check before quoting.

---

## Consent

- **Nothing is checked before the customer agrees.** The first form carries a consent tick, and every credit report call needs a consent timestamp.
- **Soft pull only.** A soft pull leaves no enquiry on the customer's report. A hard pull does, and the platform cannot make those for a software client; the licensed lender does.
- **Say why the data is collected,** keep the minimum, mask it, and delete it when the consent period ends (the DPDP Act points).
- **A report is seen only with consent.** Even a bank needs at least a tick.
- **A full name plus a mobile number can be enough** to pull someone's PAN, address and date of birth, so treat that pair carefully.

In DealerFinance: Step 1 is the terms tick followed by a 6-digit code sent to the customer's own phone, so consent is confirmed by the customer, not typed by the executive. Whether the platform stores the time of the tick is still to confirm.

## KYC

- Two proofs: identity and address. Valid documents include PAN, Aadhaar, passport, driving licence and voter ID. PAN carries no address.
- **DigiLocker** gives a signed document straight from the source. The customer is redirected to confirm with an OTP, which interrupts the journey.
- **Screening** on identity: criminal records, politically exposed persons, do-not-lend lists, anti-money-laundering lists.
- **Age:** 18 is the legal minimum, but most lenders set 21 or higher.
- **Address** has three layers: the document address, "is this your current address?", and a field visit for larger loans.
- **Name matching must be fuzzy.** Indian names vary by spelling and initials. A good rule lets a borderline match continue but re-checks it later, and sends it to a person, so good customers are not rejected.
- **Pin codes** are tagged green, amber or red by repayment history and collection reach. Lenders lend near where they have a presence.

## Lender rules (how a lender decides)

The four pillars of underwriting: contactability, capability, collectability and intent. Cheap checks (age, pin code, identity) go first; expensive ones (bank statements, field visits) later.

Rules we built into DealerFinance, as thresholds per lender (illustrative, not any lender's real policy):
- a minimum score, a maximum monthly commitment and a maximum loan amount per lender;
- a credit health rating (Bad, Good, Best) from suit-filed balance, defaults and total outstanding;
- a fit label per lender: likely, possible or not a fit;
- a path for customers new to credit (NTC), where only lenders that accept NTC are offered.

## Why this matters for a product

- The dealer is not the lender. The tool routes and informs; **the lender decides.** Our credit report is used only to route and is not shared on.
- A credit-thin person with verified stable income can be a better bet than a thin score. That is why "no score" must be a valid path, not a rejection.
- Every rule filters the customer segment. Name the segment first (new-car buyers at dealerships) and build the rules for it.

## Open or to verify

- The current rules on deemed address proofs such as utility bills **[verify]**.
- Whether the platform stores the consent timestamp itself.
- Which lenders accept customers new to credit.
