/* MyPerformance.com — site runtime */
(function () {
  'use strict';

  /* ---------- CONFIG (edit here, nothing else) ---------- */
  var CONFIG = {
    siteName: 'MyPerformance.com',
    siteUrl: 'https://myperformance.com',
    // Contact address is stored encoded so it never appears as plain text in the HTML source.
    contactEncoded: 'd2Vid29ya3NhMUBnbWFpbC5jb20=',
    // Google AdSense: set your publisher ID (ca-pub-XXXXXXXXXXXXXXXX) to activate live ads in every .ad-slot.
    adsenseClient: '',
    // YouTube: channel URL and featured video IDs (add IDs, e.g. 'dQw4w9WgXcQ').
    youtubeChannel: 'https://www.youtube.com/@myperformance',
    youtubeVideos: [],
    // Donation links (leave blank to hide a button).
    donate: { paypal: '', buymeacoffee: '', kofi: '', patreon: '', stripe: '' },
    // Google Analytics 4 measurement ID (G-XXXXXXXXXX) — optional.
    ga4: ''
  };
  window.MP_CONFIG = CONFIG;

  var decode = function (s) { try { return atob(s); } catch (e) { return ''; } };
  var contact = function () { return decode(CONFIG.contactEncoded); };

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var stored = null; try { stored = localStorage.getItem('mp-theme'); } catch (e) {}
  if (stored) root.setAttribute('data-theme', stored);
  else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) root.setAttribute('data-theme', 'dark');
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-theme-toggle]'); if (!t) return;
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next); try { localStorage.setItem('mp-theme', next); } catch (err) {}
  });

  /* ---------- Nav ---------- */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-burger]');
    var menu = document.querySelector('.menu');
    if (b && menu) { menu.classList.toggle('open'); b.setAttribute('aria-expanded', menu.classList.contains('open')); return; }
    if (menu && menu.classList.contains('open') && !e.target.closest('.menu') && !e.target.closest('[data-burger]')) menu.classList.remove('open');
  });
  // Mark active nav link
  var path = location.pathname.replace(/index\.html$/, '').replace(window.MP_BASE || '', '');
  document.querySelectorAll('.menu a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href !== '/' && path.indexOf(href.replace(/index\.html$/, '')) === 0) a.style.color = 'var(--brand)';
  });

  /* ---------- Hidden contact links ---------- */
  function wireMailLinks() {
    document.querySelectorAll('[data-mail]').forEach(function (a) {
      if (a.dataset.wired) return; a.dataset.wired = '1';
      var subject = a.getAttribute('data-subject') || 'Inquiry via MyPerformance.com';
      var set = function () { a.setAttribute('href', 'mailto:' + contact() + '?subject=' + encodeURIComponent(subject)); };
      a.addEventListener('mouseenter', set); a.addEventListener('focus', set); a.addEventListener('touchstart', set, { passive: true });
      a.addEventListener('click', function () { set(); });
      if (!a.getAttribute('href') || a.getAttribute('href') === '#') a.setAttribute('href', '#contact');
    });
  }
  wireMailLinks();

  /* ---------- Forms ---------- */
  // All forms post to a FormSubmit endpoint built at runtime from the encoded address, with a mailto fallback.
  function wireForms() {
    document.querySelectorAll('form[data-form]').forEach(function (form) {
      if (form.dataset.wired) return; form.dataset.wired = '1';
      var kind = form.getAttribute('data-form') || 'contact';
      form.setAttribute('method', 'POST');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var hp = form.querySelector('input[name="_honey"]'); if (hp && hp.value) return; // bot
        if (!form.checkValidity()) { form.reportValidity(); return; }
        var data = new FormData(form);
        var lines = [];
        data.forEach(function (v, k) { if (k.charAt(0) !== '_' && v) lines.push(k + ': ' + v); });
        var btn = form.querySelector('[type="submit"]'); if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Sending…'; }
        var endpoint = 'https://formsubmit.co/ajax/' + contact();
        var payload = {}; data.forEach(function (v, k) { payload[k] = v; });
        payload._subject = '[' + CONFIG.siteName + '] ' + kind.toUpperCase() + ' — ' + (payload.name || payload.email || 'form');
        payload._template = 'table';
        fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
          .then(function (r) { return r.json(); })
          .then(function (res) { if (!res || !(res.success === 'true' || res.success === true)) throw new Error('fail'); success(form); })
          .catch(function () {
            // Fallback: open the visitor's mail client with the content pre-filled.
            var body = lines.join('\n');
            location.href = 'mailto:' + contact() + '?subject=' + encodeURIComponent(payload._subject) + '&body=' + encodeURIComponent(body);
            success(form);
          })
          .finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
      });
    });
  }
  function success(form) {
    var ok = form.querySelector('.form-success') || form.parentElement.querySelector('.form-success');
    if (ok) { ok.style.display = 'block'; ok.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
    form.reset();
    var redirect = form.getAttribute('data-redirect'); if (redirect) setTimeout(function () { location.href = redirect; }, 1200);
    try { localStorage.setItem('mp-subscribed', '1'); } catch (e) {}
    track('form_submit', { form: form.getAttribute('data-form') });
  }
  wireForms();

  /* ---------- Multi-step lead form ---------- */
  document.querySelectorAll('[data-multistep]').forEach(function (ms) {
    var steps = ms.querySelectorAll('.fstep'), i = 0, bar = ms.querySelector('.progress > div');
    var show = function () { steps.forEach(function (s, k) { s.classList.toggle('active', k === i); }); if (bar) bar.style.width = ((i + 1) / steps.length * 100) + '%'; };
    ms.addEventListener('click', function (e) {
      var c = e.target.closest('.choice');
      if (c) { var grp = c.closest('.choice-grid'); grp.querySelectorAll('.choice').forEach(function (x) { x.classList.remove('selected'); }); c.classList.add('selected'); var hidden = grp.querySelector('input[type=hidden]'); if (hidden) hidden.value = c.textContent.trim(); if (c.dataset.next !== 'false') setTimeout(function () { if (i < steps.length - 1) { i++; show(); } }, 180); }
      if (e.target.closest('[data-next]')) { var req = steps[i].querySelectorAll('[required]'); var okk = true; req.forEach(function (r) { if (!r.checkValidity()) { r.reportValidity(); okk = false; } }); if (okk && i < steps.length - 1) { i++; show(); } }
      if (e.target.closest('[data-prev]')) { if (i > 0) { i--; show(); } }
    });
    show();
  });

  /* ---------- Ads ---------- */
  if (CONFIG.adsenseClient) {
    var s = document.createElement('script'); s.async = true; s.crossOrigin = 'anonymous';
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + CONFIG.adsenseClient; document.head.appendChild(s);
    document.querySelectorAll('.ad-slot').forEach(function (slot) {
      slot.innerHTML = '<ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="' + CONFIG.adsenseClient + '" data-ad-slot="' + (slot.dataset.slot || '') + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
      slot.style.border = 'none'; slot.style.background = 'transparent';
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }

  /* ---------- Analytics ---------- */
  function track(name, params) { if (window.gtag) window.gtag('event', name, params || {}); }
  if (CONFIG.ga4) {
    var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.ga4; document.head.appendChild(g);
    window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); }; window.gtag('js', new Date()); window.gtag('config', CONFIG.ga4);
  }
  window.mpTrack = track;

  /* ---------- YouTube ---------- */
  document.querySelectorAll('[data-youtube-grid]').forEach(function (grid) {
    if (!CONFIG.youtubeVideos.length) {
      grid.innerHTML = '<div class="card flat" style="grid-column:1/-1"><h3>Videos are on the way</h3><p class="muted">Our channel is being set up. Subscribe so you never miss a release.</p><a class="btn btn-primary" target="_blank" rel="noopener" href="' + CONFIG.youtubeChannel + '">Subscribe on YouTube →</a></div>';
      return;
    }
    grid.innerHTML = CONFIG.youtubeVideos.map(function (id) {
      return '<div class="video"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/' + id + '" title="MyPerformance video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>';
    }).join('');
  });
  document.querySelectorAll('[data-youtube-channel]').forEach(function (a) { a.setAttribute('href', CONFIG.youtubeChannel); });

  /* ---------- Donate buttons ---------- */
  document.querySelectorAll('[data-donate]').forEach(function (a) {
    var url = CONFIG.donate[a.getAttribute('data-donate')];
    if (url) a.setAttribute('href', url); else { a.classList.add('btn-ghost'); a.classList.remove('btn-primary'); a.setAttribute('data-mail', ''); a.setAttribute('data-subject', 'Support / donation — MyPerformance.com'); a.textContent = a.textContent.replace('via', 'ask about'); }
  });
  wireMailLinks();

  /* ---------- Share ---------- */
  document.querySelectorAll('[data-share]').forEach(function (a) {
    var u = encodeURIComponent(location.href), t = encodeURIComponent(document.title), n = a.getAttribute('data-share');
    var map = { x: 'https://twitter.com/intent/tweet?url=' + u + '&text=' + t, linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + u, facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + u, whatsapp: 'https://wa.me/?text=' + t + '%20' + u, email: 'mailto:?subject=' + t + '&body=' + u };
    if (n === 'copy') a.addEventListener('click', function (e) { e.preventDefault(); navigator.clipboard && navigator.clipboard.writeText(location.href); a.textContent = 'Copied!'; });
    else if (map[n]) { a.setAttribute('href', map[n]); a.setAttribute('target', '_blank'); a.setAttribute('rel', 'noopener'); }
  });

  /* ---------- Copy / download helpers for tools ---------- */
  window.mpCopy = function (sel, btn) { var el = document.querySelector(sel); var txt = el.value !== undefined ? el.value : el.innerText; navigator.clipboard && navigator.clipboard.writeText(txt).then(function () { if (btn) { var o = btn.textContent; btn.textContent = 'Copied ✓'; setTimeout(function () { btn.textContent = o; }, 1500); } }); track('tool_copy'); };
  window.mpDownload = function (sel, filename) { var el = document.querySelector(sel); var txt = el.value !== undefined ? el.value : el.innerText; var blob = new Blob([txt], { type: 'text/plain;charset=utf-8' }); var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename || 'myperformance.txt'; document.body.appendChild(a); a.click(); a.remove(); track('tool_download', { file: filename }); };
  window.mpPrint = function () { window.print(); };

  /* ---------- Reveal on scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .08 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); }); setTimeout(function () { document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); }); }, 2500);
  } else document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });

  /* ---------- Counters ---------- */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var end = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '', t0 = null;
    var run = function (ts) { if (!t0) t0 = ts; var p = Math.min((ts - t0) / 1400, 1); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString() + suf; if (p < 1) requestAnimationFrame(run); };
    if ('IntersectionObserver' in window) { var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { requestAnimationFrame(run); o.disconnect(); } }); o.observe(el); } else requestAnimationFrame(run);
  });

  /* ---------- Back to top ---------- */
  var bt = document.querySelector('.back-top');
  if (bt) { window.addEventListener('scroll', function () { bt.classList.toggle('show', window.scrollY > 600); }, { passive: true }); bt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); }); }

  /* ---------- Cookie notice ---------- */
  var ck = document.querySelector('.cookie'); var ckOk = null; try { ckOk = localStorage.getItem('mp-cookie'); } catch (e) {}
  if (ck && !ckOk) { setTimeout(function () { ck.classList.add('show'); }, 1200); ck.addEventListener('click', function (e) { if (e.target.closest('[data-cookie-ok]')) { ck.classList.remove('show'); try { localStorage.setItem('mp-cookie', '1'); } catch (er) {} } }); }

  /* ---------- Exit-intent / timed newsletter modal ---------- */
  var modal = document.querySelector('#newsletter-modal'); var seen = null; try { seen = localStorage.getItem('mp-modal') || localStorage.getItem('mp-subscribed'); } catch (e) {}
  if (modal && !seen) {
    var open = function () { if (modal.classList.contains('open')) return; modal.classList.add('open'); try { localStorage.setItem('mp-modal', String(Date.now())); } catch (er) {} track('modal_open'); };
    document.addEventListener('mouseleave', function (e) { if (e.clientY < 10) open(); });
    setTimeout(open, 45000);
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target.closest('.modal-close')) modal.classList.remove('open'); });
    wireForms();
  }

  /* ---------- Current year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Site search (client-side over index) ---------- */
  var searchInput = document.querySelector('[data-search]');
  if (searchInput) {
    var results = document.querySelector('[data-search-results]'); var index = null;
    var doSearch = function () {
      var q = searchInput.value.trim().toLowerCase(); if (!q) { results.innerHTML = ''; return; }
      var render = function () {
        var hits = index.filter(function (p) { return (p.title + ' ' + p.description + ' ' + (p.tags || '')).toLowerCase().indexOf(q) > -1; }).slice(0, 12);
        results.innerHTML = hits.length ? hits.map(function (p) { return '<a class="card flat" style="display:block;margin-bottom:10px" href="' + p.url + '"><span class="badge">' + p.section + '</span><h3 style="margin:8px 0 4px">' + p.title + '</h3><p class="muted small" style="margin:0">' + p.description + '</p></a>'; }).join('') : '<p class="muted">No results. Try “review”, “goals”, “template” or “calculator”.</p>';
      };
      if (index) render(); else fetch((window.MP_BASE || '') + '/assets/data/search-index.json').then(function (r) { return r.json(); }).then(function (j) { index = j; render(); });
    };
    searchInput.addEventListener('input', doSearch); doSearch();
  }
})();
