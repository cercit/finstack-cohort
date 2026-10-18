# Learned to used

Each row links something taught in the cohort to where it shows up in the product, and says how far it got. **Built** = in the journey. **Partly** = built as a formula or rule but not fully on a screen. **Planned** = designed, not built. **Not used** = learned, deliberately left out.

| What we learned | Where it came from | Where we used it | How far |
|---|---|---|---|
| Nothing is checked before the customer agrees; a bureau call needs consent with a timestamp | Day 1, Day 2 | Step 1: terms tick, then a 6-digit code to the customer's own phone | Built (storage of the tick time to confirm) |
| Soft pull only; hard pulls belong to the licensed lender | Day 1, Day 2 | Credit score and summaries come from a soft pull | Built |
| KYC is two proofs; DigiLocker gives signed documents but redirects the user | Day 2 | DigiLocker stage between Step 1 and Step 2 | Built |
| Chain outputs into inputs so the customer types little | Pre-read 5, Day 2 | PAN, name and date of birth pre-filled; Customer_Inputs fully pre-filled | Built |
| Names rarely match exactly; use a fuzzy match and re-check rather than reject | Day 2, Pre-read 5 | A name-match expression built from built-in functions; mismatch rule | Partly |
| Exact match for PAN | Day 2 | PAN match gives 100 or 0 | Partly |
| Put cheap checks first and costly ones later | Day 2 | Skip the vehicle-number lookup when there is no exchange car | Built |
| "No data" is a normal answer; new-to-credit customers are the market | Day 2 | NTC label and an NTC-only lender path | Built after the demo |
| Underwriting asks four things: contactability, capability, collectability, intent | Day 2 | Lender fit rules on score, credit health, loan size and monthly commitment | Built |
| Pin codes are green, amber or red | Day 2, Pre-read 5 | An extra lender rule idea | Not used |
| Lenders borrow at different costs, so they serve different customers | Day 1, Pre-reads 3 and 4 | Four lenders with different thresholds, commission and trade advance | Built (test values) |
| Origination is where lenders differ; servicing is regulated | Day 1 | We built origination and settlement figures only; no servicing | Built |
| Account Aggregator is for regulated lenders; bank statement upload is open to all | Day 2, Pre-read 5 | Bank statement analysis planned; income is declared today | Planned |
| The bank statement step is the biggest funnel drop-off | Pre-read 5 | Kept out of the dealer stage | Not used |
| A rule engine should filter the target customer, not "all of India" | Day 2 | New-car buyers at Bengaluru Kia dealers | Built |
| Assisted onboarding lets staff fill a journey for the customer | Day 2 | The executive fills the journey for the customer | Built |
| The back office can list, filter and review cases | Day 1, Day 2 | "My cases" and a review queue | Planned |
| One person on forms, one on the journey, to avoid overwriting | Day 2 | Followed the same split with my teammate | Built |
| A complete simple product beats a half-built big one | Day 1, final brief | Cut the portal, dashboard and ledger; finished one journey | Built |
| Test edge cases | Final brief | The live demo found two we missed; a test list is written | Built after the demo |
| A written launch plan covers where more data can be pre-filled | Final brief (option 1) | The production launch plan | Built (late) |
| Logic variables are single expressions with limits | Hands-on, our build | Nine rules in [no-code-platform.md](cohort/no-code-platform.md) | Built |

How to read the gaps: the rows marked Planned or Not used are the honest edge of what we did in five days. They are also the roadmap.
