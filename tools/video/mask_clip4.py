import subprocess, os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import uniform_filter
import mask_clip2 as m
from mask_clip2 import read_frames, gray, ncc, grab, W, H, X0, X1, SP, V, tm as tm_main
from mask_clip3 import tm1, detect

FPS = m.FPS
TEST = os.environ.get("CLIP_TEST") == "1"
A_T0, A_T1, A_SPEED = (4.6, 8, 1.5) if TEST else (4.6, 43, 1.5)   # start after the first typing attempt (mobile digits typed in the name box by mistake)
C_T0, C_T1, C_SPEED = (102, 106, 1.2) if TEST else (102, 216, 1.2)
OUT = os.path.join(SP, "test_clip.mp4") if TEST else m.OUT
FW, FH = 2558, 1318                       # full-resolution source frame
OW, OH = 1920, 990                        # output frame
SCALE = FW / W                            # full-res / half-res = ~2
ZOOM = 1.65

# ---------- pass 1 helpers: where is the activity (typing, field changes)? ----------
def zoom_path(frames):
    n = len(frames); g_prev = None
    active = [False]*n; centre = [None]*n
    for i, f in enumerate(frames):
        g = gray(f)[::2, ::2]
        if g_prev is not None:
            d = np.abs(g - g_prev) > 30
            d[:25, :] = False; d[300:, :] = False if False else d[300:, :]
            cnt = int(d.sum())
            if 25 <= cnt <= 2500:
                ys, xs = np.nonzero(d)
                bw, bh = xs.max()-xs.min(), ys.max()-ys.min()
                if bw <= 260 and bh <= 80:
                    active[i] = True; centre[i] = ((xs.min()+xs.max())/2*2, (ys.min()+ys.max())/2*2)
        g_prev = g
    # require activity in 3 of the last 6 frames near the same place, then hold for 8 frames
    want = [False]*n; target = [None]*n; hold = 0; last = None
    for i in range(n):
        recent = [centre[j] for j in range(max(0, i-5), i+1) if active[j]]
        if len(recent) >= 3:
            cx = float(np.median([c[0] for c in recent])); cy = float(np.median([c[1] for c in recent]))
            if all(abs(c[0]-cx) < 160 and abs(c[1]-cy) < 90 for c in recent):
                hold = 8; last = (cx, cy)
        if hold > 0:
            want[i] = True; target[i] = last; hold -= 1
    s, cx_, cy_ = 1.0, W/2, H/2; path = []
    for i in range(n):
        ts = ZOOM if want[i] else 1.0
        tc = target[i] if want[i] else (W/2, H/2)
        s += (ts - s) * 0.14; cx_ += (tc[0] - cx_) * 0.18; cy_ += (tc[1] - cy_) * 0.18
        path.append((s, cx_, cy_))
    return path, sum(want)

