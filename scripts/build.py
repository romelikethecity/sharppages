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
    "site_build_first": {"low": 3500, "high": 5000},
    "site_build_additional": {"low": 1500, "high": 2500},
    "ad_management_monthly": {"low": 1500, "high": 2500},
    "ad_setup_fee": {"low": 500, "high": 1000},
}

TIERS = [
    {
        "name": "Single Event",
        "desc": "One event registration site with tracking, built in 5 to 7 business days.",
        "price_display": f"${PRICING['site_build_first']['low']:,}",
        "price_note": f"to ${PRICING['site_build_first']['high']:,}",
        "features": [
            "Custom event registration page",
            "Mobile-responsive design",
            "GA4 + Meta Pixel installed",
            "Confirmation page with conversion tracking",
            "Deployed on your domain",
            "5 to 7 business day turnaround",
        ],
        "featured": False,
        "cta": "Book a Call",
    },
    {
        "name": "Event + Ads",
        "desc": "Registration site plus a managed Facebook ad campaign targeting your audience. The full loop.",
        "price_display": f"${PRICING['site_build_first']['low'] + PRICING['ad_management_monthly']['low']:,}",
        "price_note": f"site + first month of ads (setup fee ${PRICING['ad_setup_fee']['low']:,} to ${PRICING['ad_setup_fee']['high']:,})",
        "features": [
            "Everything in Single Event",
            "Custom audience targeting (your patient/client list)",
            "Facebook retargeting campaigns",
            "Carousel + static ad creative",
            "25-day urgency schedule",
            "Weekly performance reporting",
            "Dedicated campaign manager",
        ],
        "featured": True,
        "badge": "Most Popular",
        "cta": "Book a Call",
    },
    {
        "name": "Multi-City / Ongoing",
        "desc": "Reuse your proven template across multiple cities or events. Same quality, fraction of the cost.",
        "price_display": f"${PRICING['site_build_additional']['low']:,}",
        "price_note": f"to ${PRICING['site_build_additional']['high']:,} per additional site",
        "features": [
            "Clone from your existing template",
            "New city/event details swapped in",
            "Fresh ad campaign per market",
            "Separate tracking per event",
            "48-hour turnaround for clones",
            "Volume discounts on ad management",
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
    """Build homepage with Harry Dry 10-element formula."""

    # Organization + WebSite schema
    org_schema = get_organization_schema()

    # FAQ data
    faqs = [
        {
            "question": "How long does it take to build an event registration site?",
            "answer": "5 to 7 business days from kickoff to a live, deployed site. If you need a second site for another city or event, clones take 48 hours because the template is already built."
        },
        {
            "question": "Do I need to provide copy and images?",
            "answer": "You provide event details (date, venue, speakers, agenda). We write the copy, source imagery, and build the page. You review and approve before we go live."
        },
        {
            "question": "What ad platforms do you use?",
            "answer": "Facebook and Instagram via Meta Ads Manager. We build custom audiences from your contact list (email, phone, name, zip) and run retargeting campaigns against site visitors who did not register."
        },
        {
            "question": "Can I use my own domain?",
            "answer": "Yes. We deploy to your domain via GitHub Pages. You point your DNS, we handle the rest. If you do not have a domain, we can help you pick one."
        },
        {
            "question": "What does the ad management retainer cover?",
            "answer": f"Campaign strategy, audience building, ad creative (carousel + static images), a 25-day urgency schedule, retargeting setup, and weekly performance reports. ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,} per month plus a one-time setup fee."
        },
        {
            "question": "Do you charge per registrant or take a percentage?",
            "answer": "No. You pay a flat fee for the site and a flat monthly retainer for ad management. No per-registrant charges, no platform fees, no annual contracts."
        },
    ]
    faq_html = generate_faq_html(faqs)

    body = f'''
        <section class="section hero">
            <div class="container">
                <h1 class="hero__title">Sharp pages. <span class="text-accent">Full rooms.</span></h1>
                <p class="hero__subtitle">We build your event registration site, install tracking pixels, and run Facebook ad campaigns to fill seats. You focus on the event.</p>
                <div class="hero__cta-group">
                    <a href="/contact/" class="btn btn--primary btn--lg">Book a Call</a>
                    <a href="/work/" class="btn btn--outline btn--lg">See Our Work</a>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="stats-bar">
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">5-7</span>
                        <span class="stats-bar__label">Days to Launch</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">48hr</span>
                        <span class="stats-bar__label">Clone Turnaround</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">100%</span>
                        <span class="stats-bar__label">Mobile Responsive</span>
                    </div>
                    <div class="stats-bar__item">
                        <span class="stats-bar__number">$0</span>
                        <span class="stats-bar__label">Per-Registrant Fees</span>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="text-center mb-8">What You Get</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <span class="feature-card__icon">&#9889;</span>
                        <h3 class="feature-card__title">Event Registration Site</h3>
                        <p class="feature-card__text">A custom, mobile-responsive landing page built to convert visitors into registrants. Your branding, your domain, your event details. Not a template you wrestle with yourself.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-card__icon">&#128200;</span>
                        <h3 class="feature-card__title">Tracking + Pixels</h3>
                        <p class="feature-card__text">GA4 and Meta Pixel installed from day one. Every page view, every registration, every conversion tracked. You know exactly what is working and what is not.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-card__icon">&#127919;</span>
                        <h3 class="feature-card__title">Facebook Ad Campaigns</h3>
                        <p class="feature-card__text">Custom audience targeting from your contact list. Retargeting for site visitors who did not register. Carousel and static creative. A 25-day urgency schedule leading up to your event.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-card__icon">&#128337;</span>
                        <h3 class="feature-card__title">5 to 7 Day Turnaround</h3>
                        <p class="feature-card__text">From kickoff call to live, deployed site. Not weeks of revisions and scope creep. We move fast because the playbook is proven.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-card__icon">&#128257;</span>
                        <h3 class="feature-card__title">Clone to New Markets</h3>
                        <p class="feature-card__text">Running the same event in another city? We clone your template, swap the details, and deploy in 48 hours. Same quality at a fraction of the original cost.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-card__icon">&#128176;</span>
                        <h3 class="feature-card__title">Flat Pricing, No Surprises</h3>
                        <p class="feature-card__text">No per-registrant fees. No platform charges. No annual contracts. You pay for the site build and (optionally) monthly ad management. That is it.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <div class="case-study">
                    <span class="case-study__label">Case Study</span>
                    <h2 class="case-study__title">Medical Device Manufacturer, Detroit</h2>
                    <p class="case-study__summary">A medical device company needed a registration site for a physician dinner event in Detroit. We built the page, installed tracking, and ran targeted Facebook ads against their contact database.</p>
                    <div class="case-study__stats">
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">5 days</span>
                            <span class="case-study__stat-label">Build time</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">100%</span>
                            <span class="case-study__stat-label">Mobile responsive</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">48hrs</span>
                            <span class="case-study__stat-label">Second city clone</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">2 cities</span>
                            <span class="case-study__stat-label">Same template</span>
                        </div>
                    </div>
                    <a href="/work/" class="btn btn--outline">Read the Full Story</a>
                </div>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title="Let Us Build Your Next Event Page",
    text="Tell us about your event. We will scope it, price it, and get back to you within one business day.",
    button_text="Book a Call",
)}

        <section class="section">
            <div class="container">
                <div class="founder-note">
                    <span class="founder-note__label">From the Founder</span>
                    <p class="founder-note__text">I built SharpPages because I kept seeing the same problem: event organizers spending weeks going back and forth with agencies, or trying to piece together Eventbrite pages and boosted Facebook posts themselves.</p>
                    <p class="founder-note__text">Before SharpPages, I spent a decade in enterprise SaaS (Salesforce, Microsoft, Databricks) and earned my MBA at UC Berkeley Haas. I know what good marketing ops looks like at scale, and I know most event teams do not have time to build it themselves.</p>
                    <p class="founder-note__text">So we productized it. A sharp registration page, proper tracking, and targeted ads. One package, one flat fee, delivered in under a week. The playbook works because we have run it ourselves for real events with real registrations.</p>
                    <p class="founder-note__signature">Rome Thorndike</p>
                    <p class="founder-note__title">Founder, SharpPages</p>
                </div>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Event Registration Sites That Fill Rooms",
        description="SharpPages builds high-converting event registration sites and runs ad campaigns to fill seats. Page, pixels, and paid media. 5 to 7 day turnaround.",
        canonical_path="/",
        body_content=body,
        extra_schema=org_schema,
    )
    write_page("index.html", html)
    ALL_PAGES.append(("/", 1.0, "weekly"))


def build_services():
    """Build services page with 3 core services + FAQ."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Services", "/services/")

    service_schema = get_service_schema([
        {
            "name": "Event Registration Site Build",
            "description": "Custom, mobile-responsive event registration websites with tracking pixels, deployed on your domain in 5 to 7 business days.",
            "url": BASE_URL + "/services/",
        },
        {
            "name": "Paid Social Ad Management",
            "description": "Facebook and Instagram ad campaigns with custom audience targeting and retargeting to fill event seats.",
            "url": BASE_URL + "/services/",
        },
        {
            "name": "Tracking and Analytics Setup",
            "description": "GA4, Meta Pixel, and conversion tracking installed and configured for event registration attribution.",
            "url": BASE_URL + "/services/",
        },
    ])

    faqs = [
        {
            "question": "What is included in the site build?",
            "answer": "A custom registration page, confirmation page with conversion tracking, mobile-responsive design, GA4 and Meta Pixel installation, deployment on your domain, and a 5 to 7 business day turnaround. You provide event details. We handle design, copy, build, and deployment."
        },
        {
            "question": "Can you manage ads without building the site?",
            "answer": "We can, but the results are better when we control the full loop. If we build the site, we know the pixel is installed correctly, the conversion events fire properly, and the landing page is optimized for the audience we are targeting."
        },
        {
            "question": "What ad budget do you recommend?",
            "answer": "For most events, $15 to $25 per day over a 25-day campaign works well. That is $375 to $625 in ad spend on top of the management retainer. We can adjust based on your audience size and registration goals."
        },
        {
            "question": "Do you build on WordPress or Squarespace?",
            "answer": "Neither. We build static HTML sites. They load faster, score higher on Lighthouse, and have zero platform dependencies. No monthly hosting fees, no plugin updates, no security patches. Your site lives on GitHub Pages and is served through a CDN."
        },
        {
            "question": "How do you track conversions across the funnel?",
            "answer": "GA4 tracks page views and user behavior. Meta Pixel fires a Lead event on the confirmation page when someone completes registration. We connect the pixel to your ad account so Meta can optimize delivery toward people most likely to register."
        },
        {
            "question": "What happens after the event?",
            "answer": "The site stays live as long as you want. For recurring events, we update the date, venue, and details. For multi-city events, we clone the template and deploy a new site with fresh tracking. The ad campaign pauses 2 days before the event and can restart for the next one."
        },
    ]
    faq_html = generate_faq_html(faqs)

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Everything Your Event Needs to <span class="text-accent">Fill Seats</span></h1>
                <p class="page-header__subtitle">Registration page, tracking pixels, ad campaigns. One provider, one flat fee, and your event team does not have to learn a single new tool.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="service-block">
                    <h2 class="service-block__title">Event Registration Sites</h2>
                    <p class="service-block__text">Your event deserves better than a generic Eventbrite page with someone else's branding. We build custom registration sites from scratch: your logo, your colors, your domain. Every site is mobile-responsive, fast-loading, and designed with one goal in mind: getting visitors to register.</p>
                    <p class="service-block__text">The build takes 5 to 7 business days. You send us the event details (date, venue, speakers, agenda). We write the copy, source imagery, design the page, install tracking, and deploy. You review, approve, and share the link.</p>
                    <p class="service-block__text">Running the same event in another city? We clone the template and swap the details. 48-hour turnaround at a fraction of the original cost. The design, structure, and tracking setup carry over. You get consistency across markets without paying for a full rebuild.</p>
                    <p class="service-block__text">Every site is built as static HTML. No WordPress plugins to update, no CMS to maintain, no hosting fees beyond your domain. The site loads fast, scores well on <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener noreferrer">Lighthouse</a>, and works on every device and browser your attendees use.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Custom registration page design</span>
                        <span class="service-block__item">Mobile-responsive layout</span>
                        <span class="service-block__item">Confirmation page with conversion tracking</span>
                        <span class="service-block__item">Deployed on your domain</span>
                        <span class="service-block__item">GA4 and Meta Pixel pre-installed</span>
                        <span class="service-block__item">Copy written from your event brief</span>
                        <span class="service-block__item">5 to 7 business day turnaround</span>
                        <span class="service-block__item">48-hour clones for additional cities</span>
                    </div>
                </div>

                <div class="service-block">
                    <h2 class="service-block__title">Paid Social Ad Management</h2>
                    <p class="service-block__text">A registration page without traffic is a billboard in the desert. We run targeted Facebook and Instagram campaigns that put your event in front of the people most likely to attend.</p>
                    <p class="service-block__text">It starts with your contact list. If you have emails, phone numbers, and zip codes for your target audience, we upload that as a custom audience in Meta Ads Manager. Facebook matches those records to real user profiles and serves ads directly to them.</p>
                    <p class="service-block__text">Then we layer retargeting on top. Anyone who visits your registration page but does not complete the form gets follow-up ads. Different creative, different angles, escalating urgency as the event approaches. We run a 25-day schedule: value-led awareness for the first 10 days, agenda retargeting from day 7, exclusivity messaging from day 11, and countdown copy in the final week.</p>
                    <p class="service-block__text">Every campaign includes carousel ads (6 cards) and multiple static image variations. We build the creative using your event photography or stock imagery with dark overlays and your branding. No text on images, all copy in the ad fields, because that is what performs.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">Custom audience upload from your contact list</span>
                        <span class="service-block__item">Facebook + Instagram ad placements</span>
                        <span class="service-block__item">Carousel and static ad creative</span>
                        <span class="service-block__item">25-day urgency schedule</span>
                        <span class="service-block__item">Website visitor retargeting</span>
                        <span class="service-block__item">Weekly performance reports</span>
                        <span class="service-block__item">Ad copy variations (clinical, ROI, exclusivity, agenda)</span>
                        <span class="service-block__item">Countdown copy in the final week</span>
                    </div>
                </div>

                <div class="service-block">
                    <h2 class="service-block__title">Tracking and Analytics Setup</h2>
                    <p class="service-block__text">Tracking is the part most people skip or get wrong. A misconfigured pixel means your ad spend is flying blind: Meta cannot optimize delivery, you cannot measure ROI, and your retargeting audiences never build.</p>
                    <p class="service-block__text">We install <a href="https://analytics.google.com/" target="_blank" rel="noopener noreferrer">GA4</a> for site analytics and <a href="https://www.facebook.com/business/tools/meta-pixel" target="_blank" rel="noopener noreferrer">Meta Pixel</a> for ad conversion tracking. The pixel fires a PageView on every page and a Lead event on the confirmation page when someone registers. We configure Advanced Matching so Meta can link more conversions back to ad clicks even when cookies are blocked.</p>
                    <p class="service-block__text">We also set up Consent Mode v2 with a cookie banner, connect the pixel dataset to your ad account, and verify everything in Test Events before your campaign launches. No guessing. No "I think it is working." You see real events flowing in before a single ad dollar is spent.</p>
                    <div class="service-block__includes">
                        <span class="service-block__item">GA4 property creation and configuration</span>
                        <span class="service-block__item">Meta Pixel installation with Lead event</span>
                        <span class="service-block__item">Advanced Matching enabled</span>
                        <span class="service-block__item">Consent Mode v2 with cookie banner</span>
                        <span class="service-block__item">Dataset connected to your ad account</span>
                        <span class="service-block__item">Test Events verification before launch</span>
                    </div>
                </div>

                <div class="service-block">
                    <h2 class="service-block__title">The Full Loop</h2>
                    <p class="service-block__text">Most event marketers cobble this together from 3 or 4 vendors. A designer for the page. A media buyer for the ads. A developer to install tracking. Then weeks of coordination making sure the pixel is on the right page, the conversion event fires correctly, and the audiences are connected.</p>
                    <p class="service-block__text">We do all of it. Page, pixels, paid media. One team, one flat fee, one Slack channel. The person who builds your site is the same person who installs the pixel and manages the ad campaign. Nothing gets lost in handoffs because there are no handoffs.</p>
                    <p class="service-block__text">That matters more than it sounds. When the pixel is installed by the same team running the ads, attribution works from day one. When the landing page is built by the same team writing the ad copy, the messaging is consistent from first impression to registration confirmation.</p>
                    <p class="service-block__text">You get one point of contact, one invoice, and one team accountable for the entire funnel from ad impression to confirmed registration. If the ads are not converting, we know whether the problem is targeting, creative, or the landing page, because we built all three.</p>
                    <p class="service-block__text">See how this works in practice in our <a href="/work/">case study</a>, or check <a href="/pricing/">pricing</a> to understand what each piece costs. When you are ready, <a href="/contact/">book a call</a> and we will scope your event.</p>
                </div>
            </div>
        </section>

{faq_html}

{generate_cta_section()}'''

    html = get_page_wrapper(
        title="Services: Event Sites, Ad Campaigns, Tracking",
        description="Custom event registration sites in 5 to 7 days. Facebook ad campaigns with retargeting. GA4 and Meta Pixel tracking. One provider, flat pricing.",
        canonical_path="/services/",
        body_content=body,
        active_page="/services/",
        extra_schema=breadcrumb_schema + service_schema,
    )
    write_page("services/index.html", html)
    ALL_PAGES.append(("/services/", 0.9, "monthly"))


def build_pricing():
    """Build pricing page from PRICING/TIERS data structure."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Pricing", "/pricing/")

    # Build pricing cards
    cards_html = ""
    for tier in TIERS:
        featured_class = " pricing-card--featured" if tier.get("featured") else ""
        badge_html = ""
        if tier.get("badge"):
            badge_html = f'<span class="pricing-card__badge">{tier["badge"]}</span>'

        features_html = ""
        for feat in tier["features"]:
            features_html += f"<li>{feat}</li>\n"

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
                        <a href="/contact/" class="btn btn--primary">{tier["cta"]}</a>
                    </div>'''

    faqs = [
        {
            "question": "Why is there a price range instead of a fixed number?",
            "answer": f"Scope varies. A single-page registration site with 3 speakers is on the lower end. A multi-page site with agenda breakouts, speaker bios, and venue details is on the higher end. We scope it on the kickoff call and give you a fixed quote before we start."
        },
        {
            "question": "What is included in the setup fee for ad management?",
            "answer": f"Pixel installation and verification, custom audience upload, ad creative production (carousel + static images), campaign structure in Ads Manager, and the retargeting audience configuration. It is a one-time fee of ${PRICING['ad_setup_fee']['low']:,} to ${PRICING['ad_setup_fee']['high']:,}."
        },
        {
            "question": "Is there a minimum ad spend requirement?",
            "answer": "We recommend $15 to $25 per day for a 25-day campaign. That is $375 to $625 in ad spend paid directly to Meta. We do not mark up your ad spend or take a percentage."
        },
        {
            "question": "Do you offer retainer discounts for multiple events?",
            "answer": "Yes. If you are running 3 or more events per year, we offer volume pricing on both site builds and ad management. Book a call and we will scope a package."
        },
        {
            "question": "What if I only need the site, not the ads?",
            "answer": "That works. The site build is a standalone service. Many clients start with just the site and add ad management for their second or third event once they see the page quality."
        },
    ]
    faq_html = generate_faq_html(faqs)

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Flat Pricing. <span class="text-accent">No Surprises.</span></h1>
                <p class="page-header__subtitle">No per-registrant charges. No platform fees. No annual contracts. You pay for the work, and you own the result.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="pricing-grid">
                    {cards_html}
                </div>
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container text-center">
                <h2 class="mb-4">What You Will Not Find Here</h2>
                <p style="color: var(--color-text-muted); max-width: 640px; margin: 0 auto var(--space-4); line-height: var(--leading-relaxed);">Per-registrant fees that punish you for success. Annual contracts that lock you in before you have seen results. Platform subscription costs on top of the build. Hidden revision charges.</p>
                <p style="color: var(--color-text-muted); max-width: 640px; margin: 0 auto; line-height: var(--leading-relaxed);">We quote a flat number on the kickoff call. That is what you pay. Ad spend goes directly to Meta. We do not mark it up.</p>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title="Let Us Scope Your Event",
    text="Book a call. We will ask about your event, your audience, and your timeline, then send you a fixed quote.",
)}'''

    html = get_page_wrapper(
        title="Pricing: Event Sites and Ad Campaigns",
        description=f"Event registration sites from ${PRICING['site_build_first']['low']:,}. Ad management from ${PRICING['ad_management_monthly']['low']:,}/mo. Flat pricing, no per-registrant fees, no annual contracts.",
        canonical_path="/pricing/",
        body_content=body,
        active_page="/pricing/",
        extra_schema=breadcrumb_schema,
    )
    write_page("pricing/index.html", html)
    ALL_PAGES.append(("/pricing/", 0.8, "monthly"))


def build_work():
    """Build work/portfolio page with anonymized BTL case study."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("Work", "/work/")

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Our <span class="text-accent">Work</span></h1>
                <p class="page-header__subtitle">Real projects, real results. Here is what it looks like when the page, pixels, and paid media work together.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="case-study">
                    <span class="case-study__label">Featured Project</span>
                    <h2 class="case-study__title">Medical Device Manufacturer: Detroit Physician Dinner</h2>
                    <p class="case-study__summary">A medical device company was hosting a physician dinner event at a hotel in downtown Detroit. They needed a registration site, tracking, and a targeted ad campaign to fill seats from their physician contact database.</p>

                    <div class="case-study__stats">
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">5 days</span>
                            <span class="case-study__stat-label">Site build time</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">100%</span>
                            <span class="case-study__stat-label">Mobile responsive</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">48hrs</span>
                            <span class="case-study__stat-label">Second city clone</span>
                        </div>
                        <div class="case-study__stat">
                            <span class="case-study__stat-number">2 cities</span>
                            <span class="case-study__stat-label">Same template reused</span>
                        </div>
                    </div>

                    <h3>The Problem</h3>
                    <p class="case-study__summary">The client had a contact database of physicians in the Detroit metro area but no way to turn that list into event registrations. They had tried boosted Facebook posts in the past with minimal results. Their existing registration workflow was an email RSVP that made tracking impossible.</p>

                    <h3>What We Built</h3>
                    <p class="case-study__summary">A custom registration site on their own domain with event details, speaker information, venue logistics, and a registration form that fed directly into a tracking spreadsheet. Every registration triggered a confirmation page with a Meta Pixel Lead event and a GA4 conversion.</p>
                    <p class="case-study__summary">On the ad side, we uploaded their physician contact list as a custom audience in <a href="https://www.facebook.com/business/tools/ads-manager" target="_blank" rel="noopener noreferrer">Meta Ads Manager</a>. Facebook matched those records to real user profiles. We ran carousel ads (6 cards showing the venue, speakers, and agenda) alongside static image ads with clinical and ROI-focused copy. The site was hosted on <a href="https://pages.github.com/" target="_blank" rel="noopener noreferrer">GitHub Pages</a> with a custom domain through Cloudflare DNS.</p>
                    <p class="case-study__summary">Retargeting kicked in on day 7. Physicians who visited the site but did not register saw follow-up ads with the full agenda and countdown messaging as the event approached.</p>

                    <h3>The Replication</h3>
                    <p class="case-study__summary">The same client needed an identical event in a second city. We cloned the template, swapped the city, venue, and date details, deployed on a new domain, and launched a fresh ad campaign against the local contact list. Total time from request to live site: 48 hours.</p>
                    <p class="case-study__summary">That replication model is the whole point. The first event takes 5 to 7 days. Every event after that takes a fraction of the time and cost because the design, structure, and tracking setup carry over.</p>

                    <h3>What Made It Work</h3>
                    <p class="case-study__summary">Three things separated this from the client's previous attempts. First, the registration page was on their own domain with their branding, not a generic third-party form. Second, the pixel was installed correctly from day one, so the ad platform could optimize delivery toward people likely to register. Third, the retargeting layers meant no interested physician fell through the cracks. A site visitor who did not register on the first visit saw follow-up ads within 24 hours.</p>
                    <p class="case-study__summary">Read more about how each piece works on our <a href="/services/">services page</a>, or see <a href="/pricing/">pricing</a> for what a project like this costs. <a href="/about/">Meet the team</a> behind the work.</p>
                </div>
            </div>
        </section>

{generate_cta_section(
    title="Your Event Could Be Next",
    text="Tell us about your event and we will show you what a SharpPages registration site looks like for your industry.",
)}'''

    html = get_page_wrapper(
        title="Our Work: Event Registration Case Studies",
        description="See how SharpPages built event registration sites and ran ad campaigns for real clients. Medical device, pharma, and B2B event case studies.",
        canonical_path="/work/",
        body_content=body,
        active_page="/work/",
        extra_schema=breadcrumb_schema,
    )
    write_page("work/index.html", html)
    ALL_PAGES.append(("/work/", 0.8, "monthly"))


def build_about():
    """Build about page with Rome's background and why SharpPages exists."""

    crumbs, breadcrumb_nav, breadcrumb_schema = _breadcrumbs("About", "/about/")

    body = f'''
        {breadcrumb_nav}
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">About <span class="text-accent">SharpPages</span></h1>
                <p class="page-header__subtitle">One person who knows data, marketing, and engineering. That is the whole team, and that is the point.</p>
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
                        <p>I spent a decade in enterprise SaaS before starting SharpPages. The short version: I sold software at <a href="https://www.salesforce.com/" target="_blank" rel="noopener noreferrer">Salesforce</a>, ran customer success at Microsoft, and helped scale a data startup (Datajoy) that was acquired by <a href="https://www.databricks.com/" target="_blank" rel="noopener noreferrer">Databricks</a>. Along the way, I earned my MBA at <a href="https://haas.berkeley.edu/" target="_blank" rel="noopener noreferrer">UC Berkeley Haas</a>.</p>
                        <p>That background matters because event marketing sits at the intersection of three things most agencies only do one of: data (who to target), marketing (what to say), and engineering (how to build and track it). Most agencies have designers who cannot install a pixel, media buyers who cannot build a landing page, and project managers relaying messages between both.</p>
                        <p>SharpPages is one person doing all three. I build the site, install the tracking, write the ad copy, and manage the campaign. No handoffs. No telephone game. No "let me check with our developer and get back to you."</p>
                        <p>The result is faster delivery, tighter feedback loops, and a site where the tracking actually works on launch day. Every event site I build, I also run ads against. I see the full funnel from impression to registration, and I know where the drop-offs happen because I built every piece of it.</p>
                        <p>If your event marketing is stuck between an expensive agency and a DIY tool you do not have time to learn, that is the gap SharpPages fills.</p>
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
                <h2 class="text-center mb-8">Why SharpPages Exists</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3 class="feature-card__title">Agencies Are Slow and Expensive</h3>
                        <p class="feature-card__text">A typical marketing agency takes 3 to 6 weeks to build a landing page. They charge $8,000 to $15,000 for a site that could be built in 5 days. You are paying for their overhead, their project managers, their account executives, and their office in a trendy neighborhood.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">DIY Tools Require Expertise</h3>
                        <p class="feature-card__text">Eventbrite, Splash, and Cvent all assume you have time to learn their platform, customize their templates, and figure out pixel installation yourself. Your event team has enough to do. They should not be debugging tracking code at 10 PM.</p>
                    </div>
                    <div class="feature-card">
                        <h3 class="feature-card__title">Generic Platforms Kill Conversions</h3>
                        <p class="feature-card__text">An Eventbrite page with default styling does not communicate the quality of your event. The URL says eventbrite.com, not your brand. The design looks like every other event on the platform. Attendees notice, and your conversion rate reflects it.</p>
                    </div>
                </div>
                <p style="color: var(--color-text-muted); text-align: center; margin-top: var(--space-8); line-height: var(--leading-relaxed);">See what the alternative looks like in our <a href="/work/">case study</a>, review <a href="/services/">what we offer</a>, or check <a href="/pricing/">pricing</a>.</p>
            </div>
        </section>

{generate_cta_section(
    title="Ready to Work Together?",
    text="Book a call. I will ask about your event, scope the work, and send a fixed quote within a day.",
    button_text="Book a Call",
)}'''

    html = get_page_wrapper(
        title="About SharpPages and Rome Thorndike",
        description="SharpPages was built by Rome Thorndike (UC Berkeley Haas MBA, ex-Salesforce, Microsoft, Databricks) to give event organizers sharp registration pages and full rooms.",
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

    # Static assets
    copy_static_assets()

    # SEO files
    build_sitemap()
    build_robots_txt()
    build_cname()

    print(f"Build complete: {len(ALL_PAGES)} pages generated")


if __name__ == "__main__":
    main()
