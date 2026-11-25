---
name: drawing-excalidraw-figures
description: Draws hand-drawn Excalidraw figures (real .excalidraw scenes plus themed SVG) that explain a technical mechanism, a business flow, or a rough idea written only in words - architecture and request flows, system design with read/write paths, sequence diagrams with alt/opt/loop, business processes in swimlanes, state machines and lifecycles, ER and class diagrams, data-structure anatomy, byte layouts, timelines, hash rings, decision trees, charts, layer stacks, before/after pairs, failure paths, causal loops, 2x2 matrices, funnels, concept maps, physical metaphors. Use this whenever a lesson, doc, note, pitch or answer needs a picture, when a page is a wall of text, when someone has a half-formed idea and wants to see its shape, when an existing figure is only generic boxes and arrows, or when asked to "vẽ hình", "vẽ sơ đồ", "vẽ Excalidraw", "vẽ sequence", "vẽ luồng nghiệp vụ", "vẽ swimlane", "vẽ state", "vẽ kiến trúc hệ thống", "minh hoạ cơ chế", "thêm hình cho bài", "mô hình hoá ý tưởng", "vẽ ý tưởng này", "biến note thành sơ đồ", "giải thích bằng hình", "diagram this", "visualize this idea", even if Excalidraw is not named.
---

# Drawing Excalidraw figures

Turn one idea into a hand-drawn figure, the kind someone who understands the problem sketches on a whiteboard for someone who does not yet.
The idea can be a technical mechanism, a business process, a concept to teach, or a rough thought that so far exists only as text.
Output is a real `.excalidraw` file (opens and edits on excalidraw.com) plus an SVG that uses color tokens and works in both light and dark themes.

Text inside figures follows the source it is for: Vietnamese explanations, English technical terms as the source writes them.
The skill docs are English; the labels in `examples/` are Vietnamese on purpose.

## The load-bearing rule

**Draw the SHAPE of the idea, not the list of components.**
A row of boxes joined by arrows says "A calls B", which one sentence already says.
A good figure turns time into length, data into cells holding real values, a limit into a line, a failure into a red stroke.

The rules come from about 600 real Excalidraw figures, 20 shape libraries, and the owner's pack of sequence, swimlane, state and system-design samples.
Sources and licenses: `references/sources.md`.

## Workflow

Do all six steps in order.
Steps 1, 2 and 6 are skipped most often, and they decide whether the figure is usable.

### 1. Name the reader, then write one sentence

**First ask who reads the figure and what they already know.**
A figure can be true in every fact and still teach nothing: three figures about a browser exploit were correct, and the reader understood none of them, because they assumed the reader knew Base64, the heap and JIT.
It happened again with a Java4Shell figure: every low-level term had its gloss and five fresh-eyes rounds said OK, and a Java developer on the team still had to read up on "JDK vs Base64 vs padding" before the figures meant anything.
No line said how Base64 decoding works when nothing is wrong, and a gap that is never written down is the hardest one to see.
"What does the reader see" depends on "what does the reader already know", so settle that before anything else.

Ask the person who gave the task one question, with these three answers:

| Reader | Already knows | Mode |
|---|---|---|
| Newcomer (student, non-specialist, someone new to the field) | Everyday words, not the field's terms | **Explainer** |
| Developer (works in software, not in this exact area) | General programming terms they use in their own work | **Compact**, plus the explanations below for everything else |
| Specialist (security, database, kernel expert in this exact area) | The field's terms and numbers | **Compact** |

**Write down what this reader surely knows.**
Three to eight items, each saying what the reader does with a thing, in words from their own work (`Java language and daily work: classes, methods, byte arrays, exceptions; calls library methods such as Base64.getDecoder().decode()`).
The figure may lean on this list without a word of explanation, and on nothing else.
**Having used a thing is not knowing how it works.**
A developer who calls a library, a runtime or a protocol every day still does not know what it does inside: a Java developer who has decoded Base64 for years may not know that 4 characters carry 3 bytes, or what the `=` at the end means.
So "how it works inside" never makes the list for anything the reader only calls.

When nobody can be asked, read the level off the source (a beginner lesson, an internal postmortem, a paper) and write the assumed level and the list in the hand-off, so the person who asked can correct it.

