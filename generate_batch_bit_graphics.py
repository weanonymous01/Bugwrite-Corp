import os
from PIL import ImageDraw
import generate_bit_graphics as bg

c = bg.c
make_sprite = bg.make_sprite

# ============================================================
# ADDITIONAL CUSTOM EDITORIAL PIXEL SPRITES FOR 64 NEW TOPICS
# ============================================================

def sp_outlook_teams():
    def _f(d, im):
        # Blue Outlook envelope + violet Teams chat bubble with alert dot (44x26)
        d.rounded_rectangle([3, 4, 24, 21], radius=2, fill=c("#2b7de9"))
        d.rectangle([5, 6, 22, 19], fill=c("#ffffff"))
        d.line([(5, 7), (13, 13)], fill=c("#2b7de9"), width=2)
        d.line([(22, 7), (13, 13)], fill=c("#2b7de9"), width=2)
        d.rounded_rectangle([22, 7, 40, 22], radius=3, fill=c("#5b5fc7"))
        d.rectangle([25, 11, 37, 13], fill=c("#d6d8ff"))
        d.rectangle([25, 15, 33, 17], fill=c("#ffffff"))
        d.ellipse([33, 3, 41, 11], fill=c("#e84c4c"))
        d.rectangle([37, 5, 37, 7], fill=c("#ffffff"))
        d.point((37, 9), fill=c("#ffffff"))
    return make_sprite(44, 26, _f)


def sp_ai_spark_cube():
    def _f(d, im):
        # Clean geometric AI core processor with glowing star core (38x26)
        d.rounded_rectangle([8, 3, 29, 22], radius=4, fill=c("#202636"))
        d.rounded_rectangle([10, 5, 27, 20], radius=3, fill=c("#343e59"))
        # 4-point editorial spark inside
        d.polygon([(18, 6), (20, 11), (25, 12), (20, 14), (18, 19), (16, 14), (11, 12), (16, 11)], fill=c("#66d9ff"))
        d.ellipse([17, 11, 20, 14], fill=c("#ffffff"))
        for y in (7, 12, 17):
            d.rectangle([4, y, 7, y + 1], fill=c("#8da2cc"))
            d.rectangle([30, y, 33, y + 1], fill=c("#8da2cc"))
    return make_sprite(38, 26, _f)


def sp_code_editor():
    def _f(d, im):
        # Clean IDE coding window with syntax-highlighted lines & AI cursor (44x26)
        d.rounded_rectangle([2, 2, 41, 23], radius=2, fill=c("#1d2230"))
        d.rectangle([2, 2, 41, 6], fill=c("#31394f"))
        d.point((5, 4), fill=c("#f05a5a"))
        d.point((7, 4), fill=c("#f5c451"))
        d.point((9, 4), fill=c("#45d483"))
        # Sidebar
        d.rectangle([2, 6, 10, 23], fill=c("#252b3d"))
        for sy in (9, 12, 15, 18):
            d.rectangle([4, sy, 8, sy], fill=c("#6b7899"))
        # Code lines
        for yy, x1, x2, col in [
            (9, 13, 24, "#7aa2f7"), (11, 15, 32, "#45d483"),
            (13, 15, 28, "#f5c451"), (15, 13, 36, "#c099ff"),
            (17, 15, 26, "#7dcfff"), (19, 13, 22, "#f07178")
        ]:
            d.rectangle([x1, yy, x2, yy], fill=c(col))
    return make_sprite(44, 26, _f)


def sp_agent_orbit():
    def _f(d, im):
        # Autonomous central hub + 4 orbiting task nodes (42x26)
        cx, cy = 21, 13
        orbit = [(8, 7), (34, 7), (8, 19), (34, 19)]
        for ox, oy in orbit:
            d.line([(cx, cy), (ox, oy)], fill=c("#94a3c7"), width=1)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=c("#5468e8"))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c("#8596ff"))
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=c("#ffffff"))
        cols = ["#45d483", "#f5c451", "#f06a9e", "#4fc3f7"]
        for (ox, oy), col in zip(orbit, cols):
            d.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=c(col))
            d.point((ox, oy), fill=c("#ffffff"))
    return make_sprite(42, 26, _f)


