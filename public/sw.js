// MasakJe service worker: keeps the app usable with no signal (e.g. inside a supermarket).
// Pages and files: try the network for up to 3 s (so updates arrive), else use the saved copy.
// API calls are never cached: the app itself queues changes and syncs when back online.
const CACHE = "masakje-v1";
const SHELL = ["/", "/manifest.webmanifest", "/icon.svg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== self.location.origin || url.pathname.startsWith("/api/")) return;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const network = fetch(e.request).then(r => { if (r.ok) cache.put(e.request, r.clone()); return r; });
    const timeout = new Promise(res => setTimeout(() => res(null), 3000));
    try {
      const r = await Promise.race([network, timeout]);
      if (r) return r;
    } catch (err) { /* offline */ }
    const cached = await cache.match(e.request) || (e.request.mode === "navigate" ? await cache.match("/") : null);
    return cached || network;
  })());
});
