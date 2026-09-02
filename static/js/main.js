// IIC-IEM – main.js

// ── Official Institutional Preloader Handler ──
function dismissPreloader() {
  const loader = document.getElementById('preloader');
  if (loader) {
    loader.classList.add('hidden');
    loader.style.opacity = '0';
    loader.style.pointerEvents = 'none';
    setTimeout(() => { loader.style.display = 'none'; }, 300);
  }
}
window.addEventListener('load', dismissPreloader);
document.addEventListener('DOMContentLoaded', () => { setTimeout(dismissPreloader, 400); });
setTimeout(dismissPreloader, 800);

// Auto-dismiss toast messages after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      el.style.transition = '0.4s ease';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });

  // Mobile Navigation & Touch Gestures
  const toggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  function openMenu() {
    if (navLinks) navLinks.classList.add('open');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
  }

  function closeMenu() {
    if (navLinks) navLinks.classList.remove('open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }

  if (toggle && navLinks) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      navLinks.classList.contains('open') ? closeMenu() : openMenu();
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (navLinks.classList.contains('open')) {
        if (!navLinks.contains(e.target) && !toggle.contains(e.target)) {
          closeMenu();
        }
      }
    });

    // Close menu when tapping outside on touch devices
    document.addEventListener('touchstart', (e) => {
      if (navLinks.classList.contains('open')) {
        if (!navLinks.contains(e.target) && !toggle.contains(e.target)) {
          closeMenu();
        }
      }
    }, { passive: true });

    // Escape key closes mobile menu
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks.classList.contains('open')) {
        closeMenu();
      }
    });

    // Touch Swipe Gestures (Swipe Up or Left to close menu)
    let touchStartY = 0;
    let touchStartX = 0;

    navLinks.addEventListener('touchstart', (e) => {
      touchStartY = e.touches[0].clientY;
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    navLinks.addEventListener('touchend', (e) => {
      if (!navLinks.classList.contains('open')) return;
      const touchEndY = e.changedTouches[0].clientY;
      const touchEndX = e.changedTouches[0].clientX;

      const diffY = touchStartY - touchEndY; // Swiped Up
      const diffX = touchStartX - touchEndX; // Swiped Left

      if (diffY > 40 || Math.abs(diffX) > 60) {
        closeMenu();
      }
    }, { passive: true });
  }

  // Mobile Footer Accordion Toggle
  document.querySelectorAll('.footer-accordion-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        const section = btn.closest('.footer-section');
        if (section) {
          section.classList.toggle('active');
        }
      }
    });
  });

  // Active nav link highlighting
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath ||
        (link.getAttribute('href') !== '/' && currentPath.startsWith(link.getAttribute('href')))) {
      link.classList.add('active');
    }
  });
});
