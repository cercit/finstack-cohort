"""Scan text files for personal data before anything is committed.
Usage: python tools/scan_sensitive.py [folder]   (default: repo root)
Prints file, line and a masked sample for each hit. Exit code 1 if anything is found."""
import re, sys, pathlib

PATTERNS = {
    "MOBILE": re.compile(r"(?<!\d)(?:\+?91[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)"),
    "PAN": re.compile(r"(?<![A-Za-z0-9])[A-Z]{5}[0-9]{4}[A-Z](?![A-Za-z0-9])"),
    "AADHAAR": re.compile(r"(?<!\d)\d{4}[ -]?\d{4}[ -]?\d{4}(?!\d)"),
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "SECRET": re.compile(r"(?i)(password|passwd|pwd|secret|api[_-]?key|token)\s*[:=]\s*\S+"),
    "LOGIN-URL": re.compile(r"(?i)https?://[^\s]*(login|onboarding|\?url=)[^\s]*"),
}
# Classmates' and team members' names live in tools/names.local.txt (one per line).
# That file is git-ignored on purpose, so the names never enter the repo.
_names_file = pathlib.Path(__file__).with_name("names.local.txt")
NAMES = [n.strip() for n in _names_file.read_text(encoding="utf8").splitlines() if n.strip()] if _names_file.exists() else []
ALLOW_EMAILS = {"team@getfinstack.in"}
TEXT = {".md", ".txt", ".html", ".py", ".json", ".csv", ".js", ".css"}

def mask(s):
    return s[:2] + "*" * max(len(s) - 4, 2) + s[-2:] if len(s) > 4 else "****"

def main(root):
    root = pathlib.Path(root); hits = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts or p.suffix.lower() not in TEXT or p.name in ("scan_sensitive.py", "names.local.txt"):
            continue
        try:
            lines = p.read_text(encoding="utf8", errors="ignore").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            for tag, rx in PATTERNS.items():
                for m in rx.finditer(line):
                    if tag == "EMAIL" and m.group(0).lower() in ALLOW_EMAILS: continue
                    hits += 1; print(f"{p.relative_to(root)}:{n}: {tag} {mask(m.group(0))}")
            for name in NAMES:
                if name.lower() in line.lower():
                    hits += 1; print(f"{p.relative_to(root)}:{n}: NAME {mask(name)}")
    print(f"{hits} hit(s)")
    return 1 if hits else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
