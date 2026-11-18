import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

HOST = "www.bugwrite.com"
KEY = "e7b4c9a21f6d48039b5e2a8c1d7f4e90"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/IndexNow"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(ROOT, "public", "sitemap.xml")


def load_sitemap_urls():
    tree = ET.parse(SITEMAP_PATH)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in tree.getroot().findall("sm:url/sm:loc", ns) if el.text]


def main():
    if len(sys.argv) > 1:
        urls = [u if u.startswith("http") else f"https://{HOST}/{u.lstrip('/')}" for u in sys.argv[1:]]
    else:
        urls = load_sitemap_urls()

    if not urls:
        print("No URLs found to submit.")
        sys.exit(1)

    # First verify key file is live on production
    try:
        with urllib.request.urlopen(KEY_LOCATION, timeout=10) as resp:
            live_key = resp.read().decode("utf-8").strip()
            if live_key != KEY:
                print(f"Key mismatch at {KEY_LOCATION}: got {live_key!r}")
                sys.exit(1)
    except Exception as e:
        print(f"Key file not yet live at {KEY_LOCATION}: {e}")
        print("Deploy to Vercel first, then re-run: npm run indexnow")
        sys.exit(1)

    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")

    req = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"IndexNow SUCCESS (HTTP {resp.status}): Submitted {len(urls)} URLs to Bing, Copilot, DuckDuckGo & Yandex!")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"IndexNow HTTP {e.code}: {body}")
        sys.exit(1)


if __name__ == "__main__":
    main()
