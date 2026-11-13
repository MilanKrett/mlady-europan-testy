/* Offline režim: aplikácia a dáta sa uložia pri prvej návšteve, obrázky postupne pri zobrazení. */
var V = "me-testy-v6";
var CORE = ["./", "index.html", "style.css", "app.js", "data/otazky.json", "data/testy.json", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "pismo/inter.woff2"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(V).then(function (c) { return c.addAll(CORE); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== V; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  var u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  var core = /\.(html|js|css|json|webmanifest)$/.test(u.pathname) || u.pathname.endsWith("/");
  if (core) {
    // najprv sieť (aby sa prejavili opravy), pri výpadku cache
    e.respondWith(fetch(e.request).then(function (r) {
      var cp = r.clone(); caches.open(V).then(function (c) { c.put(e.request, cp); }); return r;
    }).catch(function () { return caches.match(e.request, { ignoreSearch: true }); }));
  } else {
    e.respondWith(caches.match(e.request).then(function (m) {
      return m || fetch(e.request).then(function (r) {
        var cp = r.clone(); caches.open(V).then(function (c) { c.put(e.request, cp); }); return r;
      });
    }));
  }
});
