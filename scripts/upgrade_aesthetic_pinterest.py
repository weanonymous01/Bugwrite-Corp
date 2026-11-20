#!/usr/bin/env python3
"""
Aesthetic Pinterest Curated Banner Upgrader for Big Tech, Security, and Business.
Eliminates diagrams, wireframe AI faces, empty furniture, and generic stock.
Replaces with authentic aesthetic Pinterest photography, real tech devices, dark-mode interfaces,
and iconic company architecture directly matching the article headline.
"""

import os
import sys
import json
import re
import shutil
import urllib.request
from PIL import Image, ImageOps
from pinterest_dl import ApiScraper

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
ARTICLES_DIR = os.path.join(PUBLIC, "blog", "articles")
DATA_JS = os.path.join(PUBLIC, "blog", "articles-data.js")
SCRATCH_DIR = os.path.join(ROOT, "scratch_pinterest", "curated_aesthetic")

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720
TARGET_ASPECT = 16 / 9

# High aesthetic, authentic Pinterest queries tailored directly to each headline:
AESTHETIC_REPLACEMENTS = [
    # --- BIG TECH (Screenshot Articles) ---
    {
        "id": "apple-outage",
        "query": "apple store fifth avenue glass cube new york night aesthetic photography 1920x1080",
        "alt": "Pinterest aesthetic night photography of Apple Fifth Avenue iconic glass cube store in New York",
    },
    {
        "id": "gmail-outage-rumors-apple-disruption",
        "query": "googleplex mountain view headquarters modern glass architecture sunset photography",
        "alt": "Pinterest aesthetic photo of Google Mountain View corporate headquarters campus at sunset",
    },
    {
        "id": "amazon-down-aws-us-east-1-friction",
        "query": "amazon spheres seattle architecture night photography aesthetic",
        "alt": "Pinterest aesthetic night photography of Amazon Spheres corporate headquarters in Seattle",
    },
    {
        "id": "facebook-italy-privacy-fine-multiple-profiles",
        "query": "meta facebook headquarters modern glass architecture menlo park aesthetic",
        "alt": "Pinterest aesthetic photography of Meta modern corporate headquarters campus in Menlo Park",
    },
    {
        "id": "microsoft-outlook-teams-copilot-outage",
        "query": "microsoft surface laptop aesthetic workspace dark mode clean photography",
        "alt": "Pinterest clean aesthetic workspace photography with Microsoft Surface laptop",
    },
    {
        "id": "why-so-many-internet-outages-2026",
        "query": "tokyo night skyline cyber aesthetic photography wallpaper 1920x1080",
        "alt": "Pinterest aesthetic night photography of illuminated metropolis network skyline",
    },
    {
        "id": "openai-gpt-6-2-astra-sol-cyber-2026",
        "query": "san francisco mission district modern tech startup office architecture aesthetic",
        "alt": "Pinterest aesthetic modern tech office architecture in San Francisco",
    },
    {
        "id": "best-ai-coding-tools-2026",
        "query": "vs code dark mode aesthetic developer workspace macbook clean",
        "alt": "Pinterest clean aesthetic developer workspace with VS Code dark mode on MacBook",
    },
    {
        "id": "ai-agents-explained-how-they-work",
        "query": "autonomous robotics laboratory clean modern aesthetic photography",
        "alt": "Pinterest aesthetic photography of modern robotics research laboratory",
    },
    {
        "id": "what-are-coding-agents-developers",
        "query": "software developer dark mode code editor mechanical keyboard aesthetic",
        "alt": "Pinterest aesthetic programming setup with code editor and mechanical keyboard",
    },
    {
        "id": "how-to-check-if-website-is-down",
        "query": "macbook pro terminal dark aesthetic coffee shop photography",
        "alt": "Pinterest aesthetic photography of MacBook Pro running network terminal",
    },
    {
        "id": "cloudflare-aws-azure-internet-dependence",
        "query": "hyperscale modern data center clean server corridor aesthetic photography",
        "alt": "Pinterest aesthetic photography of modern hyperscale cloud data center corridor",
    },
    {
        "id": "windows-11-common-errors-fixes",
        "query": "windows 11 bloom wallpaper minimal clean desk setup aesthetic",
        "alt": "Pinterest clean minimalist workspace featuring Windows 11 desktop display",
    },
    {
        "id": "android-17-features-changes-devices",
        "query": "google pixel phone sleek aesthetic photography clean",
        "alt": "Pinterest clean aesthetic photography of Google Pixel flagship smartphone",
    },
    {
        "id": "ios-27-features-siri-liquid-glass",
        "query": "apple iphone sleek aesthetic photography minimalist dark",
        "alt": "Pinterest minimalist aesthetic photography of Apple iPhone sleek glass design",
    },
    {
        "id": "why-ai-data-centers-consume-electricity",
        "query": "modern energy grid solar wind turbine clean power aesthetic photography",
        "alt": "Pinterest aesthetic landscape photography of modern renewable energy power infrastructure",
    },
    {
        "id": "what-are-ai-chips-why-companies-fight",
        "query": "silicon microchip processor macro photography aesthetic gold pins",
        "alt": "Pinterest aesthetic macro photography of high performance silicon processor microchip",
    },
    {
        "id": "best-free-ai-tools-productivity-2026",
        "query": "minimalist creative productivity desk notebook macbook coffee aesthetic",
        "alt": "Pinterest aesthetic minimalist creative productivity desk with MacBook and coffee",
    },

    # --- SECURITY ---
    {
        "id": "artex-ai-cyber-framework",
        "query": "cybersecurity operations center modern clean control room screens aesthetic",
        "alt": "Pinterest aesthetic photography of modern cybersecurity operations control center",
    },
    {
        "id": "java4shell-cve-2026-114938",
        "query": "server room corridor blue led lighting clean data center aesthetic",
        "alt": "Pinterest aesthetic photography of clean data center server corridor with blue LED lighting",
    },
    {
        "id": "fbi-warning-today-facestealer-artex",
        "query": "washington dc federal government building columns classical architecture dusk aesthetic",
        "alt": "Pinterest aesthetic dusk photography of federal government architectural columns in Washington DC",
    },
    {
        "id": "ai-finding-software-vulnerabilities-faster",
        "query": "software security source code review dark screen aesthetic",
        "alt": "Pinterest aesthetic photography of software security source code review on dark screen",
    },
    {
        "id": "what-is-a-zero-day-vulnerability",
        "query": "cyber security digital security key lock dark aesthetic",
        "alt": "Pinterest clean dark aesthetic photography of hardware security key and encryption",
    },
    {
        "id": "how-hackers-exploit-unpatched-software",
        "query": "cybersecurity researcher workstation dark room dual monitors aesthetic",
        "alt": "Pinterest aesthetic photography of cybersecurity researcher workstation with dual displays",
    },
    {
        "id": "best-password-managers-2026",
        "query": "yubikey security key plugged into modern macbook aesthetic",
        "alt": "Pinterest aesthetic macro photography of hardware security authentication key",
    },
    {
        "id": "best-vpn-services-windows-2026",
        "query": "minimalist laptop cafe public wifi privacy aesthetic photography",
        "alt": "Pinterest aesthetic photography of modern laptop working securely in cafe",
    },
    {
        "id": "how-ransomware-works-business-protection",
        "query": "corporate data center security server rack glass clean aesthetic",
        "alt": "Pinterest aesthetic photography of enterprise corporate data server infrastructure",
    },
    {
        "id": "is-personal-data-used-to-train-ai",
        "query": "modern smartphone privacy settings dark screen aesthetic",
        "alt": "Pinterest aesthetic photography of modern smartphone security interface",
    },

    # --- BUSINESS ---
    {
        "id": "harvey-jones-nvidia-chair",
        "query": "nvidia headquarters voyager santa clara silicon valley architecture photography",
        "alt": "Pinterest aesthetic architectural photography of Nvidia Voyager headquarters in Santa Clara",
    },
    {
        "id": "nvidia-q3-fy27-earnings-115-billion",
        "query": "nvidia founders edition graphics card sleek hardware photography aesthetic",
        "alt": "Pinterest sleek aesthetic hardware photography of Nvidia flagship graphics architecture",
    },
    {
        "id": "anthropic-ipo-nasdaq-ant-2026",
        "query": "times square nasdaq tower new york city night neon photography aesthetic",
        "alt": "Pinterest aesthetic night photography of Nasdaq Tower in Times Square New York City",
    },
    {
        "id": "salesforce-copilotforce-layoffs-november-2026",
        "query": "salesforce tower san francisco skyline dusk sunset aesthetic photography",
        "alt": "Pinterest aesthetic sunset photography of Salesforce Tower and San Francisco skyline",
    },
    {
        "id": "mega-millions-drawing-november-17-2026",
        "query": "lottery winning jackpot golden celebration aesthetic photography",
        "alt": "Pinterest aesthetic golden lighting celebration photography",
    },
    {
        "id": "amazon-google-ai-investment-2026",
        "query": "silicon valley tech company campus modern glass architecture sunny aesthetic",
        "alt": "Pinterest aesthetic architectural photography of modern Silicon Valley tech campus",
    },
    {
        "id": "us-ai-chip-export-restrictions-2026",
        "query": "semiconductor fabrication cleanroom silicon wafer technician aesthetic photography",
        "alt": "Pinterest aesthetic photography of semiconductor cleanroom wafer fabrication",
    },
    {
        "id": "is-ai-boom-becoming-a-bubble-2026",
        "query": "wall street new york stock exchange trading floor screens aesthetic",
        "alt": "Pinterest aesthetic photography of New York Stock Exchange financial monitors",
    },
    {
        "id": "why-tech-stocks-falling-november-2026",
        "query": "wall street sign trinity church financial district manhattan photography aesthetic",
        "alt": "Pinterest aesthetic architectural photography of Wall Street in Manhattan financial district",
    },
    {
        "id": "ai-industry-data-center-spending-2026",
        "query": "hyperscale modern data center exterior architecture sunset aesthetic",
        "alt": "Pinterest aesthetic architectural photography of modern hyperscale data center facility at sunset",
    },
    {
        "id": "ai-infrastructure-costs-startups-2026",
        "query": "liquid cooled server rack computing hardware aesthetic photography",
        "alt": "Pinterest aesthetic photography of advanced liquid-cooled server rack hardware",
    },
    {
        "id": "isomorphic-labs-5-billion-series-c",
        "query": "modern biotechnology research laboratory clean glass aesthetic photography",
        "alt": "Pinterest aesthetic photography of clean modern biotechnology research laboratory",
    },
    {
        "id": "ai-startups-changing-software-model",
        "query": "modern tech startup office open space brick glass aesthetic photography",
        "alt": "Pinterest aesthetic interior photography of modern technology startup office workspace",
    },
    {
        "id": "why-saas-companies-adding-ai-features",
        "query": "modern product design software dashboard macbook aesthetic clean",
        "alt": "Pinterest clean aesthetic workspace photography of modern software dashboard on MacBook",
    },
    {
        "id": "what-is-an-ai-agent-business",
        "query": "modern glass corporate boardroom high floor skyline view aesthetic",
        "alt": "Pinterest aesthetic architectural photography of modern high-rise corporate boardroom overlooking city",
    },
    {
        "id": "cloud-computing-competing-ai-customers",
        "query": "enterprise cloud data center blue ambient server corridor photography",
        "alt": "Pinterest aesthetic photography of enterprise cloud data server facility with blue lighting",
    },
    {
        "id": "business-impact-cloud-software-outages",
        "query": "financial district glass skyscrapers dusk reflection aesthetic photography",
        "alt": "Pinterest aesthetic photography of financial district glass skyscrapers reflecting dusk sky",
    },
    {
        "id": "cybersecurity-spending-business-priority",
        "query": "modern corporate executive desk macbook city view dusk aesthetic",
        "alt": "Pinterest aesthetic executive office workspace with city view at dusk",
    },
    {
        "id": "how-data-breaches-affect-companies-financially",
        "query": "corporate headquarters financial district night architectural photography",
        "alt": "Pinterest aesthetic night photography of corporate financial headquarters architecture",
    },
    {
        "id": "cost-to-build-ai-saas-startup-2026",
        "query": "creative founder workspace laptop coffee notebook aesthetic photography",
        "alt": "Pinterest aesthetic photography of creative startup founder workspace with laptop and notebook",
    },
    {
        "id": "best-crm-software-small-businesses-2026",
        "query": "modern boutique design agency workspace clean aesthetic photography",
        "alt": "Pinterest aesthetic clean interior photography of modern boutique business workspace",
    },
    {
        "id": "best-ai-tools-small-business-owners",
        "query": "artisan small business studio desk laptop creative aesthetic",
        "alt": "Pinterest aesthetic photography of creative small business studio workspace",
    },
    {
        "id": "why-tech-companies-restructuring-2026",
        "query": "modern glass office building corporate lobby architectural photography aesthetic",
        "alt": "Pinterest aesthetic architectural photography of modern corporate tech campus atrium",
    },
    {
        "id": "vc-evaluating-ai-startups-2026",
        "query": "silicon valley sand hill road venture capital modern architecture aesthetic",
        "alt": "Pinterest aesthetic modern architecture photography of Silicon Valley venture capital office",
    },
    {
        "id": "why-companies-invest-private-ai-models",
        "query": "modern private cloud enterprise server hardware aesthetic photography",
        "alt": "Pinterest aesthetic photography of high performance private enterprise server hardware",
    },
    {
        "id": "cost-of-running-large-ai-model",
        "query": "supercomputer server racks illuminated blue clean perspective aesthetic",
        "alt": "Pinterest aesthetic perspective photography of illuminated supercomputing cluster",
    },
    {
        "id": "us-export-controls-global-semiconductors",
        "query": "silicon wafer semiconductor manufacturing cleanroom aesthetic photography",
        "alt": "Pinterest aesthetic photography of high technology semiconductor silicon wafer manufacturing",
    },
]