Then name the **strategy**: what kind of content this is (a process flow, an interaction, an incident, a vulnerability, an architecture, a mechanism, a data model, a decision, a concept, a knowledge summary, a note, a problem from everyday life, a rough idea or pitch).
`references/strategies.md` gives each one its figure set (how many figures, in what order), its types, the reading-path rules that are mandatory for it, and its pitfalls.
Put it in the spec as `"strategy"`, and the source file as `"source"`, so the tool runs that strategy's checks and lists any number the source does not contain.

Then write a **term list** in your working notes: every term in the figure that this reader may not know (`Base64`, `heap`, `JIT`, `cgroup`, `MVCC`).
For each term, decide one of three:

- **Explain it in the figure**: a few plain words beside the term (`heap: vùng nhớ chương trình xin thêm khi đang chạy`), as a `note` or a second muted line under the label.
- **Replace it** with the everyday word, when the term itself is not what the lesson teaches.
- **Leave it**, only when it is on the reader's "surely knows" list.

A term that the figure uses and the reader does not know is a hole in the figure, the same as a missing step.
So is a fact the figure relies on and never writes: step 2 lists those.

**The two modes:**

- **Compact** (developer, specialist): one figure, dense, real values, terms used as they are. Everything below in this workflow is written for this mode.
- **Explainer** (newcomer): go from the concept to the detail, never the reverse.
  Start with an everyday example or a physical metaphor (`08-metaphor-token-bucket`) that carries the idea, then show the mechanism with real values.
  Put a short sentence in words beside each part (what it is, why it is there), not only a name.
  Fewer things per figure (3 to 5 clusters), and often two or three figures in a row (a `17a`/`17b` progressive series) instead of one dense one.
  The explained flow (`30-explained-flow`) is built for this mode: each step has a number, one line on what happens and a small example.

Now write exactly one sentence: **"Looking at this figure, the reader SEES ... that the paragraph does not show."**
If you cannot write it, do not draw: a needless figure is worse than no figure.
The sentence picks the figure type in step 3 and later becomes the caption: put it in the spec as `"caption"` so `--page` prints it under the figure.
For a newcomer, write the sentence in words the newcomer uses; if it needs a term from the term list, the figure must explain that term.

When the source is a rough idea (a note, a pitch, a paragraph of thinking out loud) rather than a worked-out text, write one more sentence first: **"This idea really says that ..."**, in at most 20 words.
Rough ideas often say three things at once; this sentence picks the one the figure is about.
If the idea genuinely holds two claims, that is two figures.

### 2. List the facts the figure must carry

There are two kinds of source, and each has its own fact list.
A technical or process source (a lesson, lab numbers, a spec, code, a procedure) uses the list right below.
A rough idea uses the idea list after it.

Read the source and write a short fact list in your working notes, not in a file:

- **Things**: every actor, component, state or table that must appear.
- **Main steps** in order, each with its real name: endpoint, command, event, status code.
- **Branches**: every alternative, error, timeout and cancel path, each with an id (A1, A2).
  "Has an error branch" is not a fact; "A2: payment times out after 30s, order goes to FAILED" is.
- **Real values**: numbers from the lab, key names, sizes, limits.
  Copy them from the source, never from memory.

When the source does not say who acts, what triggers a step, or what happens on failure, ask the person who gave the task before drawing.
Do not invent a branch or a number: a figure with a made-up value teaches something false.
Placeholder rows that only show structure (ids 1, 2, 3 in a join table) are allowed when the source gives a schema and no data; say in the hand-off that they are examples.
A value you derive (12 - 8 = 4 byte) is fine when the subtraction is visible in the figure.
When nobody can be asked (you run as a subagent or in a batch), draw the most literal reading of the source and list every assumption in your hand-off.
If the input already is structured (a Mermaid or PlantUML block, a use case, an SRS flow, output of the `dev-ba-kit` skills), take the fact list from it instead of re-deriving it.

**Idea list**, for a rough idea:

- **Concepts**: every noun the idea leans on, in the writer's own words. Do not rename them into jargon.
- **Relations**: how each pair connects, as a verb: causes, slows, trades off against, is part of, comes before, needs.
  Mark the direction and, for causes, the sign: more A gives more B (`+`) or less B (`-`).
- **Tension**: the conflict or trade-off that makes the idea worth saying. Most ideas worth a figure have one.
- **The claim**: what the writer wants the reader to believe or do after seeing it.

