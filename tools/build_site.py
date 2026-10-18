"""Builds a small static website from this repo's files, in the same design as the author's own site
(https://cercit.github.io/me/projects/cercit.html).
Usage:  python tools/build_site.py          -> writes ./site/
Preview: python -m http.server 8766 --bind 127.0.0.1 --directory site
The design files are in tools/site_assets/. No trackers; the only script is the theme and menu script from that design."""
import html, os, pathlib, re, shutil, subprocess
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
ASSETS = ROOT / "tools" / "site_assets"
md = MarkdownIt("commonmark").enable("table")
ME = "https://cercit.github.io/me"

NAV = [("Selection", "selection/index.html"), ("Learned", "learned/index.html"), ("Built", "built/index.html"), ("Tested", "tested/index.html"),
       ("Launch", "launch/index.html"), ("About", "about/index.html")]

MAP = {   # repo path -> site path
    "learned-to-used.md": "learned/learned-to-used.html",
    "cohort/day-1.md": "learned/day-1.html", "cohort/day-2.md": "learned/day-2.html", "cohort/days-3-to-5.md": "learned/days-3-to-5.html",
    "cohort/fintech-apis.md": "learned/fintech-apis.html", "cohort/no-code-platform.md": "learned/no-code-platform.html",
    "cohort/consent-and-rules.md": "learned/consent-and-rules.html",
    "product/prd.md": "built/prd.html", "product/sprint-plan.md": "built/sprint-plan.html",
    "product/prd-decisions-log.md": "built/decisions-log.html", "product/idea-and-market.md": "built/idea-and-market.html",
    "testing/failures-and-fixes.md": "tested/failures-and-fixes.html", "testing/live-demo-lessons.md": "tested/live-demo-lessons.html",
    "launch/production-launch-plan.md": "launch/index.html", "launch/production-launch-plan.pdf": "launch/production-launch-plan.pdf",
    "product/journey/wireframe-as-built.html": "built/wireframe.html",
    "selection/bhim-vs-phonepe-teardown.md": "selection/index.html", "selection/bhim-vs-phonepe-teardown.pdf": "selection/bhim-vs-phonepe-teardown.pdf",
    "README.md": "about/index.html", "REDACTION.md": "about/index.html", "LICENSE": "about/index.html",
}

LEARNED = [("What I learned, mapped to what I used", "learned-to-used.md", "Each class topic next to where it shows up in the product, and how far it got."),
           ("Day 1: banks, RBI and the platform", "cohort/day-1.md", "How banks, RBI and NBFCs work, and what a no-code lending platform is."),
           ("Day 2: underwriting, KYC and credit reports", "cohort/day-2.md", "Underwriting, KYC, credit reports, proof of income, and the platform hands-on."),
           ("Days 3 to 5: build, demo, submit", "cohort/days-3-to-5.md", "The help day, the final brief, the live demo and the written plan."),
           ("The fintech APIs", "cohort/fintech-apis.md", "Credit reports, PAN, Aadhaar, DigiLocker, vehicle lookup and statements: what goes in and out."),
           ("The no-code platform", "cohort/no-code-platform.md", "How it is put together, and nine rules for its logic variables."),
           ("Consent and rules", "cohort/consent-and-rules.md", "Consent, KYC and lender rules, and how they shaped the product.")]
BUILT = [("DealerFinance: product requirements document", "product/prd.md", "Problem, users, scope, rules and risks, in the format taught in class."),
         ("Sprint plan", "product/sprint-plan.md", "Epics, stories, tasks and gates."),
         ("Wireframe", "product/journey/wireframe-as-built.html", "Every screen with its fields, rules and test values."),
         ("The idea, the market and the flow", "product/idea-and-market.md", "The problem, why it is unsolved, the market size and how the flow works."),
         ("Decisions log", "product/prd-decisions-log.md", "The design decisions, and how the logic was built without a database.")]
