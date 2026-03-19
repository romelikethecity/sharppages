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
# ICP PAGES
# =============================================================================

ICP_PAGES = [
    {
        "slug": "medical-device-companies",
        "name": "Medical Device Companies",
        "title": "Event Registration Sites for Medical Device Companies",
        "description": "SharpPages builds registration sites and runs ad campaigns for medical device physician dinners, KOL events, and product demos. 5 to 7 day turnaround.",
        "h1": "Event Marketing for <span class=\"text-accent\">Medical Device Companies</span>",
        "intro": "Physician dinners, KOL speaker events, product demonstrations, city-by-city lunch-and-learns. Medical device companies run more field marketing events than almost any other industry, and most of them are still using email RSVPs and boosted Facebook posts to fill seats.",
        "pain_points": [
            "Your field marketing team runs 10 to 20 events per year across multiple cities, but each one starts from scratch. New landing page, new tracking setup, new ad campaign. The overhead compounds.",
            "Compliance makes everything slower. Your legal team needs to review copy. Your design team is backlogged with product launches. Meanwhile, the event is 3 weeks out and you still do not have a registration page.",
            "Eventbrite does not cut it for a premium physician dinner at a downtown hotel. The URL, the branding, the layout, none of it communicates the quality of the event or the company behind it.",
        ],
        "workflow": [
            "You send us the event brief: date, venue, speakers, agenda, specialties, and any compliance requirements for copy.",
            "We build a custom registration site on your domain with your branding. Mobile-responsive, fast-loading, and designed to convert physician traffic into registrations.",
            "We install GA4 and Meta Pixel on every page. The confirmation page fires a Lead conversion event so your ad spend can be measured down to the registration.",
            "We upload your physician contact list as a custom audience in Meta Ads Manager. Facebook matches emails, phone numbers, and zip codes to real user profiles and serves ads directly to those physicians.",
            "We run a 25-day ad campaign with carousel and static creative. Clinical angles, ROI messaging, exclusivity, and countdown urgency as the event approaches. Retargeting catches physicians who visited but did not register.",
            "After the event, we clone the template for your next city. New venue, new date, new local contact list. 48-hour turnaround. Same quality.",
        ],
        "pricing_context": f"A first event site runs ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Additional cities are ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,} each because we clone from the proven template. Ad management is ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,} per month per active campaign.",
        "faqs": [
            {"question": "Can you work with compliance-reviewed copy?", "answer": "Yes. You send us the approved copy and we build from that. Or we write the copy and send it to your compliance team for review before the site goes live. Either workflow works."},
            {"question": "How do you handle multiple events across different cities?", "answer": "We build the first event site as a template. For each additional city, we clone it, swap the venue, date, speakers, and local details, and deploy on a new subdomain or domain. 48-hour turnaround per clone."},
            {"question": "Can you target specific specialties with the ads?", "answer": "If your contact list includes specialty data (orthopedics, dermatology, urology, etc.), we can segment the audience and tailor ad copy to each group. The more specific the targeting, the better the registration rate."},
            {"question": "What if we already have a pixel on our corporate site?", "answer": "We create a separate pixel and dataset for each event site. This keeps your event tracking clean and prevents it from mixing with corporate site data. Each campaign gets its own attribution chain."},
        ],
        "deep_dive": [
            "Medical device field marketing has a pattern that most agencies do not understand. The audience is small, high-value, and skeptical. You are not targeting 50,000 consumers. You are targeting 200 to 500 physicians in a specific metro area who specialize in a handful of disciplines. They get invited to events constantly. Pharma reps, competing device companies, hospital systems, and professional associations all compete for the same calendar slots.",
            "The registration page has to do more than collect a name and email. It has to communicate clinical credibility, event exclusivity, and professional relevance in the first 5 seconds. A physician scrolling through Facebook on their phone between patients will give you exactly that long before deciding whether to tap or keep scrolling. Generic event platforms cannot deliver that level of specificity.",
            "Tracking matters more in medical device marketing than in almost any other vertical. Your field marketing budget is scrutinized quarterly. Every event needs to show ROI in the form of registrations, attendance, and downstream revenue conversations. If you cannot attribute registrations to specific ad campaigns and audience segments, you cannot defend the budget. We build that attribution chain from the first ad impression to the confirmation page.",
            "The template cloning model is built for how medical device companies actually operate. You run the same event format in Minneapolis, then Detroit, then Dallas, then Miami. Each city gets a fresh site with local venue details, but the design, tracking architecture, and proven copy structure carry over. The second city takes 48 hours instead of 7 days. By the fourth city, your cost per event site is a fraction of the first.",
        ],
        "outbound_links": [
            {"text": "Meta Business Suite", "url": "https://business.facebook.com/"},
            {"text": "Google Analytics 4", "url": "https://analytics.google.com/"},
        ],
    },
    {
        "slug": "pharma-field-marketing",
        "name": "Pharma Field Marketing",
        "title": "Event Sites for Pharma Field Marketing Teams",
        "description": "Registration sites and ad campaigns for pharma speaker programs, advisory boards, and field marketing events. Compliance-friendly. 5 to 7 day turnaround.",
        "h1": "Event Marketing for <span class=\"text-accent\">Pharma Field Marketing</span>",
        "intro": "Speaker programs, advisory boards, regional symposia, HCP engagement dinners. Pharma field marketing teams run high-touch events where the registration experience matters as much as the event itself. Your attendees are physicians and KOLs who evaluate your brand before they walk through the door.",
        "pain_points": [
            "Your marketing agency takes 4 to 6 weeks to build an event page. By the time it is live, you have lost half your promotion window. The event is 3 weeks out and your only registration channel is an email PDF with an RSVP link.",
            "Internal teams are stretched thin across product launches, congress prep, and quarterly campaigns. A regional dinner event does not get priority until it is an emergency.",
            "Generic event platforms do not meet pharma branding standards. Compliance needs to review every word on the page, and you cannot customize an Eventbrite layout to match your corporate identity system.",
        ],
        "workflow": [
            "You send us the event details and any compliance-approved copy. If copy needs writing, we draft it for your medical/legal/regulatory review.",
            "We build a branded registration site on your domain. Clean design, mobile-responsive, and compliant with your visual identity guidelines.",
            "Tracking is installed: GA4 for site analytics, Meta Pixel for conversion attribution. Each event gets its own pixel dataset to keep reporting clean.",
            "We build custom audiences from your HCP contact data (email, phone, NPI if available, zip code) and upload to Meta Ads Manager.",
            "Targeted ads run across Facebook and Instagram. Professional creative with clinical messaging, speaker credentials, and CME/CE credit details where applicable.",
            "Post-event, we clone the template for your next market. You get consistency across regions without starting over.",
        ],
        "pricing_context": f"First event site: ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Clone sites for additional markets: ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,}. Ad management: ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,}/month.",
        "faqs": [
            {"question": "Do you have experience with pharma compliance requirements?", "answer": "We build the site and copy. Your compliance team reviews and approves. We make revisions until it passes. The process is the same as working with any external agency, but faster because there are fewer people in the chain."},
            {"question": "Can the registration page capture custom fields?", "answer": "Yes. We can add fields for specialty, NPI number, institution, or any other data your team needs. All submissions flow into a tracking spreadsheet or your preferred system."},
            {"question": "How do you handle speaker programs with CME credits?", "answer": "We include CME/CE credit details, speaker bios, learning objectives, and accreditation statements on the registration page. Your medical education team provides the content; we handle the presentation."},
            {"question": "What happens to the site after the event?", "answer": "You own the files. We can take the site down, redirect it to your corporate site, or update it for a future event in the same market. For recurring programs, we archive the current version and clone the template with updated details for the next date."},
        ],
        "deep_dive": [
            "Pharma field marketing operates under constraints that most web agencies have never dealt with. Medical/legal/regulatory review cycles add days to every deliverable. Copy that mentions efficacy data, clinical outcomes, or off-label indications triggers a review chain that can stall a project for weeks if you are not prepared for it.",
            "The registration page is often the first touchpoint between your field team and the HCP audience. Speaker programs, advisory boards, and regional symposia are relationship-building events. The page needs to reflect the same professionalism that your medical science liaisons bring to one-on-one meetings. A generic Eventbrite layout with the default font and a stock photo header does not meet that standard.",
            "We have built registration sites for events where the compliance team revised copy three times before approval. The turnaround matters because every revision cycle eats into your promotion window. A 4-week agency timeline with 2 weeks of revisions leaves you 2 weeks to promote. Our 5 to 7 day build gives your compliance team room to review without killing the campaign schedule.",
            "Custom audience targeting for pharma events is precise. NPI-matched contact lists, specialty-filtered databases, and geographic targeting around the event venue. The physicians you want in the room are identifiable and reachable through Meta's custom audience matching. But only if the pixel is configured correctly and the conversion events fire on the confirmation page. We handle the technical plumbing so your field team can focus on the relationships.",
        ],
        "outbound_links": [
            {"text": "Meta Ads Manager", "url": "https://www.facebook.com/business/tools/ads-manager"},
            {"text": "GitHub Pages", "url": "https://pages.github.com/"},
        ],
    },
    {
        "slug": "b2b-saas",
        "name": "B2B SaaS",
        "title": "Event Registration Sites for B2B SaaS Companies",
        "description": "Registration sites and ad campaigns for B2B SaaS roadshows, user groups, partner summits, and product launches. Custom branding, fast turnaround.",
        "h1": "Event Marketing for <span class=\"text-accent\">B2B SaaS Companies</span>",
        "intro": "Roadshows, user group meetups, partner summits, product launch events, customer advisory boards. B2B SaaS companies run field events to deepen relationships, generate pipeline, and turn users into advocates. The registration page is the first impression, and most SaaS companies are still sending prospects to a generic form.",
        "pain_points": [
            "Your marketing team is optimized for digital campaigns, not event logistics. Building a registration page means pulling a designer off the product launch, getting engineering to install tracking, and hoping the handoff works.",
            "You are running the same event format in 5 cities but building each page from scratch. The design drifts, the tracking is inconsistent, and nobody can compare performance across markets.",
            "Splash, Bizzabo, and Cvent charge per-registrant fees or annual contracts that do not make sense for a 6-event roadshow. You end up paying platform costs on top of the actual event budget.",
        ],
        "workflow": [
            "Send us the event brief: cities, dates, venues, speakers, agenda, and your brand guidelines.",
            "We build the first city's registration site on your domain. Your brand, your design system, your tracking.",
            "GA4 and Meta Pixel installed from day one. You get clean attribution from ad impression to registration.",
            "We upload your target account list or contact database as a custom audience. If you have an ABM list, we can target those accounts directly.",
            "Ads run on Facebook and Instagram with messaging tailored to your ICP. Product-led, outcome-focused creative. No buzzwords.",
            "We clone the template for each additional city. Same design, fresh tracking, new local audience targeting. 48-hour turnaround per city.",
        ],
        "pricing_context": f"First city: ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Each additional city: ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,}. Ad management: ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,}/month per active campaign.",
        "faqs": [
            {"question": "Can you integrate with our existing marketing stack?", "answer": "The registration form can post data to Formspree, a webhook, or any endpoint your team specifies. From there, your team can route it to Salesforce, HubSpot, Marketo, or wherever leads need to go."},
            {"question": "Do you support multi-track or multi-day events?", "answer": "Yes. We can build pages with session selectors, track breakdowns, and multi-day agendas. The site structure scales with the event complexity."},
            {"question": "What about ABM targeting?", "answer": "If you have a target account list with contact data, we upload it as a custom audience. Facebook matches those records to real profiles. You can also layer LinkedIn advertising on top if your budget supports it. We handle the Meta side."},
            {"question": "Can you build pages for virtual or hybrid events?", "answer": "Yes. Virtual events get the same registration page treatment with tracking and ad campaigns. The page links to your streaming platform (Zoom, Hopin, or whatever you use) instead of a venue address. Hybrid events can display both in-person and virtual attendance options on the same registration form."},
        ],
        "deep_dive": [
            "B2B SaaS field events serve a different purpose than consumer marketing events. You are not trying to sell a product at the event. You are trying to deepen relationships with existing customers, generate pipeline from target accounts, and create content moments (customer stories, product demos, partner announcements) that your marketing team can repurpose for months afterward.",
            "The registration page for a SaaS roadshow needs to communicate value to a specific audience: VPs of Sales, Revenue Operations leaders, CIOs, or whatever your ICP looks like. Generic event copy does not work. The page needs to name the roles, the challenges, and the outcomes that matter to the people you want in the room.",
            "Most SaaS marketing teams are optimized for digital. They run webinars, email sequences, and LinkedIn campaigns with sophisticated attribution. When they shift to field events, the attribution infrastructure disappears. The registration page lives on a platform that does not support their pixel. The ad campaign runs without conversion tracking. The event happens and nobody can connect it to pipeline.",
            "We bridge that gap. The registration site gets the same tracking rigor your digital campaigns have: Meta Pixel with Lead events, GA4 with custom events, UTM parameter capture, and source attribution on every registration. Your field events feed the same attribution model as your digital programs. The data lives in the same dashboards.",
            "Multi-city roadshows are where the model scales best. Five cities over three months, same event format, different local audiences. We build the first city in a week. Each additional city clones in 48 hours with fresh venue details, local targeting, and a separate tracking dataset. Your marketing team can compare cost per registration across markets and double down on the cities that convert.",
        ],
        "outbound_links": [
            {"text": "Meta Pixel documentation", "url": "https://www.facebook.com/business/tools/meta-pixel"},
            {"text": "Google Analytics", "url": "https://analytics.google.com/"},
        ],
    },
    {
        "slug": "conference-organizers",
        "name": "Conference Organizers",
        "title": "Event Registration Sites for Conference Organizers",
        "description": "Custom registration sites and ad campaigns for conferences, summits, and multi-day events. No per-registrant fees. No platform lock-in.",
        "h1": "Event Marketing for <span class=\"text-accent\">Conference Organizers</span>",
        "intro": "You run a conference. Not a 20-person dinner, but a 200-plus attendee event with sponsors, speakers, breakout sessions, and a registration flow that needs to handle volume. You cannot justify Cvent pricing, but you need more than Eventbrite gives you.",
        "pain_points": [
            "Cvent costs $15,000 to $50,000 per year. For a single annual conference or a small series, that math does not work. You are paying for enterprise features your event does not need.",
            "Eventbrite is affordable but limited. You cannot fully customize the page, the URL says eventbrite.com, and the per-ticket fees add up fast when registration is free or low-cost.",
            "Your current setup is stitched together: Google Form for registration, Mailchimp for confirmations, a WordPress page nobody maintains, and no tracking connecting your ad spend to actual registrations.",
        ],
        "workflow": [
            "Send us the conference details: sessions, speakers, sponsors, schedule, venue, and any tiered registration (early bird, VIP, general).",
            "We build a multi-section registration site on your domain. Speaker bios, session descriptions, sponsor logos, venue details, and a registration form that feeds your tracking.",
            "GA4 and Meta Pixel installed. Every registration fires a conversion event. You know exactly which ad, audience, or channel drove each signup.",
            "We build custom audiences from your mailing list, past attendee data, or sponsor contact databases and run targeted campaigns on Facebook and Instagram.",
            "Retargeting captures interested visitors who did not complete registration. Different messaging, escalating urgency, countdown to early bird deadlines.",
            "After the conference, we keep the site live as an archive or update it for next year. The template, tracking, and audiences carry over.",
        ],
        "pricing_context": f"Conference registration site: ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Ad management: ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,}/month. No per-registrant fees. No annual platform contract.",
        "faqs": [
            {"question": "Can you handle tiered registration pricing?", "answer": "Yes. Early bird, general admission, VIP, speaker, and sponsor tiers can all be displayed on the registration page with different pricing. The form captures which tier the registrant selects."},
            {"question": "How do sponsors get visibility on the site?", "answer": "Sponsor logos, descriptions, and links can be included on the main page and/or a dedicated sponsors section. We can tier sponsor visibility (platinum, gold, silver) to match your sponsorship packages."},
            {"question": "Can attendees select specific sessions during registration?", "answer": "We can add session selection fields, track/breakout preferences, and dietary/accessibility questions to the registration form. The data flows into your tracking spreadsheet with the rest of the registration details."},
            {"question": "Do you handle email confirmations and reminders?", "answer": "The registration form triggers an automatic confirmation email through Formspree or your preferred email system. For reminder sequences (1 week before, 1 day before, morning of), we can set those up through your email platform or recommend a lightweight automation tool that connects to the registration data."},
        ],
        "deep_dive": [
            "Conference organizers face a unique version of the build-vs-buy decision. Cvent and Bizzabo are built for enterprises running 50+ events per year with dedicated event operations teams. If you run one annual conference or a small series, you are paying for features you will never touch: attendee networking apps, badge printing integrations, multi-track session management at scale.",
            "The other end of the spectrum is Eventbrite, which caps out quickly for professional conferences. Limited customization, per-ticket fees that scale with attendance, and a URL that signals 'casual meetup' rather than 'industry-leading conference.' Your sponsors paid $10,000 for a booth. They expect the registration experience to reflect that investment.",
            "A custom registration site sits in the middle. Full branding control, unlimited customization, proper tracking, and no per-registrant fees. Speaker bios with headshots and session descriptions. Sponsor logos tiered by package level. An agenda that visitors can scan in 10 seconds. Early bird pricing with countdown timers. All on your domain, loading in under a second.",
            "For recurring conferences, the template model saves weeks of work each year. Update the speakers, sessions, sponsors, and dates. The design, tracking, and proven page structure carry over. Your team spends time on programming and promotion instead of rebuilding the registration infrastructure from scratch every cycle.",
            "Sponsor visibility is another factor platform-based solutions handle poorly. Your sponsors paid to be associated with the conference. Their logos, descriptions, and links deserve prominent placement on the registration page, tiered by sponsorship level. Eventbrite gives you a description field. A custom site gives you a dedicated sponsor section with platinum, gold, and silver tiers, each with the visual prominence the sponsorship package promises.",
        ],
        "outbound_links": [
            {"text": "Google Analytics 4", "url": "https://analytics.google.com/"},
            {"text": "Formspree form backend", "url": "https://formspree.io/"},
        ],
    },
    {
        "slug": "med-spas",
        "name": "Med Spas",
        "title": "Event Registration Sites for Med Spas",
        "description": "Registration sites and ad campaigns for med spa grand openings, patient acquisition events, and treatment showcases. Local targeting, fast turnaround.",
        "h1": "Event Marketing for <span class=\"text-accent\">Med Spas</span>",
        "intro": "Grand openings, patient appreciation events, treatment showcases, injector meet-and-greets. Med spas thrive on events that get potential patients through the door. Once they see the space, meet the providers, and experience a demo, they book. The hard part is getting them there.",
        "pain_points": [
            "Your front desk team is fielding phone calls and managing appointments. They do not have time to build a landing page, install a Facebook pixel, or set up an ad campaign for next month's event.",
            "Boosted Instagram posts reach your existing followers, but not the new patients in your zip code who have never heard of your practice. You are advertising to people who already know you.",
            "A generic Eventbrite page for a med spa event sends the wrong signal. Your business sells premium aesthetics. The registration experience should match the quality of the service.",
        ],
        "workflow": [
            "Send us the event details: date, location, featured treatments, special offers, and any provider bios you want highlighted.",
            "We build a branded event page on your domain (or a dedicated event domain). Clean, premium design that matches the aesthetic your patients expect.",
            "GA4 and Meta Pixel track every page view and registration. You know exactly how many people your ads brought to the page and how many registered.",
            "We build a local custom audience: your patient email list, lookalike audiences in your zip code radius, and interest-based targeting for aesthetics, skincare, and wellness.",
            "Facebook and Instagram ads run with before/after-safe creative (no before/after patient photos per Meta policy, but lifestyle and treatment imagery works). Local targeting ensures your budget reaches people who can actually attend.",
            "Retargeting catches visitors who did not register. Follow-up ads with event details, provider credentials, and special offer reminders.",
        ],
        "pricing_context": f"Event registration site: ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Ad management: ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,}/month. If you run recurring events, additional sites clone from your template at ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,}.",
        "faqs": [
            {"question": "Can the page include special event pricing for treatments?", "answer": "Yes. We can display event-exclusive pricing, bundled packages, or promotional offers directly on the registration page. This gives attendees a reason to register rather than just showing up."},
            {"question": "Do you handle before-and-after imagery?", "answer": "We follow Meta's advertising policies, which restrict before-and-after patient imagery in ads. On the registration page itself, you can include whatever imagery your practice is comfortable displaying. We use lifestyle and treatment imagery for the ads."},
            {"question": "Can you target a specific radius around our location?", "answer": "Yes. We set a geographic radius in your ad targeting (typically 10 to 25 miles depending on your market) and layer it with interest-based and demographic targeting to reach potential patients in your area."},
            {"question": "How quickly can you turn around a site for an upcoming event?", "answer": "Standard turnaround is 5 to 7 business days for a new site. If your event is sooner, we can discuss expedited delivery. The key constraint is usually copy approval and image assets from your team, not our build time."},
        ],
        "deep_dive": [
            "Med spa marketing is visual, local, and trust-dependent. Potential patients are deciding whether to inject a substance into their face or commit to a body contouring treatment plan. The registration page for your event is the first impression of your practice for many of these prospects. If the page looks like a generic form on a free platform, it undermines the premium positioning your practice depends on.",
            "Local targeting is where the ad budget works hardest. A med spa in Scottsdale does not need to reach people in Phoenix suburbs 40 miles away. We set geographic targeting to a 10 to 15 mile radius and layer interest-based targeting (aesthetics, skincare, wellness, anti-aging) on top. The result is ads that reach potential patients who can actually walk through your door.",
            "Event marketing for med spas follows a specific conversion pattern. The prospect sees an ad, visits the registration page, attends the event, and books a consultation or treatment on-site. The registration page needs to preview the experience: which treatments will be demonstrated, which providers will be there, and what exclusive pricing is available for attendees. Vague event descriptions do not drive registrations. Specific treatment names, provider credentials, and promotional offers do.",
            "Meta's advertising policies restrict before-and-after patient imagery in ads. This is a common stumbling block for med spa marketing teams. On the registration page itself, you can display whatever imagery your practice is comfortable with. But the ads that drive traffic need to use lifestyle imagery, treatment device photos, and provider portraits. We handle this split so your ads stay compliant while your page showcases results.",
        ],
        "outbound_links": [
            {"text": "Meta advertising policies", "url": "https://www.facebook.com/business/help/488043719226498"},
            {"text": "Google Analytics 4", "url": "https://analytics.google.com/"},
        ],
    },
    {
        "slug": "real-estate",
        "name": "Real Estate",
        "title": "Event Registration Sites for Real Estate Events",
        "description": "Registration sites and ad campaigns for property launches, investor events, broker previews, and open houses. Professional branding, targeted ads.",
        "h1": "Event Marketing for <span class=\"text-accent\">Real Estate</span>",
        "intro": "Property launches, investor presentations, broker previews, luxury open houses, community events. Real estate marketing lives and dies on getting the right people in the room. A developer launching a condo project needs pre-sales interest. A brokerage hosting an investor event needs qualified attendees, not tire-kickers.",
        "pain_points": [
            "Your brokerage website is built for listings, not events. When you need a registration page for a property launch, the options are a PDF flyer with a phone number or a generic form that does not track where leads came from.",
            "Facebook ads for real estate events are powerful, but only if the pixel is installed correctly. Most real estate teams boost a post, send traffic to a page with no tracking, and have no idea which ad dollars produced which registrations.",
            "You are running events across multiple properties or markets but managing each one as a separate project. Different designers, different tracking, different follow-up systems. No consistency and no way to compare performance.",
        ],
        "workflow": [
            "Send us the event details: property, date, venue, target audience (investors, brokers, buyers), and any imagery or renderings you want featured.",
            "We build a premium registration page on your domain or a dedicated event domain. Property photos, floor plans, location maps, and event details presented in a layout that matches the caliber of the project.",
            "GA4 and Meta Pixel installed. Every registration is tracked as a conversion, and your ad spend is attributable to actual RSVPs.",
            "We build custom audiences from your contact database (broker lists, investor lists, buyer inquiry lists) and target them with Facebook and Instagram ads.",
            "Ad creative features property imagery with professional overlays. Location callouts, pricing teasers, and event exclusivity messaging drive registrations.",
            "For multi-property firms, we clone the template for each launch. Same quality, fresh branding per project, separate tracking per event.",
        ],
        "pricing_context": f"Event registration site: ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Additional property sites: ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,}. Ad management: ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,}/month.",
        "faqs": [
            {"question": "Can you include property renderings and floor plans?", "answer": "Yes. We embed high-resolution images, renderings, and floor plan PDFs directly on the registration page. The page becomes both a marketing asset and a registration tool."},
            {"question": "Do you handle real estate advertising compliance?", "answer": "We follow Meta's advertising policies for real estate, including the Special Ad Category requirements for housing-related ads. This limits some targeting options (no age, gender, or zip code targeting in housing ads) but we work within those constraints using interest and behavior targeting."},
            {"question": "Can you target specific investor or broker lists?", "answer": "Yes. If you have a contact list with emails, phone numbers, and names, we upload it as a custom audience. Facebook matches those records to profiles and serves your ads directly to those individuals."},
            {"question": "How do Special Ad Category restrictions affect real estate ads?", "answer": "Meta requires housing-related ads to use the Special Ad Category, which removes age, gender, and zip code targeting. We compensate by using interest-based targeting (real estate investment, luxury lifestyle, property development), custom audiences from your contact database, and lookalike audiences built from your existing buyer or investor profiles. The restrictions narrow the targeting options but do not eliminate effective reach."},
        ],
        "deep_dive": [
            "Real estate event marketing operates under Meta's Special Ad Category for housing, which restricts targeting options. You cannot target by age, gender, or zip code in housing-related ads. This limitation catches many real estate marketers off guard when they try to run the same targeting strategy they use for other campaigns. We work within these constraints using interest-based, behavior-based, and custom audience targeting that complies with the housing ad category rules.",
            "The registration page for a property launch or investor event serves double duty. It is both a registration tool and a marketing asset. Prospects who land on the page may not register immediately, but they are evaluating the project based on what they see. High-resolution renderings, floor plans, location maps, pricing context, and developer credentials all belong on the page. The more information available, the more qualified the registrations.",
            "For brokerages and developers running events across multiple properties, consistency matters. Each property has different branding, pricing, and positioning. But the registration infrastructure, tracking, and ad campaign structure should be consistent so you can compare performance across projects. Our template cloning model gives each property its own branded site while maintaining the same tracking architecture and campaign framework.",
            "Investor events have a different conversion dynamic than consumer open houses. Investors evaluate opportunities based on financial projections, market data, and developer track record. The registration page needs to present this information clearly and professionally. A PDF flyer attached to an email does not cut it for a $50 million condo development. The registration experience should match the scale of the project.",
        ],
        "outbound_links": [
            {"text": "Meta Special Ad Categories", "url": "https://www.facebook.com/business/help/298000447747885"},
            {"text": "GitHub Pages hosting", "url": "https://pages.github.com/"},
        ],
    },
]


