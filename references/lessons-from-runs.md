# Lessons from test runs: habits to keep, habits to drop

Source: 24 runs on 2026-11-17, eight tasks (sequence, swimlane, state, ER, system design, byte cells, threshold, timeline), each drawn once by Sonnet 5.5, Opus 5.5 and Fable 5.2 with this skill.
A second batch on the same day added GLM 5.3 on the same eight tasks; its observations are in the "GLM 5.3" section below.
All runs rendered clean and matched the facts of the task, so the tool's `✓` does not separate a good figure from a mediocre one.
What separated them is below.
One run per cell: these are observed habits, not statistics.

The owner draws mainly with Opus 5.5.
If you are Opus, read "Opus 5.5" first; it lists the habits that cost you rounds.

## Rules distilled from the runs

Each rule names the run that taught it.

### Choosing what to draw

1. **Keep the dimension the source is about.** A paragraph about "the 2 seconds after expiry" needs a time axis; three bars against a limit drop it (Sonnet, cache stampede). Before picking the simplest type, check that every quantity in the step-1 sentence (duration, count, order, limit) has a visible length, position or count.
2. **Countable things are drawn countable.** "10 hold, 4 wait" as 14 thin bars beats two boxes labelled 10 and 4 (Fable, connection pool). Ten marks standing for 500 need the scale written once ("mỗi thanh = 50").
3. **Write the reason next to the thing.** Padding cells labelled "để b vào offset 4" and dotted lines on the 4-byte boundaries teach; padding cells labelled "đệm 3" only name (Opus against Sonnet, struct padding).
4. **Name the real setting.** The line at 2s is `connectionTimeoutMillis = 2000`, not "hết timeout" (Sonnet, connection pool). A config key, flag or command in the source must appear verbatim once.
5. **A flag is not a state.** `cancel_at_period_end` is a dashed intermediate box or a note on the arrow, never a sixth solid state (Fable, subscription).
6. **Show the relation that does not exist.** For "why a join table", a dashed `muted` N-N edge with a one-line legend makes the missing foreign key visible (Fable, ER).

### Staying true to the source

7. **Do not add actors or messages the source does not name.** A Client lifeline, `nil`, `row`, `OK`, a linear ramp between two known values: each was added in some run. Add one only when a named step has no receiver, and list it under assumptions.
8. **Skip replies that carry nothing.** When the `alt` label already says hit or miss, the reply arrow repeats it (Opus drew several extra arrows on cache-aside; Fable drew none and lost nothing).
9. **Illustrative rows are allowed, measurements are not.** Rows (1,3) (1,5) (2,3) in a join table are structure and must be declared as examples in the hand-off; "21 connections" is a number and needs "20 + 1" shown so the reader sees it is derived.
10. **Keep the source's wording for a branch.** "thành công", not "gateway trả lời"; "hết 3 lần", not "lỗi".

### Color

11. **Red means broken, nothing else.** A warning note is `warn`; a terminal state reached by good and bad paths is `ink`; a struct that is merely larger is not red (Sonnet used `err` for all three).
12. **A colored frame colors everything in it.** An `alt` frame in `node` makes the failure branch look correct (Opus, cache-aside). Frames stay `muted`; color the messages.
13. **One accent for the thing under discussion.** The join table in `l4`, the DEL arrow in `l4`: the eye lands there first. Emphasis by `weight` 4 is a second-best substitute.

### Layout

14. **No diagonal edge in a swimlane, no edge that starts inside a diamond.** Give the decision one outgoing edge per side (left, bottom, right) and place each target on that side (Opus, KYC, drew a diagonal and a line leaving the tip inward).
15. **Two columns in one lane instead of a longer page.** Reject on the side of the customer, approve on the side of the reviewer, and no arrows cross (Fable, KYC: 835 tall against 1117).
16. **A label never sits on a frame border, a lifeline, a plot axis or another arrow's head.** The tool catches free text that straddles a box or frame border, or sits inside a frame less than 4 units from its edge; text on the bar or crow of an ER end it reports too; a sequence message label across a lifeline it reports too; an arrow's line through free text it reports too, and a plain `line` such as a time guide too, also through a label inside a box or `cells` strip; a detached arrow label resting on its own line it reports too; text on a plot axis or any other arrowhead it does not see. Look for it in the image: it was the most common leftover flaw in all three models.
17. **A long horizontal message that crosses a lifeline gets its label over the first gap**, not centred on the lifeline it crosses. The `sequence` macro now places it there itself, so write labels that fit one gap.
18. **An arrow into the bottom of a `db` with `kind` runs through its label.** Enter from the top or a side.
19. **Width is measured on the reported size.** Plan 780 units of content; four runs landed at 805 to 826 by planning 800.
20. **Short return and loop arrows hide behind their heads.** Keep 45 units between a note and its target and 25 between stacked nodes.

