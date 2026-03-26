/**
 * SharpPages - Main JavaScript
 * Header scroll, smooth scroll, form validation, GA4 helper,
 * scroll-triggered animations, mobile nav, audit tool.
 */
(function() {
  'use strict';
  var header = document.querySelector('.header');

  // Header shadow on scroll
  if (header) {
    window.addEventListener('scroll', function() {
      header.classList.toggle('header--scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  // Mobile menu toggle
  var menuToggle = document.querySelector('.menu-toggle');
  var mobileNav = document.querySelector('.nav--mobile');
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function() {
      menuToggle.classList.toggle('active');
      mobileNav.classList.toggle('active');
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var id = this.getAttribute('href');
      if (id === '#') return;
      var el = document.querySelector(id);
      if (el) {
        e.preventDefault();
        window.scrollTo({ top: el.getBoundingClientRect().top + window.pageYOffset - (header ? header.offsetHeight : 0), behavior: 'smooth' });
      }
    });
  });

  // Form validation with honeypot support
  document.querySelectorAll('form:not(#audit-form)').forEach(function(form) {
    form.addEventListener('submit', function(e) {
      var hp = form.querySelector('[name="_gotcha"]');
      if (hp && hp.value) { e.preventDefault(); return; }
      var ok = true;
      form.querySelectorAll('.form__error').forEach(function(el) { el.remove(); });
      form.querySelectorAll('[required]').forEach(function(input) {
        input.classList.remove('form__input--error');
        var msg = '';
        if (!input.value.trim()) msg = 'This field is required.';
        else if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) msg = 'Enter a valid email address.';
        if (msg) {
          ok = false; input.classList.add('form__input--error');
          var err = document.createElement('div'); err.className = 'form__error'; err.textContent = msg;
          input.parentNode.appendChild(err);
        }
      });
      if (!ok) { e.preventDefault(); return; }
      var btn = form.querySelector('[type="submit"]');
      if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
      trackEvent('form_submitted', 'engagement', 'contact');
    });
  });

  // GA4 event helper
  function trackEvent(action, category, label) {
    if (typeof gtag === 'function') gtag('event', action, { event_category: category, event_label: label });
  }
  window.trackEvent = trackEvent;

  // =========================================================================
  // SCROLL-TRIGGERED ANIMATIONS (Intersection Observer)
  // =========================================================================

  if ('IntersectionObserver' in window) {

    // Gauge animations (PageSpeed comparison circles) — support multiple on page
    var gaugeComparisons = document.querySelectorAll('.gauge-comparison[data-animate]');
    if (gaugeComparisons.length) {
      var gaugeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          gaugeObserver.unobserve(entry.target);
          animateGauges(entry.target);
        });
      }, { threshold: 0.3 });
      gaugeComparisons.forEach(function(gc) { gaugeObserver.observe(gc); });
    }

    // Multi-city clone animation
    var multiCities = document.querySelectorAll('.multi-city[data-animate]');
    if (multiCities.length) {
      var cityObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          cityObserver.unobserve(entry.target);
          entry.target.classList.add('animated');
        });
      }, { threshold: 0.3 });
      multiCities.forEach(function(mc) { cityObserver.observe(mc); });
    }

    // SEO chart animation (support multiple on page)
    var seoCharts = document.querySelectorAll('.seo-chart[data-animate]');
    if (seoCharts.length) {
      var chartObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          chartObserver.unobserve(entry.target);
          entry.target.classList.add('animated');
        });
      }, { threshold: 0.3 });
      seoCharts.forEach(function(chart) { chartObserver.observe(chart); });
    }

    // Cost comparison bar animation
    var costBars = document.querySelectorAll('.cost-comparison[data-animate]');
    if (costBars.length) {
      var costObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          costObserver.unobserve(entry.target);
          var fills = entry.target.querySelectorAll('.cost-comparison__fill');
          fills.forEach(function(fill) {
            var targetWidth = fill.getAttribute('data-width');
            if (targetWidth) fill.style.width = targetWidth;
          });
        });
      }, { threshold: 0.3 });
      costBars.forEach(function(bar) { costObserver.observe(bar); });
    }
  }

  function animateGauges(container) {
    var gauges = container.querySelectorAll('.gauge');
    gauges.forEach(function(gauge) {
      var score = parseInt(gauge.getAttribute('data-score'), 10);
      var fill = gauge.querySelector('.gauge__fill');
      var scoreEl = gauge.querySelector('.gauge__score');

      // circumference = 2 * PI * 54 = 339.29
      var circumference = 339.29;
      var offset = circumference - (score / 100) * circumference;

      // Animate the ring
      requestAnimationFrame(function() {
        fill.style.strokeDashoffset = offset;
      });

      // Count up the number
      var current = 0;
      var duration = 1500;
      var start = performance.now();
      function step(timestamp) {
        var progress = Math.min((timestamp - start) / duration, 1);
        current = Math.round(progress * score);
        scoreEl.textContent = current;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  // =========================================================================
  // AUDIT TOOL
  // =========================================================================

  var auditForm = document.getElementById('audit-form');
  if (auditForm) {
    var AUDIT_API = 'https://sharppages-audit.rome-workers.workers.dev';

    auditForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var urlInput = document.getElementById('audit-url');
      var url = urlInput.value.trim();
      if (!url) return;

      // Ensure https://
      if (!/^https?:\/\//i.test(url)) url = 'https://' + url;

      showElement('audit-loading');
      hideElement('audit-form');
      hideElement('audit-results');
      hideElement('audit-error');

      trackEvent('audit_started', 'engagement', url);

      fetch(AUDIT_API + '?url=' + encodeURIComponent(url))
        .then(function(res) { return res.json(); })
        .then(function(data) {
          hideElement('audit-loading');
          if (data.error) {
            showAuditError(data.error);
            return;
          }
          renderAuditResults(data, url);
          showElement('audit-results');
          trackEvent('audit_completed', 'engagement', url);
        })
        .catch(function(err) {
          hideElement('audit-loading');
          showAuditError('Could not reach the audit service. Try again in a moment.');
          trackEvent('audit_error', 'engagement', err.message);
        });
    });
  }

  function renderAuditResults(data, url) {
    // PageSpeed scores
    if (data.pagespeed && !data.pagespeed.error) {
      var scores = data.pagespeed.scores;
      animateAuditScore('score-performance', scores.performance);
      animateAuditScore('score-accessibility', scores.accessibility);
      animateAuditScore('score-best-practices', scores.bestPractices);
      animateAuditScore('score-seo', scores.seo);

      // Metrics
      var metrics = data.pagespeed.metrics;
      setText('metric-speed-index', metrics.speedIndex || '--');
      setText('metric-lcp', metrics.lcp || '--');
      setText('metric-cls', metrics.cls || '--');
      setText('metric-tbt', metrics.tbt || '--');

      // CTA score
      var ctaScore = document.getElementById('audit-cta-score');
      var ctaScoreHidden = document.getElementById('audit-cta-score-hidden');
      var ctaUrl = document.getElementById('audit-cta-url');
      if (ctaScore) ctaScore.textContent = scores.performance;
      if (ctaScoreHidden) ctaScoreHidden.value = scores.performance;
      if (ctaUrl) ctaUrl.value = url;
    }

    // SEO checks
    if (data.seo && !data.seo.error) {
      renderSeoChecklist(data.seo);
    }
  }

  function animateAuditScore(containerId, score) {
    var container = document.getElementById(containerId);
    if (!container) return;

    var ring = container.querySelector('.audit-score__ring');
    var valueEl = container.querySelector('.audit-score__value');
    var circumference = 339.292;

    // Set color based on score
    var color = score >= 90 ? '#0cce6b' : score >= 50 ? '#ffa400' : '#ff4e42';
    ring.style.stroke = color;
    valueEl.style.color = color;

    // Animate ring
    var offset = circumference - (score / 100) * circumference;
    requestAnimationFrame(function() {
      ring.style.strokeDashoffset = offset;
    });

    // Count up
    var start = performance.now();
    function step(ts) {
      var progress = Math.min((ts - start) / 1200, 1);
      valueEl.textContent = Math.round(progress * score);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function renderSeoChecklist(seo) {
    var checklist = document.getElementById('seo-checklist');
    if (!checklist) return;
    checklist.innerHTML = '';

    var checks = [
      { key: 'title', label: 'Title tag', detail: seo.title },
      { key: 'metaDescription', label: 'Meta description', detail: seo.metaDescription },
      { key: 'h1', label: 'H1 heading', detail: seo.h1 },
      { key: 'viewport', label: 'Mobile viewport', detail: seo.viewport },
      { key: 'canonical', label: 'Canonical URL', detail: seo.canonical },
      { key: 'ogTags', label: 'Open Graph tags', detail: seo.ogTags },
      { key: 'schema', label: 'Schema markup', detail: seo.schema },
    ];

    checks.forEach(function(check) {
      if (!check.detail) return;
      var status = check.detail.status || 'red';
      var icon = status === 'green' ? '\u2713' : status === 'yellow' ? '!' : '\u2717';

      var div = document.createElement('div');
      div.className = 'seo-check';
      div.innerHTML = '<span class="seo-check__icon seo-check__icon--' + status + '">' + icon + '</span>' +
        '<span class="seo-check__text">' + check.label +
        (check.detail.value ? ': ' + escapeHtml(check.detail.value.substring(0, 80)) : '') +
        '</span>';
      checklist.appendChild(div);
    });
  }

  // Helpers
  function showElement(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = '';
  }

  function hideElement(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = 'none';
  }

  function setText(id, text) {
    var el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function showAuditError(msg) {
    var el = document.getElementById('audit-error-message');
    if (el) el.textContent = msg;
    showElement('audit-error');
    showElement('audit-form');
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

})();
