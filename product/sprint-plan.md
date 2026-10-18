# DealerFinance: sprint plan

**Status:** draft for review, written 18 Oct 2026.
**Team 6:** Sameer S Mittimani and Aditya Sharan.
**Format:** the work-breakdown from Class 11: epic > story > Given/When/Then > scenarios and edge cases > tasks (team, output, estimate) > sequencing gates > scope, time and cost > roadmap.
**Honesty note:** this plan is written after the sprint, from the files, notes and chat that exist. Dates come from file times and the cohort chat. We did not record estimates at the time, so the estimate column says "not recorded" instead of inventing days. Class 11's own rule applies: task days are effort, not elapsed time.

---

## 1. Sprint frame

| Item | Value |
|---|---|
| Sprint | Sprint 1: FinStack cohort hackathon |
| Working days | 9, 10, 12 and 13 Oct 2026 (11 Oct was an office-closed day; work continued at home) |
| Goal | A customer or dealership executive can finish a car-loan journey on FinStack with minimal typing, and the executive can see the cash needed and the dealer's trade advance and commission |
| Fixed constraint | The demo slot at the end of the cohort; the time was fixed, so scope had to move |
| Team | Team 6 (two people); FinStack mentors helped on platform questions |
| Definition of done | The journey runs end to end for the approved path; other people in the room can complete it; edge cases found in testing are fixed or written down |

## 2. Epics

| ID | Epic (outcome) |
|---|---|
| E1 | Consent and identity: the customer agrees, and we know who they are |
| E2 | Price and loan: the loan amount is worked out for the chosen car without hand calculation |
| E3 | Lender fit and routing: the executive sees which lenders are open and can reroute after a rejection |
| E4 | Settlement: the exact cash needed, trade advance balance and commission are visible |
| E5 | Resilience: a missing answer from an outside service never stops the journey (added after the live demo) |

## 3. User stories and Given/When/Then

Format from class: *As a ___, I want ___, so that ___.* Priority P1 must work, P2 needed for launch, P3 later.

| ID | Epic | Story | Priority |
|---|---|---|---|
| S1 | E1 | As a customer, I want to confirm my consent with a code on my own phone, so that nothing is checked without my agreement | P1 |
| S2 | E1 | As a customer, I want to verify through DigiLocker, so that I do not hand over document copies | P1 |
| S3 | E1 | As an executive, I want PAN, name and date of birth pre-filled, so that I do not type them again | P1 |
| S4 | E2 | As an executive, I want price, road tax, insurance, TCS, on-road price and loan to fill themselves for the chosen Kia, so that the figure is right and fast | P1 |
| S5 | E3 | As an executive, I want to see which lenders are likely, possible or not a fit, so that I pick one that will accept | P1 |
| S6 | E3 | As an executive, I want a rejected case to return to the lender choice, so that the sale is not lost | P1 |
| S7 | E4 | As an executive, I want to see the extra down payment when the approved amount is lower, so that I can tell the customer the exact cash | P1 |
| S8 | E4 | As a dealer, I want the trade advance balance and commission shown for the case, so that I see my own money | P2 |
| S9 | E5 | As an executive, I want a customer with no credit score to show "NTC" and carry on, so that the journey does not stall | P1 |
| S10 | E5 | As an executive, I want the vehicle-number check skipped when there is no exchange car, so that the journey does not stop | P1 |

**Given / When / Then records**

| Story | Given | When | Then |
|---|---|---|---|
| S1 | The customer's mobile is entered and the terms box is ticked | The code is sent and the customer types it | A correct code continues to DigiLocker; a wrong code blocks and allows resend |
| S4 | A Kia model is chosen and the down payment and exchange answer are in | Step 3 opens | All seven fields are filled; loan = on-road − TCS − down payment − exchange value |
| S5 | Score, credit health, loan and monthly commitment are known | Step 4 opens | Each of the four lenders gets likely, possible or not a fit, and one can be chosen |
| S6 | A case was sent to a lender | The status is set to rejected | The case returns to Step 4 to choose another lender |
| S7 | The lender approved less than the loan requirement | Step 6 opens | Additional down payment = loan requirement − approved amount |
| S9 | The bureau returns no score | Step 4 opens | The screen shows NTC and only lenders that accept NTC are offered |
| S10 | Exchange is answered No | Step 2 is submitted | No vehicle number is asked and the journey moves on |

## 4. Scenario and edge-case matrix

| Story | Environment | Starting state | Event | Expected result | Evidence |
|---|---|---|---|---|---|
| S1 | Customer's phone | Terms ticked | Wrong code typed | Blocked, resend allowed | Seen in the screen recording |
| S2 | DigiLocker | Customer verified | Return to the journey | Step 2 opens with PAN filled | Seen in the screen recording |
| S4 | Page refresh | Step 3 filled | Browser refreshed | TCS and loan stay right | A bug was found (TCS dropped to 0 because the value came back as text) and fixed |
| S4 | Price table | Kia model not in the table | Step 3 opens | Price shows −1; executive types the price | Not built |
| S5 | Bureau | Score 650, health Good | Step 4 opens | sbi and hdfc not a fit; bajaj and chola possible | Worked through on paper from the rules |
| S6 | Routing-2 | Status chosen "rejected" | Submit | Return to Step 4 | Found a defect: error "Missing key approved_finance_amount" |
| S7 | Routing-2 | Approved 15,00,000 of 15,17,728 | Step 6 opens | Additional down payment 17,728 | Seen in the screen recording |
| S9 | Bureau | No score returned | Step 4 | NTC and NTC-accepting lenders | Found at the live demo; fixed after |
| S10 | Verification | Exchange No | Submit | Vehicle number skipped | Found at the live demo; fixed after |
| S4 | Loan formula | Exchange value filled after the loan was worked out | Step 3 | Loan recomputes | Defect: loan ignored the exchange value |
| Any | Outside API | Returns nothing | Any step | Plain label, move on | Principle; each call still to be tested |