### Stopping

21. **Round 1 is a draft even when the tool is silent.** The two one-round runs (Sonnet on ER, Fable on cache-aside) each left a fixable flaw: a diagonal edge, a label on a lifeline.
22. **Five or six rounds means the layout plan is wrong, not the coordinates.** Opus spent 5 and 6 rounds nudging labels on two figures. After round 3 with the same kind of complaint, change the structure: fewer labels on routed arrows, a `steps` list beside the figure, or two figures.
23. **Open the dark PNG after the last render**, not only after the first (Sonnet skipped it once).
24. **Never hand off a flaw you can name.** "Two arrows cross the plot axis, kept" (Fable, stampede) is a round not taken.
25. **Every success path ends in an `end` node**, not in the last box (Sonnet, KYC).

## Opus 5.5

Fastest way to a good figure with Opus: keep its strengths, cap its two costs (rounds and length).

**Strengths to keep.**
- Annotates the reason for each fact (alignment boundaries, "để 12 chia hết cho 4").
- Richest evidence: real lists as `cells`, a `code` block with the command, a time plot per mode.
- Catches its own semantic slips by eye (noticed the green `alt` frame and fixed it).
- States inferences honestly in the hand-off.

**Habits to drop.**
- **Too complete.** Draws every reply and adds an actor to receive them. Apply rules 7 and 8 before writing the spec: cross out every arrow whose removal loses no fact.
- **Too tall.** Lays branches out one below the other (1117 units for the KYC swimlane). Apply rule 15: before round 1, ask which two nodes can share a row.
- **Too many rounds.** 3.5 on average, 5 and 6 on the dense figures, mostly moving free labels off borders. Apply rule 22, and decide label positions before rendering: a label goes on the longest straight segment of its arrow, away from frames.
- **Diagonal and inward edges** in swimlanes. Apply rule 14.
- **Invents filler to make the figure concrete** (`OK`/`nil`, a linear ramp, sample rows). Apply rules 7 and 9: declare it or drop it.
- **Styles containers** (colored `alt` frame). Apply rule 12.

**Opus pre-render checklist** (30 seconds, saves a round):
1. Every arrow carries a fact from the list; no reply that repeats a label.
2. No actor the source does not name, unless a step needs a receiver.
3. Tallest column has at most 7 rows; otherwise two columns in a lane or two figures.
4. Each decision: one outgoing edge per side, targets placed on that side.
5. Content spans at most 780 units.
6. Every free label sits on a straight segment, 12 units clear of any frame, lifeline or axis.
7. Accents: at most three, `err` only on what is broken, frames `muted`.

## Sonnet 5.5

**Strengths.** Fastest (76s against 132s for Opus), compact, does not invent actors, picks the right template quickly.

**Habits to drop.**
- Stops at "correct": leaves out reasons, the config name, the `end` node (rules 3, 4, 25).
- Picks the simplest type and loses a dimension (rule 1).
- Uses `err` for emphasis (rule 11).
- Stops after one round and skips the last dark check (rules 21, 23).
- Leaves an arrow through a label when the tool is silent (rules 16, 18).

Use Sonnet for figures that follow a template closely, and add one instruction: "after the tool is clean, do one more round for reasons, real setting names and label collisions".

## Fable 5.2

**Strengths.** Best balance of compact and rich; most explicit list of assumptions; countable marks, legends, the dashed intermediate state; fewest invented messages.

**Habits to drop.**
- Runs slightly wide (805 to 820) and so has the smallest text on average (rule 19).
- Packs two figure types into one on dense topics (timeline plus two plots on cache stampede) until it reads busy: split when a figure passes about 80 elements.
- Knowingly keeps a named flaw (rule 24).
- Lets a long message label sit on a lifeline (rule 17).

