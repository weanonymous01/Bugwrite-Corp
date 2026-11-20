#!/usr/bin/env python3
"""
Robust, deeply researched article generator for Bugwrite.
Uses delimited sections instead of JSON to guarantee zero JSON syntax errors on long-form 800+ word articles.
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
PUBLIC = os.path.join(ROOT, "public")
DATA_JS = os.path.join(PUBLIC, "blog", "articles-data.js")

from scripts.pipeline_trending_blog import call_nvidia_nim, fetch_live_research, clean_html_and_punctuation

def generate_deep_article():
    print("[1] Gathering live news research...")
    live_news = fetch_live_research("fox news gta 6")
    print(f"[✔] Gathered live news context ({len(live_news.split())} words).")

    system_prompt = (
        "You are an expert senior investigative editor for Bugwrite. "
        "You write in simple, engaging, direct, and conversational human English. "
        "Rules to follow strictly:\n"
        "1. Write like an experienced, thoughtful human explaining things clearly. No big or fancy words.\n"
        "2. NO AI clichés or corporate jargon (never use 'dive into', 'delve', 'testament', 'revolutionize', 'landscape', 'beacon').\n"
        "3. NEVER use em dashes ('—') or en dashes ('–'). Use commas, colons, or parentheses.\n"
        "4. NEVER output <li> or <ul> bullet tags. Use only <p>, <h2>, and <h3> HTML tags.\n"
        "5. UNDER EVERY <h2> QUESTION HEADING, write 2 to 3 substantive, deeply informative paragraphs (minimum 150 words per section).\n"
        "6. Answer each question directly in the very first sentence, then explain the real facts, background, quotes, community reactions from Reddit and X, and historical context.\n"
        "7. The total article body must be between 750 and 1,000 words. Never output shallow or short summaries.\n"
    )

    user_prompt = f"""
Write a comprehensive, deeply researched 800+ word article for Bugwrite.
Trending Topic: Fox News GTA 6 criticism

Verified Real-World News & Incident Context:
{live_news}

KEY REAL FACTS TO COVER THOROUGHLY:
1. Outnumbered & Fox Daytime Broadcasts: Multiple segments on Fox News warned that GTA 6 drives fears of 'dangerous copycat stunts' and claimed 'GTA mania comes with serious health risks'.
2. The Rachel Campos-Duffy Incident: Co-host Rachel Campos-Duffy openly questioned whether new protagonist Lucia was a 'hooker' on live television. Her fellow panelists immediately intervened on-air to correct her, pointing out that Lucia is a co-protagonist and equal partner in crime.
3. Insult to Adult Gamers Over 40: Commentators told adults playing video games to 'grow up and get a job'. Demographic statistics from the Entertainment Software Association (ESA) refute this, confirming the average gamer is 32 to 36 years old with steady employment and disposable income.
4. The Weazel News Parody: Millions of gamers across X, Reddit, and TikTok pointed out the extreme irony that Rockstar Games created 'Weazel News' in the Grand Theft Auto series over 20 years ago as a direct satirical caricature of Fox News sensationalism. Gamers noted Fox News is acting like real-life Weazel News.
5. 2000s Moral Panic Rerun: Gaming journalists from Variety, Kotaku, and Consequence of Sound noted this mirrors the mid-2000s Jack Thompson crusade, which scientific research has thoroughly disproven regarding video games and real-world violence.

Output your response using these exact section headers:

=== TITLE ===
Fox News GTA 6 Criticism: What Happened, Rachel Campos-Duffy Lucia Comments, and the Weazel News Irony

=== SEO_TITLE ===
Fox News GTA 6 Criticism: Full Segment Breakdown & Backlash | Bugwrite

=== DEK ===
Fox News is facing severe backlash after daytime hosts called Lucia a hooker, told adult gamers to get a job, and sparked Weazel News memes.

=== META_DESCRIPTION ===
Why is Fox News facing massive criticism over GTA 6? Full breakdown of Rachel Campos-Duffy's on-air Lucia comments, adult gamer insults, and Weazel News irony.

=== KEYWORDS ===
fox news gta 6 criticism, fox news gta 6, rachel campos duffy lucia, weazel news real life, gta 6 fox and friends, gta 6 media reaction

=== FAQS ===
Q: Why is Fox News being criticized over GTA 6?
A: Fox News faces heavy backlash for daytime segments warning of copycat stunts, claiming health risks, and dismissing adult gamers, which viewers criticized as outdated moral alarmism.
Q: What did Rachel Campos-Duffy say about Lucia on Fox News?
A: During an Outnumbered broadcast, co-host Rachel Campos-Duffy asked on live television if female lead Lucia was a hooker, forcing her co-hosts to immediately correct her on air.
Q: Why are fans comparing Fox News to Weazel News?
A: Rockstar Games created Weazel News over twenty years ago as a direct satire of Fox News sensationalism, leading gamers to point out the irony of the network mimicking its own parody.
Q: What did commentators say about gamers over 40?
A: A Fox contributor suggested that adults over 40 playing video games should grow up and get a job, sparking outrage from working professionals across the gaming community.

