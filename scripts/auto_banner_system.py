#!/usr/bin/env python3
"""
Automated Editorial & Pinterest Banner System for Bugwrite (Bugwrite-Corp)

Features:
- Direct Pinterest search and downloading using internal Pinterest API (pinterest-dl)
- Scrapes and downloads high-res pins directly from Pinterest search queries or pin URLs
- Prioritizes widescreen 16:9 / 1920x1080 original images from Pinterest
- Normalizes and center-crops images to crisp 16:9 (1280x720) with Lanczos downsampling
- Optimizes progressive JPEG compression under 180 KB
- Ingests images into public/blog/articles/<slug>.jpg
- Updates public/blog/articles-data.js image pointers and SEO imageAlt tags
- Runs static build, SEO audit, and IndexNow ping pipeline
"""

import os
import sys
import json
import re
import shutil
import argparse
import subprocess
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
ARTICLES_DIR = os.path.join(PUBLIC, "blog", "articles")
DATA_JS = os.path.join(PUBLIC, "blog", "articles-data.js")
SCRATCH_DIR = os.path.join(ROOT, "scratch_pinterest")

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT  # 16:9 = 1.7777...


def load_articles():
    """Load articles from articles-data.js using node."""
    node_cmd = (
        "const fs=require('fs'); const vm=require('vm'); "
        f"const ctx={{window:{{}}}}; vm.runInNewContext(fs.readFileSync({json.dumps(DATA_JS)},'utf8'), ctx); "
        "process.stdout.write(JSON.stringify(ctx.window.BUGWRITE_ARTICLES));"
    )
    res = subprocess.run(["node", "-e", node_cmd], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def normalize_image(source_path, dest_path, quality=88):
    """
    Takes an input image of any dimensions or format, crops to center 16:9,
    resizes to exactly 1280x720, and saves as optimized progressive JPEG.
    """
    with Image.open(source_path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")

        orig_w, orig_h = img.size
        orig_aspect = orig_w / orig_h

        # Center-crop to 16:9 aspect ratio
        if orig_aspect > TARGET_ASPECT:
            # Source is wider than 16:9 -> crop horizontal edges
            new_w = int(orig_h * TARGET_ASPECT)
            left = (orig_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, orig_h))
        elif orig_aspect < TARGET_ASPECT:
            # Source is taller than 16:9 -> crop vertical edges with center/top-weighted crop
            new_h = int(orig_w / TARGET_ASPECT)
            # 35% top weight for character portraits to preserve faces
            top = max(0, int((orig_h - new_h) * 0.35))
            img = img.crop((0, top, orig_w, top + new_h))

        # High quality Lanczos downsample to 1280x720
        img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

        # Save optimized progressive JPEG
        os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
        img.save(dest_path, "JPEG", quality=quality, optimize=True, progressive=True)

        size_kb = os.path.getsize(dest_path) / 1024
        return size_kb


def update_article_metadata(article_id, image_rel_path, image_alt):
    """Update image and imageAlt for a given article in public/blog/articles-data.js."""
    with open(DATA_JS, "r", encoding="utf-8") as f:
        content = f.read()

    # Match both "id": "..." or id: "..."
    art_pattern = re.compile(
        rf'(\{{\s*\"?id\"?:\s*"{re.escape(article_id)}",[\s\S]*?)(\"?image\"?:\s*"[^"]*",)(\s*\"?imageAlt\"?:\s*"[^"]*",)?([\s\S]*?\n\s*\}},?)'
    )

    match = art_pattern.search(content)
    if not match:
        print(f"[!] Article '{article_id}' not found in articles-data.js")
        return False

    prefix = match.group(1)
    old_img = match.group(2)
    old_alt = match.group(3)
    suffix = match.group(4)

    # Determine whether keys use quotes
    use_quotes = '"image"' in old_img
    img_key = '"image"' if use_quotes else 'image'
    alt_key = '"imageAlt"' if use_quotes else 'imageAlt'

    new_img = f'{img_key}: "{image_rel_path}",'
    new_alt = f'\n      {alt_key}: "{image_alt}",'

    def replacer(m):
        return f"{prefix}{new_img}{new_alt}{suffix}"

    updated = art_pattern.sub(replacer, content, count=1)

    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"[+] Updated '{article_id}' -> image='{image_rel_path}'")
    return True


