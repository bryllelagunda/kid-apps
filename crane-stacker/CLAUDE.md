# Crane Stacker — Claude Code Context

## Project overview

A phonics/literacy crane stacking game for a 4-year-old. Built as a Progressive Web App so it installs to a tablet home screen and runs offline.

- **Current version:** 3.1
- **Production URL:** https://apps.bryllelagunda.com/cranewithkid/
- **Hosting:** cPanel-based static hosting; deploys via File Manager upload; HTTPS via Let's Encrypt
- **Operator:** Parent. Communicates in plain English about design choices. Has not been editing code by hand — Claude Code is expected to perform end-to-end changes. Has a separate Claude chat session for strategic/design conversations; this codebase is for execution.

## Tech stack (do NOT change without explicit ask)

- Single `index.html` with `<style>` and `<script>` embedded. No build step. No framework.
- Matter.js v0.19.0 (2D physics) — loaded from jsdelivr CDN.
- Google Fonts: Fredoka, Lilita One — loaded from fonts.googleapis.com.
- Web Speech API (`SpeechSynthesisUtterance`) for spoken letter/number names.
- PWA: `manifest.json` + `service-worker.js`.
- Icons generated via `_make_icons.py` (Python + Pillow) at 192/512/maskable-512/favicon-32.

Rationale: parent uploads via cPanel File Manager; any build complexity breaks that workflow. Vanilla JS keeps the source legible.

## Files

| File | Role |
|------|------|
| `index.html` | The game. ~620 lines. All HTML, CSS, JS embedded. |
| `manifest.json` | PWA metadata. |
| `service-worker.js` | Caches app shell + CDN assets for offline. **Bump `CACHE_VERSION` on every deploy.** |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `favicon-32.png` | PWA + tab icons. |
| `_make_icons.py` | Regenerates icons. Re-run if icon design changes. Requires `pip install Pillow`. |
| `README.md` | User-facing setup and deploy instructions. |
| `CLAUDE.md` | This file. |

## Design decisions (iterated with the kid, do not revert without ask)

### Game mechanics
- **Crane horizontal**: drag canvas, or arrow keys / A D.
- **Cable vertical**: hold ↓ button (or ArrowDown) to lower at 3.2 px/frame; hold ↑ (or ArrowUp) to raise at 5.0 px/frame. Up is faster because "I panicked" must feel responsive.
- **Auto-release on contact**: descending block detaches automatically when it touches the surface below. No second tap required. Reduces cognitive load for a 4yo.
- **DROP button**: secondary chaos release. Drops from current cable height, no contact check. Kept for variety.
- **Tap a landed block**: speaks its label. For reinforcement.
- **Tower-full handling**: when blocks reach the spawn point, new spawns are blocked, the reset button pulses red (`.glow` CSS class), and the game auto-retries every ~45 frames. Implemented in `spawnAreaBlocked()` and `spawnPending()`.

### Visual / audio
- Blocks have **two visible LEGO studs** on top, in a darker shade of the block color. Matches the kid's physical LEGO interest. Drawn before the block body so the body covers their bases.
- Crane trolley: **hazard-striped (yellow + black)** with wheels and a clipped diagonal pattern.
- Hook: **red-and-black electromagnet** bar with "N" and "S" labels. Visible on pending block and during cable retract.
- **Letter NAMES via TTS** ("S" → "ess", "A" → "ay"), NOT phonetic sounds. We tried phonics — browser TTS can't produce clean phonemes, and the parent prefers names regardless. Numbers spoken as their names ("one", "two").
- **Default mode is SATPIN** (the letters S A T P I N). Originally chosen for phonics density; kept after the phonics pivot because it's still a useful 6-letter starter pool.
- **No prose hints on the play screen**. The visible buttons are the documentation.

### Physics tuning
```
gravity.y = 1.0
restitution = 0.05      // blocks don't bounce much
friction = 0.95
frictionStatic = 1.2
density = 0.004
chamfer.radius = 6
block size = 60px
```
Reduces chaos-frustration without removing the topple-and-balance lesson.

## Things NOT to do

- Don't add a build tool, bundler, transpiler, or framework.
- Don't add npm dependencies. Everything via CDN, cached by service worker.
- Don't switch letter names back to phonetic sounds without explicit ask.
- Don't add ads, analytics, or external network calls.
- Don't make controls more complex — 4-year-old's game.
- Don't auto-clear the kid's tower except via explicit reset.
- Don't use localStorage for game state. Blocks are session-only and that's intentional.
- Don't introduce modal dialogs that block play.
- Don't change tunings (gravity, friction, cable speeds, block size) without ask — they were arrived at through testing.

## Deployment

1. **Bump `CACHE_VERSION`** in `service-worker.js` (e.g., `crane-stacker-v3.1` → `v3.2`). Without this, browsers serve stale cache.
2. Upload all files to `public_html/apps.bryllelagunda.com/cranewithkid/` via cPanel File Manager.
3. Confirm HTTPS is active on the subdomain (Let's Encrypt via cPanel).
4. Visit the URL once while online so the service worker caches everything.
5. Installed PWAs may need a force-quit to pick up the new service worker.

All paths in the project are relative (`./icon-192.png` etc.), so subpath hosting works without code changes. Service worker scope defaults to its location (i.e., `/cranewithkid/`).

## Version history (key turning points)

- **V1**: Basic crane, dropped blocks, three modes (numbers, letters, mixed).
- **V2**: Phonics intent — sounds on drop, SATPIN default, LEGO studs, tap-to-hear, mute toggle.
- **V3**: Replaced one-shot DROP with hold-↓-to-lower-cable + auto-release on contact. Magnet hook.
- **V3 PWA**: manifest + service worker + icons + README. Deployable.
- **V3.1**: Fixed spawn-into-stack feedback loop (kid played past the design ceiling). Switched TTS from phonetic sounds to letter names. Added reset-button glow when tower full. Cull off-screen blocks (above and below).

## Possible future features (queued, NOT committed — confirm with parent first)

- **Magnet-pickup mode**: the hook can pick up *already-placed* blocks for rearrangement. Different cognitive skill — planning, undo. Major addition.
- **Word-building mode**: target picture (e.g., a cat) appears, hopper offers needed letters, kid stacks them to spell the word. Connects letter recognition to actual reading.
- **Sound effects**: thunk/ding/crash. Needs hosted audio files — would slightly complicate offline if not bundled.
- **Save tower as PNG** via `canvas.toDataURL()` for sharing.
- **Number-counting mode**: voice counts blocks as they're added.
- **Sight-word mode**: blocks display common 3-letter words instead of single letters.

## Coding conventions

- IIFE wrap (`(() => { ... })()`) to avoid globals.
- camelCase for variables and functions.
- CSS variables in `:root` for all colors. New colors go there, not inline.
- Touch + mouse + keyboard all supported on every interactive surface.
- Safe-area insets (`env(safe-area-inset-*)`) for iOS notch/home-indicator.
- Use `Composite.allBodies(world).filter(b => b.label === 'block')` to access game blocks; static bodies have other labels.
- All physics bodies created should have a `label` and (for blocks) a `body.brick = { label, color }` attached.

## Working style with the parent

- Direct and concrete. Prefers specific options to abstract explanations.
- Push back when a request would be a mistake. Don't capitulate without new evidence.
- Confidence levels welcome (high/moderate/low) when uncertain.
- Strategic decisions happen in chat. By the time something arrives at this codebase, the *what* is decided — the question is the *how*.
