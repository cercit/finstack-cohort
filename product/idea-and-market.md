# DealerFinance: the idea, the market and the flow

The buyer just enquires about a car. In the background, the journey has already worked out which lender is likely to say yes, so the dealer talks about an EMI, not a loan form.

## The idea

DealerFinance is a loan journey for new-car dealers. It matches each buyer to the right bank or NBFC, sends the case, follows the decision and settles the dealer's trade advance and commission. It is built on a no-code lending platform.

| | |
|---|---|
| **For** | Multi-brand new-car dealers who work with several banks and NBFCs. The dealer pays for it, like a software subscription |
| **Used by** | The dealership executive, or the customer on their own link |
| **Customer** | An individual car buyer, mostly salaried. One enquiry, and the finance step happens quietly behind it |

## The problem

New-car dealers with tie-ups to several banks and NBFCs have no quick way to know which financier will approve a customer. So they guess, rejected cases bounce from lender to lender, customers wait or walk away, and the dealer's commission is chased on paper.

| Who feels it | How |
|---|---|
| Dealer principal | Loses car sales when finance falls through, and cannot see which lender performs |
| Finance coordinator | Guesses the lender, re-sends the same file and chases status by phone |
| Customer | Waits hours or days, and has several lenders check their credit one after another |
| Accounts team | Tracks commission, GST and TDS on paper and finds short payments late |

## Why it is not solved today

There is no one place that holds the whole case. The pieces sit in three systems, and cases and money leak in the gaps.

| System | What sits there | What leaks |
|---|---|---|
| CRM | Leads and follow-ups, with no idea which lender will approve | Leads are lost between the CRM and the lender |
| Lender calls and portals | The same file re-sent and status chased by phone | A rejection arrives late and the case starts again |
| Accounts | Commission, GST and TDS on paper or in a sheet | Short-paid or forgotten commission is found weeks later |

## How it works

**As built:** six steps. Enquiry with a one-time code, DigiLocker, Verification, Customer inputs (price, tax, loan, all pre-filled), Routing-1 (score and a lender pick), Routing-2 (the lender's answer), then Settlement (trade advance and commission). A rejected case goes back to Routing-1.

**The full design** was bigger. We had no database or lending system, so we built a lean version: one linear journey filled by the customer or a dealer executive. This table shows what that meant for each stage.

| Stage | What it is | Built? |
|---|---|---|
| 1. Enquiry and consent | Terms tick, then a code to the customer's phone | Built |
| 2. Credit check | Score and health from the bureau | Built |
| 3. KYC | DigiLocker: Aadhaar OTP, PAN, name, birth date | Built |
| 4. Income and EMIs | Declared by the customer, no bank statement | Simpler form |
| 5. Match to lenders | Rules on score, health, loan and EMI burden | Built |
| 6. Pick and send | One lender, chosen by the executive | Simpler form |
| 7. Lender decides | Approved or rejected, set by hand; rejected goes back | Simpler form |
| 8. Commission and trade advance | Demo limits, no running balance | Simpler form |
| Review queue, dashboard, My cases | Need a database or the listing page | Not built |

## Market size

The pool is the finance commission that lenders pay on vehicle and home loans each year. Public numbers where they exist, and marked assumptions where they do not.

| Level | Meaning | Size a year |
|---|---|---|
| TAM | All four loan lines | Rs 9,130 to 16,905 crore (base case about Rs 11,900 crore) |
| SAM | New-car finance through dealers, where we start | About Rs 4,520 crore |
| SOM | Bengaluru, six brands | About Rs 2.1 crore in software fees |

SOM is 178 Bengaluru outlets × a fee × 12 months. The fee is an assumption (Rs 10,000 per outlet per month), so change it to test. For scale only, 1,000 outlets at the same fee would be about Rs 12 crore a year.

| Line | Units a year | On loan | Average loan | Commission | Pool a year |
|---|---|---|---|---|---|
| New car | 47.05 lakh (FADA FY26) | 80% | Rs 8 lakh assumed | 1.5% | Rs 4,517 crore |
| Used car | about 60 lakh (Crisil) | 25% to 52% | Rs 4 lakh assumed | 1.5% assumed | Rs 900 to 1,872 crore |
| Two-wheeler | 2.14 crore (FADA FY26) | 75% | Rs 60,000 assumed | 1.5% assumed | Rs 1,446 crore |
| Housing loan | Rs 9.07 lakh crore disbursed (FY24) | n/a | n/a | 0.25% to 1% | Rs 2,268 to 9,070 crore |

The 1.5% commission follows one bank's published dealer payout of 1.45% on car loans. Average loan sizes and the used-car and two-wheeler commissions are assumptions, so treat the totals as an order of magnitude.

## It scales: the same engine, different lenders and rules

| Line | What changes |
|---|---|
| New car | What we built. Dealer price lists and road tax drive the loan amount |
| Used car | Same flow. A resale estimate (brand, engine size, year) sets the car's value and the exchange value |
| Two-wheeler | Smaller loans, higher volume, faster rules and lighter checks |
| Housing loan | Larger loans and property papers: more checks, lower commission rate |
| Any commission business | Anywhere a seller refers a customer to a lender and is paid when the loan is disbursed |

What stays the same: enquiry and consent, credit check, match to lenders, send, follow the decision, commission. What changes: the lender rules, the price or valuation tables and the commission rates.

## What comes next

With a database and lending-system access: two menus (sales or customer, and finance or accounts), a real review queue, dashboards and a commission ledger with GST and TDS, live trade advance and lender status, bank statement analysis, then used cars, two-wheelers and housing loans.

## Sources and assumptions

- [Auto retail FY26: passenger vehicles 47,05,056 units](https://www.outlookbusiness.com/industry/auto-retail-sales-up-133-pc-at-29671064-units-in-fy26-fada)
- [Two-wheeler retail FY26: 2,14,20,386 units](https://www.wealthy.in/invest/news/market/1684268)
- [About 80% of four-wheelers registered in 2025 were bought on loan](https://www.businesstoday.in/auto/story/nearly-80-cars-bought-on-loans-govt-rules-out-parking-proof-rule-523721-2026-04-02)
- [Used cars: about 6 million units in FY26 (Crisil)](https://integraliq.crisil.com/content/crisilratings/en/home/newsroom/press-releases/2025/07/used-car-volume-to-grow-8-10percent-over-twice-as-fast-as-new-one.html)
- [Used-car buyers on loan: 52% in 2025 (Cars24 report)](https://www.storyboard18.com/brand-makers/tier-2-india-accounts-for-62-of-used-car-demand-cars24-report-90715.htm)
- [Used-car sales financed: 25% (Business Standard, 2024)](https://www.business-standard.com/industry/auto/demand-for-3-5-years-old-used-cars-outpaces-supply-drives-prices-north-124052301254_1.html)
- [About 75% of two-wheelers financed (Bajaj Auto)](https://www.autocarindia.com/industry-amp/two-wheeler-industry-to-surpass-212-crore-unit-sales-by-fy25-says-bajaj8217s-rakesh-sharma-432269)
- [Housing loan disbursements FY24: Rs 9.07 lakh crore (NHB, reported)](https://www.business-standard.com/finance/news/india-s-housing-finance-struggles-with-regional-disparities-warns-nhb-125031201033_1.html)
- [DSA commission on home loans: 0.25% to 1% of the amount disbursed](https://easyhomefinance.in/knowledge-hub/?p=985)

All customer names, lender terms, trade advance limits and commissions shown in the product are demo values. Prices are Bengaluru ex-showroom listings checked on 12 Oct 2026.
