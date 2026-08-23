# Castle Blasters — Claude Code Context

## What this is

An offline, turn-based physics artillery game. Slingshot a cannonball at a
castle of letter and number blocks and watch it come apart. Lives at
`apps.bryllelagunda.com/castle-blasters/`.

**Source of truth is `docs/designs/castle-blasters.md`** (approved,
eng-reviewed). This file records what is actually built, the measured numbers,
and the things not to change. Where this file and the plan disagree about a
number, the disagreement is written down explicitly below with the reason.

## Status: M2 (Turns) complete

### M2 — Turns

The match. Built:

- Slot population from `?slots=` (2-4 slots, at least one HUMAN) with a
  `kind: 'human' | 'cpu'` flag per slot. The setup screen is M3; this is the
  same rule it will enforce.
- Turn manager and round manager: a fixed round order, exactly one turn per
  living player per round, eliminated players skipped without reordering.
- The full `TURN_RESULT` guard table, in the plan's order, with rule 1
  (no living human, or one player left) ahead of round rollover.
- CPU solver: ballistic solve refined against the engine's own integrator,
  weakest-castle targeting, error injection, the 12% silly shot, a think
  pause and a visible aim animation using the same dotted arc a human sees.
- Pass-the-device screen, shown only when the tablet can actually change hands.
- Hearts, the fall check, elimination, and the win condition.
- Stone blocks (bottom row, 2 hits) and stepped alternating platforms.
- `PAUSED` with a ⏸ button, and PLAY AGAIN off the results screen.
- Eliminated characters leave with a puff **and a wobble**, never an injury
  animation — drawn from the recorded silhouette, because the body is already
  out of the world by then.
- `prefers-reduced-motion` suppresses screen shake (see below).
- `?selftest=1` grew from 29 to **61 assertions**: the `cpu`, `players`,
  `render` and turn-guard-order groups M1 deliberately left unstubbed.

Still not built, and deliberately so: the setup screen, the DOM HUD, scoring
display, round intro screen, final rankings, awards, the parent settings
panel, `localStorage`, bonus targets, TTS, confetti, the launcher tile, the
poster. Those are M3-M5. Do not add them piecemeal.

### M1 — Feel

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

## How to start a match before the setup screen exists

`?slots=` takes one letter per slot: `h` human, `c` CPU. Two to four of them,
at least one `h`. Anything else is refused and the default (`hc`) is used.

| URL | Match |
|---|---|
| `/castle-blasters/` | 1 human + 1 CPU |
| `/castle-blasters/?slots=hh` | 2 humans |
| `/castle-blasters/?slots=hhc` | 2 humans + 1 CPU |
| `/castle-blasters/?slots=hccc` | the 4-player P5 falsification run |

