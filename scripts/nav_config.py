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
SITE_TAGLINE = "Sharp pages. Full rooms."
COPYRIGHT_YEAR = "2026"

# CTA button
CTA_HREF = "/contact/"
CTA_LABEL = "Book a Call"

# Main navigation items (appear in header)
NAV_ITEMS = [
    {"href": "/services/", "label": "Services"},
    {"href": "/pricing/", "label": "Pricing"},
    {"href": "/work/", "label": "Work"},
    {"href": "/about/", "label": "About"},
    {"href": "/blog/", "label": "Blog"},
]

# Footer link columns
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
