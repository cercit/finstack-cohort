import subprocess, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mask_clip2 as m
from mask_clip2 import read_frames, gray, ncc, grab, W, H, X0, X1, SP, OUT, tm as tm_main

FPS = m.FPS
A_T0, A_T1, A_SPEED = 0, 43, 1.5          # Step 1, loading, Step 7 intro (no DigiLocker screens)
C_T0, C_T1, C_SPEED = 102, 216, 1.2        # Step 2 to settlement
r24 = grab(24)
S1 = {   # Step 1 labels (English only on this screen), from the t=24 frame. Name and OTP stay visible; mobile is masked
    "s1_mobile": (r24, 642, 165, 754, 184),
    "s1_code":   (r24, 337, 301, 492, 320),
}
tm1 = {k: f[y0:y1, x0:x1] for k, (f, x0, y0, x1, y1) in S1.items()}

def detect(frames, tmpl, th=0.70):
    det = {k: [None]*len(frames) for k in tmpl}
    for i, f in enumerate(frames):
        g = gray(f)[:, X0:X1]
        for k, t in tmpl.items():
            r = ncc(g, t); j = np.unravel_index(np.argmax(r), r.shape)
            if r[j] > th: det[k][i] = (j[1]+X0, j[0], t.shape[1], t.shape[0])
    return det

def slate(n):
    img = Image.new("RGB", (W, H), (244, 246, 249))
    d = ImageDraw.Draw(img)
    try:
        f1 = ImageFont.truetype("arial.ttf", 38); f2 = ImageFont.truetype("arial.ttf", 26)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    lines = [("DigiLocker identity check", f1, 270), ("Aadhaar number, OTP and security PIN screens", f2, 335), ("are hidden in this clip to protect personal data", f2, 372)]
    for text, font, y in lines:
        w = d.textlength(text, font=font); d.text(((W-w)/2, y), text, fill=(30, 40, 52), font=font)
    return np.stack([np.array(img)]*n)

def apply(frames, det, spread=4, strip=False):
    out = frames.copy(); n = len(frames)
    def box(i, x0, y0, x1, y1): out[i, max(y0,0):min(y1,H), max(x0,0):min(x1,W)] = 0
    for k in det:
        for i in range(n):
            for d in range(-spread, spread+1):
                ii = i + d
                if not (0 <= ii < n) or det[k][ii] is None: continue
                x, y, w, h = det[k][ii]
                if k in ("lab_pan", "lab_vehicle", "lab_cust", "s1_name", "s1_mobile"):
                    box(i, x-6, y+17, x+296, y+54)
                elif k == "s1_code":
                    box(i, x-6, y+60, x+330, y+86)          # only the "Code sent to <mobile>" line; the code boxes stay visible
                else:
                    box(i, x-10, y-8, x+w+10, y+h+8)
    if strip:
        for i in range(n):
            if not any(0 <= i+d < n and det["subtitle"][i+d] is not None for d in range(-spread, spread+1)):
                box(i, 316, 46, 520, 58)
    return out

if __name__ == "__main__":
    A = read_frames(A_T0, A_T1-A_T0, A_SPEED); print("A", A.shape, flush=True)
    C = read_frames(C_T0, C_T1-C_T0, C_SPEED); print("C", C.shape, flush=True)
    dA = detect(A, tm1); print("A det", {k: sum(x is not None for x in v) for k, v in dA.items()}, flush=True)
    dC = detect(C, {k: tm_main[k] for k in ("lab_pan", "lab_vehicle")}); print("C det", {k: sum(x is not None for x in v) for k, v in dC.items()}, flush=True)
    outA = apply(A, dA, strip=False); outC = apply(C, dC, strip=False)
    seq = [outA, slate(30), outC]
    enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-an","-c:v","libx264","-crf","27","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",OUT], stdin=subprocess.PIPE)
    for part in seq:
        for fr in part: enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    print("written", OUT, os.path.getsize(OUT)//1024, "KB", len(A)+30+len(C), "frames", flush=True)
