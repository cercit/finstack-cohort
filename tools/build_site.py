"""Builds a small static website from this repo's files.
Usage:  python tools/build_site.py          -> writes ./site/
Preview: python -m http.server 8766 --bind 127.0.0.1 --directory site
Plain HTML and one CSS file. No outside scripts, fonts or trackers."""
import html, os, pathlib, re, shutil, subprocess
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
md = MarkdownIt("commonmark").enable("table")

SITE_TITLE = "FinStack cohort: learned, built, tested"
NAV = [("Home", "index.html"), ("Learned", "learned/index.html"), ("Built", "built/index.html"),
       ("Tested", "tested/index.html"), ("Launch", "launch/index.html"), ("About", "about/index.html")]

# repo path -> site path
MAP = {
    "learned-to-used.md": "learned/learned-to-used.html",
    "cohort/day-1.md": "learned/day-1.html", "cohort/day-2.md": "learned/day-2.html", "cohort/days-3-to-5.md": "learned/days-3-to-5.html",
    "cohort/fintech-apis.md": "learned/fintech-apis.html", "cohort/no-code-platform.md": "learned/no-code-platform.html",
    "cohort/consent-and-rules.md": "learned/consent-and-rules.html",
    "product/prd.md": "built/prd.html", "product/sprint-plan.md": "built/sprint-plan.html",
    "product/prd-decisions-log.md": "built/decisions-log.html", "product/formulas/formulas.md": "built/formulas.html",
    "testing/failures-and-fixes.md": "tested/failures-and-fixes.html", "testing/live-demo-lessons.md": "tested/live-demo-lessons.html",
    "launch/production-launch-plan.md": "launch/index.html", "launch/production-launch-plan.pdf": "launch/production-launch-plan.pdf",
    "product/journey/wireframe-as-built.html": "built/journey.html", "product/journey/pitch.html": "built/pitch.html",
    "product/journey/overview.html": "built/overview.html",
    "README.md": "about/index.html", "REDACTION.md": "about/index.html", "LICENSE": "about/index.html",
}

CSS = """
:root{--bg:#fbfcfd;--fg:#1c2733;--mute:#5b6b78;--line:#d3dbe2;--soft:#eef3f6;--brand:#123a52;--link:#0b5cad;--card:#fff;--warn:#fff4e0}
@media (prefers-color-scheme:dark){:root{--bg:#10171d;--fg:#e4eaef;--mute:#9db0be;--line:#2c3a46;--soft:#18232c;--brand:#9ccbe8;--link:#7db8f0;--card:#16212a;--warn:#2a2416}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 system-ui,"Segoe UI",Roboto,sans-serif}
a{color:var(--link)}
header.site{border-bottom:1px solid var(--line);background:var(--card)}
.bar{max-width:980px;margin:0 auto;padding:12px 16px;display:flex;flex-wrap:wrap;gap:8px 22px;align-items:center;justify-content:space-between}
.brand{font-weight:700;color:var(--brand);text-decoration:none;font-size:1.05rem}
nav{display:flex;flex-wrap:wrap;gap:2px 16px}
nav a{text-decoration:none;color:var(--fg);padding:4px 0;border-bottom:2px solid transparent}
nav a:hover,nav a.on{border-bottom-color:var(--brand);color:var(--brand)}
main{max-width:860px;margin:0 auto;padding:24px 16px 56px;overflow-wrap:anywhere}
h1{font-size:2rem;line-height:1.2;color:var(--brand);margin:.2em 0 .4em}
h2{font-size:1.35rem;margin:1.8em 0 .4em;color:var(--brand);border-bottom:1px solid var(--line);padding-bottom:.2em}
h3{font-size:1.1rem;margin:1.4em 0 .3em}
.tw{overflow-x:auto;margin:1em 0}
table{border-collapse:collapse;min-width:520px;width:100%;font-size:.93rem;background:var(--card)}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--soft)}
code{background:var(--soft);padding:1px 5px;border-radius:4px;font-size:.9em}
pre{background:var(--soft);padding:12px;overflow-x:auto;border-radius:6px}
pre code{background:none;padding:0}
blockquote{border-left:4px solid var(--line);margin:1em 0;padding:.1em 1em;color:var(--mute)}
.lead{font-size:1.15rem;color:var(--mute)}
.strip{background:var(--warn);border:1px solid var(--line);border-radius:8px;padding:10px 14px;font-size:.95rem;margin:1.2em 0}
video{width:100%;max-width:860px;border-radius:10px;border:1px solid var(--line);background:#000}
.cap{font-size:.9rem;color:var(--mute);margin:.4em 0 1.4em}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:1em 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card h3{margin:.1em 0 .3em}
.card a.go{display:inline-block;margin-top:.4em;font-weight:600}
.timeline{list-style:none;padding:0;margin:1em 0;border-left:3px solid var(--line)}
.timeline li{padding:0 0 12px 16px;position:relative}
.timeline li:before{content:"";position:absolute;left:-8px;top:8px;width:13px;height:13px;border-radius:50%;background:var(--brand)}
.timeline b{color:var(--brand)}
.chips{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}
.chips li{background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:.92rem}
ul.list{padding-left:1.2em}
ul.list li{margin:.5em 0}
.crumb{font-size:.9rem;color:var(--mute);margin-bottom:.6em}
footer.site{border-top:1px solid var(--line);color:var(--mute);font-size:.9rem}
footer.site .bar{padding:14px 16px}
@media (max-width:600px){h1{font-size:1.6rem}body{font-size:16px}}
"""


