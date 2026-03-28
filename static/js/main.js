/* Botanica — main.js */

// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const siteNav = document.querySelector('.site-nav');
if (navToggle && siteNav) {
  navToggle.addEventListener('click', () => {
    siteNav.style.display = siteNav.style.display === 'flex' ? 'none' : 'flex';
    siteNav.style.flexDirection = 'column';
    siteNav.style.position = 'absolute';
    siteNav.style.top = '60px';
    siteNav.style.right = '0';
    siteNav.style.left = '0';
    siteNav.style.background = 'var(--cream)';
    siteNav.style.padding = '1rem 1.5rem';
    siteNav.style.borderBottom = '1px solid var(--border)';
    siteNav.style.zIndex = '200';
  });
}

// Highlight active nav link by URL
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
  if (link.getAttribute('href') && currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/') {
    link.classList.add('active');
  }
});

// Smooth scroll for TOC links
document.querySelectorAll('.toc-link, a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href && href.startsWith('#')) {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });
});

// Fade-in on scroll for plant and post cards
if ('IntersectionObserver' in window) {
  const cards = document.querySelectorAll('.plant-card, .post-card, .plant-section');
  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  });
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });
  cards.forEach(card => observer.observe(card));
}
