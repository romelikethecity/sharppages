#!/usr/bin/env python3
"""
Master build script for the SharpPages website.

Generates a complete static site into output/ by:
- Building HTML pages via templates.py
- Copying static assets (CSS, JS, fonts, images)
- Generating sitemap.xml with all pages and priorities
- Writing robots.txt with AI crawler directives
- Writing CNAME for GitHub Pages custom domain

Usage:
    python3 scripts/build.py
"""

import os
import sys
import shutil

# Allow imports from scripts/ directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from templates import (
    get_page_wrapper,
    get_breadcrumb_schema,
    get_breadcrumb_html,
    generate_cta_section,
    generate_faq_html,
    get_organization_schema,
    get_service_schema,
    write_page,
    BASE_URL,
    OUTPUT_DIR,
)
from nav_config import SITE_NAME, SITE_URL, COPYRIGHT_YEAR


# Project root (one level up from scripts/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All pages: (path, priority, changefreq) tuples for sitemap generation
ALL_PAGES = []


# =============================================================================
# DATA STRUCTURES
# =============================================================================

PRICING = {
    # Website Design & Build
    "site_landing": {"low": 1500, "high": 2500},
    "site_standard": {"low": 3000, "high": 6000},
    "site_content": {"low": 5000, "high": 12000},
    "site_enterprise": {"low": 10000, "high": 25000},
    "lead_magnet_addon": {"low": 1000, "high": 3000},
    # Website Redesign & Migration
    "redesign_wp_sq_wix": {"low": 2500, "high": 6000},
    "redesign_webflow": {"low": 3000, "high": 8000},
    "redesign_custom_cms": {"low": 5000, "high": 15000},
    # SEO & Content Strategy
    "seo_audit": {"low": 500, "high": 1500},
    "seo_programmatic": {"low": 3000, "high": 10000},
    "seo_monthly": {"low": 1500, "high": 3000},
    # Event Registration Sites
    "event_first": {"low": 2000, "high": 4000},
    "event_clone": {"low": 500, "high": 1000},
    # Paid Social Advertising
    "ad_setup": {"low": 500, "high": 1000},
    "ad_monthly": {"low": 1000, "high": 2500},
    # PageSpeed Audit & Fix
    "pagespeed_free": 0,
    "pagespeed_detailed": 500,
    "pagespeed_fix": {"low": 1000, "high": 3000},
}

# Services overview data for homepage cards and services page
SERVICES = [
    {
        "id": "website-design",
        "name": "Website Design & Build",
        "short": "Static HTML/CSS sites, mobile-first, sub-1-second load times. 90+ PageSpeed scores. Full schema markup, OG tags, sitemap. No WordPress maintenance. Flat fee, you own all files.",
        "icon": "&#9889;",
    },
    {
        "id": "website-redesign",
        "name": "Website Redesign & Migration",
        "short": "Migrate from WordPress, Webflow, or Squarespace to static. Same design (or improved), 5x faster load times. No recurring hosting fees, no plugin bloat.",
        "icon": "&#128257;",
    },
    {
        "id": "seo-content",
        "name": "SEO & Content Strategy",
        "short": "Programmatic SEO at scale. Hub-and-spoke architecture for topical authority. Keyword-targeted content (glossary, comparisons, alternatives, location pages). Schema markup for rich results.",
        "icon": "&#128200;",
    },
    {
        "id": "event-sites",
        "name": "Event Registration Sites",
        "short": "Custom registration pages with GA4 + Meta Pixel. Template cloning for multi-city events (48hr turnaround). No per-registrant fees, no platform lock-in.",
        "icon": "&#127919;",
    },
    {
        "id": "paid-social",
        "name": "Paid Social Advertising",
        "short": "Facebook/Instagram campaign management. Custom audience targeting, retargeting, urgency scheduling. 2x industry-average CTR, lower CPC. Full attribution from ad to conversion.",
        "icon": "&#128176;",
    },
    {
        "id": "pagespeed-audit",
        "name": "PageSpeed Audit & Fix",
        "short": "Free instant audit or paid detailed audit with consult. Identify performance bottlenecks and fix them. Before/after PageSpeed scores as deliverable.",
        "icon": "&#128337;",
    },
]

# Pricing page tier cards (the 4 main website build tiers)
TIERS = [
    {
        "name": "Landing Page",
        "desc": "Single page, mobile-optimized, tracking setup. For launches, campaigns, and lead capture.",
        "price_display": f"${PRICING['site_landing']['low']:,}",
        "price_note": f"to ${PRICING['site_landing']['high']:,}",
        "features": [
            "Single-page site, mobile-first",
            "90+ PageSpeed score",
            "GA4 + conversion tracking",
            "Schema markup + OG tags",
            "Deployed on your domain",
            "You own all files",
        ],
        "featured": False,
        "cta": "Get a Free Audit",
    },
    {
        "name": "Standard Site",
        "desc": "5 to 10 pages with full SEO, contact forms, and schema markup. The right fit for most businesses.",
        "price_display": f"${PRICING['site_standard']['low']:,}",
        "price_note": f"to ${PRICING['site_standard']['high']:,}",
        "features": [
            "5-10 pages, custom design",
            "Full schema + structured data",
            "Contact form with spam protection",
            "Blog-ready architecture",
            "Sitemap + robots.txt",
            "90+ PageSpeed score",
        ],
        "featured": True,
        "badge": "Most Popular",
        "cta": "Get a Free Audit",
    },
    {
        "name": "Content Site",
        "desc": "10 to 50+ pages with programmatic SEO, blog infrastructure, and content at scale.",
        "price_display": f"${PRICING['site_content']['low']:,}",
        "price_note": f"to ${PRICING['site_content']['high']:,}",
        "features": [
            "10-50+ pages",
            "Programmatic SEO architecture",
            "Blog with Article schema",
            "Hub-and-spoke content model",
            "Automated sitemap generation",
            "Internal linking strategy",
        ],
        "featured": False,
        "cta": "Get a Free Audit",
    },
    {
        "name": "Enterprise / pSEO",
        "desc": "100+ pages generated from structured data. For businesses that need search dominance at scale.",
        "price_display": f"${PRICING['site_enterprise']['low']:,}",
        "price_note": f"to ${PRICING['site_enterprise']['high']:,}",
        "features": [
            "100+ data-driven pages",
            "Custom build scripts",
            "Comparison + alternative pages",
            "Location + industry verticals",
            "Full schema per page type",
            "Ongoing content expansion",
        ],
        "featured": False,
        "cta": "Let's Build It",
    },
]

FORMSPREE_ID = "xnjobqnr"


# =============================================================================
# HELPER: Standard breadcrumbs
# =============================================================================

def _breadcrumbs(page_name, page_path):
    """Return breadcrumb list and combined HTML+schema."""
    crumbs = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": page_name, "url": BASE_URL + page_path},
    ]
    return crumbs, get_breadcrumb_html(crumbs), get_breadcrumb_schema(crumbs)


# =============================================================================
# PAGE BUILDERS
# =============================================================================

def build_homepage():
    """Build homepage with Harry Dry formula: hero, social proof, problem, animated proof, services, how it works, audit CTA, industries, final CTA."""

    # Organization + WebSite schema
    org_schema = get_organization_schema()

    # Service cards from SERVICES data — link to individual pages
    _svc_slug_map = {
        "website-design": "web-design",
        "website-redesign": "redesign",
        "seo-content": "seo",
        "event-sites": "events",
        "paid-social": "ads",
        "pagespeed-audit": "audit",
    }
    service_cards = ""
    for svc in SERVICES:
        slug = _svc_slug_map.get(svc["id"], svc["id"])
        service_cards += f'''
                    <a href="/services/{slug}/" class="feature-card" style="text-decoration: none; display: block;">
                        <span class="feature-card__icon">{svc['icon']}</span>
                        <h3 class="feature-card__title">{svc['name']}</h3>
                        <p class="feature-card__text">{svc['short']}</p>
                    </a>'''

    # ICP industry links grid
    icp_links = ""
    for icp in ICP_PAGES:
        icp_links += f'<a href="/for/{icp["slug"]}/" class="industry-link">{icp["name"]}</a>\n'

    # FAQ data
    faqs = [
        {
            "question": "How is SharpPages different from a marketing agency?",
            "answer": "Agencies bill hours, staff projects across junior teams, and deliver on Webflow or WordPress. We build static sites that score 90+ on PageSpeed, charge flat fees, and hand you the files when we are done. No retainers unless you want ongoing SEO or ad management."
        },
        {
            "question": "What does a 98 PageSpeed score mean for my business?",
            "answer": "Google uses Core Web Vitals (including page speed) as a ranking factor. A score of 98 means your site loads in under a second on mobile, which reduces bounce rates and improves conversion rates. Most agency-built sites score between 60 and 80."
        },
        {
            "question": "Do you build on WordPress or Webflow?",
            "answer": "Neither. We build static HTML/CSS sites. They load faster, score higher on PageSpeed, cost nothing to host, and have zero security vulnerabilities from plugins. You own all the files."
        },
        {
            "question": "What is programmatic SEO?",
            "answer": "Building hundreds or thousands of pages from structured data. Each page targets a specific keyword (a school profile, a comparison, a location page). We built 398 pages for one client and 322 for another. Both rank on page one for their target terms."
        },
        {
            "question": "How long does a typical project take?",
            "answer": "Landing pages: 1 to 2 weeks. Standard sites (5-10 pages): 2 to 4 weeks. Content sites with programmatic SEO: 4 to 8 weeks. Event registration sites: 5 to 7 business days."
        },
        {
            "question": "What happens after the site launches?",
            "answer": "You own the files. Host them anywhere. If you want ongoing SEO management, content expansion, or ad campaigns, we offer monthly retainers. Otherwise, the site runs on its own with zero maintenance cost."
        },
    ]
    faq_html = generate_faq_html(faqs)

    body = f'''
        <section class="section hero">
            <div class="container">
                <h1 class="hero__title">Fast sites. Real SEO results. <span class="text-accent">No hourly billing.</span></h1>
                <p class="hero__subtitle">Sites that load in under a second. SEO that drives traffic in weeks. Ad campaigns with 2x industry CTR. No change orders, no surprises.</p>
                <div class="hero__cta-group">
                    <a href="/audit/" class="btn btn--primary btn--lg">Get a Free Site Audit</a>
                    <a href="/work/" class="btn btn--outline btn--lg">See Our Work</a>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="stats-bar">
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">98</span>
                        <span class="stats-bar__label">Mobile PageSpeed Score</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">0.9s</span>
                        <span class="stats-bar__label">Speed Index</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">2x</span>
                        <span class="stats-bar__label">Industry Avg CTR</span>
                    </div>
                </div>
                <p class="social-proof-row">Built 700+ pages across client sites. <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">Run yours through PageSpeed Insights and compare.</a></p>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <h2 class="text-center mb-8">Agencies Bill Hours. We Ship Results.</h2>
                <div class="feature-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">
                    <div class="feature-card">
                        <h3 class="feature-card__title">$150-$300/hr</h3>
                        <p class="feature-card__text">Agency hourly rates for sites that score 73 on mobile PageSpeed with 5-second load times. Plus change orders when the first version does not work. Plus Phase 2 when Phase 1 underdelivers.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">6-8 Weeks</h3>
                        <p class="feature-card__text">Typical agency timeline for a site that could ship in two. Meetings about meetings. Design reviews that loop three times. A "strategy phase" that produces a PDF nobody reads.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">Scope Creep Built In</h3>
                        <p class="feature-card__text">Agencies profit from scope changes. Every revision, every new page, every "can we also..." triggers a change order. The original quote was a starting point, not a final price.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="text-center mb-8">The Proof</h2>

                <div class="proof-section">
                    <h3 class="proof-section__heading">PageSpeed: SharpPages vs. Average Agency</h3>
                    <div class="gauge-comparison" data-animate>
                        <div class="gauge-wrapper">
                            <div class="gauge" data-score="98" data-color="green">
                                <svg class="gauge__svg" viewBox="0 0 120 120">
                                    <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                    <circle class="gauge__fill gauge__fill--green" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                                </svg>
                                <span class="gauge__score" data-target="98">0</span>
                            </div>
                            <span class="gauge__label">SharpPages</span>
                            <span class="gauge__detail">0.9s Speed Index &middot; 30ms TBT</span>
                        </div>
                        <div class="gauge-wrapper">
                            <div class="gauge" data-score="73" data-color="orange">
                                <svg class="gauge__svg" viewBox="0 0 120 120">
                                    <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                    <circle class="gauge__fill gauge__fill--orange" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                                </svg>
                                <span class="gauge__score" data-target="73">0</span>
                            </div>
                            <span class="gauge__label">Average Agency</span>
                            <span class="gauge__detail">5.0s Speed Index &middot; 280ms TBT</span>
                        </div>
                    </div>
                </div>

                <div class="proof-section">
                    <h3 class="proof-section__heading">SEO: PE Collective Impression Growth</h3>
                    <p class="proof-section__subtext">From near-zero to 363K impressions in 30 days. 322 pages, programmatic SEO. <a href="https://pecollective.com" target="_blank" rel="noopener noreferrer">See the live site.</a></p>
                    <div class="seo-chart" data-animate>
                        <svg class="seo-chart__svg" viewBox="0 0 600 200" preserveAspectRatio="none">
                            <polyline class="seo-chart__line" points="0,195 150,180 300,150 450,100 600,10" fill="none" />
                        </svg>
                        <div class="seo-chart__labels">
                            <span class="seo-chart__label" data-delay="0">Week 1: 2K</span>
                            <span class="seo-chart__label" data-delay="1">Week 2: 15K</span>
                            <span class="seo-chart__label" data-delay="2">Week 3: 30K</span>
                            <span class="seo-chart__label" data-delay="3">Week 4: 45K/day</span>
                        </div>
                    </div>
                </div>

                <div class="proof-section">
                    <h3 class="proof-section__heading">Ad Performance: BTL Events Campaign</h3>
                    <div class="stats-bar">
                        <div class="stats-bar__item">
                            <span class="stats-bar__number">2x</span>
                            <span class="stats-bar__label">Industry Avg CTR</span>
                        </div>
                        <div class="stats-bar__item">
                            <span class="stats-bar__number">Lower</span>
                            <span class="stats-bar__label">Cost per Click</span>
                        </div>
                        <div class="stats-bar__item">
                            <span class="stats-bar__number">25 days</span>
                            <span class="stats-bar__label">Campaign Structure</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <h2 class="text-center mb-8">What We Build</h2>
                <div class="feature-grid">
                    {service_cards}
                </div>
                <p class="text-center" style="margin-top: var(--space-6);"><a href="/services/" class="btn btn--outline">All Services &amp; Details</a></p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="text-center mb-8">How It Works</h2>
                <div class="process-steps process-steps--horizontal">
                    <div class="process-step">
                        <div class="process-step__number">1</div>
                        <div class="process-step__content">
                            <h3>Scope</h3>
                            <p>You tell us what you need. We review your current site, your goals, and your timeline. You get a fixed quote within two business days.</p>
                        </div>
                    </div>
                    <div class="process-step">
                        <div class="process-step__number">2</div>
                        <div class="process-step__content">
                            <h3>Build</h3>
                            <p>We build the site, write the copy, configure tracking, and set up SEO. You review drafts and approve before anything goes live.</p>
                        </div>
                    </div>
                    <div class="process-step">
                        <div class="process-step__number">3</div>
                        <div class="process-step__content">
                            <h3>Launch</h3>
                            <p>Site goes live on your domain. You own all files. If you want ongoing SEO or ad management, we set that up too. Otherwise, you are done.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container audit-cta">
                <h2 class="text-center mb-4">Free Site Audit</h2>
                <p class="text-center" style="color: var(--color-text-muted); max-width: 640px; margin: 0 auto var(--space-6); line-height: var(--leading-relaxed);">Run your site through our free audit. See your PageSpeed score, SEO gaps, and what is fixable. Takes 30 seconds.</p>
                <div class="text-center">
                    <a href="/audit/" class="btn btn--primary btn--lg">Run Your Free Audit</a>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="text-center mb-8">Industries We Serve</h2>
                <div class="industry-grid">
                    {icp_links}
                </div>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title="Ready to See What Your Site Could Be?",
    text="Tell us about your site. We will review it, discuss your goals, and send a fixed quote within two business days.",
    button_text="Let's Build It",
)}'''

    html = get_page_wrapper(
        title="Fast Sites. Real SEO Results. No Hourly Billing.",
        description="Sites that load in under a second. SEO that drives traffic in weeks. Ad campaigns with 2x industry CTR. Flat fees, no change orders. SharpPages.",
        canonical_path="/",
        body_content=body,
        extra_schema=org_schema,
    )
    write_page("index.html", html)
    ALL_PAGES.append(("/", 1.0, "weekly"))