def build_icp_page(icp):
    """Build a single ICP industry page."""
    slug = icp["slug"]
    page_path = f"/for/{slug}/"

    crumbs = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": "Industries", "url": BASE_URL + "/for/{slug}/".format(slug=slug)},
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
        workflow_html += f'''<div class="process-step">
                            <div class="process-step__number">{i}</div>
                            <div class="process-step__content"><p>{step}</p></div>
                        </div>\n'''
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

    body = f'''
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
                <h2>Why Event Marketing Is Different for {icp["name"]}</h2>
                {deep_dive_html}
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2>How SharpPages Works for {icp["name"]}</h2>
                {workflow_html}
            </div>
        </section>

        <section class="content-section section--alt">
            <div class="container">
                <h2>Pricing</h2>
                <p style="color: var(--color-text-muted); line-height: var(--leading-relaxed); margin-bottom: var(--space-4);">{icp["pricing_context"]}</p>
                <p style="color: var(--color-text-muted); line-height: var(--leading-relaxed); margin-bottom: var(--space-4);">No per-registrant fees. No annual contracts. See full details on our <a href="/pricing/">pricing page</a>.</p>
                <p style="color: var(--color-text-muted); line-height: var(--leading-relaxed);">Learn more about what is included in each service on our <a href="/services/">services page</a>, or see a <a href="/work/">case study</a> of a recent project. External tools we use:{outbound_html}</p>
            </div>
        </section>

{faq_html}

{generate_cta_section(
    title=f"Ready to Fill Your Next {icp['name']} Event?",
    text="Tell us about your event. We will scope it, price it, and get back to you within one business day.",
)}'''

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
<p>A custom registration site costs ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,} as a one-time build. No per-registrant fees. No percentage of ticket sales. You own the site and can reuse it for future events.</p>
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
<p><strong>Site build:</strong> ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,} for a custom registration site. Includes design, copy, mobile optimization, GA4, Meta Pixel, confirmation page, and deployment. Delivered in 5 to 7 business days.</p>
<p><strong>Additional cities:</strong> ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,} per clone. Same template, new details, 48-hour turnaround.</p>
<p><strong>Ad management:</strong> ${PRICING['ad_management_monthly']['low']:,} to ${PRICING['ad_management_monthly']['high']:,}/month plus a ${PRICING['ad_setup_fee']['low']:,} to ${PRICING['ad_setup_fee']['high']:,} setup fee. Includes custom audience upload, ad creative, 25-day campaign schedule, retargeting, and weekly reporting.</p>
<p>No per-registrant fees. No annual contract. You own the site files. Full <a href="/pricing/">pricing details here</a>.</p>""",
            },
            {
                "heading": "The Break-Even Math",
                "content": f"""<p>For a single free event with minimal branding requirements, DIY on Eventbrite is cheaper. No question.</p>
<p>For a paid event with 100+ registrants, the per-ticket fees on Eventbrite approach the cost of a custom site build. At $50/ticket and 200 registrants, Eventbrite fees are roughly ${50 * 200 * 0.037 + 200 * 1.79:.0f} to ${50 * 200 * 0.0695 + 200 * 1.79:.0f}. A custom site is ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,} with zero per-registrant fees and a reusable template for next time.</p>
<p>For recurring events (same format, different cities), the math tilts further toward done-for-you. The first site costs ${PRICING['site_build_first']['low']:,} to ${PRICING['site_build_first']['high']:,}. Each clone costs ${PRICING['site_build_additional']['low']:,} to ${PRICING['site_build_additional']['high']:,}. By the third event, your per-event cost is a fraction of the original investment.</p>
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
    build_all_icp_pages()
    build_all_blog()

    # Static assets
    copy_static_assets()

    # SEO files
    build_sitemap()
    build_robots_txt()
    build_cname()

    print(f"Build complete: {len(ALL_PAGES)} pages generated")


if __name__ == "__main__":
    main()
