# SharpPages

## What This Is

Done-for-you event registration websites + targeted social media ad campaigns (Facebook retargeting, custom audiences) to fill seats for recurring events. Not a DIY tool or SaaS platform. SharpPages builds the site, sets up tracking (GA4, Meta Pixel), and manages the ads. 5-7 day turnaround, premium quality. Target clients: medical device companies, pharma field marketing teams, B2B SaaS, conference organizers, med spas.

## Core Value

The marketing website at sharppages.com must clearly communicate that SharpPages handles everything (page + pixels + paid media) so event organizers just run their event. Every page drives toward a contact/inquiry conversion.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Static marketing website at sharppages.com following Provyx architecture (Python build.py, nav_config.py, templates.py)
- [ ] Homepage applying Harry Dry 10-element landing page formula
- [ ] Services page covering site builds, ad management, and tracking setup
- [ ] Pricing page with tiered pricing from single data structure
- [ ] Work/portfolio page with anonymized BTL Michigan case study
- [ ] About page with Rome's background and why SharpPages exists
- [ ] Contact page with Formspree form and honeypot
- [ ] Privacy and Terms pages
- [ ] 6 ICP pages at /for/ (medical devices, pharma, B2B SaaS, conference organizers, med spas, real estate)
- [ ] 4 blog articles (registration page optimization, Eventbrite comparison, Facebook retargeting, cost comparison)
- [ ] Blog index page
- [ ] Full SEO from day 1: unique meta tags, canonical URLs, OG tags, schema markup (Organization, WebSite, FAQPage, BreadcrumbList, Article, Service)
- [ ] Sitemap.xml and robots.txt auto-generated
- [ ] GA4 tracking placeholder
- [ ] GitHub Pages deployment with CNAME for sharppages.com
- [ ] All copy follows Rome's writing style (zero AI tells, no fabricated stats, call-to-value CTAs)
- [ ] Brand assets integrated (Midnight/Cyan/Gold palette, Instrument Sans + DM Sans, click logo)
- [ ] E-E-A-T signals: author attribution, specific numbers, outbound links to authoritative sources

### Out of Scope

- Backend/CMS functionality — pure static site
- Client portal or login — this is a marketing site, not a SaaS
- Payment processing — contact form drives leads, no checkout
- Event template itself — that's the btl-events repo, not this site
- Blog comments — no commenting system needed
- Newsletter signup — not part of v1 (can add later)
- Multi-language support — English only

## Context

- **Proven product:** BTL Michigan (btlmichigan.com) is live. BTL Minnesota (btlminnesota.com) deployed. Template is reusable and documented in BTL-ADS-PLAYBOOK.md.
- **Architecture reference:** Provyx website at /Users/rome/Documents/projects/provyx-website/ is the primary code pattern to follow (build.py, nav_config.py, templates.py).
- **Brand assets ready:** Full kit at /Users/rome/Downloads/sharppages-brand/ (colors, fonts, logos, favicons, OG images, tokens.css).
- **Writing references:** Harry Dry landing page formula, copywriting principles, Rome writing style guide, content best practices doc. All mandatory reading before any copy.
- **Pricing set:** Site build $3,500-$5,000 (first), $1,500-$2,500 (additional). Ad management $1,500-$2,500/mo + setup. Bundles available.
- **Case study data:** BTL Michigan event provides real (anonymizable) results for portfolio page.
- **Fabricated stats rule:** HARD RULE. Every number must be from BTL case study data, citable third-party source, or real pricing we set. Zero tolerance.
- **Domain:** sharppages.com already on Cloudflare.

## Constraints

- **Tech stack**: Pure static HTML/CSS/JS. Python build system only. No frameworks, no build tools beyond Python. GitHub Pages hosting.
- **Architecture**: Must follow Provyx pattern exactly (scripts/build.py, scripts/nav_config.py, scripts/templates.py, single CSS file, BEM naming).
- **Content depth**: Service/ICP pages 1,200-1,500 words minimum. Blog articles 1,500-2,000 words. Core pages 500+.
- **SEO**: Every page needs unique title (50-60 chars), meta description (150-158 chars), canonical to sharppages.com, schema markup.
- **Performance**: Lighthouse Performance 90+, Accessibility 90+, SEO 100. LCP < 2.5s, CLS < 0.1.
- **Writing**: Zero tolerance for AI writing tells. No em-dashes, no false reframes, no banned words per Rome writing style guide.
- **Stale content prevention**: No specific dates in copy. CURRENT_YEAR variable. Pricing in single data structure. Case study says "Recent" not specific months.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Dark theme (Midnight bg) as primary | Brand kit designed dark-first with cyan accents. Premium feel for high-ticket service. | — Pending |
| Formspree for contact form | No backend needed. Proven pattern from other projects. | — Pending |
| Anonymize BTL case study | Client confidentiality. "Medical Device Manufacturer — Detroit Event" framing. | — Pending |
| Single PRICING dict in build.py | One update propagates to pricing page, service pages, ICP pages. Prevents drift. | — Pending |
| No GA4 ID yet | Need to create property. Placeholder in code, add real ID before launch. | — Pending |

---
*Last updated: 2026-03-19 after initialization*