`parseSlots()` is pure and asserted in `?selftest=1`, so when M3 builds the
setup screen it wires the UI to this function rather than re-deriving the rule.

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
    physics → cpu → audio → render → ui`, calls downward only. Only `turns`
    calls `setState()`, and only `turns` mutates a player slot. `render`/`ui`
    never mutate state. `physics` records into a queue and never calls `audio`
    or `ui` directly, and never reads `players` — `physics.build()` takes the
    character ids as an argument rather than reaching up for them.

11. **`turns.frame()` routes every turn-end decision through `turnRules`.**
    Do not reimplement those predicates inline. An earlier draft did, and the
    six turn-lifecycle assertions in `?selftest=1` were then exercising a
    parallel copy the game never ran — so breaking precondition 1 in the
    shipped path would have left the harness green. `turnRules` is the
    definition; `turns.frame` is the only caller; the selftest asserts the
    definition. `turns.endTurn()` is the single exit from `PLAYER_TURN`.

12. **`playerRules` is the same discipline for the health model.** `fell()`,
    `heartsLostThisTurn()` and `heartsFor()` are the definition; `turns`
    calls them; the selftest asserts them. Do not inline a second copy of
    "did he fall".

13. **`turns.fire()` is the ONLY place a projectile is spawned**, and
    `shotFired` is what makes a turn exactly one shot. `fire()` deliberately
    does *not* check `inputLocked` — a CPU turn is input-locked for its whole
    duration by design and still has to shoot. The pointer path
    (`turns.fireShot()`) keeps that guard, so there is still exactly one route
    from a finger to a projectile and it is still closed while the lock is
    set. If you ever add a second spawn site, the mash guarantee is gone.

14. **`inputLocked` on entering `PLAYER_TURN` is now TWO clauses**: no
    projectile in flight (M1, rule 6) **and** the active player is human. The
    second is not optional — without it a human can fire the bot's shot, and
    P3 says the turn manager treats both kinds identically.

15. **The round order is snapshotted at `startMatch()` and never rebuilt.**
    Eliminating a player mid-round must skip them, not reshuffle who is still
    owed a turn. Rebuilding the order from the living players each turn is the
    obvious-looking change that silently gives someone two turns in a round.

16. **The CPU's obstruction check ignores the target's own castle.** The bot
    aims at the LOWEST standing block, and any arc that reaches it has to pass
    through the blocks stacked on top of it. Counting those as obstructions
    makes every good shot look blocked and drops the bot onto its 45°
    last-resort fallback on every single turn — which it did, until measured.

17. **Physics keeps stepping during `PASS_DEVICE`, `TURN_RESULT` and
    `ROUND_INTRO`. Only `PAUSED` freezes it.** That is why every deadline in
    the file is counted in simulated steps: a `performance.now()` deadline
    would expire behind the pause overlay, and the state table has no
    `PAUSED → TURN_RESULT` edge for it to fire into. It is also why
    `turns.ready()` re-checks that the pending player is still alive.

## Measured performance budget

The plan required this to be measured, not assumed, and required the number to
land in this file.

**Desktop (Apple Silicon Mac, headless Chrome 151, 1024×768 @ dpr 2,
`--disable-gpu`), 40 blocks + 41 dynamic bodies, six max-power shots:**

| | avg | p50 | p95 | max |
|---|---|---|---|---|
| work per frame | 0.73–0.74 ms | 0.7 | **0.8–0.9 ms** | 1.0–2.2 ms |
| — physics (3 fixed steps) | 0.50–0.52 ms | 0.5 | 0.6 ms | 0.8–2.0 ms |
| — render | 0.23 ms | 0.2 | 0.3 ms | 0.4 ms |
| rAF interval | 16.67 ms | 16.7 | 17.6 | 17.7 |

**= 4.8–5.4% of a 16.67 ms frame at p95**, across repeated runs. Holding a
full-power drag (the arc recomputes every frame) takes it to **1.0 ms p95,
6.0%**.

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

**M2, same machine, a real 4-player match** (`?perf=1&slots=hccc`) — 36 blocks
+ 4 characters + 1 projectile, 40 dynamic bodies at full board:

| | avg | p50 | p95 | max |
|---|---|---|---|---|
| work, firing at max power | 0.73 ms | 0.7 | **1.1 ms** | 1.3 ms |
| work, holding a full-power drag (406-point arc) | 0.91 ms | 0.8 | **1.5 ms** | 2.2 ms |

**= 6.6% of a frame while shooting, 9.0% while dragging.** The drag figure is
the one that grew: at 4 players the preview arc crosses four castles instead
of one. Still an order of magnitude inside budget. **Tunnelling: 0 events.**

> **TABLET NUMBER STILL OUTSTANDING.** The exit gate asks for this on the
> reference iPad and nothing above was measured there. Open
> `/castle-blasters/?perf=1&slots=hccc` on the iPad, play a couple of rounds
> including one held full-power drag, and copy the `work` row and `budget`
> line off the overlay into a third table here. If p95 work exceeds ~8 ms,
> reduce castle rows before reducing player count.

## Corrections to the approved plan

Every one was found by running the game, every one is load-bearing, and every
one is now locked by an assertion in `?selftest=1`. **Do not revert them.**

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

**3. M2 — The fall check cannot be measured against the platform top.**
The plan says a character fell if its centre ends up "more than 120 px below
its own **platform's** top surface". That can never fire. The character stands
on *top of its castle*, so on a 3-row castle its home is already 142 px
**above** the platform top; to get 120 px below it, it would have to be
underground. The rule was added in the plan's own Round-3 review to catch
exactly one case — *"knocking an enemy character off its collapsing castle
onto the ground at y ≈ 700 costs nothing at all"* — and as written it does not
catch it.

So the reference is where the character was **standing when the turn began**,
not the platform under its castle. `FALL_DY = 80`, bracketed by the castles
the game actually builds and asserted at both ends:

- must fire: a full topple off the **shortest** castle (3 rows) = 120 px
- must not fire: losing one row of cover = 40 px

so `FALL_DY` has to sit strictly inside (40, 120). 80 is two block rows.
Changing `STONE_ROWS`, the block size or `rowsFor()` re-fails the assertion.

Being knocked over *in place* is not a fall — the character is stood back up
for free. Only height and leaving its own footprint cost a heart, and a hit
plus a fall in one turn is still one heart.

**4. M2 — `PASS_DEVICE` needs "more than one human alive", not just
"the next player is human".**
The plan's guard table says PASS_DEVICE whenever the next living player is
HUMAN, and P3 says in the same breath that *"a solo game never shows one"*.
Both cannot be true: with one human and three bots the table puts a **PASS THE
TABLET TO PLAYER 1** screen in front of the only person in the room, once per
round, forever. The screen exists for the tablet changing hands, so the test is
whether it can — which also correctly suppresses it when a 2-human match loses
one of them and the survivor should just keep playing. `turnRules.needsPass()`.

**5. M2 — The silly shot's elevation band was 75–88°; it is 82–88° at 6–9.**
75° does not survive contact with the geometry. The launch point sits ~200 px
*above* the platform (the character stands on top of the castle), and the extra
fall buys enough hang time to carry a 75° shot **229 px sideways** — past its
own castle, out of its own slice, and at 4 players into the neighbour's. A
silly shot that can land on an opponent is not a silly shot, it is a lucky one.
Re-derived so the worst case in the band stays inside its own platform: 82–88°
at 6–9 gives 14–105 px, against a platform half-width of 90 and a 4-player
half-slice of 128. The selftest recomputes both bounds from CONFIG.

## Things M2 decided that the plan left open

- **Stepped platform heights (Open Question 1).** `PLATFORM_DY = 60`,
  alternating — castle `i` sits `(i % 2) × 60` px above the base ground. 60 and
  not the bounding 80, because the whole point of leaving headroom is not
  spending all of it. **`MAX_SPEED = 18` stands, re-derived:** the longest shot
  the game can require is 768 px (4 players, outermost to outermost) with a
  60 px climb, needing `v = 15.19` — **18.5% headroom**, against 17% at the
  plan's bounding 80. `?selftest=1` recomputes this from CONFIG for n = 2, 3
  and 4, so raising `PLATFORM_DY` or adding a fifth slot re-fails rather than
  silently invalidating `MAX_SPEED`.
- **Where stone goes.** The plan ships both materials and never says. Bottom
  row is stone, everything above is wood: a stone foundation is a reading a
  4-year-old can state out loud, it is identical for every castle so nothing is
  unfair, and it lands exactly where the CPU aims (the lowest standing block)
  so the bot's best shot goes clang-then-smash instead of smash. **Materials
  differ in hit points ONLY** — same density, same friction. Ice was cut for
  having a physics property; stone must not quietly acquire one, and there is
  an assertion that says so.
- **Hearts are drawn in-world above each character**, as countable pips. That
  is not the DOM HUD — M3's HUD shows only the *active* player's hearts, and a
  3- or 4-player board is unreadable without every character wearing its own.
  Same reasoning for the bobbing chevron over the active character.
- **Scoring is tracked but never displayed.** The numbers exist because the
  win condition needs them: last player standing, **points only as the
  tiebreak**, which is what `ROUND_MAX` resolves on. The floating `+25 SMASH!`
  labels, the HUD and the awards are M3/M4. `stats.bestShotDamage` is the
  points earned in one shot; `stats.selfHits` counts *shots* that damaged your
  own stuff, not collisions.
- **`ROUND_INTRO` is a 0.6 s canvas banner, `PAUSED` offers only RESUME, and
  `FINAL_RESULTS` names the winner and offers PLAY AGAIN.** All three states
  are in the plan's table and all three are load-bearing for M2 (the
  ROUND_INTRO human/CPU branch prevents the round-rollover pass-device bug;
  PAUSED is what the mash exit gate is tested against). Their *screens* are
  M3: rankings, scores, awards, SETTINGS, HOME and NEW GAME are not here.
- **`prefers-reduced-motion` suppresses screen shake, at M2 rather than M3.**
  The plan puts `reduceMotion` in M3's parent settings panel, and the persisted
  parent override still lands there. But the plan's own *default* for it is the
  OS media query, and that half needs no UI at all — so it ships now. Screen
  shake is a genuine vestibular trigger and there was otherwise no way to turn
  it off. It suppresses **shake only**: trajectory dots, block motion and the
  elimination wobble all carry game information and are untouched, which is
  what the plan says and what `?selftest=1` asserts.
- **The elimination wobble is drawn, not simulated.** `turns` removes the
  character body the instant a slot dies, so the settle predicate and the turn
  guards never see a corpse; `render.puff()` records the silhouette and facing
  and animates a copy. The exit is therefore cosmetic by construction and
  cannot reach the match. `render.drawSilhouette()` is shared with the live
  character so an eliminated player cannot leave as a different creature.
- **CPU tie-breaking is random on an exact tie.** The plan says "fewest
  standing blocks, ties to nearest" and stops there. At 4 players the two
  neighbours of a middle castle are exactly equidistant, so index order sent
  every bot at castle 0 on the opening round — and castle 0 is the human in
  every `?slots=hc..` line-up. That is an implementation accident, not the
  plan's rule.

## Things M1 did that the plan left open

- ~~A fallen character is stood back up at the start of the next turn with no
  cost.~~ **Replaced at M2**: the fall check runs at turn *end*, costs a heart,
  and re-stands the character on whatever remains of its castle.
- **`TURN_RESULT_STEPS = 90`** (0.5 s beat before the next turn) is an M1
  addition to CONFIG. M3 replaces it with the scoring display.
- **An in-world pull-back hint** fades in after `HINT_IDLE_MS` (4 s) of not
  touching anything during a turn. Canvas-drawn, not a HUD. It exists because
  the M1 exit gate is a 4-year-old firing a shot inside 30 seconds with nobody
  explaining anything.
- ~~The single M1 castle sits at the centre.~~ **Replaced at M2** by real
  slots. `castleCentres(1)` → 512 survives only as the `?perf=1` stress rig.

## Running it

```
python3 -m http.server 8000      # from the repo root
open http://localhost:8000/castle-blasters/
```

- `?selftest=1` — **61 assertions** over the pure functions and the rules
  modules. Prints to the console and to a DOM list. **Does not start the match
  or the rAF loop**: the `cpu`, `world` and `players` groups build worlds of
  their own (4 players, a flattened castle, an unreachable target) and a live
  loop mutating the same singletons underneath them makes the harness a coin
  flip. Reload without the flag to play. **This is the whole unit-test story**:
  the workspace forbids a build step and npm, so vitest and jest are
  structurally unavailable.
- `?perf=1` — builds a 40-block stress castle (one slot, cycling forever, no
  hearts, no elimination) and shows the frame-time overlay, the per-step
  projectile displacement and the tunnelling counter.
- `?perf=1&slots=hccc` — the same overlay over a **real** 4-player match. This
  is the one the M2 budget is measured against.

M1 shipped 29 assertions and left `cpu`, `players` and turn-guard-order
unstubbed because the code did not exist. M2 added 32 more and closed those
groups — with one exception, stated so it is not mistaken for coverage:
**awards are still not stubbed.** CHAMPION / BIGGEST BOOM / SILLY SHOT /
GOOD GAME are M3, and a passing stub is worse than a missing test. What M2
does assert from that group is the thing awards will be built on: the winner
is the last player standing, not the top scorer.

It deliberately does not cover: pointer-to-world mapping under real
letterboxing, service-worker freshness, font readiness on a real network, iOS
audio unlock, tunnelling under real collision, or whether the drawn arc
*visually* matches the flight. Those are integration failures on a real device
and belong to `/qa`.

## Service worker

`CACHE_VERSION = 'castle-blasters-v1.1'`. **Bump it on every deploy, without
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
- M3 (setup screen, HUD, scoring display, round intro, final rankings and
  awards, parent settings, `localStorage`), M4 (bonus targets, TTS, confetti,
  awards, launcher tile, SW → cache-first), M5 (poster + docs). Each has an
  exit gate in the plan. Do not skip them.

- **M3 MUST make the `ROUND_MAX` ending legible.** Found and reproduced at M2:
  when a match reaches `ROUND_MAX` with more than one player still standing,
  the win resolves on points — and at M2 the score is never displayed, so
  `FINAL_RESULTS` reads

      WINNER
      (2)  PLAYER 2

  with both players alive on full hearts and nothing on screen explaining why.
  To a 4-year-old the game simply stopped and picked someone. This is not a
  bug in the win condition — points-as-tiebreak is the plan, and it resolved
  correctly — it is a gap in the *screen*, and the screen is M3's. When M3
  builds final results with rankings, the points ending needs to say it is a
  points ending and show the numbers it was decided on. Lowering the frequency
  (see the `HEARTS` note below) reduces how often anyone meets it; it does not
  close it.
- ~~At M2, re-verify `MAX_SPEED` against the chosen platform heights.~~ Done —
  `PLATFORM_DY = 60`, `MAX_SPEED = 18` holds with 18.5% headroom, recomputed
  from CONFIG in `?selftest=1`.

## The M2 exit gate

| | Status |
|---|---|
| 1 human + 1 CPU completes a match | **PASS** — scripted end-to-end, FINAL_RESULTS reached, 0 forced turn ends |
| 2 humans complete a match | **PASS** — pass screen before every human turn |
| every player gets exactly one turn per round | **PASS** — turn log checked per round across 2, 3 and 4 player matches; eliminated players skipped, never reordered |
| mashing never fires twice, incl. across a pause mid-flight | **PASS** — 24 checks: pause froze the projectile and the step counter, resume left `inputLocked` set, 16 further shots under constant mashing produced no double fire |
| **P5 falsification at 4 players on the reference iPad** | **NOT RUN — needs the physical device** |

Everything above was verified headlessly (Chrome 151 over CDP, real pointer
events through the letterbox transform, not unit tests). The last row cannot
be: it is a judgement about whether castles stay readable and turns stay under
~10 s in a child's hands, on a screen this machine does not have.

**Getting the build onto the iPad without a deploy.** M2 lives on a branch and
the plan is explicit that Vercel preview URLs are the wrong answer here —
every push mints a new origin, so the kid's installed app has to be deleted
and reinstalled each iteration and loses its settings. Serve it over the LAN
instead:

```bash
python3 -m http.server 8000          # from the repo root
ipconfig getifaddr en0               # this Mac's LAN address
```

then open `http://<that-address>:8000/castle-blasters/?slots=hccc` on the iPad
in **landscape**, on the same wifi. No deploy, no new origin, no reinstall.
(The service worker will not register over plain http on a non-localhost
origin, which is fine — this is a play test, not an offline test.)

