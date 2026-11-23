# Strategies: how to draw by kind of content

The same facts need a different figure set depending on what the content IS.
A vulnerability write-up, a checkout flow, a summary of a course chapter and a note about a hard week each answer a different reader question, so each gets its own plan: how many figures, in what order, which types, and which reading-path rules are mandatory.

Pick the strategy in step 1, right after naming the reader, and write it in the spec:

```json
{"strategy": "vulnerability", "source": "../bai-goc.md", "caption": "...", "elements": [ ... ]}
```

`strategy` makes `ve.py` apply that kind's checks (table at the end).
`source` (or `--source file`) lets it list every number in the figure that the source text does not contain.

Contents: [Pick a strategy](#pick-a-strategy) · [Technical](#technical) · [Knowledge, notes, ideas, everyday life](#knowledge-notes-ideas-everyday-life) · [Medium: article, slides, page](#medium-article-slides-page) · [What the tool checks per strategy](#what-the-tool-checks-per-strategy)

## Pick a strategy

| The person says, or the source is | Strategy |
|---|---|
| "vẽ flow", "luồng nghiệp vụ", "các bước", a procedure, an approval process | `process-flow` |
| "sequence", who calls whom, a protocol handshake, an API exchange | `interaction` |
| "giải thích sự cố", a postmortem, a bug report, "vì sao hệ thống chết" | `incident` |
| a CVE, a security advisory, "lỗ hổng", an attack and its defence | `vulnerability` |
| "kiến trúc", system design, how services fit together | `architecture` |
| how something works inside: a data structure, an algorithm, a protocol, a JIT, an index | `mechanism` |
| tables, entities, relations | `data-model` |
| "chọn cái nào", a trade-off, options against criteria | `decision` |
| "giải thích khái niệm", teach one idea to someone new to it | `concept` |
| "tổng hợp kiến thức", a chapter or a course summarized, a cheat sheet, how topics connect | `knowledge-summary` |
| "note", a journal entry, meeting notes, thinking out loud | `note` |
| a problem from everyday life to model: a habit, money, family time, a team that keeps slipping | `life-problem` |
| a rough idea, a business pitch, "vẽ ý tưởng này", a claim someone wants others to believe | `idea` |

Two kinds at once (an incident caused by a vulnerability) means two figure sets: draw the one the reader asked about first, and link to the other.

## Technical

### `process-flow`

**Reader question:** what happens, in what order, and who does each step?
**Figure set:** one figure; two when the failure paths are the point (happy path, then where it breaks).
**Types:** explained flow (`30`) for one actor, swimlane (`22`) for several roles, failure branch (`09`) when errors matter.
**Mandatory:** numbered steps; every step says what changes (a value, a status, a document), not only a name.
**Optional:** a small example beside each step (`30`), a `card` with the real rule (`> 5 ngày cần HR duyệt`).
**Pitfall:** boxes that name departments with bare arrows between them. Each arrow says what passes: the form, the status, the money.

### `interaction`

**Reader question:** who sends what to whom, in what order, and what happens when an answer does not come?
**Figure set:** one sequence; a second for the failure path when it needs more than one `alt`.
**Types:** sequence (`11`), sequence with fragments (`21`).
**Mandatory:** real message names (`POST /token`, `302 Location`), numbered messages when the text refers to them.
**Optional:** a `code` block with one real payload or header beside the message that carries it, joined by a dashed arrow.
**Pitfall:** more than about 12 messages. The tool's height nudge names where to split; repeat the actor row in the second figure.

### `incident`

**Reader question:** what broke, why, how bad, and what we do now?
**Figure set:** two to four, in this order: what happened (timeline `04`, or before/after `06`), why (the mechanism: `mechanism` rules), impact (threshold `05`, curve `19`, or the affected parts marked `err`), the fix (before/after, or a decision tree "am I affected").
**Mandatory:** regions numbered in story order; every number from the postmortem (`--source`); the trigger and the root cause as two different marks, because readers confuse them.
**Optional:** a timeline of detection and response under the mechanism figure.
**Pitfall:** blaming in the figure. Draw the system and the missing guard, not a person.

### `vulnerability`

**Reader question:** what is the weakness, am I affected, and what do I do?
**Figure set:** three or four, as in the Java4Shell set: (1) the effect on memory or data, before and after; (2) why the code does it (explained flow `30` of the faulty computation); (3) am I affected (decision tree `10` with the check command and the mitigation flags); (4) disclosure timeline (`04`).
**Mandatory:** the rules of SKILL.md "Security and other sensitive topics": mechanism and defence only. The tool stops (`✗`) on text that works as attack input: a run of 16+ identical characters, escaped bytes, a shell command, a JNDI string. Write the shape of the input (`64 ký tự Base64 + "="`), not the input.
**Mandatory:** numbered regions, the cause panel joined to the effect it causes, a plain gloss under every low-level term (`intrinsic`, `heap`, `mask`), one concrete example of what the overwritten or leaked data can be, taken from the advisory (`token, khoá bí mật`).
**Optional:** a comparison pair (safe path against faulty path) as two `code` blocks side by side, the faulty one `err`.
**Pitfall:** exploitation steps (heap grooming, gadget chains). They help no defender and turn the figure into instructions.

### `architecture`

**Reader question:** which parts exist, and which path does a request or a write take through them?
**Figure set:** one overview; one zoom per path that the text discusses.
**Types:** system with two flows (`25`), layer stack (`18`), layer lanes (`16`), icons (`20`).
**Mandatory:** at most 7 clusters; the path under discussion in `hot` or numbered; everything off the path `muted`.
**Pitfall:** every component the company runs. Draw only what the current point needs.

### `mechanism`

**Reader question:** how does it work inside, with real values?
**Figure set:** one figure, or a progressive series (`17a`/`17b`) when the state evolves.
**Types:** byte cells (`03`), anatomy (`02`), hash ring (`14`), timeline (`04`), two views (`07`), metaphor first (`08`) for a newcomer.
**Mandatory:** real values in cells and labels; before/after stacked when one thing changes state.
**Pitfall:** a request flow. A mechanism lesson almost never wants one.

### `data-model`

**Reader question:** what is stored, and how do the tables relate?
**Types:** ER with crow's foot (`24`), ER with real rows (`13`).
**Mandatory:** cardinality on every edge; a few real rows when the relation is the surprise (a join table).

### `decision`

**Reader question:** which option, under which condition?
**Types:** decision tree (`10`), 2x2 matrix (`27`), before/after (`06`) for one change.
**Mandatory:** leaves are concrete answers (`SSE`, `cập nhật JDK ngay`), filled so they stand out; at most three levels of questions.
**Pitfall:** a pros and cons table drawn as boxes. If the answer depends on one or two questions, it is a tree.

## Knowledge, notes, ideas, everyday life

### `concept`

**Reader question:** what is this idea, and why does it behave as it does?
**Figure set:** explainer mode from SKILL.md step 1 when the reader is new: (1) an everyday example or physical metaphor (`08`) that carries the idea; (2) the idea itself with its real terms, each glossed; (3) optional, one common misconception set against the truth (before/after `06`).
**Types:** metaphor (`08`), explained flow (`30`), concept map (`29`) for an idea made of parts, curve (`19`) for a trend.
**Mandatory:** start from what the reader knows; number the parts when there are several; every term glossed in plain words.
**Pitfall:** a definition in a box. If the figure only restates the definition, it is not needed.

### `knowledge-summary`

**Reader question:** what are the main ideas of this topic, and how do they connect?
**Figure set:** one overview map, then one figure per idea that needs its own mechanism, never one giant map.
**Types:** concept map (`29`) for how ideas connect, layer stack (`18`) for foundations and what builds on them, progressive series (`17`) for a topic learned in stages, timeline (`04`) for a history.
**Mandatory:** at most 9 main shapes (the tool nudges above that); every arrow labelled with its relation (`là nền của`, `dùng`, `trái với`), since in a summary the relations are the knowledge; one idea marked `l4` as the centre the rest hangs on.
**Optional:** one real example under each idea (a command, a number, a case) so the map is not only names.
**Pitfall:** a mind map of every heading in the chapter. Keep the ideas a reader must remember a week later; leave the rest in the text.

### `note`

**Reader question** (often the writer, later): what did I think, decide or notice, and why?
**Figure set:** one figure, in the writer's own words.
**Types:** timeline (`04`) for a sequence of events or a decision over time, before/after (`06`) for a change of mind, 2x2 (`27`) for options weighed, causal loop (`26`) for a pattern that keeps coming back.
**Mandatory:** the writer's words, not cleaned-up jargon; the decision or the open question marked as the one accent.
**Pitfall:** turning a note into a report. Ask "is this what you meant?" after the first render (SKILL.md step 6).

### `life-problem`

**Reader question:** why does this keep happening, and where can I push to change it?
**Figure set:** one model figure, plus an optional second with the intervention drawn in.
**Types:** causal loop (`26`) when the problem feeds itself (less sleep, more coffee, worse sleep), 2x2 (`27`) for a trade-off (time against money), funnel (`28`) for something that leaks at each stage (plans that never happen), metaphor (`08`) for a feeling of overload (a bucket filling faster than it drains), curve or threshold (`19`, `05`) for a point of no return.
**Mandatory:** every arrow says its relation or its sign (`+` more gives more, `-` more gives less); the loop is named (`R` reinforcing, `B` balancing); the lever the person can actually pull marked `l4`.
**Optional:** the intervention as a dashed `node` arrow that breaks the loop.
**Pitfall:** a list of causes in boxes. A life problem worth drawing almost always has a loop or a tension; find it before choosing the type.

### `idea`

**Reader question:** what is this idea really claiming, and what makes it worth saying?
**Figure set:** one figure; a second only when the idea truly holds two claims.
**Types:** the "idea is shaped like" table in SKILL.md step 3: causal loop (`26`) for a flywheel, 2x2 (`27`) for a positioning, funnel (`28`) for a conversion, concept map (`29`), before/after (`06`).
**Mandatory:** the "This idea really says that ..." sentence first; the writer's own words; the tension drawn as a shape (two arrows pulling apart, a loop, a gap), not only written; every arrow says its relation.
**Optional:** the writer's real numbers when given (a funnel's counts), never invented ones.
**Pitfall:** polishing before asking "is this what you meant?" (SKILL.md step 6).

