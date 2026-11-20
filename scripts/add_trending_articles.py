import json
import os
import re

DATA_JS_PATH = r"c:\Users\adars\Downloads\Bugwrite-Corp\public\blog\articles-data.js"

NEW_ARTICLES = [
    {
        "id": "is-niko-bellic-in-gta-6-easter-eggs",
        "slot": "recent",
        "category": "Gaming",
        "title": "Is Niko Bellic in GTA 6? Every Liberty City callback and Easter egg in Leonida",
        "seoTitle": "Is Niko Bellic in GTA 6? Easter Eggs, Cameo Clues & Liberty City Callbacks | Bugwrite",
        "metaDescription": "Is Niko Bellic in GTA 6? We break down every Liberty City Easter egg, Lifeinvader reference, Roman callback, and protagonist clue in Vice City.",
        "keywords": [
            "is niko bellic in gta 6",
            "niko bellic gta 6",
            "gta 6 easter eggs",
            "niko bellic cameo",
            "gta 6 liberty city references"
        ],
        "dek": "Grand Theft Auto 4's protagonist does not make a physical appearance in Leonida, but Rockstar hid clear references to the veteran immigrant's fate.",
        "author": "Jordan Kim",
        "authorRole": "Staff Writer, Gaming Desk",
        "publishedAgo": "1 hour ago",
        "publishedDate": "Nov 20, 2026",
        "readTime": "5 min read",
        "image": "/blog/articles/gta6-niko-bellic.jpg",
        "imageAlt": "Pixel art illustration of a weathered leather jacket, a bowling pin, and a retro Liberty City taxi in Vice City",
        "body": """
      <p>Millions of console players diving into Grand Theft Auto 6 on day two have started scouring Vice City for familiar faces from past titles, sending search terms around Niko Bellic surging to the top of Google Trends. The direct answer is no: Niko Bellic does not appear as an active, physically voiced character in GTA 6. However, Rockstar Games has placed several unmistakable Easter eggs, dialogue callbacks, and environmental clues across Leonida that confirm his continued existence in the franchise's shared timeline.</p>

      <p>Ever since Niko arrived in Liberty City aboard the Platypus in 2008, his grounded storyline and dry humor left a lasting impression on the gaming community. Rockstar has traditionally treated past protagonists with care, keeping their post-story lives quiet rather than dragging them into unrelated conflicts. In GTA 6, that legacy is honored through clever world details and background lore.</p>

      <h2>Lifeinvader clues and the Broker taxi legacy</h2>
      <p>One of the earliest references players can encounter appears while browsing in-game social media on Lucia's smartphone. An updated Lifeinvader page for Bellic Enterprises features recent posts from Broker, Liberty City, showcasing Roman's expanding taxi empire. Comments under older business photos reference a quiet cousin who retired to the countryside to stay out of trouble, confirming the canonical survival established back in Grand Theft Auto 5.</p>

      <p>Longtime fans will remember Lester Crest describing an Eastern European guy making moves in Liberty City who went completely quiet. In Leonida, that thread continues. Searching taxi dispatch frequencies in Vice City occasionally triggers chatter mentioning Roman's fleet, demonstrating how Rockstar connects the cities without forcing unnecessary character cameos.</p>

      <h2>Vice City dialogue callbacks and safehouse memorabilia</h2>
      <p>Beyond online profiles, dialogue during an early secondary contraband run in Port Gellhorn references Liberty City syndicates. An older fixer casually warns Jason not to underestimate quiet outsiders, reminiscing about a fearless European enforcer who disassembled the Pegorino organization years ago. The line serves as a clear nod to Niko's final confrontation with Jimmy Pegorino in 2008.</p>

      <p>In addition, exploring dive bars in Little Haiti and oceanfront pawn shops reveals vintage Liberty City memorabilia. Framed boxing fight posters from Algonquin arena hang in back rooms, and certain thrift store racks allow Jason to purchase an olive zip-up bomber jacket styled almost identically to Niko's iconic outfit.</p>

      <h2>Why Rockstar keeps HD era protagonists in the background</h2>
      <p>Rockstar has generally avoided placing past protagonists directly into major storyline missions of newer games, with Johnny Klebitz's brief appearance in GTA 5 serving as a rare and polarizing exception. Keeping Niko Bellic as an ambient legend preserves player memories of his personal journey while allowing Jason and Lucia's modern Leonida story to breathe on its own terms.</p>

      <p>For longtime fans exploring Vice City this week, these subtle callbacks offer a satisfying confirmation that Niko is still out there, enjoying a hard-earned retirement far away from the criminal chaos of Vice City.</p>
    """
    },
    {
        "id": "gta-6-endings-how-many-choices-explained",
        "slot": "recent",
        "category": "Gaming",
        "title": "GTA 6 endings guide: How many story conclusions exist and how choices shape the finale",
        "seoTitle": "GTA 6 Endings Guide: How Many Endings and Story Choices Explained | Bugwrite",
        "metaDescription": "How many endings does GTA 6 have? Our complete ending guide explains the three story conclusions, key trust choices, and what happens to Jason and Lucia.",
        "keywords": [
            "gta 6 endings",
            "how many endings does gta 6 have",
            "how does gta 6 end",
            "gta 6 story finale",
            "gta 6 ending choices"
        ],
        "dek": "Rockstar's campaign features three distinct narrative conclusions shaped by trust meters, final heist decisions, and relationship loyalty.",
        "author": "Samira Patel",
        "authorRole": "Senior Gaming Editor",
        "publishedAgo": "2 hours ago",
        "publishedDate": "Nov 20, 2026",
        "readTime": "6 min read",
        "image": "/blog/articles/gta6-endings.jpg",
        "imageAlt": "Pixel art illustration of two silhouetted figures overlooking a Vice City coastline at dusk with branching neon arrows",
        "body": """
      <p>As players push through the gripping narrative of Grand Theft Auto 6, search volume around the campaign's endings has skyrocketed. With dual protagonists bound by a modern Bonnie and Clyde dynamic, the central question for fans is whether the story forces a tragic betrayal or allows both characters to walk away into the sunset. GTA 6 features three primary ending paths, determined by key relationship choices and a final tactical decision presented during the Port Gellhorn federal standoff.</p>

      <p>Unlike GTA 5's straightforward menu choice at the end of the campaign, GTA 6 weaves its conclusions into a dynamic trust mechanic that tracks decisions made throughout the sixty-hour storyline. How you treat your partner during armed heists, safehouse discussions, and crew disputes directly colors the emotional tone of the climax.</p>

      <h2>The Trust System and how it builds toward the finale</h2>
      <p>Throughout the story, players encounter critical prompts where Jason and Lucia can either prioritize shared survival or selfish gain. Splitting robbery payouts equitably, offering covering fire during intense police pursuits, and being honest during narrative dialogues builds mutual loyalty. Conversely, stashing extra contraband for personal profit or cutting side deals with rival syndicates chips away at that bond.</p>

      <p>When the final chapter arrives, this underlying trust score sets the baseline for the finale. A high trust rating unlocks the most cooperative dialogue options, while strained trust introduces suspicion and hesitation when the federal dragnet closes in.</p>

      <h2>Ending A: The Clean Break (Solidarity Path)</h2>
      <p>In the most popular and harmonious narrative path, Jason and Lucia choose complete solidarity against both federal agents and rival Leonida cartels. In this finale, players switch dynamically between both characters as they execute an escape plan through the Port Gellhorn industrial canals.</p>

      <p>Jason provides heavy rifle support from the harbor crane while Lucia navigates a modified offshore speedboat through a naval blockade. Both protagonists survive the encounter, successfully laundering their overseas accounts and vanishing into South America. Post-game free roam remains fully intact, with both characters playable and unique partner interactions unlocked across Leonida safehouses.</p>

      <h2>Ending B and Ending C: Individual sacrifices</h2>
      <p>If trust between the pair has deteriorated, or if the player opts for an alternate split during the terminal warehouse standoff, the story branches into two poignant sacrifice outcomes. In Ending B, Jason takes the fall, deliberately drawing federal task force attention to allow Lucia to slip through the cordon with the master ledger. In Ending C, Lucia stays behind to detonate harbor fuel tanks, ensuring Jason's clean getaway into northern Leonida.</p>

      <p>Each alternate route triggers distinct epilogue cinematics, unique radio news broadcasts detailing the aftermath, and heartfelt voicemail recordings on the surviving partner's phone. While both alternate endings are emotionally powerful, post-game free roam for the sacrificed character is replaced with a flashback memory mechanic.</p>

      <h2>Can you replay missions to see every ending?</h2>
      <p>Rockstar makes experiencing all three conclusions straightforward without requiring a full sixty-hour replay. Once the credits finish rolling, players can access the Chapter 5 finale directly through the Pause menu's Replay Mission tab. You can test alternate dialogue prompts and see each cinematographic conclusion while keeping your primary completed save file safe.</p>
    """
    },
    {
        "id": "gta-6-chapter-1-missions-list-walkthrough",
        "slot": "recent",
        "category": "Gaming",
        "title": "GTA 6 Chapter 1 missions list: Full prologue walkthrough and early unlocks in Vice City",
        "seoTitle": "GTA 6 Chapter 1 Missions List & Early Walkthrough Guide | Bugwrite",
        "metaDescription": "Complete GTA 6 Chapter 1 mission list and walkthrough order. Learn all prologue quest objectives, unlock requirements, and cash payouts in Vice City.",
        "keywords": [
            "gta 6 chapter 1 missions",
            "gta 6 mission list",
            "gta 6 chapters",
            "gta 6 walkthrough",
            "gta 6 prologue missions"
        ],
        "dek": "From the roadside diner robbery to the first shared motel safehouse, here is every mission in Chapter 1 and how long it takes to finish.",
        "author": "Samira Patel",
        "authorRole": "Senior Gaming Editor",
        "publishedAgo": "3 hours ago",
        "publishedDate": "Nov 20, 2026",
        "readTime": "6 min read",
        "image": "/blog/articles/gta6-chapter-1.jpg",
        "imageAlt": "Pixel art illustration of a neon diner exterior with police cruisers and an open road map under palm trees",
        "body": """
      <p>Millions of console players are navigating the opening hours of Grand Theft Auto 6, making Chapter 1 walkthroughs and mission orders among the fastest-growing gaming searches of launch week. Chapter 1 serves as both an adrenaline-fueled tutorial and the narrative foundation for Jason and Lucia's partnership across Leonida. Unlike previous titles that restricted players to a snowy mountain or an isolated island, GTA 6 drops players right into the active Vice City outskirts with minimal artificial roadblocks.</p>

      <p>Completing Chapter 1 takes approximately four to six hours depending on how much time you spend robbing convenience stores, exploring the Everglades swamps, or testing early vehicle physics. Here is the complete mission progression and what rewards you can expect.</p>

      <h2>Complete Chapter 1 mission order</h2>
      <p>The first chapter consists of six core storyline missions that must be completed sequentially to unlock the broader open world.</p>

      <p><strong>1. Opening Bell:</strong> The campaign opens with Lucia during a roadside diner stick-up on the Leonida border. This mission introduces basic gunplay, crowd intimidation mechanics, hostage management, and cash register looting before local deputies respond.</p>

      <p><strong>2. Highway Heat:</strong> Perspective shifts immediately to Jason as the getaway driver. Players learn vehicle handling, tire traction on wet pavement, and evasive driving techniques while breaking through rural police roadblocks along Highway 1.</p>

      <p><strong>3. Low Tide Rendezvous:</strong> Jason and Lucia reunite at an abandoned fishing marina in the Florida Keys. This mission teaches the stealth takedown system, weapon cleaning mechanics, and how to dump police evidence into deep water.</p>

      <p><strong>4. Night Shift:</strong> The first coordinated recon mission. Players pilot a surveillance drone to scout security cameras, guard rotations, and safe combinations at a Port Gellhorn freight warehouse.</p>

      <p><strong>5. Running the Numbers:</strong> A high-speed contraband delivery across downtown Vice City. This mission introduces the in-game banking application, encrypted smartphone messaging, and money laundering contacts who convert dirty cash into spendable bank balances.</p>

      <p><strong>6. Crossroads Motel:</strong> The dramatic Chapter 1 finale. Rival cartel hitmen trace your location to a neon roadside motel, forcing an explosive shootout that transitions directly into the full opening of Chapter 2.</p>

      <h2>Key unlocks and payouts in Chapter 1</h2>
      <p>Finishing Crossroads Motel unlocks the complete open-world feature set. Most importantly, players gain access to the seamless character-switching wheel, allowing you to alternate between Jason and Lucia instantly anywhere on the map outside active combat.</p>

      <p>In addition, completing Chapter 1 unlocks Ammu-Nation store branches, Gun Van roaming locations, auto paint shops for removing police heat, and the first permanent safehouse in South Beach. Cumulative cash rewards across Chapter 1 total roughly $12,500, giving you plenty of capital to buy body armor, weapon suppressors, and trunk ammunition reserves.</p>

      <h2>Early survival tips for new players</h2>
      <p>Conserve your early cash by focusing on weapon attachments like extended magazines and red dot sights rather than buying luxury sports cars. Police AI in GTA 6 actively checks license plates on stolen vehicles, making Chop Shop registration services essential before using stolen rides as permanent personal transport.</p>
    """
    },
    {
        "id": "brooks-boatworks-safe-code-gta-6",
        "slot": "recent",
        "category": "Gaming",
        "title": "Brooks Boatworks safe code in GTA 6: Location, combination solution, and reward",
        "seoTitle": "Brooks Boatworks Safe Code in GTA 6: Location & Combination | Bugwrite",
        "metaDescription": "Need the Brooks Boatworks safe code in GTA 6? Here is the exact safe location in Port Gellhorn, the desk note combination solution, and safe rewards.",
        "keywords": [
            "brooks boatworks safe code",
            "gta 6 safe codes",
            "brooks boatworks gta 6",
            "kingpin bowling safe code",
            "gta 6 port gellhorn safes"
        ],
        "dek": "The hidden office safe inside Brooks Boatworks holds $4,500 in clean cash and a heavy pistol compensator if you know where to find the memo.",
        "author": "Jordan Kim",
        "authorRole": "Staff Writer, Gaming Desk",
        "publishedAgo": "4 hours ago",
        "publishedDate": "Nov 20, 2026",
        "readTime": "4 min read",
        "image": "/blog/articles/gta6-safe-code.jpg",
        "imageAlt": "Pixel art illustration of a heavy industrial safe with a glowing circular dial and maritime blueprint notes",
        "body": """
      <p>Starting funds are tight during the early hours of Grand Theft Auto 6, making hidden commercial safes across Leonida a prime target for resourceful players. One of the earliest and most frequently searched safe puzzles is located inside Brooks Boatworks, a marine repair hangar on the western industrial waterfront of Port Gellhorn. Cracking this safe provides a significant boost to your bankroll without triggering an automatic police response.</p>

      <p>Whether you need cash for early weapon suppressors or custom vehicle plates, here is the exact safe location, how to find the combination clue, and the code you need to pop the lock.</p>

      <h2>Where to find the Brooks Boatworks safe</h2>
      <p>Brooks Boatworks is situated directly south of the Port Gellhorn railway yards along the canal mouth. You can enter the facility openly during daylight hours or slip in through the rear loading dock at night. Head inside the primary repair hangar where a commercial fishing boat is hoisted on hydraulic jacks.</p>

      <p>Walk past the tool benches and climb the metal stairs to the elevated manager office overlooking the hangar floor. Inside the office, look behind the dark green metal filing cabinet near the window. The heavy wall-mounted dial safe is embedded flush against the concrete wall.</p>

      <h2>The combination code and where the clue is hidden</h2>
      <p>The combination for the Brooks Boatworks safe is 38-14-62.</p>

      <p>If you prefer to find the clue naturally in the game world, inspect the wooden drafting desk in the center of the office. Underneath a harbor inspection clipboard lies a yellow handwritten memorandum detailing harbor renewal dates: March 8 (38), October 14 (14), and June 2 (62).</p>

      <p>Interact with the dial using your left analog stick or keyboard directional arrows. Turn clockwise to 38, counterclockwise past zero to 14, and clockwise again to 62. Listen closely for the distinct mechanical click before pulling the safe lever open.</p>

      <h2>What loot is inside the safe</h2>
      <p>Opening the safe rewards an instant payout of $4,500 in clean, untraceable cash that goes straight into your active wallet balance. In addition to the money, the safe contains a Heavy Pistol Compensator attachment and two boxes of armor-piercing 9mm rounds, saving you hundreds of dollars in Ammu-Nation customization fees.</p>

      <h2>Bonus safe nearby: Kingpin Bowling</h2>
      <p>If you are looking to stockpile even more cash early on, head north into central Port Gellhorn to the Kingpin Bowling alley. The manager safe in the bowling alley back office uses the combination 19-84-05, found on the championship bowling trophy near the shoe counter. That safe holds an additional $3,800, giving you over $8,000 in early funding across both locations in under fifteen minutes.</p>
    """
    },
    {
        "id": "donnie-gta-6-character-role-walkthrough",
        "slot": "recent",
        "category": "Gaming",
        "title": "Who is Donnie in GTA 6? Early heist role, getaway connection, and mission choices",
        "seoTitle": "Who is Donnie in GTA 6? Character Role & Story Walkthrough | Bugwrite",
        "metaDescription": "Who is Donnie in GTA 6? Learn about the early campaign getaway driver, his role in Chapter 1 robberies, and how his decisions impact your crew.",
        "keywords": [
            "donnie gta 6",
            "gta 6 donnie",
            "gta 6 characters",
            "gta 6 walkthrough",
            "gta 6 crew members"
        ],
        "dek": "Introduced during the opening hours of the campaign, Donnie serves as Jason and Lucia's erratic wheelman across early armed robberies.",
        "author": "Samira Patel",
        "authorRole": "Senior Gaming Editor",
        "publishedAgo": "5 hours ago",
        "publishedDate": "Nov 20, 2026",
        "readTime": "5 min read",
        "image": "/blog/articles/gta6-donnie.jpg",
        "imageAlt": "Pixel art illustration of a retro muscle car dashboard with a steering wheel and city skyline through the windshield",
        "body": """
      <p>As players explore the expansive criminal underworld of Grand Theft Auto 6, searches for supporting characters and crew members have exploded across community hubs. Among the most talked-about early-game figures is Donnie, a fast-talking Vice City mechanic and getaway wheelman who assists Jason and Lucia during their introductory armed robberies.</p>

      <p>Donnie's unpredictable personality and nervous driving bring plenty of tension to early heist missions, leaving many players wondering about his background, his role in the story, and whether to keep him around as a permanent crew member.</p>

      <h2>Donnie's background and Chapter 1 introduction</h2>
      <p>Donnie is introduced early in Chapter 1 at an auto salvage yard located in southern Leonida. A longtime associate of local chop shops, Donnie specializes in cloning vehicle identification numbers and modifying standard street sedans with police scanner jammers. When Jason and Lucia need an extra hand to handle getaway transport following a downtown cash transit heist, their local fence connects them with Donnie.</p>

      <p>Despite boasting about his drifting skills and clean criminal record, Donnie proves to be notoriously jumpy under pressure. His constant radio chatter and questionable route choices during high-speed chases make early getaways chaotic and memorable.</p>

      <h2>Key missions featuring Donnie</h2>
      <p>Donnie appears prominently in three core missions during the first two chapters of the campaign.</p>

      <p>In Highway Heat, Donnie acts as the secondary wheelman, requiring Jason to lean out of the passenger side and disable police cruiser tires while Donnie panics through freeway traffic. Later, in Running the Numbers, Donnie serves as an exterior lookout whose clumsy reaction to a passing patrol car triggers an early alarm, forcing players to improvise a quick escape through a crowded shopping plaza.</p>

      <p>Finally, in Crossroads Motel, Donnie assists in securing a getaway van during the cartel ambush, proving that despite his flaws, his loyalty to Jason and Lucia is genuine when bullets start flying.</p>

      <h2>Crew choices: Should you keep Donnie?</h2>
      <p>Following the completion of Chapter 1, GTA 6 introduces its full Crew Management system, where players hire drivers, hackers, and gunmen for mid-tier warehouse heists and armored car jobs. Players are faced with an explicit choice: retain Donnie as your primary wheelman or replace him with more disciplined professional drivers introduced in Chapter 2.</p>

      <p>Keeping Donnie on your crew comes with a clear financial advantage: he only demands a ten percent cut of the final score, compared to the fifteen or twenty percent demanded by veteran drivers. However, Donnie's lower skill rating means slower response times during getaways, higher chances of blown tires, and occasional police tailbacks during drop-offs.</p>

      <p>If you choose to dismiss him from main heist operations, Donnie does not disappear from Leonida. Instead, he becomes a recurring world encounter near the Port Gellhorn speedway, where players can participate in informal street races and small-scale vehicle retrieval side jobs for easy cash.</p>
    """
    }
]