Alternatively, merge to `main` and use the real path, which is what the plan
says M1–M4 should do once a milestone is being kept.

1. Are the four castles readable — can you tell the letters and numbers apart
   on the far castle from normal holding distance?

   *Partly answered already, so you only have to judge the rest.* The type
   size is not the risk: at 4 players the world scale is 1.0 on the reference
   iPad, so a block is **7.7 mm** and its label has a **3.3 mm cap height** —
   about twice newspaper body text (~1.6 mm) and comfortably over the ~2.5 mm
   usually quoted for comfortable reading at arm's length. On a 10.9" or 11"
   iPad it is larger still (scale 1.07–1.09). What is left to judge is
   **composition, not legibility**: do four castles across one screen read as
   four separate places, or as a row of clutter?
2. Can you tell at a glance whose turn it is, and which characters are robots?
3. Does a turn take under ~10 seconds, including the bot's think-and-aim beat?
4. Does the match finish before round 8? (`CastleBlasters.turns.round`, or
   just count the ROUND banners.)

If castles are not readable at 4, **the fix is to make 2 players the default
with a 4-row castle — not to shrink the castles further.** If matches run past
round 8, the dial is the `HEARTS` table, not `ROUND_MAX`.

### Match length, measured (Open Question 3)

Three matches per line-up driven by a **perfect shooter** — the ballistic
solution with no error at all, fired straight through `turns.fire()`. This is
the **floor**: a 4-year-old is worse than this, not better.