def sp_website_checker():
    def _f(d, im):
        # Browser window with green/red uptime ping status bar (44x26)
        d.rounded_rectangle([2, 2, 41, 23], radius=2, fill=c("#e8edf5"))
        d.rectangle([2, 2, 41, 7], fill=c("#cbd5e6"))
        d.rectangle([10, 4, 34, 5], fill=c("#ffffff"))
        d.rectangle([4, 9, 39, 21], fill=c("#ffffff"))
        # Uptime vertical status ticks
        for i in range(10):
            tx = 6 + i * 3
            col = "#eb5757" if i in (6, 7) else "#2ec471"
            d.rectangle([tx, 12, tx + 1, 18], fill=c(col))
    return make_sprite(44, 26, _f)


def sp_password_vault():
    def _f(d, im):
        # Heavy steel digital safe / password vault with dial & asterisks (40x26)
        d.rounded_rectangle([5, 2, 34, 23], radius=3, fill=c("#33415c"))
        d.rounded_rectangle([8, 5, 31, 20], radius=2, fill=c("#4c5d7d"))
        d.ellipse([13, 7, 25, 19], fill=c("#cfd8e8"))
        d.ellipse([15, 9, 23, 17], fill=c("#253045"))
        d.line([(19, 13), (23, 10)], fill=c("#f7c948"), width=2)
        d.ellipse([18, 12, 20, 14], fill=c("#ffffff"))
    return make_sprite(40, 26, _f)


def sp_vpn_tunnel():
    def _f(d, im):
        # Encrypted VPN shield + dual-endpoint tunnel line (44x26)
        d.rounded_rectangle([3, 8, 14, 18], radius=2, fill=c("#3a4a66"))
        d.rectangle([5, 10, 12, 16], fill=c("#82c4ff"))
        d.rounded_rectangle([30, 8, 41, 18], radius=2, fill=c("#3a4a66"))
        d.rectangle([32, 10, 39, 16], fill=c("#5ee39a"))
        d.rectangle([14, 11, 30, 15], fill=c("#4a8af4"))
        d.ellipse([17, 7, 27, 19], fill=c("#27ae60"))
        d.line([(20, 13), (22, 15)], fill=c("#ffffff"), width=2)
        d.line([(22, 15), (25, 10)], fill=c("#ffffff"), width=2)
    return make_sprite(44, 26, _f)


def sp_windows_desktop():
    def _f(d, im):
        # Clean Windows 11 style 4-pane blue grid + wrench badge (42x26)
        d.rounded_rectangle([4, 2, 37, 21], radius=2, fill=c("#232a38"))
        d.rectangle([6, 4, 35, 19], fill=c("#3d8ef0"))
        # Four sleek window panes
        d.rectangle([13, 6, 19, 11], fill=c("#bfe0ff"))
        d.rectangle([21, 6, 27, 11], fill=c("#ffffff"))
        d.rectangle([13, 13, 19, 17], fill=c("#8cc4ff"))
        d.rectangle([21, 13, 27, 17], fill=c("#bfe0ff"))
        d.rectangle([17, 21, 24, 23], fill=c("#4c566b"))
    return make_sprite(42, 26, _f)


def sp_android_fold():
    def _f(d, im):
        # Unfolded modern foldable smartphone + crisp green mascot dome (42x26)
        d.rounded_rectangle([4, 3, 37, 22], radius=3, fill=c("#27303b"))
        d.rectangle([6, 5, 20, 20], fill=c("#e8f8ee"))
        d.rectangle([21, 5, 35, 20], fill=c("#d2f2df"))
        # Center fold crease
        d.line([(20, 5), (20, 20)], fill=c("#9bc7ae"), width=1)
        # Green dome head in left pane
        d.pieslice([8, 9, 18, 19], 180, 360, fill=c("#34c76f"))
        d.point((11, 12), fill=c("#ffffff"))
        d.point((15, 12), fill=c("#ffffff"))
        # Floating bubble card on right pane
        d.rounded_rectangle([24, 8, 33, 16], radius=2, fill=c("#3b82f6"))
        d.rectangle([26, 10, 31, 11], fill=c("#ffffff"))
    return make_sprite(42, 26, _f)


def sp_ios_glass():
    def _f(d, im):
        # Translucent Liquid Glass modern iPhone UI with glowing orb (36x28)
        d.rounded_rectangle([9, 2, 26, 26], radius=4, fill=c("#2b3242"))
        d.rounded_rectangle([10, 3, 25, 25], radius=3, fill=c("#7bb4ff"))
        d.rectangle([11, 4, 24, 24], fill=c("#b8dcff"))
        # Translucent glass cards
        d.rounded_rectangle([12, 8, 23, 14], radius=2, fill=c("#ffffff"))
        d.ellipse([15, 9, 20, 13], fill=c("#ff6eb4"))
        d.rounded_rectangle([12, 16, 23, 22], radius=2, fill=c("#e8f4ff"))
        d.rectangle([14, 18, 21, 19], fill=c("#5a9cf5"))
    return make_sprite(36, 28, _f)


