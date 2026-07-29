# Printables — Claude Code Context

## What this is

A printable-worksheet generator for a preschooler. Unlike `crane-stacker`, this is
**a parent's tool, not a kid's game** — the adult builds sheets on screen, then prints
them and hands the kid paper and a pencil. Nothing here is meant to be played with on
a device.

Live at https://apps.bryllelagunda.com/printables/

## The seven activity modes

| Mode | What it prints |
|------|----------------|
| `strokes` | Pre-writing stroke patterns (lines, zigzags, waves, loops). Muscle control before letters — start here with a 3–4 year old. |
| `letters` | Letter of the day. Traceable upper/lowercase rows with a green start dot showing where the pencil begins. |
| `trace` | Word/name tracing. Autofits arbitrary text to the page width; warns when it has to shrink or wrap. |
| `numbers` | Numerals 1–10 with countable pictures, as a row or a ten-frame. |
| `shapes` | Traceable shape outlines with optional editable captions. |
| `maze` | Seeded, generated mazes clipped to 8 outline shapes (square, circle, star, heart…). |
| `cutting` | Dashed scissor-practice lines. |

Every mode honors the three global settings: **age level** (`y34`/`y45`/`y56` — controls
stroke weight and letter size), **orientation** (A4 portrait/landscape), and the optional
name/date header and "I did it!" reward stars.

## Architecture

- **One file.** `index.html` contains all HTML, CSS and JS. No build step, no modules,
  no dependencies — consistent with the workspace rule.
- **Fully offline, with zero CDN calls.** The Poppins subset used for the traceable
  letterforms is embedded as a base64 `@font-face` data URI. This is deliberate: the
  glyph outlines must render identically for print, and a font that fails to load would
  silently produce wrong worksheets.
- **Rendering is SVG,** generated as strings and injected into `#pages`. Each sheet is
  a `.page` div sized to A4.
- **Printing** is `window.print()` against a `@page` rule rewritten at print time by
  `setPageRule()`. `@media print` hides the sidebar. Print-to-PDF in the browser dialog
  is the intended "save" path.
- **The pack** (`const pack = []`) is an in-memory array of frozen config snapshots.
  It is **not persisted** — a reload loses it. Acceptable: a pack is one sitting's worth
  of sheets, built and printed in a few minutes.

## Key functions

- `cfgCurrent()` — snapshots every control into a plain config object. Everything else
  renders from a config, never from the DOM. Keep it that way: it's what makes the pack,
  `surprise()` and `weekPlan()` work.
- `BUILDERS[mode]` — maps a mode to its `pageX(c)` renderer. Adding a mode means adding a
  builder, a `#m_<mode>` control block, and an `<option>`.
- `buildMaze()` — seeded generator (`mulberry32`) clipped by `inShape()` point-in-polygon
  tests. The seed lives in the config, so a maze in the pack reprints identically.
- `fitBlock()` / `hWord()` — hand-rolled text layout against the embedded font's metrics
  (`HY`). This is why arbitrary names fit the page.

## Do not change

- **Don't swap the embedded font for a CDN link.** It breaks offline use and risks
  wrong glyph shapes on the printed page, which is the whole product.
- **Don't add a print/PDF library** (jsPDF, html2pdf, etc.). The browser print dialog
  already produces correct A4 PDFs, and a library would mean a build step.
- **Don't make the sidebar kid-facing.** No big buttons, no TTS, no sounds. The kid's
  interface is the paper.
- **Don't remove the `tWarn` fit warnings.** Silently shrinking a long name to unreadable
  size produces a bad worksheet the parent only discovers after printing.
- **Don't change the `@page` margin from 0.** The SVG pages already carry their own
  margins (`MX`/`MY`); a printer margin on top would double them and clip content.

## Known gaps (deliberate, not bugs)

- The child's name defaults to a hardcoded value and isn't persisted across reloads.
- The pack is lost on reload.
- A pack that mixes portrait and landscape prints as one orientation with a warning.
