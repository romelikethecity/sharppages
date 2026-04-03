#!/usr/bin/env python3
"""
Shared HTML generation module for the SharpPages website build system.

This module provides all common HTML template functions used by build.py
to generate static pages. It reads navigation and footer data from
nav_config.py and produces clean, SEO-optimized HTML output.

Usage:
    from templates import get_page_wrapper, write_page

    html = get_page_wrapper(
        title="Event Registration Sites",
        description="High-converting event pages with built-in tracking.",
        canonical_path="/services/",
        body_content="<section>...</section>",
        active_page="/services/",
    )
    write_page("services/index.html", html)
"""

import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import (
    NAV_ITEMS,
    FOOTER_COLUMNS,
    SITE_NAME,
    SITE_URL,
    SITE_TAGLINE,
    COPYRIGHT_YEAR,
    CTA_HREF,
    CTA_LABEL,
)


# =============================================================================
# CONSTANTS
# =============================================================================

BASE_URL = "https://sharppages.com"
CSS_VERSION = "12"
OUTPUT_DIR = "output"


# =============================================================================
# HTML HEAD
# =============================================================================

def get_html_head(title, description, canonical_path, extra_schema="",
                  noindex=False, og_type="website"):
    """Generate complete <head> section with meta, OG, fonts, favicon, GA4, CSS.

    Args:
        title: Page title (without site name suffix). 50-60 chars target.
        description: Meta description. 120-158 chars target.
        canonical_path: Path for canonical URL, e.g. "/services/"
        extra_schema: Optional additional JSON-LD schema script tags
        noindex: If True, add robots noindex and omit canonical tag
        og_type: Open Graph type, e.g. "website" or "article"
    """
    canonical = f"{BASE_URL}{canonical_path}"
    full_title = f"{title} | {SITE_NAME}" if title != SITE_NAME else title
    og_image = f"{BASE_URL}/assets/og/og-default.png"
    canonical_tag = "" if noindex else f'\n    <link rel="canonical" href="{canonical}">'
    if noindex:
        robots_tag = '\n    <meta name="robots" content="noindex">'
    else:
        robots_tag = '\n    <meta name="robots" content="max-snippet:-1, max-image-preview:large, max-video-preview:-1">'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#06090E">
    <title>{full_title}</title>
    <meta name="description" content="{description}">{canonical_tag}{robots_tag}

    <!-- Open Graph -->
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{og_image}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{og_image}">
{extra_schema}
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">

    <!-- Favicons -->
    <link rel="icon" href="/assets/favicons/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="/assets/favicons/favicon-32.png" sizes="32x32" type="image/png">
    <link rel="icon" href="/assets/favicons/favicon-16.png" sizes="16x16" type="image/png">
    <link rel="apple-touch-icon" href="/assets/favicons/apple-touch-icon.png">

    <!-- PWA -->
    <link rel="manifest" href="/site.webmanifest">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/styles.css?v={CSS_VERSION}">

    <!-- Google Analytics 4 with Consent Mode v2 -->
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('consent', 'default', {{
        'ad_storage': 'denied',
        'analytics_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied'
      }});
      var _sc = localStorage.getItem('sharppages-consent');
      if (_sc === 'granted') {{
        gtag('consent', 'update', {{
          'ad_storage': 'granted',
          'analytics_storage': 'granted',
          'ad_user_data': 'granted',
          'ad_personalization': 'granted'
        }});
      }}
    </script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-PLACEHOLDER"></script>
    <script>
      gtag('js', new Date());
      gtag('config', 'G-PLACEHOLDER');
    </script>
