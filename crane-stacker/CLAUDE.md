# Crane Stacker — Claude Code Context

## Project overview

A letter/number recognition crane stacking game for a 4-year-old. Built as a Progressive Web App so it installs to a tablet home screen and runs offline.

- **Current version:** 4.1
- **Production URL:** https://apps.bryllelagunda.com/crane-stacker/
- **Hosting:** Vercel (static, auto-deployed from GitHub `main` branch)
- **Operator:** Parent. Communicates in plain English about design choices. Has not been editing code by hand — Claude Code is expected to perform end-to-end changes. Has a separate Claude chat session for strategic/design conversations; this codebase is for execution.

## Tech stack (do NOT change without explicit ask)

- Single `index.html` with `<style>` and `<script>` embedded. No build step. No framework.
- Matter.js v0.19.0 (2D physics) — loaded from jsdelivr CDN.
- Google Fonts: Fredoka, Lilita One — loaded from fonts.googleapis.com.
- Web Speech API (`SpeechSynthesisUtterance`) for spoken letter/number names.
- PWA: `manifest.json` + `service-worker.js`.
- Icons generated via `_make_icons.py` (Python + Pillow) at 192/512/maskable-512/favicon-32.

Rationale: vanilla JS + no build step keeps the source legible and the deploy trivial (`git push`).

## Files

| File | Role |
|------|------|
| `index.html` | The game. All HTML, CSS, JS embedded. |
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
- **DROP button**: secondary chaos release. Drops from current cable height, no contact check. Kept for variety. In Claw Mode, DROP releases the currently carried block.
- **Tap a landed block**: speaks its label. For reinforcement.
- **Tower-full handling**: when blocks reach the spawn point, new spawns are blocked, the reset button pulses red (`.glow` CSS class), and the game auto-retries every ~45 frames. Implemented in `spawnAreaBlocked()` and `spawnPending()`.
- **Claw Mode** (v4.0): opt-in rearrangement mode toggled with the 🦾 button in the HUD right-stack. Normal drop gameplay is the default.
  - When ON, the magnet hook is replaced with a two-jaw claw grapple drawn by `drawClaw(x, y, closed)`.
  - No pending block is spawned while Claw Mode is active. `spawnPending()` returns early if `clawMode` is true.
  - Lowering the claw near a landed block auto-grabs it (`tryGrabBlock()`): sets the body static and stores a reference in `clawCarrying`. Grab radius is 55 px on both axes from `CLAW_BLOCK_Y` offset below the cable end.
  - While carrying, `Body.setPosition` and `Body.setAngle` reposition the block each frame so it follows the crane; the block is kept upright (angle 0).
  - DROP or clicking 🦾 again calls `releaseCarried()`: sets body dynamic, zeroes velocity, starts a 600 ms re-grab cooldown (`_clawReleaseMs`).
  - `trackLandings` and the off-screen cull both skip the carried block (`b !== clawCarrying`) to avoid counting it while held or culling it off-screen.
  - Switching FROM Claw Mode: releases any carried block first, then calls `spawnPending()` to resume normal play.
  - `CLAW_BLOCK_Y = 50` — block-centre y-offset from cable end when carried. Adjust only if claw visual/physics feel misaligned.
  - **Context-aware DROP/GRAB button** (v4.1): when Claw Mode is ON and claw is empty, the DROP button label changes to "GRAB" (blue) and pressing it calls `tryGrabBlock()`. When carrying a block it shows "DROP" and releases. Off-screen blocks and already-static bodies are excluded from grab candidates.
  - **Grab highlight** (v4.1): a dashed blue ring is drawn around the nearest grabbable block when the claw is within range (55 px on both axes from the grab point). Cleared during the 600 ms post-release cooldown.

### Visual / audio
- Blocks have **two visible LEGO studs** on top, in a darker shade of the block color. Matches the kid's physical LEGO interest. Drawn before the block body so the body covers their bases.
- Crane trolley: **hazard-striped (yellow + black)** with wheels and a clipped diagonal pattern.
- Hook: **red-and-black electromagnet** bar with "N" and "S" labels. Visible on pending block and during cable retract.
- **Audio is letter-name only** (no toggle, no modes):
  - Letters speak their name — S → "ess", A → "ay", T → "tee", P → "pee", I → "eye", N → "en", etc. Explicit `LETTER_NAMES` map covers A–Z for consistent TTS output across devices/browsers.
  - Numbers speak their name — 0 → "zero", 1 → "one", etc. via `NUM` array.
  - Word Clue / phonics modes were removed in v3.6 — browser TTS is not reliable for those use cases. If word-association or true phonics is ever added, the right solution is a separate app or recorded audio files (one mp3 per letter), not browser TTS.
