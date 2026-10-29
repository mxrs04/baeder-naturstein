// Bäder Natursteine und Glas – Menü, Bildbetrachter, Video, Schnelle Hilfe
(function () {
  var header = document.querySelector('.header');
  var menuBtn = document.querySelector('.menu-btn');

  // Mobiles Menü
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      header.style.setProperty('--menu-top', header.getBoundingClientRect().bottom + 'px');
      var open = header.classList.toggle('is-open');
      document.body.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', open);
      menuBtn.querySelector('span').textContent = open ? 'Schließen' : 'Menü';
    });
  }

  // Ausklappbare Menüpunkte
  var toggles = document.querySelectorAll('.nav-link[aria-controls]');
  function closeAll(except) {
    toggles.forEach(function (t) {
      if (t === except) return;
      t.setAttribute('aria-expanded', 'false');
      document.getElementById(t.getAttribute('aria-controls')).classList.remove('is-open');
    });
  }
  toggles.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = t.getAttribute('aria-expanded') !== 'true';
      closeAll(t);
      t.setAttribute('aria-expanded', open);
      document.getElementById(t.getAttribute('aria-controls')).classList.toggle('is-open', open);
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav')) closeAll();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeAll(); closeLightbox(); }
  });

  // Bildbetrachter für Galerien
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = '<button type="button" aria-label="Bild schließen">×</button><figure><img alt=""><p></p></figure>';
  document.body.appendChild(box);
  function closeLightbox() { box.classList.remove('is-open'); }
  box.addEventListener('click', function (e) { if (e.target.tagName !== 'IMG') closeLightbox(); });
  document.querySelectorAll('a[data-zoom]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      box.querySelector('img').src = a.href;
      box.querySelector('img').alt = a.getAttribute('data-zoom');
      box.querySelector('p').textContent = a.getAttribute('data-zoom');
      box.classList.add('is-open');
    });
  });

  // YouTube erst nach Klick laden (keine Daten an Google vorher)
  document.querySelectorAll('.video button[data-yt]').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.getAttribute('data-yt') + '?autoplay=1&rel=0';
      f.allow = 'autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      f.title = 'Video';
      b.parentNode.appendChild(f);
      b.remove();
    });
  });

  // Widerruf: Formular als E-Mail vorbereiten
  var wf = document.getElementById('widerruf-form');
  if (wf) {
    wf.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(wf);
      var body = 'Hiermit widerrufe ich den folgenden Vertrag.\n\n' +
        'Name: ' + d.get('name') + '\n' +
        'Bestell- oder Buchungsnummer: ' + d.get('nummer') + '\n' +
        'E-Mail: ' + d.get('email') + '\n' +
        'Artikel: ' + (d.get('artikel') || 'gesamter Vertrag') + '\n' +
        'Grund (optional): ' + (d.get('grund') || '-') + '\n';
      location.href = 'mailto:info@natursteinwerk-baeder.de?subject=' +
        encodeURIComponent('Widerruf ' + d.get('nummer')) + '&body=' + encodeURIComponent(body);
    });
  }

  // Schnelle Hilfe
  var answers = {
    zeiten: '<b>Öffnungszeiten</b><br>Montag bis Mittwoch und Freitag: 8.00–12.20 Uhr und 13.00–17.00 Uhr<br>Donnerstag: 8.00–12.20 Uhr und 13.00–18.00 Uhr<br><br><b>Adresse</b><br>In den Weiden 24, 73776 Altbach<br><a href="kontakt-anfahrt.html">Anfahrt ansehen</a>',
    materialien: '<b>Unsere Materialien</b><br>Über 70 Natursteinsorten am Lager, dazu Silestone, Lightstone, Neolith, Dekton, Laminam und Vetroplan-Glas.<br><a href="naturstein.html">Naturstein</a> · <a href="neolith-keramik.html">Keramik</a> · <a href="vetroplan-glasrueckfronten.html">Glas</a>',
    preise: '<b>Preise</b><br>Unsere Preisliste 2025/26 mit Service-, Montage- und Liefertarifen finden Sie hier:<br><a href="download-preislisten.html">Zur Preisliste</a><br><br>Hinweis: Wir verkaufen ausschließlich an Gewerbekunden.',
    kontakt: '<b>So erreichen Sie uns</b><br>Telefon: <a href="tel:+49715383130">07153 8313-0</a><br>E-Mail: <a href="mailto:info@natursteinwerk-baeder.de">info@natursteinwerk-baeder.de</a><br><a href="team.html">Alle Ansprechpartner</a>'
  };
  var labels = { zeiten: 'Öffnungszeiten', materialien: 'Materialien', preise: 'Preise', kontakt: 'Kontakt' };
  var helpBtn = document.querySelector('.help-btn');
  var help = document.querySelector('.help');
  if (helpBtn && help) {
    var body = help.querySelector('.help-body');
    function say(html, me) {
      var m = document.createElement('div');
      m.className = 'msg' + (me ? ' msg--me' : '');
      m.innerHTML = html;
      body.appendChild(m);
      body.scrollTop = body.scrollHeight;
    }
    helpBtn.addEventListener('click', function () {
      var open = help.classList.toggle('is-open');
      helpBtn.setAttribute('aria-expanded', open);
    });
    help.querySelector('.help-head button').addEventListener('click', function () {
      help.classList.remove('is-open');
      helpBtn.setAttribute('aria-expanded', 'false');
    });
    help.querySelectorAll('.help-quick button').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-q');
        say(labels[k], true);
        setTimeout(function () { say(answers[k]); }, 250);
      });
    });
  }
})();
