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

  // Mobile nav toggle
  const toggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
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