def normalize_image(source_path, dest_path, quality=88):
    with Image.open(source_path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")

        orig_w, orig_h = img.size
        orig_aspect = orig_w / orig_h

        # Center-crop to 16:9 aspect ratio
        if orig_aspect > TARGET_ASPECT:
            new_w = int(orig_h * TARGET_ASPECT)
            left = (orig_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, orig_h))
        elif orig_aspect < TARGET_ASPECT:
            new_h = int(orig_w / TARGET_ASPECT)
            top = max(0, int((orig_h - new_h) * 0.35))
            img = img.crop((0, top, orig_w, top + new_h))

        img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
        img.save(dest_path, "JPEG", quality=quality, optimize=True, progressive=True)
        return os.path.getsize(dest_path) / 1024


def update_metadata(article_id, img_path, alt_text):
    with open(DATA_JS, "r", encoding="utf-8") as f:
        content = f.read()

    art_pattern = re.compile(
        rf'(\{{\s*\"?id\"?:\s*"{re.escape(article_id)}",[\s\S]*?)(\"?image\"?:\s*"[^"]*",)(\s*\"?imageAlt\"?:\s*"[^"]*",)?([\s\S]*?\n\s*\}},?)'
    )
    match = art_pattern.search(content)
    if not match:
        print(f"[!] ID {article_id} not found in articles-data.js")
        return False

    prefix, old_img, old_alt, suffix = match.groups()
    use_quotes = '"image"' in old_img
    img_k = '"image"' if use_quotes else 'image'
    alt_k = '"imageAlt"' if use_quotes else 'imageAlt'

    new_img = f'{img_k}: "{img_path}",'
    new_alt = f'\n      {alt_k}: "{alt_text}",'

    updated = art_pattern.sub(lambda m: f"{prefix}{new_img}{new_alt}{suffix}", content, count=1)
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write(updated)
    return True


