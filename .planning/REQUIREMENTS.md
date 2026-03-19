# Requirements: SharpPages

**Defined:** 2026-03-19
**Core Value:** sharppages.com clearly communicates that SharpPages handles everything (page + pixels + paid media) and drives event organizers to inquire.

## v1 Requirements

### Infrastructure

- [ ] **INFR-01**: Python build system generates all pages via `python3 scripts/build.py`
- [ ] **INFR-02**: nav_config.py is single source of truth for nav links, site info, footer columns
- [ ] **INFR-03**: templates.py provides shared HTML generators (head, nav, footer, breadcrumbs, FAQ, CTA, schema)
- [ ] **INFR-04**: Brand assets (tokens.css, logos, favicons, OG images, webmanifest) copied into project
- [ ] **INFR-05**: Single CSS file with BEM naming, cache busting via ?v=N
- [ ] **INFR-06**: CNAME file for sharppages.com
- [ ] **INFR-07**: Sitemap.xml auto-generated with correct priorities (homepage 1.0, services 0.9, /for/ 0.8, blog 0.7, static 0.5)
- [ ] **INFR-08**: robots.txt generated with AI crawler allowances (GPTBot, ClaudeBot, PerplexityBot)
- [ ] **INFR-09**: Minimal JS for mobile nav toggle, FAQ accordion, form validation
- [ ] **INFR-10**: GA4 tracking placeholder in every page head

### Homepage

- [ ] **HOME-01**: Title follows hook formula (Value + Objection), under 8 words
- [ ] **HOME-02**: Subtitle explains how SharpPages creates the value
- [ ] **HOME-03**: Visual shows real product (btlmichigan.com screenshot or similar)
- [ ] **HOME-04**: Social proof with specific, falsifiable metrics (5-day turnaround, etc.)
- [ ] **HOME-05**: Primary CTA is call-to-value (not "Get Started")
- [ ] **HOME-06**: Features & Objections section makes value concrete
- [ ] **HOME-07**: Case study social proof below the fold
- [ ] **HOME-08**: FAQ section with minimum 5 questions + FAQPage schema
- [ ] **HOME-09**: Second CTA reinforcing value proposition
- [ ] **HOME-10**: Founder's note (Rome, in their shoes, problem → happy ending)

### Services Page

- [ ] **SERV-01**: Event registration site service with what's included, process, 5-7 day timeline
- [ ] **SERV-02**: Paid social ad management service (Facebook retargeting, custom audiences, reporting)
- [ ] **SERV-03**: Tracking setup service (GA4, Meta Pixel, conversion tracking)
- [ ] **SERV-04**: Full-loop positioning (site + ads + tracking as one package)
- [ ] **SERV-05**: FAQ section with 5+ questions + FAQPage schema
- [ ] **SERV-06**: Service schema markup (JSON-LD)

### Pricing Page

- [ ] **PRIC-01**: Site build pricing ($3,500-$5,000 first, $1,500-$2,500 additional)
- [ ] **PRIC-02**: Ad management pricing ($1,500-$2,500/mo retainer + $500-$1,000 setup)
- [ ] **PRIC-03**: Bundle pricing (single event, multi-city, ongoing)
- [ ] **PRIC-04**: "No platform fees, no per-registrant charges, no annual contracts" messaging
- [ ] **PRIC-05**: All pricing rendered from single PRICING data structure in build.py
- [ ] **PRIC-06**: FAQ section + FAQPage schema

### Work/Portfolio Page

- [ ] **WORK-01**: Anonymized BTL Michigan case study ("Medical Device Manufacturer — Detroit Event")
- [ ] **WORK-02**: Real results (registration numbers, mobile responsiveness, 5-day turnaround)
- [ ] **WORK-03**: Replication story (same template → second city in 48 hours)

### About Page

- [ ] **ABOU-01**: Rome's background (Datajoy → Databricks, Microsoft, Salesforce, Snapdocs, UC Berkeley Haas MBA)
- [ ] **ABOU-02**: Framing as data + marketing + engineering in one person
- [ ] **ABOU-03**: Why SharpPages exists (agencies slow/expensive, DIY tools require expertise, generic platforms kill conversions)

### Contact Page

- [ ] **CONT-01**: Formspree form with honeypot (_gotcha field)
- [ ] **CONT-02**: Fields: name, email, company, event type dropdown, message
- [ ] **CONT-03**: Privacy note linking to privacy page

### Legal Pages

