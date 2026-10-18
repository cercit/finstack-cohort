import subprocess, os, numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import uniform_filter
from PIL import Image

V = r"C:\Users\samsm\Videos\Screen Recordings\Screen Recording 2026-10-13 184533.mp4"
OUT = r"C:\Users\samsm\finstack-cohort\product\demo\dealerfinance-journey-masked.mp4"
SP = r"C:\Users\samsm\AppData\Local\Temp\claude\C--Users-samsm-OneDrive-Desktop-Claude\4ce94a1c-b9a0-4e67-83a4-8f71ca75bb74\scratchpad\vid"
T0, T1, SPEED, FPS, W, H = 102, 216, 1.2, 10, 1278, 658
X0, X1 = 300, 990          # search band (the page content sits here)

def read_frames(ss, dur, speed=1.0, fps=FPS):
    vf = f"setpts=PTS/{speed},fps={fps},scale={W}:{H}"
    cmd = ["ffmpeg","-v","error","-ss",str(ss),"-t",str(dur),"-i",V,"-vf",vf,"-f","rawvideo","-pix_fmt","rgb24","-"]
    raw = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
    n = len(raw)//(W*H*3)
    return np.frombuffer(raw, np.uint8)[:n*W*H*3].reshape(n,H,W,3)

def gray(f): return (0.299*f[...,0]+0.587*f[...,1]+0.114*f[...,2]).astype(np.float32)

def ncc(g, t):
    g = g.astype(np.float64); t = t.astype(np.float64)
    th, tw = t.shape
    t0 = t - t.mean(); tn = np.sqrt((t0**2).sum()) + 1e-9
    num = fftconvolve(g, t0[::-1, ::-1], mode="valid")
    sl = (slice(th//2, th//2+num.shape[0]), slice(tw//2, tw//2+num.shape[1]))
    m = uniform_filter(g, (th, tw), mode="constant")[sl]
    m2 = uniform_filter(g*g, (th, tw), mode="constant")[sl]
    var = np.maximum(m2 - m*m, 0.0) * th * tw          # sum of squared deviations in each window
    ok = var > (6.0**2) * th * tw                        # ignore flat windows (std below 6)
    r = np.zeros_like(num)
    r[ok] = num[ok] / (np.sqrt(var[ok]) * tn)
    return np.clip(r, -1, 1)

def grab(t):
    return gray(read_frames(t, 0.2, 1.0, 5)[0])

# reference frames: 130 s = Step 2 filled in, 142 s = Step 2 (scrolled), 170 s = Step 5
r130, r142, r170 = grab(130), grab(142), grab(170)
CROPS = {   # name: (frame, x0, y0, x1, y1)  in the W x H frame
    "lab_pan":     (r130, 335, 185, 525, 204),
    "lab_vehicle": (r130, 335, 510, 553, 530),
    "lab_cust":    (r170, 337, 185, 555, 204),
    "subtitle":    (r170, 322, 98, 492, 116),
    "namefield":   (r170, 348, 210, 492, 232),
}
tm = {k: f[y0:y1, x0:x1] for k, (f, x0, y0, x1, y1) in CROPS.items()}
for k, (f, x0, y0, x1, y1) in CROPS.items():
    Image.fromarray(np.clip(f[y0-5:y1+5, x0-5:x1+5],0,255).astype(np.uint8)).resize(((x1-x0+10)*3,(y1-y0+10)*3)).save(os.path.join(SP, "tmpl_"+k+".png"))
# value templates, used only to double-check the output (PAN text, vehicle number text)
CHECK = {
    "pan_value":   (r142, 700//2+0, 0, 0, 0),
}

def detect(frames, names, th):
    out = {k: [None]*len(frames) for k in names}; best = {k: [] for k in names}
    for i, f in enumerate(frames):
        g = gray(f)[:, X0:X1]
        for k in names:
            r = ncc(g, tm[k]); j = np.unravel_index(np.argmax(r), r.shape); s = float(r[j])
            best[k].append(s)
            if s > th: out[k][i] = (j[1]+X0, j[0], tm[k].shape[1], tm[k].shape[0])
    return out, best

if __name__ == "__main__":
    frames = read_frames(T0, T1-T0, SPEED)
    print("frames", frames.shape, flush=True)
    names = list(tm)
    det, best = detect(frames, names, 0.70)
    print({k: (sum(d is not None for d in det[k]), round(float(np.median(best[k])),2), round(float(max(best[k])),2)) for k in names}, flush=True)
    np.save(os.path.join(SP, "det_summary.npy"), np.array([[x is not None for x in det[k]] for k in names]))
    SPREAD = 4
    masked = frames.copy()
    def box(i, x0, y0, x1, y1):
        masked[i, max(y0,0):min(y1,H), max(x0,0):min(x1,W)] = 0
    for k in names:
        for i in range(len(frames)):
            for d in range(-SPREAD, SPREAD+1):
                ii = i + d
                if not (0 <= ii < len(frames)) or det[k][ii] is None: continue
                x, y, w, h = det[k][ii]
                if k in ("lab_pan", "lab_vehicle", "lab_cust"):
                    box(i, x-6, y+17, x+296, y+54)       # the input field under the label
                else:
                    box(i, x-10, y-8, x+w+10, y+h+8)      # name text
    for i in range(len(frames)):
        if not any(0 <= i+d < len(frames) and det['subtitle'][i+d] is not None for d in range(-SPREAD, SPREAD+1)):
            box(i, 316, 46, 520, 58)
    enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-an","-c:v","libx264","-crf","27","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",OUT], stdin=subprocess.PIPE)
    for fr in masked:
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    np.save(os.path.join(SP, "det_summary.npy"), np.array([[x is not None for x in det[k]] for k in names]))
    print("written", OUT, os.path.getsize(OUT)//1024, "KB", flush=True)
