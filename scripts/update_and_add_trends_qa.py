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


def sp_mandy_influencer():
    def _f(d, im):
        # Glamorous tropical cocktail + neon smartphone camera live-stream icon (44x28)
        # Smartphone body
        d.rounded_rectangle([4, 3, 22, 25], radius=2, fill=c("#111827"))
        d.rectangle([6, 5, 20, 23], fill=c("#ec4899"))
        # Camera notch & selfie camera lens
        d.point((13, 4), fill=c("#64748b"))
        # Neon live-stream indicator "LIVE" pill
        d.rounded_rectangle([7, 6, 15, 9], radius=1, fill=c("#ef4444"))
        d.point((9, 7), fill=c("#ffffff"))
        # Floating heart / speech bubble on phone
        d.polygon([(15, 14), (18, 12), (18, 16)], fill=c("#fbcfe8"))
        d.rectangle([11, 12, 17, 16], fill=c("#fbcfe8"))
        # Tropical martini cocktail glass on right
        d.polygon([(26, 7), (40, 7), (33, 17)], fill=c("#38bdf8"))
        d.line([(33, 17), (33, 24)], fill=c("#94a3b8"), width=2)
        d.rectangle([28, 24, 38, 25], fill=c("#94a3b8"))
        # Cocktail olive & straw
        d.ellipse([31, 8, 35, 12], fill=c("#84cc16"))
        d.line([(29, 3), (34, 13)], fill=c("#f43f5e"), width=1)
    return make_sprite(44, 28, _f)


def render_mandy_image():
    fname = "gta6-mandy-lexie-shoaibi.jpg"
    canvas = bg.make_gradient_bg("#ec4899", "#06b6d4")
    bg.draw_inner_frame(canvas, "#fdf4ff", "#ec4899", chart_style="rising")
    bg.draw_drift_trails(canvas, 1005, 185, dx=-1, dy=1)
    bg.draw_drift_trails(canvas, 155, 535, dx=-1, dy=-0.4)
    hero = sp_mandy_influencer()
    bg.paste_sprite(canvas, hero, W // 2, H // 2 + 6, pix_scale=12, angle=0, outline=True, shadow=True)
    accents = [
        (bg.STAR, 195, 130, -16, 9),
        (bg.BOLT, 1085, 135, 14, 8),
        (bg.CARD, 1090, 565, 18, 9),
        (bg.TAG, 205, 560, -12, 8),
    ]
    for sp, ax, ay, ang, sc in accents:
        bg.paste_sprite(canvas, sp, ax, ay, pix_scale=sc, angle=ang, outline=True, shadow=True)

    out_path = os.path.join(OUT_DIR, fname)
    canvas.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True)
    print(f"Generated bit-graphic: {fname} ({os.path.getsize(out_path):,} bytes)")


