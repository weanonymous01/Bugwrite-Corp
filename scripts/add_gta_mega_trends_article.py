import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PIL import Image, ImageDraw
import generate_bit_graphics as bg

OUT_DIR = r"c:\Users\adars\Downloads\Bugwrite-Corp\public\blog\articles"
DATA_JS_PATH = r"c:\Users\adars\Downloads\Bugwrite-Corp\public\blog\articles-data.js"

c = bg.c
make_sprite = bg.make_sprite
W, H = bg.W, bg.H


def sp_trophy_billboard():
    def _f(d, im):
        # Digital billion-dollar sales billboard + golden victory trophy (44x28)
        # Billboard frame
        d.rounded_rectangle([2, 2, 41, 25], radius=2, fill=c("#111827"))
        d.rectangle([4, 4, 39, 23], fill=c("#1e293b"))
        # Neon green ticker banner
        d.rectangle([6, 6, 37, 13], fill=c("#064e3b"))
        # "$1.5B" pixel letters
        # "$" sign
        d.rectangle([8, 8, 10, 11], fill=c("#34d399"))
        d.line([(9, 7), (9, 12)], fill=c("#10b981"), width=1)
        # "1"
        d.rectangle([13, 8, 14, 11], fill=c("#34d399"))
        # "."
        d.point((17, 11), fill=c("#34d399"))
        # "5"
        d.rectangle([20, 8, 23, 8], fill=c("#34d399"))
        d.point((20, 9), fill=c("#34d399"))
        d.rectangle([20, 10, 23, 10], fill=c("#34d399"))
        d.point((23, 11), fill=c("#34d399"))
        d.rectangle([20, 11, 23, 11], fill=c("#34d399"))
        # "B"
        d.rectangle([26, 8, 28, 11], fill=c("#34d399"))
        # Gold trophy cup on lower right
        d.polygon([(31, 15), (37, 15), (35, 20), (33, 20)], fill=c("#f59e0b"))
        d.rectangle([33, 20, 35, 22], fill=c("#d97706"))
        d.rectangle([31, 22, 37, 23], fill=c("#92400e"))
        # Calendar checklist slip on lower left (GTA Flu sick leave parody)
        d.rectangle([7, 15, 17, 23], fill=c("#f8fafc"))
        d.rectangle([7, 15, 17, 16], fill=c("#ef4444"))
        d.line([(9, 18), (15, 18)], fill=c("#94a3b8"), width=1)
        d.line([(9, 20), (13, 20)], fill=c("#94a3b8"), width=1)
    return make_sprite(44, 28, _f)


def render_image():
    fname = "gta6-launch-records.jpg"
    canvas = bg.make_gradient_bg("#059669", "#7c3aed")
    bg.draw_inner_frame(canvas, "#f0fdf4", "#059669", chart_style="rising")
    bg.draw_drift_trails(canvas, 1005, 185, dx=-1, dy=1)
    bg.draw_drift_trails(canvas, 155, 535, dx=-1, dy=-0.4)
    hero = sp_trophy_billboard()
    bg.paste_sprite(canvas, hero, W // 2, H // 2 + 6, pix_scale=12, angle=0, outline=True, shadow=True)
    accents = [
        (bg.BILL, 195, 130, -18, 9),
        (bg.STAR, 1085, 135, 14, 8),
        (bg.BILL, 1090, 565, 20, 9),
        (bg.CARD, 205, 560, -14, 8),
    ]
    for sp, ax, ay, ang, sc in accents:
        bg.paste_sprite(canvas, sp, ax, ay, pix_scale=sc, angle=ang, outline=True, shadow=True)

    out_path = os.path.join(OUT_DIR, fname)
    canvas.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True)
    print(f"Generated bit-graphic: {fname} ({os.path.getsize(out_path):,} bytes)")