</head>'''


# =============================================================================
# NAVIGATION
# =============================================================================

def _build_nav_items(active_page=None, add_active_class=True):
    """Build nav list items HTML."""
    items_html = ""
    for item in NAV_ITEMS:
        is_active = add_active_class and active_page and active_page.startswith(item["href"])
        link_classes = "nav__link nav__link--active" if is_active else "nav__link"
        items_html += f'<li><a href="{item["href"]}" class="{link_classes}">{item["label"]}</a></li>\n'
    return items_html


def get_nav_html(active_page=None):
    """Generate full header + mobile nav HTML with inline JS toggle.

    Args:
        active_page: Current page path for active state, e.g. "/services/"
    """
    desktop_items = _build_nav_items(active_page)
    mobile_items = _build_nav_items(active_page, add_active_class=False)

    return f'''<body>
    <a href="#main-content" class="sr-only sr-only--focusable">Skip to main content</a>
    <header class="header" role="banner">
        <div class="container header__inner">
            <a href="/" class="header__logo">
                <img src="/assets/logos/logo-full-dark.svg" alt="SharpPages" class="header__logo-icon" width="140" height="32" fetchpriority="high">
            </a>

            <nav class="nav--desktop" role="navigation" aria-label="Main navigation">
                <ul class="nav__list">
                    {desktop_items}
                </ul>
            </nav>

            <div class="header__cta">
                <a href="{CTA_HREF}" class="btn btn--primary btn--sm">{CTA_LABEL}</a>
            </div>

            <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">
                <span class="menu-toggle__icon"></span>
            </button>
        </div>
    </header>

    <nav class="nav--mobile" role="navigation" aria-label="Mobile navigation">
        <ul class="nav__list">
            {mobile_items}
        </ul>
        <a href="{CTA_HREF}" class="btn btn--primary">{CTA_LABEL}</a>
    </nav>

    <script>
    (function(){{
        var toggle=document.querySelector('.menu-toggle');
        var mobileNav=document.querySelector('.nav--mobile');
        if(!toggle||!mobileNav)return;
        toggle.addEventListener('click',function(){{
            var open=mobileNav.classList.toggle('active');
            toggle.classList.toggle('active');
            toggle.setAttribute('aria-expanded',open);
            document.body.style.overflow=open?'hidden':'';
        }});
    }})();
    </script>

    <main id="main-content">'''


# =============================================================================
# FOOTER
# =============================================================================

def get_footer_html():
    """Generate complete footer with logo, tagline, link columns, copyright."""
    columns_html = ""
    for heading, links in FOOTER_COLUMNS.items():
        links_html = ""
        for link in links:
            if link["href"].startswith("http"):
                links_html += f'<li><a href="{link["href"]}" target="_blank" rel="noopener noreferrer">{link["label"]}</a></li>\n'
            else:
                links_html += f'<li><a href="{link["href"]}">{link["label"]}</a></li>\n'

        columns_html += f'''
            <div class="footer__column">
                <h4 class="footer__heading">{heading}</h4>
                <ul class="footer__links">
                    {links_html}
                </ul>
            </div>'''

    return f'''
    </main>

    <footer class="footer" role="contentinfo">
        <div class="container">
            <div class="footer__grid">
                <div class="footer__brand">
                    <a href="/" class="footer__logo">
                        <img src="/assets/logos/logo-full-dark.svg" alt="SharpPages" class="footer__logo-icon" width="140" height="32" loading="lazy">
                    </a>
                    <p class="footer__tagline">{SITE_TAGLINE}</p>
                    <div class="footer__badges">
                        <img src="/assets/badges/best-pagespeed-agency-inline.svg" alt="Best PageSpeed Agency 2026" width="260" height="48" loading="lazy">
                        <img src="/assets/badges/fastest-web-design-inline.svg" alt="Fastest Web Design 2026" width="260" height="48" loading="lazy">
                    </div>
                </div>
                {columns_html}
            </div>
            <div class="footer__bottom">
                <span>&copy; {COPYRIGHT_YEAR} {SITE_NAME}. All rights reserved.</span>
            </div>
        </div>
    </footer>

    <div id="consent-banner" class="consent-banner" style="display:none">
        <p>We use cookies to analyze site traffic and improve your experience. <a href="/privacy/">Privacy Policy</a></p>
        <div class="consent-banner__actions">
            <button class="consent-banner__btn consent-banner__btn--accept" onclick="sharpConsent('granted')">Accept</button>
            <button class="consent-banner__btn consent-banner__btn--deny" onclick="sharpConsent('denied')">Deny</button>
        </div>
    </div>
    <script>
    function sharpConsent(v){{
      localStorage.setItem('sharppages-consent',v);
      if(v==='granted'){{
        gtag('consent','update',{{'ad_storage':'granted','analytics_storage':'granted','ad_user_data':'granted','ad_personalization':'granted'}});
      }}
      document.getElementById('consent-banner').style.display='none';
    }}
    if(!localStorage.getItem('sharppages-consent')){{
      document.getElementById('consent-banner').style.display='';
    }}
    </script>
    <script src="/js/main.js?v={CSS_VERSION}" defer></script>
