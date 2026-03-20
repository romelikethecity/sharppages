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
        "cta": "Book a Call",
    },
]

FORMSPREE_ID = "xpwdgqkl"


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

    # Service cards from SERVICES data
    service_cards = ""
    for svc in SERVICES:
        service_cards += f'''
                    <a href="/services/#{svc['id']}" class="feature-card" style="text-decoration: none; display: block;">
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
    text="Book a call. We will review your current site, discuss your goals, and send a fixed quote within two business days.",
    button_text="Book a Call",
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
    """Build services page with 6 services, each with description, includes, and anchor IDs."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Services", "/services/")

    service_schema = get_service_schema([
        {"name": s["name"], "description": s["short"], "url": BASE_URL + "/services/#" + s["id"]}
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

        <section class="content-section">
            <div class="container">
                <div class="service-block" id="website-design">
                    <h2 class="service-block__title">Website Design &amp; Build</h2>
                    <p class="service-block__text">Static HTML/CSS sites built mobile-first with sub-1-second load times. Every site scores 90+ on <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">PageSpeed Insights</a>. Full schema markup, Open Graph tags, XML sitemap, and robots.txt included. No WordPress to maintain, no plugins to update, no security patches to worry about.</p>
                    <p class="service-block__text">You get a flat fee, a fixed timeline, and you own all files when we are done. Host them anywhere. No recurring platform costs.</p>
                    <p class="service-block__text">We also build interactive lead magnets (PageSpeed audit tools, ROI calculators, assessment quizzes) that convert 2-5x better than static contact forms. These are lightweight client-side tools with no server costs.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Mobile-first, responsive design</span>
                        <span class="service-block__item">90+ PageSpeed score guaranteed</span>
                        <span class="service-block__item">Full schema markup + OG tags</span>
                        <span class="service-block__item">XML sitemap + robots.txt</span>
                        <span class="service-block__item">GA4 + conversion tracking</span>
                        <span class="service-block__item">Contact form with spam protection</span>
                        <span class="service-block__item">Deployed on your domain</span>
                        <span class="service-block__item">You own all source files</span>
                    </div>
                    <p class="service-block__pricing">Landing page: ${PRICING['site_landing']['low']:,} to ${PRICING['site_landing']['high']:,} &middot; Standard site: ${PRICING['site_standard']['low']:,} to ${PRICING['site_standard']['high']:,} &middot; Content site: ${PRICING['site_content']['low']:,} to ${PRICING['site_content']['high']:,} &middot; <a href="/pricing/">Full pricing</a></p>
                </div>

                <div class="service-block" id="website-redesign">
                    <h2 class="service-block__title">Website Redesign &amp; Migration</h2>
                    <p class="service-block__text">Migrate from WordPress, Webflow, Squarespace, or Wix to a static site. Same design (or improved), 5x faster load times. No more recurring hosting fees, no plugin bloat, no CMS updates breaking your layout at 2 AM.</p>
                    <p class="service-block__text">We provide before/after <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">PageSpeed scores</a> as proof. Most WordPress sites score 40 to 65 on mobile. After migration, those same sites score 90+. The design stays the same. The speed changes everything.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Design-faithful or improved migration</span>
                        <span class="service-block__item">5x faster load times (typical)</span>
                        <span class="service-block__item">Before/after PageSpeed scores</span>
                        <span class="service-block__item">No recurring hosting fees</span>
                        <span class="service-block__item">Zero plugin dependencies</span>
                        <span class="service-block__item">Full SEO preservation (redirects, canonicals)</span>
                    </div>
                    <p class="service-block__pricing">From WordPress/Squarespace/Wix: ${PRICING['redesign_wp_sq_wix']['low']:,} to ${PRICING['redesign_wp_sq_wix']['high']:,} &middot; From Webflow: ${PRICING['redesign_webflow']['low']:,} to ${PRICING['redesign_webflow']['high']:,} &middot; <a href="/pricing/">Full pricing</a></p>
                </div>

                <div class="service-block" id="seo-content">
                    <h2 class="service-block__title">SEO &amp; Content Strategy</h2>
                    <p class="service-block__text">Programmatic SEO that builds hundreds of pages from structured data. Hub-and-spoke architecture for topical authority. Keyword-targeted content at scale: glossary pages, comparison pages, alternative pages, location pages. Schema markup for rich results in Google.</p>
                    <p class="service-block__text">We built 322 pages for <a href="https://pecollective.com" target="_blank" rel="noopener noreferrer">PE Collective</a> and drove 363K impressions in 30 days from near-zero. We built 398 pages for getprovyx.com with a 98 PageSpeed score. The model works because the content is structured, the pages are fast, and each one targets a specific search intent.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Programmatic SEO buildout</span>
                        <span class="service-block__item">Hub-and-spoke content architecture</span>
                        <span class="service-block__item">Keyword research + targeting</span>
                        <span class="service-block__item">Schema markup for rich results</span>
                        <span class="service-block__item">Internal linking strategy</span>
                        <span class="service-block__item">Monthly performance reporting</span>
                    </div>
                    <p class="service-block__pricing">SEO audit: ${PRICING['seo_audit']['low']:,} to ${PRICING['seo_audit']['high']:,} &middot; Programmatic buildout: ${PRICING['seo_programmatic']['low']:,} to ${PRICING['seo_programmatic']['high']:,} &middot; Monthly management: ${PRICING['seo_monthly']['low']:,} to ${PRICING['seo_monthly']['high']:,}/mo &middot; <a href="/pricing/">Full pricing</a></p>
                </div>

                <div class="service-block" id="event-sites">
                    <h2 class="service-block__title">Event Registration Sites</h2>
                    <p class="service-block__text">Custom registration pages with GA4 and <a href="https://www.facebook.com/business/tools/meta-pixel" target="_blank" rel="noopener noreferrer">Meta Pixel</a> installed from day one. Template cloning for multi-city events with 48-hour turnaround. No per-registrant fees, no Eventbrite branding, no platform lock-in.</p>
                    <p class="service-block__text">Your event page lives on your domain with your branding. Every registration fires a conversion event so your ad spend is measurable down to the individual signup. Running the same event in another city? We clone the template, swap the details, and deploy in 48 hours.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Custom registration page design</span>
                        <span class="service-block__item">Mobile-responsive, sub-1-second load</span>
                        <span class="service-block__item">GA4 + Meta Pixel pre-installed</span>
                        <span class="service-block__item">Confirmation page with conversion tracking</span>
                        <span class="service-block__item">5 to 7 business day turnaround</span>
                        <span class="service-block__item">48-hour clones for additional cities</span>
                        <span class="service-block__item">No per-registrant fees</span>
                    </div>
                    <p class="service-block__pricing">First event site: ${PRICING['event_first']['low']:,} to ${PRICING['event_first']['high']:,} &middot; Additional city: ${PRICING['event_clone']['low']:,} to ${PRICING['event_clone']['high']:,} &middot; <a href="/pricing/">Full pricing</a></p>
                </div>

                <div class="service-block" id="paid-social">
                    <h2 class="service-block__title">Paid Social Advertising</h2>
                    <p class="service-block__text">Facebook and Instagram campaign management with custom audience targeting, retargeting, and urgency scheduling. Our campaigns hit 2x industry-average CTR with lower CPC. Full attribution from ad impression to conversion.</p>
                    <p class="service-block__text">We upload your contact list as a custom audience, build retargeting pools from site visitors, and run a structured campaign schedule (awareness, retargeting, urgency, countdown). Every campaign includes carousel and static ad creative with multiple copy variations tested against each other.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Custom audience upload from your contact list</span>
                        <span class="service-block__item">Facebook + Instagram placements</span>
                        <span class="service-block__item">Carousel and static ad creative</span>
                        <span class="service-block__item">Website visitor retargeting</span>
                        <span class="service-block__item">Urgency schedule with countdown copy</span>
                        <span class="service-block__item">Weekly performance reports</span>
                        <span class="service-block__item">Full conversion attribution</span>
                    </div>
                    <p class="service-block__pricing">Campaign setup: ${PRICING['ad_setup']['low']:,} to ${PRICING['ad_setup']['high']:,} &middot; Monthly management: ${PRICING['ad_monthly']['low']:,} to ${PRICING['ad_monthly']['high']:,}/mo &middot; <a href="/pricing/">Full pricing</a></p>
                </div>

                <div class="service-block" id="pagespeed-audit">
                    <h2 class="service-block__title">PageSpeed Audit &amp; Fix</h2>
                    <p class="service-block__text">Start with our <a href="/audit/">free instant audit</a>. Enter your URL and see your PageSpeed scores, SEO checklist, and performance bottlenecks in 30 seconds. The summary is free. Detailed fix priorities and a consult are available as a paid service.</p>
                    <p class="service-block__text">For sites that need hands-on work, we identify the bottlenecks (render-blocking resources, oversized images, JavaScript bloat, server response time) and fix them. You get before/after PageSpeed scores as a deliverable. This is often the entry point for a full redesign or migration project.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Free instant audit (PageSpeed + SEO checklist)</span>
                        <span class="service-block__item">Performance bottleneck identification</span>
                        <span class="service-block__item">Before/after PageSpeed scores</span>
                        <span class="service-block__item">Image optimization + compression</span>
                        <span class="service-block__item">Render-blocking resource fixes</span>
                        <span class="service-block__item">Core Web Vitals improvement</span>
                    </div>
                    <p class="service-block__pricing">Free instant audit: $0 &middot; Detailed audit + consult: $500 &middot; Audit + fix: ${PRICING['pagespeed_fix']['low']:,} to ${PRICING['pagespeed_fix']['high']:,} &middot; <a href="/pricing/">Full pricing</a></p>
                </div>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title="Not Sure Which Service You Need?",
    text="Start with a free site audit. We will show you your PageSpeed score, SEO gaps, and what is fixable. Then we can scope the right project together.",
    button_text="Get a Free Audit",
    button_href="/audit/",
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
            "answer": "Book a call. We will scope the work, give you a fixed quote, and explain exactly what is included. If it is not a fit, we will tell you."
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
                        <table class="pricing-table">
                            <thead><tr><th>Metric</th><th>SharpPages (getprovyx.com)</th><th>Agency / Webflow</th></tr></thead>
                            <tbody>
                                <tr><td>Performance</td><td>98</td><td>83</td></tr>
                                <tr><td>Speed Index</td><td>0.9s</td><td>5.0s</td></tr>
                                <tr><td>Total Blocking Time</td><td>30ms</td><td>280ms</td></tr>
                                <tr><td>Accessibility</td><td>95</td><td>92</td></tr>
                                <tr><td>Best Practices</td><td>100</td><td>73</td></tr>
                                <tr><td>SEO</td><td>100</td><td>100</td></tr>
                                <tr><td>Pages</td><td>398</td><td>~50</td></tr>
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
                    <p class="case-study__summary">This is the same programmatic SEO approach we offer as a <a href="/services/#seo-content">service</a>. The build system, content architecture, and schema patterns are reusable across industries.</p>
                </div>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="case-study">
                    <span class="case-study__label">Ad Campaign Proof</span>
                    <h2 class="case-study__title">BTL Events: 2x Industry CTR, Lower CPC</h2>
                    <p class="case-study__summary">A multi-city event campaign with custom audience targeting, retargeting, and a 25-day urgency schedule. The registration sites and ad campaigns were built and managed together, so attribution worked from day one.</p>

                    <div class="case-study__stats">
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">2x</span>
                            <span class="case-study__stat-label">Industry Avg CTR</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">Lower</span>
                            <span class="case-study__stat-label">Cost per Click</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">25 days</span>
                            <span class="case-study__stat-label">Campaign Structure</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">48hrs</span>
                            <span class="case-study__stat-label">Clone Turnaround</span>
                        </div>
                    </div>

                    <h3>Campaign Structure</h3>
                    <p class="case-study__summary">Custom audiences built from the client's contact database (physicians, medical device professionals). Facebook matched email and phone records to real user profiles. Carousel ads (6 cards) and static image variations ran with clinical, ROI, and exclusivity copy angles.</p>
                    <p class="case-study__summary">Retargeting kicked in on day 7: site visitors who did not register saw follow-up ads with full event agendas and countdown messaging. The 25-day schedule progressed from awareness to urgency, with copy updates matching the event timeline.</p>

                    <h3>The Replication Model</h3>
                    <p class="case-study__summary">The first city took 5 to 7 days for the site build. Each additional city cloned in 48 hours with fresh venue details, local contact lists, and separate tracking. The design, tracking architecture, and proven page structure carried over. By the third city, the per-event cost and setup time were a fraction of the first.</p>
                    <p class="case-study__summary">Read about our <a href="/services/#event-sites">event registration</a> and <a href="/services/#paid-social">paid social</a> services, or see <a href="/pricing/">pricing</a> for what campaigns like this cost.</p>
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
    text="Book a call. I will review your current site, discuss your goals, and send a fixed quote within two business days.",
    button_text="Book a Call",
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
        title="Contact SharpPages: Book a Call",
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
        title="Blog: Event Marketing Guides",
        description="Practical guides on event registration pages, Facebook ad campaigns, retargeting, and filling seats. Written by Rome Thorndike.",
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
                        <div class="faq-item__answer"><p>Yes. We offer a <a href="/pricing/">PageSpeed audit and fix service</a> starting at ${PRICING["pagespeed_fix"]["low"]:,}. For sites on WordPress or Webflow that need a deeper overhaul, we do full <a href="/services/#website-redesign">redesigns and migrations</a> to static HTML that consistently score 90+.</p></div>
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
    output_path = os.path.join(PROJECT_ROOT, OUTPUT_DIR, "sitemap.xml")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, priority, changefreq in ALL_PAGES:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE_URL}{path}</loc>")
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