The no-invention rule holds here too: a concept or relation the writer did not state is an assumption, so ask or list it.
A rough idea rarely has numbers, and the figure does not need any: it is a conceptual figure (see "Level of detail" in `references/visual-language.md`).
Keep a number only when the writer gave it.

**Premises**, for either kind of source.
The term list (step 1) is made of the figure's words.
A figure also leans on facts that appear nowhere in it: a rule of how a part normally works (`4 Base64 characters carry 3 bytes`), a relation between two things it names (`the JDK is what runs the decoder`), a convention (`=` at the end is padding, not data).
A reader who lacks a word sees the gap and looks it up.
A reader who lacks a premise only knows that they do not understand, and cannot tell what to look up.
Read the fact list step by step and ask of each step: what must the reader already accept for this step to make sense?
Write each answer down.
A premise that is not on the "surely knows" list goes into the figure as one line in plain words beside the step that needs it, in the figure's body size and ink: it is the line the reader is missing, not a caption.
When a step needs a premise that cannot be said in a line, the step is a detail the figure can drop.
When the thing works inside something the reader only calls, show the normal behaviour first (`references/strategies.md`, "The normal case first").

These lists are the checklist for step 6.

### 3. Pick the figure type by what must be seen

For a rough idea, first name the structure of the idea from the idea list, then take the type it points to:

| The idea is shaped like | Figure type | Template in `examples/` |
|---|---|---|
| A causes B causes C, and C feeds back | Causal loop | `26-causal-loop` |
| Two forces pull against each other, options sit between them | 2x2 matrix | `27-matrix-2x2` |
| Many enter, fewer pass each stage | Funnel | `28-funnel` |
| Several concepts and how they relate | Concept map | `29-concept-map` |
| A foundation that holds up what is above | Layer stack | `18-layer-stack` |
| Life before and after one change | Before and after | `06-before-after` |
| A choice between options | Decision tree | `10-decision-tree` |
| Who does which step | Swimlane | `22-swimlane` |
| Steps in order that a newcomer must follow | Explained flow | `30-explained-flow` |
| Something abstract that needs intuition | Physical metaphor | `08-metaphor-token-bucket` |
| A trend or a point of no return | Curve or threshold | `19-curve`, `05-threshold` |

For a technical source, or when the table above does not fit, pick from the full table:

| The reader needs to see | Figure type | Template in `examples/` |
|---|---|---|
| Who calls whom, in what order | Request flow | `01-request-flow` |
| Steps in order, each explained with a small example ("draw the flow", a newcomer) | Explained flow | `30-explained-flow` |
| What is inside a thing | Anatomy, nested frames | `02-anatomy` |
| How data lies on disk or in RAM | Byte cells | `03-byte-cells` |
| What happens over time | Timeline | `04-timeline` |
| A limit being crossed | Bars against a threshold | `05-threshold` |
| What changes when one thing is fixed | Before and after | `06-before-after` |
| One structure, two ways to look | Two views, same colors | `07-two-views` |
| Intuition before the mechanism | Physical metaphor | `08-metaphor-token-bucket` |
| The plan and where it can break | Happy path and failure branch | `09-failure-branch` |
| Which one to choose | Decision tree | `10-decision-tree` |
| Message order between parties, no branches | Sequence | `11-sequence` |
| How a thing changes state | State machine | `12-state-machine` |
| How data relates | ER and tables with real rows | `13-er-table` |
| Partitioning on a ring | Hash ring | `14-hash-ring` |
| A real payload, command, config | Annotated code block | `15-code-evidence` |
| Which layer does the work | Layer lanes | `16-layer-lanes` |
| A system growing step by step | Progressive series | `17a-progressive-1` and `17b-progressive-2` |
| Layers stacked on each other | Layer stack | `18-layer-stack` |
| Distribution, trend, long tail | Curve on axes | `19-curve` |
| Familiar components | Library icons | `20-icon` |
| A flow that branches: success, failure, retry | Sequence with `alt`/`opt`/`loop` | `21-sequence-frames` |
| Which role does which step of a process | Business flow in swimlanes | `22-swimlane` |
| A lifecycle with nested and terminal states | Composite state | `23-composite-state` |
| Cardinality between tables, or classes | ER with crow's foot | `24-er-crowfoot` |
| One architecture, two paths (write/read) | System design with two flows | `25-system-two-flows` |
| A feedback loop that amplifies or balances itself | Causal loop | `26-causal-loop` |
| Where options sit on two trade-off axes | 2x2 matrix | `27-matrix-2x2` |
| How much survives each stage | Funnel | `28-funnel` |
| Concepts joined by named relations | Concept map | `29-concept-map` |

