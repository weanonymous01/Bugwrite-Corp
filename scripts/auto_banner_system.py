#!/usr/bin/env python3
"""
Automated Editorial Banner System for Bugwrite (Bugwrite-Corp)

Features:
- Analyzes article titles, categories, and keywords to identify primary characters and motifs
- Auto-generates high-definition prompts for 16:9 cinematic/editorial banners
- Crops/pads and normalizes any input image (AI generated, editorial photo, or download) to strict 16:9 (1280x720)
- Applies progressive JPEG compression with MozJPEG-equivalent settings (<120 KB target)
- Ingests new images into public/blog/articles/<slug>.jpg
- Updates public/blog/articles-data.js image pointers and SEO-optimized imageAlt tags
- Runs static build, SEO audit, and IndexNow ping pipeline
"""

import os
import sys
import json
import re
import argparse
import subprocess
from datetime import datetime
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
ARTICLES_DIR = os.path.join(PUBLIC, "blog", "articles")
DATA_JS = os.path.join(PUBLIC, "blog", "articles-data.js")
BRAIN_DIR = os.path.expandvars(r"%USERPROFILE%\.gemini\antigravity\brain")

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


def normalize_image(source_path, dest_path, quality=86):
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
            # 40% top weight for character portraits to avoid cutting foreheads
            top = max(0, int((orig_h - new_h) * 0.40))
            img = img.crop((0, top, orig_w, top + new_h))

        # High quality Lanczos downsample to 1280x720
        img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

        # Save optimized JPEG
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


def scan_and_ingest_artifacts():
    """
    Scans the conversation brain directory for any generated images,
    matches them against known banner target slugs, normalizes them to 1280x720,
    and updates articles-data.js.
    """
    articles = load_articles()
    art_by_id = {a["id"]: a for a in articles}

    # Map filename hints to article IDs and descriptive alt texts
    MAPPINGS = [
        {
            "match_patterns": ["jason_lucia", "gta6_jason", "characters_jason"],
            "article_id": "gta-6-characters-jason-lucia-cast",
            "filename": "gta-6-characters-jason-lucia-cast.jpg",
            "alt": "GTA 6 protagonists Jason Duval and Lucia together on Leonida coastal highway at sunset",
        },
        {
            "match_patterns": ["mandy", "lexie_shoaibi", "shoaibi"],
            "article_id": "lexie-shoaibi-mandy-gta-6-actress-house-location-scene",
            "filename": "gta6-mandy-lexie-shoaibi.jpg",
            "alt": "Lexie Shoaibi viral character Mandy at Starfish Island luxury waterfront mansion in GTA 6",
        },
        {
            "match_patterns": ["niko", "niko_bellic"],
            "article_id": "is-niko-bellic-in-gta-6-easter-eggs",
            "filename": "gta6-niko-bellic.jpg",
            "alt": "Niko Bellic Liberty City easter egg and returning character clues in Grand Theft Auto 6",
        },
        {
            "match_patterns": ["endings", "choices"],
            "article_id": "gta-6-endings-how-many-choices-explained",
            "filename": "gta6-endings.jpg",
            "alt": "GTA 6 campaign finale branching story choices and character endings breakdown",
        },
        {
            "match_patterns": ["launch_records", "has_anyone_finished"],
            "article_id": "has-anyone-finished-gta-6-how-much-made-gta-flu-online",
            "filename": "gta6-launch-records.jpg",
            "alt": "GTA 6 launch day sales records completion times and GTA Flu workplace phenomenon",
        },
        {
            "match_patterns": ["chapter1", "chapter_1", "getaway"],
            "article_id": "gta-6-chapter-1-missions-list-walkthrough",
            "filename": "gta6-chapter-1.jpg",
            "alt": "GTA 6 Chapter 1 prologue missions list diner robbery and highway getaway walkthrough",
        },
        {
            "match_patterns": ["brooks_safe", "safe_code", "boatworks"],
            "article_id": "brooks-boatworks-safe-code-gta-6",
            "filename": "gta6-safe-code.jpg",
            "alt": "Brooks Boatworks industrial heavy safe combination dial and loot location in GTA 6",
        },
        {
            "match_patterns": ["donnie", "donnie_driver"],
            "article_id": "donnie-gta-6-character-role-walkthrough",
            "filename": "gta6-donnie.jpg",
            "alt": "Donnie character in GTA 6 early heist getaway driver role and mission walkthrough",
        },
        {
            "match_patterns": ["ocarina", "switch_2"],
            "article_id": "ocarina-of-time-remake-pc-port",
            "filename": "ocarina-pc-port.jpg",
            "alt": "Zelda Ocarina of Time community PC recompilation setup running with high resolution graphics",
        },
        {
            "match_patterns": ["playstation_plus", "ps_plus"],
            "article_id": "playstation-plus-november-2026",
            "filename": "playstation-plus.jpg",
            "alt": "PlayStation Plus November 2026 monthly game lineup controller and console showcase",
        },
        {
            "match_patterns": ["xbox_game_pass", "game_pass"],
            "article_id": "xbox-game-pass-november-2026-wave-2",
            "filename": "xbox-game-pass.jpg",
            "alt": "Xbox Game Pass late November game lineup streaming setup and wireless controller",
        },
        {
            "match_patterns": ["release_time", "launch_event", "playable"],
            "article_id": "when-is-gta-6-playable-release-times",
            "filename": "gta6-release-time.jpg",
            "alt": "Global midnight launch celebration outside premier electronics showcase for Grand Theft Auto 6",
        },
        {
            "match_patterns": ["map_leonida", "vice_city_map", "leonida_regions"],
            "article_id": "gta-6-map-vice-city-leonida-regions",
            "filename": "gta-6-map-vice-city-leonida-regions.jpg",
            "alt": "Aerial panoramic map view of Vice City skyline, Florida Keys, and Leonida wetlands in GTA 6",
        },
        {
            "match_patterns": ["screenshots_weather", "screenshots_gallery", "downpour"],
            "article_id": "gta-6-screenshots-gallery-weather",
            "filename": "gta6-screenshots.jpg",
            "alt": "Tropical downpour reflecting neon storefront signage and swaying palm trees on Vice City boulevard",
        },
        {
            "match_patterns": ["lucia_actress", "manni_l_perez", "perez"],
            "article_id": "manni-l-perez-gta-6-lucia-actress",
            "filename": "manni-l-perez-gta-6-lucia-actress.jpg",
            "alt": "Manni L Perez protagonist Lucia portrait looking out across Vice City oceanfront at sunset",
        },
    ]

    # Search through all subdirectories of BRAIN_DIR for matching images
    found_count = 0
    for root, _, files in os.walk(BRAIN_DIR):
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue
            f_lower = f.lower()
            for mapping in MAPPINGS:
                matched = any(p in f_lower for p in mapping["match_patterns"])
                if matched:
                    src = os.path.join(root, f)
                    dest = os.path.join(ARTICLES_DIR, mapping["filename"])
                    rel_img = f"/blog/articles/{mapping['filename']}"
                    
                    print(f"[*] Processing {f} -> {mapping['filename']}...")
                    size_kb = normalize_image(src, dest)
                    print(f"    Saved: {dest} ({size_kb:.1f} KB, 1280x720 16:9)")

                    if mapping["article_id"] in art_by_id:
                        update_article_metadata(mapping["article_id"], rel_img, mapping["alt"])
                    found_count += 1
                    break

    print(f"[✔] Total matched & ingested images: {found_count}")


