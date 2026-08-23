# Kids' Local Pass-the-Device Artillery Game
## Product Specification + Initial Build Prompt

**Working title:** Castle Blasters Kids  
**Platform:** Local browser game, optimized for tablets  
**Primary mode:** Local pass-the-device multiplayer  
**Players:** 2–8  
**Audience:** Children, with adults/older children also able to enjoy it  
**Core inspiration:** Physics-based turn-based artillery, destructible environments, castle battles, party-game chaos  
**Important:** Build an original game. Do not copy the protected characters, names, art, sounds, maps, UI, weapon designs, or other proprietary elements of existing games.

---

# 1. Product Vision

Build a polished, original, kid-friendly turn-based artillery game that combines:

- simple physics-based aiming and shooting
- destructible castles and terrain
- funny, expressive characters
- short turns
- lots of satisfying visual feedback
- local multiplayer using one shared tablet
- optional educational interaction using numbers, letters, counting, matching, and simple arithmetic

The game should be understandable by a young child almost immediately.

The ideal first-time experience is:

> Pick a character → aim → shoot → BOOM → see what happened → pass the tablet.

The learning elements should make the game more educational **without making it feel like school**.

The child should primarily think:

> "This is a fun battle game."

The parent/teacher should be able to notice:

> "This is also reinforcing numbers, letters, counting, and simple reasoning."

---

# 2. Critical Product Principles

## 2.1 Child-first usability

Assume the player may:

- not read fluently
- read only simple words
- tap the wrong thing
- hold the tablet awkwardly
- accidentally tap twice
- have limited motor precision
- understand pictures faster than text

Every important interaction should therefore be understandable visually.

Use:

- very large buttons
- strong icons
- obvious states
- minimal text
- large touch targets
- simple animations
- clear audio feedback
- friendly characters
- immediate cause-and-effect

Do not create tiny buttons, dense menus, complicated forms, or text-heavy instructions.

---

## 2.2 Learning must be integrated, not bolted on

Numbers and letters should appear naturally throughout the game.

Examples:

- Player numbers: `PLAYER 1`, `PLAYER 2`, etc.
- Turn numbers: `ROUND 2`
- Health values
- Score values
- Damage numbers
- Weapon counts
- Countdown numbers
- Alphabet-labelled targets
- Letter tiles
- Number targets
- Counting objects
- Simple addition/subtraction challenges
- Identify the requested number/letter
- Match letters to objects
- Collect alphabet/number rewards

Avoid interrupting gameplay with frequent educational quizzes.

Prefer short interactions that take only a few seconds and then immediately return to the fun.

---

## 2.3 Never punish a young child for not knowing an answer

Educational tasks should be low-pressure.

If a child answers incorrectly:

- provide a friendly hint
- explain briefly using visuals
- allow another attempt
- avoid harsh sounds
- avoid "WRONG!" screens
- do not make the child feel embarrassed

The game should feel encouraging.

---

## 2.4 One-screen simplicity

The main gameplay screen should have very few controls.

A child should quickly learn:

1. Aim.
2. Choose power.
3. Fire.
4. Watch the result.

Do not expose advanced options unnecessarily.

Advanced options can exist in Settings or a parent/host area.

---

# 3. Core Game Concept

Players control cute original characters positioned around a destructible battlefield containing castles, structures, obstacles, and enemies.

Each player receives a turn.

During the turn, the player aims a projectile and fires.

The projectile follows a visible trajectory affected by physics and environmental conditions.

Impacts can:

- damage characters
- destroy castle structures
- knock objects around
- trigger explosions
- activate special effects
- expose hidden areas
- change the battlefield

After the turn:

1. show the player's result
2. show a short celebration
3. update the score
4. transition to a pass-the-device screen
5. identify the next player visually and numerically
6. require the next player to press a large ready button

---

# 4. Local Multiplayer Model

This is intentionally a **single-device game**.

Do NOT implement:

- accounts
- matchmaking
- online multiplayer
- cloud multiplayer
- login
- internet-based game sessions

