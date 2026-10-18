import subprocess, os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mask_clip2 as m
from mask_clip2 import read_frames, gray, ncc, grab, W, H, X0, X1, SP, V, tm as tm_main
from mask_clip3 import tm1
import mask_clip4 as m4
from mask_clip4 import frost, crop_zoom, FW, FH, OW, OH, SCALE, FPS

TEST = os.environ.get("CLIP_TEST") == "1"
OUT = os.path.join(SP, "test_clip5.mp4") if TEST else m.OUT
ZOOM = 1.45
BLOCK = 12                                   # frames of ease in and out (1.2 s)


def crop(f, x0, y0, x1, y1):
    return f[y0:y1, x0:x1]


r50, r55, r62, r76, r24, r130, r142, r3 = (grab(t) for t in (50, 55, 62, 76.5, 24, 130, 142, 3.0))
TM = {
    "s1_mobile": tm1["s1_mobile"], "s1_code": tm1["s1_code"],
    "lab_pan": tm_main["lab_pan"], "lab_vehicle": tm_main["lab_vehicle"],
    "dg_aadhaar": crop(r50, 476, 183, 684, 203), "dg_mobile": crop(r62, 498, 193, 714, 213), "dg_popup": crop(r76, 505, 458, 634, 478),
}
LEAK = {
    "s1_mobile_text": crop(r24, 650, 191, 748, 212), "s1_codesent": crop(r24, 345, 362, 520, 383),
    "pan_value": crop(r130, 346, 211, 446, 231), "vehicle_value": crop(r142, 345, 476, 435, 497),
    "vehicle_typing": crop(r130, 346, 537, 392, 556), "digits_in_name_box": crop(r3, 346, 192, 412, 212),
    "aadhaar_digits": crop(r55, 495, 238, 640, 258), "dg_mobile_tail": crop(r62, 620, 193, 716, 213), "popup_account": crop(r76, 505, 342, 600, 362),
}
# (name, source start, source end, speed, templates, zoom allowed)
PIECES = [
    ("step1",       4.6, 29.0, 1.5, ("s1_mobile", "s1_code"), False),
    ("step1_wait", 29.0, 38.4, 4.0, (), False),
    ("step7_intro", 38.4, 44.0, 1.5, (), False),
    ("dg_load",    44.0, 46.3, 1.0, ("dg_aadhaar",), False),
    ("dg_pages",   46.3, 81.5, 1.5, ("dg_aadhaar", "dg_mobile", "dg_popup"), False),
    ("dg_wait",    84.0, 95.0, 4.0, (), False),
    ("step2_to_5", 102.0, 177.0, 1.2, ("lab_pan", "lab_vehicle"), False),
    ("SLATE_REROUTE", None, None, None, (), False),
    ("step5_to_6", 187.0, 216.0, 1.2, ("lab_pan", "lab_vehicle"), False),
]
if TEST:
    PIECES = [("step1", 4.6, 8.0, 1.5, ("s1_mobile", "s1_code"), True),
              ("dg_pages", 70.0, 78.0, 1.5, ("dg_aadhaar", "dg_mobile", "dg_popup"), True)]


def detect(frames, names):
    det = {k: [None] * len(frames) for k in names}
    for i, f in enumerate(frames):
        g = gray(f)[:, X0:X1]
        for k in names:
            t = TM[k]
            r = ncc(g, t)
            j = np.unravel_index(np.argmax(r), r.shape)
            if r[j] > (0.60 if k.startswith("dg_") else 0.70):
                det[k][i] = (j[1] + X0, j[0], t.shape[1], t.shape[0])
    return det


def activity(frames):
    n = len(frames)
    act = [False] * n
    cen = [None] * n
    gp = None
    for i, f in enumerate(frames):
        g = gray(f)[::2, ::2]
        if gp is not None:
            d = np.abs(g - gp) > 30
            d[:25, :] = False
            cnt = int(d.sum())
            if 25 <= cnt <= 2500:
                ys, xs = np.nonzero(d)
                if xs.max() - xs.min() <= 260 and ys.max() - ys.min() <= 80:
                    act[i] = True
                    cen[i] = ((xs.min() + xs.max()) / 2 * 2, (ys.min() + ys.max()) / 2 * 2)
        gp = g
    return act, cen