def run():
    scraper = ApiScraper()
    os.makedirs(SCRATCH_DIR, exist_ok=True)
    success_count = 0

    print(f"Starting Aesthetic Pinterest replacement for {len(AESTHETIC_REPLACEMENTS)} articles...")

    for idx, item in enumerate(AESTHETIC_REPLACEMENTS, 1):
        target_id = item["id"]
        query = item["query"]
        alt = item["alt"]
        print(f"\n[{idx}/{len(AESTHETIC_REPLACEMENTS)}] Searching Pinterest for '{target_id}': '{query}'")

        target_temp = os.path.join(SCRATCH_DIR, re.sub(r"[^a-zA-Z0-9]+", "_", target_id))
        if os.path.exists(target_temp):
            shutil.rmtree(target_temp)
        os.makedirs(target_temp, exist_ok=True)

        try:
            scraper.search_and_download(query, target_temp, num=5)
        except Exception as e:
            print(f"[!] Scraper error for {target_id}: {e}")
            continue

        candidates = [
            os.path.join(target_temp, f)
            for f in os.listdir(target_temp)
            if os.path.isfile(os.path.join(target_temp, f)) and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]

        if not candidates:
            print(f"[!] No candidate images found for '{target_id}'")
            continue

        def score(p):
            try:
                with Image.open(p) as im:
                    w, h = im.size
                    if w < 400 or h < 300:
                        return -100
                    diff = abs((w / h) - TARGET_ASPECT)
                    landscape = 10 if w > h else 0
                    return landscape - (diff * 5) + (min(w, 1920) / 1000)
            except Exception:
                return -999

        best = max(candidates, key=score)
        with Image.open(best) as b_im:
            print(f"  [✔] Selected best pin: {os.path.basename(best)} ({b_im.size[0]}x{b_im.size[1]})")

        dest_file = f"{target_id}.jpg"
        dest_path = os.path.join(ARTICLES_DIR, dest_file)
        rel_path = f"/blog/articles/{dest_file}"

        size_kb = normalize_image(best, dest_path)
        print(f"  [✔] Normalized to 1280x720 16:9 ({size_kb:.1f} KB)")

        update_metadata(target_id, rel_path, alt)
        success_count += 1

    print(f"\n[DONE] Successfully updated {success_count}/{len(AESTHETIC_REPLACEMENTS)} articles with aesthetic Pinterest photos!")


if __name__ == "__main__":
    run()