def rel(from_page, to_path):
    return os.path.relpath(to_path, os.path.dirname(from_page)).replace("\\", "/")


def page(out_path, title, body, section=None, desc=""):
    nav = "".join(f'<a href="{rel(out_path, p)}"{" class=on" if name == section else ""}>{name}</a>' for name, p in NAV)
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="data:,"><link rel="stylesheet" href="{rel(out_path, 'assets/style.css')}"></head><body>
<header class="site"><div class="bar"><a class="brand" href="{rel(out_path, 'index.html')}">FinStack cohort</a><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer class="site"><div class="bar"><span>Lender terms, rates, limits and car prices on this site are invented or demo values.</span>
<span><a href="{rel(out_path, 'about/index.html')}">About and privacy</a></span></div></footer></body></html>"""
    p = OUT / out_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf8")


def fix_links(body, src_rel, out_path):
    src_dir = (ROOT / src_rel).parent

    def anchor(m):
        href, text = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#)", href):
            return m.group(0)
        path, _, frag = href.partition("#")
        try:
            key = (src_dir / path).resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return text
        if key in MAP:
            return f'<a href="{rel(out_path, MAP[key])}{"#" + frag if frag else ""}">{text}</a>'
        return text                                   # a file that is not on the site: show the words, drop the link
    return re.sub(r'<a href="([^"]+)">(.*?)</a>', anchor, body, flags=re.S)


def render_md(src_rel, out_path, section, strip_h1=False):
    text = (ROOT / src_rel).read_text(encoding="utf8")
    body = md.render(text)
    if strip_h1:
        body = re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S)
    body = fix_links(body, src_rel, out_path)
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    title = re.search(r"<h1>(.*?)</h1>", body, re.S)
    t = re.sub(r"<.*?>", "", title.group(1)) if title else src_rel
    crumb = f'<p class="crumb"><a href="{rel(out_path, section[1])}">{section[0]}</a></p>'
    page(out_path, f"{t}", crumb + body, section[0], t)
    return t


def first_heading(src_rel):
    for line in (ROOT / src_rel).read_text(encoding="utf8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return src_rel


def index_page(out_path, section, title, intro, items, extra=""):
    lis = "".join(f'<li><a href="{rel(out_path, target)}"><b>{html.escape(name)}</b></a> {html.escape(desc)}</li>' for name, target, desc in items)
    page(out_path, title, f"<h1>{html.escape(title)}</h1><p class=lead>{html.escape(intro)}</p><ul class=list>{lis}</ul>{extra}", section, intro)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf8")
    clip = ROOT / "product/demo/dealerfinance-journey-masked.mp4"
    shutil.copy(clip, OUT / "assets/demo.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "93", "-i", str(clip), "-frames:v", "1", "-vf", "scale=1280:-1", "-q:v", "4",
                    str(OUT / "assets/poster.jpg")], check=False)
    for src, dst in (("product/journey/wireframe-as-built.html", "built/journey.html"), ("product/journey/pitch.html", "built/pitch.html"),
                     ("product/journey/overview.html", "built/overview.html"), ("launch/production-launch-plan.pdf", "launch/production-launch-plan.pdf")):
        (OUT / dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / src, OUT / dst)

    S = {n: (n, p) for n, p in NAV}
    # ---- Learned
    learned = [("What I learned, mapped to what I used", "learned-to-used.md", "Each class topic next to where it shows up in the product, and how far it got."),
               ("Day 1", "cohort/day-1.md", "How banks, RBI and NBFCs work, and what a no-code lending platform is."),
               ("Day 2", "cohort/day-2.md", "Underwriting, KYC, credit reports, proof of income, and the platform hands-on."),
               ("Days 3 to 5", "cohort/days-3-to-5.md", "Build, demo and submission."),
               ("The fintech APIs", "cohort/fintech-apis.md", "Credit reports, PAN, Aadhaar, DigiLocker, vehicle lookup, statements: what goes in and out."),
               ("The no-code platform", "cohort/no-code-platform.md", "How it is put together, and nine rules for its logic variables."),
               ("Consent and rules", "cohort/consent-and-rules.md", "Consent, KYC and lender rules, and how they shaped the product.")]
    for name, src, desc in learned:
        render_md(src, MAP[src], S["Learned"])
    index_page("learned/index.html", "Learned", "What I learned", "Five days on how lenders work, and the tools behind modern lending products.",
               [(n, MAP[s], d) for n, s, d in learned])
    # ---- Built
    for src in ("product/prd.md", "product/sprint-plan.md", "product/prd-decisions-log.md", "product/formulas/formulas.md"):
        render_md(src, MAP[src], S["Built"])
    index_page("built/index.html", "Built", "What we built", "DealerFinance: a loan journey for new-car buyers at a dealership, built on a no-code platform.",
               [("Product requirements (PRD)", MAP["product/prd.md"], "Problem, users, scope, rules, risks, in the format taught in class."),
                ("Sprint plan", MAP["product/sprint-plan.md"], "Epics, stories, tasks and gates, written from the work done."),
                ("The six-step journey", "built/journey.html", "Every screen with its fields, rules and test values."),
                ("The pitch page", "built/pitch.html", "The problem, the market, and the flow used in the demo."),
                ("Overview page", "built/overview.html", "A plain explanation of what the product is and how it works."),
                ("Decisions log", MAP["product/prd-decisions-log.md"], "The first design decisions, F1 to F26."),
                ("Formulas", MAP["product/formulas/formulas.md"], "The expressions behind price, loan, fit and commission (test values).")],
               extra='<div class="strip">The demo clip is on the <a href="../index.html">home page</a>.</div>')
    # ---- Tested
    for src in ("testing/failures-and-fixes.md", "testing/live-demo-lessons.md"):
        render_md(src, MAP[src], S["Tested"])
    index_page("tested/index.html", "Tested", "What went wrong, and the fixes", "A live demo with about 15 to 16 people found cases we had not tested.",
               [("Failures and fixes", MAP["testing/failures-and-fixes.md"], "What broke, why, the fix and the lesson, with open items marked."),
                ("Live-demo lessons", MAP["testing/live-demo-lessons.md"], "Customers new to credit, and the vehicle check with no exchange car.")])
    # ---- Launch (the launch plan is the section's index page)
    text = (ROOT / "launch/production-launch-plan.md").read_text(encoding="utf8")
    body = fix_links(md.render(text), "launch/production-launch-plan.md", "launch/index.html")
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    body = body.replace("</h1>", '</h1><p><a href="production-launch-plan.pdf">Download the PDF</a></p>', 1)
    page("launch/index.html", "Production launch plan", body, "Launch", "The production launch plan")
    # ---- About
    readme = md.render((ROOT / "README.md").read_text(encoding="utf8"))
    readme = re.sub(r"<h1>.*?</h1>", "", readme, count=1, flags=re.S)
    readme = re.sub(r"<h2>Where to look</h2>.*?(?=<h2>)", "", readme, flags=re.S)
    redact = md.render((ROOT / "REDACTION.md").read_text(encoding="utf8")).replace("<h1>", "<h2>").replace("</h1>", "</h2>")
    lic = html.escape((ROOT / "LICENSE").read_text(encoding="utf8"))
    about = "<h1>About</h1>" + fix_links(readme, "README.md", "about/index.html") + fix_links(redact, "REDACTION.md", "about/index.html") + f"<h2>Licence</h2><pre>{lic}</pre>"
    about = about.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    page("about/index.html", "About", about, "About", "About this record, privacy and licence")
    # ---- Home
    home = f"""<h1>FinStack cohort: what I learned, built and fixed</h1>