- [ ] **LEGL-01**: Privacy policy page
- [ ] **LEGL-02**: Terms of service page

### ICP Pages

- [ ] **ICP-01**: /for/medical-device-companies/ (city-by-city lunch-and-learns, product demos, KOL dinners)
- [ ] **ICP-02**: /for/pharma-field-marketing/ (speaker programs, advisory boards, compliance)
- [ ] **ICP-03**: /for/b2b-saas/ (roadshows, user groups, partner summits)
- [ ] **ICP-04**: /for/conference-organizers/ (can't justify Cvent, need more than Eventbrite)
- [ ] **ICP-05**: /for/med-spas/ (grand openings, patient acquisition events)
- [ ] **ICP-06**: /for/real-estate/ (property launches, investor events, broker previews)
- [ ] **ICP-07**: Each ICP page has 1,200+ words, pain-first opening, workflow scenarios, pricing context, FAQ (3+), CTA, internal links

### Blog

- [ ] **BLOG-01**: Blog index page listing all articles
- [ ] **BLOG-02**: "Why Your Event Registration Page Is Losing Signups" (pain-first, top funnel, 1,500-2,000 words)
- [ ] **BLOG-03**: "Eventbrite vs Custom Event Sites: What Converts Better" (comparison, mid funnel)
- [ ] **BLOG-04**: "How Facebook Retargeting Fills Event Seats" (educational, mid funnel)
- [ ] **BLOG-05**: "The Real Cost of Event Marketing: DIY vs Done-For-You" (pricing comparison, bottom funnel)
- [ ] **BLOG-06**: Each blog has unique title (50-60 chars), unique meta, H1 with keyword, 2+ outbound links, 3+ internal links, FAQ section, FAQPage schema, author byline

### SEO

- [ ] **SEO-01**: Every page has unique title (50-60 chars), keyword-first, hyphens not pipes
- [ ] **SEO-02**: Every page has unique meta description (150-158 chars), action-oriented
- [ ] **SEO-03**: Every page has canonical URL to https://sharppages.com/{path}/
- [ ] **SEO-04**: OG tags on every page (og:type, og:url, og:title, og:description, og:site_name, og:image)
- [ ] **SEO-05**: Twitter Card on every page (summary_large_image)
- [ ] **SEO-06**: Homepage schema: Organization + WebSite + FAQPage
- [ ] **SEO-07**: All inner pages: BreadcrumbList schema
- [ ] **SEO-08**: Pages with FAQs: FAQPage schema matching visible content exactly
- [ ] **SEO-09**: Blog articles: Article schema with author (Rome Thorndike)
- [ ] **SEO-10**: Service pages: Service schema
- [ ] **SEO-11**: 3+ internal links per page beyond nav/footer
- [ ] **SEO-12**: E-E-A-T: author attribution, specific numbers, outbound links (2+ per content page)

### Content Quality

- [ ] **QUAL-01**: Zero AI writing tells (no em-dashes, no false reframes, no banned words)
- [ ] **QUAL-02**: Every number sourced (BTL case study, citable source, or real pricing)
- [ ] **QUAL-03**: No specific dates in copy (use relative language)
- [ ] **QUAL-04**: CURRENT_YEAR variable for any year references
- [ ] **QUAL-05**: No "coming soon" sections

### Performance

- [ ] **PERF-01**: Lighthouse Performance 90+
- [ ] **PERF-02**: Lighthouse Accessibility 90+
- [ ] **PERF-03**: Lighthouse SEO 100
- [ ] **PERF-04**: All images have width + height attributes
- [ ] **PERF-05**: Google Fonts preconnect + display=swap
- [ ] **PERF-06**: Below-fold images lazy loaded

## v2 Requirements

### Analytics & Tracking
- **V2-01**: GA4 property created and tracking live
- **V2-02**: Google Search Console verified
- **V2-03**: Meta Pixel on marketing site (for retargeting site visitors)

### Content Expansion
- **V2-04**: Additional blog articles (event marketing content strategy from Provyx handoff)
- **V2-05**: Testimonial section (after BTL Detroit March 21 feedback)
- **V2-06**: Additional case studies as clients close

### Features
- **V2-07**: Newsletter signup integration
- **V2-08**: Additional ICP pages based on inbound demand

## Out of Scope

| Feature | Reason |
|---------|--------|
| SaaS platform / client portal | Marketing site only. Service is done-for-you, not self-serve. |
| Payment / checkout | High-ticket service sold via conversation, not e-commerce |
| Event template hosting | Separate repo (btl-events). This site markets the service. |
| CMS / admin panel | Static site. Content updates via build.py edits. |
| Blog comments | No engagement layer needed for v1 |
| Multi-language | English-only market |
| Dark/light mode toggle | Dark theme is the brand. No toggle. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFR-01 | Phase 1 | Pending |
| INFR-02 | Phase 1 | Pending |
| INFR-03 | Phase 1 | Pending |
| INFR-04 | Phase 1 | Pending |
| INFR-05 | Phase 1 | Pending |
| INFR-06 | Phase 1 | Pending |
| INFR-07 | Phase 1 | Pending |
| INFR-08 | Phase 1 | Pending |
| INFR-09 | Phase 1 | Pending |
| INFR-10 | Phase 1 | Pending |
| HOME-01 | Phase 2 | Pending |
| HOME-02 | Phase 2 | Pending |
| HOME-03 | Phase 2 | Pending |
| HOME-04 | Phase 2 | Pending |
| HOME-05 | Phase 2 | Pending |
| HOME-06 | Phase 2 | Pending |
| HOME-07 | Phase 2 | Pending |
| HOME-08 | Phase 2 | Pending |
| HOME-09 | Phase 2 | Pending |
| HOME-10 | Phase 2 | Pending |
| SERV-01 | Phase 2 | Pending |
| SERV-02 | Phase 2 | Pending |
| SERV-03 | Phase 2 | Pending |
| SERV-04 | Phase 2 | Pending |
| SERV-05 | Phase 2 | Pending |
| SERV-06 | Phase 2 | Pending |
| PRIC-01 | Phase 2 | Pending |
| PRIC-02 | Phase 2 | Pending |
| PRIC-03 | Phase 2 | Pending |
| PRIC-04 | Phase 2 | Pending |
| PRIC-05 | Phase 2 | Pending |
| PRIC-06 | Phase 2 | Pending |
| WORK-01 | Phase 2 | Pending |
| WORK-02 | Phase 2 | Pending |
| WORK-03 | Phase 2 | Pending |
| ABOU-01 | Phase 2 | Pending |
| ABOU-02 | Phase 2 | Pending |
| ABOU-03 | Phase 2 | Pending |
| CONT-01 | Phase 2 | Pending |
| CONT-02 | Phase 2 | Pending |
| CONT-03 | Phase 2 | Pending |
| LEGL-01 | Phase 2 | Pending |
| LEGL-02 | Phase 2 | Pending |
| ICP-01 | Phase 3 | Pending |
| ICP-02 | Phase 3 | Pending |
| ICP-03 | Phase 3 | Pending |
| ICP-04 | Phase 3 | Pending |
| ICP-05 | Phase 3 | Pending |
| ICP-06 | Phase 3 | Pending |
| ICP-07 | Phase 3 | Pending |
| BLOG-01 | Phase 3 | Pending |
| BLOG-02 | Phase 3 | Pending |
| BLOG-03 | Phase 3 | Pending |
| BLOG-04 | Phase 3 | Pending |
| BLOG-05 | Phase 3 | Pending |
| BLOG-06 | Phase 3 | Pending |
| SEO-01 | Phase 1 | Pending |
| SEO-02 | Phase 1 | Pending |
| SEO-03 | Phase 1 | Pending |
| SEO-04 | Phase 1 | Pending |
| SEO-05 | Phase 1 | Pending |
| SEO-06 | Phase 2 | Pending |
| SEO-07 | Phase 1 | Pending |
| SEO-08 | Phase 2 | Pending |
| SEO-09 | Phase 3 | Pending |
| SEO-10 | Phase 2 | Pending |
| SEO-11 | Phase 2 | Pending |
| SEO-12 | Phase 2 | Pending |
| QUAL-01 | Phase 2 | Pending |
| QUAL-02 | Phase 2 | Pending |
| QUAL-03 | Phase 2 | Pending |
| QUAL-04 | Phase 1 | Pending |
| QUAL-05 | Phase 2 | Pending |
| PERF-01 | Phase 1 | Pending |
| PERF-02 | Phase 1 | Pending |
| PERF-03 | Phase 1 | Pending |
| PERF-04 | Phase 2 | Pending |
| PERF-05 | Phase 1 | Pending |
| PERF-06 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 68 total
- Mapped to phases: 68
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-19*
*Last updated: 2026-03-19 after initial definition*
