# Review the figure after every render

Open `<name>-light.png` and `<name>-dark.png`, then run three passes in order.
Pass 1 matters most and is skipped most, because pass 2 and 3 errors are easier to see.

## Pass 1: does the figure say the right thing

- **Reader**: read the figure as the reader named in step 1, knowing only what that reader knows.
  Go down the term list: every term is explained in the figure, replaced by an everyday word, or already known at that level.
  A term with none of the three is a hole: fix it before anything else.
  For a newcomer (explainer mode): does the figure start from something familiar (an everyday example, a metaphor) before the mechanism, and does each part carry a few words on what it is, not only its name?
- **Retell test**: with the source text covered, write the two or three sentences this reader could say after looking at the figure for 30 seconds.
  If they do not contain the step 1 sentence, or contain something false, the figure fails for this reader even when every fact in it is correct.
  When someone else is around (the person who asked, a subagent given only the PNG and the reader level), ask them to retell it instead of guessing: their words are the measurement, yours are not.
- **Reading path (10 seconds)**: look at the figure as someone outside the field. Do you know where to start, in what order to read, and which side panel explains which part? Check the "Guiding the eye" rules in `references/visual-language.md`: numbered regions, one line from each explanation to its subject, plain gloss under each term, one concrete example under each abstract category, before/after for a change of state.
- **Coverage**: go down the fact list from step 2 of the workflow. Every actor is drawn, every main step has a mark, every alternative and error branch has its own frame, edge or node, and each branch label says the same condition as the source ("timeout", not "other error"). Add what is missing or state why it is left out.
- Cover the caption. Does the figure say the "the reader SEES ..." sentence written in step 1?
- **Drop the text**: imagine all text erased. Does the remaining structure suggest the idea, or is it just a row of identical boxes?
- **What is learned**: is there at least one real value (measurement, command name, key name, error code), or only generic labels? For a rough idea the test changes: are the concepts in the writer's own words, and does every arrow carry the relation the writer stated, not one you added?
- **One most prominent point**: where does the eye land first? Is that the main idea?
- **Writer recognizes it** (rough idea only): would the writer look at it and say "yes, that is what I meant", without you explaining? The tension from the idea list must be visible as a shape (two arrows pulling apart, a loop, a gap), not only written in a label.
- **Stranger**: what can a reader who has not read the source retell after 10 seconds with this figure? If you would have to say "ignore this part", delete that part.
- Does every arrow answer "what flows here, in which direction"?
- Is every label true? Check numbers and names against the lesson, do not trust memory.
- **The four misreads a held-out test caught** (13 figures on new content, one pass, 5 failed a strict fresh-eyes review):
  - A style in the key used for something outside it: "solid = liquid water", then the sun's heat drawn solid.
  - A placeholder where the real data belongs: `k → v` in a URL shortener's cache, with no URL anywhere in the figure.
  - A number that argues for a change but is not measured against today: "180 giờ tập trung" when the figure's own strip showed most of those hours were already free.
  - A reply dropped although a later step uses its value: `payUrl` appeared with nothing that returned it.
- **Pointers**: read each note, then follow its line. Does it end on the exact cell, box or edge the note talks about? A Heartbleed note about the claimed length pointed at the real payload cell next to it.

If this pass fails, change the figure type (go back to the table in SKILL.md), do not tweak coordinates.

## Fresh eyes: let someone who has not read the source look first

You wrote the figure, so you read into it what you meant.
A reviewer who has only the image shows what it actually says, and that is the check a team review did by hand on a correct security figure that a non-Java reader still could not follow.

Do it once the tool is clean and before you polish, for every figure meant for someone else.
When you can start a subagent (the Agent tool, or a second session), give it ONLY the light PNG and the reader level, never the source or your notes:

```text
You are <the reader from step 1, e.g. "a Java developer with little security background">.
Look only at the image at <absolute path to name-light.png>. You have not read any article about it.
Answer in <the figure's language>, briefly:
1. Where did your eye start, and in what order did you read the parts?
2. In one or two sentences, what does this figure say?
3. Which words or marks did you not understand?
4. Which part seemed unrelated to the rest?
```

Then compare:

- Answer 2 against the step 1 sentence. If it misses the point or says something false, the figure fails: change the structure (strategy, type, reading order), not the wording.
- Answer 1 against the order you intended. A different order means the badges, the joining arrows or the layout are missing (`references/visual-language.md`, "Guiding the eye").
- Answer 3: every term listed there gets a plain gloss or is replaced.
- Answer 4: that part gets a dashed arrow to what it explains, or goes.

