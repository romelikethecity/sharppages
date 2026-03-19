---
phase: 1
slug: foundation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-19
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | bash scripts (build verification) |
| **Config file** | none — shell commands only |
| **Quick run command** | `cd /Users/rome/Documents/projects/sharppages && python3 scripts/build.py` |
| **Full suite command** | `python3 scripts/build.py && python3 -c "import os; files=[f for dp,dn,fn in os.walk('output') for f in fn if f.endswith('.html')]; print(f'{len(files)} HTML files')"` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python3 scripts/build.py`
- **After every plan wave:** Run full suite command + manual browser check
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | INFR-04 | file check | `test -d logos && test -d favicons && test -f tokens.css` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 1 | INFR-02 | import | `python3 -c "from scripts.nav_config import SITE_NAME, NAV_ITEMS"` | ❌ W0 | ⬜ pending |
| 01-01-03 | 01 | 1 | INFR-03 | import | `python3 -c "from scripts.templates import get_page_wrapper, write_page"` | ❌ W0 | ⬜ pending |
| 01-01-04 | 01 | 1 | INFR-05 | file check | `test -f css/styles.css` | ❌ W0 | ⬜ pending |
| 01-01-05 | 01 | 1 | INFR-09 | file check | `test -f js/main.js` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | INFR-01 | build | `python3 scripts/build.py` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 1 | SEO-01 | grep | `grep -c '<title>' output/index.html` | ❌ W0 | ⬜ pending |
| 01-02-03 | 02 | 1 | SEO-03 | grep | `grep 'canonical' output/index.html` | ❌ W0 | ⬜ pending |
| 01-02-04 | 02 | 1 | SEO-07 | grep | `grep 'BreadcrumbList' output/about/index.html` | ❌ W0 | ⬜ pending |
| 01-02-05 | 02 | 1 | INFR-07 | file check | `test -f output/sitemap.xml` | ❌ W0 | ⬜ pending |
| 01-02-06 | 02 | 1 | INFR-08 | file check | `test -f output/robots.txt` | ❌ W0 | ⬜ pending |
| 01-02-07 | 02 | 1 | INFR-06 | file check | `test -f output/CNAME && cat output/CNAME` | ❌ W0 | ⬜ pending |
| 01-02-08 | 02 | 1 | INFR-10 | grep | `grep 'gtag' output/index.html` | ❌ W0 | ⬜ pending |
| 01-02-09 | 02 | 1 | PERF-05 | grep | `grep 'preconnect' output/index.html && grep 'display=swap' output/index.html` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] All files created by plan execution — no pre-existing test infrastructure needed
- [ ] Verification is via build success + grep/file checks on output

*Existing infrastructure covers all phase requirements via build output inspection.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Brand palette renders correctly | INFR-04, PERF-01 | Visual check | Open output/index.html in browser, verify Midnight bg, Cyan accents, Gold highlights |
| Mobile nav toggle works | INFR-09 | Interaction | Resize browser to 768px, click hamburger, verify menu opens/closes |
| FAQ accordion works | INFR-09 | Interaction | Click FAQ question, verify answer expands/collapses |
| Lighthouse scores | PERF-01, PERF-02, PERF-03 | Tool | Run Lighthouse on served page, verify Perf 90+, A11y 90+, SEO 100 |

---

## Validation Sign-Off

- [ ] All tasks have automated verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
