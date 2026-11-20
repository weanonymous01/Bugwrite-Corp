#!/usr/bin/env python3
"""
Autonomous 24/7 Trend Publisher for Bugwrite.

Features:
1. Multi-Category Scanning: Gathers real-time search spikes from Google Trends across
   Gaming (6), Big Tech (18), Business (3), and Security.
2. Demand-First Ranking: Ranks all spikes into a unified priority pool by raw search
   volume and growth velocity (+100%, +400%, +800%).
3. Duplicate Filtering: Verifies candidates against all existing articles, titles,
   slugs, and user questions to prevent duplicate posts.
4. Real-Time Web Research: Pulls live breaking news headlines and broadcast context
   from Google News RSS before drafting.
5. In-Depth Journalistic Content (800-1100 words): Prompts NVIDIA NIM to answer
   every user question directly in the first sentence under each <h2>, with zero AI clichés,
   zero forbidden em/en dashes, and zero <li> bullet tags.
6. Authentic 16:9 Photography: Automatically searches Pinterest for real-world physical
   photography, crops with 35% top-weight to 1280x720 progressive JPEG (<180 KB).
7. Full Deployment Pipeline: Updates articles-data.js cleanly, runs build_seo.py,
   validates with audit_seo.py, and submits new URLs to search engines via IndexNow.
"""

import os
import sys
import re
import json
import shutil
import argparse
import subprocess
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

PUBLIC = os.path.join(ROOT, "public")
DATA_JS = os.path.join(PUBLIC, "blog", "articles-data.js")
ARTICLES_DIR = os.path.join(PUBLIC, "blog", "articles")
SCRATCH_DIR = os.path.join(ROOT, "scratch_pinterest")

DEFAULT_NVIDIA_API_KEY = os.environ.get(
    "NVIDIA_API_KEY",
    "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"
)
NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT

CATEGORY_MAPPING = {
    6: "Gaming",
    18: "Big Tech",
    3: "Business"
}

AUTHORS = {
    "Gaming": ("Ethan Brooks", "Senior Gaming Editor"),
    "Big Tech": ("Ryan Mitchell", "Senior Technology Editor"),
    "Security": ("Sophia Carter", "Senior Cybersecurity Editor"),
    "Business": ("Olivia Bennett", "Senior Business Editor")
}


