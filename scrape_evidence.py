#!/usr/bin/env python3
"""
Evidence scraper — captures all public pages of a website as screenshots + HTML.
Usage: python scrape_evidence.py <URL>
"""

import sys
import os
import re
import json
import time
import argparse
from datetime import datetime
from urllib.parse import urlparse, urljoin, urldefrag
from pathlib import Path
from collections import deque

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


CHROMIUM_PATH = '/opt/pw-browsers/chromium'

PATTERNS_OF_INTEREST = [
    r'\$[\d,]+(?:\.\d{2})?',           # dollar amounts
    r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # phone numbers
    r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # emails
    r'\b(?:PayPal|Stripe|Venmo|Zelle|CashApp|payment|invoice|transfer|wire)\b',
    r'\b(?:account|routing|IBAN|SWIFT|bank)\b',
]
PATTERN_RE = re.compile('|'.join(PATTERNS_OF_INTEREST), re.IGNORECASE)

CSS_HIDE = """
    *::-webkit-scrollbar { display: none !important; }
    body { overflow: visible !important; }
"""


def sanitize_filename(url: str, index: int) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', path or 'homepage')[:60]
    return f"{index:03d}_{name}"


def extract_notable(text: str) -> list:
    return list(set(PATTERN_RE.findall(text)))


def build_html_report(domain: str, pages: list, ts: str) -> str:
    rows = []
    for p in pages:
        notable_html = ''
        if p['notable']:
            items = ''.join(f'<li><code>{h}</code></li>' for h in p['notable'])
            notable_html = f'<ul class="notable">{items}</ul>'
        rows.append(f"""
        <tr>
            <td><a href="pages/{p['filename']}.html" target="_blank">{p['index']}</a></td>
            <td><a href="{p['url']}" target="_blank" rel="noopener">{p['url']}</a></td>
            <td><a href="pages/{p['filename']}.png" target="_blank">screenshot</a></td>
            <td>{p['captured']}</td>
            <td>{notable_html or '—'}</td>
        </tr>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Evidence — {domain} — {ts}</title>
<style>
  body {{ font-family: monospace; padding: 2em; background: #111; color: #eee; }}
  h1 {{ color: #f90; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #444; padding: 8px 12px; text-align: left; vertical-align: top; }}
  th {{ background: #222; color: #aaa; }}
  a {{ color: #6af; }}
  .notable li {{ color: #fa0; font-size: 0.85em; }}
</style>
</head>
<body>
<h1>Evidence capture: {domain}</h1>
<p>Captured: <strong>{ts}</strong> &nbsp;|&nbsp; Pages: <strong>{len(pages)}</strong></p>
<table>
<thead><tr><th>#</th><th>URL</th><th>Screenshot</th><th>Captured at</th><th>Notable content</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</body>
</html>"""


def crawl(start_url: str, output_dir: Path):
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc

    pages_dir = output_dir / 'pages'
    pages_dir.mkdir(parents=True, exist_ok=True)

    links_file   = output_dir / 'links.txt'
    text_file    = output_dir / 'text_content.txt'
    report_file  = output_dir / 'index.html'

    visited   = set()
    queue     = deque([start_url])
    page_data = []
    index     = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=CHROMIUM_PATH,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        ctx = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            ),
        )
        page = ctx.new_page()
        page.add_style_tag(content=CSS_HIDE)

        while queue:
            url, _ = urldefrag(queue.popleft())
            if url in visited:
                continue
            visited.add(url)

            # Stay on same domain
            if urlparse(url).netloc != base_domain:
                continue

            index += 1
            captured_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            filename = sanitize_filename(url, index)

            print(f"[{index:03d}] {url}")

            try:
                page.goto(url, timeout=30_000, wait_until='networkidle')
            except PlaywrightTimeout:
                print(f"       TIMEOUT — skipping")
                continue
            except Exception as e:
                print(f"       ERROR: {e} — skipping")
                continue

            # Wait a moment for lazy-loaded content
            try:
                page.wait_for_timeout(1500)
            except Exception:
                pass

            # Screenshot (full page)
            try:
                page.screenshot(path=str(pages_dir / f'{filename}.png'), full_page=True)
            except Exception as e:
                print(f"       screenshot error: {e}")

            # Save HTML
            html = page.content()
            (pages_dir / f'{filename}.html').write_text(html, encoding='utf-8')

            # Extract visible text
            try:
                text = page.evaluate("() => document.body.innerText")
            except Exception:
                text = ''

            notable = extract_notable(text)

            page_data.append({
                'index':    index,
                'url':      url,
                'filename': filename,
                'captured': captured_at,
                'notable':  notable,
            })

            with open(text_file, 'a', encoding='utf-8') as tf:
                tf.write(f"\n{'='*80}\n[{index:03d}] {url}  |  {captured_at}\n{'='*80}\n")
                tf.write(text[:50_000])  # cap per page to keep file manageable

            # Discover links
            hrefs = page.eval_on_selector_all('a[href]', 'els => els.map(e => e.href)')
            for href in hrefs:
                clean, _ = urldefrag(href)
                if clean and clean not in visited:
                    p = urlparse(clean)
                    if p.netloc == base_domain and p.scheme in ('http', 'https'):
                        queue.append(clean)

        browser.close()

    # Write links.txt
    links_file.write_text('\n'.join(v['url'] for v in page_data), encoding='utf-8')

    # Write HTML report
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    report_file.write_text(
        build_html_report(base_domain, page_data, ts),
        encoding='utf-8'
    )

    return page_data


def main():
    parser = argparse.ArgumentParser(description='Capture public website pages as evidence.')
    parser.add_argument('url', help='Starting URL (e.g. https://example.com)')
    parser.add_argument('--out', default=None, help='Output directory (default: auto-named)')
    args = parser.parse_args()

    start_url = args.url
    if not start_url.startswith('http'):
        start_url = 'https://' + start_url

    domain = urlparse(start_url).netloc.replace(':', '_')
    ts_label = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    out_name = args.out or f'evidence_{domain}_{ts_label}'
    output_dir = Path(out_name)

    print(f"\nStarting evidence capture")
    print(f"  Target : {start_url}")
    print(f"  Output : {output_dir}/")
    print(f"  Time   : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    t0 = time.time()
    pages = crawl(start_url, output_dir)
    elapsed = time.time() - t0

    print(f"\nDone. {len(pages)} pages captured in {elapsed:.1f}s")
    print(f"  Report  : {output_dir}/index.html")
    print(f"  HTML    : {output_dir}/pages/")
    print(f"  Links   : {output_dir}/links.txt")
    print(f"  Text    : {output_dir}/text_content.txt")


if __name__ == '__main__':
    main()