def generate_suggested_prompts():
    """Generates 16:9 editorial prompts for any gaming article in catalog."""
    articles = load_articles()
    gaming = [a for a in articles if a.get("category") == "Gaming"]
    
    print(f"\n--- Suggested High-Resolution 16:9 Prompts for Gaming Articles ({len(gaming)} total) ---")
    for i, a in enumerate(gaming[:10], 1):
        print(f"\n[{i}] Article: {a['title']}")
        print(f"    Slug: {a['id']}")
        print(f"    Keywords: {', '.join(a.get('keywords', [])[:4])}")
        print(f"    16:9 Prompt Brief: Cinematic photorealistic video game editorial photography illustrating {a['title']}. High detail, vibrant atmospheric lighting, 16:9 landscape framing, no text, no logos, no watermarks, no HUD.")


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
    parser = argparse.ArgumentParser(description="Automated Banner Pipeline for Bugwrite")
    parser.add_argument("action", choices=["list", "prompts", "process-artifacts", "ingest", "pipeline"], help="Action to run")
    parser.add_argument("--source", help="Source image path for ingest action")
    parser.add_argument("--target-id", help="Target article id/slug for ingest action")
    parser.add_argument("--alt", help="Descriptive imageAlt text for ingest action")
    
    args = parser.parse_args()
    
    if args.action == "list":
        articles = load_articles()
        gaming = [a for a in articles if a.get("category") == "Gaming"]
        print(f"Total articles: {len(articles)} (Gaming: {len(gaming)})")
        for a in gaming:
            img_path = os.path.join(PUBLIC, a.get("image", "").lstrip("/"))
            exists = os.path.exists(img_path)
            size_kb = os.path.getsize(img_path) / 1024 if exists else 0
            print(f"- {a['id']:<45} | exists={exists:<5} | {size_kb:>6.1f}KB | img={a.get('image')}")
            
    elif args.action == "prompts":
        generate_suggested_prompts()
        
    elif args.action == "process-artifacts":
        scan_and_ingest_artifacts()
        
    elif args.action == "ingest":
        if not args.source or not args.target_id:
            print("[!] Both --source and --target-id are required for ingest.")
            sys.exit(1)
        dest_filename = f"{args.target_id}.jpg"
        dest_path = os.path.join(ARTICLES_DIR, dest_filename)
        size_kb = normalize_image(args.source, dest_path)
        print(f"[✔] Ingested {args.source} -> {dest_path} ({size_kb:.1f} KB)")
        alt = args.alt or f"Editorial banner illustration for {args.target_id}"
        update_article_metadata(args.target_id, f"/blog/articles/{dest_filename}", alt)
        
    elif args.action == "pipeline":
        scan_and_ingest_artifacts()
        run_pipeline()


if __name__ == "__main__":
    main()
