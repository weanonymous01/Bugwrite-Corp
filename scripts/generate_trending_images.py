import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PIL import Image, ImageDraw
import generate_bit_graphics as bg

OUT_DIR = r"c:\Users\adars\Downloads\Bugwrite-Corp\public\blog\articles"
os.makedirs(OUT_DIR, exist_ok=True)
c = bg.c
make_sprite = bg.make_sprite
hex_rgb = bg.hex_rgb
W, H = bg.W, bg.H


def sp_niko_liberty():
    def _f(d, im):
        # Weathered dark olive/brown jacket silhouette + red baseball cap + bowling pin icon (44x28)
        # Background coat
        d.rounded_rectangle([6, 6, 37, 26], radius=3, fill=c("#3b3834"))
        d.rounded_rectangle([11, 8, 32, 26], radius=2, fill=c("#544e47"))
        # Cream sweater collar
        d.polygon([(17, 8), (22, 16), (26, 8)], fill=c("#d4cfc5"))
        d.rectangle([21, 16, 23, 26], fill=c("#22201e"))
        # Leather coat lapels
        d.polygon([(10, 8), (17, 18), (12, 26)], fill=c("#2a2724"))
        d.polygon([(33, 8), (26, 18), (31, 26)], fill=c("#2a2724"))
        # Miniature Liberty City metro token / bowling pin badge on chest
        d.ellipse([27, 12, 33, 18], fill=c("#e03b3b"))
        d.ellipse([29, 13, 31, 15], fill=c("#ffffff"))
        d.rectangle([29, 15, 31, 17], fill=c("#ffffff"))
    return make_sprite(44, 28, _f)


def sp_branching_paths():
    def _f(d, im):
        # Dual branching road / compass decision motif (42x28)
        d.rounded_rectangle([2, 3, 39, 25], radius=3, fill=c("#1a1e29"))
        d.rectangle([4, 5, 37, 23], fill=c("#252b3b"))
        # Left neon pink route (Lucia path)
        d.line([(8, 20), (16, 14), (16, 9), (12, 6)], fill=c("#ff4081"), width=2)
        d.polygon([(10, 5), (14, 5), (12, 8)], fill=c("#ff4081"))
        # Right neon teal route (Jason path)
        d.line([(8, 20), (24, 17), (30, 11), (34, 7)], fill=c("#00e5ff"), width=2)
        d.polygon([(32, 6), (36, 7), (35, 10)], fill=c("#00e5ff"))
        # Center gold star node
        d.ellipse([6, 18, 10, 22], fill=c("#ffd700"))
        d.ellipse([15, 13, 17, 15], fill=c("#ffffff"))
        d.ellipse([23, 16, 25, 18], fill=c("#ffffff"))
    return make_sprite(42, 28, _f)


def sp_diner_route():
    def _f(d, im):
        # Retro diner sign + getaway car outline (44x26)
        d.rounded_rectangle([2, 3, 26, 17], radius=2, fill=c("#d93838"))
        d.rectangle([4, 5, 24, 15], fill=c("#f8fafc"))
        # "DINER" neon block
        for x in (7, 11, 15, 19, 22):
            d.rectangle([x, 8, x + 1, 12], fill=c("#d93838"))
        # Striped awning
        for x in range(3, 26, 4):
            d.rectangle([x, 15, x + 2, 17], fill=c("#ffd166"))
        # Getaway car silhouette
        d.rounded_rectangle([20, 14, 42, 23], radius=2, fill=c("#1e293b"))
        d.rectangle([25, 10, 37, 14], fill=c("#38bdf8"))
        d.ellipse([23, 21, 27, 25], fill=c("#0f172a"))
        d.ellipse([34, 21, 38, 25], fill=c("#0f172a"))
    return make_sprite(44, 26, _f)


def sp_heavy_safe():
    def _f(d, im):
        # Heavy steel dial safe with cash stack inside (40x28)
        d.rounded_rectangle([4, 2, 36, 26], radius=3, fill=c("#334155"))
        d.rounded_rectangle([6, 4, 34, 24], radius=2, fill=c("#1e293b"))
        # Circular steel dial
        d.ellipse([14, 8, 26, 20], fill=c("#64748b"))
        d.ellipse([16, 10, 24, 18], fill=c("#94a3b8"))
        d.ellipse([18, 12, 22, 16], fill=c("#334155"))
        # Dial tick mark & pointer
        d.rectangle([19, 8, 21, 11], fill=c("#fbbf24"))
        # Handle lever
        d.rectangle([28, 12, 32, 16], fill=c("#cbd5e1"))
        d.rectangle([30, 10, 32, 18], fill=c("#94a3b8"))
        # Corner bolt studs
        for bx, by in [(8, 6), (32, 6), (8, 22), (32, 22)]:
            d.rectangle([bx, by, bx + 1, by + 1], fill=c("#94a3b8"))
    return make_sprite(40, 28, _f)


