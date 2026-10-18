# How this record was made: process and learnings

Written 18 Oct 2026. It lets someone pick the work up later without the long conversation that produced it.

## What exists

| Part | Where | State |
|---|---|---|
| Learning notes (day 1, day 2, days 3 to 5, APIs, platform, consent) | `cohort/` | Written, in the author's own words |
| Class-topic to product table | `learned-to-used.md` | Written |
| PRD (Class 9 format, with a north star metric), sprint plan (Class 11 format) | `product/prd.md`, `product/sprint-plan.md` | Written afresh from the work done |
| Idea, market and flow (the old pitch and overview pages, merged) | `product/idea-and-market.md` | Written. The old pages are in `product/archive/` |
| Decisions log, short, with how the logic was built | `product/prd-decisions-log.md` | Written. The full log is in `product/archive/` |
| Wireframe (as built, from the screen recording) | `product/journey/wireframe-as-built.html` | Written |
| Formulas | `product/formulas/` | In the repo, not on the site |
| Failures and fixes, live-demo lessons | `testing/` | Written |
| Production launch plan (md, html, pdf) | `launch/` | Written, sent late |
| Masked demo clip with music | `product/demo/` | Done |
| Site builder, design files, logos | `tools/build_site.py`, `tools/site_assets/` | Done; builds `site/` (not committed) |
| What was removed and how it was checked | `REDACTION.md`, `tools/scan_sensitive.py` | Done |

## How to rebuild

- **Site:** `python tools/build_site.py`, then `python -m http.server 8766 --bind 127.0.0.1 --directory site` and open http://127.0.0.1:8766/. The builder needs `markdown-it-py` and ffmpeg.
- **Scan for personal data before any commit:** `python tools/scan_sensitive.py .`. Classmates' names go in `tools/names.local.txt`, which is git-ignored.
- **Clip:** see `tools/video/README.md`. **Music:** `python tools/make_music.py out.wav 144.7`.

## Rules we worked by

1. The repo is **private first**. It becomes public only when the author says so. Making it public also needs the history rewritten (the commit email, and the old commit that shows the first six digits of an Aadhaar number), then a force-push.
2. No mobile numbers, PAN, Aadhaar, emails, logins or other people's names in anything committed. Run the scanner every time.
3. Ask before building more than was asked. A bare "ok" is not approval.
4. FinStack's material is theirs: notes are in the author's own words, with no client figures. Their name and logo are shown only to identify the cohort.
5. Test values stay labelled as test values: lender names, rates, limits and car prices are not real terms.

## Learnings

**Working with the files**
- Convert PDFs and Word files to markdown first, then read. It is much cheaper.
- Replace fixed claims with their source. Several first drafts said things the chat or files did not support (a sign-off from FinStack, a date for the demo). Each was checked against the record and corrected.
- Keep the full original next to the short version (`product/archive/`) when shortening a document.

**Privacy**
- The things that nearly leaked were not the obvious fields. They were digits typed into the wrong box, a name scrolling half out of view, a password-manager popup with an account number, and a placeholder showing the first digits of an ID.
- A check with a control (it must find the sensitive text in the original) is worth more than looking at samples.
- Changing the rule ("show my name now") changes what the earlier checks mean. Re-run them.

**Building the site**
- Reusing the author's own design files (`tools/site_assets/`) gave a consistent look for free. Copy the stylesheet, fonts and script, and add one small extra stylesheet for the new parts (tables, code, tags).
- Test every page at phone width. A nav row with margins and long unbroken text each caused a sideways scroll.
- Show small evidence tags (Built, Planned, Assumption, Test value) as badges, with a one-paragraph explanation at the top of the page that uses them.

**Product thinking**
- The north star for this journey is completed journeys per outlet per week, with the funnel steps as inputs. Targets wait for a pilot baseline.
- The two live-demo failures (no score, no exchange car) were both "an outside call returned nothing". Every external call needs a path for an empty answer.
- The biggest open defect is that the loan ignored the exchange value. It is listed in `testing/failures-and-fixes.md`.

## Open items

- Publish: the author's explicit yes, the history rewrite, then copy the site into a `finstack/` folder of the `cercit.github.io` repo.
- Tell FinStack before the notes and logo go public.
- Ask the teammate before his name and link go public.
- Fix the loan formula and the rejected path in the journey.
- NTC: the lender list that accepts customers new to credit.
