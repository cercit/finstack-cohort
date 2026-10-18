"""Local viewer for this repo. Run:  python tools/serve.py   then open http://localhost:8765
Shows a file index, renders .md files as pages, and serves .html, .pdf, .json and .txt as they are.
Binds to localhost only."""
import html, http.server, pathlib, urllib.parse
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = 8765
md = MarkdownIt("commonmark").enable("table")
SKIP = {".git", "__pycache__"}
CSS = """body{font:15px/1.55 "Segoe UI",system-ui,sans-serif;max-width:920px;margin:0 auto;padding:20px 16px 60px;color:#1c2733;background:#fff}
a{color:#0b5cad}table{border-collapse:collapse;display:block;overflow-x:auto}th,td{border:1px solid #9aa7b2;padding:4px 8px;vertical-align:top}
th{background:#e8eef2}code{background:#eef2f5;padding:1px 4px;border-radius:3px}pre{background:#eef2f5;padding:10px;overflow-x:auto}
blockquote{border-left:4px solid #9aa7b2;margin:8px 0;padding:2px 12px;color:#44515c}nav{margin-bottom:14px;font-size:.9rem}"""

def page(title, body):
    return f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><style>{CSS}</style><body><nav><a href='/'>Index</a></nav>{body}</body>".encode("utf8")

def index():
    rows = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if p.is_file() and not (set(rel.parts) & SKIP) and p.suffix.lower() in {".md", ".html", ".pdf", ".txt", ".json", ".py", ".csv"}:
            rows.append(f"<li><a href='/{urllib.parse.quote(rel.as_posix())}'>{html.escape(rel.as_posix())}</a></li>")
    return page("finstack-cohort", "<h1>finstack-cohort</h1><ul>" + "".join(rows) + "</ul>")

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)
    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        if path in ("/", ""):
            return self.send(index())
        target = (ROOT / path.lstrip("/")).resolve()
        if ROOT in target.parents and target.suffix.lower() == ".md" and target.is_file():
            text = target.read_text(encoding="utf8", errors="ignore")
            return self.send(page(target.name, md.render(text)))
        return super().do_GET()
    def send(self, data):
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print(f"Serving {ROOT} at http://localhost:{PORT}")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
