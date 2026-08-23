# Castle Blasters

Slingshot a cannonball at a castle of letter and number blocks and watch it
come apart.

**Live:** https://apps.bryllelagunda.com/castle-blasters/

## How to play

Touch anywhere, drag back, let go. Pull further for more power. A dotted line
shows where the ball will go while you are still dragging.

A tap with no drag does nothing — it does not waste your shot.

## Status

**M1 (Feel).** One castle, one character, one player, shooting on a loop. The
turn machinery underneath is the real thing and already runs the
`PLAYER_TURN ⇄ TURN_RESULT` cycle; it just has one slot in it so far.

Coming: opponents and a CPU that mostly misses (M2), the score and setup
screens (M3), spoken bonus targets and confetti (M4), a printable battle
poster (M5).

## Install it on a tablet

Open the link in Safari or Chrome, then Share → Add to Home Screen. It runs
offline after the first load.

## Developer notes

```
python3 -m http.server 8000     # from the repo root
open http://localhost:8000/castle-blasters/
```

- `?selftest=1` — runs 29 assertions and prints pass/fail on screen.
- `?perf=1` — 40-block stress castle plus a frame-time and tunnelling overlay.

Everything is in `index.html`: no build step, no npm, no framework. Matter.js
loads from the same jsdelivr URL the other apps in this repo already cache.

Design doc: `docs/designs/castle-blasters.md`.
Context and the do-not-change list: `CLAUDE.md` in this directory.
