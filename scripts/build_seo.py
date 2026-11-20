import html
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime

DOMAIN = "https://www.bugwrite.com"
NOW_UTC = datetime.now(timezone.utc).replace(microsecond=0)
LASTMOD = NOW_UTC.strftime("%Y-%m-%d")
MOD_ISO = NOW_UTC.strftime("%Y-%m-%dT%H:%M:%SZ")
CSS_VERSION = "2"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
DATA_JS = os.path.join(PUBLIC, "blog", "articles-data.js")


def get_article_pub_dt(iso_date, idx):
    """Return a clean UTC publication datetime that is never in the future."""
    try:
        d = datetime.strptime(iso_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        d = NOW_UTC.replace(hour=0, minute=0, second=0)
    if d.date() == NOW_UTC.date():
        # Spread today's articles cleanly across earlier hours today, never after NOW_UTC
        offset_mins = min(15 + (idx * 13) % 480, max(1, int((NOW_UTC - d).total_seconds() // 60)))
        dt = NOW_UTC - timedelta(minutes=offset_mins)
    else:
        pub_hour = 18 - (idx % 12)
        pub_min = (idx * 7) % 60
        dt = d.replace(hour=pub_hour, minute=pub_min, second=0)
    return dt if dt <= NOW_UTC else NOW_UTC

PUBLISHER_ORG = {
    "@type": "NewsMediaOrganization",
    "name": "Bugwrite",
    "url": f"{DOMAIN}/",
    "logo": {
        "@type": "ImageObject",
        "url": f"{DOMAIN}/blog/bugwrite-logo.png",
        "width": 600,
        "height": 60
    }
}

GA4_SNIPPET = """  <!-- Google Search Console Verification -->
  <meta name="google-site-verification" content="OLMBxfsU2GBJlczpGNYm1WIVHs29p9nFhHP0iYyGQ6k" />
  <!-- Google Analytics 4: uncomment and replace G-XXXXXXXXXX with your live GA4 Measurement ID
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
  -->"""

SHARED_STYLES = f"""  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#0d0f12" media="(prefers-color-scheme: dark)" />
  <link rel="alternate" type="application/rss+xml" title="Bugwrite News RSS Feed" href="{DOMAIN}/rss.xml" />
  <link rel="preload" as="style" href="/assets/styles.css?v={CSS_VERSION}" />
  <link rel="stylesheet" href="/assets/styles.css?v={CSS_VERSION}" />
  <script>
    (function () {{
      if (localStorage.getItem('bugwrite-theme') === 'dark') {{
        document.documentElement.classList.add('dark');
      }}
    }})();
  </script>"""


def esc(s):
    return html.escape(str(s or ""), quote=True)


def get_cat_slug(category):
    if category in ("Gaming", "Deals"):
        return "gaming"
    if category in ("Security", "Cybersecurity"):
        return "security"
    if category in ("Business", "Enterprise"):
        return "business"
    if category in ("Big Tech", "Tech News", "Cloud", "Social Media"):
        return "big-tech"
    return re.sub(r"[^a-z0-9]+", "-", str(category or "news").lower()).strip("-")


def get_cat_label(slug):
    return {
        "gaming": "Gaming",
        "big-tech": "Big Tech",
        "security": "Security",
        "business": "Business",
    }.get(slug, "News")


def get_article_path(art):
    return f"/{get_cat_slug(art['category'])}/article/{art['id']}"


def load_articles():
    node_cmd = (
        "const fs=require('fs'); const vm=require('vm'); "
        f"const ctx={{window:{{}}}}; vm.runInNewContext(fs.readFileSync({json.dumps(DATA_JS)},'utf8'), ctx); "
        "process.stdout.write(JSON.stringify(ctx.window.BUGWRITE_ARTICLES));"
    )
    res = subprocess.run(["node", "-e", node_cmd], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def parse_iso_date(date_str):
    try:
        dt = datetime.strptime(date_str.strip(), "%b %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return LASTMOD


def build_announcement_bar(is_spa=False):
    guide_href = "/gaming/article/when-is-gta-6-playable-release-times"
    onclick = " onclick=\"event.preventDefault(); openArticleView('when-is-gta-6-playable-release-times')\"" if is_spa else ""
    return f"""  <!-- GTA 6 LAUNCH COUNTDOWN ANNOUNCEMENT BAR -->
  <div id="gta-announcement-bar" class="bg-neutral-950 dark:bg-[#161a22] text-white border-b border-neutral-800">
    <div class="max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8 py-2 flex items-center justify-between gap-3 text-xs">
      <div class="w-4 hidden sm:block shrink-0" aria-hidden="true"></div>
      <div class="flex flex-wrap items-center justify-center gap-x-2.5 gap-y-1 text-center">
        <span class="font-bold uppercase tracking-[0.09em] text-neutral-200">GTA VI Launch</span>
        <span class="text-neutral-600 hidden sm:inline">|</span>
        <span id="gta-countdown-text" class="text-neutral-300">Unlocks Nov 19 at midnight local time:</span>
        <span id="gta-countdown-timer" class="font-bold tabular-nums tracking-wider text-white">00h 00m 00s</span>
        <a href="{guide_href}"{onclick} class="ml-1 font-semibold underline underline-offset-4 text-neutral-200 hover:text-white transition-colors">
          Launch Guide &rarr;
        </a>
      </div>
      <button id="dismiss-announcement-btn" type="button" aria-label="Dismiss announcement bar" class="text-neutral-400 hover:text-white transition-colors cursor-pointer shrink-0 p-0.5">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>
  </div>"""


def build_header(active_slug="all", is_spa=False):
    nav_items = [
        ("all", "/", "News", "All"),
        ("gaming", "/gaming", "Gaming", "Gaming"),
        ("gta6", "/#gta6-hub", "GTA VI", None),
        ("big-tech", "/big-tech", "Big Tech", "Big Tech"),
        ("security", "/security", "Security", "Security"),
        ("business", "/business", "Business", "Business"),
    ]

    desktop_links = []
    mobile_links = []
    for slug, href, label, spa_cat in nav_items:
        is_active = (slug == active_slug)
        cls_d = "nav-cat hover:text-black dark:hover:text-white py-2 transition-colors"
        if is_active or slug == "gta6":
            cls_d += " text-black dark:text-white font-semibold"
        if is_spa and spa_cat is not None:
            desktop_links.append(
                f'<a href="{href}" data-cat="{spa_cat}" onclick="event.preventDefault(); filterCategory(\'{spa_cat}\')" class="{cls_d}">{label}</a>'
            )
            mobile_links.append(
                f'<a href="{href}" onclick="event.preventDefault(); filterCategory(\'{spa_cat}\')" class="hover:text-black dark:hover:text-white{" font-semibold text-neutral-900 dark:text-white" if is_active else ""}">{label}</a>'
            )
        elif is_spa and slug == "gta6":
            desktop_links.append(
                f'<a href="{href}" onclick="event.preventDefault(); jumpToGtaHub()" class="{cls_d}">{label}</a>'
            )
            mobile_links.append(
                f'<a href="{href}" onclick="event.preventDefault(); jumpToGtaHub()" class="font-semibold text-neutral-900 dark:text-white hover:text-black">{label}</a>'
            )
        else:
            desktop_links.append(f'<a href="{href}" class="{cls_d}">{label}</a>')
            mobile_links.append(
                f'<a href="{href}" class="hover:text-black dark:hover:text-white{" font-semibold text-neutral-900 dark:text-white" if (is_active or slug == "gta6") else ""}">{label}</a>'
            )

    logo_onclick = ' onclick="resetHome(event)"' if is_spa else ""
    search_btn = """        <button id="search-toggle-btn" aria-label="Search articles" class="p-1.5 text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white transition-colors cursor-pointer">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </button>""" if is_spa else """        <a href="/?search=1" aria-label="Search Bugwrite" class="p-1.5 text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </a>"""

    search_drawer = """    <!-- Live Search Dropdown Drawer -->
    <div id="search-drawer" class="hidden border-t border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-[#14171c] px-4 py-3">
      <div class="max-w-[1240px] mx-auto flex items-center gap-3">
        <svg class="w-4 h-4 text-neutral-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input id="search-input" type="text" placeholder="Search Bugwrite coverage (GTA 6, Apple, ARTEX, Java4Shell, Nvidia, Xbox, PlayStation...)" class="w-full bg-transparent text-sm focus:outline-none text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500" />
        <button id="clear-search-btn" class="text-xs text-neutral-500 dark:text-neutral-400 hover:text-black dark:hover:text-white uppercase font-medium cursor-pointer">Close</button>
      </div>
    </div>""" if is_spa else ""

    return f"""  <!-- TOP NAVIGATION HEADER -->
  <header class="sticky top-0 z-40 bg-white dark:bg-[#0d0f12] border-b border-neutral-200/90 dark:border-neutral-800 shadow-[0_1px_2px_rgba(0,0,0,0.03)]">
    <div class="max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8 h-[56px] flex items-center justify-between">
      <div class="flex items-center gap-6 lg:gap-8">
        <a href="/" id="site-logo"{logo_onclick} class="flex items-center select-none group">
          <span class="text-[24px] font-black tracking-[-0.055em] text-black dark:text-white leading-none lowercase">bugwrite</span>
        </a>
        <nav aria-label="Primary navigation" class="hidden xl:flex items-center gap-6 text-[13px] font-medium text-neutral-700 dark:text-neutral-300" id="desktop-nav">
          {' '.join(desktop_links)}
        </nav>
      </div>
      <div class="flex items-center gap-3">
{search_btn}
        <button id="theme-toggle-btn" type="button" aria-label="Toggle dark and light mode" class="inline-flex items-center gap-1.5 text-[12px] font-medium text-neutral-800 dark:text-neutral-200 hover:text-black dark:hover:text-white border border-neutral-300 dark:border-neutral-700 hover:border-neutral-400 dark:hover:border-neutral-500 px-3 py-1.5 rounded-md transition-colors cursor-pointer">
          <svg id="theme-icon-moon" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
          </svg>
          <svg id="theme-icon-sun" class="w-3.5 h-3.5 hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="5"></circle>
            <path stroke-linecap="round" d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
          </svg>
          <span id="theme-toggle-label">Dark</span>
        </button>
        <button id="mobile-menu-btn" aria-label="Toggle categories" class="xl:hidden p-1.5 text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white cursor-pointer">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
    </div>
    <div id="mobile-nav-drawer" class="hidden xl:hidden border-t border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#0d0f12] px-4 py-2.5 overflow-x-auto">
      <div class="flex items-center gap-4 text-[13px] font-medium text-neutral-700 dark:text-neutral-300 whitespace-nowrap">
        {' '.join(mobile_links)}
      </div>
    </div>
{search_drawer}
  </header>"""


def build_footer():
    return """  <!-- EDITORIAL FOOTER -->
  <footer class="border-t border-neutral-200 dark:border-neutral-800 mt-16 bg-neutral-50/70 dark:bg-[#12151a] text-neutral-600 dark:text-neutral-400 text-xs py-12">
    <div class="max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 pb-8 border-b border-neutral-200/80 dark:border-neutral-800">
        <div class="md:col-span-5">
          <a href="/" class="inline-block text-xl font-black tracking-[-0.055em] text-black dark:text-white lowercase mb-2">bugwrite</a>
          <p class="text-xs leading-relaxed text-neutral-500 dark:text-neutral-400 max-w-sm">
            Independent technology, gaming, cybersecurity, and AI business journalism. Fact-checked daily reporting, outage status coverage, and launch guides.
          </p>
        </div>
        <div class="md:col-span-3">
          <h3 class="text-[11px] font-bold uppercase tracking-[0.08em] text-neutral-900 dark:text-neutral-200 mb-3">Desks</h3>
          <div class="flex flex-col gap-2">
            <a href="/gaming" class="hover:text-black dark:hover:text-white transition-colors">Gaming</a>
            <a href="/big-tech" class="hover:text-black dark:hover:text-white transition-colors">Big Tech</a>
            <a href="/security" class="hover:text-black dark:hover:text-white transition-colors">Security</a>
            <a href="/business" class="hover:text-black dark:hover:text-white transition-colors">Business</a>
          </div>
        </div>
        <div class="md:col-span-4">
          <h3 class="text-[11px] font-bold uppercase tracking-[0.08em] text-neutral-900 dark:text-neutral-200 mb-3">Company &amp; Policies</h3>
          <div class="flex flex-col gap-2">
            <a href="/about" class="hover:text-black dark:hover:text-white transition-colors">About Bugwrite</a>
            <a href="/contact" class="hover:text-black dark:hover:text-white transition-colors">Contact &amp; News Tips</a>
            <a href="/privacy-policy" class="hover:text-black dark:hover:text-white transition-colors">Privacy Policy</a>
            <a href="/terms-of-service" class="hover:text-black dark:hover:text-white transition-colors">Terms of Service</a>
            <a href="/rss.xml" class="hover:text-black dark:hover:text-white transition-colors">RSS Feed</a>
            <a href="/sitemap.xml" class="hover:text-black dark:hover:text-white transition-colors">XML Sitemap</a>
          </div>
        </div>
      </div>
      <div class="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-neutral-500 dark:text-neutral-500">
        <span>&copy; 2026 Bugwrite Media. All rights reserved.</span>
        <span>Published at www.bugwrite.com</span>
      </div>
    </div>
  </footer>"""


SHARED_FOOTER_SCRIPT = """  <script>
    (function () {
      const mobileBtn = document.getElementById('mobile-menu-btn');
      const mobileDrawer = document.getElementById('mobile-nav-drawer');
      if (mobileBtn && mobileDrawer) {
        mobileBtn.addEventListener('click', () => mobileDrawer.classList.toggle('hidden'));
      }

      const themeBtn = document.getElementById('theme-toggle-btn');
      const moon = document.getElementById('theme-icon-moon');
      const sun = document.getElementById('theme-icon-sun');
      const label = document.getElementById('theme-toggle-label');
      function syncTheme() {
        const isDark = document.documentElement.classList.contains('dark');
        if (moon && sun && label) {
          moon.classList.toggle('hidden', isDark);
          sun.classList.toggle('hidden', !isDark);
          label.textContent = isDark ? 'Light' : 'Dark';
        }
      }
      if (themeBtn) {
        themeBtn.addEventListener('click', () => {
          const isDark = document.documentElement.classList.toggle('dark');
          localStorage.setItem('bugwrite-theme', isDark ? 'dark' : 'light');
          syncTheme();
        });
      }
      syncTheme();

      const bar = document.getElementById('gta-announcement-bar');
      const timerEl = document.getElementById('gta-countdown-timer');
      const textEl = document.getElementById('gta-countdown-text');
      const dismissBtn = document.getElementById('dismiss-announcement-btn');
      if (bar && timerEl) {
        const target = new Date(2026, 10, 19, 0, 0, 0).getTime();
        const pad = (n) => String(n).padStart(2, '0');
        function tick() {
          const diff = target - Date.now();
          if (diff <= 0) {
            textEl.textContent = 'Grand Theft Auto VI is live now on PS5 and Xbox Series X|S.';
            timerEl.textContent = '';
            timerEl.classList.add('hidden');
            return;
          }
          const days = Math.floor(diff / 86400000);
          const hours = Math.floor((diff % 86400000) / 3600000);
          const mins = Math.floor((diff % 3600000) / 60000);
          const secs = Math.floor((diff % 60000) / 1000);
          timerEl.textContent = days > 0
            ? `${pad(days)}d ${pad(hours)}h ${pad(mins)}m ${pad(secs)}s`
            : `${pad(hours)}h ${pad(mins)}m ${pad(secs)}s`;
        }
        tick();
        setInterval(tick, 1000);
        if (dismissBtn) {
          dismissBtn.addEventListener('click', () => bar.classList.add('hidden'));
        }
      }
    })();
  </script>"""


def render_static_card(art, heading_tag="h2", is_spa=False, eager=False):
    href = get_article_path(art)
    onclick = f" onclick=\"event.preventDefault(); openArticleView('{art['id']}')\"" if is_spa else ""
    load_attr = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f"""        <article class="flex flex-col group">
          <a href="{href}"{onclick} class="flex flex-col flex-1">
            <div class="relative w-full overflow-hidden rounded-[6px] bg-neutral-100 dark:bg-neutral-800 aspect-[16/9]">
              <img src="{art['image']}?v=bit1" alt="{esc(art['imageAlt'])}" width="1280" height="720" {load_attr} class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-300" />
            </div>
            <{heading_tag} class="text-[15px] font-bold text-neutral-900 dark:text-neutral-100 leading-[1.28] tracking-[-0.015em] mt-2.5 mb-1.5 article-headline">{esc(art['title'])}</{heading_tag}>
            <div class="flex items-center text-[12px] text-neutral-500 dark:text-neutral-400 font-normal mt-0.5">
              <span>{esc(art['author'])}</span>
              <span class="mx-1.5 text-neutral-400 dark:text-neutral-600">&bull;</span>
              <span>{esc(art['publishedAgo'])}</span>
            </div>
          </a>
        </article>"""


def render_static_featured(art, companions, is_spa=False):
    href = get_article_path(art)
    onclick = f" onclick=\"event.preventDefault(); openArticleView('{art['id']}')\"" if is_spa else ""
    comp_rows = []
    for c_art in companions:
        chref = get_article_path(c_art)
        conc = f" onclick=\"event.preventDefault(); openArticleView('{c_art['id']}')\"" if is_spa else ""
        comp_rows.append(
            f'            <a href="{chref}"{conc} class="w-full text-left flex items-baseline justify-between gap-3 text-[13px] text-neutral-700 dark:text-neutral-300 hover:text-blue-700 dark:hover:text-blue-400 transition-colors group/sub">'
            f'<span class="font-medium leading-snug line-clamp-1">{esc(c_art["title"])}</span>'
            f'<span class="text-neutral-400 dark:text-neutral-500 group-hover/sub:text-blue-700 dark:group-hover/sub:text-blue-400 shrink-0">&rarr;</span></a>'
        )
    comp_html = (
        f'          <div class="mt-auto pt-4 border-t border-neutral-200/75 dark:border-neutral-800/90 space-y-2">\n'
        + "\n".join(comp_rows)
        + "\n          </div>"
    ) if comp_rows else ""

    return f"""        <article class="flex flex-col h-full group">
          <a href="{href}"{onclick} class="block">
            <div class="relative w-full overflow-hidden rounded-[6px] bg-neutral-100 dark:bg-neutral-800 aspect-[16/9]">
              <img src="{art['image']}?v=bit1" alt="{esc(art['imageAlt'])}" width="1280" height="720" loading="eager" fetchpriority="high" class="w-full h-full object-cover group-hover:scale-[1.015] transition-transform duration-300" />
            </div>
            <div class="mt-4 mb-1.5 flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.09em]">
              <span class="text-blue-700 dark:text-blue-400">{esc(art['category'])}</span>
              <span class="text-neutral-300 dark:text-neutral-700">/</span>
              <span class="text-neutral-500 dark:text-neutral-400 font-semibold">{esc(art['publishedDate'])}</span>
            </div>
            <h1 class="text-2xl sm:text-[30px] lg:text-[32px] font-bold text-neutral-950 dark:text-white leading-[1.15] tracking-[-0.03em] mb-3 article-headline">
              {esc(art['title'])}
            </h1>
            <p class="text-[15px] sm:text-base text-neutral-600 dark:text-neutral-400 font-normal leading-[1.6] mb-5">
              {esc(art['dek'])}
            </p>
          </a>
{comp_html}
          <a href="{href}"{onclick} class="mt-4 pt-3.5 border-t border-neutral-200 dark:border-neutral-800 flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center text-xs text-neutral-500 dark:text-neutral-400">
              <span class="font-semibold text-neutral-900 dark:text-neutral-100">{esc(art['author'])}</span>
              <span class="mx-1.5 text-neutral-400 dark:text-neutral-600">&bull;</span>
              <span>{esc(art['publishedAgo'])}</span>
              <span class="mx-1.5 text-neutral-400 dark:text-neutral-600">&bull;</span>
              <span>{esc(art['readTime'])}</span>
            </div>
            <span class="inline-flex items-center gap-1 text-[13px] font-bold text-neutral-950 dark:text-white group-hover:text-blue-700 dark:group-hover:text-blue-400 transition-colors">
              Read Story
              <span class="inline-block transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
            </span>
          </a>
        </article>"""


# ============================================================
# HOMEPAGE 650-750 WORD SEO EDITORIAL GUIDE & FAQ
# ============================================================
FAQ_ITEMS = [
    (
        "What topics does Bugwrite cover every day?",
        "Bugwrite publishes daily reporting, explainers, and buyer guides across four primary desks: Gaming, Big Tech, Security, and Business. Coverage spans major video game launches like Grand Theft Auto VI, live platform outages across Apple, Microsoft, Google, and Amazon, critical CVE advisories, and semiconductor and AI market developments."
    ),
    (
        "How does Bugwrite verify breaking outages and cybersecurity alerts?",
        "Before publishing any outage or security story, our editors cross-check primary status dashboards, official vendor advisories, CVE databases such as Red Hat and NVD, and federal alerts from agencies like the FBI and CISA. Whenever user-reported outage spikes turn out to be localized or unrelated false alarms, we clearly separate confirmed disruptions from speculation."
    ),
    (
        "Where can readers find GTA 6 release times, guides, and updates?",
        "Every GTA 6 launch guide, including local midnight unlock schedules, preload storage requirements, Metacritic review tracking, campaign length estimates, Leonida map breakdowns, and edition comparisons, is organized inside the dedicated GTA VI section on our homepage and under the Gaming desk at bugwrite.com/gaming."
    ),
    (
        "Is Bugwrite free to read without a paid subscription?",
        "Yes. Every news article, security explainer, launch countdown tool, and buying guide on Bugwrite is completely free to access on desktop and mobile with no paywall or account registration required."
    ),
]

HOMEPAGE_SEO_GUIDE_HTML = """    <!-- SEO EDITORIAL GUIDE & FAQ SECTION (Cleanly styled below the main feed) -->
    <section id="editorial-guide" aria-label="About Bugwrite News Platform and Reader Guide" class="mt-14 pt-10 border-t border-neutral-200/90 dark:border-neutral-800">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        <div class="lg:col-span-7 space-y-5">
          <p class="text-[11px] font-bold uppercase tracking-[0.09em] text-neutral-500 dark:text-neutral-400">Editorial Guide</p>
          <h2 class="text-2xl sm:text-[26px] font-bold text-neutral-950 dark:text-white tracking-[-0.025em] leading-tight">
            Bugwrite: Independent Tech, Gaming, Cybersecurity, and AI Business News
          </h2>
          <p class="text-sm sm:text-[15px] leading-relaxed text-neutral-600 dark:text-neutral-400">
            Bugwrite is a free, fast-loading technology and gaming news publication built for readers who want verified facts without clickbait padding. Whether a global cloud outage knocks out workplace email, a critical software vulnerability forces emergency server patching, or a generational console release approaches midnight unlock, Bugwrite brings the essential context onto one uncluttered page.
          </p>

          <h3 class="text-base font-bold text-neutral-900 dark:text-neutral-100 pt-1">How to Use Bugwrite to Track Breaking Tech and Gaming Coverage</h3>
          <p class="text-sm sm:text-[15px] leading-relaxed text-neutral-600 dark:text-neutral-400">
            Start at the top of the homepage for our lead breaking story and four sub-featured reports covering the day's highest-impact technology, security, and gaming developments. Right below the main headlines, our launch-week GTA VI hub gathers release times, storage guides, Metacritic tracking, and gameplay explainers in one place. Scroll beneath the divider to browse our recently uploaded articles in a four-column feed, or click Load more stories to expand additional rows.
          </p>
          <p class="text-sm sm:text-[15px] leading-relaxed text-neutral-600 dark:text-neutral-400">
            To jump straight to a specific beat, use the top navigation bar to switch between Gaming, Big Tech, Security, and Business. You can also open the instant search bar in the header to filter across all published articles by keyword, CVE identifier, company name, or game title, and switch between light and dark reading modes at any time using the header toggle.
          </p>

          <h3 class="text-base font-bold text-neutral-900 dark:text-neutral-100 pt-1">Key Coverage Desks and Editorial Standards</h3>
          <p class="text-sm sm:text-[15px] leading-relaxed text-neutral-600 dark:text-neutral-400">
            Every story published on Bugwrite follows a strict verification workflow. Our Security desk tracks real-world flaws like OpenJDK's Java4Shell vulnerability, autonomous AI intrusion tools flagged by the FBI, and practical defense guides for everyday users and IT administrators. Our Big Tech desk separates genuine platform failures at Apple, Microsoft, Amazon, and Google from social-media outage rumors while explaining major operating system updates like Android 17 and iOS 27.
          </p>
          <p class="text-sm sm:text-[15px] leading-relaxed text-neutral-600 dark:text-neutral-400">
            On the Gaming desk, reporters combine verified publisher announcements, patch notes, and hardware market tracking across PlayStation 5, Xbox Series X|S, Nintendo Switch 2, and Windows PC. Meanwhile, our Business desk examines the economics behind artificial intelligence, from Nvidia earnings and Anthropic's public listing to data center power demand, semiconductor export rules, and startup infrastructure costs. Every article is designed to deliver clear answers, accurate citations, and fast reading on every screen.
          </p>

          <h3 class="text-base font-bold text-neutral-900 dark:text-neutral-100 pt-1">Built for Fast Reading, Clean Navigation, and Daily Use</h3>
          <p class="text-sm sm:text-[15px] leading-relaxed text-neutral-600 dark:text-neutral-400">
            Whether you are an IT administrator checking live cloud health during a workday outage, an investor tracking semiconductor policy and quarterly earnings, or a player comparing console editions before a midnight launch, Bugwrite keeps navigation straightforward. Clean category URLs, lightweight custom bit-graphics illustrations, persistent dark mode, and full-text keyword search let you move from breaking headlines to in-depth explainers in seconds without pop-up walls or distracting clutter.
          </p>
        </div>

        <div class="lg:col-span-5">
          <div class="rounded-lg border border-neutral-200 dark:border-neutral-800 bg-neutral-50/70 dark:bg-[#12151b] p-6">
            <p class="text-[11px] font-bold uppercase tracking-[0.09em] text-neutral-500 dark:text-neutral-400 mb-1">Frequently Asked Questions</p>
            <h2 class="text-lg font-bold text-neutral-950 dark:text-white tracking-tight mb-5">Quick Answers for Readers</h2>
            <div class="divide-y divide-neutral-200 dark:divide-neutral-800">
              """ + "\n              ".join(
    f"""<div class="py-4 first:pt-0 last:pb-0">
                <h3 class="text-sm font-bold text-neutral-900 dark:text-neutral-100 mb-1.5">{esc(q)}</h3>
                <p class="text-xs sm:text-[13px] leading-relaxed text-neutral-600 dark:text-neutral-400">{esc(a)}</p>
              </div>"""
    for q, a in FAQ_ITEMS
) + """
            </div>
          </div>
        </div>
      </div>
    </section>"""


def write_file(rel_path, content):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def build_head(
    title,
    desc,
    canonical,
    og_type="website",
    og_image=f"{DOMAIN}/blog/articles/gta6-release-time.jpg",
    schemas=None,
    robots="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
    og_image_alt="Bugwrite editorial illustration",
    preload_image=None,
    extra_meta="",
):
    schema_tags = []
    for sc in (schemas or []):
        schema_tags.append(
            '  <script type="application/ld+json">\n'
            + json.dumps(sc, indent=2, ensure_ascii=False)
            + "\n  </script>"
        )
    schema_html = "\n".join(schema_tags)
    preload_tag = f'  <link rel="preload" as="image" href="{esc(preload_image)}" fetchpriority="high" />\n' if preload_image else ""
    extra_block = f"{extra_meta}\n" if extra_meta else ""
    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="{robots}" />
  <meta name="googlebot" content="{robots}" />
  <link rel="canonical" href="{esc(canonical)}" />
{preload_tag}
  <!-- Open Graph Metadata -->
  <meta property="og:site_name" content="Bugwrite" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{esc(canonical)}" />
  <meta property="og:image" content="{esc(og_image)}" />
  <meta property="og:image:width" content="1280" />
  <meta property="og:image:height" content="720" />
  <meta property="og:image:alt" content="{esc(og_image_alt)}" />
{extra_block}  <!-- Twitter Card Metadata -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{esc(og_image)}" />
  <meta name="twitter:image:alt" content="{esc(og_image_alt)}" />

{GA4_SNIPPET}
{SHARED_STYLES}
{schema_html}
</head>"""


def generate_homepage(articles):
    featured = next((a for a in articles if a["slot"] == "featured"), articles[0])
    subfeatured = [a for a in articles if a["slot"] == "subfeatured"][:4]
    gta_hub = [a for a in articles if a["slot"] == "gta6-hub"][:4]
    used = {featured["id"], *(a["id"] for a in subfeatured), *(a["id"] for a in gta_hub)}
    recent_all = [a for a in articles if a["id"] not in used]
    recent_initial = recent_all[:8]
    remaining = max(0, len(recent_all) - len(recent_initial))

    featured_html = render_static_featured(featured, gta_hub[:2], is_spa=True)
    subfeatured_html = "\n".join(render_static_card(a, "h2", is_spa=True, eager=False) for a in subfeatured)
    gta_hub_html = "\n".join(render_static_card(a, "h3", is_spa=True, eager=False) for a in gta_hub)
    recent_html = "\n".join(render_static_card(a, "h3", is_spa=True, eager=False) for a in recent_initial)

    home_title = "Bugwrite: Tech, Gaming, Cybersecurity & Business News"
    home_desc = "Independent tech, gaming, cybersecurity, and AI business news from Bugwrite. Read GTA 6 launch guides, outage reports, and verified daily coverage."

    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Bugwrite",
            "url": f"{DOMAIN}/",
            "description": home_desc,
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{DOMAIN}/?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        },
        {
            "@context": "https://schema.org",
            **PUBLISHER_ORG,
        },
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Bugwrite News & Launch Tracker",
            "url": f"{DOMAIN}/",
            "applicationCategory": "NewsApplication",
            "operatingSystem": "All",
            "description": "Free real-time technology, gaming, cybersecurity, and AI business news platform with live search and launch countdown tools.",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}
                }
                for q, a in FAQ_ITEMS
            ]
        }
    ]

    head = build_head(
        home_title,
        home_desc,
        f"{DOMAIN}/",
        "website",
        f"{DOMAIN}{featured['image']}",
        schemas,
        og_image_alt=featured["imageAlt"],
        preload_image=f"{featured['image']}?v=bit1",
    )
    body = f"""<body class="bg-white dark:bg-[#0d0f12] text-neutral-900 dark:text-neutral-100 font-sans selection:bg-neutral-200 dark:selection:bg-neutral-700">

{build_announcement_bar(is_spa=True)}

{build_header(active_slug="all", is_spa=True)}

  <!-- HOME FEED VIEW (Pre-rendered static crawlable HTML + progressive enhancement) -->
  <main id="home-view" class="max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-7">

    <div id="filter-status-bar" class="hidden mb-6 pb-3 border-b border-neutral-200 dark:border-neutral-800 flex items-center justify-between">
      <div class="text-sm text-neutral-700 dark:text-neutral-300">
        Showing results for <span id="filter-label" class="font-bold text-black dark:text-white"></span>
        <span id="filter-count" class="text-neutral-400 ml-1"></span>
      </div>
      <button type="button" onclick="resetHome()" class="text-xs font-semibold text-blue-700 dark:text-blue-400 hover:underline cursor-pointer">Clear filter</button>
    </div>

    <!-- ZONE 1 & ZONE 2: FEATURED GTA 6 HERO (LEFT) + 4 SUB-FEATURED (RIGHT 2x2) -->
    <section id="featured-section" aria-label="Featured coverage">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-x-7 gap-y-8 items-start">
        <div id="featured-slot" class="lg:col-span-6 lg:pr-7 lg:border-r lg:border-neutral-200/80 dark:lg:border-neutral-800">
{featured_html}
        </div>
        <div id="subfeatured-slot" class="lg:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-x-5 gap-y-6 content-start">
{subfeatured_html}
        </div>
      </div>
    </section>

    <!-- DEDICATED GTA 6 FEATURED LAUNCH SECTION -->
    <section id="gta6-hub" aria-label="GTA 6 Launch Coverage" class="mt-9 pt-8 border-t border-neutral-200/90 dark:border-neutral-800 scroll-mt-20">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6">
        <div>
          <p class="text-[11px] font-bold uppercase tracking-[0.08em] text-neutral-500 dark:text-neutral-400 mb-1">GTA VI Coverage</p>
          <h2 class="text-xl sm:text-2xl font-bold text-neutral-950 dark:text-white tracking-[-0.02em]">Latest GTA 6 News, Guides &amp; Reviews</h2>
        </div>
        <a href="/gaming" onclick="event.preventDefault(); filterCategory('Gaming')" class="inline-flex items-center gap-1 text-xs font-bold uppercase tracking-wider text-neutral-800 dark:text-neutral-200 hover:text-blue-700 dark:hover:text-blue-400 transition-colors shrink-0">
          All Gaming News
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.4" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"></path></svg>
        </a>
      </div>

      <div id="gta6-hub-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-5 gap-y-7">
{gta_hub_html}
      </div>

      <div class="mt-6 pt-4 border-t border-neutral-100 dark:border-neutral-800/80 flex flex-wrap items-center justify-between gap-3 text-xs text-neutral-500 dark:text-neutral-400">
        <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
          <span class="font-bold text-neutral-800 dark:text-neutral-200">More Gaming News:</span>
          <button type="button" onclick="quickSearch('Xbox')" class="hover:text-black dark:hover:text-white cursor-pointer">Xbox</button>
          <span class="text-neutral-300 dark:text-neutral-700">&middot;</span>
          <button type="button" onclick="quickSearch('PlayStation')" class="hover:text-black dark:hover:text-white cursor-pointer">PlayStation</button>
          <span class="text-neutral-300 dark:text-neutral-700">&middot;</span>
          <button type="button" onclick="quickSearch('PC')" class="hover:text-black dark:hover:text-white cursor-pointer">PC Gaming</button>
          <span class="text-neutral-300 dark:text-neutral-700">&middot;</span>
          <button type="button" onclick="quickSearch('Game Awards')" class="hover:text-black dark:hover:text-white cursor-pointer">Game Awards</button>
        </div>
        <span class="text-[11px] text-neutral-400 dark:text-neutral-500">Updated for November 19 console launch</span>
      </div>
    </section>

    <!-- ZONE 3: RECENTLY UPLOADED BLOGS (4-Column Grid Under the Divider Line) -->
    <section id="recent-section" aria-label="Recently uploaded articles" class="mt-9 pt-8 border-t border-neutral-200/90 dark:border-neutral-800">
      <div class="flex items-center justify-between mb-5">
        <h2 id="recent-heading" class="text-xs font-bold uppercase tracking-[0.08em] text-neutral-500 dark:text-neutral-400">Recently Uploaded</h2>
        <span id="recent-counter" class="text-xs text-neutral-400 dark:text-neutral-500">{len(recent_initial)} of {len(recent_all)} stories</span>
      </div>

      <div id="recent-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-5 gap-y-8">
{recent_html}
      </div>

      <div id="load-more-wrap" class="{'hidden ' if remaining == 0 else ''}mt-10 text-center">
        <button id="load-more-btn" type="button" onclick="loadMoreRecent()" class="inline-flex items-center justify-center px-6 py-2.5 text-xs font-semibold uppercase tracking-wider text-neutral-900 dark:text-neutral-100 bg-white dark:bg-[#161a20] border border-neutral-300 dark:border-neutral-700 hover:border-black dark:hover:border-neutral-400 hover:bg-neutral-50 dark:hover:bg-[#1e232b] rounded-md transition-colors cursor-pointer">
          Load more stories ({remaining} remaining)
        </button>
      </div>
    </section>

{HOMEPAGE_SEO_GUIDE_HTML}

  </main>

  <!-- CLIENT-SIDE INSTANT ARTICLE READER VIEW (Strictly H2 while hidden so raw HTML keeps one H1) -->
  <article id="article-view" class="hidden max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
    <div class="max-w-[760px] mx-auto">
      <div class="mb-6 flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400">
        <button type="button" onclick="closeArticleView()" class="inline-flex items-center gap-1.5 font-semibold text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white transition-colors cursor-pointer">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"></path></svg>
          Back to Bugwrite
        </button>
        <span id="reader-category" class="font-bold uppercase tracking-wider text-blue-700 dark:text-blue-400"></span>
      </div>

      <p id="reader-title" role="heading" aria-level="1" class="text-3xl sm:text-4xl lg:text-[40px] font-bold text-neutral-950 dark:text-white leading-[1.15] tracking-[-0.03em] mb-4"></p>
      <p id="reader-dek" class="text-lg sm:text-[19px] text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6"></p>

      <div class="flex flex-wrap items-center justify-between gap-4 py-4 border-y border-neutral-200 dark:border-neutral-800 mb-7 text-xs text-neutral-500 dark:text-neutral-400">
        <div class="flex items-center gap-2.5">
          <div id="reader-avatar" class="w-8 h-8 rounded-full bg-neutral-900 dark:bg-neutral-200 text-white dark:text-neutral-900 font-bold flex items-center justify-center text-xs"></div>
          <div>
            <div class="text-neutral-900 dark:text-neutral-100 font-semibold text-[13px]" id="reader-author"></div>
            <div class="text-neutral-500 dark:text-neutral-400" id="reader-role"></div>
          </div>
        </div>
        <div class="flex items-center gap-2 text-neutral-500 dark:text-neutral-400">
          <span id="reader-date"></span>
          <span>&bull;</span>
          <span id="reader-readtime"></span>
        </div>
      </div>

      <figure class="mb-8">
        <div class="overflow-hidden rounded-[6px] bg-neutral-100 dark:bg-neutral-800 aspect-[16/9]">
          <img id="reader-image" src="/blog/articles/gta6-release-time.jpg?v=bit1" alt="Featured article illustration" width="1280" height="720" class="w-full h-full object-cover" />
        </div>
        <figcaption id="reader-caption" class="mt-2.5 text-xs text-neutral-500 dark:text-neutral-400"></figcaption>
      </figure>

      <div id="reader-body" class="article-prose"></div>
      <div id="reader-tags" class="mt-10 pt-6 border-t border-neutral-200 dark:border-neutral-800 flex flex-wrap items-center gap-2"></div>
    </div>

    <div class="mt-14 pt-10 border-t border-neutral-200 dark:border-neutral-800">
      <h2 class="text-xs font-bold uppercase tracking-[0.08em] text-neutral-500 dark:text-neutral-400 mb-6">More from Bugwrite</h2>
      <div id="related-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-5 gap-y-8"></div>
    </div>
  </article>

{build_footer()}

  <script src="/blog/articles-data.js"></script>
  <script>
    const ALL_ARTICLES = window.BUGWRITE_ARTICLES || [];
    const SITE_DOMAIN = '{DOMAIN}';
    let activeCategory = 'All';
    let activeSearch = '';
    let visibleRecentCount = 8;

    function escapeHtml(str) {{
      return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }}

    function getCategorySlug(category) {{
      if (category === 'Gaming' || category === 'Deals') return 'gaming';
      if (category === 'Security' || category === 'Cybersecurity') return 'security';
      if (category === 'Business' || category === 'Enterprise') return 'business';
      if (category === 'Big Tech' || category === 'Tech News' || category === 'Cloud' || category === 'Social Media') return 'big-tech';
      return String(category || 'news').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    }}

    function getCategoryFromSlug(slug) {{
      return ({{ 'gaming': 'Gaming', 'security': 'Security', 'business': 'Business', 'big-tech': 'Big Tech' }})[slug] || null;
    }}

    function getArticleUrl(article) {{
      return `/${{getCategorySlug(article.category)}}/article/${{article.id}}`;
    }}

    function updateCanonical(path) {{
      const link = document.querySelector('link[rel="canonical"]');
      if (link) link.setAttribute('href', `${{SITE_DOMAIN}}${{path === '/' ? '/' : path}}`);
    }}

    function safePushUrl(path, state = {{}}) {{
      if (window.location.protocol === 'file:') return;
      if (window.location.pathname !== path || window.location.hash) {{
        history.pushState(state, '', path);
      }}
      updateCanonical(path);
    }}

    function renderFeaturedCard(article) {{
      const companions = ALL_ARTICLES.filter(a => a.slot === 'gta6-hub').slice(0, 2);
      const href = getArticleUrl(article);
      const companionHtml = companions.length
        ? `<div class="mt-auto pt-4 border-t border-neutral-200/75 dark:border-neutral-800/90 space-y-2">${{companions.map(c => `<a href="${{getArticleUrl(c)}}" onclick="event.preventDefault(); openArticleView('${{c.id}}')" class="w-full text-left flex items-baseline justify-between gap-3 text-[13px] text-neutral-700 dark:text-neutral-300 hover:text-blue-700 dark:hover:text-blue-400 transition-colors group/sub"><span class="font-medium leading-snug line-clamp-1">${{escapeHtml(c.title)}}</span><span class="text-neutral-400 dark:text-neutral-500 group-hover/sub:text-blue-700 dark:group-hover/sub:text-blue-400 shrink-0">&rarr;</span></a>`).join('')}}</div>`
        : '';

      return `
        <article class="flex flex-col h-full group">
          <a href="${{href}}" onclick="event.preventDefault(); openArticleView('${{article.id}}')" class="block">
            <div class="relative w-full overflow-hidden rounded-[6px] bg-neutral-100 dark:bg-neutral-800 aspect-[16/9]">
              <img src="${{article.image}}?v=bit1" alt="${{escapeHtml(article.imageAlt)}}" width="1280" height="720" loading="eager" fetchpriority="high" class="w-full h-full object-cover group-hover:scale-[1.015] transition-transform duration-300" />
            </div>
            <div class="mt-4 mb-1.5 flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.09em]">
              <span class="text-blue-700 dark:text-blue-400">${{escapeHtml(article.category)}}</span>
              <span class="text-neutral-300 dark:text-neutral-700">/</span>
              <span class="text-neutral-500 dark:text-neutral-400 font-semibold">${{escapeHtml(article.publishedDate)}}</span>
            </div>
            <h1 class="text-2xl sm:text-[30px] lg:text-[32px] font-bold text-neutral-950 dark:text-white leading-[1.15] tracking-[-0.03em] mb-3 article-headline">${{escapeHtml(article.title)}}</h1>
            <p class="text-[15px] sm:text-base text-neutral-600 dark:text-neutral-400 font-normal leading-[1.6] mb-5">${{escapeHtml(article.dek)}}</p>
          </a>
          ${{companionHtml}}
          <a href="${{href}}" onclick="event.preventDefault(); openArticleView('${{article.id}}')" class="mt-4 pt-3.5 border-t border-neutral-200 dark:border-neutral-800 flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center text-xs text-neutral-500 dark:text-neutral-400">
              <span class="font-semibold text-neutral-900 dark:text-neutral-100">${{escapeHtml(article.author)}}</span>
              <span class="mx-1.5 text-neutral-400 dark:text-neutral-600">&bull;</span>
              <span>${{escapeHtml(article.publishedAgo)}}</span>
              <span class="mx-1.5 text-neutral-400 dark:text-neutral-600">&bull;</span>
              <span>${{escapeHtml(article.readTime)}}</span>
            </div>
            <span class="inline-flex items-center gap-1 text-[13px] font-bold text-neutral-950 dark:text-white group-hover:text-blue-700 dark:group-hover:text-blue-400 transition-colors">
              Read Story <span class="inline-block transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
            </span>
          </a>
        </article>
      `;
    }}

    function renderGridCard(article, tag = 'h3') {{
      const href = getArticleUrl(article);
      return `
        <article class="flex flex-col group">
          <a href="${{href}}" onclick="event.preventDefault(); openArticleView('${{article.id}}')" class="flex flex-col flex-1">
            <div class="relative w-full overflow-hidden rounded-[6px] bg-neutral-100 dark:bg-neutral-800 aspect-[16/9]">
              <img src="${{article.image}}?v=bit1" alt="${{escapeHtml(article.imageAlt)}}" width="1280" height="720" loading="lazy" decoding="async" class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-300" />
            </div>
            <${{tag}} class="text-[15px] font-bold text-neutral-900 dark:text-neutral-100 leading-[1.28] tracking-[-0.015em] mt-2.5 mb-1.5 article-headline">${{escapeHtml(article.title)}}</${{tag}}>
            <div class="flex items-center text-[12px] text-neutral-500 dark:text-neutral-400 font-normal mt-0.5">
              <span>${{escapeHtml(article.author)}}</span>
              <span class="mx-1.5 text-neutral-400 dark:text-neutral-600">&bull;</span>
              <span>${{escapeHtml(article.publishedAgo)}}</span>
            </div>
          </a>
        </article>
      `;
    }}

    function matchesCategory(article, cat) {{
      if (cat === 'All') return true;
      if (cat === 'Gaming') return article.category === 'Gaming' || article.category === 'Deals';
      if (cat === 'Security') return article.category === 'Security' || article.category === 'Cybersecurity';
      if (cat === 'Business') return article.category === 'Business' || article.category === 'Enterprise';
      if (cat === 'Big Tech') return article.category === 'Big Tech' || article.category === 'Tech News' || article.category === 'Cloud' || article.category === 'Social Media';
      return article.category === cat;
    }}

    function renderHomeFeed() {{
      const featuredSection = document.getElementById('featured-section');
      const featuredSlot = document.getElementById('featured-slot');
      const subfeaturedSlot = document.getElementById('subfeatured-slot');
      const gtaHubSection = document.getElementById('gta6-hub');
      const gtaHubGrid = document.getElementById('gta6-hub-grid');
      const recentSection = document.getElementById('recent-section');
      const recentGrid = document.getElementById('recent-grid');
      const recentHeading = document.getElementById('recent-heading');
      const recentCounter = document.getElementById('recent-counter');
      const loadMoreWrap = document.getElementById('load-more-wrap');
      const filterBar = document.getElementById('filter-status-bar');
      const filterLabel = document.getElementById('filter-label');
      const filterCount = document.getElementById('filter-count');
      const guideSection = document.getElementById('editorial-guide');

      const isFiltered = activeCategory !== 'All' || activeSearch.trim() !== '';

      if (!isFiltered) {{
        filterBar.classList.add('hidden');
        featuredSection.classList.remove('hidden');
        gtaHubSection.classList.remove('hidden');
        if (guideSection) guideSection.classList.remove('hidden');
        recentSection.classList.add('mt-9', 'pt-8', 'border-t', 'border-neutral-200/90', 'dark:border-neutral-800');

        const featured = ALL_ARTICLES.find(a => a.slot === 'featured') || ALL_ARTICLES[0];
        const subfeatured = ALL_ARTICLES.filter(a => a.slot === 'subfeatured').slice(0, 4);
        const gtaHub = ALL_ARTICLES.filter(a => a.slot === 'gta6-hub').slice(0, 4);
        const usedIds = new Set([featured.id, ...subfeatured.map(s => s.id), ...gtaHub.map(g => g.id)]);
        const recentAll = ALL_ARTICLES.filter(a => !usedIds.has(a.id));
        const recentVisible = recentAll.slice(0, visibleRecentCount);

        featuredSlot.innerHTML = featured ? renderFeaturedCard(featured) : '';
        subfeaturedSlot.innerHTML = subfeatured.map(a => renderGridCard(a, 'h2')).join('');
        gtaHubGrid.innerHTML = gtaHub.map(a => renderGridCard(a, 'h3')).join('');
        recentHeading.textContent = 'Recently Uploaded';
        recentCounter.textContent = `${{recentVisible.length}} of ${{recentAll.length}} stories`;
        recentGrid.innerHTML = recentVisible.map(a => renderGridCard(a, 'h3')).join('');

        if (recentAll.length > visibleRecentCount) {{
          document.getElementById('load-more-btn').textContent = `Load more stories (${{recentAll.length - visibleRecentCount}} remaining)`;
          loadMoreWrap.classList.remove('hidden');
        }} else {{
          loadMoreWrap.classList.add('hidden');
        }}
      }} else {{
        featuredSection.classList.add('hidden');
        gtaHubSection.classList.add('hidden');
        if (guideSection) guideSection.classList.add('hidden');
        recentSection.classList.remove('mt-9', 'pt-8', 'border-t', 'border-neutral-200/90', 'dark:border-neutral-800');
        loadMoreWrap.classList.add('hidden');

        const query = activeSearch.trim().toLowerCase();
        const filtered = ALL_ARTICLES.filter(a => {{
          const catOk = matchesCategory(a, activeCategory);
          const searchOk = !query ||
            a.title.toLowerCase().includes(query) ||
            a.dek.toLowerCase().includes(query) ||
            a.category.toLowerCase().includes(query) ||
            (a.keywords && a.keywords.some(k => k.toLowerCase().includes(query)));
          return catOk && searchOk;
        }});

        filterBar.classList.remove('hidden');
        filterLabel.textContent = query ? `"${{activeSearch.trim()}}"` : activeCategory;
        filterCount.textContent = `(${{filtered.length}} ${{filtered.length === 1 ? 'article' : 'articles'}})`;
        recentHeading.textContent = query ? 'Search Results' : activeCategory;
        recentCounter.textContent = '';

        recentGrid.innerHTML = filtered.length === 0
          ? `<div class="col-span-full py-16 text-center text-neutral-500 dark:text-neutral-400"><p class="text-base font-medium text-neutral-800 dark:text-neutral-200 mb-1">No matching stories found</p><p class="text-xs">Try searching for GTA 6, Apple, ARTEX, Java4Shell, Nvidia, Xbox, PlayStation, or Anthropic.</p></div>`
          : filtered.map(a => renderGridCard(a, 'h2')).join('');
      }}

      document.querySelectorAll('.nav-cat').forEach(btn => {{
        if (btn.dataset.cat === activeCategory) {{
          btn.classList.add('text-black', 'dark:text-white', 'font-semibold');
        }} else {{
          btn.classList.remove('text-black', 'dark:text-white', 'font-semibold');
        }}
      }});
    }}

    function jumpToGtaHub() {{
      activeCategory = 'All';
      activeSearch = '';
      const searchInput = document.getElementById('search-input');
      if (searchInput) searchInput.value = '';
      closeArticleView(true);
      renderHomeFeed();
      const hub = document.getElementById('gta6-hub');
      if (hub) hub.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}

    function quickSearch(term) {{
      closeArticleView(false);
      activeCategory = 'All';
      activeSearch = term;
      const searchInput = document.getElementById('search-input');
      if (searchInput) searchInput.value = term;
      renderHomeFeed();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function loadMoreRecent() {{
      visibleRecentCount += 8;
      renderHomeFeed();
    }}

    function filterCategory(cat, pushUrl = true) {{
      closeArticleView(false);
      activeCategory = cat;
      activeSearch = '';
      visibleRecentCount = 8;
      const searchInput = document.getElementById('search-input');
      if (searchInput) searchInput.value = '';
      if (pushUrl) safePushUrl(cat === 'All' ? '/' : `/${{getCategorySlug(cat)}}`, {{ category: cat }});
      renderHomeFeed();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function resetHome(e) {{
      if (e) e.preventDefault();
      activeCategory = 'All';
      activeSearch = '';
      visibleRecentCount = 8;
      const searchInput = document.getElementById('search-input');
      if (searchInput) searchInput.value = '';
      closeArticleView(true);
      renderHomeFeed();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function openArticleView(id, pushUrl = true) {{
      const article = ALL_ARTICLES.find(a => a.id === id);
      if (!article) return;

      document.getElementById('home-view').classList.add('hidden');
      document.getElementById('article-view').classList.remove('hidden');

      document.title = article.seoTitle || `${{article.title}} | Bugwrite`;
      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc && article.metaDescription) metaDesc.setAttribute('content', article.metaDescription);

      document.getElementById('reader-category').textContent = article.category;
      document.getElementById('reader-title').textContent = article.title;
      document.getElementById('reader-dek').textContent = article.dek;
      document.getElementById('reader-author').textContent = article.author;
      document.getElementById('reader-role').textContent = article.authorRole;
      document.getElementById('reader-date').textContent = article.publishedDate;
      document.getElementById('reader-readtime').textContent = article.readTime;
      document.getElementById('reader-image').src = `${{article.image}}?v=bit1`;
      document.getElementById('reader-image').alt = article.imageAlt;
      document.getElementById('reader-caption').textContent = article.imageAlt;
      document.getElementById('reader-body').innerHTML = article.body;
      document.getElementById('reader-avatar').textContent = article.author.split(' ').map(p => p[0]).join('').slice(0, 2).toUpperCase();
      document.getElementById('reader-tags').innerHTML = (article.keywords || []).map(k => `<span class="px-2.5 py-1 text-[11px] font-medium bg-neutral-100 dark:bg-[#1a1e26] text-neutral-700 dark:text-neutral-300 rounded">${{escapeHtml(k)}}</span>`).join('');

      const related = ALL_ARTICLES.filter(a => a.id !== article.id).slice(0, 4);
      document.getElementById('related-grid').innerHTML = related.map(a => renderGridCard(a, 'h3')).join('');

      if (pushUrl) safePushUrl(getArticleUrl(article), {{ articleId: id }});
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function closeArticleView(updateUrl = true) {{
      document.getElementById('article-view').classList.add('hidden');
      document.getElementById('home-view').classList.remove('hidden');
      document.title = '{home_title}';
      if (updateUrl) safePushUrl(activeCategory === 'All' ? '/' : `/${{getCategorySlug(activeCategory)}}`, {{ category: activeCategory }});
    }}

    function syncFromUrl() {{
      const path = window.location.pathname;
      const params = new URLSearchParams(window.location.search);
      const qParam = params.get('q');
      if (qParam) {{
        activeSearch = qParam;
        const si = document.getElementById('search-input');
        if (si) si.value = qParam;
        document.getElementById('search-drawer')?.classList.remove('hidden');
      }} else if (params.get('search') === '1') {{
        document.getElementById('search-drawer')?.classList.remove('hidden');
        document.getElementById('search-input')?.focus();
      }}

      const articleMatch = path.match(/^\\/([^/]+)\\/article\\/([^/]+)\\/?$/);
      if (articleMatch) {{
        const id = decodeURIComponent(articleMatch[2]);
        if (ALL_ARTICLES.some(a => a.id === id)) {{
          openArticleView(id, false);
          return;
        }}
      }}

      const catMatch = path.match(/^\\/([^/]+)\\/?$/);
      if (catMatch) {{
        const matchedCat = getCategoryFromSlug(catMatch[1].toLowerCase());
        if (matchedCat) {{
          activeCategory = matchedCat;
          closeArticleView(false);
          renderHomeFeed();
          return;
        }}
      }}

      const hash = window.location.hash;
      if (hash.startsWith('#article/')) {{
        const id = hash.replace('#article/', '');
        const art = ALL_ARTICLES.find(a => a.id === id);
        if (art) {{
          if (window.location.protocol !== 'file:') history.replaceState({{ articleId: id }}, '', getArticleUrl(art));
          openArticleView(id, false);
          return;
        }}
      }}

      activeCategory = 'All';
      closeArticleView(false);
      renderHomeFeed();
    }}

    window.addEventListener('hashchange', syncFromUrl);
    window.addEventListener('popstate', syncFromUrl);

    const searchDrawer = document.getElementById('search-drawer');
    const searchInput = document.getElementById('search-input');
    document.getElementById('search-toggle-btn').addEventListener('click', () => {{
      searchDrawer.classList.toggle('hidden');
      if (!searchDrawer.classList.contains('hidden')) searchInput.focus();
    }});
    document.getElementById('clear-search-btn').addEventListener('click', () => {{
      searchDrawer.classList.add('hidden');
      if (activeSearch) {{
        activeSearch = '';
        searchInput.value = '';
        renderHomeFeed();
      }}
    }});
    searchInput.addEventListener('input', (e) => {{
      closeArticleView(false);
      activeSearch = e.target.value;
      renderHomeFeed();
    }});

    syncFromUrl();
  </script>
{SHARED_FOOTER_SCRIPT}
</body>
</html>
"""
    full_html = head + "\n" + body
    write_file("index.html", full_html)
    write_file("code.html", full_html)
    print("Generated pre-rendered SEO index.html & code.html")


def generate_article_pages(articles):
    for idx, art in enumerate(articles):
        cat_slug = get_cat_slug(art["category"])
        cat_label = get_cat_label(cat_slug)
        path = get_article_path(art)
        canonical = f"{DOMAIN}{path}"
        iso_date = parse_iso_date(art.get("publishedDate", LASTMOD))
        raw_title = art.get("seoTitle") or f"{art['title']} | Bugwrite"
        clean_base = re.sub(r"\s*\|\s*Bugwrite.*$", "", raw_title).strip()
        max_base_len = 68 - len(" | Bugwrite")
        if len(clean_base) > max_base_len:
            clean_base = clean_base[:max_base_len].rsplit(" ", 1)[0].rstrip(" |")
        title = f"{clean_base} | Bugwrite"
        desc = art.get("metaDescription") or art["dek"]
        og_img = f"{DOMAIN}{art['image']}"
        initials = "".join(p[0] for p in art["author"].split())[:2].upper()
        plain_body = re.sub(r"<[^>]+>", " ", art.get("body", ""))
        word_count = len(plain_body.split())
        keywords_list = art.get("keywords", [])

        # Clean UTC publication timestamp (never in the future; dateModified always >= datePublished)
        pub_dt = get_article_pub_dt(iso_date, idx)
        pub_iso = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        mod_iso = MOD_ISO

        schemas = [
            {
                "@context": "https://schema.org",
                "@type": "NewsArticle",
                "headline": art["title"],
                "description": desc,
                "image": {
                    "@type": "ImageObject",
                    "url": og_img,
                    "width": 1280,
                    "height": 720,
                    "caption": art["imageAlt"]
                },
                "datePublished": pub_iso,
                "dateModified": mod_iso,
                "inLanguage": "en-US",
                "isAccessibleForFree": True,
                "articleSection": cat_label,
                "wordCount": word_count,
                "keywords": keywords_list,
                "author": {
                    "@type": "Person",
                    "name": art["author"],
                    "jobTitle": art.get("authorRole", "Staff Writer"),
                    "url": f"{DOMAIN}/about#newsroom"
                },
                "publisher": PUBLISHER_ORG,
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical}
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2, "name": cat_label, "item": f"{DOMAIN}/{cat_slug}"},
                    {"@type": "ListItem", "position": 3, "name": art["title"], "item": canonical}
                ]
            }
        ]

        # Pick 4 related stories from same desk first, then others
        same_desk = [a for a in articles if a["id"] != art["id"] and get_cat_slug(a["category"]) == cat_slug]
        others = [a for a in articles if a["id"] != art["id"] and get_cat_slug(a["category"]) != cat_slug]
        related = (same_desk + others)[:4]
        related_html = "\n".join(render_static_card(r, "h3", is_spa=False, eager=False) for r in related)
        tags_html = "\n".join(
            f'<span class="px-2.5 py-1 text-[11px] font-medium bg-neutral-100 dark:bg-[#1a1e26] text-neutral-700 dark:text-neutral-300 rounded">{esc(k)}</span>'
            for k in keywords_list
        )

        article_meta_lines = [
            f'  <meta name="author" content="{esc(art["author"])}" />',
            f'  <meta property="article:published_time" content="{pub_iso}" />',
            f'  <meta property="article:modified_time" content="{mod_iso}" />',
            f'  <meta property="article:section" content="{esc(cat_label)}" />',
            f'  <meta property="article:author" content="{esc(art["author"])}" />',
        ]
        for kw in keywords_list[:6]:
            article_meta_lines.append(f'  <meta property="article:tag" content="{esc(kw)}" />')
        if keywords_list:
            article_meta_lines.append(f'  <meta name="news_keywords" content="{esc(", ".join(keywords_list[:5]))}" />')

        head = build_head(
            title,
            desc,
            canonical,
            "article",
            og_img,
            schemas,
            og_image_alt=art["imageAlt"],
            preload_image=f"{art['image']}?v=bit1",
            extra_meta="\n".join(article_meta_lines),
        )
        page = f"""{head}
<body class="bg-white dark:bg-[#0d0f12] text-neutral-900 dark:text-neutral-100 font-sans selection:bg-neutral-200 dark:selection:bg-neutral-700">
{build_announcement_bar(is_spa=False)}
{build_header(active_slug=cat_slug, is_spa=False)}
  <main class="max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
    <article class="max-w-[760px] mx-auto">
      <nav aria-label="Breadcrumb" class="mb-6 flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400">
        <a href="/" class="inline-flex items-center gap-1.5 font-semibold text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"></path></svg>
          Back to Bugwrite
        </a>
        <a href="/{cat_slug}" class="font-bold uppercase tracking-wider text-blue-700 dark:text-blue-400 hover:underline">{esc(art['category'])}</a>
      </nav>

      <h1 class="text-3xl sm:text-4xl lg:text-[40px] font-bold text-neutral-950 dark:text-white leading-[1.15] tracking-[-0.03em] mb-4">{esc(art['title'])}</h1>
      <p class="text-lg sm:text-[19px] text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">{esc(art['dek'])}</p>

      <div class="flex flex-wrap items-center justify-between gap-4 py-4 border-y border-neutral-200 dark:border-neutral-800 mb-7 text-xs text-neutral-500 dark:text-neutral-400">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-full bg-neutral-900 dark:bg-neutral-200 text-white dark:text-neutral-900 font-bold flex items-center justify-center text-xs">{initials}</div>
          <div>
            <div class="text-neutral-900 dark:text-neutral-100 font-semibold text-[13px]">{esc(art['author'])}</div>
            <div class="text-neutral-500 dark:text-neutral-400">{esc(art.get('authorRole', 'Staff Writer'))}</div>
          </div>
        </div>
        <div class="flex items-center gap-2 text-neutral-500 dark:text-neutral-400">
          <time datetime="{iso_date}">{esc(art['publishedDate'])}</time>
          <span>&bull;</span>
          <span>{esc(art['readTime'])}</span>
        </div>
      </div>

      <figure class="mb-8">
        <div class="overflow-hidden rounded-[6px] bg-neutral-100 dark:bg-neutral-800 aspect-[16/9]">
          <img src="{art['image']}?v=bit1" alt="{esc(art['imageAlt'])}" width="1280" height="720" loading="eager" fetchpriority="high" class="w-full h-full object-cover" />
        </div>
        <figcaption class="mt-2.5 text-xs text-neutral-500 dark:text-neutral-400">{esc(art['imageAlt'])}</figcaption>
      </figure>

      <div class="article-prose">
{art['body'].strip()}
      </div>

      <div class="mt-10 pt-6 border-t border-neutral-200 dark:border-neutral-800 flex flex-wrap items-center gap-2">
        {tags_html}
      </div>
    </article>

    <section aria-label="Related stories" class="mt-14 pt-10 border-t border-neutral-200 dark:border-neutral-800">
      <h2 class="text-xs font-bold uppercase tracking-[0.08em] text-neutral-500 dark:text-neutral-400 mb-6">More from Bugwrite</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-5 gap-y-8">
{related_html}
      </div>
    </section>
  </main>
{build_footer()}
{SHARED_FOOTER_SCRIPT}
</body>
</html>
"""
        write_file(os.path.join("public", cat_slug, "article", art["id"], "index.html"), page)
    print(f"Generated {len(articles)} static SEO article pages under public/<category>/article/<slug>/index.html")


def generate_category_pages(articles):
    desks = [
        ("gaming", "Gaming News, GTA 6 Guides & Reviews | Bugwrite", "Latest gaming news, GTA 6 release guides, PlayStation Plus, Xbox Game Pass, PC hardware pricing, and Game Awards 2026 coverage on Bugwrite.", "Gaming News & Launch Coverage"),
        ("big-tech", "Big Tech News, Outages & Software Updates | Bugwrite", "Breaking Big Tech news, Apple, Microsoft, Google, and Amazon outage coverage, OpenAI model releases, Android 17, and iOS 27 updates on Bugwrite.", "Big Tech & Platform Coverage"),
        ("security", "Cybersecurity Alerts, CVEs & Privacy Guides | Bugwrite", "Urgent cybersecurity warnings, FBI advisories, Java4Shell CVE coverage, ransomware defense, and practical privacy guides from Bugwrite.", "Cybersecurity & Privacy Desk"),
        ("business", "AI Business News, Tech Markets & Startups | Bugwrite", "Technology business reporting covering Nvidia earnings, Anthropic IPO updates, chip export rules, venture funding, and AI SaaS economics.", "Business & Tech Markets"),
    ]
    for slug, title, desc, h1_text in desks:
        desk_articles = [a for a in articles if get_cat_slug(a["category"]) == slug]
        canonical = f"{DOMAIN}/{slug}"
        cards_html = "\n".join(render_static_card(a, "h2", is_spa=False, eager=(i < 4)) for i, a in enumerate(desk_articles))
        schemas = [
            {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": h1_text,
                "description": desc,
                "url": canonical,
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(desk_articles),
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": idx + 1,
                            "url": f"{DOMAIN}{get_article_path(a)}",
                            "name": a["title"]
                        }
                        for idx, a in enumerate(desk_articles[:20])
                    ]
                }
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2, "name": get_cat_label(slug), "item": canonical}
                ]
            }
        ]
        head = build_head(
            title,
            desc,
            canonical,
            "website",
            f"{DOMAIN}{desk_articles[0]['image']}",
            schemas,
            og_image_alt=desk_articles[0]["imageAlt"],
            preload_image=f"{desk_articles[0]['image']}?v=bit1",
        )
        page = f"""{head}
<body class="bg-white dark:bg-[#0d0f12] text-neutral-900 dark:text-neutral-100 font-sans">
{build_announcement_bar(is_spa=False)}
{build_header(active_slug=slug, is_spa=False)}
  <main class="max-w-[1240px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="pb-6 mb-8 border-b border-neutral-200 dark:border-neutral-800">
      <p class="text-[11px] font-bold uppercase tracking-[0.09em] text-blue-700 dark:text-blue-400 mb-1.5">Bugwrite Desk</p>
      <h1 class="text-3xl sm:text-4xl font-bold text-neutral-950 dark:text-white tracking-[-0.03em] mb-2">{esc(h1_text)}</h1>
      <p class="text-sm sm:text-base text-neutral-600 dark:text-neutral-400 max-w-2xl">{esc(desc)}</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-5 gap-y-8">
{cards_html}
    </div>
  </main>
{build_footer()}
{SHARED_FOOTER_SCRIPT}
</body>
</html>
"""
        write_file(os.path.join("public", slug, "index.html"), page)
    print("Generated 4 static SEO category hub pages")


def generate_legal_and_error_pages():
    robots_index = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    pages = [
        (
            "public/about/index.html",
            "/about",
            "About Bugwrite | Editorial Standards & Newsroom",
            "Learn about Bugwrite's independent technology, gaming, cybersecurity, and AI business journalism, editorial verification standards, and writers.",
            "About Bugwrite",
            """<p>Bugwrite is an independent digital publication covering technology, video games, cybersecurity, and the business of artificial intelligence. Published daily at www.bugwrite.com, our goal is simple: explain complex technical events clearly, verify every claim against primary sources, and respect the reader's time.</p>
            <h2>Our Editorial Standards</h2>
            <p>Every article on Bugwrite undergoes fact verification before publication. For service outages, we cross-reference official status dashboards and vendor disclosures rather than repeating unverified social media rumors. For cybersecurity reporting, we verify CVE advisories, patch releases, and federal law enforcement bulletins directly. For gaming and hardware coverage, we clearly separate confirmed publisher announcements from industry rumors.</p>
            <h2 id="newsroom">Our Newsroom Desks</h2>
            <p>Bugwrite operates four core desks. Our Gaming desk, led by Samira Patel and Jordan Kim, covers major console and PC launches, patch notes, subscription catalogs, and hardware markets. Our Big Tech and Security desks, led by Elena Rostova, Marcus Vance, and Priya Nair, report on cloud reliability, software vulnerabilities, operating systems, and consumer privacy. Our Business desk, led by David Lindholm, tracks semiconductor markets, AI infrastructure spending, and public offerings.</p>
            <h2>Corrections Policy</h2>
            <p>Accuracy comes first. If you spot a factual error or outdated technical detail in any Bugwrite article, please reach out through our <a href="/contact" class="text-blue-700 dark:text-blue-400 underline">Contact page</a> so our editors can review and update the story promptly.</p>""",
            robots_index,
            [{"@context": "https://schema.org", "@type": "AboutPage", "name": "About Bugwrite", "url": f"{DOMAIN}/about", "publisher": PUBLISHER_ORG}],
        ),
        (
            "public/contact/index.html",
            "/contact",
            "Contact Bugwrite | News Tips, Corrections & Press",
            "Contact the Bugwrite editorial team for breaking news tips, article corrections, press releases, privacy inquiries, or advertising partnerships.",
            "Contact Bugwrite",
            """<p>Have a breaking technology or gaming tip, a press announcement, a factual correction, or a business inquiry? Reach out to the Bugwrite team directly using the contact channels or form below.</p>
            <h2>Direct Newsroom Channels</h2>
            <p>For editorial tips and press releases, email <strong>editorial@bugwrite.com</strong>. For factual corrections or attribution requests, email <strong>corrections@bugwrite.com</strong> with the article URL and supporting documentation. For advertising, sponsorships, and legal inquiries, email <strong>business@bugwrite.com</strong>.</p>
            <h2>Send a Message</h2>
            <form onsubmit="event.preventDefault(); document.getElementById('contact-sent').classList.remove('hidden'); this.reset();" class="mt-4 space-y-4 max-w-xl">
              <div>
                <label for="c-name" class="block text-xs font-semibold text-neutral-700 dark:text-neutral-300 mb-1">Your Name</label>
                <input id="c-name" type="text" required placeholder="Alex Rivera" class="w-full px-3.5 py-2 text-sm rounded-md border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-[#14171c] text-neutral-900 dark:text-neutral-100 focus:outline-none focus:ring-1 focus:ring-black dark:focus:ring-white" />
              </div>
              <div>
                <label for="c-email" class="block text-xs font-semibold text-neutral-700 dark:text-neutral-300 mb-1">Email Address</label>
                <input id="c-email" type="email" required placeholder="you@example.com" class="w-full px-3.5 py-2 text-sm rounded-md border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-[#14171c] text-neutral-900 dark:text-neutral-100 focus:outline-none focus:ring-1 focus:ring-black dark:focus:ring-white" />
              </div>
              <div>
                <label for="c-msg" class="block text-xs font-semibold text-neutral-700 dark:text-neutral-300 mb-1">Message</label>
                <textarea id="c-msg" rows="4" required placeholder="Share your tip, correction, or inquiry..." class="w-full px-3.5 py-2 text-sm rounded-md border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-[#14171c] text-neutral-900 dark:text-neutral-100 focus:outline-none focus:ring-1 focus:ring-black dark:focus:ring-white"></textarea>
              </div>
              <button type="submit" class="px-5 py-2.5 text-xs font-bold uppercase tracking-wider bg-neutral-900 dark:bg-white text-white dark:text-neutral-950 rounded-md hover:opacity-90 transition-opacity cursor-pointer">Send Message</button>
              <p id="contact-sent" class="hidden text-xs font-semibold text-blue-700 dark:text-blue-400">Thank you. Your message has been recorded for our editorial desk.</p>
            </form>""",
            robots_index,
            [{"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Bugwrite", "url": f"{DOMAIN}/contact", "publisher": PUBLISHER_ORG}],
        ),
        (
            "public/privacy-policy/index.html",
            "/privacy-policy",
            "Privacy Policy | Bugwrite",
            "Read Bugwrite's Privacy Policy detailing analytics, advertising cookies including Google AdSense, local browser preferences, and your privacy rights.",
            "Privacy Policy",
            """<p>Effective Date: November 18, 2026. Bugwrite ("we", "our", or "us") respects your privacy. This Privacy Policy explains how information is collected, used, and protected when you visit www.bugwrite.com.</p>
            <h2>Information We Collect</h2>
            <p>Bugwrite can be read freely without creating an account. We store minimal local browser preferences, such as your light or dark display mode selection in your browser's localStorage. When you submit a message via our Contact page, we receive the name, email address, and message details you choose to provide.</p>
            <h2>Analytics and Advertising Cookies</h2>
            <p>We use standard web analytics tools, such as Google Analytics, to understand aggregate readership trends, popular topics, and site performance. Third-party vendors, including Google through Google AdSense, may use cookies to serve ads based on a user's prior visits to bugwrite.com or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visits to this site and other sites on the internet.</p>
            <p>Users may opt out of personalized advertising at any time by visiting Google's Ads Settings page or by visiting aboutads.info to opt out of third-party vendor cookies used for personalized advertising.</p>
            <h2>Your Privacy Rights (GDPR and CCPA)</h2>
            <p>Depending on your location, including residents of the European Economic Area, the United Kingdom, and California, you may have the right to request access to, correction of, or deletion of personal information you have submitted to us, and the right to restrict or object to certain data processing. To exercise these rights, contact privacy@bugwrite.com.</p>
            <h2>Changes to This Policy</h2>
            <p>We may update this Privacy Policy periodically to reflect changes in legal requirements or site operations. Any updates will appear on this page with a revised effective date.</p>""",
            robots_index,
            None,
        ),
        (
            "public/terms-of-service/index.html",
            "/terms-of-service",
            "Terms of Service | Bugwrite",
            "Review the Bugwrite Terms of Service governing editorial content usage, intellectual property, third-party links, and disclaimers on bugwrite.com.",
            "Terms of Service",
            """<p>Effective Date: November 18, 2026. By accessing or using www.bugwrite.com, you agree to be bound by these Terms of Service. If you do not agree with any part of these terms, please discontinue use of the website.</p>
            <h2>Editorial Content and Informational Use</h2>
            <p>All articles, guides, market summaries, and technical explainers published on Bugwrite are provided strictly for general informational and journalistic purposes. Financial and market reporting does not constitute investment advice, and cybersecurity articles do not constitute formal legal or compliance counsel.</p>
            <h2>Intellectual Property</h2>
            <p>Original text, editorial graphics, layout code, and branding published on Bugwrite are owned by Bugwrite Media unless otherwise noted. You may share links to our articles and quote brief excerpts with clear attribution and a link back to www.bugwrite.com. Reproducing full articles or scraping site content for commercial redistribution without written permission is prohibited.</p>
            <h2>External Links and Third-Party Services</h2>
            <p>Articles may reference third-party websites, vendor status dashboards, or official software stores. Bugwrite is not responsible for the content, availability, pricing, or privacy practices of external sites.</p>
            <h2>Limitation of Liability</h2>
            <p>Bugwrite is provided on an "as is" and "as available" basis without warranties of any kind. To the fullest extent permitted by law, Bugwrite Media is not liable for any direct, indirect, or incidental damages arising from your reliance on published content or temporary site unavailability.</p>""",
            robots_index,
            None,
        ),
    ]

    for rel_path, url_path, title, desc, h1_text, body_html, robots, page_schemas in pages:
        canonical = f"{DOMAIN}{url_path}"
        head = build_head(title, desc, canonical, "website", f"{DOMAIN}/blog/articles/gta6-release-time.jpg", page_schemas, robots)
        page = f"""{head}
<body class="bg-white dark:bg-[#0d0f12] text-neutral-900 dark:text-neutral-100 font-sans">
{build_announcement_bar(is_spa=False)}
{build_header(active_slug="", is_spa=False)}
  <main class="max-w-[780px] mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14">
    <h1 class="text-3xl sm:text-4xl font-bold text-neutral-950 dark:text-white tracking-[-0.03em] mb-6">{esc(h1_text)}</h1>
    <div class="article-prose">
      {body_html}
    </div>
  </main>
{build_footer()}
{SHARED_FOOTER_SCRIPT}
</body>
</html>
"""
        write_file(rel_path, page)

    # Custom 404 and 500 error pages
    for code, heading, msg in [
        ("404", "Page Not Found", "The article or page you are looking for may have moved or no longer exists. Browse our latest technology, gaming, security, and business coverage from the homepage."),
        ("500", "Temporary Server Error", "Something went wrong while loading this page. Please refresh in a moment or return to the Bugwrite homepage to continue reading."),
    ]:
        head = build_head(f"{code} {heading} | Bugwrite", msg, f"{DOMAIN}/{code}.html", "website", f"{DOMAIN}/blog/articles/gta6-release-time.jpg", None, "noindex, follow")
        err_page = f"""{head}
<body class="bg-white dark:bg-[#0d0f12] text-neutral-900 dark:text-neutral-100 font-sans">
{build_header(active_slug="", is_spa=False)}
  <main class="max-w-[680px] mx-auto px-4 sm:px-6 py-20 text-center">
    <p class="text-xs font-bold uppercase tracking-[0.12em] text-blue-700 dark:text-blue-400 mb-3">Error {code}</p>
    <h1 class="text-3xl sm:text-5xl font-bold text-neutral-950 dark:text-white tracking-[-0.03em] mb-4">{heading}</h1>
    <p class="text-sm sm:text-base text-neutral-600 dark:text-neutral-400 leading-relaxed mb-8">{msg}</p>
    <div class="flex flex-wrap items-center justify-center gap-3">
      <a href="/" class="px-5 py-2.5 text-xs font-bold uppercase tracking-wider bg-neutral-950 dark:bg-white text-white dark:text-neutral-950 rounded-md hover:opacity-90 transition-opacity">Return Home</a>
      <a href="/gaming" class="px-5 py-2.5 text-xs font-bold uppercase tracking-wider border border-neutral-300 dark:border-neutral-700 text-neutral-800 dark:text-neutral-200 rounded-md hover:border-black dark:hover:border-white transition-colors">Browse Gaming</a>
      <a href="/big-tech" class="px-5 py-2.5 text-xs font-bold uppercase tracking-wider border border-neutral-300 dark:border-neutral-700 text-neutral-800 dark:text-neutral-200 rounded-md hover:border-black dark:hover:border-white transition-colors">Big Tech</a>
    </div>
  </main>
{build_footer()}
{SHARED_FOOTER_SCRIPT}
</body>
</html>
"""
        write_file(f"public/{code}.html", err_page)

    print("Generated 4 AdSense legal/editorial pages + 404.html & 500.html")


def generate_sitemap(articles):
    static_urls = [
        (f"{DOMAIN}/", LASTMOD, "hourly", "1.0", None),
        (f"{DOMAIN}/gaming", LASTMOD, "daily", "0.9", None),
        (f"{DOMAIN}/big-tech", LASTMOD, "daily", "0.9", None),
        (f"{DOMAIN}/security", LASTMOD, "daily", "0.9", None),
        (f"{DOMAIN}/business", LASTMOD, "daily", "0.9", None),
        (f"{DOMAIN}/about", LASTMOD, "monthly", "0.5", None),
        (f"{DOMAIN}/contact", LASTMOD, "monthly", "0.5", None),
        (f"{DOMAIN}/privacy-policy", LASTMOD, "monthly", "0.4", None),
        (f"{DOMAIN}/terms-of-service", LASTMOD, "monthly", "0.4", None),
    ]
    for art in articles:
        static_urls.append((
            f"{DOMAIN}{get_article_path(art)}",
            parse_iso_date(art.get("publishedDate", LASTMOD)),
            "weekly",
            "0.8",
            (f"{DOMAIN}{art['image']}", art["title"], art["imageAlt"]),
        ))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for loc, lm, freq, prio, img_info in static_urls:
        img_xml = ""
        if img_info:
            img_loc, img_title, img_cap = img_info
            img_xml = (
                f"\n    <image:image>\n"
                f"      <image:loc>{esc(img_loc)}</image:loc>\n"
                f"      <image:title>{esc(img_title)}</image:title>\n"
                f"      <image:caption>{esc(img_cap)}</image:caption>\n"
                f"    </image:image>"
            )
        lines.append(
            f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{lm}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>{img_xml}\n  </url>"
        )
    lines.append("</urlset>\n")
    write_file("public/sitemap.xml", "\n".join(lines))
    print(f"Generated public/sitemap.xml with {len(static_urls)} URLs + image sitemap tags")


def generate_news_sitemap(articles):
    # Google News Sitemap: automatically includes articles from the rolling last 48 hours
    today = NOW_UTC.date()
    recent = []
    for idx, art in enumerate(articles):
        iso_date = parse_iso_date(art.get("publishedDate", LASTMOD))
        try:
            art_date = datetime.strptime(iso_date, "%Y-%m-%d").date()
        except Exception:
            art_date = today
        age_days = (today - art_date).days
        if 0 <= age_days <= 2:
            recent.append((idx, art, iso_date))

    # Fallback so news-sitemap.xml is never empty even if no new story was published in the last 48h
    if not recent:
        recent = [(idx, art, parse_iso_date(art.get("publishedDate", LASTMOD))) for idx, art in enumerate(articles[:10])]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">',
    ]
    for idx, art, iso_date in recent:
        pub_iso = get_article_pub_dt(iso_date, idx).strftime("%Y-%m-%dT%H:%M:%SZ")
        loc = f"{DOMAIN}{get_article_path(art)}"
        kws = ", ".join(art.get("keywords", [])[:5])
        kw_xml = f"\n      <news:keywords>{esc(kws)}</news:keywords>" if kws else ""
        lines.append(
            f"  <url>\n"
            f"    <loc>{esc(loc)}</loc>\n"
            f"    <news:news>\n"
            f"      <news:publication>\n"
            f"        <news:name>Bugwrite</news:name>\n"
            f"        <news:language>en</news:language>\n"
            f"      </news:publication>\n"
            f"      <news:publication_date>{pub_iso}</news:publication_date>\n"
            f"      <news:title>{esc(art['title'])}</news:title>{kw_xml}\n"
            f"    </news:news>\n"
            f"  </url>"
        )
    lines.append("</urlset>\n")
    write_file("public/news-sitemap.xml", "\n".join(lines))
    print(f"Generated public/news-sitemap.xml with {len(recent)} recent news URLs (window ending {LASTMOD})")


def generate_rss_feed(articles):
    build_rfc = format_datetime(NOW_UTC, usegmt=True)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">',
        '  <channel>',
        '    <title>Bugwrite: Tech, Gaming, Cybersecurity &amp; Business News</title>',
        f'    <link>{DOMAIN}/</link>',
        f'    <atom:link href="{DOMAIN}/rss.xml" rel="self" type="application/rss+xml" />',
        '    <description>Independent technology, gaming, cybersecurity, and AI business journalism from Bugwrite.</description>',
        '    <language>en-us</language>',
        f'    <lastBuildDate>{build_rfc}</lastBuildDate>',
        '    <image>',
        f'      <url>{DOMAIN}/blog/bugwrite-logo.png</url>',
        '      <title>Bugwrite</title>',
        f'      <link>{DOMAIN}/</link>',
        '    </image>',
    ]
    for idx, art in enumerate(articles[:50]):
        loc = f"{DOMAIN}{get_article_path(art)}"
        img_url = f"{DOMAIN}{art['image']}"
        iso_date = parse_iso_date(art.get("publishedDate", LASTMOD))
        rfc_date = format_datetime(get_article_pub_dt(iso_date, idx), usegmt=True)
        lines.append(
            f"    <item>\n"
            f"      <title>{esc(art['title'])}</title>\n"
            f"      <link>{esc(loc)}</link>\n"
            f"      <guid isPermaLink=\"true\">{esc(loc)}</guid>\n"
            f"      <pubDate>{rfc_date}</pubDate>\n"
            f"      <category>{esc(art['category'])}</category>\n"
            f"      <description>{esc(art.get('metaDescription') or art['dek'])}</description>\n"
            f"      <media:content url=\"{esc(img_url)}\" medium=\"image\" width=\"1280\" height=\"720\" />\n"
            f"    </item>"
        )
    lines.append('  </channel>')
    lines.append('</rss>\n')
    write_file("public/rss.xml", "\n".join(lines))
    print("Generated public/rss.xml with 50 latest stories")


def main():
    articles = load_articles()
    generate_homepage(articles)
    generate_article_pages(articles)
    generate_category_pages(articles)
    generate_legal_and_error_pages()
    generate_sitemap(articles)
    generate_news_sitemap(articles)
    generate_rss_feed(articles)


if __name__ == "__main__":
    main()
