import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
BLOG_DIR = os.path.join(PUBLIC, "blog")
os.makedirs(BLOG_DIR, exist_ok=True)


def load_bold_font(size):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
        r"C:\Windows\Fonts\verdanab.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = max(4, int(size * 0.22))
    # Crisp editorial dark square with subtle border
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=(10, 12, 16, 255))

    # Draw bold lowercase "b" + sharp accent dot
    font = load_bold_font(int(size * 0.72))
    text = "b"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = int((size - tw) / 2 - bbox[0] - size * 0.04)
    y = int((size - th) / 2 - bbox[1] - size * 0.03)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # Crisp editorial blue square period in lower right
    dot = max(3, int(size * 0.14))
    dx = min(size - dot - max(2, int(size * 0.1)), x + tw + max(1, int(size * 0.04)))
    dy = int(size * 0.66)
    draw.rectangle([dx, dy, dx + dot, dy + dot], fill=(37, 99, 235, 255))
    return img


def generate_favicon_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#0a0c10"/>
  <text x="16" y="49" font-family="system-ui, -apple-system, 'Segoe UI', Arial, sans-serif" font-size="46" font-weight="900" letter-spacing="-2" fill="#ffffff">b</text>
  <rect x="44" y="40" width="9" height="9" rx="1.5" fill="#2563eb"/>
</svg>
"""
    with open(os.path.join(PUBLIC, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


def generate_publisher_logo():
    # Google News / Article publisher logo specification:
    # Wide horizontal rectangle, height <= 60px, width <= 600px, solid white background, crisp text
    w, h = 600, 60
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Small square mark on left
    draw.rounded_rectangle([16, 10, 56, 50], radius=8, fill=(10, 12, 16))
    mark_font = load_bold_font(28)
    mb = draw.textbbox((0, 0), "b", font=mark_font)
    draw.text((27 - mb[0], 30 - (mb[3] - mb[1]) // 2 - mb[1] - 1), "b", font=mark_font, fill=(255, 255, 255))
    draw.rectangle([45, 36, 51, 42], fill=(37, 99, 235))

    # Wordmark "bugwrite"
    word_font = load_bold_font(38)
    wb = draw.textbbox((0, 0), "bugwrite", font=word_font)
    wy = (h - (wb[3] - wb[1])) // 2 - wb[1] - 1
    draw.text((70, wy), "bugwrite", font=word_font, fill=(10, 12, 16))

    out_path = os.path.join(BLOG_DIR, "bugwrite-logo.png")
    img.save(out_path, "PNG", optimize=True)


def generate_manifest():
    manifest = """{
  "name": "Bugwrite",
  "short_name": "Bugwrite",
  "description": "Independent technology, gaming, cybersecurity, and AI business journalism.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0d0f12",
  "icons": [
    {
      "src": "/favicon-48x48.png",
      "sizes": "48x48",
      "type": "image/png"
    },
    {
      "src": "/favicon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
"""
    with open(os.path.join(PUBLIC, "site.webmanifest"), "w", encoding="utf-8") as f:
        f.write(manifest)


def main():
    generate_favicon_svg()
    icon_48 = draw_icon(48)
    icon_180 = draw_icon(180)
    icon_192 = draw_icon(192)

    icon_48.save(os.path.join(PUBLIC, "favicon-48x48.png"), "PNG", optimize=True)
    icon_180.save(os.path.join(PUBLIC, "apple-touch-icon.png"), "PNG", optimize=True)
    icon_192.save(os.path.join(PUBLIC, "favicon-192x192.png"), "PNG", optimize=True)
    icon_192.save(
        os.path.join(PUBLIC, "favicon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    generate_publisher_logo()
    generate_manifest()
    print("Generated favicon.svg, favicon.ico, favicon-48x48.png, favicon-192x192.png, apple-touch-icon.png, site.webmanifest, and blog/bugwrite-logo.png")


if __name__ == "__main__":
    main()