def sp_power_datacenter():
    def _f(d, im):
        # Data center racks + bold yellow lightning energy bolt (44x26)
        for rx in (4, 14, 24):
            d.rounded_rectangle([rx, 4, rx + 8, 22], radius=1, fill=c("#2a3242"))
            for ry in (7, 11, 15, 19):
                d.rectangle([rx + 2, ry, rx + 6, ry + 1], fill=c("#5b6b87"))
                d.point((rx + 2, ry), fill=c("#45d483"))
        # Giant golden lightning bolt right side
        d.polygon([(36, 3), (30, 13), (35, 13), (31, 23), (41, 11), (36, 11)], fill=c("#ffd43b"))
    return make_sprite(44, 26, _f)


def sp_gpu_5090():
    def _f(d, im):
        # Massive triple-fan flagship graphics card (RTX 5090) (46x22)
        d.rounded_rectangle([2, 4, 43, 18], radius=2, fill=c("#1f232b"))
        d.rectangle([4, 6, 41, 16], fill=c("#333947"))
        # Three cooling fans
        for fx in (10, 22, 34):
            d.ellipse([fx - 4, 7, fx + 4, 15], fill=c("#161920"))
            d.ellipse([fx - 2, 9, fx + 2, 13], fill=c("#566075"))
            d.point((fx, 11), fill=c("#32cc6e"))
        # Gold PCIe connector edge bottom
        d.rectangle([10, 18, 28, 20], fill=c("#f2c238"))
    return make_sprite(46, 22, _f)


def sp_ssd_drive():
    def _f(d, im):
        # Sleek NVMe SSD stick + 212GB fill meter (44x22)
        d.rounded_rectangle([3, 5, 40, 17], radius=2, fill=c("#1f2633"))
        d.rectangle([5, 7, 36, 15], fill=c("#2f394d"))
        # Memory chips
        for cx in (8, 16, 24):
            d.rectangle([cx, 8, cx + 5, 14], fill=c("#171c26"))
        # Progress bar glowing pink/cyan
        d.rectangle([8, 11, 29, 12], fill=c("#ff66b2"))
        # Gold M.2 pins right
        for py in range(7, 15, 2):
            d.rectangle([37, py, 40, py], fill=c("#f5c23b"))
    return make_sprite(44, 22, _f)


def sp_headset():
    def _f(d, im):
        # Modern over-ear wireless gaming headset (36x28)
        d.arc([6, 3, 29, 24], 180, 360, fill=c("#252a36"), width=4)
        d.arc([8, 5, 27, 22], 180, 360, fill=c("#4a5368"), width=2)
        # Left & right earcups
        d.rounded_rectangle([4, 13, 11, 24], radius=3, fill=c("#1c202b"))
        d.rectangle([6, 15, 9, 22], fill=c("#4e8ef7"))
        d.rounded_rectangle([24, 13, 31, 24], radius=3, fill=c("#1c202b"))
        d.rectangle([26, 15, 29, 22], fill=c("#4e8ef7"))
        # Boom mic
        d.line([(8, 23), (16, 26)], fill=c("#545e75"), width=2)
        d.ellipse([15, 25, 18, 27], fill=c("#32cc6e"))
    return make_sprite(36, 28, _f)


def sp_arc_snow_radar():
    def _f(d, im):
        # Cold Snap icy radar scope + snowflake crystal (38x26)
        d.ellipse([7, 2, 30, 24], fill=c("#1d3145"))
        d.ellipse([9, 4, 28, 22], fill=c("#294866"))
        d.line([(18, 5), (18, 21)], fill=c("#7ed6ff"), width=2)
        d.line([(10, 13), (26, 13)], fill=c("#7ed6ff"), width=2)
        d.line([(13, 8), (23, 18)], fill=c("#ffffff"), width=1)
        d.line([(23, 8), (13, 18)], fill=c("#ffffff"), width=1)
        d.ellipse([16, 11, 20, 15], fill=c("#ffffff"))
    return make_sprite(38, 26, _f)