## 5. Tasks, team and output

Teams are shown by function. Estimates were not recorded. "Done on" comes from file dates and the chat.

| Task | Team (function) | Output | Estimate | Done on |
|---|---|---|---|---|
| Lock the product idea and problem | Product | Idea and problem statement | not recorded | 9 to 10 Oct |
| Flowchart and low-fidelity screens, emailed to FinStack | Product and design | Flowchart and wireframe | not recorded | 10 to 11 Oct (the first email was flagged for the format; a revised wireframe followed on 11 Oct) |
| PRD decisions F1 to F26 | Product | Decisions log | not recorded | 10 to 11 Oct |
| Revised wireframe and the F15 to F26 changes | Design | Wireframe v2 | not recorded | 11 Oct |
| Lender panel and personas workbook | Product and data | Workbook with ten lenders, rules and personas | not recorded | 12 Oct |
| Kia price table (182 variants) and road tax lookup | Data and build | Dictionary expressions and JSON | not recorded | 12 to 13 Oct |
| Journey screens 1 to 6 in FinStack | Build | Working six-step journey | not recorded | 12 to 13 Oct |
| Formulas: insurance, TCS, on-road, loan, LTV, credit health | Build | Logic variables | not recorded | 13 Oct |
| Lender fit formula (four inputs, six outputs) | Build | One formula, tested in Python | not recorded | 13 Oct |
| Trade advance, used, finance amount and commission | Build | Logic variables | not recorded | 13 Oct |
| Test passes and fixes (refresh bug, dictionary bracketing) | Build and test | Fixes | not recorded | 13 Oct |
| Pitch page and 5-minute problem statement | Product | Pitch page | not recorded | 13 Oct |
| Live demo | Team | Demo with about 15 to 16 people using the journey | not recorded | 13 Oct evening |
| NTC path and vehicle-number skip | Build | Two changes | not recorded | after the demo |
| Production launch plan | Product | Plan (pdf) | not recorded | written 16 Oct, sent late |

## 6. Sequencing and gates

Discovery > design > build > test > demo > fixes > launch plan.

| Gate | Passed? | Evidence |
|---|---|---|
| Idea locked | Yes | Team list and problem statement |
| Flowchart submitted in the right format | Partly | First email was flagged by FinStack for the format (no team number in the subject); a revised wireframe was sent on 11 Oct and no reply is in the chat |
| Wireframe signed off | Not confirmed | Revised wireframe sent 11 Oct, no sign-off seen |
| Journey runs end to end on the approved path | Yes | Screen recording |
| Rejected path works | **No** | Error on "rejected" |
| Zero wrong-money defects | **No** | Loan ignored the exchange value |
| Demo done | Yes | Live demo, other people completed the journey |
| Production launch plan sent on time | **No** | Sent after the deadline |

## 7. Scope, time and cost trade-off

| Axis | What was fixed | What gave |
|---|---|---|
| Time | The demo slot | Everything else |
| Scope | Started wide (lender portal, commission ledger, dashboard, review queue, CSV upload) | Cut to one linear journey with settlement figures, because FinStack's builder had no login, no database and no menu setup for us |
| Cost | No spend beyond time | Real lender data, API connections and the asset value were replaced by tables, rules and test values |

After the demo, two small changes cut paid or wasted calls: the vehicle-number lookup is skipped when there is no exchange car, and the credit report request stops once NTC is known.

## 8. Roadmap

| Sprint | Goal | Gate to leave |
|---|---|---|
| Sprint 2: fix | Fix the loan formula and the rejected path; show credit health and readable car names; remove the rejected lender from the list; test every outside call with an empty answer | All P1 stories pass on every path |
| Sprint 3: connect | Real PAN autofill, asset value, lender send and status; lender list for NTC; a date variable | One real case end to end |
| Sprint 4: pilot | One or two Kia outlets; baseline completion and decision time | Pilot report |
| Later | Bank statement analysis, review queue, dealer login and dashboard, more brands, used cars | Decided after the pilot |

## 9. Retrospective

**What went well:** the journey ran end to end; most fields pre-fill; other people could complete it at the demo; the checks (name, PAN, age) were written as expressions even where no screen shows them.

**What went wrong:**
- The first flowchart email broke the submission format, and the launch plan went in late.
- We found the loan defect and the rejected-path error late.
- Edge cases (NTC, no exchange car) were found by other people at the demo, not by our own testing.

**What we do differently:** write the edge-case matrix before building, run every outside call with an empty answer, check the money fields by hand on each path, and read the submission rules before the last day.

## 10. What stays unknown

Individual task estimates, the number of test cases run, and the outcome of the judging. They are not in any file, so this plan leaves them blank.
