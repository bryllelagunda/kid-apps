# Castle Blasters — Claude Code Context

## What this is

An offline, turn-based physics artillery game. Slingshot a cannonball at a
castle of letter and number blocks and watch it come apart. Lives at
`apps.bryllelagunda.com/castle-blasters/`.

**Source of truth is `docs/designs/castle-blasters.md`** (approved,
eng-reviewed). This file records what is actually built, the measured numbers,
and the things not to change. Where this file and the plan disagree about a
number, the disagreement is written down explicitly below with the reason.

## Status: M1 (Feel) complete

M1 was the whole bet: does slingshotting a ball at a tower feel good on a
tablet. Built:

- Canvas, fixed 1024×768 world, letterboxed with a uniform scale.
- Ground from a descriptor (flat in M1; stepped platforms land at M2).
- ONE castle: 3 columns × 4 rows = 12 wood blocks, each carrying a letter or
  a number. One character standing on top of it.
- The slingshot gesture, the live dotted arc, projectile flight, damage,
  block destruction, WebAudio boom / launch / thunk.
- `players[]`, `setState()` and the `PLAYER_TURN ⇄ TURN_RESULT` loop running
  one slot — present from the first line, not retrofitted.
- `manifest.json` + `service-worker.js` so it installs on the iPad.
- `?selftest=1` (29 assertions) and `?perf=1`.
- Both boot failure paths: Matter.js missing → retry card; fonts slow or
  missing → 2 s timeout, draw anyway.

**Not built, and deliberately so:** turns proper, opponents, CPU, scoring,
HUD, setup screen, pass-the-device, awards, bonus targets, TTS, stone blocks,
the launcher tile. Those are M2–M5. Do not add them piecemeal — each has a
milestone and an exit gate.

## Do not change

1. **`STEP_MS = 16.666 / 3`, one fixed rate, always.** No conditional
   substepping. Matter applies gravity as a force scaled by `deltaTime²`, so a
   step rate that changes mid-flight changes the trajectory, and
   `positionIterations`/`velocityIterations` are per-`Engine.update`, so towers
   would solve stiffer while a shot is airborne than while they settle.
   `crane-stacker/index.html:790,795` passes a variable `dt`. **Never copy that
   here.**

2. **`enableSleeping` stays `false`.** `Sleeping.afterCollisions` skips any
   pair containing a static body, and removing a supporting block generates no
   collision event at all — so the block above is never woken and hangs in
   mid-air. That destroys the one thing this product is for.

3. **All pointer input goes through `view.toWorld()`.** It inverse-transforms
   through the letterbox scale and offset. There is exactly one of these. Raw
   client coordinates look correct on a 4:3 tablet in landscape (the bars are
   zero px there) and are completely broken in portrait. Verified: a 224 px
   letterbox bar in portrait, world coordinates still exact.

4. **The projectile must be removed before a turn can end.** A projectile that
   comes to rest and is never removed stays a dynamic body forever: it blocks
   the settle predicate, it collides on somebody else's turn, and it holds
   `inputLocked` shut. This is a precondition, not tidiness.

5. **The settle thresholds are COARSE: `|v| < 1.2`, `|ω| < 0.08`.** Not
   crane-stacker's `0.2 / 0.02`, which are landing-detection thresholds for a
   different game. With sleeping off, fine thresholds would run almost every
   turn to the 12-second cap because one block jittering anywhere blocks the
   predicate.

6. **`inputLocked` clears on entering `PLAYER_TURN` only when no projectile is
   in flight.** Pausing mid-flight and resuming re-enters `PLAYER_TURN`;
   without that clause the lock clears while the shot is still travelling and
   the player fires twice in one turn.

7. **`frictionAir: 0` on the projectile.** Any non-zero value makes the path
   non-parabolic *and* step-rate-dependent, so the drawn arc stops matching
   the flight.

8. **The slingshot band is drawn, never simulated.** No `MouseConstraint`, no
   elastic `Constraint`. Release velocity comes from `Body.setVelocity` off the
   drag vector, which is what makes an accurate preview possible at all.

