#!/usr/bin/env python3
"""
Centralized navigation configuration for SharpPages.

Edit this file to update navigation across ALL pages on the site.
After editing, regenerate all pages by running:
    python3 scripts/build.py
"""

# Site info
SITE_NAME = "SharpPages"
SITE_URL = "https://sharppages.com"
SITE_TAGLINE = "Fast sites. Real SEO results."
COPYRIGHT_YEAR = "2026"

# CTA button
CTA_HREF = "/contact/"
CTA_LABEL = "Let's Build It"

# Main navigation items (appear in header)
NAV_ITEMS = [
    {"href": "/services/", "label": "Services"},
    {"href": "/pricing/", "label": "Pricing"},
    {"href": "/work/", "label": "Work"},
    {"href": "/audit/", "label": "Free Audit"},
    {"href": "/blog/", "label": "Blog"},
]

# Footer link columns
FOOTER_COLUMNS = {
    "Services": [
        {"href": "/services/", "label": "All Services"},
        {"href": "/services/web-design/", "label": "Web Design & Build"},
        {"href": "/services/redesign/", "label": "Redesign & Migration"},
        {"href": "/services/seo/", "label": "SEO & Content"},
        {"href": "/services/events/", "label": "Event Sites"},
        {"href": "/services/ads/", "label": "Paid Social"},
        {"href": "/services/audit/", "label": "PageSpeed Audit"},
        {"href": "/pricing/", "label": "Pricing"},
    ],
    "Industries": [
        {"href": "/for/medical-device-companies/", "label": "Medical Devices"},
        {"href": "/for/pharma-field-marketing/", "label": "Pharma"},
        {"href": "/for/b2b-saas/", "label": "B2B SaaS"},
        {"href": "/for/conference-organizers/", "label": "Conferences"},
        {"href": "/for/med-spas/", "label": "Med Spas"},
        {"href": "/for/real-estate/", "label": "Real Estate"},
        {"href": "/for/healthcare-practices/", "label": "Healthcare"},
        {"href": "/for/law-firms/", "label": "Law Firms"},
        {"href": "/for/home-services/", "label": "Home Services"},
        {"href": "/for/professional-services/", "label": "Professional Services"},
        {"href": "/for/startups/", "label": "Startups"},
        {"href": "/for/franchise-multi-location/", "label": "Franchise"},
    ],
    "Resources": [
        {"href": "/blog/", "label": "Blog"},
        {"href": "/audit/", "label": "Free Site Audit"},
        {"href": "/about/", "label": "About"},
    ],
    "Legal": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
}