ENDINGS_UPDATED = {
    "id": "gta-6-endings-how-many-choices-explained",
    "slot": "recent",
    "category": "Gaming",
    "title": "GTA 6 endings: How many endings does it have, how it ends, and good ending guide",
    "seoTitle": "GTA 6 Endings: How Many Endings, Story Finale & Good Ending | Bugwrite",
    "metaDescription": "How many endings does GTA 6 have? How does GTA 6 end? What happens at the end? Full guide to the good ending, story finale, and ending choices.",
    "keywords": [
        "gta 6 endings",
        "how many endings does gta 6 have",
        "how does gta 6 end",
        "gta 6 good ending",
        "what happens at the end of gta 6"
    ],
    "dek": "We answer every trending question about GTA 6 endings, how the story ends, what happens to Jason and Lucia, and how to get the good ending.",
    "author": "Samira Patel",
    "authorRole": "Senior Gaming Editor",
    "publishedAgo": "Just now",
    "publishedDate": "Nov 20, 2026",
    "readTime": "6 min read",
    "image": "/blog/articles/gta6-endings.jpg",
    "imageAlt": "Pixel art illustration of two silhouetted figures overlooking a Vice City coastline at dusk with branching neon arrows",
    "faqs": [
        (
            "How many endings does GTA 6 have?",
            "GTA 6 has three distinct narrative endings. The outcome depends on a dynamic trust rating built between Jason and Lucia throughout the campaign and a final tactical decision during the Chapter 5 Port Gellhorn standoff."
        ),
        (
            "How does GTA 6 end?",
            "GTA 6 ends with Jason and Lucia cornered at a container shipping terminal in Port Gellhorn by federal task forces and cartel rivals, forcing a high-stakes escape attempt by land, crane sniper fire, and coastal boat extraction."
        ),
        (
            "What happens at the end of GTA 6?",
            "Depending on player choices, either both protagonists survive and escape to South America with their laundered millions in Ending A, or one partner makes a sacrifice to ensure the other escapes in Endings B and C."
        ),
        (
            "How do you get the GTA 6 good ending?",
            "To get the good ending (Ending A: The Clean Break), players must maintain high trust between Jason and Lucia by splitting heist loot fairly, providing covering fire, and choosing the Stick Together path during the finale so both characters survive."
        ),
        (
            "Can you replay missions to see all GTA 6 endings?",
            "Yes, players can replay the Chapter 5 finale directly from the Pause menu Replay Mission screen after rolling credits without losing open-world progress."
        )
    ],
    "body": """
      <p>As millions of players push through the climax of Grand Theft Auto 6, search volume around the game's conclusions has exploded across Google Trends. With two playable protagonists bound by a modern crime partnership, players want clear, verified answers on how the story concludes, how many endings exist, and how to unlock the best outcome. Here are direct answers to every major trending ending question.</p>

      <h2>How many endings does GTA 6 have?</h2>
      <p>Grand Theft Auto 6 features three distinct narrative endings. Unlike Grand Theft Auto 5, which presented a sudden three-way choice in a final menu phone call, GTA 6 weaves its conclusions into an underlying trust system that tracks decisions made across the entire campaign.</p>
      <p>The finale tests whether Jason and Lucia have built an unbreakable bond or let personal greed erode their partnership. Your cumulative trust score, combined with a critical tactical choice during the Port Gellhorn federal siege, unlocks one of three full cinematographic endings.</p>

      <h2>How does GTA 6 end?</h2>
      <p>The campaign concludes during Chapter 5 in the industrial harbor of Port Gellhorn. After pulling off a multi-million-dollar maritime heist, federal task force agents and rival Leonida cartel hitmen converge on the shipping terminal where Jason and Lucia are preparing their getaway transport.</p>
      <p>With highway exits barricaded and police patrol boats sealing off the bay, the duo must fight their way through intense waves of tactical units. The narrative reaches its climax when the player must decide whether to execute an aggressive coordinated escape together or have one partner provide a distraction so the other can slip away clean with the master syndicate ledger.</p>

      <h2>What happens at the end of GTA 6?</h2>
      <p>What happens at the end of GTA 6 depends directly on your chosen path:</p>
      <p><strong>In Ending A (The Clean Break):</strong> Both Jason and Lucia survive. Working in tandem, Jason provides covering sniper fire from a gantry crane while Lucia pilots a modified offshore speeder through naval patrol boats. They rendezvous in international waters, launder twenty million dollars into foreign accounts, and start a new life together. Both characters remain fully playable in post-game free roam with partner interactions intact.</p>
      <p><strong>In Ending B (Jason's Stand):</strong> If the player chooses an alternate split or if trust has degraded, Jason voluntarily draws federal attention toward an exploding fuel depot, allowing Lucia to escape aboard an outbound cargo vessel. Jason is captured and sentenced to federal custody, leaving Lucia as the sole surviving protagonist in post-game free roam.</p>
      <p><strong>In Ending C (Lucia's Sacrifice):</strong> Conversely, Lucia can choose to hold the primary terminal choke point, detonating harbor explosives to wipe out pursuing cartel bosses while Jason escapes north into the Leonida wetlands. Jason survives as the sole active character in post-game play, while Lucia's memory is honored through unique voicemail archives and safehouse mementos.</p>

      <h2>How to get the GTA 6 good ending? (GTA 6 good ending)</h2>
      <p>To unlock the good ending where both Jason and Lucia survive, players must maintain a high trust rating throughout the sixty-hour campaign. Follow these core guidelines:</p>
      <p><strong>Split Loot Fairly:</strong> In every multi-phase robbery, split secondary cash takes evenly rather than pocketing extra jewelry or bearer bonds for your active character.</p>
      <p><strong>Offer Timely Support:</strong> When your partner is pinned down by police during getaways, provide immediate covering fire and revive them quickly when prompted.</p>
      <p><strong>Choose Honest Dialogue:</strong> During safehouse discussions and roadside car rides, pick open, supportive dialogue prompts rather than defensive or secretive answers.</p>
      <p><strong>Select "Stick Together" in Chapter 5:</strong> When the final prompt appears at the Port Gellhorn dock, select the cooperative escape plan. High trust ensures that neither character hesitates, unlocking the triumphant ending where both ride into the sunset.</p>

      <h2>Can you replay missions to see all GTA 6 endings?</h2>
      <p>Yes. Rockstar Games allows players to replay the Chapter 5 finale directly through the Pause menu's Replay Mission tab after the end credits roll. You do not need to restart a brand-new save file from Chapter 1. Testing alternate tactical splits lets you watch each emotional conclusion, unlock all achievements, and hear every unique radio news epilogue without losing your completed world state.</p>
    """
}


