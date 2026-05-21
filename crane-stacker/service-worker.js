// Service worker for Crane Stacker
// Caches app shell + external dependencies for offline use.

const CACHE_VERSION = 'crane-stacker-v3.3';
const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];
// Cross-origin assets that should also be cached on first load
const EXTERNAL_ASSETS = [
  'https://cdn.jsdelivr.net/npm/matter-js@0.19.0/build/matter.min.js',
  'https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Lilita+One&display=swap'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      // Core assets must succeed
      return cache.addAll(CORE_ASSETS).then(() => {
        // External assets are best-effort (won't fail the install)
        return Promise.all(
          EXTERNAL_ASSETS.map((url) =>
            cache.add(new Request(url, { mode: 'no-cors' })).catch(() => null)
          )
        );
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// Cache-first strategy: serve from cache, fall back to network, then cache the network response
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          // Only cache successful, basic/cors responses
          if (response && (response.status === 200 || response.type === 'opaque')) {
            const clone = response.clone();
            caches.open(CACHE_VERSION).then((cache) => {
              cache.put(event.request, clone).catch(() => {});
            });
          }
          return response;
        })
        .catch(() => {
          // Network failed and nothing cached — return a minimal offline response for navigations
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
          return new Response('Offline', { status: 503, statusText: 'Offline' });
        });
    })
  );
});
