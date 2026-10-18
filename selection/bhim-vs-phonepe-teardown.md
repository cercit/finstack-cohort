# BHIM vs PhonePe: the selection project

As part of FinStack's candidate evaluation, I submitted a product teardown of two payment apps with a three-year roadmap for each. The original PDF is linked at the bottom of the page and shown below it. I was selected for the cohort after it.

**The idea in one paragraph.** Both apps run on the same UPI rails, and paying a shop takes the same four steps on each: scan, amount, confirm, Face ID. Yet I use BHIM for most payments, and the reason is not features. BHIM leaves me alone; PhonePe keeps alerting me. PhonePe shows too much, BHIM shows too little, and each app's ownership explains why.

## 1. Regulation and licences decide what each can build

| | BHIM | PhonePe |
|---|---|---|
| Owner | NPCI BHIM Services Ltd (NBSL), a for-profit subsidiary of NPCI since Oct 2024. NPCI is a not-for-profit company owned by banks that runs the UPI rails | PhonePe Ltd, an Indian public company (pre-IPO). Walmart holds 71.77%. Moved home from Singapore to India in 2022 |
| Licences | None of its own beyond running the UPI app. Bill pay and UPI International sit in other NPCI companies; credit, loans, insurance and NPS come through partners | Wallet, bill-pay unit, insurance broker and stockbroker licences, each in a separate company |
| How it sells credit | Partner lenders, shown below the fold | Lending service provider for partner banks and NBFCs. No NBFC licence |
| Main constraint | Its parent runs the rails, so it must stay neutral | A 30% UPI market cap from 31 Dec 2026; it was at 45.9% in Aug 2026 |

PhonePe has applied for an NBFC licence three times (2021, 2023, January 2026), so it cannot lend from its own book and earns a commission as a middleman. It gave back its Account Aggregator licence in February 2025. Its other licences sit in separate companies, which is why tapping "Stocks" throws me out to another app. BHIM can make a profit, but its parent is the referee of the whole network, so BHIM sells quietly through partners and never pushes.

## 2. Product and experience

On PhonePe about 30% of the first screen was a credit card ad, a referral promo sat even inside money transfer, and strips sold EMIs and gold. On BHIM the top is a search bar, UPI Lite and balance, with Scan highlighted; loans, cards and investments are there but I had to scroll a long way to find them.

PhonePe is built as a store that happens to take payments, for the mass market and 50 million merchants. BHIM is built as a utility for anyone who just wants to pay. PhonePe's biggest risk is not Google Pay, it is its own home screen. BHIM has the right products but hides them so well that almost nobody knows they exist.

## 3. Who pays for free payments

| Rs crore | FY24 | FY25 | FY26 |
|---|---|---|---|
| PhonePe revenue | 5,064 | 7,115 (+40%) | 7,920 (+11%) |
| PhonePe net loss | 1,996 | 1,727 | 2,792 |
| PhonePe lending revenue | | 378 | 945 |
| NPCI profit | 1,134 | about 1,450 | 989 |
| BHIM (NBSL) loss | | 68 | 391 |

PhonePe keeps payments free because the daily habit is how it acquires customers; it earns later from loan, insurance and wealth commissions, merchant devices, ads and government UPI incentives. Lending is now the engine, up 2.5 times in a year. BHIM charges nothing because it is meant to be the neutral, ad-free option, and NPCI's surplus pays the bill. My rough estimate: PhonePe loses about Rs 0.21 per transaction and BHIM about Rs 2.4, so BHIM pays roughly ten times more per transaction to grow. From 15 October 2026 merchants pay 0.4% (capped at Rs 300) on UPI payments above Rs 2,000, the first real fee on UPI.

## 4. A three-year roadmap for each

**PhonePe: convert payers into paying customers.**

| | Year 1 (2027) | Year 2 (2028) | Year 3 (2029) |
|---|---|---|---|
| Goal | Get under the cap without losing the business | Commissions become core | Profitable enough to relist |
| Build | Engage NPCI with data, don't oppose it. Let go of small daily payers who never convert. Replace the crowded home screen with an AI search bar ("pay electricity bill" gives one option, not ten). Fewer alerts. Make the above-Rs 2,000 fee work for merchants | A loan-fit engine that offers the right loan at the right price. A loan tracking system run as a service for lenders. Non-compete terms for big lenders | Own underwriting model built on the repayment data, ready if the NBFC licence comes. Restart the IPO on commission-led profit |
| Threat | The cap; BHIM's assistant getting there first | Lenders going around PhonePe to its customers; users feeling pushed into costly loans | Regulator trust |

North star: paying customers as a share of active users. Guardrail: total commission revenue must keep growing, so the ratio can't rise just because users leave.

**BHIM: run it like KSRTC.**

| | Year 1 (2027) | Year 2 (2028) | Year 3 (2029) |
|---|---|---|---|
| Goal | Become the quiet app people choose | Win on need in rural India | 5% of UPI, top five |
| Build | Pitch working professionals who hate ads. Offer it to government staff, starting with the armed forces, not as a mandate. Move ad money from cricket news to Instagram, YouTube and Bigg Boss. Use the assistant to manage autopays from any app | Ration shops, tea stalls, mandis. A safe place for farmers to park lump-sum crop money and withdraw any time, through bank tie-ups; Tatkal NPS. Products shown by need, not by banner | First app to carry every new UPI feature. Bring the loss per transaction down each year. Pick up what PhonePe must give up under the cap |
| Ignore | Offer-chasing 18 to 27 year olds; leave them to PhonePe, Google Pay and Navi | | |

North star: active users as a share of registered users. Guardrail: monthly active users and UPI share must grow in absolute terms. Biggest threat: spending Rs 391 crore a year to stay invisible.

## Conclusion

Being government-owned doesn't make BHIM lose, just as it doesn't stop KSRTC from winning. Karnataka chooses KSRTC because it is run well, not because it is cheap. BHIM's problem is execution, not ownership. PhonePe's problem is the reverse: it does too much, too loudly, on a rail it will soon be allowed less of.

## How I made it

I used Gemini, ChatGPT, Hermes and Claude to gather research, and Claude to cross-check figures, interview me on my views and help draft the text from my answers. Every figure was checked at its source. The app observations, opinions, roadmap choices and the analogy are my own. Sources: NPCI and NBSL filings and releases; PhonePe press releases and its draft prospectus (Jan 2026); TransUnion CIBIL; Inc42, Entrackr, Outlook Business, Business Standard, Medianama, SCC Online. App observations are my own, 26 Sep 2026.

[Download the original PDF](bhim-vs-phonepe-teardown.pdf)
