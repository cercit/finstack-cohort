# What was removed from this repo, and how

This repo comes from real working files, chat messages, screenshots and a screen recording. Before anything went in, personal and platform-specific details were removed. This page says what and how, without repeating any of it.

## Removed or masked

| Kind of detail | What was done |
|---|---|
| Mobile numbers | Not included. Screens show a masked form such as `94xxxxxx99` |
| PAN numbers | Not included. Example PANs in the notes are made up |
| Aadhaar numbers | Not included. The Aadhaar steps happen on DigiLocker, and the demo clip stops before them |
| Email addresses | Not included |
| Customer and classmate names | Not included. Screens use initials such as "S. S. M."; classmates and mentors are not named |
| Platform logins, shared passwords and links to test journeys | Not included |
| Account-specific IDs in the FinStack variable paths | Replaced by `<id>` in the formulas |
| Vehicle registration records | Only the field names and the three fields our rule uses are described. No owner details |
| FinStack client figures, tech details and course material | Not copied. The cohort notes are in my own words and leave out the client examples |
| Other people's work | Not included (the teammate's data folder and a public repo he started are left out) |

## Left out entirely

- The WhatsApp group export, the participants' course sheet and their numbers.
- The screen recordings (see the note on the clip below).
- The FinStack brief and their pre-read recordings.
- Spreadsheets (all `.xlsx` files are blocked by `.gitignore`).

## The demo clip

The full recording shows a real PAN, part of an Aadhaar number, a name and a mobile number on screen. The clip in `product/demo/` is cut from the part after DigiLocker (it starts at Step 2 and ends at the settlement screen). The audio is removed. The PAN field and the vehicle number field on Step 2 are covered by solid black boxes, and so is every place the customer's name appears. The boxes are placed by finding each field's label on every frame, so they follow the field if the page scrolls. It was checked frame by frame at sample points, and the author watched the final clip before it was added.

## How it was checked

1. `tools/scan_sensitive.py` looks for mobile numbers, PAN patterns, Aadhaar patterns, emails, passwords and keys, login links and a private list of names (the list is kept outside the repo). It was run before every commit.
2. The full git history was searched for names, PAN fragments and numbers: none found.
3. Links between files were checked.

## Known limit

Commit metadata carries the author's email address. While the repo is private that is fine; it needs rewriting before the repo is ever made public.
