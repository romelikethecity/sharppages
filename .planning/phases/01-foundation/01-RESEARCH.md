# Phase 1: Foundation - Research

**Researched:** 2026-03-19
**Domain:** Static site build system (Python), dark-theme CSS, SEO templating
**Confidence:** HIGH

## Summary

Phase 1 creates the build system skeleton for sharppages.com by replicating the proven Provyx website architecture. This is a known pattern -- the Provyx codebase at `/Users/rome/Documents/projects/provyx-website/` provides the exact blueprint. The three-file architecture (build.py, nav_config.py, templates.py) is battle-tested across Provyx (355 pages), SultanOfSaaS (334 pages), and B2BSalesTools (196 pages).

The key difference from Provyx is the dark theme (Midnight #06090E background vs Provyx's white #FFFFFF) and Google Fonts (Instrument Sans + DM Sans loaded from fonts.googleapis.com vs Provyx's self-hosted Plus Jakarta Sans). Brand assets are complete and ready at `/Users/rome/Downloads/sharppages-brand/` including tokens.css with all CSS custom properties, SVG logos, favicons, OG images, and site.webmanifest.

**Primary recommendation:** Clone the Provyx three-file pattern exactly, adapt for SharpPages brand tokens and dark theme, generate a placeholder page that proves the full pipeline works (build, SEO meta, schema, fonts, Lighthouse scores).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INFR-01 | Python build system generates all pages via `python3 scripts/build.py` | Provyx build.py pattern: main() calls page generators, tracks ALL_PAGES for sitemap |
| INFR-02 | nav_config.py is single source of truth for nav links, site info, footer columns | Provyx nav_config.py exports: SITE_NAME, SITE_URL, SITE_TAGLINE, COPYRIGHT_YEAR, CTA_HREF, CTA_LABEL, NAV_ITEMS, FOOTER_COLUMNS |
| INFR-03 | templates.py provides shared HTML generators | Provyx templates.py functions documented below in Architecture Patterns |
| INFR-04 | Brand assets copied into project | Brand kit at /Users/rome/Downloads/sharppages-brand/ -- tokens.css, logos/, favicons/, og/, site.webmanifest |
| INFR-05 | Single CSS file with BEM naming, cache busting via ?v=N | Provyx pattern: CSS_VERSION constant in templates.py, referenced as `/css/styles.css?v={CSS_VERSION}` |
| INFR-06 | CNAME file for sharppages.com | Static file at project root, content: `sharppages.com` |
| INFR-07 | Sitemap.xml auto-generated with correct priorities | Provyx build_sitemap() reads ALL_PAGES list of (path, priority, changefreq) tuples |
| INFR-08 | robots.txt with AI crawler allowances | Provyx robots.txt pattern: Allow all + named AI bot allowances + block CCBot |
| INFR-09 | Minimal JS for mobile nav toggle, FAQ accordion, form validation | Nav toggle inline in templates.py get_nav_html(); FAQ uses native `<details>`; main.js for scroll/form/GA4 |
| INFR-10 | GA4 tracking placeholder in every page head | Provyx get_html_head() includes GA4 script with consent mode -- use placeholder ID |
| SEO-01 | Every page has unique title (50-60 chars), keyword-first | get_html_head() title param, appended with ` \| {SITE_NAME}` |
| SEO-02 | Every page has unique meta description (150-158 chars) | get_html_head() description param |
| SEO-03 | Every page has canonical URL | get_html_head() builds canonical from BASE_URL + canonical_path |
| SEO-04 | OG tags on every page | get_html_head() generates og:type, og:url, og:title, og:description, og:site_name, og:image |
| SEO-05 | Twitter Card on every page | get_html_head() generates twitter:card, twitter:title, twitter:description, twitter:image |
| SEO-07 | All inner pages: BreadcrumbList schema | get_breadcrumb_schema() generates JSON-LD from breadcrumb list |
| QUAL-04 | CURRENT_YEAR variable for year references | COPYRIGHT_YEAR in nav_config.py, used in footer |
| PERF-01 | Lighthouse Performance 90+ | Dark theme CSS from tokens.css, Google Fonts with preconnect + display=swap, minimal JS |
| PERF-02 | Lighthouse Accessibility 90+ | Skip-to-content link, ARIA labels, semantic HTML, proper contrast on dark bg |
| PERF-03 | Lighthouse SEO 100 | Complete meta tags, canonical, OG, robots meta |
| PERF-05 | Google Fonts preconnect + display=swap | head-snippet.html has the exact preconnect + font link with display=swap |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3 | 3.10+ | Build system | No dependencies needed. Provyx pattern uses only stdlib (os, sys, json, datetime) |
| Google Fonts | CDN | Instrument Sans + DM Sans | Brand-specified fonts. Loaded via fonts.googleapis.com with display=swap |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| rcssmin | latest | CSS minification | Optional post-build step. Provyx uses it but gracefully skips if not installed |
| Formspree | n/a | Contact form backend | Phase 2 (contact page). Placeholder in INFR-09 form validation JS |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Google Fonts CDN | Self-hosted fonts | Provyx self-hosts Plus Jakarta Sans. SharpPages brand kit specifies Google Fonts CDN. Stick with CDN per brand kit -- simpler, no font files to manage |
| rcssmin | No minification | Acceptable for v1. CSS will be small. Add later if needed |

**Installation:**
```bash
# No pip install needed for core build. Pure stdlib Python.
# Optional: pip install rcssmin (for CSS minification)
```

## Architecture Patterns

### Recommended Project Structure
```
sharppages/
├── scripts/
│   ├── build.py          # Master build: all data inline, all page generators, sitemap, main()
│   ├── nav_config.py     # SITE_NAME, SITE_URL, NAV_ITEMS, FOOTER_COLUMNS, CTA
│   └── templates.py      # get_html_head, get_nav_html, get_footer_html, get_breadcrumb_html/schema,
│                          # generate_faq_html, generate_cta_section, get_page_wrapper, write_page
├── css/
│   └── styles.css        # Single CSS file, BEM naming, uses tokens.css custom properties
├── js/
│   └── main.js           # Smooth scroll, header shadow, form handling, GA4 events
├── assets/
│   ├── logos/             # 6 SVG variants (full dark/light, icon dark/light, wordmark dark/light)
│   ├── favicons/          # favicon.svg, favicon-32.png, favicon-16.png, apple-touch-icon, PWA icons
│   └── og/               # og-default.png (1200x630)
├── tokens.css            # CSS custom properties (from brand kit, at root for @import)
├── site.webmanifest      # PWA manifest
├── CNAME                 # sharppages.com
├── robots.txt            # Generated by build or static file
└── output/               # NOT used -- Provyx builds in-place, not to output dir
```

**IMPORTANT: Provyx builds in-place, NOT to an output/ directory.** The write_page() function writes relative to PROJECT_ROOT (one level up from scripts/). Files like `about/index.html` are written directly into the project root. The success criteria says "output/ directory" but the Provyx pattern writes in-place. The planner should decide: follow Provyx pattern exactly (in-place) or add an OUTPUT_DIR constant to write_page(). Recommendation: Add OUTPUT_DIR = "output" to keep generated HTML separate from source, which is cleaner for .gitignore and deployment.

### Pattern 1: The Three-File Build System

**What:** All site generation happens through three Python files with clear responsibilities.

**nav_config.py exports:**
```python
SITE_NAME = "SharpPages"
SITE_URL = "https://sharppages.com"
SITE_TAGLINE = "Sharp pages. Full rooms."
COPYRIGHT_YEAR = "2026"
CTA_HREF = "/contact/"
CTA_LABEL = "Get Started"  # or call-to-value per HOME-05
NAV_ITEMS = [...]   # List of dicts with href, label, optional children
FOOTER_COLUMNS = {...}  # OrderedDict of heading -> list of link dicts
```

**templates.py function signatures (from Provyx, adapt for SharpPages):**
```python
# Constants
BASE_URL = "https://sharppages.com"
CSS_VERSION = "1"

# Head
def get_html_head(title, description, canonical_path, extra_schema="",
                  noindex=False, og_type="website") -> str:
    """Returns <!DOCTYPE html><html><head>...</head>"""

# Navigation
def get_nav_html(active_page=None) -> str:
    """Returns <body> + skip link + <header> + mobile nav + inline JS toggle + <main>"""

# Footer
def get_footer_html() -> str:
    """Returns </main> + <footer> + consent banner + main.js script + </body></html>"""

# Breadcrumbs
def get_breadcrumb_schema(breadcrumbs) -> str:  # JSON-LD script tag
def get_breadcrumb_html(breadcrumbs) -> str:     # Visible nav HTML

# FAQ
def generate_faq_html(faqs, heading="Frequently Asked Questions") -> str:
    """Uses <details>/<summary> for accordion. Includes FAQPage JSON-LD schema."""

# CTA
def generate_cta_section(title, text, button_text=None, button_href=None,
                         include_form=False, formspree_id="") -> str:

# Page assembly
def get_page_wrapper(title, description, canonical_path, body_content,
                     active_page=None, extra_schema="", noindex=False,
                     og_type="website") -> str:
    """Combines get_html_head + get_nav_html + body_content + get_footer_html"""

# File writer
def write_page(path, html) -> None:
    """Creates dirs, writes HTML to PROJECT_ROOT/path"""
```

**build.py pattern:**
```python
ALL_PAGES = []  # Track (path, priority, changefreq) for sitemap

def build_some_page():
    breadcrumbs = [{"name": "Home", "url": f"{BASE_URL}/"}, ...]
    extra_schema = get_breadcrumb_schema(breadcrumbs)
    body = f'''...{get_breadcrumb_html(breadcrumbs)}...'''
    html = get_page_wrapper(
        title="Page Title",
        description="Meta description here.",
        canonical_path="/page-slug/",
        body_content=body,
        active_page="/parent/",
        extra_schema=extra_schema,
    )
    write_page("page-slug/index.html", html)
    ALL_PAGES.append(("/page-slug/", 0.8, "monthly"))

def build_sitemap():
    # Iterates ALL_PAGES, writes sitemap.xml

def main():
    build_homepage()
    build_about()
    # ... all pages ...
    build_sitemap()
    print(f"Build complete: {len(ALL_PAGES)} pages generated")
```

### Pattern 2: Dark Theme Adaptation

**What:** Provyx is light theme (white bg, navy text). SharpPages is dark theme (Midnight bg, light text).

**Key differences from Provyx CSS:**
- Body background: `var(--color-bg)` (#06090E) instead of #FFFFFF
- Text color: `var(--color-text)` (#E4E8ED) instead of navy
- Card backgrounds: `var(--color-card)` (#111820) instead of white
- Borders: `var(--color-border)` (#1E2A38) instead of #E2E8F0
- Header: `rgba(6, 9, 14, 0.95)` with backdrop-blur instead of white
- Footer: `var(--color-surface)` (#0C1118) instead of navy
- CTA sections: Use `var(--color-surface)` background with cyan accent elements
- Buttons: Primary cyan (#00C2E0) on dark, Gold (#E8B931) for accents sparingly

**tokens.css is the source of truth.** The brand kit provides complete CSS custom properties. The styles.css file should `@import` tokens.css and reference variables throughout. Never hardcode color values.

### Pattern 3: Google Fonts with Performance

**What:** Load Instrument Sans + DM Sans from Google Fonts CDN with optimal performance.

**From head-snippet.html (verified):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
```

This covers PERF-05 (preconnect + display=swap). The preconnect hints go before the stylesheet link.

### Pattern 4: GA4 Placeholder with Consent Mode

**What:** Include GA4 tracking code with a placeholder measurement ID.

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    'ad_storage': 'denied',
    'analytics_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied'
  });
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PLACEHOLDER"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-PLACEHOLDER');
</script>
```

Use `G-PLACEHOLDER` as the measurement ID. Replace with real GA4 ID before launch (noted as v2 requirement V2-01).

### Anti-Patterns to Avoid
- **Building to a separate output/ dir without updating write_page():** If using OUTPUT_DIR, must update write_page() to use it. Provyx writes in-place.
- **Importing tokens.css via HTML link AND @import in styles.css:** Pick one approach. Recommendation: `@import 'tokens.css'` at top of styles.css, or inline the tokens into styles.css. Do NOT load tokens.css as a separate HTTP request.
- **Hardcoding colors instead of using CSS variables:** All colors must come from tokens.css custom properties.
- **Missing the skip-to-content link:** Provyx includes `<a href="#main-content" class="sr-only sr-only--focusable">Skip to main content</a>` before the header. Required for PERF-02 accessibility.
- **Forgetting display=swap on Google Fonts:** Already in the brand kit URL. Do not modify the font URL.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| FAQ accordion | Custom JS accordion | `<details>/<summary>` HTML | Native browser support, zero JS, accessible by default. Provyx uses this pattern. |
| Mobile nav toggle | Complex hamburger menu system | Inline JS in get_nav_html() | 30 lines of vanilla JS, baked into every page at build time. Provyx pattern works. |
| Form validation | Custom validation library | HTML5 `required` + `type="email"` | Browser-native validation covers INFR-09. Formspree handles server-side. |
| CSS reset | Custom reset stylesheet | Minimal reset in tokens.css | tokens.css already includes box-sizing reset and base element styles |
| Consent banner | Cookie consent library | 20 lines inline JS | Provyx pattern: localStorage check, show/hide banner, update gtag consent |
| Sitemap generation | External sitemap library | ALL_PAGES list + string formatting | Under 30 lines of Python. No library needed. |

## Common Pitfalls

### Pitfall 1: Contrast Ratio Failures on Dark Theme
**What goes wrong:** Text/element colors that work on light backgrounds fail WCAG contrast on dark backgrounds. Lighthouse Accessibility drops below 90.
**Why it happens:** Copying Provyx CSS patterns without adjusting for dark backgrounds.
**How to avoid:** Use the exact token values from tokens.css. Primary text (#E4E8ED) on Midnight (#06090E) = 13.9:1 ratio (excellent). Muted text (#7A8899) on Midnight = 5.2:1 (passes AA). Do NOT use --color-text-subtle (#3A4A5C) for any readable text -- it's 2.3:1 (fails).
**Warning signs:** Lighthouse accessibility score below 90, text appears washed out.

### Pitfall 2: Google Fonts Blocking Render
**What goes wrong:** Fonts block page rendering, causing poor LCP and Lighthouse Performance below 90.
**Why it happens:** Missing preconnect hints or missing display=swap.
**How to avoid:** Use the exact head-snippet.html pattern: preconnect to fonts.googleapis.com AND fonts.gstatic.com (with crossorigin), then the font CSS link with display=swap in the URL.
**Warning signs:** Flash of invisible text (FOIT), LCP above 2.5s.

### Pitfall 3: Missing Trailing Slashes on Canonical URLs
**What goes wrong:** Canonical URLs without trailing slashes cause duplicate content issues. Google sees `/about` and `/about/` as different pages.
**Why it happens:** Forgetting to enforce trailing slash convention.
**How to avoid:** All canonical_path arguments must end with `/`. The Provyx pattern always uses trailing slashes: `/about/`, `/pricing/`, `/for/medical-device-companies/`.
**Warning signs:** Google Search Console showing duplicate URLs.

### Pitfall 4: Sitemap Priority Values Wrong
**What goes wrong:** All pages get the same priority, or priorities don't match INFR-07 spec.
**Why it happens:** Not reading the requirement carefully.
**How to avoid:** Use the exact spec: homepage 1.0, services 0.9, /for/ pages 0.8, blog 0.7, static (privacy/terms) 0.5. Pass these as the second element of the ALL_PAGES tuple.
**Warning signs:** Sitemap.xml has uniform 0.5 priorities.

### Pitfall 5: Inline JS in Templates Uses Wrong Escape Syntax
**What goes wrong:** Python f-string braces conflict with JavaScript braces, causing syntax errors.
**Why it happens:** JavaScript `{}` inside Python f-strings.
**How to avoid:** Double all JS braces: `{{` and `}}` in f-strings. Provyx does this throughout templates.py (see lines 143-164 for GA4 consent, lines 265-293 for nav toggle).
**Warning signs:** Python syntax errors or malformed JS in generated HTML.

## Code Examples

### Verified: Provyx write_page with Output Directory Adaptation
```python
# Source: Provyx templates.py write_page(), adapted for output dir
OUTPUT_DIR = "output"

def write_page(path, html):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, OUTPUT_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)
    print(f"  Generated: /{path}")
```

### Verified: SharpPages get_html_head (adapted from Provyx)
```python
# Key differences from Provyx:
# 1. Google Fonts CDN instead of self-hosted
# 2. theme-color is #06090E (Midnight) not #1B2A4A
# 3. GA4 placeholder ID instead of real ID
# 4. Preconnect to fonts.googleapis.com + fonts.gstatic.com
# 5. No font preload (CDN handles this)
# 6. OG image path: /assets/og/og-default.png (matching brand kit structure)

def get_html_head(title, description, canonical_path, extra_schema="",
                  noindex=False, og_type="website"):
    canonical = f"{BASE_URL}{canonical_path}"
    full_title = f"{title} | {SITE_NAME}" if title != SITE_NAME else title
    # ... same pattern as Provyx but with:
    # <meta name="theme-color" content="#06090E">
    # <link rel="preconnect" href="https://fonts.googleapis.com">
    # <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    # <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
```

### Verified: robots.txt for SharpPages
```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: CCBot
Disallow: /

Sitemap: https://sharppages.com/sitemap.xml
```

### Verified: SharpPages nav_config.py Structure
```python
SITE_NAME = "SharpPages"
SITE_URL = "https://sharppages.com"
SITE_TAGLINE = "Sharp pages. Full rooms."
COPYRIGHT_YEAR = "2026"
CTA_HREF = "/contact/"
CTA_LABEL = "Book a Call"  # call-to-value, not "Get Started"

NAV_ITEMS = [
    {"href": "/services/", "label": "Services"},
    {"href": "/pricing/", "label": "Pricing"},
    {"href": "/work/", "label": "Work"},
    {"href": "/about/", "label": "About"},
    {"href": "/blog/", "label": "Blog"},
]

FOOTER_COLUMNS = {
    "Services": [
        {"href": "/services/", "label": "All Services"},
        {"href": "/pricing/", "label": "Pricing"},
        {"href": "/work/", "label": "Our Work"},
        {"href": "/contact/", "label": "Contact"},
    ],
    "Industries": [
        {"href": "/for/medical-device-companies/", "label": "Medical Devices"},
        {"href": "/for/pharma-field-marketing/", "label": "Pharma"},
        {"href": "/for/b2b-saas/", "label": "B2B SaaS"},
        {"href": "/for/conference-organizers/", "label": "Conferences"},
        {"href": "/for/med-spas/", "label": "Med Spas"},
        {"href": "/for/real-estate/", "label": "Real Estate"},
    ],
    "Resources": [
        {"href": "/blog/", "label": "Blog"},
        {"href": "/about/", "label": "About"},
    ],
    "Legal": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| GA4 without consent mode | GA4 Consent Mode v2 | 2024 | Required for EU/privacy compliance. Provyx already implements this. |
| Self-hosted fonts | Google Fonts CDN with preconnect | Ongoing | SharpPages brand kit specifies CDN. display=swap prevents FOIT. |
| Custom accordion JS | Native `<details>/<summary>` | 2020+ | Zero JS, accessible, supported in all modern browsers. |

## Open Questions

1. **Output directory vs in-place build**
   - What we know: Provyx writes files in-place to project root. Success criteria mentions "output/ directory."
   - What's unclear: Whether to follow Provyx pattern (in-place) or adapt for output/ dir.
   - Recommendation: Use OUTPUT_DIR = "output" for cleaner separation. Add "output/" to .gitignore. Modify write_page() to prepend OUTPUT_DIR. This matches the success criteria wording.

2. **CTA label text**
   - What we know: HOME-05 requires "call-to-value (not 'Get Started')". Provyx uses "Get Provider Data."
   - What's unclear: Exact CTA text for SharpPages.
   - Recommendation: Use "Book a Call" or "Get Your Event Site" -- planner decides. This is a Phase 2 content decision but nav_config.py needs a placeholder.

3. **Consent banner needed for Phase 1?**
   - What we know: Provyx has a consent banner for GA4. SharpPages GA4 is placeholder only in Phase 1.
   - What's unclear: Whether to include consent banner now or defer.
   - Recommendation: Include it now with the placeholder GA4 ID. It's part of the template and costs nothing extra. Easier than retrofitting later.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Bash scripts + Lighthouse CLI |
| Config file | none -- Wave 0 |
| Quick run command | `python3 scripts/build.py && echo "Build OK"` |
| Full suite command | `python3 scripts/build.py && npx lighthouse http://localhost:8000/ --output=json --quiet` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INFR-01 | build.py produces valid HTML | smoke | `python3 scripts/build.py` | No -- Wave 0 |
| INFR-02 | nav_config.py exports all constants | unit | `python3 -c "from scripts.nav_config import *; print(SITE_NAME)"` | No -- Wave 0 |
| INFR-03 | templates.py functions return HTML | unit | `python3 -c "from scripts.templates import get_page_wrapper; print('OK')"` | No -- Wave 0 |
| INFR-04 | Brand assets present | smoke | `test -f assets/logos/logo-full-dark.svg && echo OK` | No -- Wave 0 |
| INFR-05 | CSS has version param | smoke | `grep 'styles.css?v=' output/index.html` | No -- Wave 0 |
| INFR-06 | CNAME exists | smoke | `test -f output/CNAME && cat output/CNAME` | No -- Wave 0 |
| INFR-07 | Sitemap generated | smoke | `test -f output/sitemap.xml && grep 'sharppages.com' output/sitemap.xml` | No -- Wave 0 |
| INFR-08 | robots.txt correct | smoke | `grep 'GPTBot' output/robots.txt && grep 'ClaudeBot' output/robots.txt` | No -- Wave 0 |
| INFR-09 | JS files present | smoke | `test -f output/js/main.js` | No -- Wave 0 |
| INFR-10 | GA4 placeholder in HTML | smoke | `grep 'G-PLACEHOLDER' output/index.html` | No -- Wave 0 |
| SEO-01 | Unique title tag | smoke | `grep '<title>' output/index.html` | No -- Wave 0 |
| SEO-02 | Meta description | smoke | `grep 'meta name="description"' output/index.html` | No -- Wave 0 |
| SEO-03 | Canonical URL | smoke | `grep 'rel="canonical"' output/index.html` | No -- Wave 0 |
| SEO-04 | OG tags | smoke | `grep 'og:title' output/index.html` | No -- Wave 0 |
| SEO-05 | Twitter Card | smoke | `grep 'twitter:card' output/index.html` | No -- Wave 0 |
| SEO-07 | BreadcrumbList schema | smoke | `grep 'BreadcrumbList' output/about/index.html` | No -- Wave 0 |
| QUAL-04 | CURRENT_YEAR variable | smoke | `grep '2026' output/index.html` (footer copyright) | No -- Wave 0 |
| PERF-01 | Lighthouse Performance 90+ | manual | `npx lighthouse URL --only-categories=performance` | No -- Wave 0 |
| PERF-02 | Lighthouse Accessibility 90+ | manual | `npx lighthouse URL --only-categories=accessibility` | No -- Wave 0 |
| PERF-03 | Lighthouse SEO 100 | manual | `npx lighthouse URL --only-categories=seo` | No -- Wave 0 |
| PERF-05 | Google Fonts preconnect | smoke | `grep 'preconnect.*fonts.googleapis' output/index.html` | No -- Wave 0 |

### Sampling Rate
- **Per task commit:** `python3 scripts/build.py && echo "Build OK"`
- **Per wave merge:** Full build + grep checks for all SEO elements
- **Phase gate:** Build succeeds + Lighthouse scores meet thresholds on placeholder page served locally

### Wave 0 Gaps
- [ ] `tests/test_build.sh` -- bash script running all smoke checks above
- [ ] No framework install needed -- bash + grep + python3 are sufficient
- [ ] Lighthouse CLI: `npm install -g lighthouse` (for PERF verification)

## Sources

### Primary (HIGH confidence)
- Provyx website source code at `/Users/rome/Documents/projects/provyx-website/scripts/` -- templates.py (779 lines), nav_config.py (112 lines), build.py (20,733 lines) read directly
- SharpPages brand kit at `/Users/rome/Downloads/sharppages-brand/` -- tokens.css (148 lines), head-snippet.html (31 lines), site.webmanifest (27 lines) read directly
- Provyx robots.txt, js/main.js read directly

### Secondary (MEDIUM confidence)
- None needed -- this is a known architecture being replicated

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- exact same Python stdlib approach as Provyx, no new libraries
- Architecture: HIGH -- three-file pattern directly observed in Provyx source, function signatures documented
- Pitfalls: HIGH -- dark theme contrast and Google Fonts performance are well-understood concerns; JS escaping in f-strings observed in Provyx source

**Research date:** 2026-03-19
**Valid until:** 2026-04-19 (stable pattern, no external dependency changes expected)
