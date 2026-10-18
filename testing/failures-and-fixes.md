# Failures and fixes

What broke while building and testing DealerFinance, why, what we did, and what I would do differently. The status is as of 18 Oct 2026.

**Status key:** Fixed = verified working. Open = known and not fixed yet. Process = a mistake in how we worked, not in the product.

## Product and formula failures

| # | What broke | Cause | Fix | Lesson | Status |
|---|---|---|---|---|---|
| 1 | A price lookup returned the whole dictionary and the field failed with a "not of type float" error | The dictionary was not wrapped in brackets before `.get(...)` | Write `({...}).get(key, default)` | Brackets decide what `.get` acts on | Fixed |
| 2 | TCS dropped to 0 after a page refresh, and the loan and TCS disagreed | After a refresh the value reached the formula as text, so a "greater than" test failed quietly | Convert with `int(...)` or keep values numeric | A refresh can change a number's type. Test with a refresh | Fixed |
| 3 | Insurance showed the same amount as the vehicle price | Not recorded at the time | Rebuilt it as 4% of the ex-showroom variable | Name each value once and build on it | Fixed |
| 4 | On-road price and loan treated TCS differently | Two formulas made different assumptions | Decision: on-road leaves TCS out; the loan subtracts it | Write the rule down before writing formulas | Fixed |
| 5 | Loan and commission showed a trailing ".0" | A whole number came back as a decimal | Wrap in `int(...)` where it matters | Cosmetic, but visible to a customer | Open (cosmetic) |
| 6 | The lender drop-down showed "Bajaj" while formulas expected "bajaj" | Displayed text and saved value are different things | Use lowercase values, or `.lower()` | Check the saved value, not the label | Fixed |
| 7 | A fuzzy name match using a standard library was refused | The platform restricts imports | Rebuilt it from built-in functions (sorted words, pairs of letters, set overlap) | Test in the real platform early | Fixed |
| 8 | A formula that reads today's date was refused | The platform rejected the date calls we tried | Use a fixed date until the platform offers a date variable | Ask the platform team what is supported | Open |
| 9 | The loan ignored the exchange value (15,17,728 shown with an exchange value of 3,13,000; it should be 12,04,728) | The loan was worked out before the exchange value filled in | Recompute the loan after the exchange value is set; re-test | Check money fields by hand on every path | Open |
| 10 | Submitting "rejected" gave "Missing key approved_finance_amount" | The approved amount only exists on the approved path | Default it to 0 on a rejection | Every route needs every field it reads | Open |
| 11 | The rejected lender was offered again on Step 4 | The list did not remove it | Remove the rejected lender from the list | Close the loop on a reroute | Open |
| 12 | "Income p.a" was net of EMI, not gross | The figure works out as (monthly income - EMI) x 12, which is net of EMI | Rename the label or change the formula | A label is a promise | Open |
| 13 | Credit health disappeared from Steps 4 and 5 | It is not on the final screens (the formula still runs) | Show it again on Step 4 | Keep the reason for a decision visible | Open |
| 14 | Step 5 showed the car code, not the name | The saved key was shown | Show the readable name | Show people names, not keys | Open |

## Found at the live demo

See [live-demo-lessons.md](live-demo-lessons.md): customers new to credit with no score, and the vehicle-number check that stopped the journey when there was no exchange car. Both are fixed.

## Process failures

| # | What went wrong | Why | What I do now |
|---|---|---|---|
| P1 | The first submission email did not follow the required format (no team number in the subject) | I did not read the rule before sending | Read the submission rules before the last day, and check the format against the message |
| P2 | The production launch plan was sent after the deadline | I treated it as a separate task and left it to the end | Plan the written deliverable at the same time as the build |
| P3 | My Day 1 notes had the hackathon format wrong (they said to build a front-end on the APIs; the recording says to build on the form and journey builders) | I wrote from memory before checking the recording | Check notes against the source before using them |
| P4 | Price tables were built for five other car brands when only Kia was needed | I assumed the scope instead of asking | Confirm scope before building anything beyond the request |
| P5 | A short reply such as "ok" was taken as a go-ahead | I read it as approval | A bare acknowledgement is not approval; ask |
| P6 | Edge cases were found by other people at the demo, not by our own tests | We had no edge-case list before building | Write the edge-case matrix first |

## What I would do differently

1. Write the edge-case matrix before building, and run every outside call with an empty answer.
2. Test each formula in the platform on the day it is written, not only in plain code.
3. Check every money field by hand on the approved, rejected and no-exchange paths.
4. Read the submission rules on day one and plan the written deliverable early.
5. Keep a short running log of each failure as it happens, with the cause.
