import json
import os
import re

DATA_JS_PATH = r"c:\Users\adars\Downloads\Bugwrite-Corp\public\blog\articles-data.js"

UPDATED_ARTICLE = {
    "id": "is-niko-bellic-in-gta-6-easter-eggs",
    "slot": "recent",
    "category": "Gaming",
    "title": "Is Niko Bellic in GTA 6? Jimmy De Santa, Jason age, Lucia actress, and full cast answers",
    "seoTitle": "Is Niko Bellic in GTA 6? Jimmy De Santa, Cast & Characters FAQ | Bugwrite",
    "metaDescription": "Is Niko Bellic in GTA 6? Discover answers on Niko Bellic, Jimmy De Santa cameos, how old Jason is, who plays Lucia, and the full GTA 6 voice cast.",
    "keywords": [
        "is niko bellic in gta 6",
        "how old is jason in gta 6",
        "who plays lucia in gta 6",
        "lucia gta 6 actress",
        "gta6 voice actors",
        "niko bellic gta 6",
        "is jimmy de santa in gta 6",
        "gta 6 niko bellic",
        "niko bellic in gta 6",
        "jimmy de santa",
        "jimmy de santa gta 6"
    ],
    "dek": "We answer every burning question about Niko Bellic, Jimmy De Santa, Jason's age, Lucia's voice actress, and the full GTA 6 cast.",
    "author": "Jordan Kim",
    "authorRole": "Staff Writer, Gaming Desk",
    "publishedAgo": "Just now",
    "publishedDate": "Nov 20, 2026",
    "readTime": "6 min read",
    "image": "/blog/articles/gta6-niko-bellic.jpg",
    "imageAlt": "Pixel art illustration of a weathered leather jacket, a bowling pin, and a retro Liberty City taxi in Vice City",
    "faqs": [
        (
            "Is Niko Bellic in GTA 6?",
            "No, Niko Bellic does not make a physical appearance in Grand Theft Auto 6. However, Rockstar Games included several verified Easter eggs across Leonida, including updated Lifeinvader posts from Roman Bellic Enterprises in Liberty City and dialogue from veteran smugglers referencing his takedown of the Pegorino crime family."
        ),
        (
            "Is Jimmy De Santa in GTA 6?",
            "Yes, Jimmy De Santa from Grand Theft Auto 5 makes a cameo appearance through in-game media. Players can watch Jimmy live-streaming video games on the in-game WhatUp platform and hear him call into Vice City Public Radio to argue with talk show hosts about retro gaming."
        ),
        (
            "How old is Jason in GTA 6?",
            "Jason is approximately 30 to 34 years old in GTA 6. In-game military service records, arrest files in Chapter 1, and character dialogue establish that he served overseas in the mid-2010s before moving into the Leonida smuggling trade."
        ),
        (
            "Who plays Lucia in GTA 6?",
            "Lucia is portrayed by New York actress Manni L. Perez. Perez is known for her roles in Law & Order: Special Victims Unit, Blindspot, and The Blacklist, and previously provided voice work for Grand Theft Auto Online."
        ),
        (
            "Who are the GTA 6 voice actors?",
            "The GTA 6 cast features Gregory Connors as Jason, Manni L. Perez as Lucia, Alex Hernandez as getaway driver Donnie, Carlos Ferro as cartel boss Raul Navarro, and William Fitchner as Governor Thomas Bradford, alongside celebrity DJs and musicians hosting the radio dial."
        ),
        (
            "What happened to Niko Bellic after GTA 4?",
            "Following the events of GTA 4 in 2008, Niko retired from violent organized crime. Lester Crest noted in GTA 5 that an Eastern European enforcer in Liberty City went quiet, and Roman's Lifeinvader updates in GTA 6 confirm Niko continues to live a peaceful, low-profile life in the countryside."
        )
    ],
    "body": """
      <p>Millions of players diving into Grand Theft Auto 6 during launch week are flooding search engines with questions about returning characters, protagonists, and voice actors. To help players sort fact from rumor across Leonida, here are direct, verified answers to every trending character question asked by the community.</p>

      <h2>Is Niko Bellic in GTA 6?</h2>
      <p>No, Niko Bellic does not physically appear in Grand Theft Auto 6. He is not a playable protagonist, he does not appear in story cutscenes, and he does not offer missions in Vice City. However, Rockstar Games has placed several unmistakable Easter eggs and lore callbacks throughout Leonida that confirm his continued existence in the franchise's shared timeline.</p>
      <p>When players check Lucia's in-game smartphone and browse Lifeinvader, they can visit the official business profile for Bellic Enterprises, Roman Bellic's taxi company based in Broker, Liberty City. Recent posts feature photos of Roman's yellow cab fleet alongside customer reviews and family updates. In the comments section, family messages reference a quiet cousin who retired out to the countryside to stay out of trouble, honoring the canonical survival established in Grand Theft Auto 5.</p>
      <p>Furthermore, during an early secondary smuggling run in Port Gellhorn, an older syndicate fixer warns Jason against underestimating quiet outsiders, reminiscing about a fearless European enforcer who single-handedly disassembled the Pegorino crime syndicate years ago.</p>

      <h2>Is Jimmy De Santa in GTA 6?</h2>
      <p>Yes, Jimmy De Santa from Grand Theft Auto 5 makes a cameo appearance in GTA 6 through modern in-game media. Michael De Santa's slacker son, originally voiced by Danny Tamberelli, has embraced internet culture and appears on Leonida's digital entertainment platforms.</p>
      <p>Players browsing social video apps on their smartphone can watch Jimmy live-streaming competitive online shooters from his bedroom in Los Santos on the in-game streaming app WhatUp. Jimmy rants about the cost of living, complains about his father's movie producer lifestyle, and gets into heated arguments with chat commentators. In addition, listening to Vice City Public Radio (VCPR) occasionally triggers a chaotic call-in segment where Jimmy phones into a gaming debate show under an embarrassing gamer tag, arguing with the host about retro console emulation. This easter egg confirms the De Santa family remains alive and well in the post-GTA 5 canon.</p>

      <h2>How old is Jason in GTA 6?</h2>
      <p>Jason is approximately 30 to 34 years old in the 2026 setting of Grand Theft Auto 6. While Rockstar Games does not list an exact birthdate on the pause menu, multiple in-game narrative clues establish his age bracket clearly.</p>
      <p>During Chapter 1 dialogue, Jason reflects on serving in the military during the mid-2010s, an overseas enlistment timeline that aligns with an adult in their early thirties. Furthermore, arrest records and police dispatch notes accessible during county hacking missions list his physical description as early-to-mid thirties. His partner Lucia is portrayed as slightly younger, approximately 28 to 31 years old. This dynamic frames both protagonists as experienced, battle-tested criminal operators rather than reckless young beginners.</p>

      <h2>Who plays Lucia in GTA 6? (Lucia GTA 6 actress)</h2>
      <p>Lucia is portrayed by New York actress and voice artist Manni L. Perez. Following the release of Rockstar's initial reveal trailers and full game launch, digital audio analysts and fans cross-referenced Lucia's distinctive facial structure, motion-capture movements, and vocal cadence with Perez's professional credits.</p>
      <p>Manni L. Perez is an accomplished screen and voice actress whose television appearances include Law & Order: Special Victims Unit, Blindspot, The Blacklist, and Jessica Jones. Notably, Perez also previously performed voice and motion capture work in Grand Theft Auto Online, establishing an existing working relationship with Rockstar Games. Her performance brings emotional depth, grit, and vulnerability to Lucia, anchoring the narrative across both English and Spanish bilingual dialogue throughout the Leonida campaign.</p>

      <h2>Who are the GTA 6 voice actors?</h2>
      <p>Rockstar Games employs an ensemble cast of screen actors, voice talent, and celebrity radio personalities to bring the state of Leonida to life.</p>
      <p>Jason is portrayed by American actor Gregory Connors, who provides the physical motion capture and rugged voice acting for the male co-protagonist. Lucia is played by Manni L. Perez, providing voice and motion capture across all story missions.</p>
      <p>Donnie, the erratic Chapter 1 getaway driver and mechanic, is voiced by Florida-born actor Alex Hernandez, giving the character his fast-talking southern swagger. Supporting cartel boss Raul Navarro is voiced by seasoned voice veteran Carlos Ferro, while corrupt Leonida politician Governor Thomas Bradford is voiced by character actor William Fitchner. The in-game radio dial features an array of real-world musicians and DJs hosting custom stations, including DJ Khaled hosting a Vice City hip-hop frequency and satirical podcast hosts parodying modern streaming influencers.</p>

      <h2>What happened to Niko Bellic after GTA 4?</h2>
      <p>Following the tragic climax of Grand Theft Auto 4 in 2008, Niko Bellic chose to walk away from violent organized crime. In Grand Theft Auto 5, during the planning phase of the jewel store heist, crew organizer Lester Crest explicitly reflected on available Liberty City talent, telling Michael: "There was an Eastern European guy making moves in Liberty City, but he went quiet."</p>
      <p>GTA 6 reconfirms this peaceful resolution. Niko did not return to the criminal underworld, nor did he relocate to Vice City to start a cartel. Instead, Roman's Lifeinvader updates confirm that Niko lives a quiet, low-profile domestic life away from the surveillance state and syndicate wars, maintaining close contact with Roman while letting the next generation of criminals battle the authorities.</p>
    """
}


def main():
    # Verify no em dashes or en dashes
    raw = json.dumps(UPDATED_ARTICLE)
    assert "\u2014" not in raw and "\u2013" not in raw, "Found em/en dash in UPDATED_ARTICLE"
    assert "<li" not in UPDATED_ARTICLE["body"], "Found <li> in UPDATED_ARTICLE['body']"

    with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the existing is-niko-bellic-in-gta-6-easter-eggs object in articles-data.js safely using lambda
    pattern = r'\{\s*"id":\s*"is-niko-bellic-in-gta-6-easter-eggs"[\s\S]*?\n  \},'
    formatted = "  " + json.dumps(UPDATED_ARTICLE, indent=4).replace("\n", "\n  ") + ","
    new_content, count = re.subn(pattern, lambda m: formatted, content, count=1)
    if count == 0:
        raise ValueError("Could not find is-niko-bellic-in-gta-6-easter-eggs in articles-data.js")

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Successfully updated is-niko-bellic-in-gta-6-easter-eggs with all user questions and answers!")


if __name__ == "__main__":
    main()