9. **The trajectory preview iterates the engine's own integrator**, not a
   closed-form parabola. Matter's `Body.update` is position-Verlet — velocity
   updates and *then* position advances by the new velocity — so the closed
   form is `p₀ + u·n + a·n(n+1)/2`. Measured agreement with a real Matter body
   after 120 steps: **3.7 × 10⁻¹¹ px**.

10. **Module layering.** `CONFIG → view → state → world / players / turns →
    physics → audio → render → ui`, calls downward only. Only `turns` calls
    `setState()`. `render`/`ui` never mutate state. `physics` records into a
    queue and never calls `audio` or `ui` directly.

## Measured performance budget

The plan required this to be measured, not assumed, and required the number to
land in this file.

**Desktop (Apple Silicon Mac, headless Chrome 151, 1024×768 @ dpr 2,
`--disable-gpu`), 40 blocks + 41 dynamic bodies, six max-power shots:**

| | avg | p50 | p95 | max |
|---|---|---|---|---|
| work per frame | 0.73 ms | 0.7 | **0.8 ms** | 2.2 ms |
| — physics (3 fixed steps) | 0.50 ms | 0.5 | 0.6 ms | 2.0 ms |
| — render | 0.23 ms | 0.2 | 0.3 ms | 0.4 ms |
| rAF interval | 16.67 ms | 16.7 | 17.6 | 17.7 |

**= 4.8% of a 16.67 ms frame at p95.** Holding a full-power drag (the arc
recomputes every frame) takes it to **1.0 ms p95, 6.0%**.

`work` is the number that matters. The rAF interval is vsync-locked, so it
only says "60 fps is being held" — it cannot show headroom.

**Tunnelling: 0 events across every max-power shot**, including point-blank
downward fire into the tower, detected by checking whether the projectile
centre ever crossed a block's AABB in one step without a collision. Worst
observed per-step displacement **7.5 px** against a projectile radius of 18 and
a block width of 40.

Note the plan quotes 6 px/step for this. That is only the *launch* figure; a
shot fired downward keeps accelerating. The true bound, computed in
`?selftest=1` from CONFIG, is **10.69 px/step** — still well inside the radius,
but it is the number to check against if `MAX_SPEED` or `STEP_MS` is ever
retuned.

> **TABLET NUMBER STILL OUTSTANDING.** The exit gate asks for this on the
> reference iPad and nothing above was measured there. Open
> `/castle-blasters/?perf=1` on the iPad, fire a few max-power shots at the
> 40-block stress castle, and copy the `work` row and `budget` line off the
> overlay into a second table here. If p95 work exceeds ~8 ms, reduce castle
> rows before reducing player count.

## Two corrections to the approved plan

Both were found by running the game, both are load-bearing, and both are now
locked by an assertion in `?selftest=1`.

**1. `PROJECTILE_MAX_STEPS` was 300; it is 600.**
The plan's own derivation of `ARC_MAX_STEPS = 420` says a near-vertical lob at
`MAX_SPEED` takes about 389 steps. At 300 the ball was deleted in mid-air at
`y = 62`, still 240 px above the castle the preview had drawn it landing on —
and that is the first shot a 4-year-old fires (pull down, shoot straight up).
It also broke the stated Success Criterion that the drawn arc matches the
flight along its whole length.

600 is derived, not picked: `MAX_SPEED` straight up from the highest possible
launch point (top of a 4-row castle on the highest platform M2 may introduce)
then a fall to the bottom cull bound is **469 steps**. 600 gives 28% headroom.
The selftest recomputes that worst case from CONFIG, so changing `MAX_SPEED`,
the block size, the castle height or `PLATFORM_DY_MAX` re-fails it rather than
silently reintroducing the mid-air deletion.

**2. The font race cannot be built on `document.fonts`.**
The plan says to race `document.fonts.ready` against a 2 s timeout. Measured:
with the font domains blocked entirely, that cleared the splash in ~250 ms and
the game drew every block label in a fallback — exactly the failure the plan
was trying to prevent. Both APIs fail in the same direction:

- `fonts.load()` runs before the Google Fonts `<link>` has registered the
  `@font-face` rules, matches no face, and resolves instantly with an empty
  list. `fonts.ready` then resolves too, because nothing is pending.
- `fonts.check()` returns true *vacuously* when no `@font-face` matches,
  because the text is renderable with a system fallback.

