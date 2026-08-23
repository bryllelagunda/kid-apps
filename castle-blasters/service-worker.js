// Service worker for Castle Blasters.
// Caches the app shell + external dependencies for offline use.
//
// BUMP CACHE_VERSION ON EVERY DEPLOY, without exception.

const CACHE_VERSION = 'castle-blasters-v1.1';

// -----------------------------------------------------------------------------
// STRATEGY — 'network-first' through M3, flips to 'cache-first' at M4.
//
// This is one constant on purpose. A cache-first SW during rapid iteration
// means the tablet serves yesterday's build unless the version is bumped on
// every single push, and the milestone whose entire job is judging *feel* must
// not be judged against a stale file. From M4 the app is shipping rather than
// iterating, and cache-first is the correct offline story.
// -----------------------------------------------------------------------------
const STRATEGY = 'network-first';

const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

// Cross-origin assets that should also be cached on first load.
// These are added individually and best-effort: a naive SW that puts the CDN
// URLs in addAll() fails the whole install on one jsdelivr blip, and the app
// never becomes offline-capable.
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

// Runtime caching, shared by both strategies. The gstatic .ttf files behind the
// Google Fonts CSS are not precached by anything in this repo — this is what
// puts them in the cache after the first online load.
function cachePut(request, response) {
  if (response && (response.status === 200 || response.type === 'opaque')) {
    const clone = response.clone();
    caches.open(CACHE_VERSION).then((cache) => {
      cache.put(request, clone).catch(() => {});
    });
  }
  return response;
}

function offlineFallback(request) {
  if (request.mode === 'navigate') return caches.match('./index.html');
  return new Response('Offline', { status: 503, statusText: 'Offline' });
}

function networkFirst(request) {
  return fetch(request)
    .then((response) => cachePut(request, response))
    .catch(() => caches.match(request).then((cached) => cached || offlineFallback(request)));
}

function cacheFirst(request) {
  return caches.match(request).then((cached) => {
    if (cached) return cached;
    return fetch(request)
      .then((response) => cachePut(request, response))
      .catch(() => offlineFallback(request));
  });
}

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    STRATEGY === 'cache-first' ? cacheFirst(event.request) : networkFirst(event.request)
  );
});
