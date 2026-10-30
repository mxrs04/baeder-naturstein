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

  // Geöffnet oder geschlossen? (Ortszeit Altbach)
  var HOURS = { 1: [[480, 740], [780, 1020]], 2: [[480, 740], [780, 1020]], 3: [[480, 740], [780, 1020]],
                4: [[480, 740], [780, 1080]], 5: [[480, 740], [780, 1020]] };
  var DAYS = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  function hm(m) { return Math.floor(m / 60) + '.' + String(m % 60).padStart(2, '0') + ' Uhr'; }
  function openStatus() {
    var p = {};
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(p.weekday);
    var now = (parseInt(p.hour, 10) % 24) * 60 + parseInt(p.minute, 10);
    var today = HOURS[day] || [];
    for (var i = 0; i < today.length; i++) {
      if (now >= today[i][0] && now < today[i][1]) return { open: true, text: 'Jetzt geöffnet – bis ' + hm(today[i][1]) };
      if (now < today[i][0]) return { open: false, text: (i ? 'Mittagspause – ab ' : 'Noch geschlossen – ab ') + hm(today[i][0]) };
    }
    for (var d = 1; d <= 7; d++) {
      var nd = (day + d) % 7;
      if (HOURS[nd]) return { open: false, text: 'Geschlossen – ' + (d === 1 ? 'morgen' : DAYS[nd]) + ' ab ' + hm(HOURS[nd][0][0]) };
    }
  }
  var st = openStatus();
  document.querySelectorAll('.open-status').forEach(function (el) {
    el.textContent = st.text;
    el.classList.add(st.open ? 'is-open' : 'is-closed');
  });

  // Wer ist zuständig?
  var helpBtn = document.querySelector('.help-btn');
  var help = document.querySelector('.help');
  if (helpBtn && help) {
    function showView(id) {
      help.querySelectorAll('.hp-view').forEach(function (v) {
        v.hidden = id ? v.id !== id : !v.classList.contains('hp-start');
      });
      help.querySelector('.help-body').scrollTop = 0;
      var first = help.querySelector('.hp-view:not([hidden]) button, .hp-view:not([hidden]) a');
      if (id && first) first.focus();
    }
    function setOpen(open) {
      help.classList.toggle('is-open', open);
      helpBtn.setAttribute('aria-expanded', open);
      if (!open) showView(null);
    }
    helpBtn.addEventListener('click', function () { setOpen(!help.classList.contains('is-open')); });
    help.querySelector('.help-close').addEventListener('click', function () { setOpen(false); helpBtn.focus(); });
    help.querySelectorAll('[data-topic]').forEach(function (b) {
      b.addEventListener('click', function () { showView(b.getAttribute('data-topic')); });
    });
    help.querySelectorAll('.hp-back').forEach(function (b) {
      b.addEventListener('click', function () { showView(null); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  // ------------------------------------------------ Bewegung
  var anim = document.documentElement.classList.contains('anim');

  // Logo zeichnet sich einmal pro Besuch
  var brand = document.querySelector('.header .brand');
  if (brand && anim) {
    var seen = false;
    try { seen = sessionStorage.getItem('logo-seen') === '1'; sessionStorage.setItem('logo-seen', '1'); } catch (e) {}
    if (!seen) brand.classList.add('is-intro');
  }

  // Kopfzeile wird beim Scrollen schlanker
  var ticking = false;
  var heroImg = document.querySelector('.hero img.hero-bg');
  var timelines = document.querySelectorAll('.timeline');
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 40);
    if (anim && heroImg && y < 1200) {
      heroImg.style.translate = '0 ' + Math.round(y * 0.22) + 'px';
    }
    timelines.forEach(function (tl) {
      var r = tl.getBoundingClientRect();
      var mid = window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
      tl.style.setProperty('--p', p.toFixed(3));
      tl.querySelectorAll('li').forEach(function (li) {
        li.classList.toggle('passed', li.getBoundingClientRect().top < mid);
      });
    });
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  // Inhalte beim Scrollen sanft einblenden
  if (anim && 'IntersectionObserver' in window) {
    var sel = '.head, .card, .tile, .fact, .swatch, .stone, .gallery figure, .timeline li, .notice, .file, .split > div, .color-group, details.acc, .table-wrap, .chips, .subnav, .framed';
    var picked = [];
    document.querySelectorAll('main ' + sel).forEach(function (el) {
      if (el.closest('.hero, .page-head')) return;
      for (var i = 0; i < picked.length; i++) { if (picked[i].contains(el)) return; }
      picked.push(el);
    });
    var vh = window.innerHeight;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    picked.forEach(function (el) {
      if (el.getBoundingClientRect().top < vh * 0.92) return; // schon sichtbar: nicht verstecken
      var sib = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', Math.min(sib, 6) * 0.07 + 's');
      el.classList.add('rv');
      io.observe(el);
    });
    // große Bilder: von unten aufdecken
    document.querySelectorAll('main .split .photo, main .hero ~ section .photo--wide').forEach(function (ph) {
      if (ph.closest('.rv') || ph.getBoundingClientRect().top < vh * 0.92) return;
      ph.classList.add('rv-img');
      io.observe(ph);
    });
    // Facetten-Motiv im dunklen Abschnitt zeichnet sich, sobald sichtbar
    document.querySelectorAll('.section--cta').forEach(function (s) {
      new IntersectionObserver(function (en, o) {
        if (en[0].isIntersecting) { s.classList.add('in-view'); o.disconnect(); }
      }, { threshold: 0.3 }).observe(s);
    });
    // Zahlen zählen hoch (nur einzelne Zahl, z. B. „ca. 1.600“)
    document.querySelectorAll('.fact b').forEach(function (b) {
      var m = b.textContent.match(/\d[\d.]*/g);
      if (!m || m.length !== 1) return;
      var raw = m[0], target = parseInt(raw.replace(/\./g, ''), 10);
      if (!target || target < 3) return;
      var fmt = function (n) { return raw.indexOf('.') > -1 ? n.toLocaleString('de-DE') : String(n); };
      var orig = b.textContent;
      new IntersectionObserver(function (en, o) {
        if (!en[0].isIntersecting) return;
        o.disconnect();
        var t0 = performance.now();
        (function step(t) {
          var k = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - k, 3);
          b.textContent = orig.replace(raw, fmt(Math.round(target * e)));
          if (k < 1) requestAnimationFrame(step); else b.textContent = orig;
        })(t0);
      }, { threshold: 0.6 }).observe(b);
    });
  }

  // Glanz auf den Material-Kacheln folgt der Maus
  document.querySelectorAll('.tile').forEach(function (t) {
    var ph = t.querySelector('.photo');
    t.addEventListener('pointermove', function (e) {
      var r = ph.getBoundingClientRect();
      ph.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      ph.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // Ein Gruß für Neugierige in der Entwicklerkonsole
  if (window.console && console.log) {
    console.log('%cBÄDER%c  Stein auf Stein – seit 1926 in Altbach.', 'font:700 16px sans-serif;color:#7096ba;letter-spacing:2px', 'color:#5b6267');
  }
})();
