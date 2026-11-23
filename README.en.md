# drawing-excalidraw-figures

[Tiếng Việt](README.md) · **English**

<p align="center"><img src="docs/images/examples/11-sequence-en-light.png" alt="Sequence figure drawn by the skill" width="620"></p>

Turn a technical passage, or a rough idea that exists only as words, into a hand-drawn Excalidraw figure - not a row of boxes joined by arrows, but a figure where time becomes length, data becomes cells with real values, and a limit becomes a line.
A skill for Claude Code, Codex CLI, or any agent that can read SKILL.md: you hand over the text, the agent writes a short JSON spec, runs one command, and gets four files.

```
fig.excalidraw   the source scene - drop it on excalidraw.com to keep editing
fig.svg          static SVG, colors as var(--token), correct in light and dark mode
fig-light.png    preview in the 666px reading column, light theme
fig-dark.png     preview, dark theme
```

**Why it is worth using:**

- **Keeps editing** - `.excalidraw` opens on excalidraw.com, drag and tweak like any hand-drawn scene
- **Two correct themes** - SVG colored by tokens, never wrong in dark mode
- **Fully offline** - engine, Chromium bundle and fonts live in the repo; no API, no network
- **A gatekeeping tool** - blocks overflowing text, arrows through boxes and off-token colors at render time; the rest is your eye's call

