# Kid Apps

A small launcher and a growing collection of educational web games for kids. Hosted at https://apps.bryllelagunda.com.

## Live apps

| Slug | URL | Status |
|------|-----|--------|
| `crane-stacker` | `/crane-stacker/` | v3.1, shipped |
| `printables` | `/printables/` | v1.0, shipped |
| _(more to come)_ | | |

## What's in here

- `index.html` — the **launcher** (tile grid). Visit the root URL and you land here.
- `crane-stacker/` — first game. Phonics-flavored crane block-stacker for ages 4–6.
- `printables/` — worksheet maker. A parent tool: build practice sheets, print the pack as one PDF.
- `CLAUDE.md` — workspace-level conventions for AI coders working in this repo.
- `vercel.json` — Vercel routing & cache headers (esp. for service workers).

## First-time deploy (one-time migration from cPanel to Vercel)

1. **Create a GitHub repo** (suggested name: `kid-apps`). Push this directory to it as the initial commit.
2. **Create a Vercel project.** Sign in at https://vercel.com (with your GitHub account is easiest). New Project → Import the GitHub repo → keep defaults → Deploy.
3. **Add the custom domain.** Vercel project → Settings → Domains → add `apps.bryllelagunda.com`. Vercel will display a DNS record to create.
4. **Update DNS.** At wherever `bryllelagunda.com` is managed, add the CNAME Vercel asked for (typically: `apps` → `cname.vercel-dns.com`). If `apps.bryllelagunda.com` currently points at your cPanel host, change that record. Wait 5–15 minutes for DNS to propagate.
5. **Verify HTTPS.** Vercel auto-provisions a Let's Encrypt cert. Visit `https://apps.bryllelagunda.com/` — you should see the launcher. Visit `https://apps.bryllelagunda.com/crane-stacker/` — you should see the game.
6. **Decommission cPanel.** Once Vercel is live, you can remove `cranewithkid/` from your cPanel host. The DNS change in step 4 means the subdomain no longer points there anyway.

## Routine deploys

```
git add .
git commit -m "what changed"
git push
```

Vercel auto-deploys on push to `main`. Live in ~30 seconds.

**Important on every deploy that touches a service worker:** bump the `CACHE_VERSION` constant in that service worker file. Otherwise installed PWAs may keep serving the old cached version to users.

## Local preview before pushing

Service workers refuse to run over `file://`, so:

```
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. (Or `npx http-server -p 8000` if you prefer Node.)

## Adding a new app

1. Create a new subdirectory, e.g. `word-builder/`.
2. Drop in its own `index.html`, `manifest.json`, `service-worker.js`, and icons.
3. Write a `CLAUDE.md` inside that subdirectory documenting its design decisions.
4. Add a new tile to the launcher's `index.html` (in the `<main id="apps">` block).
5. Commit, push. The new app is live at `/word-builder/` and visible on the launcher.

See `CLAUDE.md` (workspace) and `crane-stacker/CLAUDE.md` (per-app example) for conventions.
