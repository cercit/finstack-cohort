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

The full recording shows a real name, mobile number, PAN, a partly typed Aadhaar number, an Aadhaar OTP, the DigiLocker security PIN, a date of birth and a password-manager popup that listed an account number. The clip in `product/demo/` is about 2 minutes 25 seconds long, has no audio and no zoom effects, and was made like this:

- **Shown on purpose:** the author's own name (in the form fields and under each step title) and the OTP boxes and digits (the Step 1 code and the Aadhaar OTP). The author chose to show these.
- **Hidden behind a frosted, see-through cover (heavy blur plus a light veil, strong enough that the text cannot be read):** the mobile number field on Step 1, the Aadhaar number boxes on DigiLocker, the partly shown registered mobile on the DigiLocker OTP page, the password-manager popup, the PAN field and the vehicle number field on Step 2. The covers are placed by finding each field's label on every frame, so they follow the field when the page moves.
- **Wiped out:** the "Code sent to <mobile>" line under the Step 1 code boxes is painted over with the card's own background.
- **Cut:** the DigiLocker result page with the date of birth and PAN, and the first seconds of the recording (the mobile number was typed into the name box by mistake before being deleted).
- **Edited for length:** waiting and loading screens are fast-forwarded.
- **Rejected-lender route:** the recording's own rejected test ended in an error pop-up. In the clip that moment is replaced by a short diagram of the designed route (rejected, back to Step 4, choose another financier, send again, approved), labelled as a diagram. The error itself is written up in `testing/failures-and-fixes.md`.

A script scanned the finished clip for leftover mobile digits, "code sent to" text, PAN text, vehicle number text, a half-typed vehicle number, digits in the name box, Aadhaar digits, the registered mobile and the popup's account number, on every second frame, and found none (the highest score was below the match limit). The same kind of scan finds each of them in the unmasked source, so the check works. Frames spread across the clip were also checked by eye, and the author watched the final clip before it was added. Income, EMI, loan figures and the credit score on screen are test values and are left visible.

## How it was checked

1. `tools/scan_sensitive.py` looks for mobile numbers, PAN patterns, Aadhaar patterns, emails, passwords and keys, login links and a private list of names (the list is kept outside the repo). It was run before every commit.
2. The full git history was searched for names, PAN fragments and numbers: none found.
3. Links between files were checked.

## Known limit

Commit metadata carries the author's email address. While the repo is private that is fine; it needs rewriting before the repo is ever made public.
