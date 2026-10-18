# The fintech APIs we met, and what each one gave us

A lending journey is a chain of calls to outside services. Each call has an input, an output, a cost and a way to fail. This note lists the ones from the cohort and says which we used. Written in my own words. **[verify]** marks class claims I have not checked.

---

## The map

| Check | Input | Output | Used in DealerFinance |
|---|---|---|---|
| Basic credit lookup (a "simple credit check") | Name and mobile | Whether the person is in the system, plus PAN, past addresses, date of birth, other mobiles. No score | Studied in class |
| Credit report, soft pull | Name, PAN, date of birth, mobile (what KYC already returned) | Score, accounts, enquiries, summaries | Yes: score and the summaries on Step 4 |
| PAN verification | PAN | Name, type of holder | Yes, through DigiLocker's PAN details |
| Aadhaar KYC | Aadhaar number, then OTP to the Aadhaar-linked phone | Name, address, date of birth | Yes, through DigiLocker |
| DigiLocker | Redirect and consent | Signed documents from the source | Yes: PAN name, PAN number, date of birth |
| Vehicle search (registration lookup) | Vehicle number | Make, model, engine size, fuel type, manufacture month and year, registration date; also owner details | Yes, for the exchange car (owner details not used or stored) |
| Bank statement analysis | Statement file, or a login or consent flow | Salary, expenses, average balance, suspicious items | Studied; planned, not built |
| Account Aggregator | Mobile, OTP, consent | Read-only bank data | Not usable: only regulated lenders can use it |

## The credit report in our build

The soft-pull response came back in sections, and we used three:
- **Account summary:** number of active, closed and total accounts, defaults, suit-filed balance, total outstanding (secured and unsecured). We built credit health (Bad, Good, Best) from three of these fields.
- **Enquiry summary:** counts of enquiries in the last 7, 30, 90 and 180 days. Many recent enquiries suggest a borrower who is shopping around.
- **Non-credit enquiry summary:** same windows, for non-loan enquiries. We left these out.
- **Score:** missing for people new to credit. We added an "NTC" label and a path for it after the live demo.

## The vehicle lookup in our build

It returns the manufacturer's name, model, engine size, fuel type, norms and registration date, and the manufacturing month and year. Our exchange-value rule uses three of these: the maker, the engine size and the manufacturing month and year. The lookup only makes sense when the customer has an exchange car, so we skip it when they do not.

## Things I learned about using APIs

1. **Chain outputs into inputs.** What KYC returns is what the credit report asks for, so the customer types almost nothing.
2. **A "not found" answer is normal.** A no-hit is not an error. Plan the next step for it.
3. **Every call costs money**, so order them cheap to costly and skip the ones that do not apply (the vehicle check with no exchange car).
4. **Vendors fail.** The platform lets several vendors serve one check, with fallback.
5. **Formats differ** (dates, names), so someone must standardise them. The platform did that for us.
6. **Consent comes first.** Every credit call needs the customer's consent and a timestamp.
7. **Some data is only for regulated lenders** (Account Aggregator, hard pulls). Check who may call an API before designing around it.
8. **Mock an API when the real one is sensitive or slow.** The platform lets you host a fake response.

## Open or to verify

- The coverage and reporting claims about bureaus **[verify]**.
- Which exact bureau product our final journey used for the basic lookup. We used the soft pull for the score.
