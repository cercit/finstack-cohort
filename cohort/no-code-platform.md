# How a no-code lending platform works, and what building on it taught me

FinStack is software for lenders. This note covers how the platform is put together and the rules I learned the hard way while building DealerFinance on it. Written in my own words.

---

## The shape of the platform

| Piece | What it is | How I used it |
|---|---|---|
| API hub | Ready verification APIs | Bureau soft pull, DigiLocker, vehicle lookup |
| Forms | The building block of a journey. Two kinds: forms that call an API, and custom forms | One form per step; custom forms for income, EMI and the car |
| Journey | Orders forms into steps, sets the unique identifier and what happens on failure | Six steps and DigiLocker; a rejected case returns to an earlier step |
| Rules | Verification rules, visibility rules, logic variables | Name match, a field that shows only when exchange is Yes, and all the money formulas |
| Back office | Listing, filters, review screens | Planned as "My cases" |
| Audit trail | Every entry and response logged | Used as the consent record |

The platform serves the lender's staff and customers. It is a horizontal tool: it orchestrates many services rather than doing one thing deeply.

## Logic variables: the rules I learned

A logic variable is a short expression that computes a value from other fields. There is no programming environment around it.

1. **It is one expression.** No statements, no libraries. Plain operators, `x if condition else y`, and built-in functions.
2. **A dictionary pasted as text is just a string.** Keep the dictionary inside the expression.
3. **Put brackets around a dictionary before `.get`:** `({...}).get(key, default)`. Without them, the whole dictionary came back and the field failed with a type error.
4. **After a page refresh a number can come back as text.** A comparison then fails quietly (our TCS dropped to 0). Wrap values in `int(...)`.
5. **Keys must match exactly.** Use lowercase, snake_case keys and lowercase lender names, or call `.lower()` on the saved value.
6. **Imports are restricted.** Our attempts to read today's date through `datetime` and to use `difflib` for a fuzzy match were refused. We rebuilt the fuzzy match with plain built-ins (sorted words, pairs of letters, set overlap). For today's date we used a fixed date until a date variable exists.
7. **Test the formula in plain Python first**, then paste it in. Python passing does not prove FinStack accepts it.
8. **A name in the display can differ from the saved value.** The financier drop-down showed "Bajaj" while the formulas expected "bajaj". Check the saved value.
9. **Labels are easy; variable paths are not.** Fix a typo in the display name only, never in the variable path.

## Journey design lessons

- **Test each form once** after building it, so the system learns its output fields.
- **Two people can edit one journey but may overwrite each other.** One person on forms, one on the journey.
- **Changes to a live journey do not reach people already past that step.** Copy the journey and roll out to a small share.
- **A rejection must have a route.** Ours had one on paper, but the field that makes the reroute possible did not exist on the rejected path, so the first test failed.
- **Every outside call needs an empty-answer path.** Two dead ends found at the live demo (no score, no exchange car) came from this.

## What the platform could not do for us

No separate login for dealers, no database to remember earlier cases, and no menu setup. That is why DealerFinance became one linear journey used by a customer or an executive, with fixed demo values for the trade advance used so far.

## What I took away

The hard part of a no-code build is not the clicking. It is knowing the rules the platform follows, testing each formula outside it first, and designing for the cases where an outside service returns nothing.