def build_services():
    """Build services page with visual service blocks: value headline, animation, stats, learn-more link."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Services", "/services/")

    service_schema = get_service_schema([
        {"name": s["name"], "description": s["short"], "url": BASE_URL + "/services/" + s["id"].replace("website-", "web-").replace("website-", "").replace("seo-content", "seo").replace("event-sites", "events").replace("paid-social", "ads").replace("pagespeed-audit", "audit") + "/"}
        for s in SERVICES
    ])

    faqs = [
        {
            "question": "Do you build on WordPress or Webflow?",
            "answer": "Neither. We build static HTML/CSS sites. They load faster (sub-1-second), score 90+ on PageSpeed, cost nothing to host on GitHub Pages or Cloudflare Pages, and have zero plugin vulnerabilities. You own every file."
        },
        {
            "question": "Can you redesign my existing site without changing the design?",
            "answer": "Yes. We can replicate your current design pixel-for-pixel on a static stack. Same look, 5x faster load time, no CMS maintenance. Or we can improve the design during migration. Your call."
        },
        {
            "question": "What does programmatic SEO look like in practice?",
            "answer": "We built 398 pages for getprovyx.com (scored 98 on PageSpeed) and 322 pages for pecollective.com (363K impressions in 30 days). Each page targets a specific keyword with unique, structured content. The build script generates all pages from data."
        },
        {
            "question": "How long does a typical site build take?",
            "answer": "Landing pages: 1 to 2 weeks. Standard sites (5-10 pages): 2 to 4 weeks. Content sites with programmatic SEO: 4 to 8 weeks. Event registration sites: 5 to 7 business days. Timelines depend on content volume and review cycles."
        },
        {
            "question": "What is included in the free site audit?",
            "answer": "You enter your URL and get your PageSpeed scores (Performance, Accessibility, Best Practices, SEO), Speed Index, LCP, CLS, TBT, plus an SEO checklist covering title tags, meta descriptions, H1 presence, schema markup, OG tags, and mobile viewport. Summary is free. Detailed fix priorities require an email."
        },
        {
            "question": "Do you handle ongoing SEO after launch?",
            "answer": "Yes. We offer monthly SEO management ($1,500 to $3,000/mo) that covers content expansion, keyword targeting, technical SEO monitoring, and search performance reporting. Or you can launch and manage it yourself with the infrastructure we build."
        },
    ]
    faq_html = generate_faq_html(faqs)

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Sites That Perform. <span class="text-accent">SEO That Compounds.</span></h1>
                <p class="page-header__subtitle">Six services, all flat-fee. We build fast sites, drive organic traffic, run ad campaigns, and hand you the files. No hourly billing, no platform lock-in.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="stats-bar">
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">700+</span>
                        <span class="stats-bar__label">Pages Built</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">98</span>
                        <span class="stats-bar__label">Avg PageSpeed</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">$0/mo</span>
                        <span class="stats-bar__label">Hosting Cost</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">363K</span>
                        <span class="stats-bar__label">Impressions in 30 Days</span>
                    </div>
                </div>
            </div>
        </section>

        <section class="content-section">
            <div class="container">

                <div class="service-card" id="website-design">
                    <div class="service-card__content">
                        <h2 class="service-card__headline">Sites That Load in Under a Second</h2>
                        <p class="service-card__text">Your visitors decide in 3 seconds. Our static HTML sites load in under one. Every site scores 90+ on Google PageSpeed, costs $0/mo to host, and you own every file. No WordPress maintenance, no plugin vulnerabilities, no platform lock-in.</p>
                        <div class="service-card__visual">
                            <div class="gauge-comparison gauge-comparison--compact" data-animate>
                                <div class="gauge-wrapper">
                                    <div class="gauge" data-score="98" data-color="green">
                                        <svg class="gauge__svg" viewBox="0 0 120 120">
                                            <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                            <circle class="gauge__fill gauge__fill--green" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                                        </svg>
                                        <span class="gauge__score" data-target="98">0</span>
                                    </div>
                                    <span class="gauge__label">SharpPages</span>
                                    <span class="gauge__detail">0.9s load &middot; $0/mo</span>
                                </div>
                                <div class="gauge-wrapper">
                                    <div class="gauge" data-score="73" data-color="orange">
                                        <svg class="gauge__svg" viewBox="0 0 120 120">
                                            <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                            <circle class="gauge__fill gauge__fill--orange" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                                        </svg>
                                        <span class="gauge__score" data-target="73">0</span>
                                    </div>
                                    <span class="gauge__label">Avg Agency Site</span>
                                    <span class="gauge__detail">5.0s load &middot; $50+/mo</span>
                                </div>
                            </div>
                        </div>
                        <div class="service-card__stats">
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">98</span>
                                <span class="service-card__stat-label">PageSpeed Score</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">0.9s</span>
                                <span class="service-card__stat-label">Speed Index</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">$0</span>
                                <span class="service-card__stat-label">Monthly Hosting</span>
                            </div>
                        </div>
                        <div class="service-card__footer">
                            <a href="/services/web-design/" class="service-card__link">See how it works &rarr;</a>
                            <span class="service-card__price">From ${PRICING['site_landing']['low']:,}</span>
                        </div>
                    </div>
                </div>

                <div class="service-card" id="website-redesign">
                    <div class="service-card__content">
                        <h2 class="service-card__headline">Same Design. 5x Faster.</h2>
                        <p class="service-card__text">Migrate from WordPress, Webflow, or Squarespace without changing your design. Your site goes from scoring 45 on mobile to 95+. Same look, zero recurring hosting fees, no plugin vulnerabilities. We deliver before/after PageSpeed scores as proof.</p>
                        <div class="service-card__visual">
                            <div class="before-after" data-animate>
                                <div class="before-after__item before-after__item--before">
                                    <span class="before-after__badge before-after__badge--red">Before</span>
                                    <div class="before-after__browser">
                                        <div class="before-after__bar"></div>
                                        <div class="before-after__skeleton">
                                            <div class="skeleton-line skeleton-line--title"></div>
                                            <div class="skeleton-line skeleton-line--text"></div>
                                            <div class="skeleton-line skeleton-line--text skeleton-line--short"></div>
                                            <div class="skeleton-line skeleton-line--img"></div>
                                            <div class="skeleton-line skeleton-line--text"></div>
                                        </div>
                                        <div class="before-after__loader">
                                            <div class="before-after__spinner"></div>
                                            <span>Loading... 4.2s</span>
                                        </div>
                                    </div>
                                    <span class="before-after__score before-after__score--red">45</span>
                                </div>
                                <div class="before-after__item before-after__item--after">
                                    <span class="before-after__badge before-after__badge--green">After</span>
                                    <div class="before-after__browser">
                                        <div class="before-after__bar"></div>
                                        <div class="before-after__loaded">
                                            <div class="loaded-line loaded-line--title"></div>
                                            <div class="loaded-line loaded-line--text"></div>
                                            <div class="loaded-line loaded-line--text loaded-line--short"></div>
                                            <div class="loaded-line loaded-line--img"></div>
                                            <div class="loaded-line loaded-line--text"></div>
                                        </div>
                                    </div>
                                    <span class="before-after__score before-after__score--green">95</span>
                                </div>
                            </div>
                        </div>
                        <div class="service-card__stats">
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">5x</span>
                                <span class="service-card__stat-label">Faster Load</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">$0</span>
                                <span class="service-card__stat-label">Recurring Cost</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">0</span>
                                <span class="service-card__stat-label">Plugin Vulnerabilities</span>
                            </div>
                        </div>
                        <div class="service-card__footer">
                            <a href="/services/redesign/" class="service-card__link">See how it works &rarr;</a>
                            <span class="service-card__price">From ${PRICING['redesign_wp_sq_wix']['low']:,}</span>
                        </div>
                    </div>
                </div>

                <div class="service-card" id="seo-content">
                    <div class="service-card__content">
                        <h2 class="service-card__headline">363K Impressions in 30 Days</h2>
                        <p class="service-card__text">Programmatic SEO that builds hundreds of keyword-targeted pages from structured data. Hub-and-spoke architecture for topical authority. We built 322 pages for PE Collective and drove 363K impressions in a single month from near-zero.</p>
                        <div class="service-card__visual">
                            <div class="seo-chart" data-animate>
                                <svg class="seo-chart__svg" viewBox="0 0 600 200" preserveAspectRatio="none">
                                    <polyline class="seo-chart__line" points="0,195 150,180 300,150 450,100 600,10" fill="none" />
                                </svg>
                                <div class="seo-chart__labels">
                                    <span class="seo-chart__label" data-delay="0">Week 1: 2K</span>
                                    <span class="seo-chart__label" data-delay="1">Week 2: 15K</span>
                                    <span class="seo-chart__label" data-delay="2">Week 3: 30K</span>
                                    <span class="seo-chart__label" data-delay="3">Week 4: 45K/day</span>
                                </div>
                            </div>
                        </div>
                        <div class="service-card__stats">
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">363K</span>
                                <span class="service-card__stat-label">Impressions</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">322</span>
                                <span class="service-card__stat-label">Pages Built</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">30</span>
                                <span class="service-card__stat-label">Days to Results</span>
                            </div>
                        </div>
                        <div class="service-card__footer">
                            <a href="/services/seo/" class="service-card__link">See how it works &rarr;</a>
                            <span class="service-card__price">From ${PRICING['seo_audit']['low']:,}</span>
                        </div>
                    </div>
                </div>

                <div class="service-card" id="event-sites">
                    <div class="service-card__content">
                        <h2 class="service-card__headline">One Site Built. Every City Cloned in 48 Hours.</h2>
                        <p class="service-card__text">Custom event registration pages with GA4 and Meta Pixel installed from day one. Running the same event in another city? We clone the template, swap the details, and deploy in 48 hours. No per-registrant fees, no Eventbrite branding.</p>
                        <div class="service-card__visual">
                            <div class="multi-city" data-animate>
                                <div class="multi-city__frame multi-city__frame--1">
                                    <div class="multi-city__bar"></div>
                                    <div class="multi-city__body">
                                        <div class="multi-city__title-line"></div>
                                        <div class="multi-city__text-line"></div>
                                        <div class="multi-city__btn-line"></div>
                                    </div>
                                    <span class="multi-city__label">Houston</span>
                                </div>
                                <div class="multi-city__frame multi-city__frame--2">
                                    <div class="multi-city__bar"></div>
                                    <div class="multi-city__body">
                                        <div class="multi-city__title-line"></div>
                                        <div class="multi-city__text-line"></div>
                                        <div class="multi-city__btn-line"></div>
                                    </div>
                                    <span class="multi-city__label">Dallas</span>
                                </div>
                                <div class="multi-city__frame multi-city__frame--3">
                                    <div class="multi-city__bar"></div>
                                    <div class="multi-city__body">
                                        <div class="multi-city__title-line"></div>
                                        <div class="multi-city__text-line"></div>
                                        <div class="multi-city__btn-line"></div>
                                    </div>
                                    <span class="multi-city__label">Phoenix</span>
                                </div>
                                <span class="multi-city__time">48hrs each</span>
                            </div>
                        </div>
                        <div class="service-card__stats">
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">$0</span>
                                <span class="service-card__stat-label">Per-Registrant Fee</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">48hr</span>
                                <span class="service-card__stat-label">Clone Turnaround</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">100%</span>
                                <span class="service-card__stat-label">Attribution</span>
                            </div>
                        </div>
                        <div class="service-card__footer">
                            <a href="/services/events/" class="service-card__link">See how it works &rarr;</a>
                            <span class="service-card__price">From ${PRICING['event_first']['low']:,}</span>
                        </div>
                    </div>
                </div>

                <div class="service-card" id="paid-social">
                    <div class="service-card__content">
                        <h2 class="service-card__headline">62% Lower Ad Costs. 2x More Clicks.</h2>
                        <p class="service-card__text">Facebook and Instagram campaigns with custom audience targeting from your contact list. We build retargeting pools, run structured urgency schedules, and deliver full attribution from ad impression to conversion. Our clients pay 62% less per click than industry average.</p>
                        <div class="service-card__visual">
                            <div class="cost-comparison" data-animate>
                                <div class="cost-comparison__bar">
                                    <span class="cost-comparison__label">Industry Average</span>
                                    <div class="cost-comparison__track">
                                        <div class="cost-comparison__fill cost-comparison__fill--competitor" style="width: 0%;" data-width="100%"></div>
                                    </div>
                                    <span class="cost-comparison__value cost-comparison__value--competitor">$3&ndash;$8+</span>
                                </div>
                                <div class="cost-comparison__bar">
                                    <span class="cost-comparison__label">SharpPages</span>
                                    <div class="cost-comparison__track">
                                        <div class="cost-comparison__fill cost-comparison__fill--sharp" style="width: 0%;" data-width="38%"></div>
                                    </div>
                                    <span class="cost-comparison__value cost-comparison__value--sharp">$1.50</span>
                                </div>
                            </div>
                        </div>
                        <div class="service-card__stats">
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">62%</span>
                                <span class="service-card__stat-label">Lower CPC</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">2x</span>
                                <span class="service-card__stat-label">Industry Avg CTR</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">Full</span>
                                <span class="service-card__stat-label">Ad-to-Conversion Tracking</span>
                            </div>
                        </div>
                        <div class="service-card__footer">
                            <a href="/services/ads/" class="service-card__link">See how it works &rarr;</a>
                            <span class="service-card__price">From ${PRICING['ad_setup']['low']:,}</span>
                        </div>
                    </div>
                </div>

                <div class="service-card" id="pagespeed-audit">
                    <div class="service-card__content">
                        <h2 class="service-card__headline">Find Out What Is Slowing You Down</h2>
                        <p class="service-card__text">Enter your URL and get your PageSpeed scores, SEO checklist, and performance bottlenecks in 30 seconds. Free, no signup required. If your site needs hands-on work, we fix render-blocking resources, oversized images, and JavaScript bloat. Before/after scores as proof.</p>
                        <div class="service-card__visual">
                            <div class="gauge-comparison gauge-comparison--compact" data-animate>
                                <div class="gauge-wrapper">
                                    <div class="gauge" data-score="45" data-color="red">
                                        <svg class="gauge__svg" viewBox="0 0 120 120">
                                            <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                            <circle class="gauge__fill gauge__fill--red" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                                        </svg>
                                        <span class="gauge__score" data-target="45">0</span>
                                    </div>
                                    <span class="gauge__label">Before</span>
                                </div>
                                <div class="gauge-wrapper gauge-wrapper--arrow">
                                    <span class="gauge-arrow">&rarr;</span>
                                </div>
                                <div class="gauge-wrapper">
                                    <div class="gauge" data-score="95" data-color="green">
                                        <svg class="gauge__svg" viewBox="0 0 120 120">
                                            <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                            <circle class="gauge__fill gauge__fill--green" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                                        </svg>
                                        <span class="gauge__score" data-target="95">0</span>
                                    </div>
                                    <span class="gauge__label">After</span>
                                </div>
                            </div>
                        </div>
                        <div class="service-card__stats">
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">Free</span>
                                <span class="service-card__stat-label">Instant Audit</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">30s</span>
                                <span class="service-card__stat-label">Time to Results</span>
                            </div>
                            <div class="service-card__stat">
                                <span class="service-card__stat-number">90+</span>
                                <span class="service-card__stat-label">Post-Fix Score</span>
                            </div>
                        </div>
                        <div class="service-card__footer">
                            <a href="/services/audit/" class="service-card__link">See how it works &rarr;</a>
                            <span class="service-card__price">Free / From ${PRICING['pagespeed_fix']['low']:,}</span>
                        </div>
                    </div>
                </div>

            </div>
        </section>

        <section class="section section--alt">
            <div class="container text-center">
                <h2 class="mb-4">Not Sure Where to Start?</h2>
                <p style="color: var(--color-text-muted); max-width: 640px; margin: 0 auto var(--space-8); line-height: var(--leading-relaxed);">Run a free audit on your current site. It takes 30 seconds and shows you exactly what is fixable. Then we can scope the right project together.</p>
                <a href="/audit/" class="btn btn--primary btn--lg">Run Your Free Audit</a>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title="Ready to See What Your Site Could Be?",
    text="Tell us about your site. We will review it, discuss your goals, and send a fixed quote within two business days.",
    button_text="Let's Build It",
)}'''

    html = get_page_wrapper(
        title="Services: Web Design, SEO, Ads, PageSpeed",
        description="Website design, redesign, programmatic SEO, event sites, paid social, and PageSpeed audits. Flat fees, 90+ PageSpeed scores, you own the files. SharpPages.",
        canonical_path="/services/",
        body_content=body,
        active_page="/services/",
        extra_schema=breadcrumb_schema + service_schema,
    )
    write_page("services/index.html", html)
    ALL_PAGES.append(("/services/", 0.9, "monthly"))


def _service_breadcrumbs(service_name, service_path):
    """Return 3-level breadcrumbs for a service sub-page."""
    crumbs = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": "Services", "url": BASE_URL + "/services/"},
        {"name": service_name, "url": BASE_URL + service_path},
    ]
    return crumbs, get_breadcrumb_html(crumbs), get_breadcrumb_schema(crumbs)


def _service_page(slug, title, meta_desc, headline, hero_text, proof_html,
                  process_steps, includes, stats, pricing_html, faqs,
                  related_services=None,
                  cta_title="Ready to Get Started?",
                  cta_text="Tell us about your project. We will scope the work, give you a fixed quote, and explain exactly what is included.",
                  cta_btn="Let's Build It", cta_href="/contact/"):
    """Build an individual service page with standardized structure."""

    path = f"/services/{slug}/"
    crumbs, breadcrumb_nav, breadcrumb_schema = _service_breadcrumbs(title, path)

    service_schema = get_service_schema([
        {"name": title, "description": meta_desc, "url": BASE_URL + path}
    ])
    faq_html = generate_faq_html(faqs)

    # Process steps HTML
    steps_html = ""
    for i, step in enumerate(process_steps, 1):
        steps_html += f'''
                    <div class="process-step">
                        <div class="process-step__number">{i}</div>
                        <div class="process-step__content">
                            <h3>{step["title"]}</h3>
                            <p>{step["text"]}</p>
                        </div>
                    </div>'''

    # Includes grid HTML
    includes_html = ""
    for item in includes:
        includes_html += f'<span class="service-block__item">{item}</span>\n'

    # Stats bar HTML
    stats_html = ""
    for stat in stats:
        stats_html += f'''
                        <div class="service-card__stat">
                            <span class="service-card__stat-number">{stat["number"]}</span>
                            <span class="service-card__stat-label">{stat["label"]}</span>
                        </div>'''

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">{headline}</h1>
                <p class="page-header__subtitle">{hero_text}</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                {proof_html}
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2 class="text-center mb-8">How It Works</h2>
                <div class="process-steps process-steps--horizontal">
                    {steps_html}
                </div>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2 class="mb-8">What Is Included</h2>
                <div class="service-block__includes">
                    {includes_html}
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="service-card__stats" style="justify-content: center; max-width: 600px; margin: 0 auto;">
                    {stats_html}
                </div>
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2 class="mb-8">Pricing</h2>
                {pricing_html}
                <p style="color: var(--color-text-muted); margin-top: var(--space-6);"><a href="/pricing/">See full pricing for all services &rarr;</a></p>
            </div>
        </section>

{faq_html}
'''

    # Related services cross-links
    if related_services:
        related_html = ""
        for rs in related_services:
            related_html += f'''
                        <a href="/services/{rs["slug"]}/" class="related-service">
                            <span class="related-service__name">{rs["name"]}</span>
                            <span class="related-service__desc">{rs["desc"]}</span>
                        </a>'''
        body += f'''
        <section class="content-section section--alt">
            <div class="container">
                <h2 class="text-center mb-8">Related Services</h2>
                <div class="related-services">
                    {related_html}
                </div>
            </div>
        </section>
'''

    body += f'''
{generate_cta_section(title=cta_title, text=cta_text, button_text=cta_btn, button_href=cta_href)}'''

    html = get_page_wrapper(
        title=f"{title} | Services",
        description=meta_desc,
        canonical_path=path,
        body_content=body,
        active_page="/services/",
        extra_schema=breadcrumb_schema + service_schema,
    )
    write_page(f"services/{slug}/index.html", html)
    ALL_PAGES.append((path, 0.8, "monthly"))


def build_service_web_design():
    """Build individual service page: Website Design & Build."""
    _service_page(
        slug="web-design",
        title="Website Design & Build",
        meta_desc="Static HTML/CSS sites that load in under a second. 90+ PageSpeed scores, $0/mo hosting, you own every file. Flat fee, no platform lock-in.",
        headline='Sites That Load in <span class="text-accent">Under a Second</span>',
        hero_text="Static HTML/CSS sites built mobile-first. Every site scores 90+ on Google PageSpeed, costs $0/mo to host, and you own all source files. No WordPress, no plugins, no recurring platform costs.",
        proof_html=f'''
                <h2>The Proof</h2>
                <p class="case-study__summary">We built getprovyx.com: 398 pages, 98 PageSpeed score, 0.9s Speed Index. Run it through <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">PageSpeed Insights</a> yourself. Compare it to any agency-built Webflow or WordPress site.</p>
                <div class="gauge-comparison" data-animate style="margin-top: var(--space-8);">
                    <div class="gauge-wrapper">
                        <div class="gauge" data-score="98" data-color="green">
                            <svg class="gauge__svg" viewBox="0 0 120 120">
                                <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                <circle class="gauge__fill gauge__fill--green" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                            </svg>
                            <span class="gauge__score" data-target="98">0</span>
                        </div>
                        <span class="gauge__label">SharpPages</span>
                        <span class="gauge__detail">0.9s Speed Index &middot; 30ms TBT</span>
                    </div>
                    <div class="gauge-wrapper">
                        <div class="gauge" data-score="73" data-color="orange">
                            <svg class="gauge__svg" viewBox="0 0 120 120">
                                <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                <circle class="gauge__fill gauge__fill--orange" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                            </svg>
                            <span class="gauge__score" data-target="73">0</span>
                        </div>
                        <span class="gauge__label">Average Agency</span>
                        <span class="gauge__detail">5.0s Speed Index &middot; 280ms TBT</span>
                    </div>
                </div>

                <div class="case-study__comparison" style="margin-top: var(--space-8);">
                    <table class="comparison-table">
                        <thead><tr><th>Metric</th><th class="col-sharp">SharpPages</th><th class="col-competitor">Agency / Webflow</th></tr></thead>
                        <tbody>
                            <tr><td>Performance</td><td class="col-sharp">98</td><td class="col-competitor">73</td></tr>
                            <tr><td>Speed Index</td><td class="col-sharp">0.9s</td><td class="col-competitor">5.0s</td></tr>
                            <tr><td>Monthly Hosting</td><td class="col-sharp">$0</td><td class="col-competitor">$29-$79/mo</td></tr>
                            <tr><td>Plugin Vulnerabilities</td><td class="col-sharp">0</td><td class="col-competitor">Varies</td></tr>
                            <tr><td>File Ownership</td><td class="col-sharp">You own all files</td><td class="col-competitor">Platform-locked</td></tr>
                        </tbody>
                    </table>
                </div>''',
        process_steps=[
            {"title": "Scope", "text": "You tell us what you need. We review your goals, content, and timeline. You get a fixed quote within two business days."},
            {"title": "Build", "text": "We design and develop the site, configure tracking and SEO. You review drafts and approve before launch."},
            {"title": "Launch", "text": "Site goes live on your domain. You own all files. Host them anywhere with zero recurring costs."},
        ],
        includes=[
            "Mobile-first, responsive design",
            "90+ PageSpeed score guaranteed",
            "Full schema markup + OG tags",
            "XML sitemap + robots.txt",
            "GA4 + conversion tracking",
            "Contact form with spam protection",
            "Deployed on your domain",
            "You own all source files",
        ],
        stats=[
            {"number": "98", "label": "PageSpeed Score"},
            {"number": "0.9s", "label": "Speed Index"},
            {"number": "$0/mo", "label": "Hosting Cost"},
            {"number": "398", "label": "Pages Built"},
        ],
        pricing_html=f'''
                <div class="pricing-table-wrap">
                    <table class="pricing-table">
                        <thead><tr><th>Tier</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>Landing Page (1 page)</td><td>${PRICING['site_landing']['low']:,} to ${PRICING['site_landing']['high']:,}</td></tr>
                            <tr><td>Standard Site (5-10 pages)</td><td>${PRICING['site_standard']['low']:,} to ${PRICING['site_standard']['high']:,}</td></tr>
                            <tr><td>Content Site (10-50+ pages)</td><td>${PRICING['site_content']['low']:,} to ${PRICING['site_content']['high']:,}</td></tr>
                            <tr><td>Enterprise / pSEO (100+ pages)</td><td>${PRICING['site_enterprise']['low']:,} to ${PRICING['site_enterprise']['high']:,}</td></tr>
                            <tr><td>Lead Magnet Add-on</td><td>+${PRICING['lead_magnet_addon']['low']:,} to ${PRICING['lead_magnet_addon']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>''',
        faqs=[
            {"question": "Do you build on WordPress or Webflow?", "answer": "Neither. We build static HTML/CSS sites. They load faster (sub-1-second), score 90+ on PageSpeed, cost nothing to host, and have zero plugin vulnerabilities. You own every file."},
            {"question": "How long does a typical site build take?", "answer": "Landing pages: 1 to 2 weeks. Standard sites (5-10 pages): 2 to 4 weeks. Content sites with programmatic SEO: 4 to 8 weeks. We give you a fixed timeline upfront."},
            {"question": "Can I update the site myself after launch?", "answer": "Yes. You own all HTML/CSS/JS files. Edit them in any code editor or hire any developer. No proprietary CMS, no platform dependency."},
            {"question": "What is a lead magnet add-on?", "answer": "An interactive tool built into your site: a PageSpeed audit, ROI calculator, assessment quiz, or similar. These convert 2-5x better than static contact forms because the visitor gets immediate value."},
        ],
        related_services=[
            {"slug": "redesign", "name": "Redesign & Migration", "desc": "Already have a site? We migrate it to static HTML."},
            {"slug": "seo", "name": "SEO & Content", "desc": "Drive organic traffic with programmatic SEO at scale."},
        ],
    )


def build_service_redesign():
    """Build individual service page: Website Redesign & Migration."""
    _service_page(
        slug="redesign",
        title="Website Redesign & Migration",
        meta_desc="Migrate from WordPress, Webflow, or Squarespace to static HTML. Same design, 5x faster load times, zero recurring hosting costs.",
        headline='Same Design. <span class="text-accent">5x Faster.</span>',
        hero_text="Migrate from WordPress, Webflow, Squarespace, or Wix to a static site. Same design (or improved), 5x faster load times. No recurring hosting fees, no plugin vulnerabilities, no CMS updates breaking your layout.",
        proof_html='''
                <h2>Before &amp; After</h2>
                <p class="case-study__summary">Most WordPress sites score 40 to 65 on mobile PageSpeed. After migration to static HTML, those same sites score 90+. The design stays the same. The speed changes everything.</p>
                <div class="before-after" data-animate style="margin-top: var(--space-8);">
                    <div class="before-after__item before-after__item--before">
                        <span class="before-after__badge before-after__badge--red">Before (WordPress)</span>
                        <div class="before-after__browser">
                            <div class="before-after__bar"></div>
                            <div class="before-after__skeleton">
                                <div class="skeleton-line skeleton-line--title"></div>
                                <div class="skeleton-line skeleton-line--text"></div>
                                <div class="skeleton-line skeleton-line--text skeleton-line--short"></div>
                                <div class="skeleton-line skeleton-line--img"></div>
                                <div class="skeleton-line skeleton-line--text"></div>
                            </div>
                            <div class="before-after__loader">
                                <div class="before-after__spinner"></div>
                                <span>Loading... 4.2s</span>
                            </div>
                        </div>
                        <span class="before-after__score before-after__score--red">45</span>
                    </div>
                    <div class="before-after__item before-after__item--after">
                        <span class="before-after__badge before-after__badge--green">After (Static)</span>
                        <div class="before-after__browser">
                            <div class="before-after__bar"></div>
                            <div class="before-after__loaded">
                                <div class="loaded-line loaded-line--title"></div>
                                <div class="loaded-line loaded-line--text"></div>
                                <div class="loaded-line loaded-line--text loaded-line--short"></div>
                                <div class="loaded-line loaded-line--img"></div>
                                <div class="loaded-line loaded-line--text"></div>
                            </div>
                        </div>
                        <span class="before-after__score before-after__score--green">95</span>
                    </div>
                </div>''',
        process_steps=[
            {"title": "Audit", "text": "We run your current site through PageSpeed, inventory all pages and content, and identify what needs to migrate."},
            {"title": "Rebuild", "text": "We recreate your design in static HTML/CSS. Same look (or improved), dramatically faster. Full SEO preservation with redirects."},
            {"title": "Deploy", "text": "New site goes live on your domain. Before/after PageSpeed scores delivered as proof. Zero recurring hosting costs."},
        ],
        includes=[
            "Design-faithful or improved migration",
            "5x faster load times (typical)",
            "Before/after PageSpeed scores",
            "No recurring hosting fees",
            "Zero plugin dependencies",
            "Full SEO preservation (redirects, canonicals)",
            "Content migration from existing CMS",
            "GA4 + tracking reconfiguration",
        ],
        stats=[
            {"number": "5x", "label": "Faster Load Times"},
            {"number": "$0/mo", "label": "Recurring Costs"},
            {"number": "0", "label": "Plugin Vulnerabilities"},
        ],
        pricing_html=f'''
                <div class="pricing-table-wrap">
                    <table class="pricing-table">
                        <thead><tr><th>Migrating From</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>WordPress / Squarespace / Wix</td><td>${PRICING['redesign_wp_sq_wix']['low']:,} to ${PRICING['redesign_wp_sq_wix']['high']:,}</td></tr>
                            <tr><td>Webflow</td><td>${PRICING['redesign_webflow']['low']:,} to ${PRICING['redesign_webflow']['high']:,}</td></tr>
                            <tr><td>Custom CMS</td><td>${PRICING['redesign_custom_cms']['low']:,} to ${PRICING['redesign_custom_cms']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>''',
        faqs=[
            {"question": "Will my design change?", "answer": "Only if you want it to. We can replicate your current design pixel-for-pixel on a static stack, or improve it during migration. Your call."},
            {"question": "What about my existing SEO rankings?", "answer": "We set up 301 redirects for every URL, preserve canonical tags, and carry over all meta data. Your rankings are protected."},
            {"question": "How long does a migration take?", "answer": "Most migrations take 2 to 4 weeks depending on page count and content complexity. We give you a fixed timeline upfront."},
            {"question": "What if I have a custom CMS?", "answer": "We can migrate from any platform. Custom CMS migrations start at $5,000 and depend on the complexity of the content structure."},
        ],
        related_services=[
            {"slug": "audit", "name": "PageSpeed Audit", "desc": "See your current scores before migrating."},
            {"slug": "seo", "name": "SEO & Content", "desc": "Preserve rankings and grow organic traffic post-migration."},
        ],
    )


def build_service_seo():
    """Build individual service page: SEO & Content Strategy."""
    _service_page(
        slug="seo",
        title="SEO & Content Strategy",
        meta_desc="Programmatic SEO at scale. 322 pages drove 363K impressions in 30 days. Hub-and-spoke architecture, keyword targeting, schema markup.",
        headline='363K Impressions. <span class="text-accent">30 Days.</span>',
        hero_text="Programmatic SEO that builds hundreds of keyword-targeted pages from structured data. Hub-and-spoke architecture for topical authority. Real results from real campaigns.",
        proof_html='''
                <h2>PE Collective Case Study</h2>
                <p class="case-study__summary">We built 322 pages for <a href="https://pecollective.com" target="_blank" rel="noopener noreferrer">PE Collective</a> and drove 363K impressions in 30 days from near-zero. Each page targets a specific search intent with structured content. Google indexed the pages quickly because the site loads fast, the content is structured, and the schema markup is correct on every page.</p>

                <div class="case-study__stats" style="margin: var(--space-8) 0;">
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">363K</span>
                        <span class="case-study__stat-label">Impressions (30 days)</span>
                    </div>
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">322</span>
                        <span class="case-study__stat-label">Pages Built</span>
                    </div>
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">8.8</span>
                        <span class="case-study__stat-label">Avg Position</span>
                    </div>
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">30 days</span>
                        <span class="case-study__stat-label">Time to Results</span>
                    </div>
                </div>

                <h3>Impression Growth</h3>
                <div class="seo-chart" data-animate>
                    <svg class="seo-chart__svg" viewBox="0 0 600 200" preserveAspectRatio="none">
                        <polyline class="seo-chart__line" points="0,195 150,180 300,150 450,100 600,10" fill="none" />
                    </svg>
                    <div class="seo-chart__labels">
                        <span class="seo-chart__label" data-delay="0">Week 1: 2K</span>
                        <span class="seo-chart__label" data-delay="1">Week 2: 15K</span>
                        <span class="seo-chart__label" data-delay="2">Week 3: 30K</span>
                        <span class="seo-chart__label" data-delay="3">Week 4: 45K/day</span>
                    </div>
                </div>

                <p class="case-study__summary" style="margin-top: var(--space-6);">We also built 398 pages for getprovyx.com with a 98 PageSpeed score. The model works because the content is structured, the pages are fast, and each one targets a specific search intent.</p>''',
        process_steps=[
            {"title": "Research", "text": "Keyword research, competitive analysis, and content architecture planning. We identify the pages that will drive the most traffic."},
            {"title": "Build", "text": "Generate pages from structured data with unique content, schema markup, and internal links on every page. Hub-and-spoke architecture for topical authority."},
            {"title": "Launch & Monitor", "text": "Deploy all pages, submit to Search Console, and monitor indexing and rankings. Monthly reports on impressions, clicks, and position changes."},
        ],
        includes=[
            "Programmatic SEO buildout",
            "Hub-and-spoke content architecture",
            "Keyword research + targeting",
            "Schema markup for rich results",
            "Internal linking strategy",
            "Monthly performance reporting",
            "Search Console monitoring",
            "Content expansion roadmap",
        ],
        stats=[
            {"number": "363K", "label": "Impressions in 30 Days"},
            {"number": "322", "label": "Pages Built"},
            {"number": "8.8", "label": "Average Position"},
            {"number": "98", "label": "PageSpeed Score"},
        ],
        pricing_html=f'''
                <div class="pricing-table-wrap">
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>SEO Audit</td><td>${PRICING['seo_audit']['low']:,} to ${PRICING['seo_audit']['high']:,}</td></tr>
                            <tr><td>Programmatic SEO Buildout</td><td>${PRICING['seo_programmatic']['low']:,} to ${PRICING['seo_programmatic']['high']:,}</td></tr>
                            <tr><td>Monthly SEO Management</td><td>${PRICING['seo_monthly']['low']:,} to ${PRICING['seo_monthly']['high']:,}/mo</td></tr>
                        </tbody>
                    </table>
                </div>''',
        faqs=[
            {"question": "What is programmatic SEO?", "answer": "Building hundreds or thousands of pages from structured data. Each page targets a specific keyword with unique content. We built 398 pages for one client and 322 for another. Both rank on page one for their target terms."},
            {"question": "How long until I see results?", "answer": "PE Collective hit 363K impressions in 30 days. Most projects see meaningful traffic within 2 to 6 weeks of launch, depending on domain authority and keyword difficulty."},
            {"question": "Do you write the content?", "answer": "We generate structured content from data. Each page has unique titles, descriptions, and body content targeting specific search intents. This is not AI-generated blog spam. It is structured, keyword-targeted content at scale."},
            {"question": "Can I manage SEO myself after launch?", "answer": "Yes. We hand you the build system, content architecture, and all files. You can expand it yourself or hire us for monthly management."},
        ],
        related_services=[
            {"slug": "web-design", "name": "Web Design & Build", "desc": "Need a new site to go with your SEO strategy?"},
            {"slug": "ads", "name": "Paid Social", "desc": "Supplement organic traffic with targeted Meta campaigns."},
        ],
    )


def build_service_events():
    """Build individual service page: Event Registration Sites."""
    _service_page(
        slug="events",
        title="Event Registration Sites",
        meta_desc="Custom event registration pages with GA4 + Meta Pixel. Multi-city cloning in 48 hours. No per-registrant fees, no Eventbrite branding.",
        headline='One Site Built. <span class="text-accent">Every City Cloned.</span>',
        hero_text="Custom registration pages with GA4 and Meta Pixel installed from day one. Running the same event in another city? We clone the template, swap the details, and deploy in 48 hours. No per-registrant fees, no platform lock-in.",
        proof_html=f'''
                <h2>BTL Events Case Study</h2>
                <p class="case-study__summary">Multi-city physician event campaign. We built the registration sites and ran the ads together. The first city took 5 to 7 days. Each additional city cloned in 48 hours with fresh venue details, local contact lists, and separate tracking.</p>

                <div class="case-study__stats" style="margin: var(--space-8) 0;">
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">$0</span>
                        <span class="case-study__stat-label">Per-Registrant Fee</span>
                    </div>
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">48hrs</span>
                        <span class="case-study__stat-label">Per-City Clone</span>
                    </div>
                    <div class="case-study__stat">
                        <span class="case-study__stat-number">100%</span>
                        <span class="case-study__stat-label">Attribution</span>
                    </div>
                </div>

                <div class="multi-city" data-animate style="margin-top: var(--space-8);">
                    <div class="multi-city__frame multi-city__frame--1">
                        <div class="multi-city__bar"></div>
                        <div class="multi-city__body">
                            <div class="multi-city__title-line"></div>
                            <div class="multi-city__text-line"></div>
                            <div class="multi-city__btn-line"></div>
                        </div>
                        <span class="multi-city__label">Houston</span>
                    </div>
                    <div class="multi-city__frame multi-city__frame--2">
                        <div class="multi-city__bar"></div>
                        <div class="multi-city__body">
                            <div class="multi-city__title-line"></div>
                            <div class="multi-city__text-line"></div>
                            <div class="multi-city__btn-line"></div>
                        </div>
                        <span class="multi-city__label">Dallas</span>
                    </div>
                    <div class="multi-city__frame multi-city__frame--3">
                        <div class="multi-city__bar"></div>
                        <div class="multi-city__body">
                            <div class="multi-city__title-line"></div>
                            <div class="multi-city__text-line"></div>
                            <div class="multi-city__btn-line"></div>
                        </div>
                        <span class="multi-city__label">Phoenix</span>
                    </div>
                    <span class="multi-city__time">48hrs each</span>
                </div>''',
        process_steps=[
            {"title": "Design", "text": "Custom registration page on your domain with your branding. GA4 and Meta Pixel pre-installed for full conversion tracking."},
            {"title": "Track", "text": "Every registration fires a conversion event. Your ad spend is measurable down to the individual signup. Full attribution dashboard."},
            {"title": "Clone", "text": "Running another city? We clone the template, swap venue details, and deploy in 48 hours. Same proven design, new tracking."},
        ],
        includes=[
            "Custom registration page design",
            "Mobile-responsive, sub-1-second load",
            "GA4 + Meta Pixel pre-installed",
            "Confirmation page with conversion tracking",
            "5 to 7 business day turnaround",
            "48-hour clones for additional cities",
            "No per-registrant fees",
            "Full conversion attribution",
        ],
        stats=[
            {"number": "$0", "label": "Per-Registrant Fee"},
            {"number": "48hr", "label": "Clone Turnaround"},
            {"number": "100%", "label": "Ad Attribution"},
        ],
        pricing_html=f'''
                <div class="pricing-table-wrap">
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>First Event Site</td><td>${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,}</td></tr>
                            <tr><td>Additional City / Clone</td><td>${PRICING['event_clone']['low']:,} to ${PRICING['event_clone']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>''',
        faqs=[
            {"question": "Why not use Eventbrite or Splash?", "answer": "Platform registration sites charge per registrant, put their branding on your page, and limit your tracking. Our sites live on your domain with your branding. Every registration fires a conversion event you own."},
            {"question": "What tracking is included?", "answer": "GA4 and Meta Pixel are pre-installed. Every form submission fires a conversion event. You get full attribution from ad impression to registration."},
            {"question": "How fast can you build the first site?", "answer": "5 to 7 business days for a new event site. Additional cities clone in 48 hours."},
            {"question": "Can you also run the ads?", "answer": "Yes. We offer paid social management as a separate service. When we build the site and run the ads together, attribution is seamless."},
        ],
        related_services=[
            {"slug": "ads", "name": "Paid Social", "desc": "Run Meta ad campaigns to fill seats at your events."},
            {"slug": "web-design", "name": "Web Design & Build", "desc": "Need a full company site alongside your event pages?"},
        ],
    )


def build_service_ads():
    """Build individual service page: Paid Social Advertising."""
    _service_page(
        slug="ads",
        title="Paid Social Advertising",
        meta_desc="Facebook and Instagram campaigns with 62% lower ad costs and 2x industry CTR. Custom audience targeting, retargeting, full attribution.",
        headline='62% Lower Ad Costs. <span class="text-accent">2x More Clicks.</span>',
        hero_text="Facebook and Instagram campaign management with custom audience targeting, retargeting, and urgency scheduling. Our clients pay 62% less per click than industry average while getting double the click-through rate.",
        proof_html='''
                <h2>BTL Events Campaign Results</h2>
                <p class="case-study__summary">Reaching physicians with ads is expensive. Most healthcare advertisers pay $3 to $8+ per click. We got it down to $1.50 per click by building custom audiences from the client's own contact database instead of relying on broad targeting.</p>

                <div class="cost-comparison" data-animate style="margin: var(--space-8) 0;">
                    <div class="cost-comparison__bar">
                        <span class="cost-comparison__label">Industry Average</span>
                        <div class="cost-comparison__track">
                            <div class="cost-comparison__fill cost-comparison__fill--competitor" style="width: 0%;" data-width="100%"></div>
                        </div>
                        <span class="cost-comparison__value cost-comparison__value--competitor">$3&ndash;$8+</span>
                    </div>
                    <div class="cost-comparison__bar">
                        <span class="cost-comparison__label">SharpPages</span>
                        <div class="cost-comparison__track">
                            <div class="cost-comparison__fill cost-comparison__fill--sharp" style="width: 0%;" data-width="38%"></div>
                        </div>
                        <span class="cost-comparison__value cost-comparison__value--sharp">$1.50</span>
                    </div>
                </div>

                <p class="case-study__summary">We uploaded the client's physician contact database directly to Facebook, which matched real profiles instead of relying on broad "healthcare" interest targeting. Retargeting kicked in on day 7 for anyone who visited but did not register.</p>''',
        process_steps=[
            {"title": "Audience", "text": "Upload your contact list as a custom audience. Build lookalike audiences and retargeting pools from site visitors."},
            {"title": "Launch", "text": "Run structured campaigns: awareness, retargeting, urgency, countdown. Carousel and static creative with multiple copy variations."},
            {"title": "Optimize", "text": "Weekly performance reports. A/B testing on creative and copy. Full attribution from ad impression to conversion."},
        ],
        includes=[
            "Custom audience upload from your contact list",
            "Facebook + Instagram placements",
            "Carousel and static ad creative",
            "Website visitor retargeting",
            "Urgency schedule with countdown copy",
            "Weekly performance reports",
            "Full conversion attribution",
            "A/B testing on creative and copy",
        ],
        stats=[
            {"number": "62%", "label": "Lower CPC"},
            {"number": "2x", "label": "Industry Avg CTR"},
            {"number": "$1.50", "label": "Cost Per Click"},
        ],
        pricing_html=f'''
                <div class="pricing-table-wrap">
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>Campaign Setup</td><td>${PRICING['ad_setup']['low']:,} to ${PRICING['ad_setup']['high']:,}</td></tr>
                            <tr><td>Monthly Management</td><td>${PRICING['ad_monthly']['low']:,} to ${PRICING['ad_monthly']['high']:,}/mo</td></tr>
                        </tbody>
                    </table>
                </div>
                <p style="color: var(--color-text-muted); font-size: var(--text-sm); margin-top: var(--space-3);">Ad spend is separate and paid directly to Meta. We manage strategy, creative, and optimization.</p>''',
        faqs=[
            {"question": "Do you manage the ad spend budget?", "answer": "No. You pay Meta directly for ad spend. We manage the strategy, audience targeting, creative, and optimization. Our fee covers management only."},
            {"question": "What platforms do you manage?", "answer": "Facebook and Instagram (Meta). If you need Google Ads or LinkedIn, we can discuss, but our strongest results are on Meta."},
            {"question": "How do you get 62% lower costs?", "answer": "Custom audience uploads. Instead of broad interest targeting, we upload your actual contact list. Facebook matches real profiles, so every dollar goes to people who are already in your pipeline."},
            {"question": "What attribution do I get?", "answer": "Full funnel: ad impression to site visit to registration/conversion. We install Meta Pixel and GA4 on your site so every conversion is tracked and attributable."},
        ],
        related_services=[
            {"slug": "events", "name": "Event Sites", "desc": "Build registration pages that convert, then drive traffic with ads."},
            {"slug": "seo", "name": "SEO & Content", "desc": "Organic traffic to complement your paid campaigns."},
        ],
    )


def build_service_audit():
    """Build individual service page: PageSpeed Audit & Fix."""
    _service_page(
        slug="audit",
        title="PageSpeed Audit & Fix",
        meta_desc="Free instant PageSpeed audit. See your scores, SEO gaps, and performance bottlenecks in 30 seconds. Paid fix service available.",
        headline='Find Out What Is <span class="text-accent">Slowing You Down</span>',
        hero_text="Enter your URL and get your PageSpeed scores, SEO checklist, and performance bottlenecks in 30 seconds. Free, no signup required. If your site needs work, we fix it and deliver before/after scores as proof.",
        proof_html='''
                <h2>Try It Right Now</h2>
                <p class="case-study__summary">Our free audit runs your URL through Google PageSpeed Insights (the same tool Google uses to evaluate sites for search ranking) and checks your HTML for common SEO issues.</p>
                <div style="text-align: center; margin: var(--space-8) 0;">
                    <a href="/audit/" class="btn btn--primary btn--lg">Run Your Free Audit</a>
                </div>

                <h3 style="margin-top: var(--space-8);">What a Fix Looks Like</h3>
                <div class="gauge-comparison gauge-comparison--compact" data-animate style="margin-top: var(--space-6);">
                    <div class="gauge-wrapper">
                        <div class="gauge" data-score="45" data-color="red">
                            <svg class="gauge__svg" viewBox="0 0 120 120">
                                <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                <circle class="gauge__fill gauge__fill--red" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                            </svg>
                            <span class="gauge__score" data-target="45">0</span>
                        </div>
                        <span class="gauge__label">Before</span>
                    </div>
                    <div class="gauge-wrapper gauge-wrapper--arrow">
                        <span class="gauge-arrow">&rarr;</span>
                    </div>
                    <div class="gauge-wrapper">
                        <div class="gauge" data-score="95" data-color="green">
                            <svg class="gauge__svg" viewBox="0 0 120 120">
                                <circle class="gauge__bg" cx="60" cy="60" r="54" />
                                <circle class="gauge__fill gauge__fill--green" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="339.29" />
                            </svg>
                            <span class="gauge__score" data-target="95">0</span>
                        </div>
                        <span class="gauge__label">After</span>
                    </div>
                </div>''',
        process_steps=[
            {"title": "Audit", "text": "Run the free audit or request a detailed paid audit. We identify performance bottlenecks, SEO issues, and Core Web Vitals problems."},
            {"title": "Diagnose", "text": "We pinpoint the specific issues: render-blocking resources, oversized images, JavaScript bloat, server response time."},
            {"title": "Fix", "text": "We fix the issues and deliver before/after PageSpeed scores as proof. Often the entry point for a full redesign."},
        ],
        includes=[
            "Free instant audit (PageSpeed + SEO checklist)",
            "Performance bottleneck identification",
            "Before/after PageSpeed scores",
            "Image optimization + compression",
            "Render-blocking resource fixes",
            "Core Web Vitals improvement",
        ],
        stats=[
            {"number": "Free", "label": "Instant Audit"},
            {"number": "30s", "label": "Time to Results"},
            {"number": "90+", "label": "Post-Fix Target"},
        ],
        pricing_html=f'''
                <div class="pricing-table-wrap">
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price</th></tr></thead>
                        <tbody>
                            <tr><td>Free Instant Audit</td><td>$0 (<a href="/audit/">try it now</a>)</td></tr>
                            <tr><td>Detailed Audit + Consult</td><td>$500</td></tr>
                            <tr><td>Audit + Fix</td><td>${PRICING['pagespeed_fix']['low']:,} to ${PRICING['pagespeed_fix']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>''',
        faqs=[
            {"question": "Is the audit really free?", "answer": "Yes. The summary scores and SEO checklist are free with no email required. We ask for your email only if you want the detailed report with prioritized fix recommendations."},
            {"question": "What if my site scores poorly?", "answer": "That is what the fix service is for. We identify the bottlenecks and fix them. You get before/after PageSpeed scores as proof. If your site needs a deeper overhaul, we can discuss a full redesign."},
            {"question": "Can you fix a WordPress site without migrating?", "answer": "We can optimize within WordPress to some extent (image compression, caching, render-blocking fixes), but the biggest gains come from migrating to static HTML. WordPress has inherent overhead that limits how fast it can be."},
        ],
        related_services=[
            {"slug": "redesign", "name": "Redesign & Migration", "desc": "Migrate your site to static HTML for permanent speed gains."},
            {"slug": "web-design", "name": "Web Design & Build", "desc": "Start fresh with a site built for speed from day one."},
        ],
        cta_title="Start With a Free Audit",
        cta_text="Run your site through our free audit. See your PageSpeed score, SEO gaps, and what is fixable. Takes 30 seconds.",
        cta_btn="Get a Free Audit",
        cta_href="/audit/",
    )


def build_all_service_pages():
    """Build all 6 individual service detail pages."""
    build_service_web_design()
    build_service_redesign()
    build_service_seo()
    build_service_events()
    build_service_ads()
    build_service_audit()


def build_pricing():
    """Build pricing page with all 6 service categories, tier cards for site builds, and lead magnet add-on."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Pricing", "/pricing/")

    # Build pricing cards for website design tiers
    cards_html = ""
    for tier in TIERS:
        featured_class = " pricing-card--featured" if tier.get("featured") else ""
        badge_html = ""
        if tier.get("badge"):
            badge_html = f'<span class="pricing-card__badge">{tier["badge"]}</span>'

        features_html = ""
        for feat in tier["features"]:
            features_html += f"<li>{feat}</li>\n"

        cta_href = "/audit/" if "Audit" in tier["cta"] else "/contact/"
        cards_html += f'''
                    <div class="pricing-card{featured_class}">
                        {badge_html}
                        <h3 class="pricing-card__name">{tier["name"]}</h3>
                        <p class="pricing-card__desc">{tier["desc"]}</p>
                        <div class="pricing-card__price">{tier["price_display"]}</div>
                        <p class="pricing-card__price-note">{tier["price_note"]}</p>
                        <ul class="pricing-card__features">
                            {features_html}
                        </ul>
                        <a href="{cta_href}" class="btn btn--primary">{tier["cta"]}</a>
                    </div>'''

    faqs = [
        {
            "question": "Why price ranges instead of fixed numbers?",
            "answer": "Scope varies. A 5-page standard site with a contact form is on the lower end. A 10-page site with custom illustrations, multiple form types, and blog infrastructure is on the higher end. We scope it on the first call and give you a fixed quote before any work starts."
        },
        {
            "question": "What does the lead magnet add-on include?",
            "answer": f"An interactive tool built into your site: a PageSpeed audit, ROI calculator, assessment quiz, or similar. These convert 2-5x better than static contact forms because the visitor gets immediate value before you ask for their email. ${PRICING['lead_magnet_addon']['low']:,} to ${PRICING['lead_magnet_addon']['high']:,} depending on complexity."
        },
        {
            "question": "Are there recurring fees?",
            "answer": "Only if you choose ongoing services (monthly SEO management or monthly ad management). Site builds, redesigns, and audits are one-time flat fees. Hosting on GitHub Pages or Cloudflare Pages is free. You own all files."
        },
        {
            "question": "What if my project does not fit these categories?",
            "answer": "Tell us about your project. We will scope the work, give you a fixed quote, and explain exactly what is included. If it is not a fit, we will tell you."
        },
        {
            "question": "Do you offer payment plans?",
            "answer": "For projects over $5,000, we can split payment into milestones (typically 50% upfront, 50% on delivery). For smaller projects, payment is due on completion."
        },
    ]
    faq_html = generate_faq_html(faqs)

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Flat Pricing. <span class="text-accent">No Hourly Billing.</span></h1>
                <p class="page-header__subtitle">Every project is scoped upfront with a fixed quote. No change orders, no scope creep, no surprises. You own all files when we are done.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2 class="text-center mb-8">Website Design &amp; Build</h2>
                <div class="pricing-grid pricing-grid--four">
                    {cards_html}
                </div>
                <p class="text-center" style="color: var(--color-text-muted); margin-top: var(--space-6); line-height: var(--leading-relaxed);"><strong>Lead magnet add-on:</strong> +${PRICING['lead_magnet_addon']['low']:,} to ${PRICING['lead_magnet_addon']['high']:,}. Interactive audit tools, calculators, or quizzes built into your site. Convert 2-5x better than static contact forms.</p>
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2 class="text-center mb-8">All Services</h2>

                <div class="pricing-table-wrap">
                    <h3>Website Redesign &amp; Migration</h3>
                    <table class="pricing-table">
                        <thead><tr><th>From</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>WordPress / Squarespace / Wix</td><td>${PRICING['redesign_wp_sq_wix']['low']:,} to ${PRICING['redesign_wp_sq_wix']['high']:,}</td></tr>
                            <tr><td>Webflow</td><td>${PRICING['redesign_webflow']['low']:,} to ${PRICING['redesign_webflow']['high']:,}</td></tr>
                            <tr><td>Custom CMS</td><td>${PRICING['redesign_custom_cms']['low']:,} to ${PRICING['redesign_custom_cms']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="pricing-table-wrap">
                    <h3>SEO &amp; Content Strategy</h3>
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>SEO audit</td><td>${PRICING['seo_audit']['low']:,} to ${PRICING['seo_audit']['high']:,}</td></tr>
                            <tr><td>Programmatic SEO buildout</td><td>${PRICING['seo_programmatic']['low']:,} to ${PRICING['seo_programmatic']['high']:,}</td></tr>
                            <tr><td>Monthly SEO management</td><td>${PRICING['seo_monthly']['low']:,} to ${PRICING['seo_monthly']['high']:,}/mo</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="pricing-table-wrap">
                    <h3>Event Registration Sites</h3>
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>First event site</td><td>${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,}</td></tr>
                            <tr><td>Additional city / clone</td><td>${PRICING['event_clone']['low']:,} to ${PRICING['event_clone']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="pricing-table-wrap">
                    <h3>Paid Social Advertising</h3>
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price Range</th></tr></thead>
                        <tbody>
                            <tr><td>Campaign setup</td><td>${PRICING['ad_setup']['low']:,} to ${PRICING['ad_setup']['high']:,}</td></tr>
                            <tr><td>Monthly management</td><td>${PRICING['ad_monthly']['low']:,} to ${PRICING['ad_monthly']['high']:,}/mo</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="pricing-table-wrap">
                    <h3>PageSpeed Audit &amp; Fix</h3>
                    <table class="pricing-table">
                        <thead><tr><th>Service</th><th>Price</th></tr></thead>
                        <tbody>
                            <tr><td>Free instant audit</td><td>$0 (<a href="/audit/">try it now</a>)</td></tr>
                            <tr><td>Detailed audit + consult</td><td>$500</td></tr>
                            <tr><td>Audit + fix</td><td>${PRICING['pagespeed_fix']['low']:,} to ${PRICING['pagespeed_fix']['high']:,}</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <section class="content-section">
            <div class="container text-center">
                <h2 class="mb-4">Pricing Principles</h2>
                <div class="feature-grid" style="grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); text-align: left;">
                    <div class="feature-card">
                        <h3 class="feature-card__title">All Flat Fee</h3>
                        <p class="feature-card__text">No hourly billing. No change orders. Scope defined upfront. If scope changes, you get a new quote before any work happens.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">You Own Everything</h3>
                        <p class="feature-card__text">HTML, CSS, JS files are yours. Host them anywhere. No vendor lock-in. No "you can leave but your site stays."</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">No Recurring Unless Ongoing</h3>
                        <p class="feature-card__text">Site builds are one-time. Hosting is free (GitHub Pages / Cloudflare). Monthly fees only apply to ongoing SEO or ad management.</p>
                    </div>
                </div>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title="Not Sure What You Need?",
    text="Start with a free site audit, or book a call and we will scope the right project together.",
    button_text="Get a Free Audit",
    button_href="/audit/",
)}'''

    html = get_page_wrapper(
        title="Pricing: Flat Fees for Web Design, SEO, Ads",
        description=f"Website builds from ${PRICING['site_landing']['low']:,}. SEO from ${PRICING['seo_audit']['low']}. Event sites from ${PRICING['event_first']['low']:,}. All flat fee, no hourly billing, you own everything.",
        canonical_path="/pricing/",
        body_content=body,
        active_page="/pricing/",
        extra_schema=breadcrumb_schema,
    )
    write_page("pricing/index.html", html)
    ALL_PAGES.append(("/pricing/", 0.8, "monthly"))


def build_work():
    """Build work/portfolio page with 3 case studies: PageSpeed, SEO, Ad campaign."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Work", "/work/")

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Our <span class="text-accent">Work</span></h1>
                <p class="page-header__subtitle">Three projects, three types of proof. PageSpeed scores are public. Search Console data is real. Ad metrics are from live campaigns. Verify anything you want.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="case-study">
                    <span class="case-study__label">PageSpeed Proof</span>
                    <h2 class="case-study__title">getprovyx.com: 398 Pages, 98 PageSpeed Score</h2>
                    <p class="case-study__summary">A 398-page static site built with programmatic SEO. Every page loads in under a second on mobile. Run it through <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">PageSpeed Insights</a> yourself.</p>

                    <div class="case-study__stats">
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">98</span>
                            <span class="case-study__stat-label">Performance</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">95</span>
                            <span class="case-study__stat-label">Accessibility</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">100</span>
                            <span class="case-study__stat-label">Best Practices</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">100</span>
                            <span class="case-study__stat-label">SEO</span>
                        </div>
                    </div>

                    <h3>The Comparison</h3>
                    <p class="case-study__summary">An agency-built competitor site on Webflow (reelist.stream) scores 83 on Performance with a 5.0s Speed Index. Our site scores 98 with a 0.9s Speed Index. Same type of content, same audience. The difference is the build approach: static HTML vs. a platform that adds framework overhead to every page load.</p>

                    <div class="case-study__comparison">
                        <table class="comparison-table">
                            <thead><tr><th>Metric</th><th class="col-sharp">SharpPages (getprovyx.com)</th><th class="col-competitor">Agency / Webflow</th></tr></thead>
                            <tbody>
                                <tr><td>Performance</td><td class="col-sharp">98</td><td class="col-competitor">83</td></tr>
                                <tr><td>Speed Index</td><td class="col-sharp">0.9s</td><td class="col-competitor">5.0s</td></tr>
                                <tr><td>Total Blocking Time</td><td class="col-sharp">30ms</td><td class="col-competitor">280ms</td></tr>
                                <tr><td>Accessibility</td><td class="col-sharp">95</td><td class="col-competitor">92</td></tr>
                                <tr><td>Best Practices</td><td class="col-sharp">100</td><td class="col-competitor">73</td></tr>
                                <tr><td>SEO</td><td class="col-sharp">100</td><td class="col-competitor">100</td></tr>
                                <tr><td>Pages</td><td class="col-sharp">398</td><td class="col-competitor">~50</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="case-study__summary">Both scores are publicly verifiable. Go to <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">pagespeed.web.dev</a>, enter the URLs, and compare.</p>
                </div>
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <div class="case-study">
                    <span class="case-study__label">SEO Proof</span>
                    <h2 class="case-study__title">PE Collective: 363K Impressions in 30 Days</h2>
                    <p class="case-study__summary">A 322-page content site built with programmatic SEO. From near-zero search visibility to 363K impressions in a single month. Average position 8.8 and climbing. <a href="https://pecollective.com" target="_blank" rel="noopener noreferrer">See the live site.</a></p>

                    <div class="case-study__stats">
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">363K</span>
                            <span class="case-study__stat-label">Impressions (30 days)</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">322</span>
                            <span class="case-study__stat-label">Pages Built</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">8.8</span>
                            <span class="case-study__stat-label">Avg Position</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">30 days</span>
                            <span class="case-study__stat-label">Time to Results</span>
                        </div>
                    </div>

                    <h3>How It Works</h3>
                    <p class="case-study__summary">Each page targets a specific search intent with structured content: firm profiles, comparison pages, industry verticals, location pages. The build script generates all 322 pages from data, with unique titles, meta descriptions, schema markup, and internal links on every page.</p>
                    <p class="case-study__summary">The growth curve was steep. Week 1: 2K impressions. Week 2: 15K. Week 3: 30K. By week 4, the site was generating 45K impressions per day. Google indexed the pages quickly because the site loads fast, the content is structured, and the schema markup is correct on every page.</p>
                    <p class="case-study__summary">This is the same programmatic SEO approach we offer as a <a href="/services/seo/">service</a>. The build system, content architecture, and schema patterns are reusable across industries.</p>

                    <h3>Impression Growth</h3>
                    <div class="seo-chart" data-animate>
                        <svg class="seo-chart__svg" viewBox="0 0 600 200" preserveAspectRatio="none">
                            <polyline class="seo-chart__line" points="0,195 150,180 300,150 450,100 600,10" fill="none" />
                        </svg>
                        <div class="seo-chart__labels">
                            <span class="seo-chart__label" data-delay="0">Week 1: 2K</span>
                            <span class="seo-chart__label" data-delay="1">Week 2: 15K</span>
                            <span class="seo-chart__label" data-delay="2">Week 3: 30K</span>
                            <span class="seo-chart__label" data-delay="3">Week 4: 45K/day</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="case-study">
                    <span class="case-study__label">Ad Campaign Proof</span>
                    <h2 class="case-study__title">BTL Events: 62% Lower Ad Costs, 2x More Clicks</h2>
                    <p class="case-study__summary">Multi-city physician event campaign. We built the registration sites and ran the ads together, so every dollar spent was tracked from ad impression to completed registration. The result: our clients spent 62% less per click than the industry average while getting double the click-through rate.</p>

                    <div class="case-study__stats">
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">62%</span>
                            <span class="case-study__stat-label">Lower Ad Costs</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">2x</span>
                            <span class="case-study__stat-label">More Clicks Than Avg</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">48hrs</span>
                            <span class="case-study__stat-label">Per-City Launch</span>
                        </div>
                    </div>

                    <h3>Ad Cost Comparison</h3>
                    <p class="case-study__summary">Reaching physicians with ads is expensive. Most healthcare advertisers pay $3 to $8+ per click. We got it down to $1.50 per click&mdash;62% below the low end of the industry range&mdash;by building custom audiences from the client's own contact database instead of relying on broad targeting.</p>
                    <div class="cost-comparison" data-animate>
                        <div class="cost-comparison__bar">
                            <span class="cost-comparison__label">Industry Average</span>
                            <div class="cost-comparison__track">
                                <div class="cost-comparison__fill cost-comparison__fill--competitor" style="width: 0%;" data-width="100%"></div>
                            </div>
                            <span class="cost-comparison__value cost-comparison__value--competitor">$3&ndash;$8+</span>
                        </div>
                        <div class="cost-comparison__bar">
                            <span class="cost-comparison__label">SharpPages</span>
                            <div class="cost-comparison__track">
                                <div class="cost-comparison__fill cost-comparison__fill--sharp" style="width: 0%;" data-width="38%"></div>
                            </div>
                            <span class="cost-comparison__value cost-comparison__value--sharp">$1.50</span>
                        </div>
                    </div>

                    <h3>How We Did It</h3>
                    <p class="case-study__summary">We uploaded the client's physician contact database directly to Facebook, which matched real profiles instead of relying on broad "healthcare" interest targeting. That's why the cost per click was so low&mdash;we were only paying to reach people who were already in the pipeline.</p>
                    <p class="case-study__summary">Retargeting kicked in on day 7: anyone who visited the registration page but didn't sign up saw follow-up ads with the full event agenda and countdown messaging. The 25-day campaign progressed from awareness to urgency, with copy updates matching the event timeline.</p>

                    <h3>The Replication Model</h3>
                    <p class="case-study__summary">The first city took 5 to 7 days for the site build. Each additional city cloned in 48 hours with fresh venue details, local contact lists, and separate tracking. The design, tracking architecture, and proven page structure carried over. By the third city, the per-event cost and setup time were a fraction of the first.</p>
                    <p class="case-study__summary">Read about our <a href="/services/events/">event registration</a> and <a href="/services/ads/">paid social</a> services, or see <a href="/pricing/">pricing</a> for what campaigns like this cost.</p>
                </div>
            </div>
        </section>

{generate_cta_section(
    title="Want Results Like These?",
    text="Start with a free site audit to see where you stand, or book a call to scope your project.",
    button_text="Get a Free Audit",
    button_href="/audit/",
)}'''

    html = get_page_wrapper(
        title="Our Work: PageSpeed, SEO, and Ad Campaign Proof",
        description="98 PageSpeed score across 398 pages. 363K impressions in 30 days from programmatic SEO. 2x industry CTR on ad campaigns. See the proof.",
        canonical_path="/work/",
        body_content=body,
        active_page="/work/",
        extra_schema=breadcrumb_schema,
    )
    write_page("work/index.html", html)
    ALL_PAGES.append(("/work/", 0.8, "monthly"))