| slots | rounds | shots | wall s | turn p50 | turn p95 | forced ends |
|---|---|---|---|---|---|---|
| `hc` | 3 / 6 / 9 | 6 / 12 / 18 | 27 / 52 / 73 | 4.1–4.5 s | 5.1–5.9 s | 0 |
| `hh` | 5 / 7 / 5 | 10 / 13 / 10 | 38–50 | 3.5–4.1 s | 5.0–6.4 s | 0 |
| `hhh` | 9 / 6 / 5 | 14 / 15 / 23 | 48–83 | 3.1–4.0 s | 4.5–5.0 s | 0 |
| `hccc` | 6 / 4 / 4 | 14 / 14 / 20 | 52–75 | 3.6–4.0 s | 5.0–5.5 s | 0 |

Two readings, and the second is the one to carry to the iPad:

- **Turn length is fine.** ~4 s median, ~5–6 s at p95, against the P5 test's
  "~10 seconds" bar — and that is the *machine* half of a turn (the CPU's
  700 ms think plus 600 ms aim, the settle, the 0.5 s result beat). A human's
  aiming time is added on top of it, not hidden inside it.
- **Match length is bimodal on accuracy, and 2 players is the long tail.**
  A perfect shooter finishes `hc` in 3–9 rounds. A deliberately *inaccurate*
  scripted shooter (±4°) ran the same line-up to 9 and 12 rounds, and 12 is
  `ROUND_MAX` — the match then resolved on points, correctly and without a
  soft lock, but it went the distance. 3 hearts at 2 players is the reason;
  3 and 4 players already drop to 2 and land at 4–6 rounds.

**So the thing to watch on the iPad is a 2-player match, not a 4-player one.**
If a real match with the kid routinely reaches round 10+, drop `HEARTS[2]`
from 3 to 2 — one number, and it touches nothing else. Do not reach for
`ROUND_MAX`: shortening the safety net does not make the game shorter, it just
makes more matches end on the safety net.

Also still outstanding from M1: the **tablet performance number**. Same
device, same session — see the Measured performance budget section.
