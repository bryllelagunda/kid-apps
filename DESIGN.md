# Design System — Kirby's Games

## Product context
- **What this is:** Personal kid app launcher + growing collection of educational games
- **Who it's for:** One 4-year-old child (primary), parent (secondary — manages settings)
- **Project type:** App launcher + individual PWA games
- **Scale:** 6+ games planned over 12 months

## Aesthetic direction
- **Direction:** Toy Chest — dark stage, bright performers
- **Decoration:** Minimal — icon colours do all the work, no surface decoration needed
- **Mood:** Exciting, inviting, "pick me pick me" energy. Feels like a lit-up toy chest, not a generic app grid.
- **Layout style:** iOS home screen — icon + label only, no outer card or border frame

## Typography
- **Display / titles:** Lilita One — used for launcher heading and game tile labels
- **Body / subtitles:** Fredoka (500 weight) — used for subtitles, HUD labels, UI text inside games
- **Loading:** Google Fonts CDN (`fonts.googleapis.com`), cached by each service worker
- **Scale:**
  - Launcher title: 52px desktop, 38px mobile
  - Subtitle: 17px desktop, 14px mobile
  - Icon label: 13px desktop, 12px mobile
  - Game HUD (Crane Stacker): 20px badges, 15px pills, 12px small

## Colour

### Launcher
- **Background:** `#1a2555` (deep navy, gradient: `160deg #1e2f6e → #1a2555 → #111d4a`)
- **Primary text:** `#ffffff`
- **Subtitle / secondary text:** `rgba(255,255,255,0.45)`
- **Icon label text:** `rgba(255,255,255,0.9)` with `text-shadow: 0 1px 4px rgba(0,0,0,0.6)`

### Game icon colour map (assign in order — permanent per game)
| Slot | Colour | Hex | Game |
|------|--------|-----|------|
| 1 | Hot Pink | `#ff3b6b` | Crane Stacker |
| 2 | Golden Yellow | `#ffd700` | Next game |
| 3 | Teal | `#00c9a7` | Slot 3 |
| 4 | Sky Blue | `#4facfe` | Slot 4 |
| 5 | Vivid Orange | `#f97316` | Slot 5 |
| 6 | Grape | `#a855f7` | Slot 6 |

### Shared game palette (used inside each game)
- **Ink / borders:** `#2a1a0a` (warm dark brown — used for all borders and hard drop shadows)
- **Paper / cream:** `#fff8e7` (warm cream — text on coloured backgrounds inside games)
- **Hot pink:** `#ff3b6b` (primary action, Crane Stacker brand)
- **Cool blue:** `#2eb8ff` (secondary action)
- **Hazard yellow:** `#ffce3a` / `#ffd86b` (in-game accents)
- **Mint:** `#43e6a5`
- **Grape:** `#a86bff`

## Spacing
- **Base unit:** 8px
- **Icon grid gap:** 32px vertical, 20px horizontal (desktop); 24px / 16px (mobile)
- **Icon border-radius:** 22% (CSS — approximates iOS superellipse)
- **Icon shadow:** `0 8px 24px rgba(0,0,0,0.5), 0 2px 6px rgba(0,0,0,0.3)`
- **Max content width:** 800px (launcher)

## Layout
- **Launcher:** Flexbox, `flex-wrap: wrap`, `justify-content: center` — 1 icon centres automatically; grows naturally as games are added
- **Icon size:** `clamp(90px, 22vw, 150px)` — ~90px on small phones, ~150px on tablets
- **Game HUD:** Fixed top, flexbox row with left stack / centre pills / right stack

## Motion
- **Hover:** `transform: scale(1.06)` + shadow deepens — soft, springy
- **Active / press:** `transform: scale(0.93)` + opacity 0.9 — tactile press feel
- **Duration:** 120ms ease
- No scroll-driven animation; no entrance animation — fast and functional for a 4yo

## Things NOT to do
- Don't add an outer card/tile frame around game icons — icon IS the button
- Don't add a "Coming Soon" placeholder tile — empty grid is cleaner than fake content
- Don't change the game colour assignment once set — each game owns its colour permanently
- Don't use a light/warm background on the launcher — the dark stage is what makes icons pop
- Don't change typography stacks (Fredoka + Lilita One) across any app in this family

## Decisions log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-21 | Launcher redesigned — iOS home screen style | Replaced warm gradient + outer-card tile with dark navy + icon-only. Removes "box on box" visual noise. |
| 2026-05-21 | Title changed from "Apps" to "Kirby's Games" | Personalises the launcher — feels like the kid's own world, not a generic app grid. |
| 2026-05-21 | Per-game colour identity established | Each icon gets a permanent bold colour, assigned in slot order. Scales cleanly to 6+ games. |
| 2026-05-21 | Removed Coming Soon placeholder | Empty grid is cleaner; placeholder implies broken/missing content. Add tiles only when apps are real. |