TESTED = [("Failures and fixes", "testing/failures-and-fixes.md", "What broke, why, the fix and the lesson, with open items marked."),
          ("Live-demo lessons", "testing/live-demo-lessons.md", "Customers new to credit, and the vehicle check with no exchange car.")]
SECTIONS = {"Selection": ("selection/index.html", "selection / project"), "Learned": ("learned/index.html", "cohort / notes"), "Built": ("built/index.html", "product / documents"),
            "Tested": ("tested/index.html", "testing / lessons"), "Launch": ("launch/index.html", "launch / plan"),
            "About": ("about/index.html", "about / privacy")}


def rel(from_page, to_path):
    return os.path.relpath(to_path, os.path.dirname(from_page) or ".").replace("\\", "/")


def esc(s):
    return html.escape(s, quote=True)


ARROW = '<span aria-hidden="true">↗</span>'
THEME_BTN = ('<button class="icon-button theme-button" data-theme-toggle aria-label="Switch theme">'
             '<svg class="moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20.5 14A8.5 8.5 0 0 1 10 3.5 8.5 8.5 0 1 0 20.5 14Z"/></svg>'
             '<svg class="sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></svg></button>')


def shell(out_path, title, desc, main, section=None):
    a = lambda p: rel(out_path, p)
    nav = "".join(f'<a href="{a(p)}"{" aria-current=page" if n == section else ""}>{n}</a>' for n, p in NAV)
    dlg = "".join(f'<a href="{a(p)}"{" aria-current=page" if n == section else ""}>{n}</a>' for n, p in NAV)
    full_title = f"{title} | Sameer Mittimani"
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title><meta name="description" content="{esc(desc)}">
<meta name="author" content="Sameer Shreenivas Mittimani"><meta name="theme-color" content="#0a0a0f">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website">
<script>try{{var t=localStorage.getItem('sameer-portfolio-theme');document.documentElement.dataset.theme=(t==='light'||t==='dark')?t:(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark')}}catch(e){{}}</script>
<link rel="icon" type="image/svg+xml" href="{a('assets/favicon.svg')}"><link rel="stylesheet" href="{a('assets/fonts.css')}"><link rel="stylesheet" href="{a('assets/style.css')}"><link rel="stylesheet" href="{a('assets/site_extra.css')}"><script defer src="{a('assets/app.js')}"></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header wrap"><a class="brand" href="{ME}/index.html" aria-label="Sameer Mittimani, home"><span class="monogram" aria-hidden="true"><span>S</span>ameer</span></a><nav class="desktop-nav" aria-label="Main navigation"><a href="{a('index.html')}"{" aria-current=page" if section == "Home" else ""}>Overview</a>{nav}<a class="resume-link" href="{ME}/work.html">My work {ARROW}</a></nav><div class="header-tools">{THEME_BTN}<button id="menuToggle" class="menu-toggle" aria-controls="menuDialog" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button></div></header>
<dialog id="menuDialog" aria-label="Navigation"><div class="dialog-top"><span class="eyebrow">Navigation</span><button id="menuClose" class="icon-button" aria-label="Close menu">×</button></div><nav aria-label="Mobile navigation"><a href="{a('index.html')}">Overview</a>{dlg}<a href="{ME}/work.html">My work {ARROW}</a></nav><p>Chennai, India</p></dialog>
<main id="main">{main}</main>
<footer id="contact" class="contact-footer"><div class="wrap"><div class="contact-top"><div><span class="eyebrow">Get in touch</span><h2>Let's talk product.</h2><p>I'm working toward a product role and would like to hear from people building in finance, auto or data. Happy to walk through a project or compare notes.</p></div><a class="contact-orbit" href="mailto:samsm@outlook.in" aria-label="Email Sameer">↗</a></div><div class="contact-bottom"><div class="email-group"><a class="button email-button" href="mailto:samsm@outlook.in">Email me {ARROW}</a><span class="email-plain">samsm@outlook.in</span></div><nav aria-label="Social links"><a href="https://www.linkedin.com/in/sameersm">LinkedIn {ARROW}</a><a href="https://github.com/cercit">GitHub {ARROW}</a><a href="https://www.kaggle.com/cercit">Kaggle {ARROW}</a><a href="{ME}/assets/resume.pdf">Resume (PDF) {ARROW}</a></nav></div><div class="footer-fine"><span>Sameer Shreenivas Mittimani</span><a href="{ME}/about.html">More about me</a><span>Lender terms and car prices on this site are invented or demo values · 2026</span></div></div></footer></body></html>"""


def write(out_path, text):
    p = OUT / out_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf8")


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
        return text
    return re.sub(r'<a href="([^"]+)">(.*?)</a>', anchor, body, flags=re.S)


TAGS = {"Built": "built", "Planned": "planned", "Assumption": "assumption", "Test value": "test"}


def clean_body(body, src_rel, out_path):
    body = fix_links(body, src_rel, out_path)
    for name, cls in TAGS.items():
        body = body.replace(f"[{name}]", f'<span class="tag tag-{cls}">{name}</span>')
    return body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")


def hero(back_href, back_text, kicker, title, deck="", summary="", actions=""):
    return (f'<section class="case-hero wrap"><a class="back-link" href="{back_href}"><span aria-hidden="true">←</span> {esc(back_text)}</a>'
            f'<div class="project-meta"><span>{esc(kicker)}</span></div><h1>{esc(title)}</h1>'
            + (f'<p class="case-deck">{esc(deck)}</p>' if deck else "") + (f'<p class="case-summary">{esc(summary)}</p>' if summary else "")
            + (f'<div class="case-actions">{actions}</div>' if actions else "") + "</section>")


def doc_page(src_rel, section, deck=""):
    out_path = MAP[src_rel]
    text = (ROOT / src_rel).read_text(encoding="utf8")
    body = md.render(text)
    m = re.search(r"<h1>(.*?)</h1>", body, re.S)
    title = re.sub(r"<.*?>", "", m.group(1)) if m else src_rel
    body = clean_body(re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S), src_rel, out_path)
    idx, kicker = SECTIONS[section]
    extra = ""
    if src_rel == "launch/production-launch-plan.md":
        extra = f'<a class="button button-secondary" href="production-launch-plan.pdf">Download the PDF {ARROW}</a>'
    back_text = section if section not in ("Launch", "Selection") else "Overview"
    back_href = rel(out_path, idx) if section not in ("Launch", "Selection") else rel(out_path, "index.html")
    main = hero(back_href, back_text, kicker, title, deck, actions=extra) + f'<div class="wrap doc-wrap"><article class="doc">{body}</article></div>'
    write(out_path, shell(out_path, title, deck or title, main, section))


def list_page(out_path, section, title, deck, items):
    rows = "".join(f'<a class="doc-item" href="{rel(out_path, MAP[s])}"><span class="num">{i:02d}</span><span><b>{esc(n)}</b><small>{esc(d)}</small></span><span class="arr" aria-hidden="true">↗</span></a>'
                   for i, (n, s, d) in enumerate(items, 1))
    main = hero(rel(out_path, "index.html"), "Overview", SECTIONS[section][1], title, deck) + f'<div class="wrap doc-wrap"><div class="doc-list">{rows}</div></div>'
    write(out_path, shell(out_path, title, deck, main, section))


def home():
    out = "index.html"
    a = lambda p: rel(out, p)
    cover = ('<div class="case-cover wrap"><div class="project-visual visual-cercit case-visual"><div class="browser-frame"><div class="browser-bar"><span aria-hidden="true">● ● ●</span><span>DealerFinance / six-step journey</span><span aria-hidden="true">↗</span></div>'
             '<video controls preload="metadata" poster="assets/poster.jpg" aria-label="Product walk-through, 2 minutes 25 seconds"><source src="assets/demo.mp4" type="video/mp4">Your browser cannot play this video.</video></div>'
             '<span class="visual-foot">Walk-through · 2:25 · name and one-time codes shown on purpose; mobile, PAN, vehicle number and Aadhaar covered · test data</span></div></div>')
    facts = ('<section class="case-facts wrap" aria-label="Project facts"><dl><div><dt>Cohort</dt><dd>9 to 13 Oct 2026, Bengaluru</dd></div><div><dt>Product</dt><dd>DealerFinance, new-car loans</dd></div>'
             '<div><dt>Data</dt><dd>Invented test values</dd></div><div><dt>My contribution</dt><dd>Product, PRD, sprint plan, no-code build</dd></div></dl></section>')
    side = ('<aside class="case-sidebar"><p class="eyebrow">Inside the project</p><nav aria-label="On this page"><a href="#section-1"><span>01</span>How I got in</a><a href="#section-2"><span>02</span>What I learned</a><a href="#section-3"><span>03</span>What I built</a>'
            '<a href="#section-4"><span>04</span>What broke, and the fixes</a><a href="#section-5"><span>05</span>The launch plan</a><a href="#section-6"><span>06</span>Privacy and credits</a><a href="#section-7"><span>07</span>Thank you</a></nav>'
            f'<a class="text-link" href="{ME}/work.html">All projects <span aria-hidden="true">↗</span></a></aside>')

    def links(items):
        return '<ul class="links">' + "".join(f'<li><a href="{a(MAP[s])}"><span>{esc(n)}<small>{esc(d)}</small></span>{ARROW}</a></li>' for n, s, d in items) + "</ul>"
    story = f"""<article class="case-story"><p class="case-intro">I joined a five-day fintech product management cohort to learn how lenders and no-code lending platforms work. Then I planned and built DealerFinance: a loan journey for new-car buyers at a dealership. I tested it live with about 15 to 16 people and fixed what broke.</p>
<div class="contribution"><h2>My contribution</h2><p>I defined the product, wrote the PRD and sprint plan, built the journey on the no-code platform (forms, journey and logic formulas), ran the testing and wrote up what I learned.</p></div>
<ul class="days"><li><time>9 Oct</time> Banks, RBI, NBFCs and a first look at the platform</li><li><time>10 Oct</time> Underwriting, KYC, credit reports, income proof, hands-on</li><li><time>11 Oct</time> Office closed. Wireframe revised</li><li><time>12 Oct</time> Help day. The journey takes shape</li><li><time>13 Oct</time> Final brief and the live demo</li><li><time>14 Oct</time> Written production launch plan</li></ul>
<section id="section-1" class="case-section"><span class="section-number">01</span><h2>How I got in: the selection project</h2><p>Before the cohort, FinStack gave candidates an assignment. I submitted a product teardown of BHIM and PhonePe, with a three-year roadmap for each. My view: PhonePe shows too much, BHIM shows too little, and each app's ownership explains why.</p><p>The page has the findings, the money table and both roadmaps, with the original PDF.</p><ul class="links"><li><a href="{a('selection/index.html')}"><span>BHIM vs PhonePe: teardown and roadmap<small>The selection project</small></span>{ARROW}</a></li></ul></section>
<section id="section-2" class="case-section"><span class="section-number">02</span><h2>What I learned</h2><p>Banks and lenders differ by what their money costs and which customers they choose. In a lending product the order of checks is a design choice: cheap checks first, costly ones later, and "no data" is a normal answer, not an error.</p><p>I wrote seven notes, and a table that links each class topic to where I used it in the product.</p>{links(LEARNED[:3])}<a class="text-link" href="{a('learned/index.html')}">All seven notes <span aria-hidden="true">↗</span></a></section>
<section id="section-3" class="case-section"><span class="section-number">03</span><h2>What I built</h2><p>DealerFinance is a six-step journey. It collects consent by one-time code, verifies identity through DigiLocker, works out the price and loan, shows which lenders are likely to accept, sends the case to one lender, reroutes after a rejection and settles the dealer's trade advance and commission.</p><p>It runs on a no-code platform, for Kia cars and four lenders. Lender terms, rates and limits are invented test values.</p>{links(BUILT[:3])}<a class="text-link" href="{a('built/index.html')}">All documents <span aria-hidden="true">↗</span></a></section>
<section id="section-4" class="case-section"><span class="section-number">04</span><h2>What broke, and the fixes</h2><p>At the live demo, customers with no credit score and customers with no car to exchange hit dead ends. I fixed both, and the second change also saved a paid lookup per case. My own testing found a loan formula that ignored the exchange value, which is still open.</p>{links(TESTED)}</section>
<section id="section-5" class="case-section"><span class="section-number">05</span><h2>The launch plan</h2><p>The plan chooses a dealership system as the place to plug in, lists the fields it must give us on each screen, says what it has to change, and sets out four phases with the assumptions marked. It went in after the deadline, and the retrospective says so.</p><ul class="links"><li><a href="{a('launch/index.html')}"><span>Production launch plan<small>Page and PDF</small></span>{ARROW}</a></li></ul></section>
<section id="section-6" class="case-section"><span class="section-number">06</span><h2>Privacy and credits</h2><p>Mobile numbers, PAN, Aadhaar, emails, logins and other people's names are not in this record. The demo clip shows my own name and one-time codes on purpose and covers the rest.</p><p>Teammate: Aditya Sharan (<a href="https://github.com/aaDhut">github.com/aaDhut</a>), Team 6.</p><ul class="chips"><li>Consent and KYC design</li><li>Credit bureau and soft pull</li><li>No-code journey building</li><li>PRD writing</li><li>Sprint planning</li><li>Edge-case testing</li><li>Production launch planning</li></ul><a class="text-link" href="{a('about/index.html')}">What was removed, and how <span aria-hidden="true">↗</span></a><section id="section-7" class="case-section"><span class="section-number">07</span><h2>Thank you</h2><p>The cohort and hackathon were an amazing experience: real products, building and experimenting across fintech. The best part was the people.</p><ul class="links"><li><a href="https://www.linkedin.com/in/gaurav-agarwal1/" rel="noopener"><span>Gaurav Agarwal<small>Cohort host, co-founder of FinStack. For walking us through how banks, loans and bonds really work.</small></span>{ARROW}</a></li><li><a href="https://www.linkedin.com/in/dhawal-patel-4095/" rel="noopener"><span>Dhawal Patel<small>Cohort host, co-founder of FinStack. For the platform walk-through, and the help while I built.</small></span>{ARROW}</a></li><li><a href="https://www.linkedin.com/in/arun-nandewal/" rel="noopener"><span>Arun Nandewal<small>Mentor. For connecting me with this group, and for helping organise the hackathon.</small></span>{ARROW}</a></li><li><a href="https://www.linkedin.com/in/adityasharan10/" rel="noopener"><span>Aditya Sharan<small>Teammate, Team 6. For being my partner in the hackathon.</small></span>{ARROW}</a></li></ul></section></article>"""
    nxt = (f'<section class="next-project wrap"><div><p class="eyebrow">Up next</p><h2><a href="{ME}/projects/upi-recovery.html">Wrong UPI payment recovery {ARROW}</a></h2><p>Request recovery from the payment receipt</p></div>'
           f'<a class="text-link" href="{ME}/work.html">Back to all work <span aria-hidden="true">→</span></a></section>')
    h = hero(f"{ME}/work.html", "All work", "cohort / case study", "FinStack cohort", "What I learned, built and fixed in five days",
             "A fintech product management cohort in Bengaluru. I learned how lenders and no-code lending platforms work, then built, tested and fixed a loan journey for new-car buyers.",
             f'<a class="button button-secondary" href="#section-3">What I built {ARROW}</a><a class="button button-secondary" href="https://github.com/cercit/finstack-cohort">Browse the files {ARROW}</a>')
    partner = (f'<div class="partner"><span>Cohort run by</span><img class="img-light" src="{a("assets/finstack-logo-light.svg")}" alt="FinStack" height="30">'
               f'<img class="img-dark" src="{a("assets/finstack-logo-dark.svg")}" alt="FinStack" height="30"></div>')
    h = h.replace("<h1>FinStack cohort</h1>", partner + "<h1>FinStack cohort</h1>", 1)
    main = h + cover + facts + f'<div class="case-layout wrap">{side}{story}</div>' + nxt
    write(out, shell(out, "FinStack cohort", "What I learned, built and fixed in the FinStack fintech product management cohort.", main, "Home"))


def about():
    out = "about/index.html"
    readme = md.render((ROOT / "README.md").read_text(encoding="utf8"))
    readme = re.sub(r"<h1>.*?</h1>", "", readme, count=1, flags=re.S)
    readme = re.sub(r"<h2>Where to look</h2>.*?(?=<h2>)", "", readme, flags=re.S)
    readme = re.sub(r"<p>To browse locally.*?</p>", "", readme, flags=re.S)
    redact = md.render((ROOT / "REDACTION.md").read_text(encoding="utf8")).replace("<h1>", "<h2>").replace("</h1>", "</h2>")
    lic = esc((ROOT / "LICENSE").read_text(encoding="utf8"))
    body = clean_body(readme, "README.md", out) + clean_body(redact, "REDACTION.md", out) + f"<h2>Licence</h2><pre><code>{lic}</code></pre>"
    main = hero(rel(out, "index.html"), "Overview", "about / privacy", "About this record", "What it is, what was removed, and the licence") + f'<div class="wrap doc-wrap"><article class="doc">{body}</article></div>'
    write(out, shell(out, "About this record", "What this record is, what was removed from it, and the licence.", main, "About"))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "fonts").mkdir(parents=True)
    for f in ("style.css", "fonts.css", "app.js", "favicon.svg", "site_extra.css", "finstack-logo-dark.svg", "finstack-logo-light.svg"):
        shutil.copy(ASSETS / f, OUT / "assets" / f)
    for f in (ASSETS / "fonts").glob("*.woff2"):
        shutil.copy(f, OUT / "assets" / "fonts" / f.name)
    clip = ROOT / "product/demo/dealerfinance-journey-masked.mp4"
    shutil.copy(clip, OUT / "assets/demo.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "98", "-i", str(clip), "-frames:v", "1", "-vf", "scale=1280:-1", "-q:v", "4", str(OUT / "assets/poster.jpg")], check=False)
    for src in ("product/journey/wireframe-as-built.html", "launch/production-launch-plan.pdf", "selection/bhim-vs-phonepe-teardown.pdf"):
        (OUT / MAP[src]).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / src, OUT / MAP[src])
    for n, s, d in LEARNED:
        doc_page(s, "Learned", d)
    for n, s, d in BUILT:
        if s.endswith(".md"):
            doc_page(s, "Built", d)
    for n, s, d in TESTED:
        doc_page(s, "Tested", d)
    doc_page("selection/bhim-vs-phonepe-teardown.md", "Selection", "The product teardown and three-year roadmaps I submitted to FinStack before the cohort.")
    doc_page("launch/production-launch-plan.md", "Launch", "Where it plugs in, the fields it needs, what it has to change, and the phases.")
    list_page("learned/index.html", "Learned", "What I learned", "Five days on how lenders work and the tools behind modern lending products.", [(n, s, d) for n, s, d in LEARNED])
    list_page("built/index.html", "Built", "What I built", "DealerFinance: a loan journey for new-car buyers at a dealership, built on a no-code platform.", [(n, s, d) for n, s, d in BUILT])
    list_page("tested/index.html", "Tested", "What broke, and the fixes", "A live demo with about 15 to 16 people found cases we had not tested.", [(n, s, d) for n, s, d in TESTED])
    about()
    home()
    print("site built:", sum(1 for _ in OUT.rglob("*") if _.is_file()), "files in", OUT)


if __name__ == "__main__":
    main()
