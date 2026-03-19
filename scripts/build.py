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
    write_page,
    BASE_URL,
    OUTPUT_DIR,
)
from nav_config import SITE_NAME, SITE_URL


# Project root (one level up from scripts/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All pages: (path, priority, changefreq) tuples for sitemap generation
ALL_PAGES = []


# =============================================================================
# PAGE BUILDERS
# =============================================================================

def build_homepage():
    """Build the homepage with hero section and CTA."""
    body = '''
        <section class="section hero">
            <div class="container">
                <h1 class="hero__title">Sharp pages. Full rooms.</h1>
                <p class="hero__subtitle">We build event registration sites and run the ads to fill them. You just run the event.</p>
                <a href="/contact/" class="btn btn--primary btn--lg">Book a Call</a>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Event Registration Sites That Fill Rooms",
        description="SharpPages builds high-converting event registration sites and runs ad campaigns to fill seats. Page, pixels, and paid media handled.",
        canonical_path="/",
        body_content=body,
    )
    write_page("index.html", html)
    ALL_PAGES.append(("/", 1.0, "weekly"))


def build_about():
    """Build the about page with breadcrumbs and schema."""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": "About", "url": BASE_URL + "/about/"},
    ]

    breadcrumb_nav = get_breadcrumb_html(breadcrumbs)
    breadcrumb_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        {breadcrumb_nav}
        <section class="section">
            <div class="container">
                <h1>About SharpPages</h1>
                <p>SharpPages was built by Rome Thorndike to give event organizers sharp registration pages and full rooms without the agency overhead. We handle everything: the page, the pixels, and the paid media.</p>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="About SharpPages",
        description="SharpPages was built by Rome Thorndike to give event organizers sharp registration pages and full rooms without the agency overhead.",
        canonical_path="/about/",
        body_content=body,
        active_page="/about/",
        extra_schema=breadcrumb_schema,
    )
    write_page("about/index.html", html)
    ALL_PAGES.append(("/about/", 0.8, "monthly"))


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
    build_about()

    # Static assets
    copy_static_assets()

    # SEO files
    build_sitemap()
    build_robots_txt()
    build_cname()

    print(f"Build complete: {len(ALL_PAGES)} pages generated")


if __name__ == "__main__":
    main()
