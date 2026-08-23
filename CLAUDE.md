# Kid Apps Workspace — Claude Code Context

## Purpose

A growing collection of educational web games for a 4-year-old child. Hosted at https://apps.bryllelagunda.com — root is a launcher with tiles linking to each app.

## Architecture

- **Monorepo**, one repo on GitHub, one Vercel project, one URL space.
- **Root** is the launcher (`/index.html` — grid of app tiles).
- **Each app** lives in its own subdirectory (`/crane-stacker/`, etc.) and is independently:
  - Installable as its own PWA (manifest + service worker per subdir).
  - Deployed via the same `git push` that deploys the launcher.
  - Documented in its own subdirectory `CLAUDE.md`.

## Stack

- Pure static site. No build step. No framework. No bundler.
- Hosted on Vercel free tier.
- Deploys triggered by `git push` to `main` on the linked GitHub repo.
- Custom domain `apps.bryllelagunda.com` mapped via CNAME at the DNS provider to Vercel.
- Browser TTS for audio. CDN-loaded libraries (Matter.js, Google Fonts). All other assets are local files in the repo.

## File layout

```
/                                      ← apps.bryllelagunda.com
├── README.md
├── CLAUDE.md                          ← (this file)
├── vercel.json                        ← cache headers, esp. for service workers
├── index.html                         ← launcher
├── manifest.json                      ← launcher PWA manifest
├── service-worker.js                  ← launcher SW (scoped to root; ignores sub-apps)
├── icon-*.png, favicon-32.png         ← launcher icons
├── _make_icons.py                     ← regenerates launcher icons
├── crane-stacker/                     ← apps.bryllelagunda.com/crane-stacker/
│   ├── CLAUDE.md                      ← app-specific context (read this when editing the crane game)
│   ├── README.md
│   ├── index.html
│   ├── manifest.json
│   ├── service-worker.js
│   └── icon-*.png, _make_icons.py
└── printables/                        ← apps.bryllelagunda.com/printables/
    ├── CLAUDE.md                      ← app-specific context (read before editing the worksheet maker)
    ├── README.md
    ├── index.html                     ← everything: HTML, CSS, JS, embedded font
    ├── manifest.json
    ├── service-worker.js
    └── icon-*.png, _make_icons.py
```

Not every app is a *game*. `printables/` is a parent-facing tool that produces paper for
the kid; the launcher tiles it alongside the games, but its UI is meant for an adult.

## Conventions for any new app added to this workspace

1. **One subdirectory per app.** Slug-style folder name (`crane-stacker`, `word-builder`, etc.).
2. **Self-contained.** No code imported from sibling apps. If something is genuinely shared (e.g. a future shared sound library), the parent will decide consciously when to extract it.
3. **Each app gets its own `CLAUDE.md`** with its own design decisions and "do not change" list.
4. **Each app gets its own service worker**, scoped to its subdirectory. The launcher SW explicitly ignores subdirectory requests so scopes don't collide.
5. **All paths relative** (`./manifest.json`, `./icon-192.png`). Subpath hosting must just work.
6. **Each app gets its own tile** in the launcher's `index.html` `<main id="apps">` block. Use the app's icon-512.png as the tile image.
7. **Bump cache versions on every deploy** to that app's service worker.

## Things NOT to do (workspace-level)

- **Don't add a build step** (no webpack, vite, rollup, parcel, etc.). The deploy workflow assumes static files.
- **Don't add npm dependencies** that need bundling. CDN is fine.
- **Don't share code between apps prematurely.** Each game is small enough to live independently.
- **Don't add a database** (Turso, Postgres, etc.) unless the parent explicitly asks. `localStorage` solves 95% of "save the high score" needs without backend complexity.
- **Don't add auth.** No login flow exists; don't introduce one.
- **Don't add ads, analytics, or third-party tracking.**
- **Don't restructure the monorepo** (move files between folders, rename subdirectories, etc.) without explicit ask. URLs are user-facing.

## Deployment

The deploy is two steps the first time, one step after that.

**First-time setup** (done by parent, not by Claude Code):

1. Create a new GitHub repo (suggest: `kid-apps`).
2. Push this directory to the repo.
3. In Vercel: New Project → Import the GitHub repo → keep defaults (auto-detected as static) → Deploy.
4. In the Vercel project's Settings → Domains: add `apps.bryllelagunda.com`. Vercel will show a DNS record to add.
5. At the parent's DNS provider, add the CNAME (typically `apps → cname.vercel-dns.com`).
6. Wait ~5 minutes for DNS to propagate. Vercel auto-provisions HTTPS.

**Routine deploys** (after first-time setup):

```bash
git add . && git commit -m "what changed" && git push
```

Vercel auto-deploys. Live in ~30 seconds.

## Domain & DNS

- Apex domain: `bryllelagunda.com` (registered separately, not managed here).
- Subdomain: `apps.bryllelagunda.com` → points to Vercel.
- Other related subdomains (e.g. `stocks.bryllelagunda.com`) stay on cPanel; only `apps` moves to Vercel.

## When the parent says "ship it"

The deploy workflow is just `git push`. Don't suggest manual file uploads — that's the cPanel era and it's behind us.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec
