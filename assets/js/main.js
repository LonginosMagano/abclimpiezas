/* ABC Limpiezas - Main JS */
document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  var menuBtn = document.querySelector('.mobile-menu-btn');
  var nav = document.querySelector('.header-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function() {
      nav.classList.toggle('open');
      menuBtn.textContent = nav.classList.contains('open') ? '\u2715' : '\u2630';
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = this.parentElement;
      var wasActive = item.classList.contains('active');
      document.querySelectorAll('.faq-item').forEach(function(el) { el.classList.remove('active'); });
      if (!wasActive) item.classList.add('active');
    });
  });

  // Contact form
  document.querySelectorAll('.contact-form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var btn = form.querySelector('.btn-submit');
      var successEl = form.querySelector('.form-success');
      btn.textContent = 'Enviando...';
      btn.disabled = true;
      setTimeout(function() {
        btn.textContent = 'Solicitud Enviada';
        btn.style.background = '#1A8C3E';
        if (successEl) {
          successEl.style.display = 'block';
          successEl.textContent = 'Hemos recibido su solicitud. Le llamaremos en menos de 30 minutos.';
        }
        form.reset();
        setTimeout(function() {
          btn.textContent = 'Solicitar Presupuesto Gratis';
          btn.style.background = '';
          btn.disabled = false;
          if (successEl) successEl.style.display = 'none';
        }, 5000);
      }, 1200);
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (nav && nav.classList.contains('open')) {
          nav.classList.remove('open');
          if (menuBtn) menuBtn.textContent = '\u2630';
        }
      }
    });
  });
});
