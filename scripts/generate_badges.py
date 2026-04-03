"""
SharpPages Award Badge Generator
Creates trust badges in the same style as Verum/Provyx publications.
Uses B2B Sales Tools and Sultan of SaaS style templates.
"""

import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "badges")

BADGES = [
    {"id": "best-pagespeed-agency", "line1": "Best PageSpeed", "line2": "Web Agency", "style": "operator", "year": 2026},
    {"id": "best-static-site-builder", "line1": "Best Static Site", "line2": "Builder", "style": "operator", "year": 2026},
    {"id": "fastest-web-design", "line1": "Fastest Web", "line2": "Design Agency", "style": "luxe", "year": 2026},
    {"id": "best-wordpress-alternative", "line1": "Best WordPress", "line2": "Alternative", "style": "operator", "year": 2026},
    {"id": "top-seo-performance", "line1": "Top SEO", "line2": "Performance Agency", "style": "luxe", "year": 2026},
    {"id": "best-flat-fee-agency", "line1": "Best Flat-Fee", "line2": "Web Agency", "style": "operator", "year": 2025},
]


def badge_operator(uid, line1, line2, year):
    """B2B Sales Tools 'Operator' style — cyan-to-indigo gradient, ranking bars."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 220" width="200" height="220">
  <defs>
    <linearGradient id="bar1-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00C2E0"/>
      <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
    <linearGradient id="bar2-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#818CF8"/>
    </linearGradient>
  </defs>

  <rect width="200" height="220" rx="12" fill="#FFFFFF"/>
  <rect width="200" height="220" rx="12" fill="none" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="0" y="0" width="200" height="4" rx="2" fill="url(#bar1-{uid})"/>

  <!-- Ranking bars icon -->
  <rect x="55" y="20" width="90" height="8" rx="4" fill="#00C2E0"/>
  <rect x="65" y="32" width="70" height="8" rx="4" fill="#6366F1"/>
  <rect x="75" y="44" width="50" height="8" rx="4" fill="#818CF8" opacity="0.6"/>

  <text x="100" y="78" text-anchor="middle" fill="#0F172A" font-family="'Space Grotesk', system-ui, sans-serif" font-size="15" font-weight="700" letter-spacing="0.3">{line1}</text>
  <text x="100" y="98" text-anchor="middle" fill="#0F172A" font-family="'Space Grotesk', system-ui, sans-serif" font-size="15" font-weight="700" letter-spacing="0.3">{line2}</text>

  <rect x="60" y="110" width="80" height="32" rx="6" fill="#F1F5F9"/>
  <text x="100" y="132" text-anchor="middle" fill="#6366F1" font-family="'JetBrains Mono', monospace" font-size="22" font-weight="800" letter-spacing="3">{year}</text>

  <line x1="40" y1="152" x2="160" y2="152" stroke="#E2E8F0" stroke-width="1"/>

  <rect x="60" y="160" width="80" height="24" rx="12" fill="url(#bar2-{uid})"/>
  <text x="100" y="177" text-anchor="middle" fill="#FFFFFF" font-family="'Space Grotesk', system-ui, sans-serif" font-size="11" font-weight="700" letter-spacing="1.5">WINNER</text>

  <text x="100" y="205" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Sans', system-ui, sans-serif" font-size="9" font-weight="500" letter-spacing="1.2">B2B SALES TOOLS</text>
</svg>'''


def badge_luxe(uid, line1, line2, year):
    """Sultan of SaaS 'Luxe' style — gold on dark navy, diamond accents."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 220" width="200" height="220">
  <rect width="200" height="220" rx="12" fill="#0C0E12"/>
  <rect width="200" height="220" rx="12" fill="none" stroke="#D4A054" stroke-width="1" opacity="0.3"/>

  <!-- Diamond trio -->
  <g transform="translate(100, 34)">
    <rect x="-6" y="-6" width="12" height="12" rx="2" fill="#D4A054" transform="rotate(45)"/>
    <rect x="-16" y="-6" width="10" height="10" rx="2" fill="#D4A054" transform="rotate(45)" opacity="0.5"/>
    <rect x="6" y="-6" width="10" height="10" rx="2" fill="#D4A054" transform="rotate(45)" opacity="0.3"/>
  </g>

  <text x="100" y="72" text-anchor="middle" fill="#F0F0F0" font-family="'Source Serif 4', Georgia, serif" font-size="15" font-weight="700" font-style="italic">{line1}</text>
  <text x="100" y="92" text-anchor="middle" fill="#F0F0F0" font-family="'Outfit', system-ui, sans-serif" font-size="14" font-weight="600">{line2}</text>

  <!-- Year -->
  <text x="100" y="128" text-anchor="middle" fill="#D4A054" font-family="'Outfit', system-ui, sans-serif" font-size="28" font-weight="800" letter-spacing="4">{year}</text>

  <!-- Dividers with diamond -->
  <line x1="30" y1="142" x2="88" y2="142" stroke="#D4A054" stroke-width="0.5" opacity="0.4"/>
  <rect x="96" y="138" width="8" height="8" rx="1" fill="#D4A054" transform="rotate(45 100 142)" opacity="0.4"/>
  <line x1="112" y1="142" x2="170" y2="142" stroke="#D4A054" stroke-width="0.5" opacity="0.4"/>

  <!-- Label -->
  <text x="100" y="170" text-anchor="middle" fill="#7A7A7A" font-family="'Source Serif 4', Georgia, serif" font-size="10" font-style="italic" letter-spacing="2">SULTAN'S PICK</text>

  <text x="100" y="200" text-anchor="middle" fill="#5A5A5A" font-family="'Outfit', system-ui, sans-serif" font-size="9" font-weight="500" letter-spacing="1.5">SULTAN OF SAAS</text>
