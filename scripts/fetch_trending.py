#!/usr/bin/env python3
"""
Real-Time Trending Search & Question Extraction Engine for Bugwrite.

Directly pulls live trending queries, search volumes, growth percentages,
and breakdown questions from Google Trends (e.g. Games, Tech, Business)
without requiring external API keys.

Categories:
  6  = Games / Gaming
  18 = Technology
  3  = Business & Finance
  4  = Entertainment
  17 = Sports
  all = All Categories
"""

import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

CATEGORIES = {
    "games": 6,
    "gaming": 6,
    "tech": 18,
    "technology": 18,
    "business": 3,
    "entertainment": 4,
    "sports": 17,
    "all": None
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


def fetch_google_trends(geo="US", category=6):
    """
    Fetches real-time trending topics and questions from Google Trends.
    Parses the internal AF_initDataCallback (ds:0) payload.
    """
    url = f"https://trends.google.com/trending?geo={geo}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"[!] Network error fetching Google Trends: {e}")
        return []

    # Locate the ds:0 data chunk
    match = re.search(r"AF_initDataCallback\((\{key:\s*'ds:0'.*?\})\);", html, re.DOTALL)
    if not match:
        print("[!] Could not find ds:0 data block in Google Trends page.")
        return []

    raw_callback = match.group(1)
    data_match = re.search(r"data:(\[.*?\]),\s*sideChannel:", raw_callback, re.DOTALL)
    if not data_match:
        print("[!] Could not parse JSON array from data block.")
        return []

    try:
        parsed = json.loads(data_match.group(1))
    except Exception as e:
        print(f"[!] JSON parsing error: {e}")
        return []

    if len(parsed) < 2 or not isinstance(parsed[1], list):
        print("[!] Unexpected Google Trends data structure.")
        return []

    raw_trends = parsed[1]
    results = []

    for t in raw_trends:
        if not isinstance(t, list) or len(t) < 10:
            continue

        trend_title = t[0]
        categories_found = t[10] if len(t) > 10 and isinstance(t[10], list) else []

        # Filter by category if requested
        if category is not None and category not in categories_found:
            continue

        search_volume = t[6] if len(t) > 6 else 0
        growth_rate = t[8] if len(t) > 8 else 0
        timestamp = t[3][0] if len(t) > 3 and isinstance(t[3], list) and t[3] else None

        started_dt = (
            datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M UTC")
            if timestamp
            else "Unknown"
        )

        breakdown_queries = t[9] if len(t) > 9 and isinstance(t[9], list) else []

        # Distinguish questions (who, what, where, when, why, how, is, can, does, will, has, are, was)
        question_starters = (
            "what", "why", "how", "where", "who", "when",
            "is", "can", "does", "will", "has", "are", "was", "did", "do"
        )
        questions = [
            q for q in breakdown_queries
            if any(q.lower().startswith(s + " ") for s in question_starters) or "?" in q
        ]
        related_searches = [q for q in breakdown_queries if q not in questions]

        results.append({
            "trend": trend_title,
            "search_volume": f"{search_volume:,}+" if search_volume else "N/A",
            "volume_raw": search_volume,
            "growth": f"+{growth_rate}%" if growth_rate else "N/A",
            "growth_raw": growth_rate,
            "started": started_dt,
            "categories": categories_found,
            "questions": questions,
            "related_searches": related_searches,
            "all_breakdown": breakdown_queries
        })

    # Sort primarily by raw volume descending
    results.sort(key=lambda x: (x.get("volume_raw") or 0, x.get("growth_raw") or 0), reverse=True)
    return results


def fetch_extended_questions(keyword, limit=8):
    """
    Fetches user questions from Google Autocomplete using question stems.
    """
    stems = ["how", "what", "where", "is", "why", "who"]
    discovered = []
    
    for stem in stems:
        query = f"{stem} {keyword}"
        url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if len(data) > 1 and isinstance(data[1], list):
                    for item in data[1]:
                        if item not in discovered:
                            discovered.append(item)
        except Exception:
            continue
        if len(discovered) >= limit:
            break

    return discovered[:limit]


def main():
    parser = argparse.ArgumentParser(description="Fetch live trending searches & questions from Google Trends.")
    parser.add_argument("--geo", default="US", help="Country code (default: US)")
    parser.add_argument(
        "--category",
        default="gaming",
        choices=["gaming", "games", "tech", "business", "entertainment", "sports", "all"],
        help="Category to filter (default: gaming / 6)"
    )
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")
    parser.add_argument("--expand", action="store_true", help="Fetch extended questions via Google Autocomplete")
    parser.add_argument("--limit", type=int, default=25, help="Number of trends to display (default: 25)")
    args = parser.parse_args()

    cat_id = CATEGORIES.get(args.category.lower(), 6)
    trends = fetch_google_trends(geo=args.geo, category=cat_id)

    if args.expand:
        for t in trends[:args.limit]:
            extra_q = fetch_extended_questions(t["trend"], limit=5)
            # Merge without duplicates
            for eq in extra_q:
                if eq not in t["questions"]:
                    t["questions"].append(eq)

    if args.json:
        print(json.dumps(trends[:args.limit], indent=2))
        return

    print("=" * 80)
    print(f" GOOGLE TRENDS LIVE: {args.category.upper()} ({args.geo}) | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"Total matching trends found: {len(trends)}\n")

    for idx, t in enumerate(trends[:args.limit], 1):
        print(f"[{idx}] {t['trend'].upper()}  |  Volume: {t['search_volume']}  |  Growth: {t['growth']}")
        
        if t["questions"]:
            print(f"    Questions People Are Asking ({len(t['questions'])}):")
            for q in t["questions"][:6]:
                print(f"      ? {q}")

        if t["related_searches"]:
            print(f"    Related Searches / Breakdown ({len(t['related_searches'])}):")
            searches_inline = ", ".join(t["related_searches"][:8])
            print(f"      > {searches_inline}")

        print("-" * 80)


if __name__ == "__main__":
    main()
