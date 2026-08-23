# Castle Blasters

Slingshot a cannonball at a castle of letter and number blocks and watch it
come apart.

**Live:** https://apps.bryllelagunda.com/castle-blasters/

## How to play

Touch anywhere on your side, drag back, let go. Pull further for more power. A
dotted line shows where the ball will go while you are still dragging.

A tap with no drag does nothing — it does not waste your shot.

Each player has a castle and a character standing on top of it. Knock the
other characters down. **You lose when your guy falls** — that is the whole
rule. Hearts over each character say how many falls they have left. Last one
standing wins.

Grey blocks are stone and take two hits. Tan blocks are wood and take one.

## Status

**M2 (Turns).** 2 to 4 players, any mix of humans and robots, taking turns on
one tablet. Stepped platforms, stone blocks, hearts, elimination, a win
condition, a pass-the-tablet screen between human turns, and a CPU that mostly
misses — and on about one shot in eight deliberately lobs it straight up onto
its own castle.

The setup screen lands at M3, so until then the line-up comes off the URL:

| URL | Match |
|---|---|
| `/castle-blasters/` | you vs one robot (the default) |
| `/castle-blasters/?slots=hh` | two humans |
| `/castle-blasters/?slots=hccc` | you vs three robots |
| `/castle-blasters/?slots=hhc` | two humans and a robot |

`h` is a human, `c` is a robot. Two to four of them, and at least one human.

Coming: the setup and score screens (M3), spoken bonus targets and confetti
(M4), a printable battle poster (M5).

## Install it on a tablet

Open the link in Safari or Chrome, then Share → Add to Home Screen. It runs
offline after the first load.

## Developer notes

```
python3 -m http.server 8000     # from the repo root
open http://localhost:8000/castle-blasters/
```

- `?selftest=1` — runs 60 assertions and prints pass/fail on screen. Does not
  start the match; reload without it to play.
- `?perf=1` — 40-block stress castle plus a frame-time and tunnelling overlay.
- `?perf=1&slots=hccc` — the same overlay over a real 4-player match.

Everything is in `index.html`: no build step, no npm, no framework. Matter.js
loads from the same jsdelivr URL the other apps in this repo already cache.

Design doc: `docs/designs/castle-blasters.md`.
Context and the do-not-change list: `CLAUDE.md` in this directory.
