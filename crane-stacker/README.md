# Crane Stacker — PWA (v3.1)

A phonics crane stacking game for kids learning letters and numbers.

**What's new in v3.1:**
- Tower-full detection: when blocks reach the spawn point, new blocks stop spawning instead of feedback-looping (fixes "DROP making lots of letters at once").
- Reset button glows red when the tower fills up, so it's obvious what to press.
- Voice now says **letter names** (S → "ess", A → "ay") instead of letter sounds.
- Numbers still spoken as their names (1 → "one").
- Off-screen blocks (above or below the screen) are now cleaned up automatically.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The game itself. Self-contained HTML + JS. |
| `manifest.json` | PWA metadata (app name, icons, theme color). |
| `service-worker.js` | Caches the app for offline use. |
| `icon-192.png` | Home-screen icon (small). |
| `icon-512.png` | Home-screen icon (large). |
| `icon-maskable-512.png` | Android adaptive icon variant. |
| `favicon-32.png` | Browser tab icon. |
| `_make_icons.py` | Optional. Regenerate icons if you tweak colors/letter. |

## How to test locally

You can't just double-click `index.html` because service workers refuse to run over `file://`. You need a local web server. From inside this folder:

**Option A — Python (already installed on most systems):**
```bash
python3 -m http.server 8000
```
Then open `http://localhost:8000` in Chrome or Safari.

**Option B — Node:**
```bash
npx http-server -p 8000
```

Once it loads, open DevTools → Application → Service Workers to confirm it registered.

## How to put it on the internet (free, no signup needed for the simplest path)

**Easiest: Netlify Drop**
1. Go to https://app.netlify.com/drop
2. Drag this entire folder onto the page.
3. You get a URL like `https://random-words-12345.netlify.app`. That's your app.
4. Open the URL on your kid's tablet and follow the install steps below.

(If you create a free Netlify account, you can claim the site and rename it to something like `crane-for-mykid.netlify.app`.)

**Other free hosts that work the same way:**
- **Cloudflare Pages** (https://pages.cloudflare.com) — free, fast, requires a free account.
- **GitHub Pages** — free if you know git. Push the folder to a repo, enable Pages in repo settings.
- **Vercel** (https://vercel.com) — free, requires account, deploys from git or via CLI.

## How to put it on your own cPanel subdomain (e.g. apps.yourdomain.com/cranewithkid)

1. **Confirm HTTPS is enabled** on the subdomain in cPanel. Service workers will not register over plain HTTP. cPanel → "SSL/TLS Status" → enable AutoSSL or install Let's Encrypt for the subdomain if not already on.
2. In cPanel's File Manager, navigate to the subdomain's document root (typically `public_html/apps.yourdomain.com/`).
3. Create a folder named `cranewithkid`.
4. Upload all the files from this bundle into `cranewithkid/` (you can drag the contents of the unzipped folder, or upload the zip and extract in cPanel).
5. Visit `https://apps.yourdomain.com/cranewithkid/` to verify it works.

All file paths in this app are relative (`./icon-192.png`, `./manifest.json`, etc.), so subpath hosting works without any code changes. The service worker registers with scope `/cranewithkid/` automatically — it can only control URLs under that subpath, which is what you want.

## How to install on a tablet/phone

### Android (Chrome)
1. Open the URL in Chrome.
2. Chrome usually pops up an "Install" prompt at the bottom — tap it.
3. If it doesn't, tap the three-dot menu → "Install app" or "Add to Home screen".
4. The crane icon appears on the home screen. Tap it — it opens fullscreen with no browser chrome.

### iOS (Safari — must be Safari, not Chrome)
1. Open the URL in Safari.
2. Tap the Share button (the square with an arrow).
3. Scroll down and tap "Add to Home Screen".
4. Tap "Add" in the top right.
5. The crane icon appears on the home screen.

### iPad-specific note
iPadOS treats PWAs slightly differently — they still work fullscreen, but you may want to lock orientation in iPad's settings if the kid keeps rotating the screen mid-game.

## Updating the app

When you change `index.html` and redeploy:
- The service worker caches the *old* version. Users will see the new version on the **second** load after the deploy.
- To force an immediate update, bump `CACHE_VERSION` in `service-worker.js` (e.g., `v3.0` → `v3.1`) before deploying. This invalidates the old cache.

## Known limitations

- **iOS speech synthesis**: works inside PWAs, but the first sound may be delayed until the kid taps something. The unlock is handled automatically, but be aware.
- **iOS install isn't obvious**: the Share → Add to Home Screen flow is not discoverable for most users. Walk grandma through it once.
- **Offline only works after the first online visit**. The service worker can only cache what it's seen.
- **Service workers require HTTPS** in production (localhost is exempt). All the hosts listed above provide HTTPS automatically.

## Regenerating icons

If you want to change the icon (different letter, different color), edit `_make_icons.py` and run:

```bash
pip install Pillow
python3 _make_icons.py
```

The script generates all four sizes.
