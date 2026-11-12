/* Mladý Európan – cvičné testy. Bez knižníc; stav v localStorage. */
(function () {
  "use strict";
  var LIMIT = 30 * 60 * 1000, PASS = 90, KEY = "me-testy-v1";
  var D = null, T = null, Q = null, KAT = null, CRED = null;
  var app = document.getElementById("app");
  var tick = null;

  /* ---------- stav ---------- */
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || { hist: [], cur: null }; } catch (e) { return { hist: [], cur: null }; }
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* súkromné okno */ } }
  var S = load();

  /* ---------- pomocné ---------- */
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function mmss(ms) { ms = Math.max(0, ms); var s = Math.ceil(ms / 1000); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function fmtDate(t) { var d = new Date(t); return d.toLocaleDateString("sk-SK") + " " + d.toLocaleTimeString("sk-SK", { hour: "2-digit", minute: "2-digit" }); }
  function body(n) { return n === 1 ? "bod" : (n >= 2 && n <= 4 ? "body" : "bodov"); }
  function host(u) { try { var x = new URL(u); return x.hostname.replace(/^www\./, "") + x.pathname.replace(/\/$/, ""); } catch (e) { return u; } }
  function L(i) { return "ABC".charAt(i); }
  function qOf(test, i) { return Q[T[test - 1][i]]; }
  function score(test, ans) {
    var pts = 0, ok = 0, per = {};
    T[test - 1].forEach(function (qi, i) {
      var q = Q[qi], k = q.k, p = KAT[k].body;
      per[k] = per[k] || { ok: 0, n: 0, pts: 0, max: 0 };
      per[k].n++; per[k].max += p;
      if (ans[i] === q.c) { pts += p; ok++; per[k].ok++; per[k].pts += p; }
    });
    return { pts: pts, ok: ok, per: per };
  }
  function doneTests() { var m = {}; S.hist.forEach(function (h) { m[h.t] = 1; }); return m; }
  function stopTick() { if (tick) { clearInterval(tick); tick = null; } }
  function go(h) { if (location.hash === h) route(); else location.hash = h; }

  /* ---------- úvod ---------- */
  function home() {
    stopTick();
    var cur = S.cur, done = doneTests(), nDone = Object.keys(done).length;
    var passed = S.hist.filter(function (h) { return h.pts >= PASS; }).length;
    var avg = S.hist.length ? Math.round(S.hist.reduce(function (a, h) { return a + h.pts; }, 0) / S.hist.length) : 0;
    var h = '<section class="card hero"><h1>Cvičné testy na súťaž Mladý Európan</h1>' +
      '<p class="muted">Ako test v autoškole: 40 otázok, na každú tri možnosti a práve jedna je správna. Výsledok a správne odpovede uvidíš až po odovzdaní.</p>' +
      '<div class="facts"><div class="fact"><b>40</b><span>otázok v teste</span></div><div class="fact"><b>30 min</b><span>časový limit</span></div>' +
      '<div class="fact"><b>100</b><span>bodov spolu</span></div><div class="fact"><b>90</b><span>bodov na úspech</span></div></div>' +
      '<div class="row"><button class="btn primary" id="rnd">Náhodný test</button>' +
      '<form class="pick" id="pick"><label for="tn" class="small muted">alebo test č.</label><input id="tn" type="number" min="1" max="1000" inputmode="numeric" placeholder="1 – 1000" required>' +
      '<button class="btn" type="submit">Spustiť</button></form></div>' +
      '<p class="small muted" style="margin:12px 0 0">K dispozícii je 1000 pevných testov z ' + Q.length + ' overených otázok (z toho ' +
      Q.filter(function (q) { return q.img; }).length + ' s obrázkom).</p></section>';
    if (cur) {
      var left = cur.deadline - Date.now();
      h += '<section class="card resume"><h2>Rozpracovaný test č. ' + cur.t + '</h2><p class="muted">Zodpovedané ' +
        cur.ans.filter(function (a) { return a >= 0; }).length + ' zo 40 · zostáva ' + (left > 0 ? mmss(left) : "0:00") + '</p>' +
        '<div class="row"><button class="btn gold" id="cont">' + (left > 0 ? "Pokračovať v teste" : "Vyhodnotiť test") + '</button>' +
        '<button class="btn ghost" id="drop">Zahodiť</button></div></section>';
    }
    if (S.hist.length) {
      h += '<section class="card"><h2>Tvoje výsledky</h2><div class="stats">' +
        '<div class="stat"><b>' + S.hist.length + '</b><span class="small muted">absolvovaných</span></div>' +
        '<div class="stat"><b>' + passed + '</b><span class="small muted">úspešných</span></div>' +
        '<div class="stat"><b>' + avg + '</b><span class="small muted">priemer bodov</span></div></div>' +
        '<p class="small muted">Rôznych testov: ' + nDone + ' z 1000. Klikni na test a pozri si, čo si mal zle.</p><ul class="hist">' +
        S.hist.slice().reverse().slice(0, 60).map(function (x) {
          var pass = x.pts >= PASS;
          return '<li><a href="#/vysledok/' + x.id + '"><span>Test č. ' + x.t + ' <span class="small muted">· ' + fmtDate(x.end) + '</span></span>' +
            '<span><b>' + x.pts + '</b> b. <span class="tag ' + (pass ? "ok" : "bad") + '">' + (pass ? "úspech" : "neúspech") + '</span></span></a></li>';
        }).join("") + '</ul></section>';
    }
    app.innerHTML = h;
    document.getElementById("rnd").onclick = function () {
      var done = doneTests(), free = [];
      for (var i = 1; i <= 1000; i++) if (!done[i]) free.push(i);
      if (!free.length) for (i = 1; i <= 1000; i++) free.push(i);
      start(free[Math.floor(Math.random() * free.length)]);
    };
    document.getElementById("pick").onsubmit = function (e) {
      e.preventDefault();
      var n = parseInt(document.getElementById("tn").value, 10);
      if (n >= 1 && n <= 1000) start(n);
    };
    if (cur) {
      document.getElementById("cont").onclick = function () { go("#/test"); };
      document.getElementById("drop").onclick = function () {
        if (confirm("Naozaj zahodiť rozpracovaný test? Nezapočíta sa do výsledkov.")) { S.cur = null; save(S); home(); }
      };
    }
  }

  function start(t) {
    if (S.cur && !confirm("Máš rozpracovaný test č. " + S.cur.t + ". Zahodiť ho a začať test č. " + t + "?")) return;
    var now = Date.now();
    S.cur = { t: t, ans: new Array(40).fill(-1), start: now, deadline: now + LIMIT, pos: 0 };
    save(S);
    go("#/test");
  }

  /* ---------- test ---------- */
  function test() {
    var c = S.cur;
    if (!c) return go("#/");
    if (Date.now() >= c.deadline) return finish(true);
    var i = c.pos, q = qOf(c.t, i), k = KAT[q.k];
    var h = '<div class="testbar"><div><b>Test č. ' + c.t + '</b> <span class="muted small">· otázka ' + (i + 1) + '/40</span></div>' +
      '<div class="row"><span class="timer" id="timer" aria-live="off">' + mmss(c.deadline - Date.now()) + '</span>' +
      '<button class="btn primary" id="end">Odovzdať</button></div></div>' +
      '<div class="grid" role="navigation" aria-label="Otázky">' + c.ans.map(function (a, j) {
        return '<button data-j="' + j + '" class="' + (a >= 0 ? "done " : "") + (j === i ? "cur" : "") + '" aria-label="Otázka ' + (j + 1) + (a >= 0 ? ", zodpovedaná" : "") + '">' + (j + 1) + '</button>';
      }).join("") + '</div>' +
      '<article class="card"><div class="qmeta"><span>' + esc(k.nazov) + '</span><span>' + k.body + ' ' + body(k.body) + '</span></div>' +
      (q.img ? '<div class="qimg"><img src="' + esc(q.img) + '" alt="Obrázok k otázke"></div>' : "") +
      '<p class="qtext">' + esc(q.q) + '</p><div class="opts">' + q.a.map(function (o, j) {
        return '<button class="opt' + (c.ans[i] === j ? " sel" : "") + '" data-o="' + j + '" aria-pressed="' + (c.ans[i] === j) + '"><span class="l">' + L(j) + '</span><span>' + esc(o) + '</span></button>';
      }).join("") + '</div>' +
      '<div class="nav"><button class="btn" id="prev"' + (i === 0 ? " disabled" : "") + '>← Predchádzajúca</button>' +
      (i < 39 ? '<button class="btn primary" id="next">Ďalšia →</button>' : '<button class="btn gold" id="end2">Odovzdať test</button>') + '</div></article>';
    app.innerHTML = h;
    app.querySelectorAll(".grid button").forEach(function (b) { b.onclick = function () { c.pos = +b.dataset.j; save(S); test(); }; });
    app.querySelectorAll(".opt").forEach(function (b) {
      b.onclick = function () { c.ans[i] = +b.dataset.o; save(S); test(); };
    });
    document.getElementById("prev").onclick = function () { if (c.pos > 0) { c.pos--; save(S); test(); } };
    var nx = document.getElementById("next"); if (nx) nx.onclick = function () { c.pos++; save(S); test(); };
    document.getElementById("end").onclick = ask;
    var e2 = document.getElementById("end2"); if (e2) e2.onclick = ask;
    stopTick();
    tick = setInterval(function () {
      var left = c.deadline - Date.now(), el = document.getElementById("timer");
      if (left <= 0) { stopTick(); finish(true); return; }
      if (el) { el.textContent = mmss(left); el.classList.toggle("low", left < 5 * 60 * 1000); }
    }, 500);
  }

  function ask() {
    var c = S.cur, open = c.ans.filter(function (a) { return a < 0; }).length;
    var dlg = document.getElementById("dlg");
    document.getElementById("dlg-t").textContent = "Odovzdať test?";
    document.getElementById("dlg-p").textContent = open ? "Nezodpovedaných otázok: " + open + ". Za nezodpovedanú otázku nedostaneš body." : "Všetky otázky sú zodpovedané. Po odovzdaní uvidíš výsledok a správne odpovede.";
    dlg.hidden = false;
    document.getElementById("dlg-yes").focus();
    document.getElementById("dlg-no").onclick = function () { dlg.hidden = true; };
    document.getElementById("dlg-yes").onclick = function () { dlg.hidden = true; finish(false); };
  }

  function finish(timeout) {
    stopTick();
    var c = S.cur;
    if (!c) return go("#/");
    var end = Math.min(Date.now(), c.deadline), sc = score(c.t, c.ans);
    var rec = { id: String(c.start), t: c.t, ans: c.ans, start: c.start, end: end, pts: sc.pts, ok: sc.ok, timeout: !!timeout };
    S.hist.push(rec);
    if (S.hist.length > 400) S.hist = S.hist.slice(-400);
    S.cur = null;
    save(S);
    go("#/vysledok/" + rec.id);
  }

  /* ---------- výsledok a prehľad ---------- */
  function result(id, filter) {
    stopTick();
    var r = S.hist.filter(function (x) { return x.id === id; })[0];
    if (!r) return go("#/");
    var sc = score(r.t, r.ans), pass = sc.pts >= PASS;
    var wrong = [], none = [];
    r.ans.forEach(function (a, i) { var q = qOf(r.t, i); if (a < 0) none.push(i); else if (a !== q.c) wrong.push(i); });
    filter = filter || (wrong.length + none.length ? "zle" : "vsetky");
    var used = Math.round((r.end - r.start) / 1000);
    var h = '<section class="card result ' + (pass ? "pass" : "fail") + '"><div class="verdict">' + (pass ? "Test si urobil(a) úspešne" : "Test nebol úspešný") + '</div>' +
      '<div class="big">' + sc.pts + ' <span style="font-size:.4em" class="muted">/ 100 bodov</span></div>' +
      '<p class="muted">Test č. ' + r.t + ' · správne ' + sc.ok + ' zo 40 · čas ' + Math.floor(used / 60) + ' min ' + (used % 60) + ' s' +
      (r.timeout ? " · čas vypršal" : "") + ' · ' + fmtDate(r.end) + '</p>' +
      '<div class="row" style="justify-content:center"><a class="btn" href="#/">Úvod</a><button class="btn" id="again">Zopakovať test č. ' + r.t + '</button>' +
      '<button class="btn primary" id="nexttest">Ďalší test</button></div></section>' +
      '<section class="card"><h2>Podľa kategórií</h2><table><thead><tr><th>Kategória</th><th class="num">Správne</th><th class="num">Body</th></tr></thead><tbody>' +
      Object.keys(KAT).map(function (k) {
        var p = sc.per[k]; if (!p) return "";
        return '<tr><td>' + esc(KAT[k].nazov) + '</td><td class="num">' + p.ok + '/' + p.n + '</td><td class="num">' + p.pts + '/' + p.max + '</td></tr>';
      }).join("") + '</tbody></table></section>' +
      '<section class="card"><h2>Prehľad otázok</h2>' +
      '<div class="grid">' + r.ans.map(function (a, i) {
        var q = qOf(r.t, i); return '<button data-j="' + i + '" class="' + (a === q.c ? "r-ok" : "r-bad") + '" aria-label="Otázka ' + (i + 1) + '">' + (i + 1) + '</button>';
      }).join("") + '</div>' +
      '<div class="tabs" role="tablist"><button data-f="zle" class="' + (filter === "zle" ? "on" : "") + '">Nesprávne a nezodpovedané (' + (wrong.length + none.length) + ')</button>' +
      '<button data-f="vsetky" class="' + (filter === "vsetky" ? "on" : "") + '">Všetky (40)</button>' +
      '<button data-f="dobre" class="' + (filter === "dobre" ? "on" : "") + '">Správne (' + sc.ok + ')</button></div></section><div id="revs"></div>';
    app.innerHTML = h;
    var idx = [];
    for (var i = 0; i < 40; i++) {
      var q = qOf(r.t, i), a = r.ans[i];
      if (filter === "vsetky" || (filter === "zle" && a !== q.c) || (filter === "dobre" && a === q.c)) idx.push(i);
    }
    document.getElementById("revs").innerHTML = idx.length ? idx.map(function (i) { return review(r, i); }).join("") :
      '<p class="card muted">Žiadne otázky v tomto výbere – výborne!</p>';
    app.querySelectorAll(".tabs button").forEach(function (b) { b.onclick = function () { result(id, b.dataset.f); }; });
    app.querySelectorAll(".grid button").forEach(function (b) {
      b.onclick = function () {
        var el = document.getElementById("rv" + b.dataset.j);
        if (!el) { result(id, "vsetky"); el = document.getElementById("rv" + b.dataset.j); }
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
      };
    });
    document.getElementById("again").onclick = function () { start(r.t); };
    document.getElementById("nexttest").onclick = function () { start(r.t % 1000 + 1); };
  }

  function review(r, i) {
    var q = qOf(r.t, i), a = r.ans[i], k = KAT[q.k];
    var st = a < 0 ? '<span class="tag bad">nezodpovedané</span>' : (a === q.c ? '<span class="tag ok">správne</span>' : '<span class="tag bad">nesprávne</span>');
    return '<article class="card rev" id="rv' + i + '"><div class="qmeta"><span>' + (i + 1) + '. ' + esc(k.nazov) + ' · ' + k.body + ' ' + body(k.body) + '</span>' + st + '</div>' +
      (q.img ? '<div class="qimg"><img src="' + esc(q.img) + '" alt="Obrázok k otázke" loading="lazy"></div>' : "") +
      '<p class="qtext">' + esc(q.q) + '</p><div class="opts">' + q.a.map(function (o, j) {
        var cls = j === q.c ? " is-ok" : (j === a ? " is-bad" : "");
        var lab = j === a ? '<span class="yours">tvoja odpoveď</span>' : (j === q.c ? '<span class="yours" style="color:var(--ok)">správne</span>' : "");
        return '<button class="opt' + cls + '" disabled><span class="l">' + L(j) + '</span><span>' + esc(o) + '</span>' + lab + '</button>';
      }).join("") + '</div>' +
      '<div class="why"><b>Vysvetlenie:</b> ' + esc(q.v) + (q.z && q.z.length ? '<div class="src">Zdroj: ' + q.z.map(function (u) {
        return '<a href="' + esc(u) + '" target="_blank" rel="noopener">' + esc(host(u)) + '</a>';
      }).join(" · ") + '</div>' : "") + '</div></article>';
  }

  /* ---------- informácie a licencie ---------- */
  function info() {
    stopTick();
    var rows = Object.keys(KAT).map(function (k) {
      var n = Q.filter(function (q) { return q.k === k; }).length;
      return '<tr><td>' + esc(KAT[k].nazov) + '</td><td class="num">' + KAT[k].pocet + '</td><td class="num">' + KAT[k].body + '</td><td class="num">' + n + '</td></tr>';
    }).join("");
    app.innerHTML = '<section class="card info"><h2>Ako testy fungujú</h2>' +
      '<p>Každý test má 40 otázok a 30 minút. Každá otázka má tri možnosti, správna je vždy práve jedna. Otázky majú podľa kategórie 1 až 4 body, spolu 100 bodov. Test je úspešný od 90 bodov. Odpovede môžeš meniť až do odovzdania; keď čas vyprší, test sa odovzdá sám.</p>' +
      '<p>Po odovzdaní uvidíš body, výsledok podľa kategórií a pri každej otázke tvoju odpoveď, správnu odpoveď, krátke vysvetlenie a odkaz na zdroj. Výsledky sa ukladajú len v tomto zariadení (v prehliadači), takže sa k nim môžeš kedykoľvek vrátiť.</p>' +
      '<p>Testov je 1000 a sú pevne dané: test č. 25 má vždy tie isté otázky. Otázky sa medzi testami striedajú rovnomerne a v jednom teste nie sú dve otázky na ten istý fakt.</p>' +
      '<table><thead><tr><th>Kategória</th><th class="num">V teste</th><th class="num">Body za otázku</th><th class="num">Otázok v databáze</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<h2>Odkiaľ sú otázky</h2><p>Všetky fakty sú overené v oficiálnych zdrojoch – najmä na portáli european-union.europa.eu, v informačných listoch Európskeho parlamentu, na stránkach Európskej komisie, Rady EÚ, Európskej centrálnej banky, Národnej banky Slovenska a Štatistického úradu SR. Pri každej otázke je odkaz na stránku, z ktorej fakt pochádza. Stav k novembru 2026.</p>' +
      '<p class="small muted">Ide o neoficiálnu pomôcku na precvičovanie, nie o materiál organizátora súťaže.</p>' +
      '<h2>Obrázky a licencie</h2><p class="small">Fotografie a logá pochádzajú z oficiálnych webov inštitúcií EÚ a ECB. Obsah inštitúcií EÚ sa smie opätovne použiť s uvedením zdroja (rozhodnutie Komisie 2011/833/EÚ); obrázky euromincí sú zo stránky ECB. Logá sú majetkom príslušných inštitúcií a agentúr.</p>' +
      '<div id="cred" class="small muted">Načítavam zoznam obrázkov…</div></section>';
    var show = function () {
      var keys = Object.keys(CRED).sort();
      document.getElementById("cred").outerHTML = '<table class="cred"><thead><tr><th></th><th>Obrázok</th><th>Autor / práva</th></tr></thead><tbody>' + keys.map(function (k) {
        var c = CRED[k];
        return '<tr><td><img src="' + esc(k) + '" alt="" loading="lazy"></td><td><a href="' + esc(c.stranka) + '" target="_blank" rel="noopener">' + esc(host(c.stranka)) +
          '</a><br><a class="muted" href="' + esc(c.obrazok) + '" target="_blank" rel="noopener">súbor</a></td><td>' + esc(c.autor) + '</td></tr>';
      }).join("") + '</tbody></table>';
    };
    if (CRED) show(); else fetch("img/kredity.json").then(function (r) { return r.json(); }).then(function (j) { CRED = j; show(); });
  }

  /* ---------- smerovanie ---------- */
  function route() {
    var h = location.hash || "#/";
    var m = h.match(/^#\/vysledok\/(\w+)/);
    if (h.indexOf("#/test") === 0) test();
    else if (m) result(m[1]);
    else if (h.indexOf("#/info") === 0) info();
    else home();
    window.scrollTo(0, 0);
  }

  document.addEventListener("keydown", function (e) {
    if (!S.cur || (location.hash || "").indexOf("#/test") !== 0 || !document.getElementById("dlg").hidden) return;
    if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
    var k = e.key.toLowerCase(), c = S.cur, map = { "1": 0, "2": 1, "3": 2, a: 0, b: 1, c: 2 };
    if (k in map) { c.ans[c.pos] = map[k]; save(S); test(); }
    else if (k === "arrowright" && c.pos < 39) { c.pos++; save(S); test(); }
    else if (k === "arrowleft" && c.pos > 0) { c.pos--; save(S); test(); }
  });
  window.addEventListener("hashchange", route);

  Promise.all([fetch("data/otazky.json").then(function (r) { return r.json(); }), fetch("data/testy.json").then(function (r) { return r.json(); })])
    .then(function (x) { D = x[0]; Q = D.otazky; KAT = D.kat; T = x[1]; route(); })
    .catch(function () { app.innerHTML = '<p class="loading">Otázky sa nepodarilo načítať. Skontroluj pripojenie a obnov stránku.</p>'; });

  if ("serviceWorker" in navigator && location.protocol === "https:") {
    navigator.serviceWorker.register("sw.js").catch(function () { });
  }
})();