## GLM 5.3

**Strengths.**
- Keeps the dimension the source is about (rules 1 and 2): time axis for stampede and pool exhaustion, a byte ruler that lines up with cell edges for struct padding, 14 countable bars for the pool.
- Real settings verbatim: `connectionTimeoutMillis = 2000` on the timeline, `SET lock:home:feed NX EX 5` as a code block, `max_connections = 200` as the threshold label.
- Restructures instead of nudging: when the first swimlane draft had overlapping boxes and a crossed arrow, it rebuilt the lane layout (rule 22) rather than spending rounds moving coordinates.
- Reviews rendered images and fixes what it names; every flaw it recorded, it fixed before hand-off (rule 24).

**Habits to drop.**
- Writes notes longer than the container: hit the sequence `note` single-line limit twice and the swimlane first draft had two boxes sharing a lane without `dx`. Compose the reason inside the box text or split the lane into two columns before rendering.
- Sizes diamonds for one line of text: three of the first drafts had a diamond grow after render. Plan diamond `w` at twice the text width before the first render (spec.md says it; this model still had to learn it the expensive way).
- Lets two arrows converge on one edge point (both the auto-approve and the manual-approve paths entering the top of the same success box). Pick `toAt` positions per incoming arrow before rendering.
- First system-design draft ran 871 units wide; folding a floating note into the component it describes (the worker box carried "> 1M follower: không fan-out" itself) brought it to 779 without losing a fact.

## Rough ideas and non-technical sources

Source: a third batch on 2026-11-17 after the skill learned rough ideas: four non-technical tasks (a coffee-shop pricing pitch, natural selection for a class, a 2 a.m. note about leaving a job, an expense-approval process), each drawn once by Sonnet 5.5 and Opus 5.5.
All eight runs drew the idea the writer meant; on the two open-ended tasks both models independently found the same core (8 months with an exit against 5 years ending in regret; a loop against a dead end).

**What worked.**
- The "This idea really says that" sentence. Every run wrote it, and every run then dropped the side claims instead of cramming them in. The personal note became a time axis in both models: "8 tháng" and "5 năm" are lengths, so the bounded risk and the long one are seen, not read.
- Keeping the writer's words. Opus put the writer's own verbs on the arrows (`kéo tới`, `thành khách quen`, `nhận ra ngay`) instead of `+`; that reads better than signs for a pitch. Use signs when the writer reasons about more and less, verbs when the writer tells a story.
- Countable things in a teaching figure. Opus drew every moth across generations (1/10, 2/10, 4/10 dark, then a 50-moth grid at 98%) and crossed out the students' wrong idea first; the reader watches the proportion change and sees no moth change colour.

**Habits to drop.**
- Drawing a literally dark thing in `ink`. Both moth runs drew dark moths and the sooty trunk in `ink`, which flips to light in the dark theme, so the dark PNG taught the opposite. Use `lit-dark` / `lit-light` for a real brightness (added after this batch).
- Leaving a loop's arrows unlabelled when the loop is the point. One run drew the loop with bare arrows; a reader cannot tell "brings" from "blocks". Label every edge of the loop the idea is about.
- Two figures in one when the idea has two options: fine when they share rows that line up across the divide (Opus put "hạt rẻ" level with "chất lượng"), busy when they do not.

A regression check ran the three technical evals with Sonnet on the new skill: Kafka lag and MVCC passed every grader.
OOM 137 missed the "limit line" grader, and an A/B against the skill before this change chose the same angle ("two causes, one exit code 137"), so the miss comes from how the lesson reads, not from the change.

## Numbers

| | Sonnet 5.5 | Opus 5.5 | Fable 5.2 | GLM 5.3 |
|---|---|---|---|---|
| Mean time per figure | 76s | 132s | 114s | not comparable* |
| Mean tokens | 105k | 112k | 109k | not comparable* |
| Mean render rounds | 2.5 | 3.5 | 2.6 | 3.9 |
| Mean smallest text | 13.1px | 13.1px | 12.7px | 13.6px |
| Mean width (units) | - | - | - | 699 |

\* GLM ran in a separate session with interruptions and reviewed renders through a
vision tool, so time and tokens are not comparable with the automated batch.