def build_about():
    """Build about page with broader performance web studio positioning."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("About", "/about/")

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">About <span class="text-accent">SharpPages</span></h1>
                <p class="page-header__subtitle">A performance web studio that competes with agencies on outcomes, not hours. One person, full stack, measurable results.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="about-intro">
                    <div>
                        <div style="background: var(--color-card); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-8); text-align: center;">
                            <h3 style="margin-bottom: var(--space-2);">Rome Thorndike</h3>
                            <p style="color: var(--color-text-muted); font-size: var(--text-sm);">Founder, SharpPages</p>
                        </div>
                    </div>
                    <div class="about-intro__text">
                        <h2>Data + Marketing + Engineering</h2>
                        <p>I spent a decade in enterprise SaaS before starting SharpPages. I sold software at <a href="https://www.salesforce.com/" target="_blank" rel="noopener noreferrer">Salesforce</a>, ran customer success at Microsoft, and helped scale a data startup (Datajoy) that was acquired by <a href="https://www.databricks.com/" target="_blank" rel="noopener noreferrer">Databricks</a>. Along the way, I earned my MBA at <a href="https://haas.berkeley.edu/" target="_blank" rel="noopener noreferrer">UC Berkeley Haas</a>.</p>
                        <p>SharpPages grew out of a pattern I kept seeing: businesses paying agencies $150 to $300 per hour for sites that score 70 on PageSpeed, take 8 weeks to deliver, and come with change orders for every revision. Then those same businesses wonder why their site does not rank and their ads do not convert.</p>
                        <p>I started building sites the way I thought they should be built: static HTML that loads in under a second, programmatic SEO that generates hundreds of targeted pages, and ad campaigns with full attribution from impression to conversion. The results spoke for themselves. A 98 PageSpeed score across 398 pages. 363K impressions in 30 days from programmatic SEO. 2x industry CTR on paid social campaigns.</p>
                        <p>Agencies staff projects across junior designers, developers, and project managers. Every handoff introduces delay and information loss. SharpPages is one person doing all of it: site architecture, design, development, SEO, content, and ad management. Faster delivery, tighter feedback loops, and zero "let me check with the developer and get back to you."</p>
                        <ul class="credentials-list">
                            <li>UC Berkeley, Haas School of Business (MBA)</li>
                            <li>Databricks (via Datajoy acquisition)</li>
                            <li>Microsoft, Customer Success</li>
                            <li>Salesforce, Enterprise Sales</li>
                            <li>Snapdocs, GTM Strategy</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2 class="text-center mb-8">Why This Approach Wins</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3 class="feature-card__title">Speed Matters More Than Agencies Admit</h3>
                        <p class="feature-card__text">Google uses Core Web Vitals as a ranking factor. A 98 PageSpeed score means your site loads in under a second. Most agency-built sites on WordPress or Webflow score 60 to 80. The performance gap shows up in search rankings, bounce rates, and conversion rates.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">SEO at Scale Requires Engineering</h3>
                        <p class="feature-card__text">Building 300+ pages of keyword-targeted content requires build scripts, data structures, and template systems. Agencies hire copywriters to produce 4 blog posts per month. We generate hundreds of pages from structured data, each with unique content, schema markup, and internal links.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">Flat Fees Align Incentives</h3>
                        <p class="feature-card__text">Agencies profit from scope creep and change orders. Hourly billing rewards slow work. Flat fees mean I am incentivized to scope correctly, build efficiently, and ship on time. If the scope changes, you get a new quote before any extra work starts.</p>
                    </div>
                </div>
                <p style="color: var(--color-text-muted); text-align: center; margin-top: var(--space-8); line-height: var(--leading-relaxed);">See the proof in our <a href="/work/">case studies</a>, review <a href="/services/">services and pricing</a>, or <a href="/audit/">run a free audit</a> on your current site.</p>
            </div>
        </section>

{generate_cta_section(
    title="Ready to Work Together?",
    text="Tell us about your site. We will review it, discuss your goals, and send a fixed quote within two business days.",
    button_text="Let's Build It",
)}'''

    html = get_page_wrapper(
        title="About SharpPages: Performance Web Studio",
        description="SharpPages is a performance web studio built by Rome Thorndike (UC Berkeley Haas MBA, ex-Salesforce, Microsoft, Databricks). Fast sites, real SEO, flat fees.",
        canonical_path="/about/",
        body_content=body,
        active_page="/about/",
        extra_schema=breadcrumb_schema,
    )
    write_page("about/index.html", html)
    ALL_PAGES.append(("/about/", 0.7, "monthly"))


def build_contact():
    """Build contact page with Formspree form and honeypot."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Contact", "/contact/")

    action_url = f"https://formspree.io/f/{FORMSPREE_ID}"

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Book a <span class="text-accent">Call</span></h1>
                <p class="page-header__subtitle">Tell us about your event. We will scope it, price it, and get back to you within one business day.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="contact-grid">
                    <div>
                        <form class="form" action="{action_url}" method="POST">
                            <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                            <div class="form__row">
                                <div class="form__group">
                                    <label class="form__label" for="contact-name">Name</label>
                                    <input class="form__input" type="text" id="contact-name" name="name" required>
                                </div>
                                <div class="form__group">
                                    <label class="form__label" for="contact-email">Email</label>
                                    <input class="form__input" type="email" id="contact-email" name="email" required>
                                </div>
                            </div>
                            <div class="form__group">
                                <label class="form__label" for="contact-company">Company</label>
                                <input class="form__input" type="text" id="contact-company" name="company">
                            </div>
                            <div class="form__group">
                                <label class="form__label" for="contact-event-type">Event Type</label>
                                <select class="form__input" id="contact-event-type" name="event_type">
                                    <option value="">Select one...</option>
                                    <option value="physician-dinner">Physician Dinner / KOL Event</option>
                                    <option value="conference">Conference or Summit</option>
                                    <option value="product-launch">Product Launch / Demo Day</option>
                                    <option value="workshop">Workshop or Training</option>
                                    <option value="networking">Networking Event</option>
                                    <option value="recurring">Recurring Event Series</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                            <div class="form__group">
                                <label class="form__label" for="contact-message">Tell us about your event</label>
                                <textarea class="form__textarea" id="contact-message" name="message" rows="5" placeholder="Event date, location, target audience, and anything else that helps us scope the work."></textarea>
                            </div>
                            <p style="font-size: var(--text-xs); color: var(--color-text-subtle); margin-bottom: var(--space-4);">By submitting this form, you agree to our <a href="/privacy/">Privacy Policy</a>.</p>
                            <button type="submit" class="btn btn--primary btn--lg form__submit">Send Message</button>
                        </form>
                    </div>
                    <div>
                        <div class="contact-info__item">
                            <p class="contact-info__label">Response Time</p>
                            <p class="contact-info__value">Within one business day. Usually faster.</p>
                        </div>
                        <div class="contact-info__item">
                            <p class="contact-info__label">What Happens Next</p>
                            <p class="contact-info__value">We review your event details, ask a few follow-up questions, and send a fixed quote with a timeline. No pressure, no sales pitch. If we are the right fit, we start.</p>
                        </div>
                        <div class="contact-info__item">
                            <p class="contact-info__label">Typical Project Timeline</p>
                            <p class="contact-info__value">5 to 7 business days for a new site build. 48 hours for a clone. Ad campaigns launch within 3 days of site approval.</p>
                        </div>
                        <div class="contact-info__item">
                            <p class="contact-info__label">Learn More First?</p>
                            <p class="contact-info__value">Read about our <a href="/services/">services</a>, check <a href="/pricing/">pricing</a>, or see a <a href="/work/">case study</a> before reaching out.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Contact SharpPages: Let's Build Your Site",
        description="Tell us about your event. We will scope it, price it, and get back to you within one business day. No per-registrant fees, no platform lock-in.",
        canonical_path="/contact/",
        body_content=body,
        active_page="/contact/",
        extra_schema=breadcrumb_schema,
    )
    write_page("contact/index.html", html)
    ALL_PAGES.append(("/contact/", 0.8, "monthly"))


