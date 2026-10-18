# Lessons from the live demo

About 15 to 16 people used the journey during the live demo, and some of them tried edge cases we had not tested. This note records what that taught us and the small changes we made afterwards, some of which also cut cost.

Written 18 Oct 2026 from the team's own account. We did not log each attempt, so the counts below are only what we remember.

## What happened

| # | Situation | What the journey did | Why it was a problem |
|---|---|---|---|
| 1 | A customer new to credit (NTC) | The credit report returned no score. The screen had nothing to show and the next step needed a number | A dead end, and the credit report request kept going |
| 2 | A customer with no car to exchange | The vehicle-number check only works with an exchange car, so the journey stopped on that screen | A dead end, and a paid lookup that could not succeed |

## What we changed

| # | Change | Effect |
|---|---|---|
| 1 | If no score comes back, show "NTC" and carry on, offering only lenders that accept NTC. The credit report request stops at that point. No change is needed on the dealer platform | No dead end for NTC customers; no repeat requests for someone with no file |
| 2 | Skip the vehicle-number check when exchange is No. It runs only when exchange is Yes | No dead end; one paid lookup fewer for every case without an exchange car |

Still to do for the NTC path: the lender fit rule must treat "NTC" as a valid answer, and we need the list of lenders that accept NTC, confirmed with each lender.

## What it taught me

1. **"Not available" is a normal answer.** Every outside call needs a path for an empty reply that shows a plain label and moves on.
2. **Other people find the cases you did not think of.** Our own testing followed the happy path. A room of strangers took other paths within minutes.
3. **Cost and experience can improve together.** Removing a call that could not succeed saved money and removed a dead end in one change.
4. **Do the check that applies.** A step should run only when it is relevant to this customer.

## What I would test next time

- A customer with no score, a very low score, and a score just on a lender's threshold.
- No exchange car, an exchange car with a bad vehicle number, an exchange car too old to value.
- Wrong OTP, an expired OTP, a refresh in the middle of a step.
- A name or PAN that does not match DigiLocker.
- A car that is not in the price table.
- A lender that approves less than asked, and one that rejects.
- Slow or empty answers from each outside service.
- A phone-sized screen.