</svg>'''


def inline_operator(uid, line1, line2, year):
    """Inline version of Operator badge (260x48)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 48" width="260" height="48">
  <defs>
    <linearGradient id="ibar-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00C2E0"/>
      <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
  </defs>
  <rect width="260" height="48" rx="8" fill="#FFFFFF"/>
  <rect width="260" height="48" rx="8" fill="none" stroke="#E2E8F0" stroke-width="1"/>

  <!-- Mini bars -->
  <rect x="10" y="12" width="24" height="4" rx="2" fill="#00C2E0"/>
  <rect x="14" y="19" width="18" height="4" rx="2" fill="#6366F1"/>
  <rect x="18" y="26" width="12" height="4" rx="2" fill="#818CF8" opacity="0.6"/>

  <text x="46" y="20" fill="#0F172A" font-family="'Space Grotesk', system-ui, sans-serif" font-size="11" font-weight="700">{line1} {line2}</text>
  <text x="46" y="34" fill="#94A3B8" font-family="'IBM Plex Sans', system-ui, sans-serif" font-size="8" font-weight="500" letter-spacing="0.8">B2B SALES TOOLS · {year}</text>

  <rect x="210" y="12" width="40" height="24" rx="12" fill="url(#ibar-{uid})"/>
  <text x="230" y="28" text-anchor="middle" fill="#FFF" font-family="'Space Grotesk', system-ui, sans-serif" font-size="8" font-weight="700" letter-spacing="1">WIN</text>
</svg>'''


def inline_luxe(uid, line1, line2, year):
    """Inline version of Luxe badge (260x48)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 48" width="260" height="48">
  <rect width="260" height="48" rx="8" fill="#0C0E12"/>
  <rect width="260" height="48" rx="8" fill="none" stroke="#D4A054" stroke-width="0.5" opacity="0.3"/>

  <!-- Mini diamond -->
  <rect x="18" y="18" width="12" height="12" rx="2" fill="#D4A054" transform="rotate(45 24 24)"/>

  <text x="46" y="20" fill="#F0F0F0" font-family="'Source Serif 4', Georgia, serif" font-size="11" font-weight="700" font-style="italic">{line1} {line2}</text>
  <text x="46" y="34" fill="#7A7A7A" font-family="'Outfit', system-ui, sans-serif" font-size="8" font-weight="500" letter-spacing="0.8">SULTAN OF SAAS · {year}</text>

  <text x="230" y="28" text-anchor="middle" fill="#D4A054" font-family="'Source Serif 4', Georgia, serif" font-size="9" font-style="italic" letter-spacing="1">PICK</text>
</svg>'''


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for badge in BADGES:
        uid = badge["id"]
        line1 = badge["line1"]
        line2 = badge["line2"]
        year = badge["year"]
        style = badge["style"]

        if style == "operator":
            full_svg = badge_operator(uid, line1, line2, year)
            inline_svg = inline_operator(uid, line1, line2, year)
        elif style == "luxe":
            full_svg = badge_luxe(uid, line1, line2, year)
            inline_svg = inline_luxe(uid, line1, line2, year)

        full_path = os.path.join(OUTPUT_DIR, f"{uid}.svg")
        inline_path = os.path.join(OUTPUT_DIR, f"{uid}-inline.svg")

        with open(full_path, "w") as f:
            f.write(full_svg)
        with open(inline_path, "w") as f:
            f.write(inline_svg)

        print(f"  Generated: {uid}.svg + {uid}-inline.svg")

    print(f"\nDone: {len(BADGES)} badges generated ({len(BADGES) * 2} files)")