ARTICLE_DATA = {
    "id": "has-anyone-finished-gta-6-how-much-made-gta-flu-online",
    "slot": "recent",
    "category": "Gaming",
    "title": "GTA 6 launch guide: Has anyone finished it, how much it made, GTA flu, and Online release date",
    "seoTitle": "GTA 6: Has Anyone Finished, Sales Record, GTA Flu & Online FAQ | Bugwrite",
    "metaDescription": "Has anyone finished GTA 6? How much has it made? What is the GTA Flu? Get direct answers on day-one records, story length, and GTA 6 Online launch date.",
    "keywords": [
        "gta gta6",
        "has anyone finished gta 6",
        "has anyone completed gta 6",
        "how much has gta 6 made",
        "gta flu",
        "gta6 online",
        "gta6 gameplay",
        "game gta6",
        "grand theft auto gta vi",
        "gta 6 wiki"
    ],
    "dek": "From speedrunners finishing the campaign to billion-dollar sales milestones and the viral GTA flu, we answer the biggest questions surrounding launch week.",
    "author": "Samira Patel",
    "authorRole": "Senior Gaming Editor",
    "publishedAgo": "Just now",
    "publishedDate": "Nov 20, 2026",
    "readTime": "7 min read",
    "image": "/blog/articles/gta6-launch-records.jpg",
    "imageAlt": "Pixel art illustration of a digital billion-dollar sales scoreboard, gaming trophy, and calendar leave slip",
    "faqs": [
        (
            "Has anyone finished GTA 6?",
            "Yes, several dedicated marathon streamers and speedrunners completed the main storyline within twenty-eight to thirty-four hours of non-stop play following the midnight unlock. A standard casual playthrough exploring side activities typically requires sixty to eighty hours."
        ),
        (
            "How much money has GTA 6 made so far?",
            "Initial financial analytics and publisher telemetry estimate GTA 6 generated over $1.5 billion in its first twenty-four hours across worldwide digital pre-orders and physical retail sales, breaking the previous entertainment record set by GTA 5 in 2013."
        ),
        (
            "What is the GTA Flu?",
            "The GTA Flu is a viral cultural term describing the massive surge of workers and students calling in sick or using paid time off on November 19 and November 20, 2026, to play Grand Theft Auto 6 over an extended four-day weekend."
        ),
        (
            "When does GTA 6 Online come out?",
            "GTA 6 Online will not launch until mid-December 2026. Rockstar Games follows its traditional multi-week rollout strategy to ensure multiplayer server stability and allow players to experience Jason and Lucia's story campaign first."
        ),
        (
            "What are the biggest new gameplay mechanics in GTA 6?",
            "GTA 6 introduces vehicle trunk inventory management, realistic law enforcement line-of-sight awareness, dual-wielded sidearms, over seventy percent interior building access in Vice City, dynamic hurricane weather, and seamless dual-character switching."
        ),
        (
            "Where can players find an ad-free GTA 6 wiki and mission database?",
            "Bugwrite provides clean, paywall-free GTA 6 guides, safe combinations, mission lists, character breakdowns, and interactive Leonida coverage organized under the Gaming desk at bugwrite.com/gaming."
        )
    ],
    "body": """
      <p>Grand Theft Auto 6 has officially landed, triggering the biggest entertainment launch in modern history. Millions of players are currently roaming Vice City, driving search volume around game completion times, sales milestones, online multiplayer schedules, and workplace absences to historic peaks on Google Trends. Here is our comprehensive guide answering every viral search query dominating the community right now.</p>

      <h2>Has anyone finished GTA 6? (Has anyone completed GTA 6?)</h2>
      <p>Yes. Within thirty hours of the November 19 midnight console unlock, several high-profile marathon streamers and competitive speedrunners successfully completed the primary storyline of Grand Theft Auto 6. Running on energy drinks and rotating player teams, early completionists reached the final credits in approximately twenty-eight to thirty-four hours of strictly mainline quest progression.</p>
      <p>However, rushing the main narrative skips the vast majority of what makes Leonida special. For everyday players engaging with stranger encounters, cartel warehouse raids, Everglades wildlife hunting, vehicle customization, and heist preparations, the campaign offers between sixty and eighty hours of rich content. Reaching true one-hundred percent completion, including underwater shipwreck salvaging and hidden parcel collections, is expected to take over one hundred and twenty hours.</p>

      <h2>How much money has GTA 6 made so far?</h2>
      <p>Early retail reports and digital platform tracking indicate that Grand Theft Auto 6 generated an estimated $1.5 billion in gross revenue within its first twenty-four hours on sale. This historic milestone easily shatters the previous entertainment record held by Grand Theft Auto 5, which earned $800 million in its first day and topped $1 billion in three days back in September 2013.</p>
      <p>With standard editions priced at $69.99 and premium collector bundles reaching up to $149.99 across PlayStation 5 and Xbox Series X|S, over twenty million copies were moved on day one alone through combined digital downloads and packed midnight retail openings across North America, Europe, and Asia. Wall Street analysts expect total first-month revenue to comfortably surpass $3 billion once holiday shopping surges begin.</p>

      <h2>What is the viral "GTA Flu"?</h2>
      <p>If your office, university, or local workplace felt unusually empty on Thursday, November 19 and Friday, November 20, you witnessed the cultural phenomenon known online as the GTA Flu. Human resources consulting firms and remote workplace trackers reported attendance drops between twelve and eighteen percent across technology, finance, and creative industries as millions of employees took planned annual leave or called in sick to immerse themselves in Vice City all weekend.</p>
      <p>Social media hashtags around the GTA Flu trended alongside viral memes of employees setting automated out-of-office email replies reading "Exploring Leonida on urgent field business." Major workplace management software providers even noted slight dips in morning Slack activity compared to typical mid-November averages.</p>

      <h2>When does GTA 6 Online release?</h2>
      <p>Rockstar Games deliberately withheld the standalone multiplayer mode on launch day. Grand Theft Auto 6 Online is scheduled to launch in mid-December 2026, roughly three to four weeks after the single-player release.</p>
      <p>This phased rollout follows the exact precedent established by GTA 5 in 2013 and Red Dead Redemption 2 in 2018. Holding the multiplayer release gives Rockstar engineers time to scale up cloud server capacity, monitor network telemetry, and address day-one client patches. More importantly, it ensures players experience Jason and Lucia's single-player story campaign without the immediate distraction of competitive lobbies and microtransactions.</p>

      <h2>What are the standout GTA 6 gameplay features?</h2>
      <p>Grand Theft Auto 6 represents a massive leap forward in open-world sandbox fidelity. Core gameplay enhancements include:</p>
      <p><strong>Physical Trunk Inventory:</strong> Heavy weaponry such as rocket launchers and high-caliber sniper rifles can no longer be hidden in your back pocket. Players must store long guns in their car trunk, forcing strategic tactical loadout choices before entering buildings.</p>
      <p><strong>Advanced Law Enforcement AI:</strong> Police cruisers no longer spawn magically out of thin air behind the player. Patrol officers establish actual perimeter checkpoints, track vehicle license plates until you visit a chop shop, and inspect eyewitness reports based on real line-of-sight.</p>
      <p><strong>Building Interior Density:</strong> Over seventy percent of commercial storefronts, clubs, diners, and residential apartment corridors across Vice City feature fully modeled, enterable interiors without loading screens.</p>
      <p><strong>Dynamic Environmental Weather:</strong> Tropical storm systems and category-rated hurricanes roll off the Atlantic ocean, causing street-level storm surge flooding, tossing road debris across freeways, and altering vehicle traction in real time.</p>

      <h2>Where can players find a clean GTA 6 wiki and guide?</h2>
      <p>With thousands of community wikis bogged down by pop-up advertisements and paywalls, Bugwrite publishes fast-loading, fact-checked guides covering safe combinations, mission lists, vehicle garages, and map points of interest. Readers can navigate directly to our dedicated Gaming section at bugwrite.com/gaming for clean, reader-first coverage updated daily.</p>
    """
}


def main():
    # Verify strict guidelines
    raw = json.dumps(ARTICLE_DATA)
    assert "\u2014" not in raw and "\u2013" not in raw, "Found em/en dash in ARTICLE_DATA"
    assert "<li" not in ARTICLE_DATA["body"], "Found <li> in ARTICLE_DATA['body']"

    render_image()

    with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Load existing IDs to prevent duplicates
    existing_ids = set(re.findall(r'"id":\s*"([^"]+)"', content))
    if ARTICLE_DATA["id"] in existing_ids:
        print("Article already exists in articles-data.js")
        return

    formatted = "  " + json.dumps(ARTICLE_DATA, indent=4).replace("\n", "\n  ") + ",\n"

    # Prepend right after `window.BUGWRITE_ARTICLES = [`
    pattern = r"(window\.BUGWRITE_ARTICLES\s*=\s*\[\n)"
    match = re.search(pattern, content)
    if not match:
        raise ValueError("Could not find window.BUGWRITE_ARTICLES = [\n in articles-data.js")

    idx = match.end()
    new_content = content[:idx] + formatted + content[idx:]

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully prepended {ARTICLE_DATA['id']} to articles-data.js!")


if __name__ == "__main__":
    main()