def build_privacy():
    """Build privacy policy page."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Privacy Policy", "/privacy/")

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Privacy Policy</h1>
                <p class="page-header__subtitle">Last updated: January {COPYRIGHT_YEAR}</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="legal-content">
                    <p>SharpPages ("we," "us," or "our") operates the website sharppages.com. This page informs you of our policies regarding the collection, use, and disclosure of personal information when you use our site.</p>

                    <h2>Information We Collect</h2>
                    <p>When you submit our contact form, we collect the information you provide: your name, email address, company name, event type, and message. This information is processed through Formspree, a third-party form handling service.</p>
                    <p>We do not collect information from you unless you actively submit it through our contact form.</p>

                    <h2>Analytics</h2>
                    <p>We use Google Analytics 4 (GA4) to understand how visitors use our site. GA4 collects anonymous usage data including pages visited, time on site, and referring sources. This data is aggregated and cannot identify individual visitors.</p>
                    <p>Analytics tracking is subject to your consent preference. You can accept or deny analytics cookies using the consent banner when you first visit the site. Your preference is stored locally in your browser and respected on subsequent visits.</p>

                    <h2>Cookies</h2>
                    <p>We use the following cookies:</p>
                    <ul>
                        <li><strong>Analytics cookies</strong> (GA4): Set only if you consent. Used to measure site traffic and usage patterns.</li>
                        <li><strong>Consent preference</strong>: Stored in your browser's localStorage to remember your cookie choice. Not a tracking cookie.</li>
                    </ul>
                    <p>We do not use advertising cookies on sharppages.com. Our Meta Pixel and ad tracking are used only on client event registration sites, not on this marketing site.</p>

                    <h2>How We Use Your Information</h2>
                    <p>Information submitted through our contact form is used to:</p>
                    <ul>
                        <li>Respond to your inquiry about our services</li>
                        <li>Scope and price the work you described</li>
                        <li>Follow up on your event marketing needs</li>
                    </ul>
                    <p>We do not sell, rent, or share your personal information with third parties for marketing purposes.</p>

                    <h2>Third-Party Services</h2>
                    <ul>
                        <li><strong>Formspree</strong>: Processes form submissions. <a href="https://formspree.io/legal/privacy-policy/" target="_blank" rel="noopener noreferrer">Formspree Privacy Policy</a></li>
                        <li><strong>Google Analytics 4</strong>: Provides site analytics. <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google Privacy Policy</a></li>
                        <li><strong>GitHub Pages</strong>: Hosts this website. <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub Privacy Statement</a></li>
                        <li><strong>Google Fonts</strong>: Serves web fonts. <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google Privacy Policy</a></li>
                    </ul>

                    <h2>Data Retention</h2>
                    <p>Contact form submissions are retained for as long as necessary to respond to your inquiry and fulfill any resulting service agreement. You may request deletion of your data at any time by contacting us.</p>

                    <h2>Your Rights</h2>
                    <p>You have the right to:</p>
                    <ul>
                        <li>Access the personal information we hold about you</li>
                        <li>Request correction of inaccurate information</li>
                        <li>Request deletion of your information</li>
                        <li>Withdraw consent for analytics tracking (via the consent banner)</li>
                    </ul>

                    <h2>Children's Privacy</h2>
                    <p>Our site is not directed at individuals under the age of 18. We do not knowingly collect personal information from children.</p>

                    <h2>Changes to This Policy</h2>
                    <p>We may update this privacy policy from time to time. Changes will be posted on this page with an updated revision date.</p>

                    <h2>Contact</h2>
                    <p>If you have questions about this privacy policy, contact us through our <a href="/contact/">contact page</a>.</p>
                </div>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Privacy Policy",
        description="SharpPages privacy policy. How we collect, use, and protect your information when you visit sharppages.com or submit our contact form.",
        canonical_path="/privacy/",
        body_content=body,
        extra_schema=breadcrumb_schema,
    )
    write_page("privacy/index.html", html)
    ALL_PAGES.append(("/privacy/", 0.3, "yearly"))


def build_terms():
    """Build terms of service page."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Terms of Service", "/terms/")

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Terms of Service</h1>
                <p class="page-header__subtitle">Last updated: January {COPYRIGHT_YEAR}</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="legal-content">
                    <p>These terms govern your use of the sharppages.com website ("Site") operated by SharpPages ("we," "us," or "our"). By accessing the Site, you agree to these terms.</p>

                    <h2>Services</h2>
                    <p>SharpPages provides done-for-you event registration website builds, paid social media ad campaign management, and tracking/analytics setup. Services are scoped, quoted, and agreed upon individually for each client engagement.</p>
                    <p>This Site is a marketing website describing our services. It is not a SaaS platform, does not provide self-service tools, and does not process payments.</p>

                    <h2>Use of This Site</h2>
                    <p>You may use this Site to learn about our services and to contact us through our contact form. You may not:</p>
                    <ul>
                        <li>Use the Site for any unlawful purpose</li>
                        <li>Attempt to gain unauthorized access to any part of the Site</li>
                        <li>Submit false or misleading information through our contact form</li>
                        <li>Scrape, copy, or redistribute the content of this Site without permission</li>
                    </ul>

                    <h2>Intellectual Property</h2>
                    <p>All content on this Site, including text, design, logos, and code, is owned by SharpPages and protected by applicable intellectual property laws. You may not reproduce, distribute, or create derivative works from this content without written permission.</p>

                    <h2>Client Work</h2>
                    <p>Event registration sites built by SharpPages are custom deliverables for each client. Upon full payment, clients receive ownership of their site's HTML, CSS, and JavaScript files. SharpPages retains the right to reference anonymized project details in our portfolio.</p>

                    <h2>Disclaimer</h2>
                    <p>This Site is provided "as is" without warranties of any kind, either express or implied. We do not guarantee that the Site will be error-free or uninterrupted.</p>
                    <p>Our portfolio and case studies describe real project outcomes. Results vary by event type, audience size, ad budget, and market conditions. Past performance does not guarantee future results.</p>

                    <h2>Limitation of Liability</h2>
                    <p>To the fullest extent permitted by law, SharpPages shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of this Site.</p>

                    <h2>Third-Party Links</h2>
                    <p>This Site may contain links to third-party websites. We are not responsible for the content or practices of those sites.</p>

                    <h2>Changes to These Terms</h2>
                    <p>We may update these terms from time to time. Changes will be posted on this page. Continued use of the Site after changes constitutes acceptance of the updated terms.</p>

                    <h2>Governing Law</h2>
                    <p>These terms are governed by the laws of the State of California, without regard to conflict of law provisions.</p>

                    <h2>Contact</h2>
                    <p>Questions about these terms? Contact us through our <a href="/contact/">contact page</a>.</p>
                </div>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Terms of Service",
        description="SharpPages terms of service. Rules governing use of sharppages.com and our event registration site build services.",
        canonical_path="/terms/",
        body_content=body,
        extra_schema=breadcrumb_schema,
    )
    write_page("terms/index.html", html)
    ALL_PAGES.append(("/terms/", 0.3, "yearly"))


