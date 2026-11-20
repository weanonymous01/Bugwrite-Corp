import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import re

api_key = "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"
url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

# 1. Fetch live Google News research
q = "fox news gta 6"
news_url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=en-US&gl=US&ceid=US:en"
req = urllib.request.Request(news_url, headers={"User-Agent": "Mozilla/5.0"})
news_items = []
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode("utf-8")
    root = ET.fromstring(data)
    for it in root.findall(".//item")[:6]:
        title = it.find("title").text if it.find("title") is not None else ""
        desc = it.find("description").text if it.find("description") is not None else ""
        clean_desc = re.sub(r"<[^>]+>", " ", desc).strip()
        news_items.append(f"- {title}: {clean_desc}")

live_news = "\n".join(news_items)

research_facts = f"""
LIVE REAL-TIME NEWS FINDINGS (November 2026):
{live_news}

VERIFIED INCIDENT DETAILS:
1. Fox News Broadcasts: Multiple segments aired on Fox News daytime programs including 'Outnumbered' and Fox Digital opinion pieces framing GTA 6 as a cultural threat, warning of 'dangerous copycat stunts' and 'serious health risks'.
2. The Rachel Campos-Duffy Incident: Co-host Rachel Campos-Duffy openly questioned whether new protagonist Lucia was a 'hooker' on live television. Her fellow panelists immediately stepped in to correct her, pointing out that Lucia is a co-protagonist and partner in crime.
3. Insult to Adult Gamers: Panelists questioned why adults over 40 would spend hours playing video games, telling them to 'grow up and get a job'. Demographic statistics from the Entertainment Software Association (ESA) refute this, confirming that the average gamer is in their mid-30s with steady employment.
4. The Weazel News Parody: Millions of gamers across X, Reddit, and TikTok pointed out the extreme irony that Rockstar Games created 'Weazel News' in the Grand Theft Auto series over 20 years ago as a direct satirical caricature of Fox News sensationalism.
5. Reheating Mid-2000s Moral Panic: Critics and gaming journalists from Variety, Kotaku, and Consequence of Sound noted this mirrors the mid-2000s Jack Thompson crusade, which scientific research has thoroughly disproven regarding video games and real-world violence.
"""

prompt = f"""You are a senior gaming investigative editor for Bugwrite. Write in clean, conversational, natural human English.
Do NOT use fancy words or AI cliches.
Strictly NO em dashes ('—') or en dashes ('–'). Use commas, colons, or parentheses.
Never use <li> or <ul> tags. Use only <p>, <h2>, and <h3> HTML tags.
Write in-depth. For every question heading, provide 2 to 3 detailed, informative paragraphs explaining the real facts, quotes, and community reactions.

Research Data:
{research_facts}

Write a comprehensive 750+ word article answering:
1. Why is Fox News facing massive criticism over GTA 6 coverage?
2. What happened during the on-air discussion about Lucia?
3. What did commentators say about adult gamers over 40?
4. Why are fans pointing out the Weazel News parody?

Return ONLY valid JSON:
{{
  "title": "Clear hook headline incorporating the primary search and questions",
  "seoTitle": "Title under 65 chars | Bugwrite",
  "dek": "One clear sentence summarizing the facts under 140 chars",
  "metaDescription": "Direct summary under 155 chars",
  "body": "Full HTML article with multiple paragraphs under each h2"
}}
"""

payload = {
    "model": "nvidia/nemotron-3.5-bolt-e4b",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 3500,
    "temperature": 0.3
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=30) as r:
    res = json.loads(r.read().decode("utf-8"))
    content = res["choices"][0]["message"].get("content")
    parsed = json.loads(content[content.find("{"):content.rfind("}")+1])
    print("SUCCESS!")
    print("Title:", parsed.get("title"))
    print("Word count:", len(parsed.get("body", "").split()))
    print("\n--- BODY PREVIEW ---")
    print(parsed.get("body", "")[:800])