- **Voice selection**: `initVoices()` picks the best available English voice at startup (prefers Samantha / Karen / Google UK English Female / Microsoft Zira). Falls back to any `en-US/GB/AU` voice, then any English voice. Rate and pitch are in `SPEAK_RATE` / `SPEAK_PITCH` constants at the top of the script.
- **Default mode is SATPIN** (the letters S A T P I N). Originally chosen for phonics density; kept because it's a useful 6-letter starter pool.
- **No prose hints on the play screen**. The visible buttons are the documentation.
- **Custom block set** (v4.1): the SATPIN mode pool is parent-editable. A small ⚙ button beside the mode pills opens a compact settings panel (non-modal). The parent types any letters A–Z and/or digits 0–9; invalid characters are stripped, duplicates removed, lowercase uppercased. Minimum 1 character, maximum 36. The pill label changes from "SATPIN" to "CUSTOM" when the set differs from the default. A "Reset SATPIN" button restores the default. If the current pending block's label is no longer in the new set, a fresh block is spawned. A–Z and 0–9 modes are unaffected by the custom set.
  - `localStorage` key: `craneStackerCustomSet` — stores a JSON array of characters, e.g. `["A","B","C"]`. This is the **only** use of localStorage in this app. Block/tower positions are NOT persisted and remain session-only.

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
- Don't add a second audio mode (no toggle, no wordclue, no phonics). Audio is letter names + number names only.
- Don't add ads, analytics, or external network calls.
- Don't make controls more complex — 4-year-old's game.
- Don't auto-clear the kid's tower except via explicit reset.
- Don't use localStorage for game state. Blocks are session-only and that's intentional. **Exception (v4.1)**: `localStorage` is used for the parent's custom block set preference only (`craneStackerCustomSet`). Block and tower positions are never persisted.
- Don't introduce modal dialogs that block play.
- Don't change tunings (gravity, friction, cable speeds, block size) without ask — they were arrived at through testing.

## Deployment

Routine deploy: `git add <files> && git commit -m "..." && git push`. Vercel auto-deploys in ~30 seconds.

**Always bump `CACHE_VERSION`** in `service-worker.js` (e.g., `crane-stacker-v3.6` → `v3.7`). Without this, browsers serve stale cache.

All paths in the project are relative (`./icon-192.png` etc.), so subpath hosting works without code changes.

## Version history (key turning points)

- **V1**: Basic crane, dropped blocks, three modes (numbers, letters, mixed).
- **V2**: Phonics intent — sounds on drop, SATPIN default, LEGO studs, tap-to-hear, mute toggle.
- **V3**: Replaced one-shot DROP with hold-↓-to-lower-cable + auto-release on contact. Magnet hook.
- **V3 PWA**: manifest + service worker + icons + README. Deployable.
- **V3.1**: Fixed spawn-into-stack feedback loop (kid played past the design ceiling). Switched TTS from phonetic sounds to letter names. Added reset-button glow when tower full. Cull off-screen blocks (above and below).
- **V3.3**: Improved voice selection (prefers Samantha/Karen/Google UK English Female). Explicit LETTER_NAMES map for consistent TTS. Added Phonics-ish mode (experimental) with parent toggle "Aa/Ph" button in HUD.
- **V3.4**: Fixed audio in Chrome/Brave — `speechSynthesis.resume()` added before every speak so Chrome doesn't silently stall. Refactored voice init into `initVoices()` with `DEBUG_SPEECH` flag. Per-drop speech guard (`_lastDropMs` + clearing `pending` before speaking) prevents duplicate speech from same release event. Unlock utterance now completes near-instantly (`rate=10`).
- **V3.5**: Replaced Phonics-ish mode (awkward browser TTS phonemes) with Word Clue mode — speaks letter name + anchor word (e.g. "ess. Sun."). Toggle label changed from "Ph" to "Ww". Full A-Z `WORD_CLUES` map with familiar 4-year-old words.
- **V3.7**: Fixed letter A TTS — changed `LETTER_NAMES.A` from `'ay'` to `'A'`. Some TTS engines (especially NZ/AU voices) read the word "ay" as /aɪ/, identical to "eye" for I. The bare uppercase letter `'A'` triggers each engine's built-in letter-name pronunciation, which is reliably /eɪ/.
- **V3.6**: Removed Ww / Word Clue mode entirely. Crane Stacker now uses only letter names and number names — no toggle, no secondary mode. Word-association and true phonics belong in a future separate app or a recorded-audio feature, not browser TTS inside Crane Stacker. Moved hosting from cPanel to Vercel.
- **V4.0**: Added optional Claw Pickup mode (🦾 toggle in HUD). Normal crane-drop gameplay is unchanged and remains the default. Claw mode lets the child grab and rearrange already-landed blocks with a two-jaw grapple attachment. No new physics tuning — only existing `Body.setPosition`/`Body.setStatic` APIs used.
- **V4.1**: Improved Claw Mode UX — DROP button becomes "GRAB" (blue) when claw is empty; pressing GRAB attempts a manual grab of the nearest eligible block. Grab highlight (dashed blue ring) shows the nearest grabbable block when in range. Added parent-editable custom block set: ⚙ button near mode pills opens a compact panel; set is persisted to localStorage. SATPIN pill relabels to "CUSTOM" when the set differs from default. A–Z and 0–9 modes unchanged.

## Possible future features (queued, NOT committed — confirm with parent first)

- **Word-building mode**: target picture (e.g., a cat) appears, hopper offers needed letters, kid stacks them to spell the word. Connects letter recognition to actual reading.
- **Phonics / word-clue audio**: per-letter recorded mp3 files (not browser TTS). Would require hosted audio — keep offline bundle in mind.
- ~~**Magnet-pickup mode**~~ — shipped as **Claw Pickup mode** in v4.0.
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
