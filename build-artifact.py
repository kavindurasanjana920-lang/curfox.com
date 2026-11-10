#!/usr/bin/env python3
"""Bundle a page + styles.css + assets/ into one self-contained file.

The Artifact host wraps the output in <!doctype html><head></head><body>, so we
emit only <title>, the font <link>, an inline <style>, and the body content.

    python3 build-artifact.py            # build every page
    python3 build-artifact.py index.html # build one

Each published artifact is its own single page, so relative links between pages
(features.html <-> index.html) cannot resolve there. Paste each page's artifact
URL into ARTIFACT_URLS below and re-run to rewrite those links in the bundles.
"""
import base64
import mimetypes
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent

PAGES = {
    "index.html": "curfox-landing.html",
    "features.html": "curfox-features.html",
    "about.html": "curfox-about.html",
    "privacy.html": "curfox-privacy.html",
}

# Live artifact URL for each page; leave blank to keep the relative link.
ARTIFACT_URLS = {
    "index.html": "https://claude.ai/code/artifact/d6eb119b-7a4d-4306-8615-f5f6a8408c31",
    "features.html": "https://claude.ai/code/artifact/64072efd-f15b-4e4e-8ed7-76aa739c4bb4",
    "about.html": "https://claude.ai/code/artifact/dd02350a-1449-487c-80ce-aed72fbf2fbe",
    "privacy.html": "",
}

STRIP = (
    r"<!doctype html>\s*", r"</?html[^>]*>\s*", r"</?head>\s*", r"</?body>\s*",
    r'<meta charset[^>]*>\s*', r'<meta name="viewport"[^>]*>\s*',
    r'<link rel="icon"[^>]*>\s*', r'<link rel="apple-touch-icon"[^>]*>\s*',
)


def data_uri(rel_path: str) -> str:
    path = ROOT / rel_path
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def build(page: str) -> None:
    html = (ROOT / page).read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")

    # Inline every local asset reference as a data URI.
    html = re.sub(r'(?:src|href)="(assets/[^"]+)"',
                  lambda m: m.group(0).replace(m.group(1), data_uri(m.group(1))),
                  html)

    # Point cross-page links at the other page's published artifact, if known.
    for target, url in ARTIFACT_URLS.items():
        if url and target != page:
            html = re.sub(rf'href="{re.escape(target)}(#[^"]*)?"',
                          lambda m: f'href="{url}{m.group(1) or ""}"',
                          html)

    # The live pages link styles.css?v=<date> to bust caches; match any version.
    html = re.sub(r'<link rel="stylesheet" href="styles\.css(?:\?v=[^"]*)?">',
                  lambda m: f"<style>\n{css}\n</style>",
                  html)

    for pattern in STRIP:
        html = re.sub(pattern, "", html, flags=re.I)

    out = ROOT / "dist" / PAGES[page]
    out.parent.mkdir(exist_ok=True)
    out.write_text(html.strip() + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  ({out.stat().st_size / 1024:.0f} KB)")


for target in (sys.argv[1:] or PAGES):
    build(target)