=== BODY ===
<p>Intro paragraph connecting the viral controversy to what millions of players are seeing online...</p>

<h2>Why is Fox News facing massive criticism over GTA 6?</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph with facts, quotes from the broadcast, and warnings about copycat stunts...</p>
<p>Third paragraph detailing the broader media reaction...</p>

<h2>What happened during Rachel Campos-Duffy's on-air segment about Lucia?</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph detailing the exact live exchange where co-hosts corrected her...</p>
<p>Third paragraph with online reactions and viral clips on TikTok and X...</p>

<h2>Why did commentators attack adult gamers over 40?</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph citing ESA demographics proving gamers are working adults with careers...</p>
<p>Third paragraph highlighting community backlash...</p>

<h2>Why are fans calling Fox News the real-life Weazel News?</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph exploring Rockstar's 20-year satirical history of Weazel News...</p>
<p>Third paragraph highlighting the irony of Fox News acting out the exact parody...</p>

<h2>Are claims of GTA 6 health risks and copycat stunts backed by evidence?</h2>
<p>Direct answer in first sentence...</p>
<p>Second detailed paragraph reviewing scientific research debunking video game violence links...</p>
<p>Third paragraph offering concluding perspectives for gamers and readers...</p>
"""

    print("[2] Prompting NVIDIA NIM...")
    raw = call_nvidia_nim(user_prompt, system_prompt=system_prompt, max_tokens=3500)
    if not raw:
        print("[!] No response from model.")
        return

    # Extract sections using regex
    def get_section(name):
        pat = rf"===\s*{name}\s*===\s*\n([\s\S]*?)(?=(?:===\s*[A-Z_]+\s*===|$))"
        m = re.search(pat, raw)
        return m.group(1).strip() if m else ""

    title = get_section("TITLE") or "Fox News GTA 6 Criticism: What Happened, Rachel Campos-Duffy Lucia Comments, and the Weazel News Irony"
    seo_title = get_section("SEO_TITLE") or f"{title} | Bugwrite"
    dek = get_section("DEK")
    meta_desc = get_section("META_DESCRIPTION")
    keywords_raw = get_section("KEYWORDS")
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    faqs_raw = get_section("FAQS")
    body = get_section("BODY")

    # Parse FAQs
    faqs = []
    qa_pairs = re.findall(r"Q:\s*(.*?)\s*\n\s*A:\s*(.*?)(?=(?:\n\s*Q:|$))", faqs_raw, re.DOTALL)
    for q, a in qa_pairs:
        faqs.append({"q": clean_html_and_punctuation(q.strip()), "a": clean_html_and_punctuation(a.strip())})

    title = clean_html_and_punctuation(title)
    dek = clean_html_and_punctuation(dek)
    meta_desc = clean_html_and_punctuation(meta_desc)
    body = clean_html_and_punctuation(body)

    word_count = len(re.sub(r"<[^>]+>", " ", body).split())
    print(f"\n[✔] Successfully parsed deep article: {word_count} words!")
    print(f"Title: {title}")
    print(f"Dek: {dek}")
    print(f"FAQs count: {len(faqs)}")

    # Update articles-data.js using clean JSON manipulation
    slug = "fox-news-gta-6-criticism-explained"
    new_art = {
        "id": slug,
        "slot": "latest",
        "category": "Gaming",
        "title": title,
        "seoTitle": seo_title,
        "metaDescription": meta_desc,
        "keywords": keywords,
        "dek": dek,
        "author": "Jordan Kim",
        "authorRole": "Senior Staff Writer",
        "publishedAgo": "Just now",
        "publishedDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "readTime": "6 min read",
        "image": f"/blog/articles/{slug}.jpg",
        "imageAlt": "Authentic photograph of a player seated before a monitor following video game news",
        "faqs": faqs,
        "body": body
    }

    node_cmd = (
        "const fs=require('fs'); const vm=require('vm'); "
        f"const ctx={{window:{{}}}}; vm.runInNewContext(fs.readFileSync({json.dumps(DATA_JS)},'utf8'), ctx); "
        "process.stdout.write(JSON.stringify(ctx.window.BUGWRITE_ARTICLES));"
    )
    res = subprocess.run(["node", "-e", node_cmd], capture_output=True, text=True, check=True)
    articles = json.loads(res.stdout)

    idx = next((i for i, a in enumerate(articles) if a["id"] == slug), None)
    if idx is not None:
        articles[idx] = new_art
        print(f"[✔] Updated existing article '{slug}' at index {idx}.")
    else:
        articles.insert(0, new_art)
        print(f"[✔] Prepended new article '{slug}' to catalog.")

    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("window.BUGWRITE_ARTICLES = " + json.dumps(articles, indent=2) + ";\n")

    print("\n[3] Running build and audit pipeline...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_seo.py")], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "audit_seo.py")], check=True)

    print(f"\n" + "=" * 80)
    print(f" [SUCCESS] DEEPLY RESEARCHED INVESTIGATIVE ARTICLE PUBLISHED")
    print(f" URL: https://www.bugwrite.com/gaming/article/{slug}")
    print(f"=" * 80)

if __name__ == "__main__":
    generate_deep_article()
