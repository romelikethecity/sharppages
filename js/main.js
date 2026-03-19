/**
 * SharpPages - Main JavaScript
 * Header scroll, smooth scroll, form validation, GA4 helper.
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
  document.querySelectorAll('form').forEach(function(form) {
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
})();
