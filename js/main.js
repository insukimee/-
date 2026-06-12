(function () {
  'use strict';

  // ── Hamburger / Mobile Nav ─────────────────────────────────────────────────
  const hamburger = document.getElementById('hamburger-btn');
  const mobileNav = document.getElementById('mobile-nav');
  const navOverlay = document.getElementById('nav-overlay');

  function closeNav() {
    hamburger && hamburger.classList.remove('open');
    mobileNav && mobileNav.classList.remove('open');
    navOverlay && navOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  function toggleNav() {
    const isOpen = mobileNav && mobileNav.classList.contains('open');
    if (isOpen) {
      closeNav();
    } else {
      hamburger && hamburger.classList.add('open');
      mobileNav && mobileNav.classList.add('open');
      navOverlay && navOverlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  if (hamburger) hamburger.addEventListener('click', toggleNav);
  if (navOverlay) navOverlay.addEventListener('click', closeNav);

  // Close nav on link tap
  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeNav);
    });
  }

  // ── Cookie Banner ──────────────────────────────────────────────────────────
  const cookieBanner = document.getElementById('cookie-banner');
  const cookieAccept = document.getElementById('cookie-accept');
  const COOKIE_KEY = 'mi_cookie_consent';

  function setCookieConsent() {
    try {
      localStorage.setItem(COOKIE_KEY, '1');
    } catch (_) {}
    if (cookieBanner) cookieBanner.classList.remove('show');
  }

  if (cookieBanner) {
    try {
      const hasConsent = localStorage.getItem(COOKIE_KEY);
      if (!hasConsent) {
        setTimeout(function () {
          cookieBanner.classList.add('show');
        }, 800);
      }
    } catch (_) {}
  }

  if (cookieAccept) cookieAccept.addEventListener('click', setCookieConsent);

  // ── Intersection Observer – animate-on-scroll ──────────────────────────────
  var ioOptions = { threshold: 0.1, rootMargin: '0px 0px -40px 0px' };

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, ioOptions);

  document.querySelectorAll('.animate-on-scroll').forEach(function (el) {
    observer.observe(el);
  });

  // Stagger parent containers
  var staggerObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        staggerObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  document.querySelectorAll('.stagger-children').forEach(function (el) {
    staggerObserver.observe(el);
  });

  // ── Contact form (no-op handler) ───────────────────────────────────────────
  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = contactForm.querySelector('.submit-btn');
      if (btn) {
        btn.textContent = btn.getAttribute('data-success') || 'Sent';
        btn.disabled = true;
      }
    });
  }
})();