def smooth(t):
    return t * t * (3 - 2 * t)


def zoom_runs(frames):
    n = len(frames)
    act, cen = activity(frames)
    on = [sum(act[j] for j in range(max(0, i - 5), i + 1)) >= 3 for i in range(n)]
    runs, cur = [], []
    for i in [i for i in range(n) if on[i]]:          # merge gaps up to 2.5 s, split when the place changes a lot
        c = cen[i]
        if cur and i - cur[-1] > 25:
            runs.append(cur)
            cur = []
        if cur and c is not None:
            pts = [cen[j] for j in cur if cen[j]]
            if pts:
                mx = np.median([p[0] for p in pts])
                my = np.median([p[1] for p in pts])
                if abs(c[0] - mx) > 150 or abs(c[1] - my) > 90:
                    runs.append(cur)
                    cur = []
        cur.append(i)
    if cur:
        runs.append(cur)
    out = []
    for r in runs:
        if r[-1] - r[0] < 10:
            continue
        cs = [cen[j] for j in r if cen[j]]
        if cs:
            out.append((r[0], r[-1], float(np.median([c[0] for c in cs])), float(np.median([c[1] for c in cs]))))
    path = []
    for i in range(n):
        es = []
        for (a, b, cx, cy) in out:
            if i < a - BLOCK or i > b + 6 + BLOCK:
                e = 0.0
            elif i < a:
                e = smooth((i - (a - BLOCK)) / BLOCK)
            elif i <= b + 6:
                e = 1.0
            else:
                e = smooth(1 - (i - (b + 6)) / BLOCK)
            es.append((e, cx, cy))
        tot = sum(e for e, _, _ in es)
        if tot <= 0:
            path.append((1.0, W / 2, H / 2))
            continue
        emax = max(e for e, _, _ in es)
        cx = sum(e * c for e, c, _ in es) / tot
        cy = sum(e * c for e, _, c in es) / tot
        path.append((1 + (ZOOM - 1) * emax, cx, cy))
    return path, len(out)


def boxes_for(det, i, n):
    out = []
    for k in det:
        spread = 2 if k == "s1_code" else 4
        for d in range(-spread, spread + 1):
            ii = i + d
            if 0 <= ii < n and det[k][ii] is not None:
                x, y, w, h = det[k][ii]
                if k in ("lab_pan", "lab_vehicle", "s1_mobile"):
                    out.append(("frost", x - 6, y + 17, x + 296, y + 54))
                elif k == "s1_code":
                    out.append(("white", x - 6, y + 60, x + 330, y + 86))
                elif k == "dg_aadhaar":
                    out.append(("frost", x - 6, y + 28, x + 340, y + 92))
                elif k == "dg_mobile":
                    out.append(("frost", x + w - 100, y - 4, x + w + 8, y + h + 4))
                elif k == "dg_popup":
                    out.append(("frost", x - 50, y - 150, x + w + 60, y + h + 26))
    return out


def apply_box(img, kind, x0, y0, x1, y1):
    if kind == "frost":
        frost(img, x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE)
    else:
        a, b = max(int(x0 * SCALE), 0), max(int(y0 * SCALE), 0)
        c, d = min(int(x1 * SCALE), FW), min(int(y1 * SCALE), FH)
        img[b:d, a:c] = 255


def fonts():
    try:
        return ImageFont.truetype("arial.ttf", 54), ImageFont.truetype("arial.ttf", 34), ImageFont.truetype("arial.ttf", 28)
    except OSError:
        f = ImageFont.load_default()
        return f, f, f


