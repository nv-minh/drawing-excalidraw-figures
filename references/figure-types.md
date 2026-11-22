# Figure types: when to use, how to build, where they break

Contents: [1 Request flow](#1-request-flow) · [2 Anatomy](#2-anatomy) · [3 Byte cells](#3-byte-cells) · [4 Timeline](#4-timeline) · [5 Threshold](#5-threshold) · [6 Before and after](#6-before-and-after) · [7 Two views](#7-two-views) · [8 Physical metaphor](#8-physical-metaphor) · [9 Failure branch](#9-failure-branch) · [10 Decision tree](#10-decision-tree) · [11 Sequence](#11-sequence) · [12 State machine](#12-state-machine) · [13 ER and tables](#13-er-and-tables) · [14 Hash ring](#14-hash-ring) · [15 Code block](#15-code-block) · [16 Layer lanes](#16-layer-lanes) · [17 Progressive build](#17-progressive-build) · [18 Layer stack](#18-layer-stack) · [19 Curve](#19-curve) · [20 Icons](#20-icons) · [21 Sequence with fragments](#21-sequence-with-fragments) · [22 Business flow in swimlanes](#22-business-flow-in-swimlanes) · [23 Composite state](#23-composite-state) · [24 ER with crow's foot](#24-er-with-crows-foot) · [25 System design with two flows](#25-system-design-with-two-flows) · [26 Causal loop](#26-causal-loop) · [27 Matrix 2x2](#27-matrix-2x2) · [28 Funnel](#28-funnel) · [29 Concept map](#29-concept-map) · [Rare figure types](#rare-figure-types) · [Building a new figure from primitives](#building-a-new-figure-from-primitives)

Each section points to a file in `examples/`.
Copy that file, then edit it.

## 1 Request flow

**Use when** the point is who calls whom and in what order.
**Template:** `01-request-flow.json`.

- Left to right: client, gateway (tall narrow box), service, store.
- One request colored `hot` along its whole path, labels numbered `1.` `2.` `3.`.
- Dashed line for an async step, plus a `note` explaining the dashed line.
- Stores use `db`, queues use `queue`, clients with a UI use `window`.

**Common failure:** drawing every component of the system instead of only the ones this request passes through.
More than half of the source figures are this type, and most teach nothing beyond the box names.
Before choosing this type, check that the main point really is "who calls whom".

## 2 Anatomy

**Use when** the reader must see what is inside a thing: a process, a node, a data structure.
**Template:** `02-anatomy.json`.

- The outermost `frame` carries the name of the thing being dissected.
- Inside: `cells` for arrays, `box` filled `hachure` for each data element, arrows as pointers.
- Real values in cells: `user:1`, not `key`.
- `span` to mark sizes, `note` pointing at the surprising spot.
- Nest at most three levels, one title per level.

**Common failure:** the `cells` indexes touch the `frame` border.
Leave 60 units on the left when using `index` with `dir: "col"`.

**Ownership variant** (who may write which cell of shared memory: SPSC ring buffer, single-writer log, double buffer).
Put each owner as a full-width bar, one above and one below the shared `frame`, so every arrow is vertical and the cross reads never cross each other.
Each cell gets exactly one solid arrow, from its owner; the other side's reads are dashed arrows leaving the cell; a `legend` says solid is write, dashed is read.
Give each owner one accent and repeat it on the cells it owns: the eye then counts one color per cell.
Number the owner's writes `1 ·` `2 ·` when their order is the point (data before index), and put the "what if swapped" note in `err` right beside them.
Arrows entering cells from above and below collide with `index` numbers, so write the slot numbers as the cell `labels`.
A frame title would sit in the path of the vertical arrows: leave the `frame` untitled and write the name as free text in a gap between arrows.
Run that taught it: FE25 SPSC ring buffer (`fe25-spsc-hai-chu-so-huu`).

**Paged tree variant** (B-Tree against B+Tree, any tree whose node is a fixed-size page).
Draw every node as one `cells` strip of the SAME width: the page size is fixed, so how many keys fit in it is the fanout, and the reader counts it.
Keys are cells with real values; a value is an empty `l4` `hachure` cell, so "value takes room" reads as blue cells crowding keys out of the page.
Child pointers are `points` arrows leaving the bottom edge at the cell boundaries (`x + i × cw`), one per gap between keys, to the top centre of the child.
Write the fanout in words beside each root ("1 page: 2 khoá + 2 value, fanout 3") and add the real figure from the lesson once (Postgres ~407).
Two trees go one above the other with the roots at the same `x`, so the equal page width is visible without a bracket.
Sibling links between leaves: two single-head arrows in the gap, forward at a third of the leaf height and back at two thirds; a 35-unit gap is the minimum for the pair (one `both: true` arrow needs 64).
A range scan is `hot` on the key cells it returns plus the descent arrow; when the visit order matters (in-order walk up and down a B-Tree) number it with `badge`s under the leaf cells and above the root cell, not with return arrows that would lie on the pointer arrows.
A two-digit key at size 16 needs `cw` 32: at 28 Excalidraw wraps it and every cell grows taller.
Run that taught it: DBI2 B-Tree against B+Tree (`dbi2-btree-va-bplus-cung-mot-page`).

**Slot variant** (a cluster that hands out fixed resource units: Flink task slots, YARN containers, Kubernetes pods per node, worker threads per pool).
The coordinator goes on top as one frame holding the logical plan (operators as `stack` `n: 2` when the parallelism is 2), the workers below as frames side by side, each holding its units as a 2 × 2 grid of sharp boxes.
A used unit is an `l4` sharp box holding one hachure box per subtask with its real index (`source 1/2`); a free unit is a dashed `muted` box with the single word `rảnh`, so the reader counts used against free without a legend.
Leave the worker frames untitled and write each name as free text along their bottom edge: the assignment arrows come down from the coordinator and would run through a top-left title.
Put the used units under the coordinator's bottom edge so every assignment arrow is vertical, and start the units 40 units below the worker frame's top, or the arrowhead sits on the frame border (lint 2c).
State the count that is the point as one line under the figure (`2 task × song song 2 = 4 subtask, chỉ chiếm 2 slot`).
Run that taught it: SD53 Flink cluster (`sd53-slot-sharing-hai-task-manager`).

**Snapshot variant** (what a listing such as `KEYS`, `ls` or `SHOW TABLES` returns, when what it does NOT return is the lesson).
Stack two full-width frames: a solid `muted` frame for what the listing holds, a `dashed` `muted` frame under it for what the reader expects and does not find.
Inside the top frame group items by kind, one row per kind, with the kind on the second line of each sharp box; countable items (one key per job) go as a `cells` strip with their real names.
Inside the bottom frame draw each missing item as a dashed `muted` sharp box with the kind it would have, and write the reason under the group it covers (a `span` across several ghosts, a centred text under one).
Close the bottom frame with the consequence of the absence, the wrong conclusion in `err`.
Spend the accents on the surprise in each half (what stays that should not, the one item with a TTL), not on the frames.
Run that taught it: hang-doi 6.4 BullMQ keyspace (`bullmq-keyspace-co-mat-vang-mat`).

## 3 Byte cells

**Use when** the physical layout is the point: padding, alignment, header, page, packet, bits in an ID.
**Template:** `03-byte-cells.json`.

- `cells` with `widths` in true byte proportion (for example 10 units per byte).
- Wasted space colored `err` with `hachure` fill.
- Two strips stacked vertically to compare, same scale, same left edge.
- `axis` below with `gap` equal to exactly one step width so ticks align with cell edges.
- The saved space drawn as a dashed `node`-colored box right in the gap.

**Where one item sits, step by step** (a row version across the line pointers of a page, a slot reused after cleanup): one `cells` strip per step at the same x and `cw`, slot numbers as `index` on the top strip only, the step as a `muted` `badge` plus one line of text above its strip.
Live item `l4`, dead `muted` `soft` hachure, never-used and freed slots dashed `muted` (freed ones say so), and what a reader remembered as a 3-cell strip to the right of every step strip.
The match that fools the check is a heavy `err` `sharp` box drawn over the cell on the last step and a dashed one over the same cell on the first step; the verdict of each check is a box below in the color of its outcome (thiet-ke-mau-thiet-ke 2.3 run, `tranh-chap-ctid-quay-ve-ngan-cu`).

**A command that walks a structure in passes** (`SCAN`, `XAUTOCLAIM`, any call that returns a cursor): one `cells` strip per snapshot at the same x and `widths`, the full command of each pass in `mono` with an `l4` `badge` between two strips, and the cells that pass changed in `l4` fill.
The returned cursor is a vertical `l4` arrow from the cell it names in one snapshot to the same cell in the next, labelled beside its upper half, so the reader sees that the next pass starts there; a `span` above the strip measures what `COUNT` took, and the pass that returns `0-0` ends in one `node` line.
Write in each cell what the pass changes (owner, delivery count), and label a snapshot the lab did not run as such under its row name (hang-doi 5.1 run, `nhan-lai-tin-autoclaim-con-tro-tung-luot`).

**A dedup store that was cleaned** (inbox table, seen-id set, any window of remembered keys): two columns side by side, the store as one `cells` strip of ids per column at the same `cw`, cleaned slots dashed `muted` empty with `span`s under them naming the cleanup and what is kept, and the cleanup command once in `mono` under the column title.
The late duplicate is the same `l4` box above both strips: in the kept column its arrow stops on the id's cell (`l4` fill), in the cleaned column a `points` arrow runs straight through the empty slot to an `err` verdict box, so the "slipped through" needs no label (accept the "crosses shape" nudge for that one arrow).
Under each verdict the effect table as a second strip, with the extra effect appended as one `err` cell; the rule for the window length goes in one muted line under both columns (thiet-ke-mau-thiet-ke 3.7 run, `nhieu-buoc-hop-thu-don-lot-ban-trung`).

**Each partition cuts its own top-N, a coordinator merges** (Elasticsearch `terms` with `shard_size`, per-shard `LIMIT`, distributed top-k): one row per partition, its sorted values as `key count` cells, split into TWO `cells` strips at the cut with a 30-unit gap or more, and the cut drawn as a dashed `l4` vertical `line` in that gap with the setting name above it.
A cut line laid on a shared cell border merges with the cell strokes and reads as one thick border (round 1 of the run below).
Values past the cut are dashed `muted`, except the ones whose absence makes a returned total wrong, which are dashed `err`.
A value the cut defines (the count just before it, the per-partition error bound) gets its label right after its cell and BEFORE the cut line; placed past the unsent strip it read as part of what was not sent.
The coordinator is a `table` below with one column per partition, a plain `-` in a dashed `err` cell where a partition sent nothing, then merged total, true total and bound columns, so the reader matches each red `-` to the red cell above by column (thiet-ke-cong-nghe 2.8 run, `tim-kiem-vach-cat-giau-so-dem`).

**A lookup through a sparse index** (Kafka `.index` into `.log`, an SSTable index block, any "binary search, then scan").
Stack one strip per file, top to bottom in lookup order, each step a `badge` with its rule as one line above its strip.
The index is a contiguous strip of narrow two-line cells (key over position) and the data file a wider strip of blocks with `widths` in byte proportion, so the reader sees a small dense array pointing into a large file.
Draw one `points` arrow per visible index entry from the cell's bottom centre to the START of the block it names: they fan out, and the gap between two heads is the sparseness; only the entry the search found is `l4`, the others `muted`.
Measure that gap with a `span` under the data strip whose text subtracts the two positions shown in the index cells and compares the result to the interval setting, so the reader derives the spacing instead of trusting it.
The scan is a short `l4` arrow beside the span at the same y, from the found block to the block holding the key (filled `l4`), with the blocks it passes stroked `l4`.
Put a step heading LEFT of the data strip, not above it: the fan of arrows crosses any text in the band between the two strips (thiet-ke-cong-nghe 3.x run, `luong-su-kien-tra-offset-qua-ba-tep`).

**Common failure:** a one-byte cell is too narrow to hold text.
Increase the scale, or leave the cell empty and name it with a `note`.

## 4 Timeline

**Use when** duration, order or the gap between two events is the point: latency, timeout, window, lock, race.
**Template:** `04-timeline.json`.

- `axis` at the bottom, with a unit.
- One horizontal lane per participant, lane name as bare text on the left.
- A lasting activity is a `box` whose width equals its duration. An instantaneous event is a `badge` or a small dot.
- The dangerous interval is measured with an `err`-colored `span`.
- A moment that cuts across lanes (timeout, deadline, expiry) is a dashed vertical `line` at axis `x` + n × `gap`, labelled at its top with the real setting (`connectionTimeoutMillis = 2000`).
- When the count matters (10 hold, 4 wait), draw one thin bar per item so it can be counted; generate them with a script.
- Diagonal arrows between two lanes are request and response.

**Comparing two modes on the same scenario** (two isolation levels, with and without retry): draw two parallel axes on the same scale, and put the shared event (the other transaction commits, a node dies) in the gap between them with one arrow pointing up and one pointing down.
Under each mark put what is observed as real values (`cells` of the visible rows, `count = 3`), and color only the exact spot where the two lanes differ.
**Two orders of the same two steps** (subscribe then read the log, or the reverse; lock then check, or the reverse): one block per order, stacked, each step a `sharp` box at the same x in both blocks, so the only change is which label sits in which box.
The gap between the two boxes is the same `span` in both blocks, and the one event that falls in it is a dashed `l4` vertical guide through both blocks, labelled once at its top with what happens there.
Mark the outcome on the guide in each block (`cross` where nobody receives it, `check` where it arrives), and put what the client ends up holding as a `cells` strip under each block: the lost item as a dashed `err` cell, the duplicate as a dashed `muted` cell after the real one.
Keep every free text 6+ units off the guide's x; the tool now flags a `line` through text (thiet-ke-mau-thiet-ke 1.3 run).
When the thing that misses the event is a one-shot registration held by the server (a ZooKeeper watch, a one-time subscription), give it its own thin lane under the client lane and draw each stretch where it is armed as a `weight` 4 `l4` segment that starts at the right edge of the call box that sets it.
The reader then sees the guide cross an empty stretch of that lane in one block and an armed one in the other, which says why without a word; mark each firing with a small `ellipse` on the lane and a dashed `muted` `points` arrow up to the call it triggers (thiet-ke-cong-nghe 5.1 run, `dieu-phoi-watch-khe-giua-doc-va-dat`).

**Two detectors, two failures** (heartbeat vs poll timeout, liveness vs readiness probe): one block per failure scenario, stacked on one shared axis, with the same lanes in each block (one lane per thread or clock).
A periodic signal (a ping every 3 s) is a comb of `weight` 1 `line`s at its true spacing, generated by a script; 5 units apart still reads as "steady", and where the comb stops is the failure.
Each block ends at its own dashed `err` line labelled with the setting that fires, and an `err` `span` measures the detection delay from the last signal to that line; the block where the signal keeps flowing shows why the other detector is blind (mq1 run).
A comb of 100+ marks (a retry every second for two minutes) is one `line` with `sharp: true` whose points pulse `(x, base) → (x, top) → (x, base)` per mark: it draws the same comb as one element instead of 120, and the true spacing still shows the backoff bunching at the start (thiet-ke-cong-nghe 3.2 run, `luong-su-kien-hai-phut-producer-im-lang`).

**A clock that moves with the data** (watermark, low-water mark, replication lag): rows top to bottom in arrival order, `x` = the data's own time on a true scale, one dot per arrival with its timestamp in a left column and what happened in a right column.
The clock is one `l4` staircase `line` (`sharp`), stepping right between rows only when it advances, so an event left of the staircase on its row is late and one right of it is on time; the reader sees lateness without a word.
The states the clock drives (Open, Grace, Closed) are a band of adjacent `sharp` boxes above the rows, each spanning the clock range that holds it, with thin dashed `line` guides down from the band borders so the step that crosses a border is the transition.
Pick timestamps that keep dots 6+ units off the guides, and put the clock's rule (`max đã thấy − 10s`) on its longest horizontal step (sd53 watermark run).

**One item through the containers that hold it, read by snapshots** (a job through the Redis keys of its states, a row through buffer, WAL and page): one `lanes` row per container with its type and count command in the label, the item as a staircase of `sharp` boxes with no arrows (boxes meet at corners, so the transition is the edge), and the command that put it there written inside each box.
Each read is a dashed vertical `line` placed 10 to 12 units inside the right edge of a box, clear of the centred text, and what the read counts the item as goes under the lanes at that `x`; the one read the source records is the only `l4` line (hang-doi 6.2 run, `bullmq-mot-job-qua-nam-key`).

**How long a lock lives across network round trips** (pessimistic vs conditional UPDATE vs one statement): one block per approach on one shared ms axis, each block two thin lanes (`app` above, `DB` below) with every statement drawn as a V of two `points` arrows, down to the DB lane at arrival and back up at reply, the statement name centred above the V in `mono`.
The lock is a `sharp` `l4` box on the DB lane from the arrival that takes it to the COMMIT arrival that frees it, with an `l4` `span` 22 units below the lane giving its length; where the check runs is a 16-unit `diamond` on its lane, `node` inside the lock and `err` outside it.
Generate the blocks with a script from (statement, send time) pairs so every V sits on the true scale; a 1 ms lock is then 6 units wide, which is the point, so draw that box after the diamond it would hide (thiet-ke-mau-thiet-ke 2.1 run, `tranh-chap-khoa-giu-qua-vong-mang`).

**When the loser finds out** (check-then-pay vs hold-then-pay, any race where the fix moves the moment of contention): one block per approach on one shared axis, one thin lane per party with its long human step (pay, type the OTP) as a `sharp` `muted` box, and a bottom lane that is the contested row itself as a `cells` strip whose `widths` change exactly at the write that changes it (`trống` until B's `UPDATE`, then `ban = true (B)`).
Each statement is a `mono` label above its party's box (left-aligned at the start, right-aligned at the end) with its row count (`0 hàng`, `1 hàng`); the `cross`/`check` sits just right of the box end and the outcome text starts 34+ units past it.
The losing party's whole window is an `err` `span` under the strip in the first block; in the second block the loser has no box at all, only an `l4` diamond at the click and the message it gets, and the held row is the one `l4` cell (thiet-ke-mau-thiet-ke 2.4 run, `tranh-chap-giu-cho-doi-luc-thua`).

**Where the next task waits after a worker dies** (sticky queue, partition owned by a dead consumer, lease held by a dead node): a shared top `lanes` block for what does not change with the setting (the dead worker with a `cross`, the server lane holding the durable state), then one block per setting value with the same three lanes (queue of the dead worker, shared queue, new worker).
The task is a staircase of `sharp` boxes: a `warn` box in the dead worker's queue whose width is the timeout, with a `span` under it giving the value, then a box in the shared queue, then a `node` box on the new worker; when the hand-off is instant, replace the middle box with a `sharp` elbow arrow leaving the right edge of the `warn` box, never a vertical arrow from its bottom, which runs through the span's end tick.
The new worker's idle time is a dashed `muted` box, and the empty shared queue gets one `muted` line saying it is empty while the worker polls; that empty lane is the point.
Badge the moments (`muted`, d 24) and explain them in a numbered list under the axis, so no event label has to squeeze between two moments 2 s apart (thiet-ke-mau-thiet-ke 3.9 run, `nhieu-buoc-luot-chay-ket-o-hang-doi-rieng`).

**How long a copy stays stale** (cache TTL vs invalidate-on-write vs lost invalidation, replica lag, any copy that trails its source): one `cells` strip on top for the source with one cell per version, then one block per approach holding the copy as a staircase of `sharp` boxes on the same x scale, the stale part `err` hachure under the source cell that already moved on.
Draw the reads as a comb of short vertical `line`s above each copy at one spacing, colored by what each read got (`muted` fresh, `err` stale, `ink` and taller for a miss that reloads), so the stale share is countable and the early miss an invalidation costs is visible; key the comb once with hand-built line + text pairs, since `legend` lines are horizontal.
The write and the expiry are dashed guides as per-block segments that stop above each block's `span`, so the span label under the box never meets a guide; a block where the expiry no longer matters simply has no expiry guide.
When the failure case (the invalidation is lost) gives the same picture as the baseline, draw it as its own block anyway: the identical shape is the lesson (thiet-ke-mau-thiet-ke 4.3 run, `doc-nhieu-mot-khoa-ba-cua-so-cu`).

**Variants:** tumbling, sliding and session windows are staggered bars on one axis; a rate limiter is squares stacked on the axis with a dashed threshold line.

**Common failure:** bars not drawn to the axis scale.
Compute `x` and `w` from the axis `gap`.

## 5 Threshold

**Use when** a limit is exceeded: capacity, SLO, quota, hot key.
**Template:** `05-threshold.json`.

- `plot` with `bars` and one `thresholds`.
- Normal bars colored `l2`, only the bar over the threshold colored `err`.
- Real name on top of the bar over the threshold (`user:celeb`).
- The vertical axis has a unit.

**Common failure:** coloring every bar differently.
Only the problem bar gets a color.

## 6 Before and after

**Use when** the lesson lies in exactly one change.
**Template:** `06-before-after.json`.

- Draw the frame once, then use `group` with `dx` and `prefix` to draw the second copy.
- The "after" copy uses `dim: true` for the unchanged part, and colors the changed part `l4`.
- A thin dashed `line` splits the two halves, each half titled with bare text.
- Only one thing changes. Two changes means two figure pairs.

**Strongest variant** in the sources: two identical figures where only the red moves, from three hops down to one bypass.

**Common failure:** the two halves do not share coordinates, so the eye cannot compare them.
`group` + `dx` removes this error.

**Variant: a node moves (query plan rewrite, predicate pushdown).** `group` + `dx` does not fit when the change is a node changing level, so write both trees with absolute coordinates, one `y` per tree level shared by both halves (dbi4 run).
- Data flows from the leaves up to the root: arrows point up, and the row count sits on each edge as a free label (`labelDx` about 45 off the line).
- Volume is stroke weight: `weight` 4 for millions of rows, 2 for thousands, so the bill reads before the numbers do.
- In the after tree, leave a dashed `muted` ghost box where the node used to be ("Filter / đã chìm xuống"), off the main axis, with a dashed `l4` arrow down to the leaf that now carries the condition.
- Both roots end in the same bare result text at the same `y`; a `text` is not an arrow target, so those last arrows use `points`.

**Variant: a check in code against a constraint in the schema (tenant FK, CHECK, UNIQUE).** The two halves stack top and bottom, not side by side, so each row of entry paths has the full width (td5 run).
- One box per path into the table (endpoint, helper, `psql`/seed), each with its reason as a second line ("người mới, quên check"); the code check is a box on the one path that has it, and that arrow ends there.
- The paths that skip it run straight into the rows they write: the table sits so its rows line up with the paths, `err` filled rows with illustrative ids.
- In the after half, dim the unchanged boxes and add one tall `node` bar in front of the table spanning every path; each arrow stops on it at its own height, with the error code (`23503`) as text right of the bar, and the table rows `dashed` `muted` and empty.
- One outcome line under each half carries the "so what": silent cross-tenant rows against an error with a status and a log.

**Variant: a key too coarse merges rows (upsert or dedup on part of an id).** The halves stack top and bottom with the source strip at the same x and `cw`, dimmed in the after half (hang-doi 3.1 run).
- Draw the before table as `cells` strips with `dir: "col"` and `widths` = rows sharing the key × source `ch`, so each target row is exactly as tall as the source rows that land in it and every arrow stays horizontal (`points` from the strip edge to the table edge at each source row centre).
- Several horizontal arrows into one tall cell is the merge; a `table` with equal rows forces converging slanted arrows whose heads crowd one spot.
- Overwritten writes are `dashed` `err`, the write that survives is `ink`, and a short `err` text right of each merged row names what was overwritten.
- The after half is a normal `table` with `rh` equal to the source `ch` and its header one row above the strip, so its rows line up one to one with the source.
- Write the clause that does the silent overwrite verbatim once (`ON CONFLICT (...) DO UPDATE`), and one outcome line per half ("5 entry vào, 2 dòng ra").

**Variant: a victim behind duplicates in a shared pool (stampede, retry storm, fan-out into one connection pool).** The halves stack top and bottom with the same x for the sources, the queue and the pool (thiet-ke-mau-thiet-ke 4.4 run).
- Two sources in the left column: the flood (top, its arrow drops onto the middle of the queue from above) and the unrelated traffic (bottom, its arrow enters the queue tail from the left).
- The queue is one `cells` strip with the head on the right next to the pool: the victim is the tail cell in `err`, the duplicates `warn` with one `…` cell for the bulk; duplicates whose caller already gave up are `dashed`, explained in one `muted` line.
- The pool is a `grid` with one cell per slot, so "full" and "8 of 16" are counted, not read.
- Put the wait as an `err` `span` under the cells ahead of the victim, with the estimate written as its arithmetic on two centred lines.
- The after half drops the queue: the coalesced arrow goes straight into the pool, the victim's arrow lands on an empty slot row, and the price of coalescing goes as one `muted` line.

## 7 Two views

**Use when** a structure has two representations: space and tree, table and index, logical and physical.
**Template:** `07-two-views.json`.

- Two views side by side, separated by a clear gap.
- The same entity has the same color and the same name in both views. This is the whole technique.
- Dashed `frame` for bounding regions, `tree` for the tree.

**Common failure:** using different colors in the two views, so the reader cannot connect them.

**Paired ladders variant** (two scales whose rungs match one to one: CPU memory model and distributed consistency, isolation level and anomaly).
One color per pair spends the whole three-accent cap on decoration, so keep the rungs `ink` and let position carry the pairing instead.
Put each pair on one row and join it with a dashed two-headed `l4` arrow that names what the two rungs share.
The direction the whole ladder runs (faster, weaker, harder to reason about) goes on one vertical `muted` arrow beside the columns, not repeated on every rung.
Box with the rung name at `valign: "top"` plus a centered `muted` text inside for the one-line meaning keeps the name readable at a glance.
Run that taught it: A3 memory model ladder (`ba3-hai-thang-nhat-quan`).

**Same items, two engines variant** (one version chain stored two ways: PostgreSQL O2N against InnoDB N2O, copy against delta, heap against log).
Stack the two engines as two dashed `frame`s, one above the other, and give each item its own column in BOTH frames, named once above the top frame ("bản của txn 205").
The reader then compares column by column, and arrows that run in opposite directions (`t_ctid` rightward, `roll_ptr` leftward) carry the difference without a word.
Draw each stored record as a vertical `cells` strip with its real fields (`xmin=205`, `bal=900`), header fields filled `soft`; a delta record simply has fewer cells, bottom-aligned with the full row so its pointer cell lines up with the row's.
The entry point (index, clustered-index lookup) is an `l4` box above the strip it enters: it shows which end of the chain a reader starts from.
Show the cost per reader: a short `muted` `span` for the reader that stops at the entry, and a long `hot` `points` arrow in the walking direction for the reader that walks the whole chain, with its count as text ("xét cả 3 bản, đi 2 lần roll_ptr"); fill `hot` the cell that reader finally returns.
A nested frame (undo log) whose border sits near a pointer's head cuts the head: keep its border 25+ units clear of the strip the pointer lands on.
Run that taught it: DBI3 O2N against N2O (`dbi3-o2n-n2o-ba-ban`).

**One list, several numberings variant** (0-based index against displayed position, forward against reverse rank, offset against line number).
Draw the list once as a `table`, one column per numbering, with the direction in the header (`ZRANK ↑`, `ZREVRANK ↓`), so every row shows all numbers side by side and no arrow is needed.
An off-by-one condition is a pair of `sharp` `line` brackets right of the table, 14+ units clear of its edge: the wrong one (`err`) inner and longer, the right one (`node`) outer and shorter, each with the condition in `mono` beside it; the wrong bracket's label sits under the end of the right one so neither label crosses a bracket.
Fill the row at the edge `l4` and the extra row the wrong condition lets in `err`; the conversion formula goes in one muted line under the table (hang-doi 10.2 run, `ra-khoi-khoa-rank-chi-so-hai-chieu`).

**Same keys, two sort orders variant** (collation against byte order, `text_ops` against `text_pattern_ops`, signed against unsigned).
Draw the same five or six keys twice as vertical `cells` strips side by side, split by a thin dashed `line`, each titled with the order and one `muted` line saying the rule ("chữ HOA đứng trước mọi chữ thường").
Pick example keys so the decisive difference is a letter at the same position in every key; punctuation that some collations ignore then cannot change the order you claim.
Fill the keys that match the predicate `l4` in both strips; in the order that fails, a sharp `err` `[` bracket from the first to the last match shows the stranger in between, and in the order that works a `node` bracket covers the contiguous run plus a `weight` 4 box on the first key past it (where the scan stops).
Under each strip goes one outcome line; under the working one, the bounds verbatim in `mono` as EXPLAIN prints them (`Index Cond: email ~>=~ 'user123'`). Label the keys as examples (postgres 2.5 run, `index-like-tien-to-dai-lien`).

## 8 Physical metaphor

**Use when** the reader needs an intuition before the mechanism: token bucket, leaky bucket, Bloom filter, backpressure, funnel.
**Template:** `08-metaphor-token-bucket.json`.

- Build the real object from `line` with `closed: true`: a bucket is a trapezoid, a funnel is a truncated triangle.
- Countable things are small `ellipse` shapes filled `hachure`.
- Three short notes carry the whole rule: how things enter, how they leave, what happens when full.

**Common failure:** a forced metaphor.
Use it only when the real object behaves exactly like the mechanism.

## 9 Failure branch

**Use when** the lesson covers the places where a process can break: saga, multi-step workflow, retry.
**Template:** `09-failure-branch.json`.

- The happy path is a `row` of black boxes joined by black arrows.
- Each possible failure point hangs off a dashed `err`-colored `diamond`, staggered above and below so they do not collide.
- The failure cause is the label on the dashed arrow.

**Common failure:** the diamond is too small for its text.
Make it twice as wide as the text.

**Variant "saga: compensate backwards, then the point of no return"** (thiet-ke-mau-thiet-ke 3.4 run).
The diamonds of the template ask "hoàn tiền?" but cannot show that compensation runs in reverse order, so for a saga use two rows instead.
- Top row: the forward steps, one column per system (a muted `span` above each column names the system, one `span` across two columns when one system owns two steps), each box holding the real operation (`ton = ton − 1`).
- Bottom row: each step's compensation directly under it, `l4`, with the real operation (`ton = ton + 1`, `khoá = mã đơn`); steps with none get a dashed `muted` ghost ("không bù được").
- The failing step gets a `cross` at its corner and one dashed `err` arrow down to the compensation of the step before it; then `l4` arrows run right to left with `badge` 1, 2 for the order.
- The failed step's own compensation stays dashed `l4` with one muted line saying why it does not run.
- The pivot is one dashed `warn` vertical line between the last compensable step and the first that is not, labelled beside the line; one line of text on each side at the bottom says "bù ngược" and "chỉ tiến tới".
- End nodes for both outcomes go under their last box, not to the right, so the row stays under 780 units.

## 10 Decision tree

**Use when** the reader must choose between options.
**Template:** `10-decision-tree.json`.

- `tree` with `shape: "diamond"` nodes for questions, `box` for leaves.
- `có` / `không` labels sit on the edges (`edge`).
- Leaves are concrete technology names, filled so they stand out.
- At most three levels of questions.

**Common failure:** `nh` is smaller than the diamond, so levels overlap.
Set `nh` to the diamond height, and give leaves their own smaller `h`.

## 11 Sequence

**Use when** the message order between two to four parties is the point: handshake, retry, timeout, protocol.
**Template:** `11-sequence.json`.

- At most four parties in the site column. More than that overflows the width: split by scenario, or see section 21 for the off-site case.
- Branches (`alt`), optional parts (`opt`), retries (`loop`): section 21.
- Solid line is a call, dashed line is a reply.
- A full-width `note` states the condition that causes the incident, colored `err`.
- `fail: true` marks a failed message.
- `n` numbers messages when the lesson refers to "step 2".

**Common failure:** a label longer than the distance between two lifelines.
Increase `gap`.
With four actors the column fits only about `gap` 215: write long actor names on two lines (`"Role app-admin\naccount 456"`), and move a long identifier off the message into a one-line `note` right under the call (`đích: arn:aws:iam::456:role/app-admin` under the label `assume-role`).
A Mermaid `Note over S` with several `<br/>` lines becomes one multi-line `note` whose `over` spans S and its neighbour, since a note over one lifeline is only 80 wide.
Run that taught it: AWS 1 role chain (`aws1-chuoi-assume-role-bi-tu-choi`).
Six actors on a hot read path (browser, edge, service, cache, store, queue) do not fit any `gap`: draw a request flow instead, number the steps for order, put key names in the store labels (`Redis\nlink:aB3xK9p`) so arrow labels stay short (`3. GET → nil`), and give the async step a dashed arrow numbered after the reply.
Run: ds-3 hot path (`ds3-duong-nong-redirect`, was a 6-actor Mermaid at 7.3px).

**Activation bars** (a worker frozen, a worker still busy while another acts) are not drawn by the macro.
Render once, read the message y values and the lifeline x from the `.excalidraw`, then add a 14-wide `box` centred on the lifeline.
List the bars BEFORE the `sequence` element so notes and arrows draw over them; listed after, a bar covered the state note it crossed.
A frozen span reads well as `muted` with `fillStyle: hachure`, a busy span as `ink` with `fill: soft`, each with a short free label beside it.
Run: thiet-ke-mau-thiet-ke 7.2 (`viec-dai-rao-hoi-sai-noi`, A frozen while B holds the lease).

**A race window across lifelines** (check-then-act where another party's commands land between the check and the act): a `sharp` `dashed` `warn` box with `fill` `warn` behind every lifeline, from just above the check's label to just below the act's arrow, listed BEFORE the `sequence` element so the messages draw over it.
The other party's messages that fall inside the box are the bug; one free text beside the last lifeline says what lands in the window, and the fix goes in an `alt`/`else` right after the act.
Give the box `opacity` 45: at full opacity the `warn` fill turned into a heavy brown slab in the dark PNG and took the eye off the messages; `opacity` also lightens the dashed border, which still reads.
Run: thiet-ke-cong-nghe 4.2 (`bo-nho-nhanh-khoa-nx-tinh-hai-lan`, B's `GET` and `SET NX` with A's `SET` and `DEL` between them).

## 12 State machine

**Use when** a thing changes state on events: circuit breaker, connection, order, lock.
**Template:** `12-state-machine.json`.

- A state is a filled rounded `box`, colored by meaning (`node` healthy, `err` broken, `warn` probing).
- The transition condition is the label on the arrow.
- Both directions between two states: two arrows with the same `bend` value.
- Self-loop: `from` equals `to`.
- Lay out as a triangle or a ring, not a horizontal row: a row hides the loop.
- Lifecycles with a start, terminal states or nested states: section 23.
- Two states only (on/off): write a sentence or a table, not a diagram.

## 13 ER and tables

**Use when** the relations between tables, or the concrete data in a table, is the point: index, join, foreign key, partition key.
**Template:** `13-er-table.json`.

- `entity` for structure, `table` for real data.
- Cardinality is the label on the edge (`1 - N`), and the edge has no arrowhead.
- Color exactly the rows the query refers to.
- List only the relevant columns.
- Crow's foot ends instead of `1 - N` labels: section 24.

**Variant:** a main table and its index, key column filled `hachure`, non-projected cells left empty in `muted`.
**Variant:** a column copied from another table (denormalized snapshot, cached total).
Stack the two `table`s and give the source the same column widths as the copy, so the foreign key and each copy are parallel vertical edges between header cells (`<id>.h.<col>`).
Fill the copied cells, and add one row from before and one from after the source changed so the two values differ on screen (run `be05-ban-sao-dong-bang`).
**Variant:** a key shared by two tables (Class Table Inheritance, 1:1 extension table).
Draw the parent and child as `table`s with real rows and join row to row (`p.0` to `c.0`) with `one` / `zero-one` ends, filling the key cell on both sides: the same value 7 on both ends is the whole point.
Order the parent rows by child table so the row edges never cross (run `td2-khoa-chung-bang-con`).
**Variant:** one table per query (query-first modelling, partition and sort keys).
Stack the tables, each with the query it serves as a `code` block on its left, all blocks at the same `w`.
Draw one short horizontal `l4` arrow from each `WHERE` / `ORDER BY` line to the row it uses (`fromAt` from the line formula in spec.md `code`, `toAt` inside the row), fill the partition key row `l4` solid and the sort key row `l4` hachure.
Put the table every other one relates to in the middle so the ER edges between them stay short and vertical (run `ds3-ba-bang-ba-truy-van`).
**Variant:** a table that stores a derived structure (closure table, adjacency list, path column).
Draw the structure itself (`tree` with `lines: true`) beside the `table` of its rows, pick one node, fill that node and exactly the rows it owns, and draw the pairs that exist only in the table as dashed edges in the same accent, self pairs as a small loop (run `td2-closure-table-cay-va-cap`).

## 14 Hash ring

**Use when** the topic is consistent hashing, ring partitioning, token ring.
**Template:** `14-hash-ring.json`.

- `ring` with `ticks` as numbers on the ring, `nodes` as machines, `arcs` as the affected key range.
- Dead node: `err` color, `dashed`, with a `cross` placed next to it.
- `steps` on the right tells what happens.

**Common failure:** an arc label lands on a tick label.
Remove some ticks.

**Variant: same node dies, without and with vnodes (sd09 run).** Two rings side by side at the same `r` and `cy`, a dashed divider between them.
- Left ring: one node per server at four angles; right ring: three vnodes per server, 12 nodes every 30 degrees with `d` 22, ordered so each dead vnode is followed by a different survivor.
- Each moved range is an `arc` from the previous node to the dead node, labelled "→ DB3"; the node that receives it gets `warn` fill, so arc and receiver read as one color.
- Dead nodes: `err` dashed node with a small `cross` (size 14) centred on the disc; no text is under it.
- Under each ring, one bar row per survivor: own share as a `soft` box, the absorbed share as a `warn` box appended at the same scale, and the sum written out ("25 + 25 = 50%", "25 + 8,3 ≈ 33%"). The doubled bar carries "gánh gấp đôi" before any number does.
- A tick may share a node's angle (positions 0, 25, 50, 75): the tool moves that tick label inward past the node disc.

## 15 Code block

**Use when** the real thing (payload, header, command, config) is more convincing than any box.
**Template:** `15-code-evidence.json`.

- `code` holds exactly the snippet under discussion, 2 to 6 lines.
- A `note` points at the block and says what the code line does not say by itself.
- Two blocks, one above the other, for a request and response pair.

**Common failure:** putting a whole function into the figure.
Long code belongs in the lesson.

**Variant: run it again (idempotency, imperative against declarative, retry).** Two columns, one per approach, and one row per run, so "lần 2" of both sits on the same `y` (infra2 run).
- Row 0 is the source (`script.sh`, `main.tf`) with the same line count in both columns; pad the shorter one with real lines (`set -e`) instead of leaving a gap.
- Each run is its own `code` block titled with its number and command (`lần 2 · terraform apply`) and holding the tool's real output (`No changes.`, `(DBInstanceAlreadyExists)`), not a box that says "lỗi".
- Color the run blocks by border: `err` for the run that breaks, `node` for the run that stays silent, `l4` for a diff worth reading; one short line of the same color under each says the result in words.
- The reason a run behaves that way ("mỗi lần chạy: đọc state, hỏi API thật") is one `muted` line between the source and run 1, not an arrow.
- No arrows between runs: the row order already is the time axis.

## 16 Layer lanes

**Use when** the reader must see what happens at which layer: application, kernel, disk; client, edge, origin.
**Template:** `16-layer-lanes.json`.

- `lanes` as the background, elements placed on top with normal coordinates.
- An operation crosses the lanes as an arrow.
- An incident note points at the exact lane where it happens.

**Mirrored variant** (send and receive, request and response through the same layers): one column per direction over shared lanes, arrows down in one column and up in the other, a dashed `line` between the columns.
The lane where each column changes form (cut, merge, encode, decrypt) is the point of the figure: put the two change boxes in different lanes when the source does, and keep one accent for the form the upper layers see.
Many small units next to one big unit: generate a comb of thin vertical `line` strokes with a script, exactly as wide as the single block it becomes, so equal width reads as equal bytes.
A comb has no id, so aim arrows at it with `points`.
Run that taught it: A2 offload figure, TSO cuts 45 segments at the NIC while GRO merges them in the NAPI poll (`ba2-tso-gro-mot-sk-buff`).

**Columns variant** (one operation through the subsystems of one engine, five or more steps: an UPDATE through buffer manager, concurrency control and recovery manager).
Horizontal lanes with steps left to right run out of width after four steps, so turn the lanes into columns with the `swimlane` macro (`laneW` about 250, nodes 236 wide at size 16) and let time read downward.
Number the steps `①` `②` in the node text and give each step the real value it leaves behind (`pageLSN = A7B3`, `xmax = 42`); a later step that only depends on the operation, not on the step before it, shares a row with it.
The main path is `hot`; the edges that hand a value to another column carry that value as their label (`LSN A7B3`, `dirty`), which is the point of the figure.
A concurrent actor (a reader in another transaction) is a node in the column it touches, reached by a dashed edge, not a step of the main path.
Two steps that are deliberately unordered (commit and page flush under NO-FORCE) get no edge between them; one line under the figure says why.
Run that taught it: DBI3 hero (`dbi3-mot-update-ba-he-con`).

## 17 Progressive build

**Use when** a system grows across several sections of the lesson.
**Template:** `17a-progressive-1.json` then `17b-progressive-2.json`.

- The later figure `extends` the earlier one. Old parts drop to `muted` automatically, new parts are colored `l4`.
- Each step adds one to three things.
- Do not move old things.
- This is Hello Interview's main teaching technique, but they do not mark what is new, so the reader has to hunt for it. `extends` fixes exactly that weakness.

**Common failure:** by step five the figure is too wide and the text too small.
At that point split off a zoomed-in figure for the part under discussion.

## 18 Layer stack

**Use when** layers sit on top of each other: OSI, VM and container, storage engine.
**Template:** `18-layer-stack.json`.

- `cells` with `dir: "col"`.
- Two stacks side by side to compare, with differing layers colored.
- Stack height is itself information: a shorter stack has fewer layers.
- Variant "layers that hold members" (a reading map, a curriculum, a module map): one `sharp` box per layer, touching the next, name at top-left, members as a `cells` strip in the same row and one muted line of what they cover below.
  Start every strip at the same `x` and keep one `cw`, so strip length counts the members of each layer.
  A layer that feeds the next stage gets a gap and one arrow; put that arrow's label beside it with `labelDx`, since a 56-unit vertical arrow broken by its label shows only a stub.
  A feedback arrow back into "one of these layers" ends on a `line` bracket (`[`-shaped, 8 units deep) beside the stack, not on one band, or it says only that band.
  Run: SD 01 set map (`sd01-ban-do-set-ba-lop`).

## 19 Curve

**Use when** the shape of a distribution or trend is the point: p99 tail, long tail, growth.
**Template:** `19-curve.json`.

- `plot` with `lines`, `xticks`, and `thresholds` for the SLO.
- Axes have names and units.
- One `note` says what the curve shows.

For exact data with many points use the site's `echarts`, not a hand-drawn figure.
Hand-drawn figures are for the SHAPE of the curve.

## 20 Icons

**Use when** a familiar shape reads faster than text: user, firewall, key, clock, mail.
**Template:** `20-icon.json`.

- `python3 scripts/ve.py --icons` lists them.
- At most 4 to 5 icon kinds per figure.
- An icon always has a text label below it.
- Main system components (store, queue, service) use the tool's `db` `queue` `pipe` `box`, not icons: they are bigger, clearer, and bind to arrows better.
- **Cloud deployment figures** are the exception: when the lesson is about which cloud service does what, use the `aws-`, `azure-` or `gcp-` icons (`ve.py --icons` lists them all; `db-` and `tech-` hold engine logos such as `db-postgres`, `db-mysql`, `tech-redis`, `tech-kubernetes`). The AWS set: (39 services: `aws-ec2` `aws-lambda` `aws-s3` `aws-rds` `aws-dynamodb` `aws-sqs` `aws-sns` `aws-msk` `aws-alb` `aws-cloudfront` `aws-api-gateway` `aws-vpc` and more).
  Label each with the service name and its role in this design ("S3 · ảnh gốc"), because recolored AWS icons look alike.
  `aws-auto-scaling-group` is a dashed group outline with a corner badge, not a node: for a VPC or subnet boundary draw a dashed `frame` and put `aws-vpc` small on its corner.
  Write the label as `"ALB\nnhận request vào"`: the tool centres each line under the icon.
  Icons are hollow, so a frame border drawn through one shows inside it: put the Internet Gateway just outside the VPC frame, not on its border.
  When arrows enter subnets from above, leave the frames untitled and write the names as free text where no arrow runs (VPC top-right, subnet bottom-left), or the vertical arrows cut the titles.
  A route table is a `table` (Destination, Target) under its subnet, joined by a dashed `line`; color its `0.0.0.0/0` row like the arrows that row sends, so the reader matches the row to the path.
  Run that taught it: AWS 1 public and private route tables (`aws1-hai-route-table-public-private`).

## 21 Sequence with fragments

**Use when** a flow between parties has a branch that matters: success and failure of a payment, cache hit and miss, retry, an optional step.
**Template:** `21-sequence-frames.json`.

- Write the fact list first: the actors, the main steps in order, then every alternative and error branch with an id (A1 declined, A2 timeout). Each branch becomes one `alt`/`else` or `opt`.
- Happy path and failure share one `alt` frame, so the reader sees where they split.
- `alt` for two or more exclusive branches, `opt` for one step that may happen, `loop` only around real messages (a loop holding only a note says nothing), `par` only for truly independent work.
- Rules that apply to the whole flow (idempotency, retry three times) go in one `note` at the top, not in a frame.
- `divider` separates two scenarios on the same lifelines (read path, write path). Two unrelated scenarios are two figures.
- Skip the reply message when it carries nothing: fewer dashed arrows, same meaning.
- Number with `n` only when the text refers to step numbers.
- **Timeout and retry:** a `loop` frame labelled with the limit ("tối đa 3 lần"), inside it the request with `"lost": true` and the timeout as the label or a `delay`. What happens once the retries are used up comes after the loop, in `err`.
- A header or key that must be seen (Idempotency-Key) goes on its own short message label or in a `note` right under the call, not on a second line.
- A human told by the system (báo CSKH) is a dashed arrow: it is asynchronous.
- One figure one goal: the lifecycle of the order belongs in a state diagram (section 23), not here.

**Size limits.** More than 15 messages, more than 4 actors in the site column (8 anywhere), or nesting deeper than 2: split into two or three figures.
A business sequence for a document outside the site may keep up to 8 actors: render with `--col 1100`.
Six actors with a hand-off in the middle (a topic, a queue): two `sequence` elements stacked, each in a dashed `muted` frame titled by who waits (`Trong request · Alice chờ` / `Ngoài request · SLO riêng`).
Give the shared actor the same `aw` and x in both, so its lower lifeline continues the upper one; order the lower actors right to left when that is what lines it up.
Each sequence keeps its own `gap`, so the three-actor half can afford long labels (`pipeline LPUSH + LTRIM 0 999`).
Run: ds-3 write path (`ds3-duong-ghi-fanout`, was a 6-actor Mermaid at 6.4px).

**Common failure:** nested condition labels with square brackets inside (`group [x]` renders `[[x]]`).
Use round brackets.

## 22 Business flow in swimlanes

**Use when** a process crosses roles and who does each step is the point: approval, refund, onboarding, order fulfilment.
**Template:** `22-swimlane.json`.

- One lane per role, in the order the work first reaches them. Declare the lane order before placing nodes.
- The flow runs top to bottom. One row per step, so time reads downward.
- `start` and `end` dots mark where it begins and where it stops.
- A decision is a diamond with a short question and a label on every outgoing edge.
- Step labels carry the real business rule: "token hết hạn sau 15 phút", not "kiểm tra".
- **Converge before you branch again.** When several branches end in the same steps, lead them all into one shared step ("Lưu quyết định") and split after it. Repeating the tail of each branch produces duplicate steps and crossing lines.
- Merge conditions when it removes a diamond: "duyệt và trên 5 ngày?".
- When the tails differ slightly (approval email, rejection email) still converge on one step and name the difference in it, or put one decision after the shared step. Do not draw the tail twice.
- A system or person that is called but owns no step (payment gateway) is named inside the step label, not given a lane.
- The first role's lane is mostly empty in any swimlane; that emptiness is the point (they wait), not a layout fault.
- The failure path is `err` and dashed.

**Not a swimlane:** one role only (use a decision tree or a plain flow), or the layers of a system (use section 16).

**Common failure:** a long edge crossing two lanes through other nodes.
Move the target node to another row so the edge runs in an empty band, or give the edge a `route` and `shift`.

## 23 Composite state

**Use when** an entity with three or more states has a lifecycle: payment, order, pull request, subscription.
**Template:** `23-composite-state.json`.

- `start` dot into the first state.
- **One `end` node per terminal state.** Arrows from several terminal states into one end point pile up and hide each other. With a single terminal state, draw one `end` and let the arrows into that state arrive on different sides.
- Transition labels are real event names: `payment_ok`, `timeout 15m`, `3ds_required`. When the source gives only conditions in prose, use its wording, shortened.
- A composite state is a `frame` with a title, sub-states inside. Arrows may start from the frame itself (any sub-state can time out) or from a sub-state.
- A loop back to an earlier state (`push_fix`) is the thing to show: place the two states so the return arrow is short.
- Skip self-transitions unless they are the point: the label lands on the state name.
- Color by meaning: `node` for the good outcomes, `err` for the failed ones. The frame takes `l4` when it is the thing under discussion, `warn` when the composite is itself a degraded state. A terminal state reached by both good and bad paths stays `ink`.
- Invalid transitions the reader would expect (no way back from `paid` to `pending`) deserve a `note`.

**Common failure:** a tall single column.
Put the main path down the middle, failures to the right, cancellations to the left.

## 24 ER with crow's foot

**Use when** the cardinality between tables is the point and the reader knows ER notation: data model of a feature, foreign keys, a join table.
**Template:** `24-er-crowfoot.json`.

- `tail` and `head` carry the cardinality: `one`, `many`, `one-many`, `zero-one`, `zero-many`.
- Optionality is a fact: an `o` end in the source (Mermaid `|o`, `o{`) is a nullable FK, so draw `zero-one` or `zero-many`, never round it to `one` or `many`. When the text is about optionality, add a four-row legend of the ends with what each means for the FK (run `td1-bang-noi-va-fk-nullable`).
  When the Mermaid ends and the `CREATE TABLE` in the same lesson disagree, the column wins: a FK without `NOT NULL` is a `zero-one` end even if the Mermaid says `||` (run `td4-variant-giu-gia-va-ton-kho`, `order_items.variant_id`).
- Land each FK edge on its column row: at the default size 16, field k (from 0) is centred at `y + 51 + 20k`. Give the other entity the `y` that puts its `id` row on the same line, then set `fromAt`/`toAt` so the edge stays horizontal.
  A vertical edge between stacked entities of different width runs centre to centre and comes out slightly diagonal: set `toAt` to `(centre x of the upper entity - x of the lower) / w of the lower`.
- Write `PK` `FK` `UNIQUE` after the column name. A join table shows its composite key.
- A column that points at another table but has no `REFERENCES` in the DDL (Mermaid still draws it as a relation) is a `dashed` edge with a short "không có FK" text beside it, `err` when the text calls the gap a bug, `muted` otherwise (run `td5-quan-sat-hai-duong-ve-benh-nhan`).
  Keep 150 units or more between the two entities: each solid ER end takes 40 units, and a shorter edge shows no dashes at all.
- A self-referencing FK (`amends_id`, `parent_id`) is a `points` bracket on the right side, from the FK row out 60 units, along, and back into the `id` row, label to its right.
  The corner self-loop of `from` = `to` lands on neither row.
- A composite FK cannot land on two rows: land it on one of its columns and spell the full pair once, in a `note` pointing at the child table (run `td5-danh-tinh-va-fk-composite`).
- Two FKs from one table to the same parent (`follower_id`/`followee_id`, `sender_id`/`recipient_id`) are a fork, not two parallel edges: the FK rows are 20 apart, so two edges would land on the parent's `id` row and the row under it.
  Draw one `sharp` `points` edge from the parent's `id` row to a fork 48 units out, then up 10 to the first FK row; a second edge starts at the fork with `tail: none` and runs down 10 to the second row.
  Keep each branch 80 units or more so crow, ring and the verb label fit, and put the label on the upper branch with `labelDy` -20 (run `sd52-nam-quan-he-quanh-users`).
- A many-to-many relation of a table with itself (Mermaid `users }o--o{ users`) is a join table with two FKs to it, drawn as the fork above; the Mermaid line has no table to land on.
- An elbow ER edge (`points` with three or more points) needs `sharp: true`, or the corners come out as curves.
- Leave 110 units or more between entities so the feet and the verb label fit.
- Put the verb label beside the line with `labelDy` or `labelDx`, not on it.
- The ring of a `zero-` end sits 24 to 34 units inside the edge, so on a horizontal edge under about 130 units a label centred at `labelDy` -16 lands on it: use `labelDy` -24, or `labelAt` toward the other end (run `td4-variant-giu-gia-va-ton-kho`). The tool reports it.
- The table the text is about gets `l4`; the rest stay `ink`.
- Class diagrams use the same build: `entity` for the class, `head` `inherit` `compose` `aggregate` for the relation.

## 25 System design with two flows

**Use when** one architecture serves two paths that must both be seen: write and read, online and batch, happy and fallback.
**Template:** `25-system-two-flows.json`.

- A dashed `frame` per path, titled with the path name (Đường ghi, Đường đọc; Speed layer, Batch layer).
- Number the first flow `1.` `2.` `3.`, letter the second `A.` `B.` `C.`. Parallel branches take a suffix: `7a` `7b`.
- One color per flow, on its arrows and labels only.
- Component labels carry the design decision: `(base62, 7 ký tự)`, `PK=conversation, CK=seq`, `TTL 1h`, `(sticky WebSocket)`.
- Compute is a `box`, a store is a `db`, a stream is a `pipe`, a third party is a `cloud`. Shared stores sit outside the frames.
- An arrow that leaves a frame runs in the gap between frames, not across a title.
- Mark what is not strongly consistent on the arrow: `eventually consistent`, `async`.
- Nested boundaries (VPC around cluster around service) are nested `frame`s, solid for real containment.

**Common failure:** a return arrow that circles the whole figure.
Enter and leave the client on different sides, or drop the return when the status code is not the point.

**Variant "sync and async, stacked"** (one path feeds the other, as nodes behind an LB handing slow work to a queue):
- Two full-width frames stacked: sync on top (client, LB, a row of nodes), async below (queue, workers). The nodes are the hand-off, so they sit at the bottom of the top frame.
- Every node feeds the queue: a comb of short `line`s from each node down to one bus in the gap between the frames, then ONE arrow into the queue tail. Three arrows converging on the tail stack their heads.
- The queue is a `cells` strip of `l3` hachure cells (cw 46 shows the hatch) with a `span` under it naming the depth metric (`consumer lag`); depth is the async path's imbalance, so it is drawn as length.
- Put each path's "how imbalance shows" note inside its own frame, the same muted size, so the two costs read side by side.
- A short dashed reply from a node's side to the client's side, looping left of the LB, says "answered before the slow work runs" without a return across the figure.
- Run: SD 03 §3.2.1 (`sd03-hai-duong-phan-phoi`).

## 26 Causal loop

**Use when** the idea is a cycle of causes: A grows B, B grows C, C feeds back into A, possibly with a second loop that slows it down.
Common in business ("happy customers bring more customers"), economics, habits, team dynamics.
**Template:** `26-causal-loop.json`.

- Four to six concepts placed on a ring, each a short noun phrase in the writer's words ("khách hài lòng", not "customer satisfaction index").
- Every arrow carries a sign as its label: `+` when more of A gives more of B, `-` when more of A gives less of B. Size 24 so the sign is not lost.
- All arrows stay `ink`. The sign carries the meaning; color goes only on the loop's name.
- Name each loop in the space it encloses: `R` with "vòng tự khuếch đại" for a reinforcing loop (even number of `-`), `B` with "vòng cân bằng" for a balancing one (odd number of `-`). The loop the idea is about is `l4`, the other `muted`.
- A balancing loop that leaves the ring takes an outside route (`points` with `sharp`) along the figure's edge, so it never crosses the ring.
- Curve the ring arrows with the same `bend` sign so the whole ring turns one way.

**Common failure:** drawing a list of causes as a ring when the last one does not really feed the first.
If the writer never said C changes A, it is a chain: use a left-to-right concept map instead.

## 27 Matrix 2x2

**Use when** two forces or criteria pull against each other and options sit in the four combinations: impact and effort, price and quality, urgent and important, risk and reward.
**Template:** `27-matrix-2x2.json`.

- Two axes as `arrow`s from a shared origin at bottom-left, with the axis name at the tip and `thấp` / `cao` in `muted` at both ends.
- Four equal boxes. Each box title is a verdict (`làm ngay`, `bỏ qua`), not a coordinate (`cao-thấp`).
- Under each title, the writer's own items as short bullets: the items are what the reader learns.
- Accent only the quadrant the idea argues for (`l4`, weight 3, no fill so the text keeps full contrast). Mark the quadrant to avoid `muted` and `dashed`.
- Keep quadrants just tall enough for their items; empty space inside a quadrant reads as "nothing belongs here".

**Common failure:** a 2x2 where the two axes are not independent (cost and price), so two quadrants are impossible.
Then the idea is a spectrum: draw one axis with options as points on it.

## 28 Funnel

**Use when** many things enter, fewer pass each stage, and the point is where they are lost: sales, hiring, sign-ups, applications, a learning path.
**Template:** `28-funnel.json`.

- One closed `line` trapezoid per stage, each one's bottom edge as wide as the next one's top, so width reads as "how many are left".
- Inside each stage: the real count large (size 24), the stage name small under it.
- Between stages, a dotted leader to the right with the pass rate worded as `12% đi tiếp`. A bare `12%` beside a narrowing shape is read as a loss rate.
- The stage with the biggest loss is the only `err` mark. The stage the idea is about (usually the last) is `l4` fill with `ink` text: `l4` text on an `l4` fill vanishes in the dark theme.
- With no numbers in the source, keep the shape, drop the rates, and do not invent counts.

**Common failure:** stage widths drawn to scale. Ten thousand against forty-five makes the last stage a sliver too narrow for its label; keep a fixed step in width and let the numbers carry the scale.

## 29 Concept map

**Use when** several concepts relate to each other and the reader must see how: teaching a concept, untangling a messy note, explaining a policy.
**Template:** `29-concept-map.json`.

- Five to seven concepts. More than seven turns into a mind map of every word; split it.
- Every edge is labelled with the verb that joins its two ends (`làm tăng`, `đẩy lên`, `là một phần của`, `cần`). An unlabelled edge says only "related", which the reader already assumed.
- Lay causes on the left, effects on the right, so the map reads in one direction; side influences come in from above or below.
- The concept the lesson is about sits in the middle in `l4` with weight 3. A short definition under it in `l4` text works as the anchor.
- The harm at the end of the chain, if the idea has one, is `err` with its edge.
- Keep at least 120 units between boxes on a horizontal edge: verb labels are 60 to 90 units wide and need line on both sides.

**Common failure:** every concept linked to every other.
Go back to the "This idea really says that" sentence of step 1 and keep only the edges that serve it.

## Rare figure types

| Need to show | How to build |
|---|---|
| Fan-out, one to many | One box in the middle, arrows spreading to targets stacked in a column |
| Convergence, many to one | The reverse, or a funnel from a closed `line` |
| Loop, feedback | Boxes arranged in a ring, last arrow returning to the first |
| Venn, intersection | Two or three overlapping `ellipse` shapes, bare text in each region |
| Map, geographic grid | `grid`, the cell under study outlined `err`, joined to a zoomed-in grid by two `line` elements |
| Scale (vertical scale) | Two `ellipse` shapes of clearly different sizes |
| Event chain on one line | `pipe` or a long arrow, small colored `ellipse` shapes placed on it like beads on a string |
| Notes page with requirements and API | A `card` per text block, placed above or left of the main figure |
| Comparing several options | One `frame` per option, same size, each holding a small figure with the same layout. When the options differ in WHERE something lives (who knows which machine holds a user: the hash, a store, a broker), stack the frames as full-width bands with the same slots (caller left, the thing that knows in the lower middle, target right), accent only that thing `l4` so the eye sees it move between bands, and end each band with its failure as one `✗` `err` line. Run: thiet-ke-mau-thiet-ke 1.2 (`thoi-gian-thuc-ai-biet-nguoi-o-may-nao`) When the options differ in WHERE an atomic boundary sits (Kafka transaction vs database transaction), keep the crash at the same arrow in every band (dashed `err` arrow labelled `✗ chết` into step 2), draw the boundary as a solid `l4` frame that encloses a different slot per band, put the slots in rows so the frame can hold one row or both, and end each band with a `✓` `node` or `✗` `err` outcome line. Run: hang-doi 9.2 (`sai-thi-sao-ranh-gioi-giao-dich`) |
| Multi-part token string (JWT, URL, ID) | One `text` line per part, one color per part, an explanation box in the same color below |
| Mind map, taxonomy | `tree` with `dir: "right"` and `lines: true` |
| Data pipeline | A `row` of boxes, a real data sample in `code` hung below each stage |
| Data flow diagram (DFD) | External entities as `box`, processes as `ellipse`, stores as `db`, every arrow labelled with the data that moves |
| Use case overview | `person` actors outside a `frame` (the system boundary), `ellipse` use cases inside, plain lines between them |
| Deployment | Nested `frame`s (region, VPC, cluster), `stack` for replicas, `db` per service |
| User journey | `axis` for the steps, a `plot` line for satisfaction 1 to 5, the low point marked `err` |
| Org chart | `tree` with `person` or `box` nodes and `lines: true` |
| Roadmap, milestones | `axis` with dated ticks, a short label per milestone. Not a Gantt |
| Partition by key (RSS queues, Kafka partitioner, shard router): why one key never spreads | The mixed input as one `cells` strip on top, items named by key and sequence (`A1 B1 A2`), the key under discussion `l4` hachure. Below it the hash box, then the mapping as a `table` with one column per target, so each column sits straight above its target and every arrow is vertical. Each target gets a `cells` strip holding only its key's items: strip length is the load, and the sequence numbers show order is kept. Add one dashed `muted` target with no arrow and "0" in it for "adding a target does not help this key". The reason the mapping is per key goes as a short `→` chain of muted text in the empty corner beside the hash box. Run: A2 RSS (`ba2-rss-mot-flow-mot-core`) |
| Ordered path with stops inserted at the right moment (reading path, migration plan) | One row per phase, phase name and a countable strip of `hachure` squares (one per week or session) in a left column. Main stops in the top lane, inserted stops `l4` in a lower lane: the path dips down into a stop and climbs back from its top, at 30% and 70% of the same edge so in and out never share a spot. A stop read alongside a main stop hangs below it as a small tag on a dashed line. Rows join by an arrow that drops into the gap and runs left to the next row's first box. Run: A6 reading path (`ba6-duong-mac-dinh-14-chang`) |
| Course or document map: a few framework lessons around many evidence chapters, and what each chapter stands on | Not the chapter table again: draw the relation the table cannot show. Framework lessons as `l4` filled boxes at the top and bottom, numbered with `badge`s for the short reading path, and joined by a dashed `l4` bypass in a narrow left lane (its label sits in the gap above the chapter frame, not in the lane). Chapters as same-size muted boxes in a two-column grid inside one dashed muted frame: title, the technologies it rebuilds as square `cells`, and the prerequisite course as one muted line (`đứng trên: ...`), so no arrow fans out from a prerequisite column. When the closing lesson is a lookup table, draw it as a `cells` strip with one cell per row, labelled with the chapter number that supplies the evidence, so the reader counts how many rows each chapter feeds. Use the empty last grid slot for the legend. Run: thiet-ke-cong-nghe 0.1 (`bat-dau-khung-va-bay-chuong`) |
| Levels that each buy one capability (history levels, isolation levels, consistency tiers) and what each costs | One full-width band per level, stacked top to bottom, all the same width; never one column per level, since four columns of prose force the text under 12px (the old hand-drawn version was 740 wide at 7.7px). Inside a band: level name in an unfilled box at the left, the question it answers as the first line of text, mechanism and domains as `muted` lines under it, and a `code` block on the right holding what every query must now carry. Give each block the same `w` and the same base line (`WHERE product_id = $1`), so the blocks grow down the page and band height itself shows the cost. Put the count in the block title (`1 trục: giá tại $2`). An ordinal cost from the source (0 / thấp / trung bình / cao) goes under the level name as a 3-cell strip with that many cells filled `warn`. Accent only the blocks that add something (`code` `color: l4`). Run: td-2 history levels (`td2-bon-muc-lich-su`) |
| One artifact promoted through stages (build, registry, staging, canary, 100%): what stays the same and what changes | A vertical spine of stage boxes, one per stage, so promotion reads downward and the figure stays under 800 wide (the Mermaid `LR` version was 1861 wide at 7.7px). Put the invariant (the digest `sha256:3f9a`) as the `l4` label of every promotion arrow, beside the line with `labelDx`, and keep it out of the boxes; each box holds only what that stage changes (`overlay: 2 replica, db staging`). Repeated identical arrow labels are what the reader sees as "the same thing moves". The gate is a diamond on the spine with its stop outcome to one side; the forbidden shortcut (rebuild for prod) is a dashed `err` box on the other side, reached by a `hv` route from the first stage and leaving by a `vh` route into the stage it corrupts, with its consequence as one `err` line under that last segment. Run: infra-2 PROMOTION (`infra2-mot-digest-qua-moi-moi-truong`) |
| A buffer flushed by size OR by time (Kafka producer batch, Nagle, write-behind cache, log flush) and what happens after the flush | Never the Mermaid loop of two diamonds (`đủ size?` → `hết giờ?` → back): drawn `LR` it was 1991 wide at 7.2px. Put two buffers side by side in one frame, each a `cells` strip of the same length so the length is the size limit: one full (all cells `l4` with real record names) with a `span` naming the size setting, one partly full (2 cells `l4`, the rest dashed `muted`) with the time setting and its default. Under each, one bold line for its trigger (`đầy → gửi ngay`, `hết giờ → gửi dù chưa đầy`), so the two flush causes read as two columns, not two questions. Both columns join into one vertical spine for the steps after the flush; slots that cap concurrency are a short `cells` strip with the used ones filled. Number each tuning knob with a `badge` beside its exact setting name, and put its consequence as one `muted` line to the side. Leave the frame untitled and centre its name between the two arrows that come down into the strips. Run: mq-1 producer batch (`mq1-bon-num-producer`) |
| A marker that travels with the data (checkpoint barrier, Chandy-Lamport snapshot, epoch marker) and what the snapshot holds | Freeze ONE moment instead of drawing steps: two sources into one operator, so the 'wait for the marker on every input' rule has two inputs to show. Each channel is a plain `muted` arrow with records as small `cells` riding on it (the arrow-through-shape nudge is expected there), named by source and order (`a5`, `b3`); the marker is a `weight` 5 `l4` vertical `line` across the channel with its id above. On the input the marker already reached, the records behind it are `warn` and held; on the other, records still ahead of it are plain and will be processed first. Under the topology, a `table` of the snapshot being assembled: one row per operator, what it saves written so the cut is checkable (`đọc lại từ a5` beside `count của a1-a4, b1-b4`), done rows `node`, pending rows `dashed` `muted`. Recovery goes as one short text beside the table (load the last COMPLETE snapshot), not as a second flow. Run: sd-53 CHECKPOINT (`sd53-checkpoint-barrier-hai-input`) |
| A deterministic rule fed a random input (round-robin assignor over sorted member ids, hash over a random id, leader by lowest id): why the count repeats but the owner does not | Two runs stacked as two bands with the same coordinates, column headers written once above both. Columns: the members in the order they started (box with the real prefix and an illustrative random suffix), the sorted list as a `cells` strip (`vị trí 0: …3f2a`), and the targets as a `cells` strip whose labels hold the real arithmetic (`p2: 2 mod 2 = 0`). One member is `l4` in both bands and its targets are filled `l4`, so the reader sees the colour move; the sort step is two arrows that run parallel in run 1 and cross in run 2. Leave the sorted-list to target gap without arrows: interleaved `i mod n` arrows always cross, and the colour already links them. One result line per band right-aligned under the targets, and one closing line for the invariant. Run: hang-doi 8.3 (`kafka-consumer-hai-luot-doi-chu`) |
| A retry loop and the counter it moves (job `attempts`, HTTP client retries, redelivery count): which value the code sees on each run and where the item ends | Unroll the loop: one row per run, so the reader counts the runs instead of following a back-arrow. Columns are who acts (the waiting list, the worker, the retry test, the script that writes the counter), headers as `muted` text above the first row. The worker box holds the value the code reads on that run (`thấy attemptsMade 0`) in `l4`; the test is a diamond with that run's real arithmetic (`0 + 1 < 3`), not the abstract rule, which goes once in the column header; the script box holds the write as before → after (`HINCRBY atm: 0 → 1`), so the off-by-one between what the code saw and what the store holds is visible on one row. Each non-final row returns to the next row's first box with a `sharp` `points` elbow under the row, labelled once with the destination (`về wait`). The last row exits down to the terminal box; the value read afterwards and the option the scenario did not take (backoff) go as one `l4` line and one dashed `muted` box beside it. Run: hang-doi 6.3 (`bullmq-attempts-ba-luot-mot-bo-dem`) |
| Optimistic retry under contention (WATCH/EXEC, compare-and-set, version column): why the total work grows with the square of the contenders | Top: one attempt as a strip of empty cells with the commands in free `mono` text, and one `sharp` `err` elbow under the strip from the last command back to the first, labelled with the failing reply. Below: a grid with one row per round and one column per client, built from separate boxes on a fixed pitch (a `cells` strip has no gaps, so columns would not line up with a second row of different cells). Each row has one `node` winner and `err` losers; finished clients get no cell, so the grid becomes a triangle the eye reads as quadratic before any number. Put the per-round attempt count in a right column with a rule and the sum under it, add how many of them failed, then one row of the single-command alternative in the same columns with its count in the same column. Use the empty lower-left triangle for the two lines that explain why the losers lose. Draw a small N labelled "ví dụ" and write the general sum in `mono` underneath; never the lab's total. Run: redis 7.2 (`atomic-watch-moi-vong-mot-nguoi-thang`) |

## Building a new figure from primitives

When no type fits, build from `box` `ellipse` `diamond` `line` `arrow` `text`.

- **Free polygon**: `line` with `points` and `closed: true`, plus `fill`. Bucket, funnel, block arrow, parallelogram, label tag.
- **Arcs and curves**: a `line` or `arrow` with three or more points is rounded automatically. Add `sharp` to keep the corners.
- **Repeated things**: write a short Python script that generates the element list and writes JSON. Do not hand-type thirty cells.
- **Reused shapes**: wrap in a `group`, then move it with `dx` `dy`.
- **Background layer**: elements declared earlier sit underneath. Declare filled background regions first.

After building an unusual figure that works, save its spec to `examples/` with a `_` line saying what it is for, so there is a template next time.
