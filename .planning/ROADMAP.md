# Roadmap: SharpPages

## Overview

SharpPages marketing site ships in 3 phases: build system and brand foundation first, then all core pages (homepage through legal) with full SEO and schema, then ICP industry pages and blog content for long-tail organic reach. Every phase produces a deployable site -- Phase 1 is a working skeleton, Phase 2 is a complete marketing site, Phase 3 adds content depth for SEO.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation** - Build system, brand assets, templates, and infrastructure that every page depends on
- [ ] **Phase 2: Core Pages** - Homepage, services, pricing, work, about, contact, and legal pages with full SEO and schema
- [ ] **Phase 3: Content Expansion** - 6 ICP industry pages, 4 blog articles, blog index, and deployment

## Phase Details

### Phase 1: Foundation
**Goal**: A working build system that generates a deployable site skeleton with brand styling, shared templates, SEO defaults, and performance baselines
**Depends on**: Nothing (first phase)
**Requirements**: INFR-01, INFR-02, INFR-03, INFR-04, INFR-05, INFR-06, INFR-07, INFR-08, INFR-09, INFR-10, SEO-01, SEO-02, SEO-03, SEO-04, SEO-05, SEO-07, QUAL-04, PERF-01, PERF-02, PERF-03, PERF-05
**Success Criteria** (what must be TRUE):
  1. Running `python3 scripts/build.py` produces an output/ directory with valid HTML, CSS, CNAME, sitemap.xml, and robots.txt
  2. Generated pages render with Midnight/Cyan/Gold brand palette, Instrument Sans + DM Sans fonts, and the SharpPages logo
  3. Every generated page has unique meta title, meta description, canonical URL, OG tags, Twitter Card, BreadcrumbList schema, and GA4 placeholder in head
  4. Mobile nav toggle, FAQ accordion, and form validation JS work on mobile and desktop
  5. A placeholder page scores Lighthouse Performance 90+, Accessibility 90+, SEO 100 with Google Fonts preconnected and display=swap
**Plans**: TBD

Plans:
- [ ] 01-01: TBD
- [ ] 01-02: TBD

### Phase 2: Core Pages
**Goal**: A complete marketing site with homepage, services, pricing, work, about, contact, privacy, and terms pages -- each with real copy, proper schema, and conversion-driving CTAs
**Depends on**: Phase 1
**Requirements**: HOME-01, HOME-02, HOME-03, HOME-04, HOME-05, HOME-06, HOME-07, HOME-08, HOME-09, HOME-10, SERV-01, SERV-02, SERV-03, SERV-04, SERV-05, SERV-06, PRIC-01, PRIC-02, PRIC-03, PRIC-04, PRIC-05, PRIC-06, WORK-01, WORK-02, WORK-03, ABOU-01, ABOU-02, ABOU-03, CONT-01, CONT-02, CONT-03, LEGL-01, LEGL-02, SEO-06, SEO-08, SEO-10, SEO-11, SEO-12, QUAL-01, QUAL-02, QUAL-03, QUAL-05, PERF-04, PERF-06
**Success Criteria** (what must be TRUE):
  1. Visitor lands on homepage and sees a clear hook (under 8 words), visual proof of the product, social proof with specific numbers, and a call-to-value CTA -- all above the fold
  2. Visitor can navigate from homepage to services, pricing, work, about, or contact and find complete, substantive content on each (500+ words on core pages, 1,200+ on services)
  3. Pricing page renders all tiers from a single PRICING data structure and changing one number in build.py updates every page that references pricing
  4. Contact form submits via Formspree with honeypot, validation, and privacy link -- no backend required
  5. Every page passes zero-AI-tells check (no em-dashes, no banned words), every number is sourced, no specific dates appear in copy, and no "coming soon" sections exist
**Plans**: TBD

Plans:
- [ ] 02-01: TBD
- [ ] 02-02: TBD
- [ ] 02-03: TBD

### Phase 3: Content Expansion
**Goal**: 6 ICP industry pages and 4 blog articles that capture long-tail organic traffic and position SharpPages for specific verticals, plus deployment to sharppages.com
**Depends on**: Phase 2
**Requirements**: ICP-01, ICP-02, ICP-03, ICP-04, ICP-05, ICP-06, ICP-07, BLOG-01, BLOG-02, BLOG-03, BLOG-04, BLOG-05, BLOG-06, SEO-09
**Success Criteria** (what must be TRUE):
  1. Each of the 6 ICP pages at /for/{vertical}/ has 1,200+ words with pain-first opening, workflow scenarios specific to that industry, pricing context, 3+ FAQ questions with FAQPage schema, CTA, and 3+ internal links
  2. Blog index at /blog/ lists all 4 articles with titles, descriptions, and publish dates
  3. Each blog article has 1,500-2,000 words, unique meta tags, H1 with target keyword, 2+ outbound links to authoritative sources, 3+ internal links, FAQ section, FAQPage schema, Article schema with author, and author byline
  4. Site is deployed to sharppages.com via GitHub Pages with CNAME, and all pages are accessible at their canonical URLs

**Plans**: TBD

Plans:
- [ ] 03-01: TBD
- [ ] 03-02: TBD
- [ ] 03-03: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/0 | Not started | - |
| 2. Core Pages | 0/0 | Not started | - |
| 3. Content Expansion | 0/0 | Not started | - |