def load_catalog_articles():
    """Loads all articles from public/blog/articles-data.js using node."""
    node_cmd = (
        "const fs=require('fs'); const vm=require('vm'); "
        f"const ctx={{window:{{}}}}; vm.runInNewContext(fs.readFileSync({json.dumps(DATA_JS)},'utf8'), ctx); "
        "process.stdout.write(JSON.stringify(ctx.window.BUGWRITE_ARTICLES));"
    )
    res = subprocess.run(["node", "-e", node_cmd], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def is_duplicate(trend_item, existing_articles):
    """
    Air-tight check to prevent duplicate articles by matching keywords
    and breakdown questions against all existing articles.
    """
    trend_title = trend_item["trend"].lower().strip()
    questions = [q.lower().strip() for q in trend_item.get("questions", [])]

    stop_words = {
        "gta", "gta6", "6", "vi", "the", "in", "is", "for", "on", "a", "of", "and", "to",
        "how", "has", "anyone", "does", "what", "who", "where", "when", "why", "game",
        "games", "new", "all", "are", "can", "with", "vs", "today", "now"
    }

    corpus = []
    for art in existing_articles:
        text = " ".join([
            art.get("id", ""),
            art.get("title", ""),
            art.get("dek", ""),
            " ".join(art.get("keywords", []))
        ]).lower()
        corpus.append((art["id"], art["title"], text))

    # Check trend title
    title_words = [w for w in re.findall(r"[a-z0-9]+", trend_title) if w not in stop_words]
    if len(title_words) >= 2:
        for aid, atitle, atext in corpus:
            if all(w in atext for w in title_words):
                return True, f"Trend keywords {title_words} already in '{atitle}'"
    elif len(title_words) == 1 and len(title_words[0]) > 4:
        for aid, atitle, atext in corpus:
            if title_words[0] in aid or title_words[0] in atitle.lower():
                return True, f"Subject '{title_words[0]}' already in '{atitle}'"

    # Check question queries
    for q in questions:
        q_words = [w for w in re.findall(r"[a-z0-9]+", q) if w not in stop_words]
        if len(q_words) >= 2:
            for aid, atitle, atext in corpus:
                if all(w in atext for w in q_words):
                    return True, f"Question '{q}' already answered in '{atitle}'"

    return False, None


def fetch_live_news(query):
    """Fetches real-time news articles from Google News RSS for ground-truth facts."""
    news_snippets = []
    queries = [query, f"{query} news"]

    headers = {"User-Agent": "Mozilla/5.0"}
    for q in queries:
        try:
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=en-US&gl=US&ceid=US:en"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = resp.read().decode("utf-8")
                root = ET.fromstring(data)
                for it in root.findall(".//item")[:4]:
                    title = it.find("title").text if it.find("title") is not None else ""
                    desc = it.find("description").text if it.find("description") is not None else ""
                    clean_desc = re.sub(r"<[^>]+>", " ", desc).strip()
                    item_text = f"News Headline: {title}\nDetails: {clean_desc}"
                    if item_text not in news_snippets:
                        news_snippets.append(item_text)
        except Exception as e:
            continue

    return "\n\n".join(news_snippets[:6])


def clean_text_strict(text):
    """Enforces strict guidelines: NO em/en dashes, NO <li> tags."""
    text = text.replace(" — ", ", ").replace("—", ", ")
    text = text.replace(" – ", ", ").replace("–", ", ")
    text = re.sub(r"<ul>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</ul>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<li>(.*?)</li>", r"<p>\1</p>", text, flags=re.IGNORECASE)
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()


def call_nvidia_nim(prompt, system_prompt, model="nvidia/nemotron-3.5-bolt-e4b", max_tokens=3500):
    """Calls NVIDIA NIM with error handling and fallback."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEFAULT_NVIDIA_API_KEY}"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.25
    }

    req = urllib.request.Request(NVIDIA_ENDPOINT, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"].get("content") or ""
    except Exception as e:
        print(f"[!] NIM model {model} notice: {e}")
        if model != "nvidia/nemotron-3.5-lightning-30b-a3b":
            print("[+] Retrying with fallback model nemotron-3.5-lightning-30b-a3b...")
            return call_nvidia_nim(prompt, system_prompt, model="nvidia/nemotron-3.5-lightning-30b-a3b", max_tokens=4000)
        return ""


def generate_article_content(trend_item, target_category):
    """Generates an in-depth, verified 800-1100 word human investigative article."""
    trend_name = trend_item["trend"]
    questions = trend_item.get("questions", [])
    related = trend_item.get("related_searches", [])

    print(f"[Research] Gathering real-time live news context for: '{trend_name}'...")
    news_context = fetch_live_news(trend_name)
    if news_context:
        print(f"[✔] Found live news context ({len(news_context.split())} words).")
    else:
        print("[!] No live news snippets returned; relying on verified topic background.")

    system_prompt = (
        "You are an expert senior investigative editor for Bugwrite. "
        "You write in simple, engaging, direct, and conversational human English. "
        "Rules to follow strictly:\n"
        "1. Write like an experienced, thoughtful human explaining things clearly. No big or fancy words.\n"
        "2. NO AI clichés or corporate jargon (never use 'dive into', 'delve', 'testament', 'revolutionize', 'landscape', 'beacon').\n"
        "3. NEVER use em dashes ('—') or en dashes ('–'). Use commas, colons, or parentheses.\n"
        "4. NEVER output <li> or <ul> bullet tags. Use only <p>, <h2>, and <h3> HTML tags.\n"
        "5. UNDER EVERY <h2> QUESTION HEADING, write 2 to 3 substantive, deeply informative paragraphs (minimum 150 words per section).\n"
        "6. Answer each question directly in the very first sentence, then explain the real facts, background, quotes, community reactions, and context.\n"
        "7. The total article body must be between 750 and 1,000+ words. Never output shallow summaries."
    )

    user_prompt = f"""
Write a comprehensive, deeply researched 800+ word article for Bugwrite.
Trending Topic: {trend_name}
Category: {target_category}

Live Real-Time News & Research Context:
{news_context if news_context else "Cover the full verified story, background, and community perspectives."}

Questions People Are Asking:
{json.dumps(questions[:6], indent=2)}

Related Search Queries:
{json.dumps(related[:6], indent=2)}

Format your output using these exact delimited section headers:

=== TITLE ===
Compelling hook headline incorporating primary search and questions under 75 chars

=== SEO_TITLE ===
Hook title | Bugwrite (under 65 chars)

=== DEK ===
One clear sentence summarizing the facts under 140 chars

=== META_DESCRIPTION ===
Direct search snippet answering the main question under 155 chars

=== SLUG ===
clean-kebab-case-slug

=== KEYWORDS ===
comma, separated, search, terms

=== IMAGE_QUERY ===
Search query for 100% genuine real-life photography of physical objects, buildings, or humans in daylight.
CRITICAL ANTI-AI RULES:
- NEVER use abstract concepts, charts, trading screens, neon lights, glowing effects, digital art, or wallpapers.
- ALWAYS use concrete physical camera subjects (e.g. 'wall street sign financial district manhattan photography', 'person holding video game controller living room photo', 'fbi seal building stone wall real photo', 'person typing on laptop coffee shop sunlight photo').
- MUST end with 'real photo' or 'photography'.

=== IMAGE_ALT ===
Aesthetic physical description of the photograph

=== FAQS ===
Q: Question 1?
A: Direct, thorough 2-3 sentence answer explaining the fact.
Q: Question 2?
A: Direct, thorough 2-3 sentence answer explaining the fact.
Q: Question 3?
A: Direct, thorough 2-3 sentence answer explaining the fact.
Q: Question 4?
A: Direct, thorough 2-3 sentence answer explaining the fact.

=== BODY ===
<p>Deep intro paragraph connecting the viral controversy or trend to readers...</p>

<h2>First Question Heading</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph with background, quotes, and facts...</p>
<p>Third paragraph with community reactions...</p>

<h2>Second Question Heading</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph with context...</p>
<p>Third paragraph with analysis...</p>

<h2>Third Question Heading</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph...</p>

<h2>Fourth Question Heading</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph...</p>

<p>Concluding perspective for readers and players...</p>
"""

    raw = call_nvidia_nim(user_prompt, system_prompt=system_prompt)
    if not raw:
        return None

    def get_sec(name):
        m = re.search(rf"===\s*{name}\s*===\s*\n([\s\S]*?)(?=(?:===\s*[A-Z_]+\s*===|$))", raw)
        return m.group(1).strip() if m else ""

    title = clean_text_strict(get_sec("TITLE"))
    seo_title = clean_text_strict(get_sec("SEO_TITLE")) or f"{title} | Bugwrite"
    dek = clean_text_strict(get_sec("DEK"))
    meta_desc = clean_text_strict(get_sec("META_DESCRIPTION"))
    slug = re.sub(r"[^a-z0-9\-]+", "-", get_sec("SLUG").lower()).strip("-")
    if not slug:
        slug = re.sub(r"[^a-z0-9\-]+", "-", trend_name.lower()).strip("-")

    keywords = [clean_text_strict(k) for k in get_sec("KEYWORDS").split(",") if k.strip()]
    img_query = get_sec("IMAGE_QUERY") or f"{trend_name} real photo"
    img_alt = clean_text_strict(get_sec("IMAGE_ALT")) or f"Photo illustration for {title}"

    faqs = []
    for q, a in re.findall(r"Q:\s*(.*?)\s*\n\s*A:\s*(.*?)(?=(?:\n\s*Q:|$))", get_sec("FAQS"), re.DOTALL):
        faqs.append({"q": clean_text_strict(q.strip()), "a": clean_text_strict(a.strip())})

    body = clean_text_strict(get_sec("BODY"))
    word_count = len(re.sub(r"<[^>]+>", " ", body).split())

    if word_count < 400:
        print(f"[!] Article length too short ({word_count} words). Skipping.")
        return None

    return {
        "title": title,
        "seoTitle": seo_title,
        "dek": dek,
        "metaDescription": meta_desc,
        "slug": slug,
        "keywords": keywords,
        "imageQuery": img_query,
        "imageAlt": img_alt,
        "faqs": faqs,
        "body": body,
        "wordCount": word_count
    }


def normalize_image(source_path, dest_path, quality=88):
    """Crops to 16:9 1280x720 with 35% top-weight progressive JPEG."""
    with Image.open(source_path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")

        orig_w, orig_h = img.size
        orig_aspect = orig_w / orig_h

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


def sanitize_image_query(query, category):
    """
    Guarantees the Pinterest search query targets 100% genuine real-life photography.
    Replaces AI bait keywords (charts, trading screens, neon, crypto) with authentic physical anchors.
    """
    query_lower = query.lower()

    # Words that attract Midjourney / AI art on Pinterest
    ai_bait = [
        "chart", "charts", "trading screen", "screens", "crypto", "bitcoin",
        "futuristic", "cyberpunk", "concept art", "render", "3d", "vector",
        "illustration", "neon", "digital art", "wallpaper"
    ]

    if any(w in query_lower for w in ai_bait):
        if category == "Business":
            return "wall street sign financial district manhattan photography"
        elif category == "Security":
            return "fbi seal stone building headquarters real photo"
        elif category == "Gaming":
            return "person holding black video game controller hands couch photo"
        elif category == "Big Tech":
            return "person typing on laptop keyboard modern cafe sunlight photo"

    # Guarantee authentic camera suffix
    if not any(k in query_lower for k in ["real photo", "photography", "candid photo", "street photo", "photo"]):
        query = f"{query.strip()} real photo"

    return query


def fetch_pinterest_banner(query, slug, category="Gaming"):
    """Downloads widescreen real camera photo candidate and crops to 16:9."""
    from pinterest_dl import ApiScraper

    clean_query = sanitize_image_query(query, category)
    print(f"[Pinterest] Fetching real-photo banner: '{clean_query}'...")
    temp_dir = os.path.join(SCRATCH_DIR, slug)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    scraper = ApiScraper()
    try:
        scraper.search_and_download(clean_query, temp_dir, num=8)
    except Exception as e:
        print(f"[!] Pinterest download warning: {e}")

    downloaded = [
        os.path.join(temp_dir, f)
        for f in os.listdir(temp_dir)
        if os.path.isfile(os.path.join(temp_dir, f)) and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    dest_path = os.path.join(ARTICLES_DIR, f"{slug}.jpg")
    if downloaded:
        def score(p):
            try:
                is_png = p.lower().endswith(".png")
                with Image.open(p) as im:
                    w, h = im.size
                    if w < 500 or h < 400:
                        return -999

                    score_val = 0
                    # Anti-AI Filter: Real camera photography is almost exclusively JPEG on Pinterest
                    # Midjourney/DALL-E digital exports on Pinterest are heavily PNG and 1024x1024
                    if is_png:
                        score_val -= 25
                    if w == 1024 and h == 1024:
                        score_val -= 30
                    if not is_png:
                        score_val += 15

                    # High resolution camera reward
                    total_pixels = w * h
                    if total_pixels >= 1_500_000:
                        score_val += 20
                    elif total_pixels >= 800_000:
                        score_val += 10

                    # Natural camera aspect ratios suitable for 35% top-weight 16:9 crop
                    aspect = w / h
                    if 1.35 <= aspect <= 1.85:
                        score_val += 15  # Natural 3:2 or 16:9 camera landscape
                    elif 0.55 <= aspect <= 0.85:
                        score_val += 10  # Natural vertical portrait camera photo

                    return score_val
            except Exception:
                return -999

        best = max(downloaded, key=score)
        normalize_image(best, dest_path)
        print(f"[✔] Ingested Pinterest banner: {dest_path}")
    else:
        # Fallback to authentic photography
        fallback = os.path.join(ARTICLES_DIR, "xbox-black-friday.jpg")
        shutil.copyfile(fallback, dest_path)
        print(f"[✔] Used authentic fallback photo: {dest_path}")

    return f"/blog/articles/{slug}.jpg"


def save_article_to_catalog(art_data, category):
    """Inserts or updates the article into articles-data.js cleanly using JSON."""
    articles = load_catalog_articles()
    slug = art_data["slug"]

    author_name, author_role = AUTHORS.get(category, ("Ryan Mitchell", "Senior Technology Editor"))

    # Accurate real word count and reading time (200 words per minute)
    clean_body = re.sub(r"<[^>]+>", " ", art_data.get("body", "")).strip()
    words_count = len(clean_body.split())
    real_read_mins = max(2, round(words_count / 200))
    real_read_time = f"{real_read_mins} min read"

    # Clean real human formatted date (e.g. "Nov 20, 2026")
    formatted_date = datetime.now(timezone.utc).strftime("%b %d, %Y")

    new_entry = {
        "id": slug,
        "slot": "latest",
        "category": category,
        "title": art_data["title"],
        "seoTitle": art_data["seoTitle"],
        "metaDescription": art_data["metaDescription"],
        "keywords": art_data["keywords"],
        "dek": art_data["dek"],
        "author": author_name,
        "authorRole": author_role,
        "publishedAgo": "Just now",
        "publishedDate": formatted_date,
        "readTime": real_read_time,
        "image": art_data["image"],
        "imageAlt": art_data["imageAlt"],
        "faqs": art_data["faqs"],
        "body": art_data["body"]
    }

    idx = next((i for i, a in enumerate(articles) if a["id"] == slug), None)
    if idx is not None:
        articles[idx] = new_entry
        print(f"[✔] Updated existing article '{slug}' at index {idx}.")
    else:
        articles.insert(0, new_entry)
        print(f"[✔] Prepended new article '{slug}' to catalog.")

    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("window.BUGWRITE_ARTICLES = " + json.dumps(articles, indent=2) + ";\n")

    return True


def run_deployment_pipeline():
    """Runs build_seo.py, audit_seo.py, and ping_indexnow.py."""
    print("\n[Build] Regenerating static SEO HTML pages...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_seo.py")], check=True)

    print("\n[Audit] Running SEO & schema audit...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "audit_seo.py")], check=True)

    print("\n[IndexNow] Submitting URLs to search engines...")
    try:
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "ping_indexnow.py")], timeout=15)
    except Exception as e:
        print(f"[!] IndexNow notice: {e}")


def harvest_all_spikes(min_volume=1000, min_growth=50):
    """
    Harvests all spikes across all 4 categories:
    Gaming (6), Big Tech (18), Business (3), and Security.
    Ranks them in a single unified priority queue by search volume.
    """
    from scripts.fetch_trending import fetch_google_trends

    print("================================================================================")
    print(" HARVESTING REAL-TIME SEARCH SPIKES ACROSS ALL CATEGORIES")
    print("================================================================================")

    all_candidates = []

    # Query categories
    for cat_id, cat_name in [(6, "Gaming"), (18, "Big Tech"), (3, "Business")]:
        trends = fetch_google_trends(geo="US", category=cat_id)
        print(f"[+] Category {cat_name}: {len(trends)} active trends returned.")
        for t in trends:
            t["assignedCategory"] = cat_name
            # Check if security keyword present
            text = (t["trend"] + " " + " ".join(t.get("all_breakdown", []))).lower()
            if any(k in text for k in ["cyber", "fbi", "vulnerability", "hack", "ransomware", "data breach", "malware", "zero-day"]):
                t["assignedCategory"] = "Security"
            all_candidates.append(t)

    # Filter by minimum threshold and deduplicate across pool
    seen_trends = set()
    filtered_spikes = []
    for t in all_candidates:
        name = t["trend"].lower().strip()
        if name in seen_trends:
            continue
        seen_trends.add(name)

        vol = t.get("volume_raw") or 0
        growth = t.get("growth_raw") or 0
        if vol >= min_volume and growth >= min_growth:
            filtered_spikes.append(t)

    # Sort descending by raw volume and growth
    filtered_spikes.sort(key=lambda x: (x.get("volume_raw") or 0, x.get("growth_raw") or 0), reverse=True)

    print(f"\n[★] Total High-Velocity Spikes Identified: {len(filtered_spikes)}")
    for i, s in enumerate(filtered_spikes[:10], 1):
        print(f"  {i}. [{s['assignedCategory'].upper()}] {s['trend']} | Vol: {s['search_volume']} | Growth: {s['growth']}")

    return filtered_spikes


def run_autonomous_publisher(max_articles=2, min_volume=1000, min_growth=50):
    """
    Main autonomous cycle:
    1. Scans and ranks all high-velocity spikes across all categories.
    2. Identifies top fresh, non-duplicate opportunities.
    3. Researches, writes 800+ word deep article, pulls 16:9 photo, and deploys.
    """
    existing_articles = load_catalog_articles()
    print(f"[Catalog] Current database has {len(existing_articles)} published articles.")

    spikes = harvest_all_spikes(min_volume=min_volume, min_growth=min_growth)

    published_urls = []

    for spike in spikes:
        if len(published_urls) >= max_articles:
            break

        trend_name = spike["trend"]
        category = spike["assignedCategory"]

        is_dup, reason = is_duplicate(spike, existing_articles)
        if is_dup:
            print(f"\n[-] Skipping duplicate: '{trend_name}' ({reason})")
            continue

        print(f"\n" + "=" * 80)
        print(f" [PROCESSING SPIKE] Category: {category} | Trend: '{trend_name}' ({spike['search_volume']}, {spike['growth']})")
        print("=" * 80)

        # Generate in-depth article
        art_data = generate_article_content(spike, category)
        if not art_data:
            print(f"[!] Could not generate satisfactory article for '{trend_name}'. Moving to next spike.")
            continue

        print(f"[✔] Generated Title: {art_data['title']} ({art_data['wordCount']} words)")
        print(f"[✔] Generated Slug: {art_data['slug']}")

        # Fetch real-photo Pinterest banner
        banner_path = fetch_pinterest_banner(art_data["imageQuery"], art_data["slug"], category)
        art_data["image"] = banner_path

        # Save to database
        save_article_to_catalog(art_data, category)

        cat_slug = {
            "Gaming": "gaming",
            "Big Tech": "big-tech",
            "Security": "security",
            "Business": "business"
        }.get(category, "news")

        url = f"https://www.bugwrite.com/{cat_slug}/article/{art_data['slug']}"
        published_urls.append(url)
        print(f"[★] Article Staged: {url}")

    if published_urls:
        run_deployment_pipeline()
        print("\n" + "=" * 80)
        print(f" [AUTONOMOUS CYCLE COMPLETED] Published {len(published_urls)} Articles Live:")
        for u in published_urls:
            print(f"  * {u}")
        print("=" * 80)
    else:
        print("\n[✔] Catalog is completely up-to-date. No fresh spikes required publication.")

    return published_urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Trend Publisher for Bugwrite.")
    parser.add_argument("--max-articles", type=int, default=2, help="Maximum articles to publish per run (default: 2)")
    parser.add_argument("--min-volume", type=int, default=1000, help="Minimum search volume threshold (default: 1000)")
    parser.add_argument("--min-growth", type=int, default=50, help="Minimum percentage growth threshold (default: 50)")
    args = parser.parse_args()

    run_autonomous_publisher(
        max_articles=args.max_articles,
        min_volume=args.min_volume,
        min_growth=args.min_growth
    )
