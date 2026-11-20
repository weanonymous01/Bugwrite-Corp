#!/usr/bin/env python3
"""
Automated Multi-Category Pinterest & Editorial Banner System for Bugwrite (Bugwrite-Corp)

Features:
- Direct Pinterest search and downloading using internal Pinterest API (pinterest-dl)
- Covers all 4 publication categories: Gaming, Big Tech, Cybersecurity/Security, and Business
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
import time
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


def fetch_from_pinterest(query, target_id, alt_text=None, num_candidates=4):
    """
    Searches Pinterest for the given query, downloads candidate images,
    selects the best widescreen / highest quality candidate, crops to 1280x720,
    and updates the article.
    """
    from pinterest_dl import ApiScraper

    print(f"\n[Pinterest] Searching: '{query}' for '{target_id}'...")
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
                aspect_diff = abs(aspect - TARGET_ASPECT)
                is_landscape = 1 if w > h else 0
                return (is_landscape * 10) - (aspect_diff * 5) + (min(w, 1920) / 1000)
        except Exception:
            return -999

    best_candidate = max(downloaded, key=score_image)
    with Image.open(best_candidate) as b_im:
        print(f"[✔] Best Pinterest candidate: {os.path.basename(best_candidate)} ({b_im.size[0]}x{b_im.size[1]})")

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
    """Downloads image from a specific Pinterest pin page or direct i.pinimg.com image URL."""
    import urllib.request
    from pinterest_dl import ApiScraper

    print(f"\n[Pinterest URL] Fetching pin: '{pin_url}' for {target_id}...")
    temp_dir = os.path.join(SCRATCH_DIR, "single_pin")
    os.makedirs(temp_dir, exist_ok=True)

    if "i.pinimg.com" in pin_url:
        filename = os.path.basename(pin_url.split("?")[0])
        local_path = os.path.join(temp_dir, filename)
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(pin_url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(local_path, "wb") as f_out:
            f_out.write(resp.read())
        best_candidate = local_path
    else:
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


# ==============================================================================
# BATCH DEFINITIONS ACROSS ALL CATEGORIES
# ==============================================================================

PINTEREST_TECH_BATCH = [
    {
        "query": "apple store macbook iphone aesthetic wallpaper 1920x1080",
        "target_id": "apple-outage",
        "alt": "Pinterest photo of modern Apple MacBook and iPhone workspace setup",
    },
    {
        "query": "microsoft office modern tech desk aesthetic wallpaper",
        "target_id": "microsoft-outlook-teams-copilot-outage",
        "alt": "Pinterest photo of Microsoft modern enterprise workspace with dual monitors",
    },
    {
        "query": "google workspace minimal desk setup aesthetic wallpaper",
        "target_id": "gmail-outage-rumors-apple-disruption",
        "alt": "Pinterest photo of clean modern desk with laptop accessing Google services",
    },
    {
        "query": "cloud computing server network fiber optic cables",
        "target_id": "why-so-many-internet-outages-2026",
        "alt": "Pinterest photo of enterprise cloud fiber optic network cables and servers",
    },
    {
        "query": "cloud computing infrastructure global network globe",
        "target_id": "cloudflare-aws-azure-internet-dependence",
        "alt": "Pinterest graphic of global internet cloud infrastructure and server nodes",
    },
    {
        "query": "artificial intelligence glowing neural network 4k wallpaper",
        "target_id": "openai-gpt-6-2-astra-sol-cyber-2026",
        "alt": "Pinterest aesthetic visual of artificial neural network and machine learning",
    },
    {
        "query": "software developer mechanical keyboard dual monitor coding setup",
        "target_id": "best-ai-coding-tools-2026",
        "alt": "Pinterest desk setup of software developer coding on widescreen monitors",
    },
    {
        "query": "software engineering terminal code dark mode wallpaper",
        "target_id": "what-are-coding-agents-developers",
        "alt": "Pinterest photo of programmer terminal workstation running automated scripts",
    },
    {
        "query": "autonomous robotics artificial intelligence futuristic laboratory",
        "target_id": "ai-agents-explained-how-they-work",
        "alt": "Pinterest concept photo of autonomous AI agent technology in research lab",
    },
    {
        "query": "server rack network cables ethernet switchboard",
        "target_id": "how-to-check-if-website-is-down",
        "alt": "Pinterest photo of network switchboard cables and data center hardware",
    },
    {
        "query": "windows 11 modern minimal desktop workspace setup",
        "target_id": "windows-11-common-errors-fixes",
        "alt": "Pinterest photo of clean minimalist Windows 11 desktop workspace",
    },
    {
        "query": "google pixel android smartphone sleek display wallpaper",
        "target_id": "android-17-features-changes-devices",
        "alt": "Pinterest aesthetic photo of modern Android flagship smartphone",
    },
    {
        "query": "apple iphone futuristic design concept wallpaper",
        "target_id": "ios-27-features-siri-liquid-glass",
        "alt": "Pinterest aesthetic concept design of next generation Apple iOS smartphone",
    },
    {
        "query": "electric power grid substation energy infrastructure",
        "target_id": "why-ai-data-centers-consume-electricity",
        "alt": "Pinterest photo of high voltage power grid infrastructure supporting data centers",
    },
    {
        "query": "microchip silicon wafer semiconductor processor macro",
        "target_id": "what-are-ai-chips-why-companies-fight",
        "alt": "Pinterest macro photograph of high-tech silicon AI microchip processor",
    },
    {
        "query": "minimalist creative productivity desk notebook coffee laptop",
        "target_id": "best-free-ai-tools-productivity-2026",
        "alt": "Pinterest photo of minimalist everyday productivity workspace with laptop",
    },
]

PINTEREST_SECURITY_BATCH = [
    {
        "query": "cyber security operations room blue screens wallpaper 1920x1080",
        "target_id": "artex-ai-cyber-framework",
        "alt": "Pinterest photo of enterprise cybersecurity operations center with alert monitors",
    },
    {
        "query": "server room data center blue led lighting perspective",
        "target_id": "java4shell-cve-2026-114938",
        "alt": "Pinterest photo of data center server rack corridor with blue LED indicators",
    },
    {
        "query": "fbi headquarters building columns washington dc",
        "target_id": "fbi-warning-today-facestealer-artex",
        "alt": "Pinterest photo of federal government building architectural columns",
    },
    {
        "query": "cyber security code vulnerability matrix wallpaper",
        "target_id": "ai-finding-software-vulnerabilities-faster",
        "alt": "Pinterest visual of source code and security vulnerability analysis",
    },
    {
        "query": "cyber security digital padlock binary keyhole wallpaper",
        "target_id": "what-is-a-zero-day-vulnerability",
        "alt": "Pinterest graphic of glowing digital security lock and zero day protection",
    },
    {
        "query": "ethical hacker dark room computer monitors coding",
        "target_id": "how-hackers-exploit-unpatched-software",
        "alt": "Pinterest photo of cybersecurity researcher working in dark room with terminals",
    },
    {
        "query": "hardware security key yubikey laptop keyboard macro",
        "target_id": "best-password-managers-2026",
        "alt": "Pinterest photo of hardware authentication key plugged into modern laptop",
    },
    {
        "query": "laptop coffee shop public wifi security privacy",
        "target_id": "best-vpn-services-windows-2026",
        "alt": "Pinterest photo of laptop user connected to public Wi-Fi network in cafe",
    },
    {
        "query": "digital cybersecurity shield firewall network protection",
        "target_id": "how-ransomware-works-business-protection",
        "alt": "Pinterest concept of digital firewall security shield protecting business data",
    },
    {
        "query": "smartphone privacy settings lock screen protection",
        "target_id": "is-personal-data-used-to-train-ai",
        "alt": "Pinterest photo of smartphone privacy and security settings interface",
    },
    {
        "query": "meta facebook headquarters modern office building",
        "target_id": "facebook-italy-privacy-fine-multiple-profiles",
        "alt": "Pinterest photo of modern corporate technology campus glass exterior",
    },
]

PINTEREST_BUSINESS_BATCH = [
    {
        "query": "nvidia headquarters architecture silicon valley building",
        "target_id": "harvey-jones-nvidia-chair",
        "alt": "Pinterest photo of modern Silicon Valley glass corporate headquarters",
    },
    {
        "query": "nvidia rtx ai chip graphics card technology",
        "target_id": "nvidia-q3-fy27-earnings-115-billion",
        "alt": "Pinterest photo of cutting-edge Nvidia hardware silicon architecture",
    },
    {
        "query": "nasdaq times square wall street stock exchange display",
        "target_id": "anthropic-ipo-nasdaq-ant-2026",
        "alt": "Pinterest photo of Times Square financial market stock exchange displays",
    },
    {
        "query": "salesforce tower san francisco skyline dusk sunset",
        "target_id": "salesforce-copilotforce-layoffs-november-2026",
        "alt": "Pinterest skyline photo of Salesforce Tower overlooking San Francisco at dusk",
    },
    {
        "query": "amazon aws cloud fulfillment center architecture",
        "target_id": "amazon-down-aws-us-east-1-friction",
        "alt": "Pinterest photo of modern cloud logistics and enterprise data infrastructure",
    },
    {
        "query": "lottery mega millions winning ticket cash jackpot",
        "target_id": "mega-millions-drawing-november-17-2026",
        "alt": "Pinterest photo of winning lottery jackpot tickets and numbers",
    },
    {
        "query": "google cloud headquarters silicon valley modern campus",
        "target_id": "amazon-google-ai-investment-2026",
        "alt": "Pinterest photo of modern technology corporate campus in California",
    },
    {
        "query": "microchip semiconductor fabrication cleanroom asml",
        "target_id": "us-ai-chip-export-restrictions-2026",
        "alt": "Pinterest photo of advanced cleanroom semiconductor fabrication manufacturing",
    },
    {
        "query": "stock market trading floor screens financial charts",
        "target_id": "is-ai-boom-becoming-a-bubble-2026",
        "alt": "Pinterest photo of financial trading terminals and stock market analytics",
    },
    {
        "query": "wall street new york stock exchange financial district",
        "target_id": "why-tech-stocks-falling-november-2026",
        "alt": "Pinterest photo of Wall Street financial district architectural perspective",
    },
    {
        "query": "massive enterprise data center server room perspective",
        "target_id": "ai-industry-data-center-spending-2026",
        "alt": "Pinterest photo of hyperscale data center facility with server corridors",
    },
    {
        "query": "liquid cooling server rack high performance computing",
        "target_id": "ai-infrastructure-costs-startups-2026",
        "alt": "Pinterest photo of advanced liquid cooling server rack in AI facility",
    },
    {
        "query": "biotech laboratory genetics molecular biology research",
        "target_id": "isomorphic-labs-5-billion-series-c",
        "alt": "Pinterest photo of state of the art biotechnology and pharmaceutical lab",
    },
    {
        "query": "modern tech startup loft office glass conference room",
        "target_id": "ai-startups-changing-software-model",
        "alt": "Pinterest photo of modern technology startup workspace with glass meeting room",
    },
    {
        "query": "modern saas dashboard analytics sleek laptop screen",
        "target_id": "why-saas-companies-adding-ai-features",
        "alt": "Pinterest photo of software executive inspecting SaaS metrics dashboard",
    },
    {
        "query": "fintech executive corporate office desk laptop",
        "target_id": "what-is-an-ai-agent-business",
        "alt": "Pinterest photo of modern executive desk with financial intelligence tools",
    },
    {
        "query": "hyperscale data center building exterior at twilight",
        "target_id": "cloud-computing-competing-ai-customers",
        "alt": "Pinterest architectural photo of modern enterprise cloud computing facility",
    },
    {
        "query": "corporate executive boardroom meeting glass table",
        "target_id": "business-impact-cloud-software-outages",
        "alt": "Pinterest photo of executive boardroom overlooking city skyline",
    },
    {
        "query": "cyber security spending enterprise corporate budget",
        "target_id": "cybersecurity-spending-business-priority",
        "alt": "Pinterest photo of corporate leadership reviewing enterprise security strategy",
    },
    {
        "query": "financial audit spreadsheet cyber security data breach",
        "target_id": "how-data-breaches-affect-companies-financially",
        "alt": "Pinterest photo of financial audit reports and cybersecurity risk metrics",
    },
    {
        "query": "startup founder working desk minimal coffee laptop",
        "target_id": "cost-to-build-ai-saas-startup-2026",
        "alt": "Pinterest photo of startup founder workstation with planning documents",
    },
    {
        "query": "modern small business coffee shop counter point of sale",
        "target_id": "best-crm-software-small-businesses-2026",
        "alt": "Pinterest photo of modern small business retail counter with digital POS",
    },
    {
        "query": "creative entrepreneur workspace macbook air minimalist",
        "target_id": "best-ai-tools-small-business-owners",
        "alt": "Pinterest photo of clean creative entrepreneur desk with notebook and laptop",
    },
    {
        "query": "silicon valley tech corporate campus aerial twilight",
        "target_id": "why-tech-companies-restructuring-2026",
        "alt": "Pinterest aerial twilight photo of major technology corporate campus",
    },
    {
        "query": "venture capital partner meeting glass modern office",
        "target_id": "vc-evaluating-ai-startups-2026",
        "alt": "Pinterest photo of venture capital investors in modern conference room",
    },
    {
        "query": "secure enterprise private cloud server infrastructure",
        "target_id": "why-companies-invest-private-ai-models",
        "alt": "Pinterest photo of dedicated private cloud servers in enterprise facility",
    },
    {
        "query": "supercomputer liquid cooling server blades high performance",
        "target_id": "cost-of-running-large-ai-model",
        "alt": "Pinterest photo of advanced supercomputer cluster computing architecture",
    },
    {
        "query": "semiconductor cleanroom silicon wafer manufacturing",
        "target_id": "us-export-controls-global-semiconductors",
        "alt": "Pinterest photo of high-tech semiconductor cleanroom manufacturing line",
    },
]

PINTEREST_GAMING_REMAINING_BATCH = [
    {
        "query": "gta 6 pc gaming setup 4k wallpaper 1920x1080",
        "target_id": "gta-6-pc-release-date-windows",
        "alt": "Pinterest photo of high-end PC gaming battle station setup",
    },
    {
        "query": "gta 6 steelbook collector box artwork",
        "target_id": "gta-6-standard-vs-ultimate-edition",
        "alt": "Pinterest photo of video game special collector edition packaging",
    },
    {
        "query": "ps5 ssd nvme storage expansion gaming console",
        "target_id": "gta-6-download-size-storage-guide",
        "alt": "Pinterest photo of PlayStation 5 console storage expansion setup",
    },
    {
        "query": "the game awards gold trophy gaming ceremony",
        "target_id": "gta-6-eight-game-awards-nominations",
        "alt": "Pinterest photo of The Game Awards golden statue and ceremony stage",
    },
    {
        "query": "the game awards stage lights orchestra gaming",
        "target_id": "the-game-awards-2026-nominees",
        "alt": "Pinterest photo of premier video game awards ceremony live broadcast",
    },
    {
        "query": "gta 6 vice city speedboat turquoise ocean wallpaper",
        "target_id": "gta-6-gameplay-features-details",
        "alt": "Pinterest photo of luxury speedboat cruising turquoise Vice City waters",
    },
    {
        "query": "gta 5 gta 6 comparison graphics wallpaper",
        "target_id": "gta-6-vs-gta-5-biggest-changes",
        "alt": "Pinterest side by side visual of open world game graphics evolution",
    },
    {
        "query": "game of the year gold award trophy gaming",
        "target_id": "can-gta-6-win-goty-before-release",
        "alt": "Pinterest photo of Game of the Year prestigious trophy award",
    },
    {
        "query": "arc raiders game winter snow mech robot wallpaper",
        "target_id": "arc-raiders-update-2-6-0-cold-snap",
        "alt": "Pinterest wallpaper of ARC Raiders mech in frozen winter landscape",
    },
    {
        "query": "arc raiders survival shooter game wallpaper",
        "target_id": "arc-raiders-beginner-tips-survival",
        "alt": "Pinterest wallpaper of cooperative survival extraction shooter combat",
    },
    {
        "query": "playstation 5 game disc collection cases",
        "target_id": "best-ps5-games-2026",
        "alt": "Pinterest photo of top PlayStation 5 game collection and case artwork",
    },
    {
        "query": "league of legends champion splash art 4k wallpaper",
        "target_id": "league-of-legends-patch-26-23-notes",
        "alt": "Pinterest high resolution splash art of League of Legends champion",
    },
    {
        "query": "wireless gaming headset rgb desk setup wallpaper",
        "target_id": "best-gaming-headsets-2026",
        "alt": "Pinterest photo of premium gaming headset on audio stand with RGB lighting",
    },
    {
        "query": "nvidia geforce rtx graphics card modern gaming rig",
        "target_id": "nvidia-rtx-5090-prices-shortage-2026",
        "alt": "Pinterest photo of flagship Nvidia GeForce RTX graphics card in custom PC",
    },
    {
        "query": "half life gordon freeman crowbar wallpaper",
        "target_id": "half-life-3-game-awards-2026-hlx",
        "alt": "Pinterest atmospheric artwork of iconic sci-fi shooter protagonist",
    },
    {
        "query": "tomb raider lara croft ancient ruins wallpaper",
        "target_id": "tomb-raider-legacy-of-atlantis-2027-delay",
        "alt": "Pinterest cinematic wallpaper of ancient archaeological ruins exploration",
    },
    {
        "query": "civilization strategy game hex map world",
        "target_id": "firaxis-layoffs-civilization-xcom-2026",
        "alt": "Pinterest screenshot of turn based historical strategy game world map",
    },
]


def run_batch_list(batch_list, category_name):
    """Processes a list of Pinterest downloads with graceful error handling and delay."""
    print(f"\n================================================================================")
    print(f"  PROCESSING {len(batch_list)} PINTEREST BANNERS FOR: {category_name.upper()}")
    print(f"================================================================================")
    success = 0
    for idx, item in enumerate(batch_list, 1):
        print(f"\n[{idx}/{len(batch_list)}] Target: {item['target_id']}")
        try:
            ok = fetch_from_pinterest(item["query"], item["target_id"], item["alt"], num_candidates=3)
            if ok:
                success += 1
            time.sleep(0.15)
        except Exception as e:
            print(f"[!] Error on {item['target_id']}: {e}")
            continue

    print(f"\n[✔] Completed {category_name}: {success}/{len(batch_list)} banners updated from Pinterest!")
    return success


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
    parser = argparse.ArgumentParser(description="Multi-Category Pinterest Banner System")
    parser.add_argument("action", choices=["list", "pinterest-fetch", "pinterest-url", "pinterest-category", "pipeline"], help="Action to run")
    parser.add_argument("--query", help="Pinterest search query")
    parser.add_argument("--url", help="Pinterest pin page URL or direct image URL")
    parser.add_argument("--target-id", help="Target article id/slug")
    parser.add_argument("--category", choices=["tech", "security", "business", "gaming-remaining", "all"], help="Category to process")
    parser.add_argument("--alt", help="Custom alt text")
    parser.add_argument("--count", type=int, default=4, help="Number of Pinterest pins to inspect")
    
    args = parser.parse_args()
    
    if args.action == "list":
        articles = load_articles()
        print(f"Total articles in catalog: {len(articles)}")
        for a in articles:
            img_path = os.path.join(PUBLIC, a.get("image", "").lstrip("/"))
            exists = os.path.exists(img_path)
            size_kb = os.path.getsize(img_path) / 1024 if exists else 0
            print(f"- {a['id']:<45} | {a.get('category','News'):<14} | {size_kb:>6.1f}KB | img={a.get('image')}")
            
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
            
    elif args.action == "pinterest-category":
        cat = args.category or "all"
        total = 0
        if cat in ("tech", "all"):
            total += run_batch_list(PINTEREST_TECH_BATCH, "Big Tech")
        if cat in ("security", "all"):
            total += run_batch_list(PINTEREST_SECURITY_BATCH, "Cybersecurity & Security")
        if cat in ("business", "all"):
            total += run_batch_list(PINTEREST_BUSINESS_BATCH, "Business & Enterprise")
        if cat in ("gaming-remaining", "all"):
            total += run_batch_list(PINTEREST_GAMING_REMAINING_BATCH, "Remaining Gaming")

        print(f"\n[✔] Finished Pinterest ingestion! Total updated: {total}")
        run_pipeline()
        
    elif args.action == "pipeline":
        run_pipeline()


if __name__ == "__main__":
    main()