## Medium: article, slides, page

The strategy says what to draw; the medium says how big.

- **Article or docs column (default):** 666px column, keep under about 800 units wide, one screen tall (the tool nudges above 900px).
- **Presentation to a team:** one figure per slide, numbered parts so the speaker can say "look at ②"; render all figures of the set with `--page deck.pdf --title ... --caption ...` to hand out; check `-dark.png` for a dark slide theme.
  The set uses one meaning per color across all figures (in the Java4Shell set, `err` is the faulty path everywhere).
- **Wiki or wide page:** preview with `--col 1100`, never to silence the font check on a figure meant for the column.

## What the tool checks per strategy

Every strategy gets the general checks (overflow, crossings, size, colors) and these reading-path checks, as `•` nudges unless marked `✗`:

| Check | When |
|---|---|
| A `code` block or `card` beside the main structure has no arrow or note reaching it (a side-by-side comparison pair counts as one) | Always |
| Badge numbers skip or repeat | Always |
| A figure of several parts (3+ regions, or side panels beside a main structure) has no badge | `process-flow`, `incident`, `vulnerability`, `concept` |
| Text works as attack input (16+ identical characters, `\x..` bytes, a shell, `${jndi:`) | Always `•`; `✗` for `vulnerability` |
| An arrow without a label (dashed note pointers excepted) | `knowledge-summary`, `life-problem`, `idea` |
| More than 9 main shapes | `knowledge-summary`, `note` |
| Numbers in the figure that the source does not contain | Any strategy with `--source` or `"source"`; `incident` and `vulnerability` nudge you to give one |

The tool still cannot tell whether the figure is right for its reader.
That is the fresh-eyes check in `references/review.md`.