# =============================================================================
# ICP PAGES
# =============================================================================

from _icp_data import get_icp_pages
ICP_PAGES = get_icp_pages(PRICING)


def build_icp_page(icp):
    """Build a single ICP industry page."""
    slug = icp["slug"]
    page_path = f"/for/{slug}/"

    crumbs = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": "Industries", "url": BASE_URL + "/for/" + slug + "/"},
        {"name": icp["name"], "url": BASE_URL + page_path},
    ]
    breadcrumb_nav = get_breadcrumb_html(crumbs)
    breadcrumb_schema = get_breadcrumb_schema(crumbs)

    # Pain points
    pain_html = ""
    for p in icp["pain_points"]:
        pain_html += f'<p class="content-section__text" style="color: var(--color-text-muted); line-height: var(--leading-relaxed); margin-bottom: var(--space-4);">{p}</p>\n'

    # Workflow steps
    workflow_html = '<div class="process-steps">\n'
    for i, step in enumerate(icp["workflow"], 1):
        workflow_html += f'''''<div class="process-step">
                            <div class="process-step__number">{i}</div>
                            <div class="process-step__content"><p>{step}</p></div>
                        </div>\n'''''
    workflow_html += '</div>'

    # Outbound links
    outbound_html = ""
    for link in icp.get("outbound_links", []):
        outbound_html += f' <a href="{link["url"]}" target="_blank" rel="noopener noreferrer">{link["text"]}</a>.'

    # Deep dive paragraphs
    deep_dive_html = ""
    for p in icp.get("deep_dive", []):
        deep_dive_html += f'<p style="color: var(--color-text-muted); line-height: var(--leading-relaxed); margin-bottom: var(--space-4);">{p}</p>\n'

    faq_html = generate_faq_html(icp["faqs"])

    body = f'''''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">{icp["h1"]}</h1>
                <p class="page-header__subtitle">{icp["intro"]}</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2>The Problem</h2>
                {pain_html}
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2>Why {icp["name"]} Need a Different Approach</h2>
                {deep_dive_html}
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2>How We Work with {icp["name"]}</h2>
                {workflow_html}
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2>Pricing</h2>
                <p style="color: var(--color-text-muted); line-height: var(--leading-relaxed); margin-bottom: var(--space-4);">{icp["pricing_context"]}</p>
                <p style="color: var(--color-text-muted); line-height: var(--leading-relaxed); margin-bottom: var(--space-4);">All flat fee. No hourly billing. See full details on our <a href="/pricing/">pricing page</a>.</p>
                <p style="color: var(--color-text-muted); line-height: var(--leading-relaxed);">Learn more about our <a href="/services/">services</a>, see <a href="/work/">proof of results</a>, or <a href="/audit/">run a free audit</a> on your current site.{outbound_html}</p>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title=f"Ready to Upgrade Your {icp['name']} Web Presence?",
    text="Start with a free site audit, or book a call and we will scope the right project together.",
    button_text="Get a Free Audit",
    button_href="/audit/",
)}'''''

    html = get_page_wrapper(
        title=icp["title"],
        description=icp["description"],
        canonical_path=page_path,
        body_content=body,
        extra_schema=breadcrumb_schema,
    )
    write_page(f"for/{slug}/index.html", html)
    ALL_PAGES.append((page_path, 0.8, "monthly"))