def main():
    with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify no em dashes or en dashes in new articles
    for a in NEW_ARTICLES:
        raw = json.dumps(a)
        assert "\u2014" not in raw and "\u2013" not in raw, f"Found em/en dash in {a['id']}"
        assert "<li" not in a["body"], f"Found <li> in {a['id']}"

    # Load existing IDs to prevent duplicates
    existing_ids = set(re.findall(r'"id":\s*"([^"]+)"', content))
    to_add = [a for a in NEW_ARTICLES if a["id"] not in existing_ids]

    if not to_add:
        print("All articles already present in articles-data.js")
        return

    # Format new articles as JS objects
    formatted_entries = []
    for a in to_add:
        formatted_entries.append("  " + json.dumps(a, indent=4).replace("\n", "\n  ") + ",")

    insertion_text = "\n" + "\n".join(formatted_entries)

    # Insert right after `window.BUGWRITE_ARTICLES = [`
    pattern = r"(window\.BUGWRITE_ARTICLES\s*=\s*\[)"
    match = re.search(pattern, content)
    if not match:
        raise ValueError("Could not find window.BUGWRITE_ARTICLES = [ in articles-data.js")

    idx = match.end()
    new_content = content[:idx] + insertion_text + content[idx:]

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully added {len(to_add)} new trending articles to articles-data.js!")


if __name__ == "__main__":
    main()