Fix, render, and ask a NEW reviewer (the first one has now seen the answer).
With no subagent available, ask the person who gave the task the same four questions, or do it yourself with the source closed, knowing it is the weakest of the three.

## Pass 2: visible errors

The tool is silent about most of these; `references/lessons-from-runs.md` rules 14 to 20 list the ones that survived in test runs.

- Text clipped, overflowing a border, or overlapping other text.
- Arrow passing through a box, overlapping a label, or crossing another arrow.
- Arrow pointing at empty space or at the wrong shape.
- Floating label with no clear owner.
- X mark or check mark covering the name of the thing it marks.
- Things that should be evenly spaced are uneven; boxes with the same role are misaligned.
- Half the figure is cramped, the other half empty.
- Text too small: the summary line prints the smallest on-screen size. Below 12px the tool nudges and the figure must be tightened (stack vertically, drop a column, split). At 800 units wide, size-15 text shows at 12.5px and size 16 at 13.3px.
- An arrow so short that only its head shows: move the two shapes apart.
- Two nearly equal font sizes (17 and 18) look like a mistake: merge them.
- Unfinished elements: empty box, `?` label, draft note.
- Spelling errors in labels.

## Pass 3: dark theme and tool

- In `-dark.png`, all text is still readable and every stroke still visible.
- A `solid` fill in the dark theme does not swallow the text inside it.
- A thing whose real brightness is the point (a dark moth, a night sky, white paper) is still dark or light in `-dark.png`. If it flipped, it is drawn in a theme token: use `lit-dark` / `lit-light`.
- The tool prints no `✗` line. Every `•` line is fixed or has a clear reason to stay.

## When to stop

Stop when all three hold:

1. The figure says the step 1 sentence without a caption, to the reader named in step 1.
2. No pass 2 errors remain.
3. You can hand the figure to someone else without adding "except this bit".

It usually takes 2 to 4 rounds.
Do not stop after the first round just because there are no hard errors: the first-round layout can almost always be improved.

## Common errors and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Figure is a row of boxes joined by arrows, but the lesson is about a mechanism | Figure type chosen by habit | Go back to the figure type table |
| Figure is all text stacked in columns | It is a list, not a figure | Leave it in the text |
| Tiny text | Figure too wide | Stack vertically, split the figure, drop unrelated components |
| Every box is filled | Fill used as decoration | Remove all color, then fill exactly one thing |
| Two consecutive figures look identical | The new thing is not marked | Use `extends`: new thing `l4`, old things drop to `muted` automatically |
| Diamond or ellipse distorted or bloated | Text does not fit, so Excalidraw auto-expands the shape | Set `w`/`h` to twice the text |
| Arrow label overlaps both boxes | Arrow shorter than its label | Move the boxes apart, shorten the label, or turn it into a `note` |
| Axis ticks misaligned with cell edges | Ticks spread evenly along the axis length | Set `gap` to exactly one unit's width |
| Dozens of identical cells to type | Writing JSON by hand | Write a small script that generates the spec |
| Arrow winds around and cuts across the figure | Two related things placed far apart | Move them closer, do not bend the arrow |
| Figure needs three paragraphs to understand | Several ideas crammed into one figure | One figure, one idea: split it |
| Rough idea drawn as a mind map of every word | Concepts listed, relations skipped | Keep the 4 to 7 concepts on the main relation, label every edge with its verb, drop the rest |
| Concept map where every node links to every other | No claim chosen | Go back to the "This idea really says that" sentence, keep only edges that serve it |
| Reader asks "where do I start?" or "what does this panel have to do with that strip?" | Regions not ordered, explanations not joined | Badges ① ② ③ in story order, one dashed arrow from each panel to the part it explains |
| Reader nods at `object khác`, `dữ liệu nhạy cảm`, but the severity does not land | Abstract category with no instance | One real example from the source under the label |
| Every fact is right, and the reader still does not get it | The figure assumes terms the reader lacks | Step 1 term list: explain or replace each term, and for a newcomer switch to explainer mode |
| Figure is taller than one screen | One figure carries the whole story | Split where the tool's nudge says, or make a progressive series |
| Security figure reads like a how-to | Steps copied from an exploit write-up | Cut back to mechanism and defence (SKILL.md, "Security and other sensitive topics") |