def build_all_icp_pages():
    """Build all ICP industry pages."""
    for icp in ICP_PAGES:
        build_icp_page(icp)


# =============================================================================
# BLOG
# =============================================================================

BLOG_ARTICLES = [
    {
        "slug": "event-registration-page-losing-signups",
        "title": "Why Your Event Registration Page Is Losing Signups",
        "description": "Most event registration pages lose signups before visitors finish scrolling. Here are the conversion killers and how to fix them.",
        "h1": "Why Your Event Registration Page Is Losing Signups",
        "author": "Rome Thorndike",
        "sections": [
            {
                "heading": "The Registration Page Is Your Conversion Funnel",
                "content": """<p>Every event marketer knows the funnel: awareness, interest, registration. The registration page is where interest becomes action. And for most events, it is also where the funnel leaks the worst.</p>
<p>The problem is not traffic. Ads are running, emails are going out, the event details are solid. The problem is the page itself. Visitors land, scroll for a few seconds, and leave. They were interested enough to click, but the page did not close the deal.</p>
<p>After building registration sites for medical device dinners, pharma speaker programs, and B2B SaaS roadshows, patterns emerge. The same mistakes show up across industries, and they are all fixable.</p>""",
            },
            {
                "heading": "The URL Problem",
                "content": """<p>When your registration page lives on eventbrite.com, splash.that, or lu.ma, you are borrowing credibility instead of building it. The URL is the first thing a sophisticated attendee notices, and it signals whether this is a premium event or a last-minute setup.</p>
<p>For a $500/plate investor dinner or a physician KOL event at a five-star hotel, the URL matters. yourcompany.com/event says "we planned this." eventbrite.com/e/some-long-string says "we found a free tool."</p>
<p>Custom domains are cheap. GitHub Pages hosting is free. The technical barrier to putting your event on your own domain is about 2 hours of work. The perception difference is significant.</p>""",
            },
            {
                "heading": "No Tracking, No Attribution",
                "content": """<p>If you cannot answer "which ad produced which registrations," your event marketing is flying blind. Most event pages are either missing a <a href="https://www.facebook.com/business/tools/meta-pixel" target="_blank" rel="noopener noreferrer">Meta Pixel</a> entirely, or the pixel is installed but not firing conversion events.</p>
<p>The difference matters. A pixel that tracks PageView tells you how many people visited. A pixel that fires a Lead event on the confirmation page tells you how many registered and lets Meta optimize your ads toward people who are likely to register. Without the Lead event, your ad campaign is optimizing for clicks, not conversions.</p>
<p><a href="https://analytics.google.com/" target="_blank" rel="noopener noreferrer">GA4</a> adds another layer: traffic sources, time on page, bounce rate, device breakdown. You learn that 70% of your physician audience visits on mobile but your registration form is unusable below 768px. That is an actionable insight, and you only get it with tracking installed.</p>""",
            },
            {
                "heading": "Mobile Is Not Optional",
                "content": """<p>More than half of event page traffic comes from mobile devices. The physician who sees your Facebook ad is scrolling their phone between patients. The conference attendee who gets your email opens it on their phone during a commute.</p>
<p>If the registration form is hard to fill out on mobile, if the text is too small, if the page takes 5 seconds to load over a cellular connection, you lose them. They intended to register. The page made it too hard.</p>
<p>Test your registration page on a phone. Actually fill out the form. Time the page load over LTE. If any of it feels clunky, your visitors feel it too, and they have less patience than you do.</p>""",
            },
            {
                "heading": "Too Many Fields Kill Conversions",
                "content": """<p>Every field on your registration form is a decision point. Name and email are easy. Company and title are reasonable. But when you add phone, dietary restrictions, session preferences, how-did-you-hear-about-us, and a 200-word text box, each additional field chips away at completion rates.</p>
<p>For most events, you need: name, email, company, and an optional message field. That is it. You can collect dietary preferences and session selections in a follow-up email after they have committed to attending.</p>
<p>The goal of the registration page is registration. Not data collection, not market research, not CRM enrichment. Get the commitment first. Collect the details later.</p>""",
            },
            {
                "heading": "Missing Social Proof",
                "content": """<p>Why should someone register for your event? "Because we are hosting it" is not a compelling answer. Visitors need evidence that the event is worth their time.</p>
<p>Speaker credentials. Past event attendance numbers. Testimonials from previous attendees. Sponsor logos. A specific, detailed agenda. These elements turn "this might be interesting" into "I need to be there."</p>
<p>The more specific the proof, the more persuasive. "Join our event" is generic. "Harvard KOL presenting peer-reviewed outcomes across five treatment platforms, followed by hands-on demonstrations and a custom revenue model for your practice" tells the visitor exactly what they are getting.</p>""",
            },
            {
                "heading": "Page Speed Kills or Converts",
                "content": """<p>A static HTML registration page loads in under 1 second on most connections. A WordPress page with a form plugin, analytics scripts, and a slider loads in 3 to 6 seconds. Research from Google shows that 53% of mobile visits are abandoned if a page takes longer than 3 seconds to load.</p>
<p>For event registration, page speed compounds with intent decay. The person who clicked your Facebook ad had enough interest to tap. Every second of loading time erodes that interest. By the time a slow page finally renders, they have already swiped back to their feed.</p>
<p>Static HTML sites hosted on GitHub Pages or Cloudflare load fast everywhere because the files are served from a CDN with no server-side processing. There is no database query, no PHP execution, no plugin overhead. The browser downloads a small HTML file and renders it immediately. For event pages that exist to capture a single registration, this speed advantage translates directly into more conversions.</p>""",
            },
            {
                "heading": "The Fix Is Not Complicated",
                "content": """<p>A registration page that converts needs five things: your own domain, proper tracking, mobile-responsive design, a short registration form, and social proof. None of these are technically difficult. The challenge is that most event teams do not have a web developer on staff, and by the time they brief an agency, the event is 2 weeks away.</p>
<p>That is the gap SharpPages fills. We build <a href="/services/">custom registration sites</a> in 5 to 7 business days with tracking pre-installed, mobile-responsive design, and copy that converts. See our <a href="/work/">case study</a> for an example, or check <a href="/pricing/">pricing</a> for what it costs.</p>""",
            },
        ],
        "faqs": [
            {"question": "What is a good conversion rate for an event registration page?", "answer": "For targeted traffic (custom audience ads, email list sends), 15 to 30% is a strong registration rate. For cold traffic, 5 to 10% is typical. If you are below these benchmarks, the page itself is likely the bottleneck."},
            {"question": "Should I use a multi-step form or a single-page form?", "answer": "For events with fewer than 5 registration fields, a single-page form works best. Multi-step forms add complexity without improving conversions unless you have 8 or more fields that cannot be reduced."},
            {"question": "How important is page load speed for registration pages?", "answer": "Critical. Every additional second of load time reduces conversions by roughly 7% according to research from Google and Akamai. A static HTML page loads in under 1 second. A WordPress page with 15 plugins loads in 4 to 6 seconds. The math is not subtle."},
        ],
    },
    {
        "slug": "eventbrite-vs-custom-event-sites",
        "title": "Eventbrite vs Custom Event Sites: What Converts Better",
        "description": "Comparing Eventbrite pages with custom event registration sites. Branding, tracking, conversions, and total cost of ownership.",
        "h1": "Eventbrite vs Custom Event Sites: What Converts Better",
        "author": "Rome Thorndike",
        "sections": [
            {
                "heading": "Two Approaches, Same Goal",
                "content": """<p>Eventbrite is the default choice for event registration because it is fast and free to start. Create an event, share the link, collect RSVPs. For a casual meetup or a free community event, that works fine.</p>
<p>For a premium event where the registration page represents your brand, where ad dollars are driving traffic, and where you need to track which campaigns produce registrations, the limitations add up fast.</p>
<p>This is not a hit piece on Eventbrite. It is a good product for what it is built to do. The question is whether what it is built to do matches what you need.</p>""",
            },
            {
                "heading": "Branding and Perception",
                "content": """<p>An Eventbrite page looks like an Eventbrite page. The layout, the URL (eventbrite.com/e/...), the footer, the sidebar with "other events you might like." Your event is presented inside someone else's platform, surrounded by their branding and their recommendations.</p>
<p>For a tech meetup, nobody cares. For a medical device company hosting a physician dinner at the Ritz-Carlton, it matters. The registration page sets expectations for the event itself. Premium events deserve premium registration experiences.</p>
<p>A custom site on your domain, with your logo, your colors, and zero third-party branding, communicates that you planned this event deliberately. It is a small detail that sophisticated attendees notice.</p>""",
            },
            {
                "heading": "Tracking and Attribution",
                "content": """<p>Eventbrite offers built-in analytics: page views, ticket sales, referral sources. For basic events, that is sufficient. But if you are running <a href="https://www.facebook.com/business/tools/ads-manager" target="_blank" rel="noopener noreferrer">Facebook ad campaigns</a> with custom audiences and retargeting, you need pixel-level tracking.</p>
<p>Installing a Meta Pixel on an Eventbrite page is possible but limited. You cannot fire custom conversion events on the confirmation page. You cannot track the full registration funnel. <a href="https://analytics.google.com/" target="_blank" rel="noopener noreferrer">GA4</a> integration is similarly constrained.</p>
<p>On a custom site, you control every line of code. The pixel fires a Lead event when someone completes registration. GA4 tracks the full journey. Your ad platform can optimize for actual registrations, not page views. The data difference compounds over the life of a campaign.</p>""",
            },
            {
                "heading": "Cost Comparison",
                "content": f"""<p>Eventbrite is free for free events. For paid events, fees range from 3.7% + $1.79 per ticket (Essentials) to 6.95% + $1.79 (Professional). A $50 ticket event with 200 registrants costs $997 to $1,937 in fees.</p>
<p>A custom registration site costs ${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,} as a one-time build. No per-registrant fees. No percentage of ticket sales. You own the site and can reuse it for future events.</p>
<p>For free events, Eventbrite's cost advantage is clear. For paid events with 100+ registrants, or for recurring events where you reuse the template, a custom site pays for itself quickly. The break-even is usually around the second or third event when template cloning eliminates the rebuild cost.</p>""",
            },
            {
                "heading": "Customization and Control",
                "content": """<p>Eventbrite gives you a template with some customization options: banner image, description text, ticket types, FAQ section. You work within their layout framework.</p>
<p>A custom site gives you full control. Multi-section pages with speaker bios, venue details, agenda breakdowns, sponsor logos, embedded maps, and custom form fields. You decide the layout, the flow, and the messaging. Nothing is dictated by a template.</p>
<p>For simple events, Eventbrite's constraints are not a problem. For complex events with specific branding requirements, compliance review, or multi-track agendas, the template becomes a limitation.</p>""",
            },
            {
                "heading": "Data Ownership and Portability",
                "content": """<p>Eventbrite owns your event page. If you cancel your account or the platform changes its terms, your event history and page designs go with it. The registrant data exports as a CSV, but the page itself is not portable.</p>
<p>A custom site is a set of HTML, CSS, and JavaScript files that you own. Host them anywhere: GitHub Pages, Netlify, Cloudflare Pages, or your own server. Move providers without rebuilding. Archive past events as static files that load forever without a platform subscription. The files are yours.</p>
<p>For companies that run events as a core part of their marketing, data portability matters. Your registration pages are marketing assets. Treating them as disposable platform pages means rebuilding from scratch every time you switch tools.</p>""",
            },
            {
                "heading": "When Eventbrite Makes Sense",
                "content": """<p>Use Eventbrite if your event is free or low-cost, your branding requirements are minimal, you do not need pixel-level ad tracking, and you want to launch in 15 minutes. Community meetups, casual networking events, and open houses fit well.</p>
<p>The platform handles payment processing, email confirmations, and basic analytics out of the box. If those features solve your problem, the simplicity is valuable.</p>""",
            },
            {
                "heading": "The Reusability Factor",
                "content": """<p>One advantage of custom sites that platform comparisons miss: a custom registration site is a template you own. The first build takes 5 to 7 days. Every subsequent event in the same format clones from that template in 48 hours. Swap the venue, date, speakers, and local details. The design, tracking, and conversion-optimized layout carry forward.</p>
<p>Eventbrite requires rebuilding the page for each event. The platform stores your past events, but each new one starts from a blank form. Splash offers templates within their platform, but you are locked into their ecosystem and pricing tier. A custom site template lives in your GitHub repository. No vendor lock-in. No recurring platform fees. Clone it as many times as you need.</p>""",
            },
            {
                "heading": "When a Custom Site Makes Sense",
                "content": """<p>Use a custom site if your event represents your brand, you are spending money on ad campaigns, you need precise conversion tracking, or you run recurring events across multiple markets.</p>
<p>Physician dinners, investor presentations, product launches, conference registrations, and any event where the registration experience is part of the marketing. These are the use cases where the investment in a <a href="/services/">custom registration site</a> pays for itself in better attribution, higher conversion rates, and reusable templates.</p>
<p>See our <a href="/pricing/">pricing</a> for the full breakdown, or look at a <a href="/work/">real project example</a>.</p>""",
            },
        ],
        "faqs": [
            {"question": "Can I use Eventbrite's payment processing on a custom site?", "answer": "Not directly. If you need payment processing, you can use Stripe, Square, or another payment provider on your custom site. For free registration events, no payment processing is needed at all."},
            {"question": "Is it possible to migrate from Eventbrite to a custom site mid-campaign?", "answer": "Yes. We can build the custom site while your Eventbrite page is still live, then redirect the URL once the new site is ready. No registration data is lost in the transition."},
            {"question": "How long does it take to build a custom registration site?", "answer": "5 to 7 business days for a new site. 48 hours for a clone of an existing template. Eventbrite is faster to launch, but the custom site is reusable for every future event."},
        ],
    },
    {
        "slug": "facebook-retargeting-fills-event-seats",
        "title": "How Facebook Retargeting Fills Event Seats",
        "description": "A practical guide to Facebook retargeting for event registration. Custom audiences, pixel setup, urgency schedules, and campaign structure.",
        "h1": "How Facebook Retargeting Fills Event Seats",
        "author": "Rome Thorndike",
        "sections": [
            {
                "heading": "Most Event Ads Stop at Awareness",
                "content": """<p>A typical event ad campaign goes like this: create a Facebook post, boost it, hope people see it and register. When the campaign ends, you look at reach and impressions but have no idea how many registrations the ads actually produced.</p>
<p>Retargeting fixes the biggest leak in that funnel. Someone sees your ad, clicks through to the registration page, and then... does not register. Life happens. They got interrupted. They wanted to check the date. They planned to come back later.</p>
<p>Without retargeting, that interested visitor is gone. With retargeting, they see a follow-up ad the next day with the full event agenda. Then another ad 3 days later with a countdown. Then a final "last seats" message. Each touchpoint increases the probability of registration.</p>""",
            },
            {
                "heading": "How Retargeting Works (Technically)",
                "content": """<p>The <a href="https://www.facebook.com/business/tools/meta-pixel" target="_blank" rel="noopener noreferrer">Meta Pixel</a> is a small piece of JavaScript installed on your event registration page. When someone visits the page, the pixel fires and adds them to an audience pool in your ad account.</p>
<p>You then create a retargeting audience: "People who visited my event page in the last 30 days but did NOT visit the confirmation page." This audience is people who showed interest but did not complete registration.</p>
<p>You serve that audience different ads with different messaging. The first round of ads introduced the event. The retargeting ads close the deal with specifics, urgency, and social proof.</p>
<p>The pixel also fires a Lead event on the confirmation page. This tells <a href="https://www.facebook.com/business/tools/ads-manager" target="_blank" rel="noopener noreferrer">Meta's ad delivery system</a> which users convert, so it can optimize ad delivery toward people with similar profiles. Without the Lead event, Meta optimizes for clicks. With it, Meta optimizes for registrations.</p>""",
            },
            {
                "heading": "Custom Audiences vs Retargeting Audiences",
                "content": """<p>These are two different things, and most event marketers conflate them.</p>
<p>A custom audience is a list you upload to Meta: emails, phone numbers, names, and zip codes from your contact database. Facebook matches those records to user profiles and shows your ads to those specific people. This is your first layer of targeting.</p>
<p>A retargeting audience is built automatically by the pixel from people who visit your site. This includes people from your custom audience who clicked an ad AND people who found your page through other channels (email campaigns, organic search, word of mouth).</p>
<p>Use both. Custom audiences for the initial outreach. Retargeting audiences for the follow-up. The two layers together cover your existing contacts plus any new interest your marketing generates.</p>""",
            },
            {
                "heading": "The 25-Day Campaign Structure",
                "content": """<p>For most events, the ad campaign runs for 25 days and stops 2 days before the event (you do not want to show ads after registration closes). Here is the structure we use:</p>
<p><strong>Days 1 to 10: Value-led awareness.</strong> Carousel ads showing the venue, speakers, and agenda. Static ads with clinical angles (for medical events) or ROI messaging (for business events). The goal is to introduce the event and drive initial site traffic.</p>
<p><strong>Days 7+: Agenda retargeting.</strong> For people who have seen your earlier ads or visited the page, serve the full event agenda. Specific times, session breakdowns, speaker credentials. The detail converts people who were interested but needed more information.</p>
<p><strong>Days 11+: Exclusivity messaging.</strong> "Not every physician in Minnesota gets this invitation." Scarcity and status drive registrations from people who have been considering it but have not committed.</p>
<p><strong>Days 19 to 25: Countdown urgency.</strong> "5 days left to register." "Final seats for April 11." Update the copy on your existing ads with deadline-driven language. No new images needed.</p>""",
            },
            {
                "heading": "Ad Creative That Works for Events",
                "content": """<p>Event ads work best when the imagery shows what attendees will experience: the venue, the speakers, the setup. Abstract stock photos perform poorly because they do not answer the question "what will this event actually look like?"</p>
<p>For carousel ads, we use 6 cards: venue exterior, event space, speaker headshots, agenda highlights, and a closing card with the registration CTA. Each card has a headline but no text overlay on the image (clean images outperform text-heavy ones on Meta platforms).</p>
<p>For static ads, we test 4 variations: clinical/educational angle, ROI/business case angle, exclusivity angle, and a full-agenda retarget. Different messaging resonates with different segments of your audience. Running all four and letting Meta optimize delivery is more effective than picking one.</p>""",
            },
            {
                "heading": "Common Retargeting Mistakes",
                "content": """<p>Launching retargeting too early is the most common mistake. If your pixel has only captured 30 events and most of them are your own test visits, the retargeting audience is too small and too noisy to be useful. Wait until you have 100+ real visitor events, which usually takes 7 to 10 days of running your initial campaign.</p>
<p>The second mistake is using the same creative for retargeting that you used for the initial outreach. If someone saw your carousel ad, clicked through, and did not register, showing them the same carousel again is unlikely to change their mind. The retargeting creative needs to provide new information: the full agenda, speaker credentials, countdown urgency, or social proof from confirmed registrants.</p>""",
            },
            {
                "heading": "Measuring What Matters",
                "content": """<p>The only metric that matters for event ad campaigns is cost per registration. Not cost per click, not reach, not impressions. If your ads generate 1,000 clicks but 5 registrations, the campaign failed regardless of how cheap the clicks were.</p>
<p>With the Meta Pixel firing a Lead event on the confirmation page, you can see cost per Lead directly in <a href="https://www.facebook.com/business/tools/ads-manager" target="_blank" rel="noopener noreferrer">Ads Manager</a>. This number tells you exactly what each registration costs and which ad sets are producing them.</p>
<p>Typical cost per registration for custom audience campaigns ranges from $5 to $25 depending on audience size and event type. Retargeting audiences tend to convert at lower cost because the audience is already warmed up.</p>
<p>If you want to see how this works in practice, read our <a href="/work/">case study</a> of a medical device event campaign, or learn about our <a href="/services/">ad management service</a>.</p>""",
            },
        ],
        "faqs": [
            {"question": "How many pixel events do I need before launching retargeting?", "answer": "Wait until you have at least 100 real pixel events (not your own test visits). This usually takes 7 to 10 days of running your initial custom audience campaign. Launching retargeting too early means you are retargeting mostly your own team's test traffic."},
            {"question": "What daily budget do you recommend for event ads?", "answer": "For most events, $15 to $25 per day over a 25-day campaign works well. That is $375 to $625 in total ad spend. We set the budget at the campaign level and let Meta distribute across ad sets based on performance."},
            {"question": "Can I retarget people who saw my event email but did not register?", "answer": "If they clicked the email link and visited your registration page, yes. The pixel captures that visit. If they only opened the email without clicking, Meta does not have visibility into that. Email opens stay within your email platform's analytics."},
        ],
    },
    {
        "slug": "event-marketing-cost-diy-vs-done-for-you",
        "title": "The Real Cost of Event Marketing: DIY vs Done-For-You",
        "description": "Comparing the true cost of DIY event marketing tools vs done-for-you services. Platform fees, hidden costs, time investment, and what you actually get.",
        "h1": "The Real Cost of Event Marketing: DIY vs Done-For-You",
        "author": "Rome Thorndike",
        "sections": [
            {
                "heading": "The Sticker Price Is Not the Real Price",
                "content": """<p>Event marketing costs more than the invoice suggests. The $0/month Eventbrite plan has per-ticket fees. The $99/month Splash subscription requires a designer to customize templates. The "free" WordPress site needs a developer to install tracking, a hosting provider, a security plugin, and someone to update it all.</p>
<p>When companies compare DIY tools to done-for-you services, they compare sticker prices. The registration platform costs X dollars per month, the done-for-you service costs Y dollars per project. X is almost always lower than Y, and the comparison stops there.</p>
<p>But the real cost includes the hours your team spends on setup, the ad dollars wasted on misconfigured tracking, the registrations lost to a poor mobile experience, and the opportunity cost of your marketing team building event pages instead of running campaigns.</p>""",
            },
            {
                "heading": "DIY Platform Costs (What You See)",
                "content": """<p><strong>Eventbrite:</strong> Free for free events. 3.7% + $1.79 per ticket (Essentials) or 6.95% + $1.79 (Professional). A 200-person event at $50/ticket runs $997 to $1,937 in fees. <a href="https://www.eventbrite.com/organizer/pricing" target="_blank" rel="noopener noreferrer">Eventbrite pricing</a></p>
<p><strong>Splash:</strong> Starts around $10,000/year for the base plan. Enterprise plans run higher. Includes templates, email marketing, and analytics. Requires design time to customize. <a href="https://splashthat.com/" target="_blank" rel="noopener noreferrer">Splash</a></p>
<p><strong>Cvent:</strong> $15,000 to $50,000/year depending on features and event volume. The enterprise standard for large organizations. Overkill for most mid-market event programs.</p>
<p><strong>WordPress + plugins:</strong> Hosting ($10-30/month), domain ($12/year), SSL (usually included), registration plugin ($50-200/year), form plugin ($50-100/year). Technical cost is low; time cost is high.</p>""",
            },
            {
                "heading": "DIY Hidden Costs (What You Do Not See)",
                "content": """<p><strong>Setup time:</strong> Your marketing coordinator spends 8 to 20 hours setting up the registration page, configuring email confirmations, testing the form, and troubleshooting mobile layout issues. At a loaded cost of $40 to $75/hour, that is $320 to $1,500 per event in labor.</p>
<p><strong>Tracking setup:</strong> Installing GA4 and Meta Pixel correctly takes a developer 2 to 4 hours if they have done it before. If they have not, add research time. A misconfigured pixel means your ad spend has no attribution. You are spending money on ads and guessing whether they work.</p>
<p><strong>Ad campaign management:</strong> Running Facebook ads effectively is a skill. Setting up custom audiences, building retargeting pools, creating multiple ad variations, scheduling creative rotation, and optimizing bids takes 10 to 15 hours per campaign if you know what you are doing. If your team is learning as they go, double it.</p>
<p><strong>Design and copy:</strong> A registration page needs copy that converts and design that builds trust. Your team either writes it themselves (takes longer, likely lower quality) or hires a freelancer ($500 to $2,000 depending on scope).</p>
<p><strong>Opportunity cost:</strong> Every hour your team spends on event page logistics is an hour they are not spending on campaign strategy, content creation, or pipeline generation. For a lean marketing team, this is the biggest hidden cost.</p>""",
            },
            {
                "heading": "Done-For-You Costs (What You Get)",
                "content": f"""<p>A done-for-you service like SharpPages bundles the page build, tracking setup, and (optionally) ad campaign management into flat-fee packages.</p>
<p><strong>Site build:</strong> ${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,} for a custom registration site. Includes design, copy, mobile optimization, GA4, Meta Pixel, confirmation page, and deployment. Delivered in 5 to 7 business days.</p>
<p><strong>Additional cities:</strong> ${PRICING['event_clone']['low']:,} to ${PRICING['event_clone']['high']:,} per clone. Same template, new details, 48-hour turnaround.</p>
<p><strong>Ad management:</strong> ${PRICING['ad_monthly']['low']:,} to ${PRICING['ad_monthly']['high']:,}/month plus a ${PRICING['ad_setup']['low']:,} to ${PRICING['ad_setup']['high']:,} setup fee. Includes custom audience upload, ad creative, 25-day campaign schedule, retargeting, and weekly reporting.</p>
<p>No per-registrant fees. No annual contract. You own the site files. Full <a href="/pricing/">pricing details here</a>.</p>""",
            },
            {
                "heading": "The Break-Even Math",
                "content": f"""<p>For a single free event with minimal branding requirements, DIY on Eventbrite is cheaper. No question.</p>
<p>For a paid event with 100+ registrants, the per-ticket fees on Eventbrite approach the cost of a custom site build. At $50/ticket and 200 registrants, Eventbrite fees are roughly ${50 * 200 * 0.037 + 200 * 1.79:.0f} to ${50 * 200 * 0.0695 + 200 * 1.79:.0f}. A custom site is ${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,} with zero per-registrant fees and a reusable template for next time.</p>
<p>For recurring events (same format, different cities), the math tilts further toward done-for-you. The first site costs ${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,}. Each clone costs ${PRICING['event_clone']['low']:,} to ${PRICING['event_clone']['high']:,}. By the third event, your per-event cost is a fraction of the original investment.</p>
<p>Factor in the hidden costs (team hours, misconfigured tracking, lower conversion rates from generic pages) and the break-even point arrives sooner than the sticker prices suggest.</p>""",
            },
            {
                "heading": "The Recurring Event Advantage",
                "content": """<p>The done-for-you model gets cheaper with every event. The first site costs the full build price. The second site clones from the template at a fraction of the cost. By the fourth or fifth event, your per-event cost is lower than what most teams spend on internal labor alone.</p>
<p>This is where the DIY model breaks down for companies running recurring events. Each DIY event requires the same setup time because there is no template to clone. Your coordinator spends the same 15 hours whether it is the first event or the tenth. The done-for-you model amortizes the design and development investment across every future event.</p>""",
            },
            {
                "heading": "Choosing the Right Approach",
                "content": """<p>DIY makes sense when: your events are free, casual, or low-stakes; your team has the technical skills and time; you do not need ad attribution; branding is not a priority.</p>
<p>Done-for-you makes sense when: your events represent your brand; you are spending money on ad campaigns and need to measure ROI; your team does not have time to build pages and configure tracking; you run recurring events and want a reusable template.</p>
<p>Most companies start DIY and switch to done-for-you after the second or third event, when they realize the hidden costs have already exceeded what a custom site would have cost. If that sounds familiar, <a href="/contact/">book a call</a> and we will scope your next event.</p>
<p>Read more about our <a href="/services/">services</a> or see a <a href="/work/">project example</a>.</p>""",
            },
        ],
        "faqs": [
            {"question": "Can I switch from Eventbrite to a custom site mid-event?", "answer": "Yes. We can build the custom site and redirect the URL once it is ready. Existing Eventbrite registrations are preserved. New traffic goes to the custom page with proper tracking."},
            {"question": "Do I need to hire a developer to maintain a custom site?", "answer": "No. The site is static HTML hosted on GitHub Pages. There is nothing to maintain, no plugins to update, no security patches. If you need content changes, we can make them or you can edit the HTML directly."},
            {"question": "What if I only run one event per year?", "answer": "A custom site still makes sense if the event represents your brand and you are spending money to drive registrations. The site cost is a one-time investment, and you can reuse it the following year with updated details."},
        ],
    },
]

