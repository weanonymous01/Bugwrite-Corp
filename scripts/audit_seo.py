import glob
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

CANONICAL_HOST = "https://www.bugwrite.com"

# 1. Homepage audit
home = open("index.html", encoding="utf-8").read()
title = re.search(r"<title>([^<]+)</title>", home).group(1)
desc = re.search(r'<meta name="description" content="([^"]+)"', home).group(1)
guide_html = re.search(r'<section id="editorial-guide"[\s\S]*?</section>', home).group(0)
guide_words = len(re.sub(r"<[^>]+>", " ", guide_html).split())
print(f"Home Title ({len(title)} chars): {title}")
print(f"Home Desc ({len(desc)} chars): {desc}")
print(f"SEO Guide + FAQ word count: {guide_words} words")
assert len(title) <= 60, f"Home title too long: {len(title)}"
assert len(desc) <= 160, f"Home desc too long: {len(desc)}"

# 2. Check compiled static CSS & brand assets
css_path = "public/assets/styles.css"
assert os.path.exists(css_path), "Missing compiled Tailwind CSS: public/assets/styles.css"
css_size_kb = os.path.getsize(css_path) / 1024
print(f"Compiled Tailwind CSS: {css_size_kb:.1f} KB (replaces ~400 KB render-blocking CDN JS!)")
assert css_size_kb < 60, f"CSS unexpectedly large: {css_size_kb:.1f} KB"

for asset in [
    "public/favicon.svg",
    "public/favicon.ico",
    "public/favicon-48x48.png",
    "public/favicon-192x192.png",
    "public/apple-touch-icon.png",
    "public/site.webmanifest",
    "public/blog/bugwrite-logo.png",
    "vercel.json",
]:
    assert os.path.exists(asset), f"Missing required asset: {asset}"

# 3. Audit ALL generated static HTML pages
html_files = ["index.html", "public/404.html", "public/500.html"]
html_files += sorted(glob.glob("public/*/index.html"))
html_files += sorted(glob.glob("public/*/article/*/index.html"))

total_schemas = 0
for fp in html_files:
    txt = open(fp, encoding="utf-8").read()
    no_scripts = re.sub(r"<script[\s\S]*?</script>", "", txt)
    h1s = re.findall(r"<h1[\s>]", no_scripts)
    assert len(h1s) == 1, f"{fp} has {len(h1s)} <h1> tags!"
    assert "cdn.tailwindcss.com" not in txt, f"{fp} still loads render-blocking Tailwind CDN!"
    assert "fonts.googleapis.com" not in txt, f"{fp} still loads unused Google Fonts!"
    assert "/assets/styles.css" in txt, f"{fp} missing local styles.css!"
    assert 'rel="icon"' in txt, f"{fp} missing favicon!"
    assert 'application/rss+xml' in txt, f"{fp} missing RSS link!"
    canon_m = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
    assert canon_m, f"{fp} missing canonical!"
    assert canon_m.group(1).startswith(CANONICAL_HOST), f"{fp} non-www canonical: {canon_m.group(1)}"
    if not fp.endswith(("404.html", "500.html")):
        assert "max-image-preview:large" in txt, f"{fp} missing Google Discover max-image-preview:large!"
    assert "og:title" in txt and "twitter:card" in txt, f"{fp} missing OG/Twitter!"
    assert txt.count("\u2014") == 0 and txt.count("\u2013") == 0, f"{fp} has em/en dash!"
    for m in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', txt):
        json.loads(m)
        total_schemas += 1
    for img in re.findall(r"<img\b[^>]*>", no_scripts):
        assert "alt=" in img and "width=" in img and "height=" in img, f"Bad img in {fp}: {img}"

print(f"Audited {len(html_files)} HTML pages: 0 Tailwind CDN, all www canonicals, max-image-preview:large, favicons, {total_schemas} valid JSON-LD schemas, 0 em/en dashes!")

# 4. Validate sitemap.xml, news-sitemap.xml, and rss.xml dynamically
article_pages = glob.glob("public/*/article/*/index.html")
expected_total_urls = len(article_pages) + 9
tree = ET.parse("public/sitemap.xml")
urls = tree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
imgs = tree.getroot().findall(".//{http://www.google.com/schemas/sitemap-image/1.1}image")
assert len(urls) == expected_total_urls, f"Expected {expected_total_urls} sitemap URLs, got {len(urls)}"
assert len(imgs) == len(article_pages), f"Expected {len(article_pages)} image sitemap entries, got {len(imgs)}"
for u in urls:
    loc = u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
    assert loc.startswith(CANONICAL_HOST), f"Non-www URL in sitemap: {loc}"
print(f"Valid sitemap.xml: {len(urls)} URLs + {len(imgs)} image entries (all {CANONICAL_HOST})")

news_tree = ET.parse("public/news-sitemap.xml")
news_urls = news_tree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
assert len(news_urls) > 0, "news-sitemap.xml is empty!"
print(f"Valid news-sitemap.xml: {len(news_urls)} recent news URLs")

rss_tree = ET.parse("public/rss.xml")
rss_items = rss_tree.getroot().findall("./channel/item")
assert len(rss_items) == min(50, len(article_pages)), f"Unexpected RSS item count: {len(rss_items)}"
print(f"Valid rss.xml: {len(rss_items)} feed items")

assert os.path.exists("public/e7b4c9a21f6d48039b5e2a8c1d7f4e90.txt"), "Missing IndexNow verification key file!"

# 5. Verify live HTTP 200 on local Vite (or verify static files if server is offline)
live_routes = [
    "/", "/robots.txt", "/sitemap.xml", "/news-sitemap.xml", "/rss.xml", "/ads.txt",
    "/favicon.svg", "/favicon.ico", "/favicon-48x48.png", "/site.webmanifest",
    "/assets/styles.css", "/blog/bugwrite-logo.png",
    "/about", "/contact", "/privacy-policy", "/terms-of-service",
    "/404.html", "/500.html",
    "/gaming", "/big-tech", "/security", "/business",
    "/gaming/article/new-zealand-gta-6-trick",
    "/business/article/anthropic-ipo-nasdaq-ant-2026",
    "/security/article/java4shell-cve-2026-114938",
    "/big-tech/article/apple-outage",
]

server_online = False
try:
    with urllib.request.urlopen("http://localhost:5173/", timeout=1) as resp:
        if resp.status == 200:
            server_online = True
except Exception:
    pass

if server_online:
    for r in live_routes:
        with urllib.request.urlopen("http://localhost:5173" + r, timeout=5) as resp:
            assert resp.status == 200, f"{r} -> {resp.status}"
    print(f"ALL {len(live_routes)} live dev server routes verified HTTP 200!")
else:
    for r in live_routes:
        if r == "/":
            target = "index.html"
        elif r.endswith(".html") or r.endswith((".txt", ".xml", ".svg", ".ico", ".png", ".css", ".webmanifest")):
            target = "public" + r
        else:
            target = os.path.join("public", r.strip("/"), "index.html")
        assert os.path.exists(target), f"Static file target missing: {target}"
    print(f"ALL {len(live_routes)} static route targets verified on disk (dev server offline)!")