See what the skill draws when four AI models race on the same brief: [32 figures, eight cases](https://drawing-excalidraw-figures.vercel.app/#so-sanh).

## Not only for engineering

A business pitch, a concept that needs teaching, a tangled 2 a.m. note, an internal process: every idea has its own shape.
For a rough idea, the skill first writes one sentence - "this idea really says that..." - lists the concepts, relations and tensions in the writer's own words, then picks the figure type from the idea's structure: causal loop, 2x2 matrix, funnel, concept map, timeline, swimlane.
When there is someone to ask, the skill shows the first draft and asks "is this what you meant?" before polishing.

<p align="center"><img src="docs/images/y-tuong/ghi-chu-light.png" alt="A quitting-decision note drawn as a timeline" width="620"></p>

Four non-technical cases live in `evals/`, with results and lessons in `references/lessons-from-runs.md`.
The `nguoi-moi-mat-khau-salt` case measures whether a newcomer understands the figure: the judge looks at the PNG as a parent who never programmed and answers three questions from the image alone.
Run it as a controlled comparison (with and without the skill, reported as `Δ`) as described in `evals/README.md`.

## The rules that carry weight

**Draw the SHAPE of an idea, not the list of its parts.**
A row of rectangles joined by arrows only says "A calls B" - something one sentence already said.
A good figure makes time into length, data into cells with real values, a limit into a line, an incident into a red stroke.

The skill was distilled from about 600 real Excalidraw figures from Hello Interview plus the owner's own corpus:
nothing guessed, every rule has its source recorded in `references/sources.md`.

## The six-step workflow

1. Ask who the reader is and what they already know (newcomer, developer, specialist), list the terms the figure must explain, and pick compact or newcomer-explainer mode. Then write exactly one sentence: "Looking at this figure, the reader SEES ... which the passage does not show." If you cannot write that sentence, do not draw.
2. List the facts: actors, steps, failure branches, real numbers taken verbatim from the source. For a rough idea: concepts, relations, tensions, and what the writer wants the reader to believe.
3. Pick the figure type by what must be seen (sequence, swimlane, state, ER, byte cells, timeline, threshold...).
4. Write the JSON spec - copy a template from `examples/`, never start from scratch.
5. Render with `ve.py`.
6. Open both PNGs and look until the figure can say the sentence from step 1 to that reader. A green tool does not yet mean a readable figure.

A figure can be right in every fact and still useless if it assumes the reader knows Base64, the heap or JIT: that is why step 1 asks about the reader first.
For newcomers the skill goes from an everyday example to the mechanism, puts a plain sentence beside each part, and has a ready "explained flow" type (`30-explained-flow`): a number, one line and a small example per step.
For security topics it draws the mechanism and the defence, and stops before anything that works as attack instructions (details in `SKILL.md`).

## Install

Requirements: Python 3.11+, Playwright Chromium, and the fonts already in `assets/fonts/` (nothing is fetched from the network while rendering).

```bash
git clone https://github.com/nv-minh/drawing-excalidraw-figures.git
cd drawing-excalidraw-figures
python3 -m pip install -r requirements.txt && python3 -m playwright install chromium

# check the environment: Python, Playwright, Chromium; prints the install command for anything missing
python3 scripts/ve.py --check

# try a bundled example right away and open what it rendered
python3 scripts/ve.py examples/03-byte-cells.json --out /tmp/fig --open
```

A missing Playwright makes `ve.py` print the one command that installs it, not a traceback.
Without Playwright's Chromium, `ve.py` uses the Chrome or Edge already installed (identical SVG); it asks you to install Chromium only when there is no browser at all.
There is no browser-free mode: the shapes, the text measuring and the SVG all come from the real Excalidraw library running in a browser.

For Claude Code to use it as a skill, put the whole folder into your skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R drawing-excalidraw-figures ~/.claude/skills/
```

Codex CLI reads the same `SKILL.md` standard - only the install folder differs.
One clone serves both through a symlink:

```bash
mkdir -p ~/.codex/skills
ln -s ~/.claude/skills/drawing-excalidraw-figures ~/.codex/skills/drawing-excalidraw-figures
```

## Other agents: Antigravity, Cursor, Gemini CLI, Copilot

At its core the skill is a Markdown brief plus a Python CLI, so any agent that can read files and run commands can use it - Antigravity, Cursor, Windsurf, Gemini CLI, the GitHub Copilot coding agent.
For tools without a skills folder, add a few lines to their rules file (`AGENTS.md`, `.cursor/rules`, `.windsurfrules`, `.github/copilot-instructions.md`):

```text
When asked to draw a diagram, read <path-to-the-repo>/SKILL.md
and follow its six-step workflow exactly.
```

Step 6 (looking at both PNGs) needs a multimodal agent; every major model qualifies.
A text-only model can still draw - you just open the PNGs yourself.

`ve.py` walks up from its own location to find `engine/`, so it works placed under `~/.claude/skills/` or inside a larger project's `.claude/skills/`.

## The spec in 30 seconds

```json
{
  "_": "The reader SEES that a pool of 10 connections cannot serve 14 requests: 4 requests time out at second 2, before the first connection comes back at second 3.",
  "elements": [
    {"t":"axis","x":60,"y":352,"length":510,"gap":170,"ticks":["0s","1s","2s","3s"],"label":"t"},
    {"t":"span","x1":60,"x2":570,"y":28,"text":"10 requests hold a connection 3s per query · pool = 10","color":"muted"},
    {"t":"cells","id":"q","x":60,"y":46,"cw":510,"ch":13,"labels":["","","","","","","","","",""],"fill":"warn","fillStyle":"hachure"}
  ]
}
```

Run `python3 scripts/ve.py spec.json` and the four files appear.
Full syntax of every element: `references/spec.md`.

A few utilities come with it:

```bash
python3 scripts/ve.py spec.json --open                       # render, then open both PNGs
python3 scripts/ve.py a.json b.json --page post.html \
    --title "Base64 for newcomers" --caption "Two figures, read in order"   # several figures on one page; .pdf works too
python3 scripts/ve.py spec.json --extract-labels en          # pull every label into spec.en.labels.json to translate
python3 scripts/ve.py spec.json --lang en                    # render the English version, spec untouched
```

A spec's `"caption"` (the step 1 sentence) is printed under its figure on the `--page` page and is translated with the labels.

## Thirty figure types with ready templates

`examples/` holds 30 templates: request flow, anatomy, byte cells, timeline, threshold, before/after, two views, physical metaphor, failure branch, decision tree, sequence (including alt/opt/loop), state machine, ER table, hash ring, code evidence, layer lanes, progressive series, layer stack, curve, icon, swimlane, composite state, ER crow's foot, system two flows, causal loop, 2x2 matrix, funnel, concept map, explained step-by-step flow.

Each template is a runnable JSON spec with Vietnamese labels; `--extract-labels en` and `--lang en` render it in English without editing it.

## Color is meaning

Default `ink` strokes, no fill.
At most three accent colors per figure: `err` for what breaks, `node` for the correct result, `l4` for the thing under discussion, `warn` for the affected region, `hot` for the path of one request.
Colors accept token names only - the tool refuses hex codes - so a figure can never drift off the palette and flips correctly in dark mode.

## What the tool checks by itself

Hard errors (`✗`): a box expanded by Excalidraw because its text did not fit, text overflowing its frame, text under 8px on screen, colors that are not tokens, spec errors (naming the element: index, `t`, `id`, start of its text).
Soft reminders (`•`): an arrow crossing a box, a label as long as its arrow, an arrowhead landing on another arrow's start point, more than three accents, a figure that is only boxes and arrows, a figure taller than one screen or wider than the column.
Many reminders carry the fix: a crossing arrow gets a `route`/`bend` already tested to clear it, overlapping text gets a new `y`, a too-tall figure gets the place where it splits.
Text in a figure such as `lỗi #1480` is never mistaken for a color code.
Whether the figure tells the right story is something only a human eye can check - that is step 6, and `evals/` measures it across runs.

## Four models, one brief

Four models (Sonnet 5.5, Opus 5.5, Fable 5.2, GLM 5.3) drew the same eight cases with this skill - a sequence with a branch, a business swimlane, nested states, ER crow's foot, a two-flow system design, a byte-cell strip, threshold and time, a timeline.
See all 32 figures on the [comparison page](https://drawing-excalidraw-figures.vercel.app/#so-sanh), with render rounds and figure sizes.

## Repo layout

```
SKILL.md            the full skill brief - the agent reads this file
scripts/ve.py       renderer: spec JSON -> 4 files
engine/             the real render engine (Excalidraw + Playwright Chromium)
.cache/             prebuilt Excalidraw bundle; rebuild with scripts/excalidraw-bundle.mjs
assets/             icons.json 188 icons + Nunito, Patrick Hand, IBM Plex Mono fonts
references/         figure-type rules, spec syntax, visual language, review checklist
examples/           30 template spec JSONs
evals/              evaluation briefs
tests/              unit tests for theme/renderer + a golden render of all 30 examples
docs/               landing page + the four-model comparison
```

## Tests

Setup: `pip install -r requirements.txt pytest` (the golden render additionally needs `playwright install chromium`).
`python3 -m pytest` runs 100 tests: units for the color system (`engine/theme.py`), the token gate and spec compiler (`scripts/ve.py`), element-naming spec errors, fix suggestions, the flow macro, label translation, the multi-figure page, icon building (`scripts/build_icons.py`), and a golden render that runs the real `ve.py` over all 30 examples, then checks for off-token colors, raw lit hexes and valid `.excalidraw` scenes.
Skip the render (~80 seconds): `python3 -m pytest -m "not slow"`.
GitHub Actions runs the whole suite in `.github/workflows/tests.yml`; the bundle and fonts are committed, so CI needs no Node and runs offline.

## Sources and license

- The [Excalidraw](https://excalidraw.com) library and `@excalidraw/mermaid-to-excalidraw`: MIT.
- Icons in `assets/`: see `assets/ICONS-LICENSE.txt`.
- Sources for the geometry and style rules: `references/sources.md`.
- Every rule in this skill is recorded next to a real measurement taken on the corpus, never a guess.