from _blog_new_articles import get_new_articles
BLOG_ARTICLES.extend(get_new_articles(PRICING))


def build_blog_article(article):
    """Build a single blog article page."""
    slug = article["slug"]
    page_path = f"/blog/{slug}/"

    crumbs = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": "Blog", "url": BASE_URL + "/blog/"},
        {"name": article["title"], "url": BASE_URL + page_path},
    ]
    breadcrumb_nav = get_breadcrumb_html(crumbs)
    breadcrumb_schema = get_breadcrumb_schema(crumbs)

    # Article schema
    article_schema_obj = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["description"],
        "author": {
            "@type": "Person",
            "name": article["author"],
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": BASE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/assets/logos/logo-full-dark.svg"
            }
        },
        "url": BASE_URL + page_path,
        "mainEntityOfPage": BASE_URL + page_path,
    }
    import json as _json
    article_schema = f'''
    <script type="application/ld+json">
{_json.dumps(article_schema_obj, indent=2)}
    </script>'''

    # Build sections
    sections_html = ""
    for section in article["sections"]:
        sections_html += f'''
                <h2>{section["heading"]}</h2>
                {section["content"]}'''

    faq_html = generate_faq_html(article["faqs"])

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">{article["h1"]}</h1>
                <p style="color: var(--color-text-muted); font-size: var(--text-sm); margin-top: var(--space-2);">By {article["author"]}</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="legal-content">
                    {sections_html}
                </div>
            </div>
        </section>