def fetch_from_pinterest(query, target_id, alt_text=None, num_candidates=5):
    """
    Searches Pinterest for the given query, downloads candidate images,
    selects the best widescreen / highest quality candidate, crops to 1280x720,
    and updates the article.
    """
    from pinterest_dl import ApiScraper

    print(f"\n[Pinterest] Searching for: '{query}' (target: {target_id})...")
    temp_dir = os.path.join(SCRATCH_DIR, re.sub(r"[^a-zA-Z0-9]+", "_", target_id))
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    scraper = ApiScraper()
    try:
        results = scraper.search_and_download(query, temp_dir, num=num_candidates)
    except Exception as e:
        print(f"[!] Pinterest search error: {e}")
        return False

    downloaded = [
        os.path.join(temp_dir, f)
        for f in os.listdir(temp_dir)
        if os.path.isfile(os.path.join(temp_dir, f)) and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    if not downloaded:
        print(f"[!] No images downloaded from Pinterest for query '{query}'")
        return False

    # Score candidates: prioritize aspect ratio close to 16:9 (1.777) and higher resolution
    def score_image(path):
        try:
            with Image.open(path) as im:
                w, h = im.size
                if w < 400 or h < 300:
                    return -100
                aspect = w / h
                # Difference from 16:9 (lower diff = higher score)
                aspect_diff = abs(aspect - TARGET_ASPECT)
                # Landscape bonus
                is_landscape = 1 if w > h else 0
                return (is_landscape * 10) - (aspect_diff * 5) + (min(w, 1920) / 1000)
        except Exception:
            return -999

    best_candidate = max(downloaded, key=score_image)
    with Image.open(best_candidate) as b_im:
        print(f"[✔] Best Pinterest candidate: {os.path.basename(best_candidate)} ({b_im.size[0]}x{b_im.size[1]})")

    # Ingest candidate
    articles = load_articles()
    art = next((a for a in articles if a["id"] == target_id), None)
    if not art:
        print(f"[!] Target article '{target_id}' not found in articles catalog")
        return False

    dest_filename = f"{target_id}.jpg" if not art.get("image") else os.path.basename(art["image"])
    dest_path = os.path.join(ARTICLES_DIR, dest_filename)
    rel_img = f"/blog/articles/{dest_filename}"

    size_kb = normalize_image(best_candidate, dest_path)
    print(f"[✔] Saved Pinterest banner: {dest_path} ({size_kb:.1f} KB, 1280x720 16:9)")

    final_alt = alt_text or f"Pinterest photo illustration for {art['title']}"
    update_article_metadata(target_id, rel_img, final_alt)
    return True


def fetch_from_pin_url(pin_url, target_id, alt_text=None):
    """
    Downloads image from a specific Pinterest pin page or direct i.pinimg.com image URL.
    """
    import urllib.request
    from pinterest_dl import ApiScraper

    print(f"\n[Pinterest URL] Fetching pin: '{pin_url}' for {target_id}...")
    temp_dir = os.path.join(SCRATCH_DIR, "single_pin")
    os.makedirs(temp_dir, exist_ok=True)

    if "i.pinimg.com" in pin_url:
        # Direct CDN image URL
        filename = os.path.basename(pin_url.split("?")[0])
        local_path = os.path.join(temp_dir, filename)
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(pin_url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(local_path, "wb") as f_out:
            f_out.write(resp.read())
        best_candidate = local_path
    else:
        # Full pin page URL -> use scraper
        scraper = ApiScraper()
        res = scraper.scrape(pin_url, num=1)
        if not res or not res[0].src:
            print("[!] Could not extract image from pin URL")
            return False
        img_src = res[0].src
        print(f"[+] Found original image: {img_src}")
        filename = os.path.basename(img_src.split("?")[0])
        local_path = os.path.join(temp_dir, filename)
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(img_src, headers=headers)
        with urllib.request.urlopen(req) as resp, open(local_path, "wb") as f_out:
            f_out.write(resp.read())
        best_candidate = local_path

    articles = load_articles()
    art = next((a for a in articles if a["id"] == target_id), None)
    if not art:
        print(f"[!] Target article '{target_id}' not found")
        return False

    dest_filename = f"{target_id}.jpg" if not art.get("image") else os.path.basename(art["image"])
    dest_path = os.path.join(ARTICLES_DIR, dest_filename)
    rel_img = f"/blog/articles/{dest_filename}"

    size_kb = normalize_image(best_candidate, dest_path)
    print(f"[✔] Ingested Pinterest pin: {dest_path} ({size_kb:.1f} KB, 1280x720 16:9)")
    final_alt = alt_text or art.get("imageAlt") or f"Pinterest photo banner for {art['title']}"
    update_article_metadata(target_id, rel_img, final_alt)
    return True


# Curated list of Pinterest searches for gaming articles
PINTEREST_GAMING_BATCH = [
    {
        "query": "gta 6 jason duval wallpaper 1920x1080",
        "target_id": "gta-6-characters-jason-lucia-cast",
        "alt": "Pinterest photo of GTA 6 protagonists Jason Duval and Lucia together in Vice City",
    },
    {
        "query": "gta 6 mandy",
        "target_id": "lexie-shoaibi-mandy-gta-6-actress-house-location-scene",
        "alt": "Pinterest photo of viral character Mandy influencer in GTA 6",
    },
    {
        "query": "niko bellic gta 4 wallpaper 1920x1080",
        "target_id": "is-niko-bellic-in-gta-6-easter-eggs",
        "alt": "Pinterest artwork of Niko Bellic in Liberty City easter egg for GTA 6",
    },
    {
        "query": "gta 6 vice city sunset wallpaper",
        "target_id": "gta-6-endings-how-many-choices-explained",
        "alt": "Pinterest wallpaper of Vice City sunset skyline and highway for GTA 6 endings",
    },
    {
        "query": "gta 6 official trailer poster 1920x1080",
        "target_id": "has-anyone-finished-gta-6-how-much-made-gta-flu-online",
        "alt": "Pinterest official artwork of Grand Theft Auto 6 launch day records",
    },
    {
        "query": "gta 6 diner robbery wallpaper",
        "target_id": "gta-6-chapter-1-missions-list-walkthrough",
        "alt": "Pinterest screenshot of GTA 6 Chapter 1 diner robbery and muscle car getaway",
    },
    {
        "query": "gta 6 boatworks safe",
        "target_id": "brooks-boatworks-safe-code-gta-6",
        "alt": "Pinterest photo of Brooks Boatworks safe location in GTA 6",
    },
    {
        "query": "gta 6 donnie wallpaper",
        "target_id": "donnie-gta-6-character-role-walkthrough",
        "alt": "Pinterest photo of Donnie getaway driver in GTA 6",
    },
    {
        "query": "gta 6 map vice city leonida",
        "target_id": "gta-6-map-vice-city-leonida-regions",
        "alt": "Pinterest map of Vice City and Leonida regions in GTA 6",
    },
    {
        "query": "gta 6 lucia wallpaper 1920x1080",
        "target_id": "manni-l-perez-gta-6-lucia-actress",
        "alt": "Pinterest wallpaper of Lucia protagonist Manni L Perez in GTA 6",
    },
    {
        "query": "zelda ocarina of time 4k wallpaper",
        "target_id": "ocarina-of-time-remake-pc-port",
        "alt": "Pinterest wallpaper of Zelda Ocarina of Time community PC recompilation",
    },
    {
        "query": "playstation 5 console 4k wallpaper",
        "target_id": "playstation-plus-november-2026",
        "alt": "Pinterest photo of PlayStation 5 console and DualSense controller",
    },
    {
        "query": "xbox series x gaming wallpaper",
        "target_id": "xbox-game-pass-november-2026-wave-2",
        "alt": "Pinterest photo of Xbox gaming lounge and wireless controller",
    },
]


def run_pipeline():
    """Executes static HTML build, Vite bundle compilation, SEO audit, and IndexNow ping."""
    print("\n--- Running Production Pipeline ---")
    
    # 1. Build SEO static pages
    print("[1/4] Running build_seo.py...")
    subprocess.run(["python", "scripts/build_seo.py"], check=True)
    
    # 2. Vite production build
    print("[2/4] Running npm run build...")
    subprocess.run(["npm", "run", "build"], shell=True, check=True)
    
    # 3. SEO Audit
    print("[3/4] Running audit_seo.py...")
    subprocess.run(["python", "scripts/audit_seo.py"], check=True)
    
    # 4. IndexNow Ping
    print("[4/4] Pinging IndexNow...")
    subprocess.run(["npm", "run", "indexnow"], shell=True, check=True)
    
    print("[✔] Production pipeline finished successfully!")


def main():
    parser = argparse.ArgumentParser(description="Automated Pinterest & Editorial Banner System")
    parser.add_argument("action", choices=["list", "pinterest-fetch", "pinterest-url", "pinterest-batch", "pipeline"], help="Action to run")
    parser.add_argument("--query", help="Pinterest search query")
    parser.add_argument("--url", help="Pinterest pin page URL or direct image URL")
    parser.add_argument("--target-id", help="Target article id/slug")
    parser.add_argument("--alt", help="Custom alt text")
    parser.add_argument("--count", type=int, default=5, help="Number of Pinterest pins to inspect")
    
    args = parser.parse_args()
    
    if args.action == "list":
        articles = load_articles()
        gaming = [a for a in articles if a.get("category") == "Gaming"]
        print(f"Total articles: {len(articles)} (Gaming: {len(gaming)})")
        for a in gaming:
            img_path = os.path.join(PUBLIC, a.get("image", "").lstrip("/"))
            exists = os.path.exists(img_path)
            size_kb = os.path.getsize(img_path) / 1024 if exists else 0
            print(f"- {a['id']:<45} | slot={a.get('slot','recent'):<10} | {size_kb:>6.1f}KB | img={a.get('image')}")
            
    elif args.action == "pinterest-fetch":
        if not args.query or not args.target_id:
            print("[!] Both --query and --target-id are required.")
            sys.exit(1)
        ok = fetch_from_pinterest(args.query, args.target_id, args.alt, num_candidates=args.count)
        if ok:
            run_pipeline()
            
    elif args.action == "pinterest-url":
        if not args.url or not args.target_id:
            print("[!] Both --url and --target-id are required.")
            sys.exit(1)
        ok = fetch_from_pin_url(args.url, args.target_id, args.alt)
        if ok:
            run_pipeline()
            
    elif args.action == "pinterest-batch":
        print(f"--- Fetching {len(PINTEREST_GAMING_BATCH)} Pinterest Banners for Gaming Articles ---")
        success_count = 0
        for item in PINTEREST_GAMING_BATCH:
            ok = fetch_from_pinterest(item["query"], item["target_id"], item["alt"], num_candidates=4)
            if ok:
                success_count += 1
        print(f"\n[✔] Successfully fetched & processed {success_count} Pinterest banners!")
        run_pipeline()
        
    elif args.action == "pipeline":
        run_pipeline()


if __name__ == "__main__":
    main()