**"Flow" is not a broken rule.**
When someone asks for a flow (`luồng`, `các bước`, "how does it go"), they want arrows in order, and that is right.
The load-bearing rule forbids boxes that only NAME things, because their arrows say only "A calls B".
A flow passes the rule when every step carries what changes at that step: a real value, an example, a condition.
Use `30-explained-flow` for that (number, one line, small example per step); add a `sequence`, `swimlane` or failure branch only when several parties or branches matter.

`references/figure-types.md` describes each type: when to use it, when not to, how to build it, where it breaks.
Read the section of the chosen type before writing the spec.
Then run the nine-line pre-render checklist in `references/lessons-from-runs.md`: it removes the mistakes that cost the most rounds in testing.
A lesson about the mechanism inside a technology almost never wants a plain request flow.
Interaction over time is a sequence, the life of one entity is a state diagram, who does what is a swimlane: do not mix two of those three in one figure.
Supporting pieces are fine: a timeline may carry a small `plot`, an ER figure a `table` of rows, any figure a `code` block.

### 4. Write the spec

Copy the template of the chosen type and edit it; do not start from a blank file.
A template's `"strategy"` describes the template's own content: set it to the strategy you picked in step 1.
A spec is short JSON: coordinates, text, colors by token name.
Full syntax of every element: `references/spec.md`.
Conventions for shapes, color, layout, arrows: `references/visual-language.md`.

Four things to remember even before opening those files:

- **Real values beat generic names.** `user:1`, `1 023`, `429`, `POST /orders` instead of "key", "n", "error", "request".
  A figure with real values teaches; a figure of generic labels only names things.
- **Color is meaning.** Default is `ink` stroke, no fill.
  At most three accent colors per figure: `err` broken, `node` correct, `l4` the thing under discussion or the new thing, `warn` the affected region, `hot` the path of one request.
- **Show the reader the path.** A figure with several regions numbers them ① ② ③ in story order, joins each side panel to the part it explains with one dashed line, glosses each term in plain words under it, and gives each abstract category one real example. Rules and when to skip them: "Guiding the eye" in `references/visual-language.md`.
- **The default reading column is 666px** (a typical article column; `--col N` previews another width). Keep the figure under about 800 units wide (the width the tool reports, which includes 20 units of padding); it is a guide, the tool enforces text size.
  Out of room: stack vertically or split the figure, never shrink the text.

Name the spec after the lesson slug plus what the figure shows, lowercase ASCII with hyphens: `mvcc-snapshot-hai-transaction.json`.
A file name given by the person who asked wins.

### 5. Render

```bash
python3 .claude/skills/drawing-excalidraw-figures/scripts/ve.py <spec.json> [--out dir] [--col N] [--open]
```

The first time on a machine, run `ve.py --check`: it checks Python, Playwright and Chromium and prints the one command that installs whatever is missing.

The tool prints one summary line per figure, then the paths of the two PNGs to open.
A `✗` line is a hard error to fix (text overflow, shape grown by Excalidraw, text too small, a spec error naming its element).
A `•` line is a nudge: read each one, fix it or know exactly why you keep it.
Many nudges carry the fix: a crossing arrow names the `route` or `bend` that clears it, overlapping text names the `y` that frees it, a figure taller than one screen names where it splits.
`--col N` previews at another column width, only for a figure that will not sit in the site column.
`--open` opens the two PNGs after rendering.

Other options, all in `references/spec.md` under Command line:

- `--page out.html` (or `out.pdf`) puts every rendered figure on one page, each with its `caption`, under a shared `--title` and `--caption`.
- `--extract-labels en` writes `<spec>.en.labels.json` with every label; translate its values, then `--lang en` renders `<spec>.en-*.png` without touching the spec.

### 6. Open the images, check, fix