{faq_html}

{generate_cta_section()}'''

    html = get_page_wrapper(
        title=article["title"],
        description=article["description"],
        canonical_path=page_path,
        body_content=body,
        extra_schema=breadcrumb_schema + article_schema,
        og_type="article",
    )
    write_page(f"blog/{slug}/index.html", html)
    ALL_PAGES.append((page_path, 0.7, "monthly"))


def build_blog_index():
    """Build the blog index page listing all articles."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Blog", "/blog/")

    articles_html = ""
    for article in BLOG_ARTICLES:
        articles_html += f'''
                <a href="/blog/{article["slug"]}/" class="feature-card" style="text-decoration: none; display: block;">
                    <h3 class="feature-card__title">{article["title"]}</h3>
                    <p class="feature-card__text">{article["description"]}</p>
                    <span style="color: var(--color-primary); font-size: var(--text-sm); font-weight: 600; margin-top: var(--space-3); display: inline-block;">Read article &rarr;</span>
                </a>'''

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Blog</h1>
                <p class="page-header__subtitle">Practical guides on event registration pages, ad campaigns, and filling seats. No fluff.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="feature-grid" style="grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));">
                    {articles_html}
                </div>
            </div>
        </section>

{generate_cta_section()}'''

    html = get_page_wrapper(
        title="Blog: Web Performance, SEO & Digital Marketing Guides",
        description="Practical guides on PageSpeed optimization, SEO strategy, event marketing, and paid social. Written by Rome Thorndike.",
        canonical_path="/blog/",
        body_content=body,
        active_page="/blog/",
        extra_schema=breadcrumb_schema,
    )
    write_page("blog/index.html", html)
    ALL_PAGES.append(("/blog/", 0.7, "weekly"))


def build_all_blog():
    """Build blog index and all articles."""
    build_blog_index()
    for article in BLOG_ARTICLES:
        build_blog_article(article)


# =============================================================================
# AUDIT PAGE
# =============================================================================

def build_audit():
    """Build the free site audit page with URL input form and results area."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Free Site Audit", "/audit/")

    action_url = f"https://formspree.io/f/{FORMSPREE_ID}"

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Free <span class="text-accent">Site Audit</span></h1>
                <p class="page-header__subtitle">Enter your URL. Get your PageSpeed score, SEO gaps, and what is fixable. Takes 15 seconds.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container" style="max-width: 720px;">
                <form id="audit-form" class="audit-form">
                    <div class="audit-form__input-row">
                        <input class="form__input audit-form__url" type="url" id="audit-url" name="url" placeholder="https://yoursite.com" required>
                        <button type="submit" class="btn btn--primary btn--lg audit-form__submit" id="audit-submit">Run Audit</button>
                    </div>
                    <p style="font-size: var(--text-xs); color: var(--color-text-subtle); margin-top: var(--space-2);">We check mobile performance, accessibility, SEO, and best practices using Google PageSpeed Insights.</p>
                </form>

                <div id="audit-loading" class="audit-loading" style="display: none;">
                    <div class="audit-loading__spinner"></div>
                    <p>Analyzing your site...</p>
                </div>

                <div id="audit-results" class="audit-results" style="display: none;">
                    <h2 class="audit-results__title">Your Results</h2>

                    <div class="audit-scores">
                        <div class="audit-score" id="score-performance">
                            <svg class="audit-score__gauge" viewBox="0 0 120 120">
                                <circle cx="60" cy="60" r="54" fill="none" stroke="var(--color-border)" stroke-width="8"/>
                                <circle class="audit-score__ring" cx="60" cy="60" r="54" fill="none" stroke-width="8" stroke-linecap="round"
                                    stroke-dasharray="339.292" stroke-dashoffset="339.292" transform="rotate(-90 60 60)"/>
                            </svg>
                            <span class="audit-score__value">0</span>
                            <span class="audit-score__label">Performance</span>
                        </div>
                        <div class="audit-score" id="score-accessibility">
                            <svg class="audit-score__gauge" viewBox="0 0 120 120">
                                <circle cx="60" cy="60" r="54" fill="none" stroke="var(--color-border)" stroke-width="8"/>
                                <circle class="audit-score__ring" cx="60" cy="60" r="54" fill="none" stroke-width="8" stroke-linecap="round"
                                    stroke-dasharray="339.292" stroke-dashoffset="339.292" transform="rotate(-90 60 60)"/>
                            </svg>
                            <span class="audit-score__value">0</span>
                            <span class="audit-score__label">Accessibility</span>
                        </div>
                        <div class="audit-score" id="score-best-practices">
                            <svg class="audit-score__gauge" viewBox="0 0 120 120">
                                <circle cx="60" cy="60" r="54" fill="none" stroke="var(--color-border)" stroke-width="8"/>
                                <circle class="audit-score__ring" cx="60" cy="60" r="54" fill="none" stroke-width="8" stroke-linecap="round"
                                    stroke-dasharray="339.292" stroke-dashoffset="339.292" transform="rotate(-90 60 60)"/>
                            </svg>
                            <span class="audit-score__value">0</span>
                            <span class="audit-score__label">Best Practices</span>
                        </div>
                        <div class="audit-score" id="score-seo">
                            <svg class="audit-score__gauge" viewBox="0 0 120 120">
                                <circle cx="60" cy="60" r="54" fill="none" stroke="var(--color-border)" stroke-width="8"/>
                                <circle class="audit-score__ring" cx="60" cy="60" r="54" fill="none" stroke-width="8" stroke-linecap="round"
                                    stroke-dasharray="339.292" stroke-dashoffset="339.292" transform="rotate(-90 60 60)"/>
                            </svg>
                            <span class="audit-score__value">0</span>
                            <span class="audit-score__label">SEO</span>
                        </div>
                    </div>

                    <div class="audit-metrics">
                        <div class="audit-metric">
                            <span class="audit-metric__label">Speed Index</span>
                            <span class="audit-metric__value" id="metric-speed-index">--</span>
                        </div>
                        <div class="audit-metric">
                            <span class="audit-metric__label">LCP</span>
                            <span class="audit-metric__value" id="metric-lcp">--</span>
                        </div>
                        <div class="audit-metric">
                            <span class="audit-metric__label">CLS</span>
                            <span class="audit-metric__value" id="metric-cls">--</span>
                        </div>
                        <div class="audit-metric">
                            <span class="audit-metric__label">TBT</span>
                            <span class="audit-metric__value" id="metric-tbt">--</span>
                        </div>
                    </div>

                    <div class="audit-seo-checks" id="audit-seo-checks">
                        <h3>SEO Checklist</h3>
                        <div id="seo-checklist"></div>
                    </div>

                    <div class="audit-cta">
                        <h3>Want the full report with fix priorities?</h3>
                        <p>Your site scored <span id="audit-cta-score" class="text-accent">--</span> on mobile performance. Our clients average 95+. Enter your email for the detailed breakdown and recommended fixes.</p>
                        <form class="audit-cta__form" action="{action_url}" method="POST">
                            <input type="hidden" name="_subject" value="Audit Report Request">
                            <input type="hidden" name="audit_url" id="audit-cta-url" value="">
                            <input type="hidden" name="audit_score" id="audit-cta-score-hidden" value="">
                            <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                            <div class="audit-cta__input-row">
                                <input class="form__input" type="email" name="email" placeholder="you@company.com" required>
                                <button type="submit" class="btn btn--primary">Get Full Report</button>
                            </div>
                        </form>
                    </div>
                </div>

                <div id="audit-error" class="audit-error" style="display: none;">
                    <p id="audit-error-message">Something went wrong. Check the URL and try again.</p>
                    <button class="btn btn--outline" onclick="document.getElementById('audit-form').style.display='block'; document.getElementById('audit-error').style.display='none';">Try Again</button>
                </div>
            </div>
        </section>

        <section class="content-section" style="border-top: 1px solid var(--color-border);">
            <div class="container" style="max-width: 720px;">
                <h2>How the Audit Works</h2>
                <p>We run your URL through Google PageSpeed Insights (the same tool Google uses to evaluate sites for search ranking) and check your HTML for common SEO issues: missing title tags, meta descriptions, heading structure, schema markup, OG tags, and mobile viewport configuration.</p>
                <p>The scores you see are the same scores Google sees. If your site scores below 90 on mobile, you are leaving traffic and conversions on the table.</p>
                <p>Our clients' sites average 95+ on Performance and 100 on SEO. If you want to see what that looks like, <a href="/work/">check our case studies</a> or <a href="/contact/">book a call</a>.</p>
            </div>
        </section>

        <section class="faq-section">
            <div class="container" style="max-width: 720px;">
                <h2>Frequently Asked Questions</h2>
                <div class="faq-list">
                    <details class="faq-item">
                        <summary class="faq-item__question">Is this really free?</summary>
                        <div class="faq-item__answer"><p>Yes. The summary scores and SEO checklist are free with no email required. We ask for your email only if you want the detailed report with prioritized fix recommendations.</p></div>
                    </details>
                    <details class="faq-item">
                        <summary class="faq-item__question">What data do you collect?</summary>
                        <div class="faq-item__answer"><p>The URL you enter and the scores returned by Google. If you submit your email, we store that to send the report. We do not track, sell, or share your data. See our <a href="/privacy/">privacy policy</a>.</p></div>
                    </details>
                    <details class="faq-item">
                        <summary class="faq-item__question">Why does my score differ from what I see on PageSpeed Insights directly?</summary>
                        <div class="faq-item__answer"><p>Scores can vary slightly between runs because Google tests from different servers and network conditions. The variance is typically 3 to 5 points. If your score is consistently below 80, the issue is your site, not the measurement.</p></div>
                    </details>
                    <details class="faq-item">
                        <summary class="faq-item__question">Can you fix my site if it scores poorly?</summary>
                        <div class="faq-item__answer"><p>Yes. We offer a <a href="/pricing/">PageSpeed audit and fix service</a> starting at ${PRICING["pagespeed_fix"]["low"]:,}. For sites on WordPress or Webflow that need a deeper overhaul, we do full <a href="/services/redesign/">redesigns and migrations</a> to static HTML that consistently score 90+.</p></div>
                    </details>
                </div>
            </div>
        </section>'''

    faq_schema = """
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Is this really free?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. The summary scores and SEO checklist are free with no email required. We ask for your email only if you want the detailed report with prioritized fix recommendations."
                }
            },
            {
                "@type": "Question",
                "name": "What data do you collect?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The URL you enter and the scores returned by Google. If you submit your email, we store that to send the report. We do not track, sell, or share your data."
                }
            },
            {
                "@type": "Question",
                "name": "Why does my score differ from what I see on PageSpeed Insights directly?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Scores can vary slightly between runs because Google tests from different servers and network conditions. The variance is typically 3 to 5 points."
                }
            },
            {
                "@type": "Question",
                "name": "Can you fix my site if it scores poorly?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. We offer a PageSpeed audit and fix service. For sites needing a deeper overhaul, we do full redesigns and migrations to static HTML that consistently score 90+."
                }
            }
        ]
    }
    </script>"""

    html = get_page_wrapper(
        title="Free Site Audit: Check Your PageSpeed and SEO",
        description="Run your site through our free audit. See your PageSpeed score, SEO gaps, and what is fixable. Instant results, no signup required.",
        canonical_path="/audit/",
        body_content=body,
        active_page="/audit/",
        extra_schema=breadcrumb_schema + faq_schema,
    )
    write_page("audit/index.html", html)
    ALL_PAGES.append(("/audit/", 0.9, "monthly"))


# =============================================================================
# STATIC ASSETS
# =============================================================================

def copy_static_assets():
    """Copy CSS, JS, tokens, webmanifest, and assets into output/."""
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR)

    # Directories: copy entire trees
    dir_copies = [
        ("css", "css"),
        ("js", "js"),
        ("assets", "assets"),
    ]
    for src_dir, dest_dir in dir_copies:
        src = os.path.join(PROJECT_ROOT, src_dir)
        dest = os.path.join(output_path, dest_dir)
        if os.path.exists(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
            print(f"  Copied: {src_dir}/ -> output/{dest_dir}/")

    # Individual files
    file_copies = [
        ("tokens.css", "tokens.css"),
        ("site.webmanifest", "site.webmanifest"),
    ]
    for src_file, dest_file in file_copies:
        src = os.path.join(PROJECT_ROOT, src_file)
        dest = os.path.join(output_path, dest_file)
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"  Copied: {src_file} -> output/{dest_file}")


# =============================================================================
# SITEMAP & SEO FILES
# =============================================================================

def build_sitemap():
    """Generate sitemap.xml from ALL_PAGES list."""
    from datetime import date
    today = date.today().isoformat()
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR, "sitemap.xml")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, priority, changefreq in ALL_PAGES:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE_URL}{path}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append("  </url>")

    lines.append("</urlset>")

    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Generated: /sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots_txt():
    """Write robots.txt with AI crawler directives."""
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR, "robots.txt")

    content = """User-agent: *
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
"""

    with open(output_path, "w") as f:
        f.write(content)
    print("  Generated: /robots.txt")


def build_cname():
    """Write CNAME file for GitHub Pages custom domain."""
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR, "CNAME")

    with open(output_path, "w") as f:
        f.write("sharppages.com")
    print("  Generated: /CNAME")


def build_nojekyll():
    """Write .nojekyll file to prevent Jekyll processing on GitHub Pages."""
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR, ".nojekyll")
    with open(output_path, "w") as f:
        pass
    print("  Generated: /.nojekyll")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Build the complete SharpPages site into output/."""
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR)

    # Clean output directory
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    print(f"Building {SITE_NAME}...")

    # Pages
    build_homepage()
    build_services()
    build_all_service_pages()
    build_pricing()
    build_work()
    build_about()
    build_contact()
    build_privacy()
    build_terms()
    build_all_icp_pages()
    build_all_blog()
    build_audit()

    # Static assets
    copy_static_assets()

    # SEO files
    build_sitemap()
    build_robots_txt()
    build_cname()
    build_nojekyll()

    print(f"Build complete: {len(ALL_PAGES)} pages generated")


if __name__ == "__main__":
    main()
