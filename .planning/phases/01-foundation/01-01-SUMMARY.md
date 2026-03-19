---
phase: 01-foundation
plan: 01
subsystem: infra
tags: [html-templates, css-tokens, google-fonts, ga4, og-tags, bem, seo]

# Dependency graph
requires: []
provides:
  - "nav_config.py with site metadata, nav items, footer columns"
  - "templates.py with 9 HTML generator functions for build.py"
  - "styles.css with BEM naming and 52 CSS custom property references"
  - "main.js with scroll, form validation, GA4 helper"
  - "Brand assets (logos, favicons, OG images) at assets/"
  - "tokens.css design tokens and site.webmanifest"
affects: [01-02, 02-core-pages, 03-content-expansion]

# Tech tracking
tech-stack:
  added: [google-fonts-cdn, formspree, ga4-consent-mode-v2]
  patterns: [provyx-build-pattern, dark-theme, bem-css, tokens-css-import]

key-files:
  created:
    - scripts/nav_config.py
    - scripts/templates.py
    - scripts/__init__.py
    - css/styles.css
    - js/main.js
    - tokens.css
    - site.webmanifest
    - assets/logos/ (6 SVGs)
    - assets/favicons/ (6 files)
    - assets/og/ (2 files)
  modified: []

key-decisions:
  - "Google Fonts CDN (not self-hosted) for Instrument Sans + DM Sans"
  - "Output dir pattern: templates.py writes to output/ subdirectory"
  - "No dropdown nav needed -- SharpPages nav is flat (5 items)"
  - "Fixed webmanifest icon paths to /assets/favicons/ to match project structure"

patterns-established:
  - "nav_config.py: single source of truth for site metadata, nav, footer"
  - "templates.py: get_page_wrapper assembles full HTML pages from head+nav+content+footer"
  - "BEM CSS with @import tokens.css, never hardcoded colors"
  - "GA4 Consent Mode v2 with sharppages-consent localStorage key"
  - "sharpConsent() function for consent banner"

requirements-completed: [INFR-02, INFR-03, INFR-04, INFR-05, INFR-09, INFR-10, SEO-01, SEO-02, SEO-03, SEO-04, SEO-05, SEO-07, QUAL-04, PERF-01, PERF-02, PERF-03, PERF-05]

# Metrics
duration: 4min
completed: 2026-03-19
---

# Phase 1 Plan 1: Brand Assets and Shared Templates Summary

**Dark-theme HTML template system with Google Fonts CDN, GA4 Consent Mode v2, BEM CSS tokens, and 9 shared generator functions adapted from Provyx**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-19T19:09:37Z
- **Completed:** 2026-03-19T19:13:57Z
- **Tasks:** 2
- **Files modified:** 21

## Accomplishments
- Brand assets (6 logos, 6 favicons, 2 OG images) copied and paths verified
- nav_config.py exports all 8 required constants (SITE_NAME, SITE_URL, SITE_TAGLINE, COPYRIGHT_YEAR, CTA_HREF, CTA_LABEL, NAV_ITEMS, FOOTER_COLUMNS)
- templates.py provides all 9 required functions producing HTML with Google Fonts preconnect, GA4 G-PLACEHOLDER, OG/Twitter tags, canonical URLs, and consent banner
- styles.css uses 52 CSS custom property references via @import tokens.css with full BEM naming
- main.js delivers header scroll, smooth scroll, form validation with honeypot, and GA4 trackEvent helper in 59 lines

## Task Commits

Each task was committed atomically:

1. **Task 1: Copy brand assets and create nav_config.py** - `3854da8` (feat)
2. **Task 2: Create templates.py, styles.css, and main.js** - `8dcdcc9` (feat)

## Files Created/Modified
- `scripts/nav_config.py` - Site metadata, nav items, footer columns
- `scripts/templates.py` - 9 HTML generator functions for build system
- `scripts/__init__.py` - Package init for imports
- `css/styles.css` - Full site styling with BEM naming and token references
- `js/main.js` - Client-side interactivity (59 lines)
- `tokens.css` - CSS custom properties (copied from brand kit)
- `site.webmanifest` - PWA manifest with corrected icon paths
- `assets/logos/` - 6 SVG logo files (full, icon, wordmark in dark/light)
- `assets/favicons/` - 6 favicon files (SVG, PNG 16/32, apple-touch, PWA 192/512)
- `assets/og/` - OG default image (PNG + SVG)

## Decisions Made
- Used Google Fonts CDN (not self-hosted) matching brand kit head-snippet.html
- templates.py writes to `output/` subdirectory (Provyx writes in-place)
- Fixed webmanifest icon paths from `/favicons/` to `/assets/favicons/` to match project directory structure
- Kept nav flat (no dropdowns) -- SharpPages is simpler than Provyx

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed webmanifest icon paths**
- **Found during:** Task 1 (Copy brand assets)
- **Issue:** Brand kit webmanifest referenced `/favicons/` but project stores favicons at `/assets/favicons/`
- **Fix:** Updated all icon src paths in site.webmanifest to `/assets/favicons/`
- **Files modified:** site.webmanifest
- **Verification:** Paths match actual file locations
- **Committed in:** 3854da8 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Essential path correction for PWA manifest. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All foundation files ready for Plan 02 (build system) to import
- `from nav_config import *` and `from templates import *` both verified working
- styles.css and main.js ready to be served from output directory

---
*Phase: 01-foundation*
*Completed: 2026-03-19*
