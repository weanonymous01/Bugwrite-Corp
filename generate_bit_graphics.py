import os
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 1280, 720
SCALE = 8
PW, PH = W // SCALE, H // SCALE  # 160 x 90 virtual pixel grid

OUT_DIR = r"c:\Users\adars\Downloads\Bugwrite-Corp\public\blog\articles"
os.makedirs(OUT_DIR, exist_ok=True)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def make_gradient_bg(top_hex, bot_hex, grid_alpha=30):
    c1, c2 = hex_rgb(top_hex), hex_rgb(bot_hex)
    bg = Image.new("RGBA", (W, H))
    px = bg.load()
    for y in range(H):
        t = y / (H - 1)
        col = lerp_color(c1, c2, t) + (255,)
        for x in range(W):
            px[x, y] = col

    # Subtle graph-paper pixel grid texture across the gradient border (matches reference)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = 14
    line_col = (255, 255, 255, grid_alpha)
    for x in range(0, W, step):
        gd.line([(x, 0), (x, H)], fill=line_col, width=1)
    for y in range(0, H, step):
        gd.line([(0, y), (W, y)], fill=line_col, width=1)
    return Image.alpha_composite(bg, grid)


def draw_pixel_layer(canvas, draw_fn):
    layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_fn(d, layer)
    big = layer.resize((W, H), Image.Resampling.NEAREST)
    canvas.alpha_composite(big)


def draw_inner_frame(canvas, paper_hex, accent_hex, chart_style="rising"):
    """Clean pastel paper card + stepped editorial infographic (no noisy dots)."""
    paper = hex_rgb(paper_hex) + (255,)
    acc = hex_rgb(accent_hex)
    acc_solid = acc + (255,)
    acc_soft = acc + (82,)
    acc_mid = acc + (170,)

    def _draw(d, layer):
        # Clean inner editorial card inset inside gradient border
        x1, y1, x2, y2 = 12, 9, 147, 80
        d.rectangle([x1 - 1, y1 - 1, x2 + 1, y2 + 1], fill=(255, 255, 255, 240))
        d.rectangle([x1, y1, x2, y2], fill=paper)

        # Crisp L-axis inside frame (just like the red chart frame in the reference)
        ax_x, ax_y = x1 + 3, y2 - 3
        d.rectangle([ax_x, y1 + 4, ax_x + 1, ax_y], fill=acc_solid)
        d.rectangle([ax_x, ax_y - 1, x2 - 4, ax_y], fill=acc_solid)

        if chart_style == "rising":
            # Stepped diagonal staircase with shaded ribbon underneath (exact reference motif)
            steps = [
                (21, 61), (26, 56), (31, 51), (36, 45), (42, 39),
                (49, 32), (57, 26), (67, 22), (88, 22)
            ]
            for i in range(len(steps) - 1):
                sx1, sy1 = steps[i]
                sx2, sy2 = steps[i + 1]
                d.rectangle([sx1, sy1, sx2, sy1 + 3], fill=acc_soft)
                d.rectangle([sx1, sy1, sx2, sy1 + 1], fill=acc_solid)
                d.rectangle([sx2 - 1, min(sy1, sy2), sx2, max(sy1, sy2) + 1], fill=acc_solid)
            # Bottom jagged horizon area
            heights = [3, 5, 8, 7, 11, 10, 9, 12, 9, 11, 8, 10, 7, 9, 11, 8, 6, 8, 6, 9, 10, 7, 6, 5]
            for i, hh in enumerate(heights):
                bx = ax_x + 2 + i * 5
                if bx < x2 - 6:
                    d.rectangle([bx, ax_y - 2 - hh, min(bx + 4, x2 - 5), ax_y - 2], fill=acc_mid)
            # Right escalating thin vertical bars
            for i, bh in enumerate([5, 11, 18, 25, 34, 44]):
                bx = 117 + i * 4
                d.rectangle([bx, ax_y - 2 - bh, bx + 1, ax_y - 2], fill=acc_solid)

        elif chart_style == "spike":
            # Outage / alert peak curve
            pts = [
                (17, 74), (24, 74), (31, 72), (38, 73), (44, 67), (50, 56),
                (55, 29), (60, 19), (65, 26), (71, 44), (78, 53), (85, 48),
                (92, 60), (102, 68), (114, 71), (126, 73), (141, 74)
            ]
            for i in range(len(pts) - 1):
                px1, py1 = pts[i]
                px2, py2 = pts[i + 1]
                for xx in range(px1, px2 + 1):
                    t = (xx - px1) / max(1, (px2 - px1))
                    yy = int(py1 + (py2 - py1) * t)
                    d.rectangle([xx, yy, xx, ax_y - 2], fill=acc_soft)
                    d.rectangle([xx, yy - 1, xx, yy], fill=acc_solid)
            for i, bh in enumerate([6, 12, 20, 15, 28, 36]):
                bx = 117 + i * 4
                d.rectangle([bx, ax_y - 2 - bh, bx + 1, ax_y - 2], fill=acc_solid)

        elif chart_style == "drop":
            # Stepped price drop (-80%) or stock slide
            steps = [(21, 22), (38, 22), (48, 30), (58, 41), (70, 54), (86, 63), (110, 65)]
            for i in range(len(steps) - 1):
                sx1, sy1 = steps[i]
                sx2, sy2 = steps[i + 1]
                d.rectangle([sx1, sy1, sx2, sy1 + 3], fill=acc_soft)
                d.rectangle([sx1, sy1, sx2, sy1 + 1], fill=acc_solid)
                d.rectangle([sx2 - 1, min(sy1, sy2), sx2, max(sy1, sy2) + 1], fill=acc_solid)
            for i, bh in enumerate([38, 31, 24, 17, 11, 6]):
                bx = 117 + i * 4
                d.rectangle([bx, ax_y - 2 - bh, bx + 1, ax_y - 2], fill=acc_solid)
            heights = [9, 10, 8, 9, 7, 8, 6, 7, 5, 6, 5, 4, 5, 4, 3, 4, 3, 4, 3, 4, 3, 3, 2, 2]
            for i, hh in enumerate(heights):
                bx = ax_x + 2 + i * 5
                if bx < x2 - 6:
                    d.rectangle([bx, ax_y - 2 - hh, min(bx + 4, x2 - 5), ax_y - 2], fill=acc_soft)

        elif chart_style == "bars":
            # Clean comparison bars + right escalating bar chart
            for i, bw in enumerate([24, 40, 64, 32]):
                by = 20 + i * 7
                d.rectangle([21, by, 21 + bw, by + 2], fill=acc_soft)
                d.rectangle([21, by, 21 + min(bw, 14), by + 2], fill=acc_solid)
            for i, bh in enumerate([8, 16, 24, 33, 43, 28]):
                bx = 117 + i * 4
                d.rectangle([bx, ax_y - 2 - bh, bx + 1, ax_y - 2], fill=acc_solid)
            d.rectangle([ax_x + 2, ax_y - 6, x2 - 5, ax_y - 2], fill=acc_soft)

        elif chart_style == "wave":
            for xx in range(ax_x + 2, x2 - 5):
                yy = int(60 + 9 * math.sin(xx * 0.14) + 3 * math.cos(xx * 0.32))
                d.rectangle([xx, yy, xx, ax_y - 2], fill=acc_soft)
                d.rectangle([xx, yy - 1, xx, yy], fill=acc_solid)
            for i, bh in enumerate([6, 12, 18, 26, 34, 42]):
                bx = 117 + i * 4
                d.rectangle([bx, ax_y - 2 - bh, bx + 1, ax_y - 2], fill=acc_solid)

    draw_pixel_layer(canvas, _draw)