So the font is measured instead: render a probe string in the target family
with a generic fallback and in the generic alone, and compare widths. Required
to differ against 2 of 3 generics. Blocked fonts now correctly wait the full
2 s and then draw; a normal load resolves in ~330 ms with both fonts genuinely
present.

## Things this M1 does that the plan left open

- **A fallen character is stood back up at the start of the next turn**
  (on whatever remains of its castle, or the bare platform). The plan makes
  falling cost a heart — that is M2, along with hearts and elimination. M1 just
  keeps the loop playable.
- **`TURN_RESULT_STEPS = 90`** (0.5 s beat before the next turn) is an M1
  addition to CONFIG. M3 replaces it with the scoring display.
- **An in-world pull-back hint** fades in after `HINT_IDLE_MS` (4 s) of not
  touching anything during a turn. Canvas-drawn, not a HUD. It exists because
  the M1 exit gate is a 4-year-old firing a shot inside 30 seconds with nobody
  explaining anything.
- **The single M1 castle sits at the centre** (`castleCentres(1)` → 512), so
  the only thing to shoot at is your own tower. That is intentional for a feel
  test: pull down, fire straight up, watch it land on your own castle.

## Running it

```
python3 -m http.server 8000      # from the repo root
open http://localhost:8000/castle-blasters/
```

- `?selftest=1` — 29 assertions over the pure functions. Prints to the console
  and to a DOM list. Skipped entirely on a normal load. **This is the whole
  unit-test story**: the workspace forbids a build step and npm, so vitest and
  jest are structurally unavailable.
- `?perf=1` — builds a 40-block stress castle and shows the frame-time
  overlay, the per-step projectile displacement and the tunnelling counter.

`?selftest=1` covers 29 of the plan's assertion set. The `cpu`, `players`
(hearts, awards, scoring) and turn-guard-order groups cover code that does not
exist until M2/M3 and are **not stubbed** — a passing stub is worse than a
missing test.

It deliberately does not cover: pointer-to-world mapping under real
letterboxing, service-worker freshness, font readiness on a real network, iOS
audio unlock, tunnelling under real collision, or whether the drawn arc
*visually* matches the flight. Those are integration failures on a real device
and belong to `/qa`.

## Service worker

`CACHE_VERSION = 'castle-blasters-v1.0'`. **Bump it on every deploy, without
exception.**

`STRATEGY = 'network-first'` through M3, flipping to `'cache-first'` at M4 —
one constant. A cache-first SW during rapid iteration means the tablet serves
yesterday's build unless the version is bumped on every single push, and the
milestones whose job is judging *feel* must not be judged against a stale file.

Core assets go through `cache.addAll` (must succeed); the jsdelivr and Google
Fonts URLs go through individual `cache.add(...).catch(() => null)`
(best-effort). A naive SW that puts the CDN URLs in `addAll` fails the whole
install on one jsdelivr blip and the app never becomes offline-capable.

Runtime caching (`cache.put` on every successful GET) is what puts the gstatic
`.ttf` files behind the Google Fonts CSS into the cache after the first online
load. Nothing precaches them and nothing needs to.

Verify a deploy with:

```bash
curl -s https://apps.bryllelagunda.com/castle-blasters/service-worker.js | grep CACHE_VERSION
```

## Icons

`_make_icons.py` is **pure standard library** (zlib + struct) — unlike
`crane-stacker/_make_icons.py`, it does not need Pillow, so it runs anywhere
python3 does. Regenerate with `python3 castle-blasters/_make_icons.py`.

## Not yet done

- **The launcher tile.** Lands at M4, and the same commit must bump
  `CACHE_VERSION` in the **root** `/service-worker.js` — otherwise every
  installed launcher keeps serving the cached tile-less page forever. That root
  SW returns early on any subdirectory request, so the bump cannot touch
  installed Crane Stacker or Printables clients.
- M2 (turns, CPU, stone, stepped platforms), M3 (shell), M4 (delight),
  M5 (poster + docs). Each has an exit gate in the plan. Do not skip them.
- At M2, re-verify `MAX_SPEED` against the chosen platform heights. The
  derivation is only valid while `PLATFORM_DY_MAX ≤ 80`.