def sp_muscle_driver():
    def _f(d, im):
        # Driver cockpit with steering wheel and rearview mirror (42x26)
        d.rounded_rectangle([3, 3, 39, 23], radius=3, fill=c("#111827"))
        # Windshield view showing palm tree sunset
        d.rectangle([5, 5, 37, 17], fill=c("#f97316"))
        d.rectangle([5, 11, 37, 17], fill=c("#ec4899"))
        # Palm silhouette in windshield
        d.rectangle([28, 8, 29, 17], fill=c("#1e1b4b"))
        d.polygon([(24, 8), (28, 7), (26, 10)], fill=c("#1e1b4b"))
        d.polygon([(30, 7), (34, 8), (32, 10)], fill=c("#1e1b4b"))
        # Rearview mirror hanging
        d.rectangle([18, 5, 24, 7], fill=c("#475569"))
        # Steering wheel arc
        d.ellipse([10, 14, 26, 26], fill=c("#374151"))
        d.ellipse([12, 16, 24, 24], fill=c("#1f2937"))
        d.rectangle([17, 18, 19, 22], fill=c("#4b5563"))
    return make_sprite(42, 26, _f)


TRENDING_ARTICLES_ART = [
    (
        "gta6-niko-bellic.jpg",
        "#6b7280", "#b45309", "#faf5ea", "#b45309", "wave",
        sp_niko_liberty(), 12,
        [
            (bg.TAG, 195, 130, -18, 9),
            (bg.BOLT, 1085, 135, 14, 8),
            (bg.BILL, 1090, 565, 22, 9),
            (bg.KEY, 205, 560, -15, 8),
        ], False
    ),
    (
        "gta6-endings.jpg",
        "#ec4899", "#8b5cf6", "#fdf4ff", "#d946ef", "rising",
        sp_branching_paths(), 12,
        [
            (bg.STAR, 195, 130, -14, 9),
            (bg.BOLT, 1085, 135, 16, 8),
            (bg.PLUS, 1090, 565, 14, 9),
            (bg.CARD, 200, 560, -16, 8),
        ], True
    ),
    (
        "gta6-chapter-1.jpg",
        "#f59e0b", "#ef4444", "#fefce8", "#ea580c", "bars",
        sp_diner_route(), 12,
        [
            (bg.TAG, 195, 135, -12, 9),
            (bg.BILL, 1085, 135, 20, 9),
            (bg.STAR, 1090, 565, -14, 8),
            (bg.KEY, 205, 560, 16, 8),
        ], True
    ),
    (
        "gta6-safe-code.jpg",
        "#0284c7", "#0d9488", "#f0fdfa", "#059669", "drop",
        sp_heavy_safe(), 12,
        [
            (bg.KEY, 195, 130, -16, 9),
            (bg.BILL, 1085, 135, 22, 9),
            (bg.LOCK, 1090, 565, -12, 8),
            (bg.BILL, 200, 560, 15, 8),
        ], False
    ),
    (
        "gta6-donnie.jpg",
        "#ea580c", "#6366f1", "#fff7ed", "#c2410c", "spike",
        sp_muscle_driver(), 12,
        [
            (bg.WARN, 195, 135, -14, 9),
            (bg.BOLT, 1085, 135, 15, 8),
            (bg.BILL, 1090, 565, 18, 9),
            (bg.CARD, 205, 560, -12, 8),
        ], True
    ),
]


def render_all_images():
    for fname, g1, g2, paper, accent, chart, hero, hscale, accents, trails in TRENDING_ARTICLES_ART:
        canvas = bg.make_gradient_bg(g1, g2)
        bg.draw_inner_frame(canvas, paper, accent, chart_style=chart)
        if trails:
            bg.draw_drift_trails(canvas, 1005, 185, dx=-1, dy=1)
            bg.draw_drift_trails(canvas, 155, 535, dx=-1, dy=-0.4)
        bg.paste_sprite(canvas, hero, W // 2, H // 2 + 6, pix_scale=hscale, angle=0, outline=True, shadow=True)
        for sp, ax, ay, ang, sc in accents:
            bg.paste_sprite(canvas, sp, ax, ay, pix_scale=sc, angle=ang, outline=True, shadow=True)

        out_path = os.path.join(OUT_DIR, fname)
        canvas.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True)
        print(f"Generated bit-graphic: {fname} ({os.path.getsize(out_path):,} bytes)")


if __name__ == "__main__":
    render_all_images()