</body>
</html>'''


# =============================================================================
# BREADCRUMBS
# =============================================================================

def get_breadcrumb_schema(breadcrumbs):
    """Generate BreadcrumbList JSON-LD schema.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys.
    Returns:
        JSON-LD script tag as string, or empty string if no breadcrumbs.
    """
    if not breadcrumbs:
        return ""

    items = []
    for i, crumb in enumerate(breadcrumbs, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": crumb.get("name", ""),
            "item": crumb.get("url", "")
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

    return f'''
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>'''


def get_breadcrumb_html(breadcrumbs):
    """Generate visible breadcrumb navigation HTML.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys.
                    Last item is treated as current page (no link).
    """
    if not breadcrumbs:
        return ""

    crumb_parts = []
    for i, crumb in enumerate(breadcrumbs):
        if i < len(breadcrumbs) - 1:
            crumb_parts.append(f'<a href="{crumb["url"]}">{crumb["name"]}</a>')
            crumb_parts.append('<span class="breadcrumb__separator">/</span>')
        else:
            crumb_parts.append(f'<span class="breadcrumb__current">{crumb["name"]}</span>')

    return f'''<nav class="breadcrumb" aria-label="Breadcrumb">
            {" ".join(crumb_parts)}
        </nav>'''


# =============================================================================
# FAQ
# =============================================================================

def generate_faq_html(faqs, heading="Frequently Asked Questions"):
    """Generate FAQ section HTML with FAQPage schema markup.

    Args:
        faqs: List of dicts with 'question' and 'answer' keys
        heading: Section heading text

    Returns:
        HTML string for FAQ section with schema, or empty string if no FAQs
    """
    if not faqs:
        return ""

    faq_items_html = ""
    for faq in faqs:
        faq_items_html += f'''
                <details class="faq-item">
                    <summary class="faq-item__question">{faq["question"]}</summary>
                    <div class="faq-item__answer"><p>{faq["answer"]}</p></div>
                </details>'''

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }
    schema_html = f'<script type="application/ld+json">{json.dumps(faq_schema)}</script>'

    return f'''
        {schema_html}
        <section class="section faq-section">
            <div class="container">
                <h2>{heading}</h2>
                {faq_items_html}
            </div>
        </section>'''


# =============================================================================
# SCHEMA HELPERS
# =============================================================================

def get_organization_schema():
    """Generate Organization + WebSite JSON-LD schema for the homepage."""
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": BASE_URL,
        "logo": f"{BASE_URL}/assets/logos/logo-full-dark.svg",
        "description": "Performance web studio: fast static sites, programmatic SEO, paid social, and PageSpeed optimization. Flat fees, 90+ PageSpeed scores, you own the files.",
        "founder": {
            "@type": "Person",
            "name": "Rome Thorndike"
        },
        "sameAs": []
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": BASE_URL,
        "description": "SharpPages builds fast static sites, runs programmatic SEO at scale, and manages paid social campaigns. Flat fees, no platform lock-in."
    }
    return f'''
    <script type="application/ld+json">
{json.dumps(org, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(website, indent=2)}
    </script>'''


def get_service_schema(services):
    """Generate Service JSON-LD schema.

    Args:
        services: List of dicts with 'name', 'description', 'url' keys.
    """
    parts = []
    for svc in services:
        item = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": svc["name"],
            "description": svc["description"],
            "url": svc.get("url", BASE_URL + "/services/"),
            "provider": {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": BASE_URL
            }
        }
        parts.append(f'''
    <script type="application/ld+json">
{json.dumps(item, indent=2)}
    </script>''')
    return "".join(parts)


# =============================================================================
# CTA SECTION
# =============================================================================

def generate_cta_section(title="Ready to Fill Your Next Event?",
                         text="We build the page, set up the pixels, and run the ads. You run the event.",
                         button_text=None, button_href=None,
                         include_form=False, formspree_id=""):
    """Generate CTA section with button or contact form.

    Args:
        title: CTA heading
        text: CTA description
        button_text: Button label (defaults to CTA_LABEL from nav_config)
        button_href: Button URL (defaults to CTA_HREF from nav_config)
        include_form: If True, render a contact form instead of a button
        formspree_id: Formspree form ID for the action URL
    """
    btn_text = button_text or CTA_LABEL
    btn_href = button_href or CTA_HREF

    if include_form and formspree_id:
        action_url = f"https://formspree.io/f/{formspree_id}"
        inner = f'''
                <form class="form" action="{action_url}" method="POST">
                    <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                    <div class="form__row">
                        <div class="form__group">
                            <label class="form__label" for="cta-name">Name</label>
                            <input class="form__input" type="text" id="cta-name" name="name" required>
                        </div>
                        <div class="form__group">
                            <label class="form__label" for="cta-email">Email</label>
                            <input class="form__input" type="email" id="cta-email" name="email" required>
                        </div>
                    </div>
                    <div class="form__group">
                        <label class="form__label" for="cta-company">Company</label>
                        <input class="form__input" type="text" id="cta-company" name="company">
                    </div>
                    <div class="form__group">
                        <label class="form__label" for="cta-message">Tell us about your event</label>
                        <textarea class="form__textarea" id="cta-message" name="message" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn--primary btn--lg form__submit">{btn_text}</button>
                </form>'''
    else:
        inner = f'''
                <a href="{btn_href}" class="btn btn--primary btn--lg">{btn_text}</a>'''

    return f'''
        <section class="section cta-section">
            <div class="container">
                <div class="cta-section__header">
                    <h2 class="cta-section__title">{title}</h2>
                    <p class="cta-section__text">{text}</p>
                </div>
                {inner}
            </div>
        </section>'''


# =============================================================================
# PAGE WRAPPER
# =============================================================================

def get_page_wrapper(title, description, canonical_path, body_content,
                     active_page=None, extra_schema="", noindex=False,
                     og_type="website"):
    """Generate a complete HTML page by combining head, nav, content, footer.

    Args:
        title: Page title for <title> tag
        description: Meta description
        canonical_path: Path for canonical URL, e.g. "/services/"
        body_content: Inner HTML content (sections, etc.)
        active_page: Nav item to highlight, e.g. "/services/"
        extra_schema: Additional JSON-LD schema script tags
        noindex: If True, add robots noindex and omit canonical tag
        og_type: Open Graph type, e.g. "website" or "article"

    Returns:
        Complete HTML page as string
    """
    head = get_html_head(title, description, canonical_path, extra_schema,
                         noindex=noindex, og_type=og_type)
    nav = get_nav_html(active_page)
    footer = get_footer_html()

    return f'''{head}
{nav}

{body_content}

{footer}'''


# =============================================================================
# FILE WRITER
# =============================================================================

def write_page(path, html):
    """Write an HTML page to disk, creating directories as needed.

    Args:
        path: Relative file path from output dir, e.g. "services/index.html"
        html: Complete HTML content string
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, OUTPUT_DIR, path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)

    print(f"  Generated: /{path}")