<p class="lead">A five-day fintech product management cohort in Bengaluru (9 to 13 Oct 2026). We learned how lenders and no-code lending platforms work, then built DealerFinance, a loan journey for new-car buyers at a dealership, tested it live with about 15 to 16 people, and fixed what broke.</p>
<div class="strip">Lender names, rates, limits and thresholds here are invented test values, not any lender's real policy.</div>
<video controls preload="metadata" poster="assets/poster.jpg"><source src="assets/demo.mp4" type="video/mp4">Your browser cannot play this video.</video>
<p class="cap">The product walk-through, 2 min 25 s, with a calm background track. The name and one-time codes are shown on purpose. Mobile number, PAN, vehicle number and Aadhaar details are covered.</p>
<h2>The five days</h2>
<ul class="timeline">
<li><b>9 Oct</b> Banks, RBI, NBFCs, and a first look at the platform</li>
<li><b>10 Oct</b> Underwriting, KYC, credit reports, income proof, hands-on build</li>
<li><b>11 Oct</b> Office closed. Wireframe revised</li>
<li><b>12 Oct</b> Help day. The journey takes shape</li>
<li><b>13 Oct</b> Final brief and the live demo</li>
<li><b>14 Oct</b> Written production launch plan</li>
</ul>
<div class="cards">
<div class="card"><h3>Learned</h3><p>Seven notes on how lending works and the tools behind it.</p><a class="go" href="learned/index.html">Read the notes</a></div>
<div class="card"><h3>Built</h3><p>The PRD, sprint plan, the six-step journey and the formulas.</p><a class="go" href="built/index.html">See what we built</a></div>
<div class="card"><h3>Tested and fixed</h3><p>What broke at the live demo, and what we changed.</p><a class="go" href="tested/index.html">See the fixes</a></div>
<div class="card"><h3>Launch plan</h3><p>Where it plugs in, the fields needed, and the phases.</p><a class="go" href="launch/index.html">Read the plan</a></div>
</div>
<h2>Skills this shows</h2>
<ul class="chips"><li>Consent and KYC design</li><li>Credit bureau and soft pull</li><li>No-code journey building</li><li>PRD writing</li><li>Sprint planning</li><li>Edge-case testing</li><li>Production launch planning</li><li>Plain-language documentation</li></ul>
<h2>People</h2>
<p><b>Sameer S Mittimani</b>: product, build, write-ups. <b>Aditya Sharan</b> (<a href="https://github.com/aaDhut">github.com/aaDhut</a>): teammate and colleague on Team 6.</p>"""
    page("index.html", SITE_TITLE, home, "Home", "What I learned, built and fixed in the FinStack fintech PM cohort")
    print("site built:", sum(1 for _ in OUT.rglob("*") if _.is_file()), "files in", OUT)


if __name__ == "__main__":
    main()