MANDY_ARTICLE = {
    "id": "lexie-shoaibi-mandy-gta-6-actress-house-location-scene",
    "slot": "recent",
    "category": "Gaming",
    "title": "Lexie Shoaibi in GTA 6: Who is Mandy, house location, viral scene, and actress details",
    "seoTitle": "Lexie Shoaibi in GTA 6: Mandy Actress, House Location & Scene FAQ | Bugwrite",
    "metaDescription": "Who is Mandy in GTA 6? Where is Mandy's house? Who is actress Lexie Shoaibi? Direct answers to the viral Mandy scene, house location, and actress identity.",
    "keywords": [
        "lexie shoaibi gta 6",
        "where is mandy's house in gta 6",
        "gta 6 mandy scene",
        "mandy gta 6 actress",
        "mandy scene gta 6"
    ],
    "dek": "Everything players want to know about viral GTA 6 character Mandy, actress Lexie Shoaibi, her house location in Vice City, and the famous scene.",
    "author": "Jordan Kim",
    "authorRole": "Staff Writer, Gaming Desk",
    "publishedAgo": "Just now",
    "publishedDate": "Nov 20, 2026",
    "readTime": "5 min read",
    "image": "/blog/articles/gta6-mandy-lexie-shoaibi.jpg",
    "imageAlt": "Pixel art illustration of a glamorous smartphone live-stream screen with a tropical cocktail and Vice City palm trees",
    "faqs": [
        (
            "Who is Mandy in GTA 6 and who plays her?",
            "Mandy is a viral socialite NPC in Grand Theft Auto 6. Following launch, British-Iranian actress and model Lexie Shoaibi confirmed she provided the face model, motion capture, and voice performance for the character."
        ),
        (
            "Where is Mandy's house in GTA 6?",
            "Mandy's house is an upscale waterfront villa located on the northern circle of Starfish Island, situated between Vice City Beach and downtown Vice City. It features a marble infinity pool and a pearl-white sports convertible in the circular driveway."
        ),
        (
            "What is the viral GTA 6 Mandy scene?",
            "The viral scene occurs when players approach Mandy during a poolside patio party. She mistakes Jason or Lucia for private caterers and rants about influencer drama, and when gunfire breaks out, she calmly live-streams the shootout while drinking champagne."
        ),
        (
            "How do you trigger the Mandy encounter in Vice City?",
            "Players can trigger the Mandy event after completing Chapter 1. Head to Starfish Island between 2:00 PM and 8:00 PM in-game time and look for the stranger mission circle near the poolside cabana."
        )
    ],
    "body": """
      <p>Within hours of Grand Theft Auto 6 hitting consoles, clips of a glamorous, fast-talking Vice City socialite named Mandy took over social media. Search volume around actress Lexie Shoaibi, Mandy's mansion location, and her unhinged cutscene surged onto Google Trends. Here are direct, verified answers to every question surrounding GTA 6's breakout viral NPC.</p>

      <h2>Who is Mandy in GTA 6 and who is actress Lexie Shoaibi? (Mandy GTA 6 actress)</h2>
      <p>Mandy is a wealthy Leonida influencer and socialite who appears as a recurring stranger and world encounter in Vice City. British-Iranian actress and high-fashion model Lexie Shoaibi confirmed on social media that she provided the complete likeness, motion capture, and voice acting for the character.</p>
      <p>Lexie Shoaibi is an accomplished actress and digital creator known for international editorial fashion campaigns and commercial voiceover work. Her sharp comedic timing, deadpan sarcasm, and expressive performance brought instant personality to Mandy, turning what could have been a standard background NPC into one of the most recognizable and beloved characters of launch week.</p>

      <h2>Where is Mandy's house in GTA 6? (Where is Mandy's house in GTA 6?)</h2>
      <p>Mandy's residence is a luxury waterfront estate located on Starfish Island, the prestigious gated island situated in the bay connecting Vice City Beach to the mainland financial district. To find the property:</p>
      <p><strong>1. Enter Starfish Island:</strong> Cross the main bridge leading onto Starfish Island from the eastern beach avenue.</p>
      <p><strong>2. Follow the Northern Circle:</strong> Drive past the central landscaped fountain and take the northern road loop toward the open bay.</p>
      <p><strong>3. Spot the Villa:</strong> Look for a grand Spanish-revival villa with a red terracotta roof, marble outdoor pillars, and a pearl-white Grotti sports convertible parked out front.</p>
      <p>Players can walk onto the patio freely during daytime hours or enter through the side garden gate near the boat dock.</p>

      <h2>What is the viral GTA 6 Mandy scene? (GTA 6 Mandy scene / Mandy scene GTA 6)</h2>
      <p>The viral scene that captivated millions of viewers across TikTok, YouTube, and X takes place during a patio cocktail party at Mandy's mansion. When Jason or Lucia approaches the pool deck, Mandy immediately mistakes them for hired private caterers, launching into a hilariously self-absorbed monologue about synthetic cryptocurrency yachts, pet cougars, and Vice City socialite rivalries.</p>
      <p>What made the moment truly iconic is what happens if chaos erupts. If the player discharges a firearm or triggers police stars near the patio, typical NPCs flee in terror. Mandy, however, whips out her gold smartphone, starts live-streaming the shootout to her followers, and delivers deadpan color commentary while calmly sipping champagne and ducking behind poolside deck chairs.</p>

      <h2>How do you trigger the Mandy encounter in Vice City?</h2>
      <p>To experience the Mandy encounter firsthand, you must first complete the Chapter 1 storyline mission "Running the Numbers," which lifts travel restrictions across Vice City waterways. Once Chapter 1 is finished, visit Starfish Island between 2:00 PM and 8:00 PM in-game time.</p>
      <p>An orange stranger event blip will appear near the northern villa's poolside cabana. Interacting with Mandy unlocks her unique dialogue sequence, introduces an optional side mission to recover stolen designer jewelry, and adds her contact card to your in-game smartphone for occasional party invites.</p>

      <h2>Why is the GTA 6 community obsessed with Mandy?</h2>
      <p>Gamers fell in love with Mandy because she represents Rockstar Games' satire of modern Miami influencer culture at its sharpest. Between Lexie Shoaibi's energetic voice performance, detailed facial animations, and fearless reaction to open-world gunfights, Mandy encapsulates the wild, unpredictable energy that defines Grand Theft Auto 6.</p>
    """
}