# ---------- frosted translucent cover ----------
VEIL = np.array([236, 239, 244], np.float32)
def frost(img, x0, y0, x1, y1):
    x0, y0 = max(int(x0), 0), max(int(y0), 0); x1, y1 = min(int(x1), FW), min(int(y1), FH)
    if x1 <= x0 or y1 <= y0: return
    reg = Image.fromarray(img[y0:y1, x0:x1])
    small = reg.resize((max((x1-x0)//34, 1), max((y1-y0)//34, 1)), Image.BOX)
    blur = np.asarray(small.resize((x1-x0, y1-y0), Image.BILINEAR), np.float32)
    img[y0:y1, x0:x1] = (0.40*blur + 0.60*VEIL).astype(np.uint8)

def boxes_for(det, i, n, spread=4):
    out = []
    for k in det:
        for d in range(-spread, spread+1):
            ii = i + d
            if 0 <= ii < n and det[k][ii] is not None:
                x, y, w, h = det[k][ii]
                if k in ("lab_pan", "lab_vehicle", "s1_mobile"): out.append((x-6, y+17, x+296, y+54))
                elif k == "s1_code": out.append((x-6, y+60, x+330, y+86))
    return out

def crop_zoom(img, s, cx, cy):
    if s < 1.01:
        return np.asarray(Image.fromarray(img).resize((OW, OH), Image.LANCZOS))
    cw, ch = FW/s, FH/s
    x0 = min(max(cx*SCALE - cw/2, 0), FW-cw); y0 = min(max(cy*SCALE - ch/2, 0), FH-ch)
    return np.asarray(Image.fromarray(img).resize((OW, OH), Image.LANCZOS, box=(x0, y0, x0+cw, y0+ch)))

def slate_frame():
    img = Image.new("RGB", (OW, OH), (244, 246, 249)); d = ImageDraw.Draw(img)
    try: f1 = ImageFont.truetype("arial.ttf", 56); f2 = ImageFont.truetype("arial.ttf", 38)
    except OSError: f1 = f2 = ImageFont.load_default()
    for text, font, y in [("DigiLocker identity check", f1, 380), ("Aadhaar number, OTP and security PIN screens", f2, 470), ("are hidden in this clip to protect personal data", f2, 525)]:
        w = d.textlength(text, font=font); d.text(((OW-w)/2, y), text, fill=(30, 40, 52), font=font)
    return np.asarray(img)

def read_full(ss, dur, speed):
    cmd = ["ffmpeg","-v","error","-ss",str(ss),"-t",str(dur),"-i",V,"-vf",f"setpts=PTS/{speed},fps={FPS}","-f","rawvideo","-pix_fmt","rgb24","-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FW*FH*3*2)
    sz = FW*FH*3
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz: break
        yield np.frombuffer(b, np.uint8).reshape(FH, FW, 3).copy()
    p.wait()

LEAK = {}
def leak_templates():
    r24, r130, r142, r3 = grab(24), grab(130), grab(142), grab(3.0)
    C = {"s1_mobile_text": (r24, 650, 191, 748, 212), "s1_codesent": (r24, 345, 362, 520, 383),
         "pan_value": (r130, 346, 211, 446, 231), "vehicle_value": (r142, 345, 476, 435, 497), "vehicle_typing": (r130, 346, 537, 392, 556), "digits_in_name_box": (r3, 346, 192, 412, 212)}
    return {k: f[y0:y1, x0:x1] for k, (f, x0, y0, x1, y1) in C.items()}

if __name__ == "__main__":
    segs = []
    for name, (t0, t1, sp), tmpl in (("A", (A_T0, A_T1, A_SPEED), tm1), ("C", (C_T0, C_T1, C_SPEED), {k: tm_main[k] for k in ("lab_pan", "lab_vehicle")})):
        fr = read_frames(t0, t1-t0, sp); det = detect(fr, tmpl); path, nz = zoom_path(fr)
        print(name, fr.shape, "det", {k: sum(x is not None for x in v) for k, v in det.items()}, "zoomed frames", nz, flush=True)
        segs.append((name, (t0, t1, sp), len(fr), det, path)); del fr
    leak_t = leak_templates(); worst = {k: 0.0 for k in leak_t}; where = {}
    enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{OW}x{OH}","-r",str(FPS),"-i","-",
        "-an","-c:v","libx264","-crf","26","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",OUT], stdin=subprocess.PIPE)
    total = 0
    for name, (t0, t1, sp), n, det, path in segs:
        count = 0
        for i, img in enumerate(read_full(t0, t1-t0, sp)):
            if i >= n: break
            for (bx0, by0, bx1, by1) in boxes_for(det, i, n):
                frost(img, bx0*SCALE, by0*SCALE, bx1*SCALE, by1*SCALE)
            if i % 2 == 0:          # leak check on the masked, unzoomed frame, scaled back to the analysis size
                g_full = gray(np.asarray(Image.fromarray(img).resize((W, H), Image.LANCZOS)))[:, X0:X1]
                g_ex = g_full.copy()
                if name == "A": g_ex[186:217, 335-X0:640-X0] = g_full.mean()   # the name field is shown on purpose
                for k, t in leak_t.items():
                    g = g_full if k == "digits_in_name_box" else g_ex
                    r = ncc(g, t); j = np.unravel_index(np.argmax(r), r.shape); sc = float(r[j])
                    if sc > worst[k]:
                        worst[k] = sc; where[k] = (name, i, j[1]+X0, j[0], t.shape[1], t.shape[0])
            s, cx, cy = path[i]
            enc.stdin.write(crop_zoom(img, s, cx, cy).tobytes()); count += 1; total += 1
        print(name, "frames written", count, "of", n, flush=True)
        if name == "A":
            sl = slate_frame().tobytes()
            for _ in range(30): enc.stdin.write(sl); total += 1
    enc.stdin.close(); enc.wait()
    print("WORST LOCATIONS (segment, frame, x, y)", {k: v[:4] for k, v in where.items()}, flush=True)
    print("LEAK CHECK (every 2nd frame, masked unzoomed): max score per template", {k: round(v, 2) for k, v in worst.items()}, "limit 0.6", flush=True)
    print("written", OUT, os.path.getsize(OUT)//1024, "KB", total, "frames", flush=True)
