#!/usr/bin/env python3
"""Fail when Hangul appears in the Japanese site outside an allowlist.

Checks two things, and does not write any pages:

1. Committed files under ja/ (the published pages, including news that was
   edited into the HTML and is not in generate.py).
2. Japanese HTML rendered in memory from generate.py, so a shared string
   that is still Korean cannot leak back in on the next intentional
   regenerate. This does not call generate.main() and does not touch ko/.

Hangul covered: syllables (AC00–D7A3), jamo (1100–11FF), compatibility
jamo (3130–318F).
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
JA_DIR = ROOT / "ja"

# Exact phrases kept on purpose. Keep each entry the full phrase, not a
# short fragment, so accidental Hangul next to it still fails.
ALLOWLIST = [
    # Language switch on every ja page. The visible label is "🌐 KR".
    # The accessible name is Korean on purpose, in the language being
    # switched to (ko pages use aria-label="日本語に切り替え").
    "한국어로 전환",
]

HANGUL = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]")


def strip_allowed(text: str) -> str:
    for phrase in ALLOWLIST:
        text = text.replace(phrase, "")
    return text


def hangul_lines(text: str) -> list[tuple[int, str]]:
    """Return (1-based line, snippet) for lines that still contain Hangul."""
    cleaned = strip_allowed(text).splitlines()
    original = text.splitlines()
    found = []
    for i, line in enumerate(cleaned):
        if not HANGUL.search(line):
            continue
        orig = original[i]
        match = HANGUL.search(orig)
        if match and len(orig.strip()) > 180:
            start = max(0, match.start() - 40)
            snippet = orig[start:match.end() + 40].strip()
        else:
            snippet = orig.strip()
        found.append((i + 1, snippet))
    return found


def check_tree() -> list[str]:
    if not JA_DIR.is_dir():
        return [f"ja directory not found: {JA_DIR}"]
    failures = []
    files = sorted(p for p in JA_DIR.rglob("*") if p.is_file())
    for path in files:
        data = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for lineno, snippet in hangul_lines(data):
            failures.append(f"{rel}:{lineno}: {snippet}")
    return failures


def check_generator() -> list[str]:
    """Render ja pages in memory. Never writes, never touches ko/ output."""
    sys.path.insert(0, str(ROOT))
    import generate  # noqa: WPS433 — local generator, import is side-effect free

    failures = []
    rendered = {
        "index.html": generate.render_index("ja"),
        "stock-analysis.html": generate.render_hub("ja"),
        "economy-trends.html": generate.render_economy("ja"),
        "about.html": generate.render_about("ja"),
        "contact.html": generate.render_contact("ja"),
        "privacy-policy.html": generate.render_privacy("ja"),
        "terms.html": generate.render_terms("ja"),
    }
    for ticker in generate.TICKERS:
        rendered[f"post-{ticker['slug']}.html"] = generate.render_post(ticker, "ja")
    for name, html in rendered.items():
        for lineno, snippet in hangul_lines(html):
            failures.append(f"generate.py → ja/{name}:{lineno}: {snippet}")
    return failures


def main() -> int:
    tree_failures = check_tree()
    gen_failures = check_generator()
    file_count = sum(1 for p in JA_DIR.rglob("*") if p.is_file()) if JA_DIR.is_dir() else 0
    print(f"Checked {file_count} files under ja/, plus in-memory ja render from generate.py.")
    failures = tree_failures + gen_failures
    if failures:
        print(f"Hangul found ({len(failures)} line(s)):")
        for item in failures:
            print(f"  {item}")
        print(
            "If this Korean text is a proper noun or an intentional label, "
            "add the exact phrase to ALLOWLIST in scripts/check_ja_hangul.py."
        )
        return 1
    print("No unintended Hangul in ja output.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