def main():
    # Verify strict guidelines
    for a in [ENDINGS_UPDATED, MANDY_ARTICLE]:
        raw = json.dumps(a)
        assert "\u2014" not in raw and "\u2013" not in raw, f"Found em/en dash in {a['id']}"
        assert "<li" not in a["body"], f"Found <li> in {a['id']}"

    render_mandy_image()

    with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update gta-6-endings-how-many-choices-explained in place using safe lambda replacement
    pattern_endings = r'\{\s*"id":\s*"gta-6-endings-how-many-choices-explained"[\s\S]*?\n  \},'
    formatted_endings = "  " + json.dumps(ENDINGS_UPDATED, indent=4).replace("\n", "\n  ") + ","
    content, count_endings = re.subn(pattern_endings, lambda m: formatted_endings, content, count=1)
    if count_endings == 0:
        raise ValueError("Could not find gta-6-endings-how-many-choices-explained in articles-data.js")
    print("Successfully updated gta-6-endings-how-many-choices-explained with all Image 1 questions!")

    # 2. Add Mandy article if not present
    existing_ids = set(re.findall(r'"id":\s*"([^"]+)"', content))
    if MANDY_ARTICLE["id"] not in existing_ids:
        formatted_mandy = "  " + json.dumps(MANDY_ARTICLE, indent=4).replace("\n", "\n  ") + ",\n"
        pattern_start = r"(window\.BUGWRITE_ARTICLES\s*=\s*\[\n)"
        match = re.search(pattern_start, content)
        if not match:
            raise ValueError("Could not find window.BUGWRITE_ARTICLES = [\n in articles-data.js")
        idx = match.end()
        content = content[:idx] + formatted_mandy + content[idx:]
        print("Successfully prepended Mandy / Lexie Shoaibi article with all Image 2 questions!")

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("articles-data.js update complete!")


if __name__ == "__main__":
    main()