Open both `<name>-light.png` and `<name>-dark.png` with the image reader.
A valid spec and a silent tool do not mean the figure reads well: the tool cannot know whether the figure says the right thing.
Go through `references/review.md`, which starts with the reader check against step 1 (term list, retell test) and the coverage check against the fact list of step 2, then fix the spec and render again.
Expect 2 to 4 rounds.
Stop when the figure says the sentence of step 1 with the caption covered.

Before polishing, get **fresh eyes**: give only the PNG, the reader and the "surely knows" list to a subagent (or the person who asked) with the questions in `references/review.md`.
The first four are asked as the reader; the rest have the reviewer list what the figure takes for granted, which is how a missing premise shows up.
Fix what the answers show the figure does not say.

For a rough idea with a person to ask, show the first clean render before polishing and ask one question: "Is this what you meant?"
Name the one relation or tension you were least sure of, so the answer is about the idea and not the colors.
Writers often see their idea more clearly in the draft and change it; that is the figure doing its job, so redraw rather than defend the first version.
With nobody to ask, list the relations you assumed in the hand-off instead.

## Security and other sensitive topics

A figure travels further than the text around it, so decide how far it goes before drawing.

**Draw**: the mechanism and the defence.
What the weakness is, why it exists (the design choice or the missing check), which condition an attack needs, where in the chain each defence stops it, and how to detect it.
A figure that shows "the bounds check is missing here, so a long input overwrites the next field, and this check or this setting stops it" teaches defenders and students.

**Stop before**: anything that works as instructions against a system the reader does not own.
No working payloads or shellcode, no exact offsets, addresses or gadget chains, no ordered step-by-step exploitation of a named product or version, no commands aimed at a target, no bypass recipe for a specific defence, no real credentials, tokens or personal data.
Name the class of the step (`ghi đè con trỏ hàm`, `<payload>`) instead of its content, and keep real values to the ones the defence needs (a limit, a status code, a log line).

Test before rendering: could someone copy the figure into a terminal or a debugger and attack a real system with it?
If yes, cut it back to mechanism level and say in the hand-off what was left out and why.
The same rule holds for other harm-sensitive topics (weapons, self-harm, getting around safety controls): show how it works and how it is prevented, not how to do it.

## When no type fits

The table covers the common cases, not all of them.
`references/figure-types.md` has a "Rare figure types" table (DFD, use case, deployment, journey, org chart, roadmap and more).
For a truly new idea ask: what does this resemble in the real world (a bucket, a funnel, an assembly line, a ledger, a queue of people)?
Then build it from primitives (`box` `ellipse` `diamond` `line` `arrow` `text`) and free polygons (`line` with `closed`), following "Building a new figure from primitives" in the same file.

## Where files go

The four output files (`.excalidraw`, `.svg`, `-light.png`, `-dark.png`) land next to the spec unless `--out` is given.
Keep the `.json` spec with the outputs: it is the source for later edits.
Which file to hand over depends on where the figure goes:

| Destination | Use |
|---|---|
| Markdown on GitHub, a chat, a slide, a doc tool | `-light.png` (or `-dark.png` for a dark slide) |
| A web page you control | `.svg` plus `dist/assets/tokens.css`, which defines the color tokens for both themes |
| Someone who will keep editing by hand | `.excalidraw`, opens on excalidraw.com |

A site that already has its own figure pipeline and checker (for example a docs site that embeds token SVG through a fence and runs a contrast check) keeps its own rules: follow them, and run its checker after copying the SVG in.
When the destination is unclear, ask the person who gave the task; when nobody can be asked, leave the files next to the spec and say so.
The skill stops at producing correct files; it does not edit the site's engine or source code.

## Bundled references

| File | Read when |
|---|---|
| `references/strategies.md` | In step 1, to plan the figure set for this kind of content |
| `references/figure-types.md` | After picking the type, before writing the spec |
| `references/spec.md` | You need the exact syntax of an element |
| `references/visual-language.md` | Unsure which shape for what, color, layout, arrow labels |
| `references/lessons-from-runs.md` | Before the first render (checklist), and when a figure needs more than three rounds |
| `references/review.md` | After every render, starting with the reader check |
| `references/sources.md` | You need to know where a rule comes from, or an icon's license |
| `references/samples/README.md` | You want a real example of a whole system-design scene or a business diagram source to look at |
| `examples/*.json` | Always: copy one as the starting point |
