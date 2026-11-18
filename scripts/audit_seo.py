import glob
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

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

# 2. Audit ALL generated static HTML pages
html_files = ["index.html", "public/404.html", "public/500.html"]
html_files += sorted(glob.glob("public/*/index.html"))
html_files += sorted(glob.glob("public/*/article/*/index.html"))

total_schemas = 0
for fp in html_files:
    txt = open(fp, encoding="utf-8").read()
    no_scripts = re.sub(r"<script[\s\S]*?</script>", "", txt)
    h1s = re.findall(r"<h1[\s>]", no_scripts)
    assert len(h1s) == 1, f"{fp} has {len(h1s)} <h1> tags!"
    assert 'rel="canonical"' in txt, f"{fp} missing canonical!"
    assert "og:title" in txt and "twitter:card" in txt, f"{fp} missing OG/Twitter!"
    assert txt.count("\u2014") == 0 and txt.count("\u2013") == 0, f"{fp} has em/en dash!"
    for m in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', txt):
        json.loads(m)
        total_schemas += 1
    for img in re.findall(r"<img\b[^>]*>", no_scripts):
        assert "alt=" in img and "width=" in img and "height=" in img, f"Bad img in {fp}: {img}"

print(f"Audited {len(html_files)} HTML pages: strictly 1 H1 each, all canonicals/OG/Twitter/img attrs valid, {total_schemas} valid JSON-LD schemas, 0 em/en dashes!")

# 3. Validate sitemap.xml
tree = ET.parse("public/sitemap.xml")
urls = tree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
print(f"Valid XML sitemap: {len(urls)} URLs")
assert len(urls) == 93

# 4. Verify live HTTP 200 on Vite
live_routes = [
    "/", "/robots.txt", "/sitemap.xml", "/ads.txt",
    "/about", "/contact", "/privacy-policy", "/terms-of-service",
    "/404.html", "/500.html",
    "/gaming", "/big-tech", "/security", "/business",
    "/gaming/article/new-zealand-gta-6-trick",
    "/business/article/anthropic-ipo-nasdaq-ant-2026",
    "/security/article/java4shell-cve-2026-114938",
    "/big-tech/article/apple-outage",
]
for r in live_routes:
    with urllib.request.urlopen("http://localhost:5173" + r, timeout=5) as resp:
        assert resp.status == 200, f"{r} -> {resp.status}"
print(f"ALL {len(live_routes)} live SEO routes verified HTTP 200!")