def sp_lol_sword():
    def _f(d, im):
        # Crossed fantasy blade & glowing crystal crest (38x28)
        d.polygon([(19, 2), (24, 9), (19, 22), (14, 9)], fill=c("#4da6ff"))
        d.polygon([(19, 4), (22, 9), (19, 19), (16, 9)], fill=c("#b8e0ff"))
        d.rectangle([11, 18, 27, 20], fill=c("#f2c238"))
        d.rectangle([17, 20, 21, 26], fill=c("#8c5828"))
        d.ellipse([17, 17, 21, 21], fill=c("#ffe46b"))
    return make_sprite(38, 28, _f)


def sp_hlx_crate():
    def _f(d, im):
        # Iconic industrial orange science crate with bold glowing mark (36x26)
        d.rounded_rectangle([6, 3, 29, 23], radius=3, fill=c("#d96218"))
        d.rounded_rectangle([8, 5, 27, 21], radius=2, fill=c("#f28029"))
        # Geometric chevron/A-shape symbol inside
        d.line([(13, 18), (18, 8)], fill=c("#1c1a18"), width=2)
        d.line([(18, 8), (22, 18)], fill=c("#1c1a18"), width=2)
        d.line([(16, 13), (12, 18)], fill=c("#1c1a18"), width=2)
    return make_sprite(36, 26, _f)


def sp_atlantis_relic():
    def _f(d, im):
        # Golden compass artifact & ancient temple archway (40x26)
        d.rectangle([5, 4, 34, 8], fill=c("#c99d5b"))
        for px in (8, 16, 24, 30):
            d.rectangle([px, 8, px + 2, 22], fill=c("#dec085"))
        d.rectangle([4, 21, 35, 24], fill=c("#a67e43"))
        # Turquoise glowing relic center
        d.polygon([(20, 9), (25, 14), (20, 19), (15, 14)], fill=c("#2ec4c9"))
        d.polygon([(20, 11), (23, 14), (20, 17), (17, 14)], fill=c("#a8f5f7"))
    return make_sprite(40, 26, _f)


