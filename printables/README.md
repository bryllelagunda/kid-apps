# Printables

A worksheet maker for preschoolers. Build a practice sheet on screen, add it to today's
pack, print the whole lesson as one PDF.

Live at **https://apps.bryllelagunda.com/printables/**

## Activities

- **Pre-writing strokes** — lines, zigzags, waves, loops. Pencil control before letters.
- **Letter of the day** — traceable upper and lowercase rows, with a green dot showing
  where the pencil starts.
- **Trace words / name** — type any words; they're fitted to the page automatically.
- **Numbers & counting** — 1 to 10, as a row of pictures or a ten-frame.
- **Shapes** — traceable outlines with editable names.
- **Maze** — generated mazes in 8 outline shapes, three difficulties.
- **Cutting practice** — dashed lines for scissor skills.

Each sheet adapts to an **age level** (3–4, 4–5, 5–6) and prints A4 portrait or landscape,
with an optional name/date line and reward stars.

## How to use it

1. Type the child's name at the top.
2. Pick an activity and adjust its options — the preview updates as you type.
3. **Print this** for a single sheet, or **+ Add to pack** to collect several.
4. **Print pack** sends the whole pack to one print job. In the print dialog choose
   *Save as PDF* if you want to keep it.

Two shortcuts: **🎲 Surprise me** adds one random sheet, and **📅 Build a 5-page lesson**
fills a pack with a warm-up → letter → name → numbers → maze progression.

## Notes

- Works fully offline once loaded — install it to your home screen and it keeps working
  on a plane.
- The pack isn't saved. Reloading the page clears it. Print before you close the tab.
- Set your printer to **100% / actual size**, not "fit to page", or the letter sizing
  won't match the age level you picked.

## Developing

No build step. Edit `index.html` directly, then:

```
python3 -m http.server 8000    # from the repo root
```

and open http://localhost:8000/printables/.

Bump `CACHE_VERSION` in `service-worker.js` on every deploy that changes app files.
Icons are regenerated with `_make_icons.py` (needs Pillow).

See `CLAUDE.md` for design decisions and the "do not change" list.
