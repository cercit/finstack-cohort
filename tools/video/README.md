# Making the masked demo clip

These scripts turned a 3 min 40 s screen recording that showed personal data into the clip in `product/demo/`. They are kept so the clip can be remade. Paths at the top of each file (the source video, a scratch folder, the output) are for the author's computer: change them first.

## Files

| File | What it does |
|---|---|
| `mask_clip2.py` | Shared helpers: reads frames from the video with ffmpeg, finds a small text image on each frame (normalised cross-correlation using numpy and scipy), and holds the label images for the PAN and vehicle-number fields |
| `mask_clip3.py` | Adds the Step 1 label images (mobile field, code boxes) |
| `mask_clip4.py` | The frosted cover (heavy blur plus a light veil), the zoom crop and the output size |
| `mask_clip5.py` | The final renderer: the list of video pieces, which covers apply to which piece, fast-forwarded waiting screens, the reroute diagram card, the leak check, and the encoder. Zoom is switched off in the pieces list |

Run (after editing the paths): `python mask_clip5.py`. It takes about 15 to 25 minutes. Set `CLIP_TEST=1` for a short test render. Needs ffmpeg, numpy, scipy and Pillow.

## How it works

1. Cut the useful parts of the recording into pieces, and fast-forward the waiting screens.
2. On every frame, find each field's **label** (a stable piece of text such as "PAN Number"), and cover the field below it. Placing covers by label, not by fixed position, keeps them on the field when the page scrolls or the layout shifts.
3. Cover with a frosted block, not black and not a light blur. A heavy blur plus a veil cannot be read back.
4. Replace whole screens that are too risky to cover piecemeal (a title card or diagram instead).
5. **Leak check:** for every second frame of the finished picture, search for images of the real sensitive text (the mobile number, PAN, vehicle number, Aadhaar digits, the popup's account number). Each must score below the match limit. The same search finds all of them in the unmasked source, which proves the check can see them.
6. Look at sample frames by eye, and have the owner watch the clip before it is committed.

## Lessons

- **Cover by label, not by position.** The first version used fixed boxes and missed a name that had scrolled half out of view.
- **Check the content, not just the covers.** Showing the name field was safe only after trimming the first seconds, where mobile digits had been typed into the name box by mistake.
- **Solid black is the safest, but a frosted cover reads better.** Use a strong blur, and let the leak check confirm it.
- **Replace screens with credentials.** The DigiLocker screens held an Aadhaar number, an OTP, a security PIN and a password-manager popup listing an account number. Cover every part, or replace the screen.
- **Write the check before trusting the result.** A scan with a control (it must find the text in the original) beats looking at a few frames.
- **Match scores can mislead.** Different text in the same font can score about 0.5 to 0.7, so leave out areas that are shown on purpose (the name field) when checking for other text.
- **Zoom can look shaky.** If you add zoom, pick a few calm moments, hold the centre fixed, and ease in and out over about a second. Zoom was dropped here.
- **Write big files with the file tool.** Long scripts pasted through a shell here-document failed on quote characters.