def add_sticker_outline(sprite, outline_color=(255, 255, 255, 230), pad=1):
    w, h = sprite.size
    out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sp = sprite.load()
    op = out.load()
    for y in range(h):
        for x in range(w):
            if sp[x, y][3] > 20:
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + pad + dx, y + pad + dy
                    if 0 <= nx < w + pad * 2 and 0 <= ny < h + pad * 2:
                        op[nx, ny] = outline_color
    out.paste(sprite, (pad, pad), sprite)
    return out


def paste_sprite(canvas, sprite, cx, cy, pix_scale=8, angle=0, outline=True, shadow=True):
    s = add_sticker_outline(sprite) if outline else sprite
    big = s.resize((s.width * pix_scale, s.height * pix_scale), Image.Resampling.NEAREST)
    if angle != 0:
        big = big.rotate(angle, resample=Image.Resampling.NEAREST, expand=True)

    x0 = int(cx - big.width // 2)
    y0 = int(cy - big.height // 2)

    if shadow:
        sh = Image.new("RGBA", big.size, (30, 28, 46, 0))
        alpha = big.split()[3].point(lambda a: int(a * 0.16))
        sh.putalpha(alpha)
        sh = sh.filter(ImageFilter.GaussianBlur(radius=7))
        canvas.alpha_composite(sh, (x0 + 5, y0 + 7))

    canvas.alpha_composite(big, (x0, y0))


def make_sprite(w, h, fn):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fn(d, im)
    return im


def c(h, a=255):
    return hex_rgb(h) + (a,)


# ============================================================
# RICH, SHADED, NO-HARSH-OUTLINE EDITORIAL PIXEL ART OBJECTS
# (High craft, soft multi-tone pixel shading like reference!)
# ============================================================

def sp_dualsense():
    def _f(d, im):
        # Smooth multi-tone PS5 DualSense silhouette (38x24)
        # Main white shell
        d.rounded_rectangle([4, 3, 33, 15], radius=5, fill=c("#e8ecf2"))
        d.rounded_rectangle([6, 4, 31, 13], radius=4, fill=c("#f7f9fc"))
        # Left & right grips
        d.polygon([(4, 10), (11, 10), (9, 22), (3, 21)], fill=c("#cfd6e2"))
        d.polygon([(5, 10), (10, 10), (8, 21), (4, 20)], fill=c("#eef1f6"))
        d.polygon([(26, 10), (33, 10), (34, 21), (28, 22)], fill=c("#cfd6e2"))
        d.polygon([(27, 10), (32, 10), (33, 20), (29, 21)], fill=c("#eef1f6"))
        # Dark center touchpad + face
        d.polygon([(11, 5), (26, 5), (28, 16), (9, 16)], fill=c("#232730"))
        d.rectangle([13, 4, 24, 10], fill=c("#eef2f8"))
        d.rectangle([13, 9, 24, 10], fill=c("#548bf5"))  # DualSense blue lightbar!
        # Thumbsticks
        d.ellipse([12, 11, 17, 16], fill=c("#161920"))
        d.ellipse([13, 12, 16, 15], fill=c("#3a404f"))
        d.ellipse([20, 11, 25, 16], fill=c("#161920"))
        d.ellipse([21, 12, 24, 15], fill=c("#3a404f"))
        # D-pad (left)
        d.rectangle([7, 7, 8, 11], fill=c("#7e8799"))
        d.rectangle([6, 8, 9, 10], fill=c("#7e8799"))
        # Action buttons (right)
        d.point((30, 7), fill=c("#48b878"))
        d.point((31, 9), fill=c("#e85c5c"))
        d.point((29, 9), fill=c("#d966c4"))
        d.point((30, 11), fill=c("#4a8af4"))
    return make_sprite(38, 24, _f)


def sp_xbox_controller():
    def _f(d, im):
        d.rounded_rectangle([4, 3, 33, 16], radius=5, fill=c("#22262e"))
        d.rounded_rectangle([6, 4, 31, 14], radius=4, fill=c("#303642"))
        # Grips
        d.polygon([(4, 10), (11, 10), (9, 22), (3, 21)], fill=c("#1c2026"))
        d.polygon([(5, 10), (10, 10), (8, 20), (4, 19)], fill=c("#2a303b"))
        d.polygon([(26, 10), (33, 10), (34, 21), (28, 22)], fill=c("#1c2026"))
        d.polygon([(27, 10), (32, 10), (33, 20), (29, 19)], fill=c("#2a303b"))
        # Glowing green Xbox guide button
        d.ellipse([17, 5, 20, 8], fill=c("#32cc6e"))
        d.point((18, 6), fill=c("#b8ffd2"))
        # Offset sticks
        d.ellipse([7, 7, 11, 11], fill=c("#14171c"))
        d.ellipse([8, 8, 10, 10], fill=c("#485161"))
        d.ellipse([21, 11, 25, 15], fill=c("#14171c"))
        d.ellipse([22, 12, 24, 14], fill=c("#485161"))
        # D-pad lower left
        d.rectangle([12, 11, 15, 14], fill=c("#454e5e"))
        # ABXY buttons
        d.point((28, 7), fill=c("#f2c94c"))
        d.point((30, 9), fill=c("#eb5757"))
        d.point((26, 9), fill=c("#2f80ed"))
        d.point((28, 11), fill=c("#27ae60"))
    return make_sprite(38, 24, _f)


def sp_apple_phone_cloud():
    def _f(d, im):
        # Sleek aluminum iPhone on left + iCloud cloud with alert badge on right (42x26)
        d.rounded_rectangle([3, 3, 17, 23], radius=3, fill=c("#384152"))
        d.rounded_rectangle([4, 4, 16, 22], radius=2, fill=c("#d9e4f5"))
        d.rectangle([5, 5, 15, 21], fill=c("#f5f8fd"))
        # Dynamic Island notch
        d.rectangle([8, 5, 12, 6], fill=c("#232833"))
        # Red alert icon on screen
        d.ellipse([7, 10, 13, 16], fill=c("#e84c4c"))
        d.rectangle([10, 11, 10, 13], fill=c("#ffffff"))
        d.point((10, 15), fill=c("#ffffff"))
        # Fluffy pixel iCloud on right
        d.ellipse([19, 8, 31, 20], fill=c("#7bb4f5"))
        d.ellipse([25, 5, 36, 17], fill=c("#9ecbff"))
        d.ellipse([28, 10, 39, 20], fill=c("#7bb4f5"))
        d.rectangle([22, 13, 36, 20], fill=c("#8ec1fa"))
        # Inner white cloud highlight
        d.ellipse([21, 10, 30, 18], fill=c("#e8f3ff"))
        d.ellipse([26, 7, 34, 16], fill=c("#ffffff"))
        d.rectangle([23, 13, 34, 18], fill=c("#f0f7ff"))
        # Red status slash badge
        d.ellipse([30, 13, 38, 21], fill=c("#e84c4c"))
        d.line([(32, 15), (36, 19)], fill=c("#ffffff"), width=1)
        d.line([(36, 15), (32, 19)], fill=c("#ffffff"), width=1)
    return make_sprite(42, 26, _f)


def sp_artex_terminal():
    def _f(d, im):
        # Dark terminal window + glowing autonomous AI agent nodes (42x26)
        d.rounded_rectangle([2, 2, 39, 23], radius=2, fill=c("#202433"))
        d.rectangle([2, 2, 39, 6], fill=c("#383e54"))
        d.point((5, 4), fill=c("#f05a5a"))
        d.point((7, 4), fill=c("#f5c451"))
        d.point((9, 4), fill=c("#45d483"))
        # Code lines on left
        for yy, ln, col in [(9, 12, "#45d483"), (11, 9, "#7aa2f7"), (13, 14, "#f05a5a"), (15, 10, "#9aa5ce"), (17, 13, "#f5c451"), (19, 8, "#45d483")]:
            d.rectangle([5, yy, 5 + ln, yy], fill=c(col))
        # Connected autonomous agent cluster on right
        nodes = [(27, 10), (34, 13), (26, 18), (33, 19)]
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                d.line([nodes[i], nodes[j]], fill=c("#e85668"), width=1)
        for nx, ny in nodes:
            d.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=c("#f05a5a"))
            d.point((nx, ny), fill=c("#ffffff"))
    return make_sprite(42, 26, _f)


def sp_java_server():
    def _f(d, im):
        # Enterprise server rack + classic steaming coffee mug (Java4Shell) (42x26)
        d.rounded_rectangle([3, 2, 22, 23], radius=1, fill=c("#2c3342"))
        for ry in (4, 9, 14, 19):
            d.rectangle([5, ry, 20, ry + 3], fill=c("#444e63"))
            d.point((7, ry + 1), fill=c("#eb4d4b") if ry >= 14 else c("#46d181"))
            d.point((9, ry + 1), fill=c("#4d94ff"))
            d.rectangle([13, ry + 1, 18, ry + 1], fill=c("#232836"))
        # Steaming Java coffee mug on right
        d.rounded_rectangle([25, 10, 36, 22], radius=2, fill=c("#ffffff"))
        d.rectangle([26, 11, 35, 21], fill=c("#f0ebe4"))
        d.rectangle([26, 11, 35, 13], fill=c("#7a4b2a"))
        d.arc([34, 12, 39, 19], 270, 90, fill=c("#d9d2c7"), width=2)
        # Coral steam wisps
        d.line([(28, 8), (29, 5)], fill=c("#e8684a"), width=1)
        d.line([(32, 8), (31, 4)], fill=c("#e8684a"), width=1)
    return make_sprite(42, 26, _f)


def sp_nvidia_chip():
    def _f(d, im):
        # Silicon die microchip + glass corporate tower (42x26)
        # Pins
        for p in range(6, 23, 3):
            d.rectangle([p, 3, p + 1, 22], fill=c("#d4af37"))
            d.rectangle([4, p, 24, p + 1], fill=c("#d4af37"))
        d.rounded_rectangle([6, 5, 22, 20], radius=2, fill=c("#1d3b2b"))
        d.rounded_rectangle([8, 7, 20, 18], radius=1, fill=c("#34a867"))
        d.rectangle([10, 9, 18, 16], fill=c("#75e8a3"))
        d.rectangle([12, 11, 16, 14], fill=c("#1d3b2b"))
        # Glass headquarters tower beside it
        d.polygon([(27, 22), (27, 7), (34, 3), (39, 8), (39, 22)], fill=c("#4a6e96"))
        d.polygon([(34, 3), (39, 8), (39, 22), (34, 22)], fill=c("#7ea5cf"))
        for wy in range(8, 21, 3):
            d.rectangle([29, wy, 32, wy + 1], fill=c("#d6ebff"))
            d.rectangle([35, wy, 37, wy + 1], fill=c("#ffffff"))
    return make_sprite(42, 26, _f)


def sp_zelda_pc():
    def _f(d, im):
        # Ultrawide PC monitor with golden triangular relic over emerald meadow (44x26)
        d.rounded_rectangle([2, 2, 41, 19], radius=2, fill=c("#252b36"))
        d.rectangle([4, 4, 39, 17], fill=c("#68c4e8"))
        # Meadow hills
        d.rectangle([4, 13, 39, 17], fill=c("#36a868"))
        d.polygon([(4, 14), (14, 10), (24, 14)], fill=c("#298a52"))
        d.polygon([(20, 14), (31, 9), (39, 14)], fill=c("#42ba74"))
        # Golden Triforce-inspired 3-triangle crest in sky
        d.polygon([(21, 5), (18, 9), (24, 9)], fill=c("#ffd84d"))
        d.polygon([(18, 9), (15, 13), (21, 13)], fill=c("#f2b824"))
        d.polygon([(24, 9), (21, 13), (27, 13)], fill=c("#f2b824"))
        # Stand + keyboard
        d.rectangle([19, 19, 24, 22], fill=c("#3d4654"))
        d.rectangle([14, 22, 29, 23], fill=c("#546073"))
    return make_sprite(44, 26, _f)


def sp_clock_midnight():
    def _f(d, im):
        # Crisp 00:00 glowing neon digital clock (44x22)
        d.rounded_rectangle([2, 2, 41, 19], radius=3, fill=c("#222436"))
        d.rounded_rectangle([4, 4, 39, 17], radius=2, fill=c("#141724"))
        # Draw 4 crisp '0' digits in vibrant Vice magenta/pink
        def draw_zero(ox):
            d.rectangle([ox, 6, ox + 5, 15], fill=c("#ff5ea8"))
            d.rectangle([ox + 2, 8, ox + 3, 13], fill=c("#141724"))
        draw_zero(7)
        draw_zero(14)
        # Colon
        d.rectangle([21, 8, 22, 9], fill=c("#ffd15c"))
        d.rectangle([21, 12, 22, 13], fill=c("#ffd15c"))
        draw_zero(24)
        draw_zero(31)
        # Feet
        d.rectangle([7, 19, 11, 20], fill=c("#3c405c"))
        d.rectangle([32, 19, 36, 20], fill=c("#3c405c"))
    return make_sprite(44, 22, _f)


def sp_globe_nz():
    def _f(d, im):
        # Detailed ocean globe highlighting New Zealand + toggle pill (36x28)
        d.ellipse([5, 2, 29, 24], fill=c("#3d8fe0"))
        d.ellipse([7, 3, 27, 22], fill=c("#56a8f5"))
        # Continents (Australia + Asia hints)
        d.polygon([(11, 7), (17, 6), (19, 11), (13, 12)], fill=c("#52c482"))
        d.polygon([(15, 14), (21, 13), (22, 18), (16, 19)], fill=c("#52c482"))
        # Glowing golden New Zealand islands on lower right!
        d.line([(24, 17), (26, 15)], fill=c("#ffd24c"), width=2)
        d.line([(22, 20), (24, 18)], fill=c("#ffd24c"), width=2)
        # Stand
        d.rectangle([16, 24, 18, 26], fill=c("#4b5568"))
        d.rectangle([11, 26, 23, 27], fill=c("#68758c"))
    return make_sprite(36, 28, _f)


def sp_metacritic_97():
    def _f(d, im):
        # Iconic green Metacritic square badge with crisp '97' (32x28)
        d.rounded_rectangle([3, 2, 28, 25], radius=4, fill=c("#22a85b"))
        d.rounded_rectangle([5, 4, 26, 23], radius=3, fill=c("#34c973"))
        # Crisp white '9'
        d.rectangle([8, 8, 14, 14], fill=c("#ffffff"))
        d.rectangle([10, 10, 12, 12], fill=c("#34c973"))
        d.rectangle([13, 8, 14, 19], fill=c("#ffffff"))
        d.rectangle([8, 18, 14, 19], fill=c("#ffffff"))
        # Crisp white '7'
        d.rectangle([17, 8, 23, 9], fill=c("#ffffff"))
        d.line([(23, 9), (19, 19)], fill=c("#ffffff"), width=2)
    return make_sprite(32, 28, _f)


def sp_leonida_bridge():
    def _f(d, im):
        # Turquoise Keys causeway bridge + sunset + hourglass motif (44x26)
        d.rounded_rectangle([2, 2, 41, 23], radius=2, fill=c("#7dd4e8"))
        # Sunset glow sky
        d.rectangle([2, 2, 41, 11], fill=c("#f7c38a"))
        d.ellipse([17, 4, 26, 13], fill=c("#ffe46b"))
        # Turquoise ocean
        d.rectangle([2, 12, 41, 23], fill=c("#29b2ba"))
        # Shimmer waves
        for wx, wy in [(6, 17), (15, 20), (26, 18), (34, 21)]:
            d.rectangle([wx, wy, wx + 4, wy], fill=c("#8cecf0"))
        # Causeway highway across center
        d.rectangle([2, 11, 41, 14], fill=c("#454e5e"))
        for dx in range(4, 40, 5):
            d.rectangle([dx, 12, dx + 2, 12], fill=c("#ffd84d"))
        # Bridge pillars
        for px in (8, 16, 24, 32, 38):
            d.rectangle([px, 14, px + 1, 21], fill=c("#343c4a"))
    return make_sprite(44, 26, _f)


def sp_vice_polaroid():
    def _f(d, im):
        # Clean Polaroid / gallery frame with neon Miami skyline & storm clouds (42x28)
        d.rectangle([3, 2, 38, 26], fill=c("#ffffff"))
        d.rectangle([5, 4, 36, 21], fill=c("#d96bb8"))
        # Dramatic storm cloud bank top left
        d.ellipse([6, 4, 18, 11], fill=c("#485378"))
        d.ellipse([14, 3, 25, 10], fill=c("#5f6d96"))
        # Lightning & rain streaks
        d.line([(13, 10), (11, 14)], fill=c("#ffe359"), width=1)
        d.line([(20, 10), (19, 13)], fill=c("#b8d4ff"), width=1)
        # Sunset sun right
        d.ellipse([27, 7, 33, 13], fill=c("#ffb84d"))
        # Pastel Art-Deco city silhouette
        d.rectangle([6, 15, 11, 21], fill=c("#323a63"))
        d.rectangle([12, 13, 17, 21], fill=c("#465082"))
        d.rectangle([18, 16, 24, 21], fill=c("#2c3459"))
        d.rectangle([25, 14, 31, 21], fill=c("#56488a"))
        d.rectangle([32, 17, 36, 21], fill=c("#323a63"))
        # Neon cyan window lights
        for bx, by in [(8, 17), (14, 15), (15, 18), (27, 16), (29, 18)]:
            d.point((bx, by), fill=c("#66f2ff"))
    return make_sprite(42, 28, _f)


def sp_awards_trophy():
    def _f(d, im):
        # Sleek golden winged awards statue on stage pedestal (34x30)
        # Pedestal
        d.rectangle([9, 24, 24, 28], fill=c("#2b3040"))
        d.rectangle([11, 23, 22, 24], fill=c("#4b536b"))
        # Golden winged figure / chalice
        d.polygon([(14, 23), (19, 23), (18, 14), (15, 14)], fill=c("#d99a1e"))
        d.polygon([(16, 23), (18, 23), (17, 14), (16, 14)], fill=c("#ffd859"))
        # Left & right sweeping wings
        d.polygon([(15, 15), (6, 6), (9, 4), (16, 11)], fill=c("#f2bc33"))
        d.polygon([(15, 13), (8, 6), (10, 5), (15, 10)], fill=c("#fff0a6"))
        d.polygon([(18, 15), (27, 6), (24, 4), (17, 11)], fill=c("#d99a1e"))
        d.polygon([(18, 13), (25, 6), (23, 5), (18, 10)], fill=c("#ffd859"))
        # Crown / sphere head
        d.ellipse([14, 7, 19, 12], fill=c("#ffe47a"))
        d.point((15, 8), fill=c("#ffffff"))
    return make_sprite(34, 30, _f)


def sp_mega_millions():
    def _f(d, im):
        # 5 crisp pearl white lottery spheres + giant golden Mega Ball (44x26)
        whites = [(8, 14), (16, 19), (26, 19), (35, 14), (11, 8)]
        for wx, wy in whites:
            d.ellipse([wx - 5, wy - 5, wx + 5, wy + 5], fill=c("#cfd8e8"))
            d.ellipse([wx - 4, wy - 4, wx + 4, wy + 4], fill=c("#ffffff"))
            d.point((wx - 2, wy - 2), fill=c("#e8f0ff"))
        # Giant golden Mega Ball center
        d.ellipse([16, 4, 30, 18], fill=c("#db9812"))
        d.ellipse([17, 5, 29, 17], fill=c("#f7c836"))
        d.ellipse([19, 7, 25, 12], fill=c("#ffe985"))
        d.point((20, 8), fill=c("#ffffff"))
    return make_sprite(44, 26, _f)


def sp_fbi_shield():
    def _f(d, im):
        # Federal navy & gold badge shield with alert bar (34x28)
        d.polygon([(17, 2), (30, 6), (28, 18), (17, 26), (6, 18), (4, 6)], fill=c("#2c4f9e"))
        d.polygon([(17, 4), (28, 7), (26, 17), (17, 24), (8, 17), (6, 7)], fill=c("#4470d1"))
        # Gold inner seal + exclamation
        d.ellipse([11, 8, 23, 20], fill=c("#f5c23b"))
        d.ellipse([13, 10, 21, 18], fill=c("#e84c4c"))
        d.rectangle([16, 11, 17, 14], fill=c("#ffffff"))
        d.rectangle([16, 16, 17, 17], fill=c("#ffffff"))
    return make_sprite(34, 28, _f)


def sp_salesforce_clouds():
    def _f(d, im):
        # Interlocking blue + indigo enterprise clouds with Zero Copy gold arrows (44x26)
        # Left blue cloud
        d.ellipse([4, 9, 17, 21], fill=c("#3898e6"))
        d.ellipse([10, 5, 23, 18], fill=c("#5cb3f7"))
        d.rectangle([9, 13, 21, 21], fill=c("#48a6f0"))
        # Right purple-indigo cloud
        d.ellipse([21, 9, 34, 21], fill=c("#6858d6"))
        d.ellipse([26, 6, 39, 19], fill=c("#8476ed"))
        d.rectangle([25, 13, 37, 21], fill=c("#7566e0"))
        # Bidirectional gold sync arrows
        d.rectangle([16, 12, 27, 13], fill=c("#ffd24c"))
        d.rectangle([16, 16, 27, 17], fill=c("#ffffff"))
    return make_sprite(44, 26, _f)


def sp_gamepass_tv():
    def _f(d, im):
        # Sleek OLED TV displaying misty horror forest + green Game Pass badge (44x26)
        d.rounded_rectangle([2, 2, 41, 20], radius=2, fill=c("#1c2120"))
        d.rectangle([4, 4, 39, 18], fill=c("#1b3328"))
        # Mist glow moon
        d.ellipse([18, 6, 25, 13], fill=c("#bfe8cf"))
        # Pine trees silhouettes
        for tx in (7, 12, 31, 36):
            d.polygon([(tx, 7), (tx - 3, 18), (tx + 3, 18)], fill=c("#0f1c16"))
        # Green pass pill bottom right
        d.rounded_rectangle([27, 13, 38, 17], radius=1, fill=c("#32c46c"))
        d.rectangle([29, 15, 36, 15], fill=c("#ffffff"))
        # Stand
        d.rectangle([18, 20, 25, 22], fill=c("#37403e"))
        d.rectangle([13, 22, 30, 23], fill=c("#4f5c59"))
    return make_sprite(44, 26, _f)


def sp_gmail_allclear():
    def _f(d, im):
        # Crisp white/red envelope with green checkmark badge (42x26)
        d.rounded_rectangle([3, 4, 33, 22], radius=2, fill=c("#f2f4f8"))
        d.rectangle([4, 5, 32, 21], fill=c("#ffffff"))
        # Red M envelope flaps
        d.rectangle([4, 5, 7, 21], fill=c("#e64c45"))
        d.rectangle([29, 5, 32, 21], fill=c("#e64c45"))
        d.line([(6, 6), (18, 14)], fill=c("#e64c45"), width=3)
        d.line([(30, 6), (18, 14)], fill=c("#e64c45"), width=3)
        # Green All Clear check badge
        d.ellipse([25, 11, 39, 25], fill=c("#27ae60"))
        d.ellipse([27, 13, 37, 23], fill=c("#36cc74"))
        d.line([(29, 18), (31, 20)], fill=c("#ffffff"), width=2)
        d.line([(31, 20), (35, 15)], fill=c("#ffffff"), width=2)
    return make_sprite(42, 26, _f)


def sp_amazon_box():
    def _f(d, im):
        # Kraft cardboard shipping box + cloud server badge (42x26)
        d.rounded_rectangle([5, 8, 29, 23], radius=1, fill=c("#c98a42"))
        d.rectangle([6, 9, 28, 22], fill=c("#e0a660"))
        d.rectangle([15, 8, 19, 14], fill=c("#f5d4a6"))  # Packing tape
        # Classic curved smile accent
        d.arc([10, 15, 24, 21], 10, 170, fill=c("#2b2620"), width=2)
        # Cloud server badge top right
        d.ellipse([23, 3, 34, 13], fill=c("#5ea2e8"))
        d.ellipse([28, 5, 39, 14], fill=c("#7bb8f5"))
        d.rectangle([26, 8, 36, 14], fill=c("#68abf0"))
        d.point((31, 10), fill=c("#ffd15c"))
        d.point((34, 10), fill=c("#ffffff"))
    return make_sprite(42, 26, _f)


def sp_facebook_privacy():
    def _f(d, im):
        # Smartphone photo gallery + blue social profile card + coral alert (42x26)
        d.rounded_rectangle([4, 3, 20, 23], radius=2, fill=c("#2c3547"))
        d.rectangle([6, 5, 18, 21], fill=c("#ffffff"))
        # Photo gallery landscape tile inside phone
        d.rectangle([7, 6, 17, 13], fill=c("#82c4f8"))
        d.polygon([(7, 13), (11, 9), (15, 13)], fill=c("#47b872"))
        d.point((15, 8), fill=c("#ffd84d"))
        # Secondary fading profile avatars right
        d.rounded_rectangle([23, 4, 38, 12], radius=2, fill=c("#3b73db"))
        d.ellipse([25, 6, 29, 10], fill=c("#ffffff"))
        d.rectangle([31, 7, 36, 8], fill=c("#c9dcff"))
        d.rounded_rectangle([23, 14, 38, 22], radius=2, fill=c("#cbd5e6"))
        d.ellipse([25, 16, 29, 20], fill=c("#ffffff"))
        # Red slash across fading secondary profile
        d.line([(24, 21), (37, 15)], fill=c("#e8524a"), width=2)
    return make_sprite(42, 26, _f)


# ============================================================
# FLOATING EDITORIAL ACCENTS (soft shaded, crisp cutout!)
# ============================================================

def ac_bill():
    def _f(d, im):
        d.rectangle([1, 2, 13, 8], fill=c("#69a870"))
        d.rectangle([2, 3, 12, 7], fill=c("#9ed1a2"))
        d.ellipse([5, 3, 9, 7], fill=c("#528a58"))
        d.point((7, 5), fill=c("#e8f5e9"))
    return make_sprite(15, 11, _f)


def ac_car(body_hex, hi_hex):
    def _f(d, im):
        d.rounded_rectangle([1, 2, 14, 8], radius=2, fill=c(body_hex))
        d.rectangle([3, 3, 12, 7], fill=c(hi_hex))
        d.rectangle([4, 3, 6, 7], fill=c("#252333"))  # Windshield
        d.rectangle([10, 3, 11, 7], fill=c("#252333"))  # Rear glass
    return make_sprite(16, 11, _f)


def ac_star():
    def _f(d, im):
        d.polygon([(6, 1), (7, 4), (11, 5), (8, 7), (9, 11), (6, 9), (3, 11), (4, 7), (1, 5), (5, 4)], fill=c("#f5c23b"))
        d.point((6, 5), fill=c("#fff6cc"))
    return make_sprite(13, 12, _f)


def ac_warn():
    def _f(d, im):
        d.polygon([(6, 1), (11, 10), (1, 10)], fill=c("#f2b632"))
        d.rectangle([6, 4, 6, 7], fill=c("#26221e"))
        d.point((6, 9), fill=c("#26221e"))
    return make_sprite(13, 12, _f)


def ac_lock():
    def _f(d, im):
        d.arc([3, 1, 9, 7], 180, 360, fill=c("#7e8a9e"), width=2)
        d.rounded_rectangle([2, 5, 10, 11], radius=1, fill=c("#f2b838"))
        d.rectangle([5, 7, 7, 9], fill=c("#383124"))
    return make_sprite(13, 13, _f)


def ac_bolt():
    def _f(d, im):
        d.polygon([(7, 1), (3, 6), (6, 6), (4, 11), (10, 5), (7, 5)], fill=c("#ffd43b"))
    return make_sprite(13, 12, _f)


def ac_check():
    def _f(d, im):
        d.ellipse([1, 1, 11, 11], fill=c("#2db86a"))
        d.line([(3, 6), (5, 8)], fill=c("#ffffff"), width=2)
        d.line([(5, 8), (9, 4)], fill=c("#ffffff"), width=2)
    return make_sprite(13, 13, _f)


def ac_card():
    def _f(d, im):
        d.rounded_rectangle([1, 2, 13, 9], radius=1, fill=c("#3d7ee6"))
        d.rectangle([3, 4, 5, 5], fill=c("#ffd24c"))
        d.rectangle([3, 7, 11, 7], fill=c("#c2dbff"))
    return make_sprite(15, 11, _f)


def ac_palm():
    def _f(d, im):
        d.line([(6, 11), (7, 5)], fill=c("#9c6334"), width=2)
        d.line([(7, 5), (2, 4)], fill=c("#34a867"), width=2)
        d.line([(7, 5), (12, 4)], fill=c("#34a867"), width=2)
        d.line([(7, 5), (4, 2)], fill=c("#54cc85"), width=2)
        d.line([(7, 5), (10, 2)], fill=c("#54cc85"), width=2)
    return make_sprite(14, 13, _f)


def ac_tag():
    def _f(d, im):
        d.rounded_rectangle([1, 2, 13, 9], radius=1, fill=c("#e64848"))
        d.point((3, 5), fill=c("#ffffff"))
        d.rectangle([6, 4, 11, 5], fill=c("#ffffff"))
        d.rectangle([6, 7, 10, 7], fill=c("#ffc9c9"))
    return make_sprite(15, 11, _f)


def ac_plus():
    def _f(d, im):
        d.rectangle([5, 1, 7, 11], fill=c("#f5c23b"))
        d.rectangle([1, 5, 11, 7], fill=c("#f5c23b"))
        d.point((6, 6), fill=c("#fff7cc"))
    return make_sprite(13, 13, _f)


def ac_key():
    def _f(d, im):
        d.ellipse([1, 3, 6, 8], fill=c("#f2bc33"))
        d.point((3, 5), fill=c("#ffffff"))
        d.rectangle([6, 5, 13, 6], fill=c("#f2bc33"))
        d.rectangle([10, 7, 11, 8], fill=c("#d99a1e"))
        d.rectangle([12, 7, 13, 8], fill=c("#d99a1e"))
    return make_sprite(15, 11, _f)


def draw_drift_trails(canvas, x, y, dx=-1, dy=1):
    def _draw(d, layer):
        px, py = x // SCALE, y // SCALE
        for i in range(14):
            alpha = max(30, 155 - i * 9)
            col = (88, 84, 104, alpha)
            tx = px + int(dx * i * 1.15)
            ty = py + int(dy * (i * 0.55 + (i * i) * 0.045))
            d.point((tx, ty), fill=col)
            d.point((tx, ty + 3), fill=col)
    draw_pixel_layer(canvas, _draw)


# ============================================================
# 20 STORY-SPECIFIC EDITORIAL BIT-GRAPHICS (Refined Edition)
# Notice accent sprites overlap the inner frame border just like reference!
# ============================================================

BILL = ac_bill()
CAR_P = ac_car("#7f2ef2", "#9e54ff")
CAR_Y = ac_car("#e8b81a", "#ffd542")
STAR = ac_star()
WARN = ac_warn()
LOCK = ac_lock()
BOLT = ac_bolt()
CHECK = ac_check()
CARD = ac_card()
PALM = ac_palm()
TAG = ac_tag()
PLUS = ac_plus()
KEY = ac_key()

ARTICLES_ART = [
    ("apple-outage.jpg", "#7fa8e8", "#f0b48c", "#f6f8fc", "#e35b54", "spike",
     sp_apple_phone_cloud(), 11, [
         (CARD, 195, 130, -18, 8),
         (WARN, 1085, 135, 12, 8),
         (LOCK, 1090, 565, -14, 8),
     ], False),

    ("artex.jpg", "#8d74e8", "#e88989", "#f8f4fb", "#d94f5c", "spike",
     sp_artex_terminal(), 11, [
         (KEY, 195, 135, -20, 8),
         (BOLT, 1085, 135, 16, 8),
         (LOCK, 200, 560, 12, 8),
         (WARN, 1085, 565, -10, 8),
     ], False),

    ("java4shell.jpg", "#e06d5b", "#f0ca78", "#fcf6f2", "#d9534f", "bars",
     sp_java_server(), 11, [
         (WARN, 195, 130, -14, 8),
         (BOLT, 1085, 135, 16, 8),
         (LOCK, 1090, 565, -10, 8),
     ], False),

    ("harvey-jones.jpg", "#5ab888", "#e8cb78", "#f4faf6", "#2f9e66", "rising",
     sp_nvidia_chip(), 11, [
         (BILL, 195, 130, -24, 9),
         (STAR, 1085, 135, 14, 8),
         (BILL, 1090, 565, 22, 9),
     ], False),

    ("ocarina-pc-port.jpg", "#4ba89b", "#e8cf78", "#f3faf8", "#2d9c8a", "rising",
     sp_zelda_pc(), 11, [
         (STAR, 195, 135, -14, 8),
         (BOLT, 1085, 135, 14, 8),
         (CHECK, 1090, 565, -8, 8),
     ], False),

    ("gta6-release-time.jpg", "#c375e3", "#f0c27a", "#faf3fb", "#e05a6d", "rising",
     sp_clock_midnight(), 11, [
         (PALM, 195, 130, -12, 9),
         (CAR_P, 1070, 140, -22, 9),
         (CAR_Y, 215, 515, -18, 9),
         (BILL, 1095, 565, 20, 9),
     ], True),

    ("gta6-new-zealand.jpg", "#4ba4c9", "#b68ce8", "#f3f8fc", "#3e85c7", "rising",
     sp_globe_nz(), 11, [
         (CAR_Y, 215, 515, -20, 9),
         (BOLT, 1085, 135, 14, 8),
         (STAR, 195, 135, -14, 8),
         (WARN, 1090, 565, 10, 8),
     ], True),

    ("gta6-metacritic.jpg", "#58c488", "#efd06b", "#f4fbf6", "#29a863", "rising",
     sp_metacritic_97(), 12, [
         (STAR, 195, 130, -16, 9),
         (STAR, 1085, 135, 16, 9),
         (CHECK, 1090, 565, -10, 8),
         (BILL, 200, 560, 16, 9),
     ], False),

    ("gta6-story-length.jpg", "#4ac2c9", "#f29e83", "#f4fafb", "#e36858", "bars",
     sp_leonida_bridge(), 11, [
         (PALM, 195, 130, -12, 9),
         (CAR_P, 1070, 140, -22, 9),
         (CAR_Y, 215, 515, -18, 9),
         (STAR, 1090, 565, 12, 8),
     ], True),

    ("gta6-screenshots.jpg", "#e374b5", "#7a85e0", "#fbf4f9", "#d64d94", "wave",
     sp_vice_polaroid(), 11, [
         (BOLT, 195, 135, -15, 8),
         (CAR_P, 1070, 140, -22, 9),
         (PALM, 1090, 565, 10, 9),
         (CAR_Y, 215, 515, -18, 9),
     ], True),

    ("game-awards-2026.jpg", "#e8be63", "#797ed6", "#faf8f2", "#d99e26", "bars",
     sp_awards_trophy(), 11, [
         (STAR, 195, 130, -14, 9),
         (STAR, 1085, 135, 14, 9),
         (STAR, 200, 560, 12, 8),
         (CHECK, 1090, 565, -10, 8),
     ], False),

    ("mega-millions-nov17.jpg", "#5a90e6", "#f2c85b", "#f5f8fd", "#3b76d9", "rising",
     sp_mega_millions(), 11, [
         (BILL, 195, 130, -24, 9),
         (STAR, 1085, 135, 14, 9),
         (BILL, 1090, 565, 22, 9),
         (BILL, 200, 560, 16, 8),
     ], False),

    ("fbi-warning.jpg", "#5879c9", "#e87676", "#f4f6fb", "#d94e4e", "spike",
     sp_fbi_shield(), 11, [
         (WARN, 195, 135, -14, 9),
         (LOCK, 1085, 135, 12, 8),
         (BILL, 1090, 565, 18, 9),
         (KEY, 200, 560, -16, 8),
     ], False),

    ("xbox-black-friday.jpg", "#42b872", "#637387", "#f3faf5", "#2ba35b", "drop",
     sp_xbox_controller(), 12, [
         (TAG, 195, 130, -16, 9),
         (BILL, 1085, 135, 22, 9),
         (STAR, 1090, 565, -12, 8),
         (TAG, 200, 560, 14, 8),
     ], False),

    ("playstation-plus.jpg", "#b47be8", "#f2c87e", "#f7f3fb", "#e35c54", "rising",
     sp_dualsense(), 12, [
         (BILL, 195, 130, -24, 9),
         (PLUS, 1085, 135, 14, 9),
         (BILL, 1090, 565, 22, 9),
         (CARD, 205, 560, -15, 8),
     ], False),

    ("salesforce.jpg", "#5ab3eb", "#9c8ce6", "#f4f9fd", "#4b8be0", "drop",
     sp_salesforce_clouds(), 11, [
         (BILL, 195, 130, -22, 9),
         (BOLT, 1085, 135, 14, 8),
         (LOCK, 1090, 565, -10, 8),
     ], False),

    ("xbox-game-pass.jpg", "#399c62", "#a2d977", "#f3faf4", "#2c9957", "bars",
     sp_gamepass_tv(), 11, [
         (STAR, 195, 135, -14, 8),
         (BOLT, 1085, 135, 14, 8),
         (PLUS, 1090, 565, 12, 8),
     ], False),

    ("gmail-outage.jpg", "#e86f68", "#7ab4e8", "#fdf5f5", "#d9504a", "wave",
     sp_gmail_allclear(), 11, [
         (CHECK, 195, 130, -10, 9),
         (WARN, 1085, 135, 12, 8),
         (CHECK, 1090, 565, -8, 9),
     ], False),

    ("amazon-down.jpg", "#eb9d4b", "#6c8eb8", "#fcf8f2", "#d9822b", "spike",
     sp_amazon_box(), 11, [
         (WARN, 195, 130, -12, 8),
         (BOLT, 1085, 135, 14, 8),
         (CARD, 1090, 565, -14, 8),
     ], False),

    ("facebook-meta.jpg", "#4f83e3", "#e08d6c", "#f4f7fc", "#3e6fd4", "bars",
     sp_facebook_privacy(), 11, [
         (BILL, 195, 130, -22, 9),
         (WARN, 1085, 135, 12, 8),
         (BILL, 1090, 565, 20, 9),
         (LOCK, 200, 560, -12, 8),
     ], False),
]


def render_all():
    for fname, g1, g2, paper, accent, chart, hero, hscale, accents, trails in ARTICLES_ART:
        canvas = make_gradient_bg(g1, g2)
        draw_inner_frame(canvas, paper, accent, chart_style=chart)
        if trails:
            draw_drift_trails(canvas, 1005, 185, dx=-1, dy=1)
            draw_drift_trails(canvas, 155, 535, dx=-1, dy=-0.4)
        paste_sprite(canvas, hero, W // 2, H // 2 + 6, pix_scale=hscale, angle=0, outline=True, shadow=True)
        for sp, ax, ay, ang, sc in accents:
            paste_sprite(canvas, sp, ax, ay, pix_scale=sc, angle=ang, outline=True, shadow=True)

        out_path = os.path.join(OUT_DIR, fname)
        canvas.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True)
        print(f"Generated refined bit-graphic: {fname} ({os.path.getsize(out_path):,} bytes)")


if __name__ == "__main__":
    render_all()
