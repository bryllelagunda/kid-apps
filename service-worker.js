// Service worker for the LAUNCHER (apps.bryllelagunda.com/).
// Carefully scoped: does NOT cache or intercept requests for sub-apps —
// each app subdirectory has its own service worker with its own scope.

const CACHE_VERSION = 'kid-apps-launcher-v1.0';

const OWN_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './favicon-32.png'
];

// External CDN assets the launcher itself uses (best-effort cached)
const EXTERNAL_ASSETS = [
  'https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Lilita+One&display=swap'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) =>
      cache.addAll(OWN_ASSETS).then(() =>
        Promise.all(
          EXTERNAL_ASSETS.map((u) =>
            cache.add(new Request(u, { mode: 'no-cors' })).catch(() => null)
          )
        )
      )
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  const sameOrigin = url.origin === self.location.origin;

  // Hands-off: anything in a subdirectory (e.g. /crane-stacker/...) belongs to that app's SW.
  // Match a path with at least one segment, e.g. /something/...
  if (sameOrigin && /^\/[\w-]+\/(.+)?$/.test(url.pathname)) {
    return; // let the network and the sub-app's SW handle it
  }

  // Decide whether this is a request we own
  const isOwnPath =
    sameOrigin && (
      url.pathname === '/' ||
      url.pathname === '/index.html' ||
      OWN_ASSETS.some((a) => url.pathname === a.replace(/^\.\//, '/'))
    );
  const isAllowedExternal =
    url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';

  if (!isOwnPath && !isAllowedExternal) return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          if (response && (response.status === 200 || response.type === 'opaque')) {
            const clone = response.clone();
            caches.open(CACHE_VERSION).then((c) => c.put(event.request, clone).catch(() => {}));
          }
          return response;
        })
        .catch(() => {
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
          return new Response('Offline', { status: 503 });
        });
    })
  );
});