The game should function locally.

One person opens the site/app.

Players physically pass the device.

Example:

### 4 players

Player 1 → Player 2 → Player 3 → Player 4 → Player 1

The game should support configurable player counts.

Recommended initial range:

**2–8 players**

Architect the player system so the range can be changed later.

---

# 5. Player Setup

Create a very simple setup flow.

## Step 1: Number of players

Use large visual buttons:

`2  3  4  5  6  7  8`

Do not require typing.

## Step 2: Choose characters

Show large character cards with:

- character image
- name
- simple icon-based description
- color identity

Example:

**BOB**

🛡️ Tough  
💥 Big attack  
🐢 Slow

Use very simple language.

## Step 3: Optional names

Player names are optional.

Provide:

- default `PLAYER 1`, `PLAYER 2`, etc.
- optional simple name entry

Do not force typing.

---

# 6. Character Design

Create original, memorable, child-friendly characters.

Examples of archetypes:

- brave little knight
- energetic archer
- funny wizard
- tiny robot
- strong but slow creature
- fast ninja-like creature
- goofy inventor
- magical animal

These are only archetypes. Create original names and visual identities.

Characters may have different strengths, but avoid complex numerical min-maxing.

Prefer intuitive differences:

- strong
- fast
- accurate
- explosive
- defensive
- tricky

---

# 7. Core Controls

The primary control should be touch-friendly.

A simple aiming model:

- drag to aim
- visual trajectory appears
- adjust launch angle
- adjust power
- release to fire

Optionally provide an obvious power meter.

Controls must also work with mouse input on desktop.

Use large touch targets and forgiving input.

Do not require precision tapping.

---

# 8. Combat Feel

Every action should provide clear feedback.

When something is hit:

- show a hit effect
- show a number such as `25`
- play an appropriate sound
- animate the target
- show damage or destruction

When the player causes major destruction:

- use stronger effects
- use a larger number
- use screen shake sparingly
- show a brief celebration

Never let a major action happen silently.

---

# 9. Physics

Implement satisfying but reliable projectile physics.

Potential mechanics:

- gravity
- wind
- bounce
- collision
- knockback
- explosions
- destructible structures

Physics should feel consistent.

Avoid unpredictable simulation that makes aiming feel random.

When appropriate, show the predicted trajectory before firing.

---

# 10. Castle and Terrain

The battlefield should contain meaningful destructible structures.

Include:

- castle towers
- walls
- platforms
- bridges
- shields
- wood/stone-like structures
- obstacles
- decorative objects

Different materials may respond differently to attacks.

Example:

- wood: easy to destroy
- stone: hard to destroy
- magic blocks: behave differently

The battlefield should visibly change over time.

---

# 11. Weapons

Start with a small but varied set.

Examples:

### Basic Ball
Simple and predictable.

### Bomb
Explodes on impact.

### Bouncer
Bounces before exploding.

### Rocket
Fast and powerful.

### Ice Projectile
Slows/freezes a target.

### Split Shot
Splits into multiple smaller projectiles.

### Mega Blast
Large, satisfying explosion with limited availability.

### Silly Weapon
Something humorous and original that creates chaos without being violent or scary.

Weapons should be mechanically distinct rather than just different damage numbers.

---

# 12. Special Abilities

Characters may have one easy-to-understand special ability.

Examples:

- shield
- extra bounce
- healing
- stronger next attack
- wider explosion
- temporary speed
- trajectory assist

Use simple iconography.

Do not require children to understand complex cooldown systems.

---

# 13. Kid-Friendly Tone

Avoid:

- graphic violence
- blood
- realistic injury
- frightening horror
- cruel language
- humiliating defeat screens

Prefer:

- cartoon impact effects
- comic reactions
- puff clouds
- stars
- sparks
- confetti
- funny sounds
- exaggerated animations

Characters can react with surprise, wobble, tumble, or bounce rather than appearing injured.

---