def sp_strategy_hex():
    def _f(d, im):
        # Civilization/XCOM inspired interlocking hex map tiles (42x26)
        def hex_poly(cx, cy, r):
            return [(cx - r, cy), (cx - r // 2, cy - r), (cx + r // 2, cy - r),
                    (cx + r, cy), (cx + r // 2, cy + r), (cx - r // 2, cy + r)]
        d.polygon(hex_poly(14, 13, 7), fill=c("#45b876"))
        d.polygon(hex_poly(26, 9, 7), fill=c("#4a8ef0"))
        d.polygon(hex_poly(26, 18, 7), fill=c("#f0b84a"))
        d.ellipse([24, 16, 28, 20], fill=c("#ffffff"))
    return make_sprite(42, 26, _f)


def sp_dna_biotech():
    def _f(d, im):
        # Isomorphic Labs AI drug discovery double helix + capsule (42x26)
        for i in range(6):
            xx = 6 + i * 5
            y1 = 6 if i % 2 == 0 else 19
            y2 = 19 if i % 2 == 0 else 6
            d.line([(xx, y1), (xx, y2)], fill=c("#b8c9e8"), width=1)
            d.ellipse([xx - 2, y1 - 2, xx + 2, y1 + 2], fill=c("#4695eb"))
            d.ellipse([xx - 2, y2 - 2, xx + 2, y2 + 2], fill=c("#e866a0"))
        # Clean capsule on right
        d.rounded_rectangle([34, 7, 40, 19], radius=3, fill=c("#ffffff"))
        d.rounded_rectangle([34, 7, 40, 13], radius=3, fill=c("#34c77b"))
    return make_sprite(42, 26, _f)


def sp_ipo_bell():
    def _f(d, im):
        # Nasdaq golden opening bell + stock ticker screen (42x26)
        d.rounded_rectangle([4, 4, 24, 21], radius=2, fill=c("#1b263b"))
        d.line([(7, 17), (12, 13), (16, 15), (21, 8)], fill=c("#38d982"), width=2)
        # Golden IPO bell right
        d.pieslice([26, 6, 39, 20], 180, 360, fill=c("#f5c23b"))
        d.rectangle([26, 13, 39, 19], fill=c("#e0a61e"))
        d.rectangle([24, 19, 41, 21], fill=c("#ffd966"))
        d.ellipse([31, 21, 34, 23], fill=c("#b87d0b"))
    return make_sprite(42, 26, _f)


def sp_stock_candles():
    def _f(d, im):
        # Financial candlestick chart card (44x26)
        d.rounded_rectangle([3, 2, 40, 23], radius=2, fill=c("#181e29"))
        candles = [
            (9, 7, 15, "#36c975"), (15, 9, 17, "#36c975"),
            (21, 6, 14, "#eb5757"), (27, 10, 19, "#eb5757"),
            (33, 12, 20, "#eb5757")
        ]
        for cx, y1, y2, col in candles:
            d.line([(cx + 1, y1 - 2), (cx + 1, y2 + 2)], fill=c(col), width=1)
            d.rectangle([cx, y1, cx + 3, y2], fill=c(col))
    return make_sprite(44, 26, _f)


def sp_crm_cards():
    def _f(d, im):
        # Clean CRM pipeline board / contact cards (44x26)
        for ix, col in [(4, "#4a8ef0"), (17, "#826aed"), (30, "#34c77b")]:
            d.rounded_rectangle([ix, 3, ix + 10, 22], radius=2, fill=c("#ffffff"))
            d.rectangle([ix, 3, ix + 10, 7], fill=c(col))
            d.rectangle([ix + 2, 10, ix + 8, 12], fill=c("#cbd5e6"))
            d.rectangle([ix + 2, 15, ix + 6, 17], fill=c("#dbe3f0"))
    return make_sprite(44, 26, _f)


def sp_export_map():
    def _f(d, im):
        # Microchip + global shipping barrier line (44x26)
        d.rounded_rectangle([4, 6, 18, 20], radius=2, fill=c("#294538"))
        d.rectangle([7, 9, 15, 17], fill=c("#45c482"))
        # Red customs barrier dash
        d.line([(22, 3), (22, 23)], fill=c("#e84c4c"), width=2)
        # Destination server tower
        d.rounded_rectangle([27, 5, 40, 21], radius=2, fill=c("#33415c"))
        for ry in (8, 12, 16):
            d.rectangle([29, ry, 38, ry + 1], fill=c("#82b4ff"))
    return make_sprite(44, 26, _f)


# Sprite palette shortcuts
S = {
    "outlook": sp_outlook_teams(),
    "ai_cube": sp_ai_spark_cube(),
    "code": sp_code_editor(),
    "agent": sp_agent_orbit(),
    "checker": sp_website_checker(),
    "vault": sp_password_vault(),
    "vpn": sp_vpn_tunnel(),
    "win11": sp_windows_desktop(),
    "android": sp_android_fold(),
    "ios": sp_ios_glass(),
    "power": sp_power_datacenter(),
    "gpu": sp_gpu_5090(),
    "ssd": sp_ssd_drive(),
    "headset": sp_headset(),
    "arc": sp_arc_snow_radar(),
    "lol": sp_lol_sword(),
    "hlx": sp_hlx_crate(),
    "atlantis": sp_atlantis_relic(),
    "hex": sp_strategy_hex(),
    "dna": sp_dna_biotech(),
    "ipo": sp_ipo_bell(),
    "candles": sp_stock_candles(),
    "crm": sp_crm_cards(),
    "export": sp_export_map(),
    "phone_cloud": bg.sp_apple_phone_cloud(),
    "terminal": bg.sp_artex_terminal(),
    "server": bg.sp_java_server(),
    "chip": bg.sp_nvidia_chip(),
    "trophy": bg.sp_awards_trophy(),
    "dualsense": bg.sp_dualsense(),
    "xbox": bg.sp_xbox_controller(),
    "vice": bg.sp_vice_polaroid(),
    "bridge": bg.sp_leonida_bridge(),
    "shield": bg.sp_fbi_shield(),
    "clouds": bg.sp_salesforce_clouds(),
    "clock": bg.sp_clock_midnight(),
    "score": bg.sp_metacritic_97(),
}

BILL, CAR_P, CAR_Y, STAR, WARN, LOCK, BOLT, CHECK, CARD, PALM, TAG, PLUS, KEY = (
    bg.BILL, bg.CAR_P, bg.CAR_Y, bg.STAR, bg.WARN, bg.LOCK, bg.BOLT,
    bg.CHECK, bg.CARD, bg.PALM, bg.TAG, bg.PLUS, bg.KEY
)

BATCH_ART = [
    # === 21 TECH & SECURITY ===
    ("microsoft-outlook-teams-copilot-outage.jpg", "#5b9be8", "#937ce6", "#f4f7fd", "#4b7be0", "spike", "outlook", [WARN, BOLT, LOCK]),
    ("why-so-many-internet-outages-2026.jpg", "#e07268", "#7d9be8", "#faf5f5", "#d94f4f", "spike", "checker", [WARN, BOLT, CARD]),
    ("ai-finding-software-vulnerabilities-faster.jpg", "#7d6be6", "#4db8a4", "#f5f4fb", "#6956d9", "rising", "terminal", [KEY, BOLT, CHECK]),
    ("openai-gpt-6-2-astra-sol-cyber-2026.jpg", "#4ca8b8", "#8f7ae6", "#f3f9fb", "#348ea3", "rising", "ai_cube", [STAR, BOLT, KEY]),
    ("best-ai-coding-tools-2026.jpg", "#558be6", "#58c49a", "#f4f8fc", "#3c72d6", "bars", "code", [BOLT, STAR, CHECK]),
    ("ai-agents-explained-how-they-work.jpg", "#7c72e8", "#5ab8e8", "#f6f5fc", "#5e54d6", "wave", "agent", [BOLT, STAR, CHECK]),
    ("what-are-coding-agents-developers.jpg", "#48b0a8", "#6d8ce8", "#f3faf9", "#30968e", "rising", "code", [KEY, BOLT, STAR]),
    ("how-to-check-if-website-is-down.jpg", "#58b88a", "#6ca4e8", "#f4faf7", "#2ea36c", "wave", "checker", [CHECK, WARN, BOLT]),
    ("cloudflare-aws-azure-internet-dependence.jpg", "#eb9e52", "#6a95e0", "#fcf8f2", "#d9822b", "spike", "clouds", [WARN, BOLT, LOCK]),
    ("what-is-a-zero-day-vulnerability.jpg", "#d95d5d", "#8d74e0", "#fcf4f4", "#c94040", "spike", "shield", [WARN, KEY, LOCK]),
    ("how-hackers-exploit-unpatched-software.jpg", "#d96b52", "#6d7d96", "#fbf5f2", "#c74e38", "bars", "terminal", [LOCK, WARN, BOLT]),
    ("best-password-managers-2026.jpg", "#4896d9", "#5bc48c", "#f3f8fc", "#2f7cc2", "bars", "vault", [KEY, LOCK, CHECK]),
    ("best-vpn-services-windows-2026.jpg", "#487de6", "#4bc4b0", "#f3f7fd", "#3368d1", "wave", "vpn", [LOCK, CHECK, BOLT]),
    ("windows-11-common-errors-fixes.jpg", "#4e96e8", "#7db8f0", "#f4f8fd", "#2d78d6", "bars", "win11", [CHECK, WARN, BOLT]),
    ("android-17-features-changes-devices.jpg", "#46c27e", "#76c9a8", "#f3faf6", "#2aa662", "rising", "android", [STAR, PLUS, CHECK]),
    ("ios-27-features-siri-liquid-glass.jpg", "#73a8f0", "#d48ce8", "#f6f8fd", "#5482e0", "wave", "ios", [STAR, BOLT, CHECK]),
    ("why-ai-data-centers-consume-electricity.jpg", "#f0b44c", "#667894", "#fcf9f2", "#d98c24", "rising", "power", [BOLT, WARN, BILL]),
    ("what-are-ai-chips-why-companies-fight.jpg", "#4ab885", "#e8c45e", "#f4faf6", "#2fa16c", "rising", "chip", [BOLT, BILL, STAR]),
    ("how-ransomware-works-business-protection.jpg", "#d95555", "#e89f54", "#fcf4f4", "#c73c3c", "spike", "shield", [LOCK, BILL, WARN]),
    ("is-personal-data-used-to-train-ai.jpg", "#6a7ee0", "#e0829c", "#f6f6fc", "#5466c9", "bars", "vault", [LOCK, WARN, KEY]),
    ("best-free-ai-tools-productivity-2026.jpg", "#58b8d9", "#9e7ee8", "#f4f9fc", "#3d96b8", "rising", "ai_cube", [STAR, CHECK, PLUS]),

    # === 19 GAMING ===
    ("gta-6-eight-game-awards-nominations.jpg", "#e6b855", "#c46ed9", "#faf7f2", "#d4961c", "bars", "trophy", [STAR, CAR_P, CAR_Y]),
    ("gta-6-pc-release-date-windows.jpg", "#c274e0", "#5aa8e6", "#f8f4fb", "#9b4ec4", "bars", "code", [PALM, CAR_P, STAR]),
    ("gta-6-standard-vs-ultimate-edition.jpg", "#e8886b", "#b874e3", "#fcf5f3", "#d65a47", "bars", "dualsense", [BILL, TAG, STAR]),
    ("gta-6-download-size-storage-guide.jpg", "#7a7ce8", "#e87ab0", "#f6f6fc", "#5d5ed4", "bars", "ssd", [BOLT, WARN, CHECK]),
    ("gta-6-map-vice-city-leonida-regions.jpg", "#47c4c9", "#f0a47a", "#f3fafb", "#2da1a8", "wave", "bridge", [PALM, CAR_Y, STAR]),
    ("gta-6-characters-jason-lucia-cast.jpg", "#e372b0", "#f0b86b", "#fcf4f8", "#d44c92", "rising", "vice", [CAR_P, STAR, BILL]),
    ("gta-6-gameplay-features-details.jpg", "#b574e6", "#f2c272", "#f8f4fb", "#d9586a", "rising", "dualsense", [CAR_P, CAR_Y, BOLT]),
    ("manni-l-perez-gta-6-lucia-actress.jpg", "#e87c9e", "#877ce6", "#fcf4f7", "#d4537d", "rising", "trophy", [STAR, PALM, CHECK]),
    ("gta-6-vs-gta-5-biggest-changes.jpg", "#58b89c", "#e884b4", "#f4faf8", "#399c7e", "bars", "vice", [CAR_Y, CAR_P, PLUS]),
    ("can-gta-6-win-goty-before-release.jpg", "#e8c05a", "#6e7ee0", "#faf8f2", "#d19b1e", "rising", "trophy", [STAR, CHECK, WARN]),
    ("arc-raiders-update-2-6-0-cold-snap.jpg", "#56a8d9", "#8fd4eb", "#f3f9fc", "#3588bd", "wave", "arc", [BOLT, STAR, CHECK]),
    ("arc-raiders-beginner-tips-survival.jpg", "#4d8ec9", "#69b89c", "#f3f8fc", "#3474b0", "bars", "arc", [CHECK, PLUS, STAR]),
    ("best-ps5-games-2026.jpg", "#4778e3", "#7cb8f5", "#f3f7fd", "#3062cc", "rising", "dualsense", [STAR, PLUS, CHECK]),
    ("league-of-legends-patch-26-23-notes.jpg", "#4e8be0", "#e6ba55", "#f4f7fc", "#356ec4", "bars", "lol", [BOLT, STAR, PLUS]),
    ("best-gaming-headsets-2026.jpg", "#6a74e6", "#4ab8c4", "#f5f6fc", "#4d58cc", "wave", "headset", [STAR, CHECK, TAG]),
    ("nvidia-rtx-5090-prices-shortage-2026.jpg", "#46b874", "#d96c5a", "#f4faf6", "#2ea15d", "rising", "gpu", [BILL, WARN, BILL]),
    ("half-life-3-game-awards-2026-hlx.jpg", "#e8853c", "#5e6a7d", "#fcf6f2", "#d46a1c", "spike", "hlx", [STAR, WARN, BOLT]),
    ("tomb-raider-legacy-of-atlantis-2027-delay.jpg", "#42b0b8", "#d9a95b", "#f3faf9", "#2a9199", "wave", "atlantis", [STAR, WARN, KEY]),
    ("firaxis-layoffs-civilization-xcom-2026.jpg", "#5b89c9", "#d97a68", "#f5f7fb", "#4470b0", "drop", "hex", [WARN, BILL, LOCK]),

    # === 24 BUSINESS ===
    ("nvidia-q3-fy27-earnings-115-billion.jpg", "#3cb872", "#e6c963", "#f3faf5", "#249c57", "rising", "chip", [BILL, STAR, BILL]),
    ("anthropic-ipo-nasdaq-ant-2026.jpg", "#d98c5f", "#6a82d9", "#fcf7f3", "#c46d3b", "rising", "ipo", [BILL, STAR, CHECK]),
    ("amazon-google-ai-investment-2026.jpg", "#e89e4c", "#5294e6", "#fcf8f2", "#3b7ad6", "rising", "clouds", [BILL, BOLT, STAR]),
    ("us-ai-chip-export-restrictions-2026.jpg", "#5873b8", "#d9625b", "#f4f6fb", "#c94640", "bars", "export", [LOCK, WARN, KEY]),
    ("is-ai-boom-becoming-a-bubble-2026.jpg", "#8f74e0", "#e89468", "#f8f5fc", "#7358cc", "spike", "candles", [BILL, WARN, BOLT]),
    ("why-tech-stocks-falling-november-2026.jpg", "#d95b5b", "#6b7c9c", "#fcf4f4", "#c94040", "drop", "candles", [WARN, BILL, BOLT]),
    ("ai-industry-data-center-spending-2026.jpg", "#4d8be0", "#e6b455", "#f4f8fc", "#3570c7", "rising", "power", [BILL, BOLT, BILL]),
    ("ai-infrastructure-costs-startups-2026.jpg", "#e08458", "#7c84d9", "#fcf6f3", "#c9683a", "rising", "server", [BILL, WARN, KEY]),
    ("isomorphic-labs-5-billion-series-c.jpg", "#4aa6e8", "#e072a8", "#f4f9fd", "#3389cc", "rising", "dna", [BILL, STAR, CHECK]),
    ("ai-startups-changing-software-model.jpg", "#6a7ce8", "#4bc49b", "#f5f6fc", "#4f62d1", "rising", "agent", [BILL, BOLT, STAR]),
    ("why-saas-companies-adding-ai-features.jpg", "#54a2e6", "#8d74e3", "#f4f9fd", "#3b86cc", "bars", "clouds", [PLUS, STAR, BILL]),
    ("what-is-an-ai-agent-business.jpg", "#54b89c", "#7486e6", "#f3faf8", "#389c7f", "rising", "agent", [BILL, CHECK, BOLT]),
    ("cloud-computing-competing-ai-customers.jpg", "#4c96e6", "#58c2b8", "#f3f8fd", "#337ac9", "bars", "clouds", [BILL, BOLT, STAR]),
    ("business-impact-cloud-software-outages.jpg", "#e06c60", "#7c90b8", "#fcf5f4", "#c94c40", "spike", "checker", [BILL, WARN, LOCK]),
    ("cybersecurity-spending-business-priority.jpg", "#4a75cc", "#4ab88c", "#f4f7fc", "#345eb5", "rising", "shield", [BILL, LOCK, CHECK]),
    ("how-data-breaches-affect-companies-financially.jpg", "#d95c5c", "#e8a85a", "#fcf4f4", "#c44141", "drop", "shield", [BILL, WARN, LOCK]),
    ("cost-to-build-ai-saas-startup-2026.jpg", "#5ab885", "#6a95e6", "#f4faf7", "#3a9c68", "bars", "code", [BILL, CARD, CHECK]),
    ("best-crm-software-small-businesses-2026.jpg", "#4f8de6", "#8c74e3", "#f4f8fd", "#3872cc", "bars", "crm", [CHECK, STAR, CARD]),
    ("best-ai-tools-small-business-owners.jpg", "#4cb8a8", "#e6ba5a", "#f3faf9", "#329c8c", "rising", "crm", [STAR, BOLT, CHECK]),
    ("why-tech-companies-restructuring-2026.jpg", "#6b7ea8", "#d98470", "#f5f6fa", "#53658f", "drop", "candles", [BILL, WARN, KEY]),
    ("vc-evaluating-ai-startups-2026.jpg", "#529e82", "#7885e0", "#f4faf7", "#398268", "rising", "ipo", [BILL, CHECK, STAR]),
    ("why-companies-invest-private-ai-models.jpg", "#5078c9", "#8c6ed9", "#f4f7fc", "#395eb0", "bars", "vault", [LOCK, KEY, CHECK]),
    ("cost-of-running-large-ai-model.jpg", "#e8a24c", "#747ed9", "#fcf8f2", "#cf832b", "rising", "gpu", [BILL, BOLT, WARN]),
    ("us-export-controls-global-semiconductors.jpg", "#5278bd", "#d98952", "#f4f7fb", "#3a5fa3", "wave", "export", [WARN, BILL, LOCK]),
]


def render_batch():
    positions = [
        (195, 130, -20, 9),
        (1085, 135, 16, 9),
        (1090, 565, -14, 8),
    ]
    for fname, g1, g2, paper, accent, chart, sp_key, acc_list in BATCH_ART:
        canvas = bg.make_gradient_bg(g1, g2)
        bg.draw_inner_frame(canvas, paper, accent, chart_style=chart)
        hero = S[sp_key]
        hscale = 11 if hero.width <= 44 else 10
        bg.paste_sprite(canvas, hero, bg.W // 2, bg.H // 2 + 6, pix_scale=hscale, angle=0, outline=True, shadow=True)
        for sp, (ax, ay, ang, sc) in zip(acc_list, positions):
            bg.paste_sprite(canvas, sp, ax, ay, pix_scale=sc, angle=ang, outline=True, shadow=True)
        out_path = os.path.join(bg.OUT_DIR, fname)
        canvas.convert("RGB").save(out_path, "JPEG", quality=91, optimize=True)
    print(f"Generated all {len(BATCH_ART)} new bit-graphics images cleanly!")


if __name__ == "__main__":
    render_batch()
