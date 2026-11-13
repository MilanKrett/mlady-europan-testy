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

  /* ---------- úvod: len tlačidlo ---------- */
  function home() {
    stopTick();
    app.innerHTML = '<div class="start"><button class="btn primary xl" id="go">Spustiť test</button></div>';
    document.getElementById("go").onclick = start;
  }

  // rozpracovaný test pokračuje; inak náhodný test, ktorý ešte nebol
  function start() {
    if (!S.cur) {
      var done = doneTests(), free = [], i;
      for (i = 1; i <= 1000; i++) if (!done[i]) free.push(i);
      if (!free.length) for (i = 1; i <= 1000; i++) free.push(i);
      var now = Date.now();
      S.cur = { t: free[Math.floor(Math.random() * free.length)], ans: new Array(40).fill(-1), start: now, deadline: now + LIMIT, pos: 0 };
      save(S);
    }
    go("#/test");
  }

  /* ---------- test ---------- */
  function test() {
    var c = S.cur;
    if (!c) return go("#/");
    if (Date.now() >= c.deadline) return finish(true);
    var i = c.pos, q = qOf(c.t, i);
    var h = '<div class="testbar"><span class="timer" id="timer" aria-live="off">' + mmss(c.deadline - Date.now()) + '</span>' +
      '<button class="btn primary" id="end">Odovzdať</button></div>' +
      '<div class="grid" role="navigation" aria-label="Otázky">' + c.ans.map(function (a, j) {
        return '<button data-j="' + j + '" class="' + (a >= 0 ? "done " : "") + (j === i ? "cur" : "") + '" aria-label="Otázka ' + (j + 1) + (a >= 0 ? ", zodpovedaná" : "") + '">' + (j + 1) + '</button>';
      }).join("") + '</div>' +
      '<article class="card">' +
      (q.img ? '<div class="qimg"><img src="' + esc(q.img) + '" alt=""></div>' : "") +
      '<p class="qtext">' + esc(q.q) + '</p><div class="opts">' + q.a.map(function (o, j) {
        return '<button class="opt' + (c.ans[i] === j ? " sel" : "") + '" data-o="' + j + '" aria-pressed="' + (c.ans[i] === j) + '"><span class="l">' + L(j) + '</span><span>' + esc(o) + '</span></button>';
      }).join("") + '</div>' +
      '<div class="nav"><button class="btn arrow" id="prev" aria-label="Predchádzajúca otázka"' + (i === 0 ? " disabled" : "") + '>←</button>' +
      (i < 39 ? '<button class="btn primary arrow" id="next" aria-label="Ďalšia otázka">→</button>' : '<button class="btn primary" id="end2">Odovzdať</button>') + '</div></article>';
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
    var open = S.cur.ans.filter(function (a) { return a < 0; }).length;
    var dlg = document.getElementById("dlg"), p = document.getElementById("dlg-p");
    p.textContent = open ? "Nezodpovedané: " + open : "";
    p.hidden = !open;
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

  /* ---------- výsledok: body, mriežka a chyby ---------- */
  function result(id, all) {
    stopTick();
    var r = S.hist.filter(function (x) { return x.id === id; })[0];
    if (!r) return go("#/");
    var sc = score(r.t, r.ans), pass = sc.pts >= PASS, idx = [];
    for (var i = 0; i < 40; i++) if (all || r.ans[i] !== qOf(r.t, i).c) idx.push(i);
    var again = '<button class="btn primary xl again">Spustiť test</button>';
    app.innerHTML = '<section class="card result ' + (pass ? "pass" : "fail") + '">' +
      '<div class="big">' + sc.pts + '<span>/100</span></div>' +
      '<div class="grid">' + r.ans.map(function (a, j) {
        return '<button data-j="' + j + '" class="' + (a === qOf(r.t, j).c ? "r-ok" : "r-bad") + '" aria-label="Otázka ' + (j + 1) + '">' + (j + 1) + '</button>';
      }).join("") + '</div>' + again + '</section>' +
      idx.map(function (j) { return review(r, j); }).join("") +
      (idx.length ? '<div class="end">' + again + '</div>' : "");
    app.querySelectorAll(".again").forEach(function (b) { b.onclick = start; });
    app.querySelectorAll(".grid button").forEach(function (b) {
      b.onclick = function () {
        var el = document.getElementById("rv" + b.dataset.j);
        if (!el) { result(id, true); el = document.getElementById("rv" + b.dataset.j); }
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
      };
    });
  }

  function review(r, i) {
    var q = qOf(r.t, i), a = r.ans[i];
    return '<article class="card rev" id="rv' + i + '"><span class="qno ' + (a === q.c ? "ok" : "bad") + '">' + (i + 1) + '</span>' +
      (q.img ? '<div class="qimg"><img src="' + esc(q.img) + '" alt="" loading="lazy"></div>' : "") +
      '<p class="qtext">' + esc(q.q) + '</p><div class="opts">' + q.a.map(function (o, j) {
        var cls = j === q.c ? " is-ok" : (j === a ? " is-bad" : "");
        return '<button class="opt' + cls + '" disabled><span class="l">' + L(j) + '</span><span>' + esc(o) + '</span></button>';
      }).join("") + '</div>' +
      '<div class="why">' + esc(q.v) + '</div></article>';
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