# 14. Learning Layer

The learning system should be configurable.

Recommended modes:

### OFF
Normal game.

### LIGHT
Occasional educational elements.

### LEARNING
More frequent educational interactions.

### PARENT-SELECTED
Allow adults to choose focus areas.

Potential learning categories:

- numbers 1–20
- counting
- comparing more/less
- simple addition
- simple subtraction
- number recognition
- letters A–Z
- letter recognition
- letter matching
- beginning sounds
- simple word association

The initial implementation should keep this limited and polished rather than attempting an entire educational curriculum.

---

# 15. Examples of Educational Integration

## Number Targets

The environment contains targets:

`3`, `7`, `12`, `15`

The game says or shows:

> Hit 7!

The child aims and shoots the `7` target.

---

## Letter Targets

Targets show:

`A`, `B`, `C`, `D`

The game asks:

> Find B!

The child shoots the correct target.

---

## Counting

A character says:

> How many stars?

The child taps or shoots the correct number.

---

## Simple Math

Example:

> 2 + 3 = ?

Possible answers:

`4   5   6`

The child hits `5`.

Keep the presentation visual and playful.

---

## More / Less

Show:

⭐ ⭐ ⭐ ⭐

versus:

⭐ ⭐

Ask:

> Which has more?

Use a visual answer rather than requiring typed text.

---

# 16. Educational Difficulty

Difficulty should adapt to the player's configured level.

Potential progression:

### Level 1
- numbers 1–5
- letters A–E
- counting small groups

### Level 2
- numbers 1–10
- letters A–J
- simple comparisons

### Level 3
- numbers 1–20
- full alphabet
- simple addition/subtraction

### Level 4
- larger numbers
- more challenging arithmetic
- more complex letter/word relationships

Do not force the educational system into the core combat loop for every player.

---

# 17. Learning Rewards

Reward learning without making it feel like a separate school application.

Examples:

- stars
- stickers
- character accessories
- castle decorations
- new projectile visual effects
- badges
- funny celebration animations

Avoid requiring purchases.

Progress should be locally stored.

---

# 18. Pass-the-Device Experience

This is one of the most important UX systems in the game.

At the end of every turn:

### SCREEN

# 🎉 GREAT JOB!

**PLAYER 2**

Score: **350**

Then:

# PASS THE TABLET

➡️

**PLAYER 3'S TURN**

Display a large visual identifier:

`3`

and optionally the character image.

Then:

## I'M READY!

The next player presses the large button.

Only after that should gameplay resume.

---

# 19. Hide Information Between Turns

When useful, prevent the previous player from accidentally seeing or interacting with information intended for the next player.

Possible approaches:

- transition screen
- "pass the tablet" overlay
- short screen animation
- optional privacy/blanking mode

Do not create unnecessary complexity, but protect turn ownership.

---

# 20. Rounds

A round consists of every active player receiving one turn.

Example:

### ROUND 1

1. Player 1
2. Player 2
3. Player 3
4. Player 4

Then:

### ROUND 2

1. Player 1
2. Player 2
3. Player 3
4. Player 4

Continue until the match ends.

The current round and player should always be visually obvious.

---

# 21. Turn Length

Allow an optional turn timer.

Suggested options:

- 30 seconds
- 45 seconds
- 60 seconds
- 90 seconds
- No timer

The default should be appropriate for children.

When time expires:

- end the turn cleanly
- save results
- show a friendly transition
- pass to the next player

Never create a harsh "YOU LOST" feeling just because the timer ended.

---

# 22. Game Modes

Start with a focused set.

## Battle
Free-for-all.

## Team Battle
Players form teams.

## Castle Siege
Destroy the opposing castle.

## Boss Battle
Players cooperate against a large AI enemy.

## Learning Challenge
More educational targets while retaining the artillery gameplay.

Do not implement every mode simultaneously if that would reduce quality. Prioritize a polished core mode first.

---

# 23. Scoring

Use easy-to-understand numbers.

Possible score sources:

- enemy hits
- structural destruction
- special targets
- combos
- educational objectives
- bonus objectives

Avoid complicated scoring formulas that players cannot understand.

Show why points were awarded.

Example:

`+50 HIT!`

`+100 CASTLE WALL!`

`+25 GREAT SHOT!`

---

# 24. Final Results

After the match:

# 🏆 FINAL RESULTS

Use large character portraits.

Example:

🥇 PLAYER 3 — 1,240  
🥈 PLAYER 1 — 1,100  
🥉 PLAYER 2 — 980  
4️⃣ PLAYER 4 — 750

Use celebration for the winner.

Also provide positive recognition for everyone.

Examples:

- Biggest Boom
- Best Bounce
- Great Aim
- Best Builder Breaker
- Learning Star

The goal is to make losing less discouraging.

---

# 25. Restart / Replay

After the match:

### PLAY AGAIN
Restart using the same players.

### NEW GAME
Return to setup.

### HOME
Return to title.

Make replaying extremely fast.

Families should be able to finish one match and immediately start another.

---

# 26. Parent / Host Controls

Keep these separate from the child-facing interface where practical.

Possible controls:

- learning mode
- learning difficulty
- turn duration
- sound
- music
- vibration/haptics
- player limit
- game difficulty
- fullscreen
- reset local progress

Do not expose technical configuration to children.

---

# 27. Audio

Use audio as part of usability.

Examples:

- menu tap sound
- aiming feedback
- projectile launch
- impact
- destruction
- score reward
- turn transition
- player announcement
- victory
- defeat

For educational interactions, audio can pronounce:

- letters
- numbers
- simple prompts

Do not depend on sound alone. Everything important must also be visually communicated.

---

# 28. Accessibility

Provide:

- large text
- high visual contrast
- color-independent cues
- icons plus labels where useful
- reduced-motion option
- sound toggle
- touch-friendly controls
- readable font choices
- no critical information communicated by color alone

Do not assume every child sees or hears perfectly.

---

# 29. Responsive Design

Primary target:

**Tablet landscape**

Also support:

- tablet portrait where feasible
- desktop browser

Do not let the interface become tiny when the viewport changes.

Prioritize the tablet layout.

---

# 30. Local Storage

Persist appropriate local data:

- settings
- learning preferences
- unlocked cosmetics
- high scores
- achievements
- player preferences

Do not store unnecessary personal information.

No cloud account should be required.

---

# 31. Technical Requirements

Before coding:

1. Inspect the existing project.
2. Identify the framework/build system.
3. Reuse suitable infrastructure.
4. Determine the best local rendering/game approach.
5. Keep the architecture maintainable.
6. Avoid unnecessary dependencies.
7. Bundle critical assets locally so the game can run without internet access.

Organize the game into clear systems such as:

- game state
- player state
- turn manager
- round manager
- combat system
- physics
- destruction
- AI
- education engine
- scoring
- audio
- UI
- persistence

Do not tightly couple all of these systems into one large component.

---

# 32. State Machine

Use an explicit, reliable game-state model.

Example states:

```text
HOME
PLAYER_SETUP
GAME_SETUP
ROUND_INTRO
PLAYER_TURN
PAUSED
TURN_RESULTS
PASS_DEVICE
NEXT_PLAYER_READY
ROUND_COMPLETE
FINAL_RESULTS
```

The state machine must prevent:

- duplicate turns
- skipped players
- accidental extra turns
- stale score updates
- timers continuing after the turn ends
- inputs being accepted in the wrong screen
- multiple "start turn" events
- game state corruption

---

# 33. Input Safety

Child users will press buttons repeatedly.

Handle:

- double taps
- long presses
- rapid taps
- accidental presses
- taps during transitions
- taps while paused
- taps after a turn has ended

Every action should be idempotent where practical.

A single tap should never accidentally start two turns or fire two shots.

---

# 34. Performance

The game should feel responsive.

Prioritize:

- fast startup
- smooth animations
- stable frame rate
- responsive touch
- predictable physics
- efficient rendering
- minimal loading delays

Avoid loading huge assets unnecessarily.

---

# 35. Content Safety

The game is intended for children.

Avoid:

- advertising
- external links
- chat systems
- user-generated public content
- tracking
- unnecessary data collection
- gambling mechanics
- loot-box mechanics
- scary or graphic content

Keep the environment self-contained.

---

# 36. QA Requirements

After implementation, perform a production-level QA pass.

Do not stop after confirming that the game loads.

Play complete games manually through the browser.

Test:

- 2 players
- 3 players
- 4 players
- maximum supported players
- every player receiving exactly one turn per round
- pass-device flow
- timer expiration
- restarting
- pausing
- resuming
- finishing a complete match
- final scoring
- final ranking
- replay
- new game
- learning mode OFF
- learning mode LIGHT
- learning mode LEARNING
- wrong educational answers
- repeated taps
- touch interaction
- mouse interaction
- different screen sizes
- portrait/landscape where supported
- browser refresh during safe states
- local persistence
- sound off
- sound on
- reduced motion
- edge cases around game-over conditions

Look specifically for:

- soft locks
- inaccessible buttons
- incorrect player ownership
- wrong score attribution
- missing turn transitions
- timers that continue running
- stale state
- duplicate actions
- broken collision detection
- broken destruction
- educational prompts that interrupt gameplay badly
- UI text that is too difficult for children
- touch controls that are too small
- visual clutter

Fix discovered issues rather than simply documenting them.

---

# 37. UX Acceptance Tests

A child should be able to answer these without adult explanation:

### Starting
"How do I start?"

### Turn
"Whose turn is it?"

### Aim
"How do I aim?"

### Shoot
"How do I fire?"

### End
"When am I finished?"

### Pass
"Who gets the tablet next?"

### Learning
"What am I supposed to find?"

### Results
"Who won?"

If any of these are unclear, simplify the UI.

---

# 38. Definition of Done

The first production-quality version is complete only when:

- it launches reliably
- the core game is fun and playable
- children can understand the basic controls
- local multiplayer works
- pass-the-device transitions are reliable
- the game supports the selected player count
- turns and rounds are correct
- physics are reliable
- projectiles work
- collisions work
- destruction works
- scoring works
- victory/defeat works
- replay works
- learning elements work
- learning can be disabled
- settings work
- local persistence works
- touch controls work
- responsive tablet UI works
- the game works without requiring an online backend
- the interface feels polished rather than prototype-like
- the complete game has been QA tested

---

# 39. Product Priorities

When trade-offs are necessary, prioritize in this order:

1. **Child usability**
2. **Core gameplay fun**
3. **Reliable turn system**
4. **Responsive touch controls**
5. **Visual feedback and polish**
6. **Destruction/physics quality**
7. **Learning integration**
8. **Replayability**
9. **Extra game modes**
10. **Advanced features**

Do not sacrifice the first five priorities to add more content.

A smaller game that feels fantastic is better than a huge game with mediocre UX.

---

# INITIAL BUILD PROMPT

Use the following as the initial prompt to the coding agent.

---

You are building an original, production-quality, kid-friendly local multiplayer browser game.

The game is a **turn-based physics artillery / castle battle game** for children, inspired by the general design principles of physics-based artillery games and destructible castle games, but it must be completely original.

Do not copy proprietary names, characters, art, sounds, UI, maps, weapons, or other protected game content from existing titles.

## Product goal

Build a game that a young child can understand almost immediately:

**Pick → Aim → Shoot → BOOM → Pass the tablet.**

The game is designed for **one shared tablet/device**.

There is no online multiplayer.

One person opens the game, selects **2–8 players**, and players take turns physically passing the device.

## Most important requirements

### 1. Child-first UX

The users are children.

The UI must therefore prioritize:

- extremely large touch targets
- minimal text
- simple language
- icons and visual explanations
- obvious state changes
- friendly animations
- instant feedback
- forgiving controls
- no complicated forms
- no dense menus

A child who cannot read fluently should still be able to understand most of the game through visuals.

### 2. Core gameplay

Create original characters battling around destructible castles and terrain.

Gameplay should include:

- aiming
- adjustable shot power
- visible projectile trajectory
- gravity
- collisions
- explosions
- destructible structures
- damage
- knockback
- different projectile types
- simple character abilities
- enemies
- scoring
- rounds
- victory conditions

The gameplay should feel responsive and satisfying.

### 3. Pass-the-device multiplayer

This is a critical system.

Every player's turn must follow:

```text
PLAYER TURN
→ TURN RESULTS
→ PASS DEVICE SCREEN
→ NEXT PLAYER IDENTIFICATION
→ NEXT PLAYER PRESSES READY
→ NEXT PLAYER TURN
```

Example:

**🎉 GREAT JOB!**

**PLAYER 2**

**350 POINTS**

Then:

**PASS THE TABLET**

**PLAYER 3'S TURN**

**3**

**I'M READY**

Only after the next player presses the large Ready button should the turn begin.

Players must never accidentally receive an extra turn, skip a turn, or interact during another player's turn.

### 4. Learning integration

Integrate numbers and letters naturally into the game.

Start with:

- number recognition
- counting
- letters
- simple comparisons
- simple addition/subtraction

Examples:

- shoot target `7`
- find letter `B`
- count stars
- choose which group has more
- solve `2 + 3`
- collect alphabet targets

Learning should be optional and configurable.

The player should still feel like they are playing a game, not taking a test.

Wrong answers should produce supportive feedback rather than punishment.

### 5. Original kid-friendly art direction

Use an original visual identity.

Characters should be:

- cute
- funny
- expressive
- memorable
- colorful
- non-graphic

Combat should be cartoon-like.

No blood or realistic injury.

Use:

- explosions
- stars
- sparks
- clouds
- confetti
- wobbling
- bouncing
- humorous reactions

### 6. Tablet-first design

Primary target:

**landscape tablet**

The game must also work reasonably on desktop browsers.

Touch interaction is the priority.

Use large controls and forgiving gestures.

### 7. Game flow

Implement:

```text
HOME
→ PLAYER SETUP
→ GAME SETUP
→ ROUND INTRO
→ PLAYER TURN
→ TURN RESULTS
→ PASS DEVICE
→ NEXT PLAYER
→ ...
→ ROUND COMPLETE
→ NEXT ROUND
→ FINAL RESULTS
→ PLAY AGAIN / NEW GAME
```

Use an explicit game-state architecture so transitions are reliable.

### 8. Quality bar

Do not build a mockup or proof-of-concept.

Build the actual playable game.

Before considering the task finished:

- play multiple complete games
- test multiple player counts
- test all major states
- test touch interaction
- test repeated taps
- test timer expiration
- test scoring
- test round transitions
- test final results
- test learning interactions
- test settings
- test local persistence
- test responsive layout

Fix bugs you discover.

Do not merely report them.

## Implementation approach

First inspect the existing project and determine the existing framework/build system.

Reuse appropriate existing infrastructure.

Then create a clean architecture for:

- game state
- players
- turns
- rounds
- combat
- physics
- destruction
- education
- scoring
- audio
- UI
- persistence

Do not unnecessarily rewrite unrelated project code.

Avoid unnecessary online services.

The game should run locally and should not require accounts, external APIs, matchmaking, or cloud infrastructure.

## Important product judgment

Use your own judgment to fill in unspecified details.

Do not stop and ask for clarification for every design decision.

Choose the simplest implementation that produces a polished, fun, child-friendly result.

Prioritize quality over feature count.

Make the core loop excellent before adding secondary features.

## Deliverable

Produce a working, polished browser game, not a design document.

After implementation, perform a comprehensive QA pass on the actual running game and fix the issues discovered.

Use the product specification above as the source of truth.