def reroute_slate():
    img = Image.new("RGB", (OW, OH), (244, 246, 249))
    d = ImageDraw.Draw(img)
    f1, f2, f3 = fonts()
    title = "If a lender rejects the case"
    d.text(((OW - d.textlength(title, font=f1)) / 2, 120), title, fill=(30, 40, 52), font=f1)
    boxes = [("Step 5: Routing-2", "status = rejected"), ("Back to Step 4", "choose a different financier"),
             ("Send again", "Routing-2 for the new lender"), ("Approved", "continue to Step 6")]
    bw, bh, gap = 370, 170, 90
    x = (OW - (4 * bw + 3 * gap)) // 2
    y = 330
    for i, (a, b) in enumerate(boxes):
        col = (255, 235, 232) if i == 0 else ((228, 241, 232) if i == 3 else (255, 255, 255))
        d.rounded_rectangle((x, y, x + bw, y + bh), 18, fill=col, outline=(30, 40, 52), width=3)
        d.text((x + (bw - d.textlength(a, font=f2)) / 2, y + 40), a, fill=(30, 40, 52), font=f2)
        d.text((x + (bw - d.textlength(b, font=f3)) / 2, y + 100), b, fill=(70, 82, 94), font=f3)
        if i < 3:
            ax, ay = x + bw + 12, y + bh // 2
            d.line((ax, ay, ax + gap - 34, ay), fill=(30, 40, 52), width=5)
            d.polygon([(ax + gap - 34, ay - 14), (ax + gap - 34, ay + 14), (ax + gap - 8, ay)], fill=(30, 40, 52))
        x += bw + gap
    note = ["This is the designed route, shown as a diagram.",
            "In the recording, the first test of \"rejected\" ended in an error",
            "(missing approved amount). The fix is listed in testing/failures-and-fixes.md."]
    for k, t in enumerate(note):
        d.text(((OW - d.textlength(t, font=f3)) / 2, 600 + k * 44), t, fill=(70, 82, 94), font=f3)
    return np.asarray(img)


def read_full(ss, dur, speed):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", V, "-vf", f"setpts=PTS/{speed},fps={FPS}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FW * FH * 3 * 2)
    sz = FW * FH * 3
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz:
            break
        yield np.frombuffer(b, np.uint8).reshape(FH, FW, 3).copy()
    p.wait()


if __name__ == "__main__":
    plan = []
    for (name, t0, t1, sp, tpl, zoom) in PIECES:
        if name.startswith("SLATE"):
            plan.append((name, None, 0, {}, []))
            continue
        fr = read_frames(t0, t1 - t0, sp)
        det = detect(fr, tpl) if tpl else {}
        path, nr = zoom_runs(fr) if zoom else ([(1.0, W / 2, H / 2)] * len(fr), 0)
        print(name, len(fr), "frames; det", {k: sum(x is not None for x in v) for k, v in det.items()}, "; zoom runs", nr, flush=True)
        plan.append((name, (t0, t1, sp), len(fr), det, path))
        del fr
    worst = {k: 0.0 for k in LEAK}
    where = {}
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                            "-an", "-c:v", "libx264", "-crf", "27", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT],
                           stdin=subprocess.PIPE)
    total = 0
    for name, src, n, det, path in plan:
        if src is None:
            sl = reroute_slate().tobytes()
            for _ in range(70):
                enc.stdin.write(sl)
                total += 1
            continue
        t0, t1, sp = src
        for i, img in enumerate(read_full(t0, t1 - t0, sp)):
            if i >= n:
                break
            for (kind, a, b, c, d) in boxes_for(det, i, n):
                apply_box(img, kind, a, b, c, d)
            if i % 2 == 0 and name not in ("step1_wait", "dg_wait"):
                g_full = gray(np.asarray(Image.fromarray(img).resize((W, H), Image.LANCZOS)))[:, X0:X1]
                g_ex = g_full.copy()
                if name == "step1":
                    g_ex[186:217, 335 - X0:640 - X0] = g_full.mean()
                for k, t in LEAK.items():
                    g = g_full if k == "digits_in_name_box" else g_ex
                    sc = float(ncc(g, t).max())
                    if sc > worst[k]:
                        worst[k] = sc
                        where[k] = (name, i)
            s, cx, cy = path[i]
            enc.stdin.write(crop_zoom(img, s, cx, cy).tobytes())
            total += 1
        print(name, "written", flush=True)
    enc.stdin.close()
    enc.wait()
    print("LEAK CHECK max score per template (limit 0.6):", {k: round(v, 2) for k, v in worst.items()}, flush=True)
    print("WORST AT", {k: v for k, v in where.items() if worst[k] > 0.55}, flush=True)
    print("written", OUT, os.path.getsize(OUT) // 1024, "KB", total, "frames =", round(total / FPS, 1), "s", flush=True)
