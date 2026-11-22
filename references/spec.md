# Spec syntax of `scripts/ve.py`

Contents: [File skeleton](#file-skeleton) · [Common properties](#common-properties) · [Primitive elements](#primitive-elements) · [System components](#system-components) · [Data](#data) · [Time and measurements](#time-and-measurements) · [Prebuilt diagrams](#prebuilt-diagrams) · [Annotations](#annotations) · [Layout and reuse](#layout-and-reuse) · [Icon](#icon) · [Command line](#command-line) · [What the tool checks](#what-the-tool-checks)

## File skeleton

```json
{
  "_": "ghi chú tự do, công cụ bỏ qua",
  "extends": "buoc-1.json",
  "dimBase": true,
  "remove": ["id-cũ"],
  "elements": [ { "t": "box", "id": "a", "x": 0, "y": 0, "w": 120, "h": 56, "text": "API" } ]
}
```

- Coordinates are Excalidraw units, origin at top-left, `x` to the right, `y` downward.
- `x`,`y` of every element is its **top-left corner**. Negative coordinates work, the frame fits the content tightly.
- Order in `elements` is draw order: a later element sits on top of an earlier one.
- `extends`, `dimBase`, `remove` are only for progressive figure series, see [Layout and reuse](#layout-and-reuse).

## Common properties

| Property | Value | Notes |
|---|---|---|
| `color` | `ink` `muted` `line` `l2` `l3` `l4` `l6` `l7` `err` `warn` `node` `heap` `hot` | Stroke and text color. Default `ink`. Accepts token names only, no hex codes. Text never renders in `warn`: amber text is 2.44:1 on the light page, under the site's 3:1 gate, so the tool draws it in `ink` and keeps `warn` for strokes and fills |
| `fill` | `soft` or `l2` `l3` `l4` `l6` `l7` `err` `warn` `node` `heap` `hot` | Light background color of that token. Empty means no fill |
| `lit-dark` / `lit-light` | as `color` or `fill` | A literal object color that stays the same in both themes: a dark moth, a soot-black trunk, white paper, a dark night sky. Every other token flips in the dark theme, so a "dark" thing drawn in `ink` turns light there (both moth eval runs hit this). Never put text inside a `lit-*` fill: `ink` text flips and vanishes in one of the two themes. Label it beside or below |
| `fillStyle` | `solid` (default) `hachure` `cross-hatch` | `hachure` for countable things and the "lost" part, `solid` for regions. Excalidraw draws hachure lines in the pale fill tint, 8 units apart, so the tool helps two cases: `soft` hachure lines use the `line` token (in `fill-soft` they vanished at any width), and a shape with no text whose short side is under 30 units gets its lines from an under-layer in the saturated fill token at 55% opacity, 6 apart (cw 13 and cw 18 hachure cells read as empty, sd01 and hang-doi 3.3 runs). Cells with text keep the tint |
| `dashed` / `dotted` | `true` | Dashed / dotted stroke |
| `weight` | number | Stroke weight, default 2. Use 4 to emphasize one line |
| `size` | number | Font size. Default 20 for text in shapes, 16 for arrow labels |
| `opacity` | 0-100 | Rarely needed |
| `id` | string | Target for arrows and notes. Must be unique. A free `text` is never a target, even with an `id`: point a `points` arrow at it |

## Primitive elements

### `box` `ellipse` `diamond`

```json
{"t":"box","id":"svc","x":320,"y":78,"w":150,"h":64,"text":"Order Service","color":"l4","fill":"l4"}
```

`x y w h` are required.
Optional: `text` (line break with `\n`), `sharp` (square corners, `box` only), `align` (`left|center|right`), `valign` (`top|middle|bottom`).

Excalidraw auto-expands a shape when its text does not fit, which shifts the whole layout, and the tool reports `✗`.
A diamond or ellipse needs about twice the text width and twice the text height.

### `arrow`

```json
{"t":"arrow","from":"svc","to":"pg","text":"2. INSERT","color":"hot"}
{"t":"arrow","points":[[132,52],[210,60],[226,118]],"color":"warn"}
```

| Property | Meaning |
|---|---|
| `from` `to` | ids of the two ends. Endpoints are clipped at the shape edge. `from` equal to `to` gives a self-loop at the top-right corner |
| `fromSide` `toSide` | Force an edge: `top` `right` `bottom` `left` |
| `fromAt` `toAt` | Position along the edge, 0 to 1, default 0.5. Always name the side too (`fromSide`/`toSide`) when you pin a position: with `fromAt` alone the tool picks the side itself and the arrow can leave from a different edge than planned (three arrows left a container frame from mid-bottom at wrong x and one crossed a neighbouring label, app-nhin-thay-gi 5.1 run) Use when several arrows share one edge. When only one end is pinned, the free end aims at that pinned point, so `toSide: "left"` + `toAt` on a tall target gives a level arrow from a box at that height (before the td5 run the free end aimed at the target's centre and the arrow sloped) |
| `bend` | Offset in units to curve the arrow, negative curves the other way. Two opposite arrows between two shapes: give both the same `bend` |
| `route` | Orthogonal routing: `hv` `vh` `hvh` `vhv`. Add `shift` to move the middle segment |
| `points` | Replaces `from`/`to`: a list of absolute coordinates. Three or more points make a curve, add `sharp` to keep sharp corners |
| `text` | Label at the middle of the arrow. Three words at most; an identifier, an endpoint or a step number counts as one word. `\n` gives a second line |
| `head` `tail` | `arrow` `triangle` `dot` `bar` `none`. ER ends: `one` `many` `one-many` `zero-one` `zero-many` (crow's foot; the two `zero-` ends add the hollow ring of an optional side, which Excalidraw lacks, so Mermaid `|o` and `o{` keep their meaning). On a `dashed` or `dotted` arrow the ER ends and rings stay solid: Excalidraw would dash them into stubs, so the tool draws each ER end on its own solid 40-unit segment. UML ends: `inherit` (hollow triangle) `compose` (filled diamond) `aggregate` (hollow diamond) `circle`. `both: true` gives arrowheads at both ends |
| `labelAt` `labelDx` `labelDy` | Any of these turns the label into free text beside the line instead of a label that breaks the line. `labelAt` is a position along the whole drawn path, corners included: 0 to 1 is a fraction of its length, above 1 is units from the start (default 0.5). On a routed arrow check which segment that lands on. `labelDx` `labelDy` offset the label centre from that point; the default puts it above a horizontal segment and right of a vertical one. Use on short arrows, on routed arrows whose midpoint is a corner, and on ER edges so the feet stay visible |
| `id` | With an id, a `note` can point at the arrow's midpoint. Declare the arrow before the note |

### `line`

```json
{"t":"line","points":[[170,130],[330,130],[300,270],[200,270]],"closed":true,"fill":"soft","weight":3}
```

A stroke without arrowheads.
`closed: true` makes a closed, fillable polygon: a bucket, a funnel, a trapezoid, a block arrow.
`smooth: true` rounds it into a curve.

### `text`

```json
{"t":"text","x":392,"y":22,"text":"mỗi request lấy 1 token","color":"node","size":18}
```

Free text.
`mono: true` for monospace text.
`align` also changes the meaning of `x`: with `left` (default) `x` is the left edge, with `center` `x` is the **center** of the text block, with `right` `x` is the right edge.
Use `center` to put text exactly at the middle of a column or a tick without measuring the text width.
A `text` cannot be the `from` or `to` of an arrow (the tool says so and stops); for an arrow ending at a bare label such as a plan tree's "kết quả", use `points` and stop about 6 units short of the text (dbi4 run).

## System components

Every component below accepts `id x y w h text color fill` and can be an arrow target.
`id` is required on these components and on `cells` `grid` `table` `entity` `code`.

| `t` | Draws | Own properties |
|---|---|---|
| `db` | Upright cylinder: a data store | `kind`: `sql` (three disks) `doc` `kv` `col` (vertical columns) `ts` (zigzag line) `blob` `search` `vector` `graph`. With `kind`, the label sits below the cylinder |
| `pipe` | Horizontal pipe: stream, log, Kafka topic | `segments`: number of segments (partitions). With `segments`, the label sits above |
| `queue` | Flat box holding messages | `items`: a list of `{"color":..,"text":..}`, or `n` for n empty messages. `labelPos: "above"` |
| `stack` | Offset stack of boxes: multiple instances | `n` (default 3). The id points at the top box |
| `person` | Stick figure | No `w`, only `h`. Label sits below |
| `window` | Browser window or app screen | `title` on the title bar |
| `cloud` | Cloud: external service, internet, CDN | `dashed` |
| `doc` | Sheet with a folded corner: file, page, document | |
| `frame` | Frame around a group, title at top-left | `title` `titleColor` `dashed` |

```json
{"t":"db","id":"pg","x":560,"y":14,"w":90,"h":92,"kind":"sql","text":"Postgres"}
{"t":"pipe","id":"k","x":0,"y":170,"w":300,"h":50,"text":"topic orders","segments":4}
{"t":"queue","id":"q","x":540,"y":150,"w":170,"h":46,"text":"events","items":[{"color":"hot"},{},{}]}
{"t":"frame","id":"f","x":0,"y":0,"w":330,"h":210,"title":"Redis node","dashed":true,"color":"l2"}
```

## Data

### `cells`: strip of cells

```json
{"t":"cells","id":"bk","x":60,"y":70,"cw":64,"ch":40,"dir":"col",
 "labels":["","","","","…"],"index":["0","1","2","3","1023"],"title":"mảng bucket",
 "marks":{"1":{"color":"hot","fill":"hot"}}}
```

- `labels`: text of each cell, `""` is an empty cell.
- `cw` `ch`: size of one cell. `dir`: `row` (default) or `col`.
- `widths`: per-cell width when cells differ in size (bytes, durations). With `dir: "col"` this is the height.
- `index`: `true` to number from 0, or a list of labels. Numbers sit ABOVE the cell (horizontal strip) or LEFT of the cell (vertical strip), size 15, color `muted`: leave 24 units on that side.
- Estimate text width to pick `cw`: character count × font size × 0.52, plus 16 units of padding. `order-1001` at size 16 needs `cw` around 100.
- `marks`: style individual cells by index. Each mark accepts `color`, `fill`, `fillStyle`, `dashed`.
- `size`: font size in cells (default 18 for a strip, 16 for `grid`).
- `title`: small title above.
- Cell i has id `<id>.<i>`, the whole strip has id `<id>`.

### `grid`: two-dimensional grid

```json
{"t":"grid","id":"g","x":0,"y":0,"cw":44,"ch":40,"rows":[["0","1"],["2","3"]],"marks":{"1,0":{"fill":"err"}}}
```

A cell has id `<id>.<row>.<col>`.

### `table`: table with a header and real rows

```json
{"t":"table","id":"t","x":300,"y":190,"cols":[60,90,90],"head":["id","user_id","total"],
 "rows":[["1","7","120"],["2","7","80"]],"marks":{"0":{"fill":"l4"},"1,2":{"color":"err"}},"title":"orders"}
```

`cols` is the width of each column, `rh` is the row height (default 38).
`marks` accepts `"row"` or `"row,col"`, each with `color`, `fill`, `fillStyle`, `dashed`.
A `dashed` `muted` row with empty cells is a row that never got written, for the "after" half of a figure where a constraint stopped the insert (td5 run).
Row i has id `<id>.<i>`, a cell has id `<id>.<i>.<col>`.
A header cell has id `<id>.h.<col>`: aim an edge at it with `toSide: "top"` when the edge stands for a whole column, not one row.
The `title` sits 28 units above the top-left corner, so an edge entering the top of the first column runs through it: move that edge with `toAt`.

### `entity`: entity with a column list

```json
{"t":"entity","id":"o","x":300,"y":0,"w":190,"name":"orders","fields":["id  PK","user_id  FK","total"]}
```

### `code`: dark-background code block

```json
{"t":"code","id":"req","x":0,"y":0,"title":"request","text":"POST /payments HTTP/1.1\nIdempotency-Key: 7f3a-91c2"}
```

Dark background in both themes, monospace text.
Width is computed from the longest line, or set `w` (equal `w` lines up several blocks so arrows leave them at one x).
The `title` counts as a line: a `w` narrower than the longest line or title stops the tool, since text over the box is free text and no overflow check sees it leave the box (ds3 run).
`color` (`err` `node` `l4`) draws the border in that accent at weight 2; the text stays light on dark, so the border is the only way to mark one block as the failing run, the silent run or the diff under discussion (infra2 run).
`size` sets the code font; the `title` follows it down (never above 15), so a size-12 block does not sit under a bigger heading.
Line i (from 0) of `text` is centred at `y + 38 + 18.75 i + 9.4` with a `title` (`y + 12 + ...` without), at the default size 15: use it with `fromAt` = that offset / block height to start an arrow level with one line.

## Time and measurements

### `axis`: axis with ticks

```json
{"t":"axis","x":80,"y":200,"length":620,"gap":140,"ticks":["0s","10s","20s","30s","40s"],"label":"t"}
```

`dir: "y"` for a vertical axis (arrowhead pointing up).
`gap` is the distance between two ticks, counted from the origin: **set it when ticks must line up with the edge of a cell or bar above**, otherwise ticks are spread evenly.

### `span`: bracket measuring a range

```json
{"t":"span","x1":290,"x2":380,"y":150,"text":"mất tin nếu có ở đây","color":"err"}
```

`side: "above"` puts the text above.

### `plot`: chart

```json
{"t":"plot","id":"p","x":60,"y":230,"w":420,"h":180,"ylabel":"request/giây","max":120,
 "bars":[{"label":"shard 1","value":38,"color":"l2","fill":"l2"},{"label":"shard 3","value":112,"color":"err","text":"user:celeb"}],
 "thresholds":[{"value":80,"label":"sức chứa một node"}]}
```

- `x`,`y` is the **bottom-left corner** of the plot area (the only exception to the top-left rule).
- `bars`: `label` below the bar, `text` above the bar. Bars are filled `hachure` with the `fill` color by default (no `fill` means the bar's own `color`); set `"fillStyle":"solid"` per bar for a solid fill.
- `lines`: `[{"points":[[x,y],...],"color":..,"label":..}]`, coordinates in data units. Set `xmax` and `max` to fix the scale.
- `thresholds`: dashed horizontal lines. The label is drawn to the RIGHT of the plot area, outside `w`: leave room for it. Bar labels and `ylabel` also fall outside the `x`/`w` box.
- Each bar is an arrow target with id `<plot id>.<i>`; the plot id itself is not.
- Lines are smoothed by default; `"smooth": false` on a line keeps straight segments (use it for a flat-then-ramp shape).
- `xticks`: `[{"at":0.5,"label":"p50"}]`, `at` from 0 to 1.

## Prebuilt diagrams

### `sequence`

```json
{"t":"sequence","x":0,"y":0,"gap":220,
 "actors":[{"id":"c","label":"Client"},{"id":"lb","label":"ALB","color":"l4"}],
 "messages":[
   {"from":"c","to":"lb","text":"GET /orders","n":1},
   {"from":"lb","self":true,"text":"tra bảng route"},
   {"note":"timeout 30s","over":["c","lb"],"color":"err","fill":"err"},
   {"from":"lb","to":"c","text":"502","dashed":true,"color":"err","fail":true}]}
```

`gap` is the distance between two lifelines, `step` is the distance between two messages.
`n` numbers the step.
`fail: true` adds an X next to the label.
`note` spans across the actors listed in `over`.

Fragments and separators are entries in the same `messages` list:

```json
{"alt":"thanh toán được duyệt"},
{"from":"pay","to":"ord","text":"approved","dashed":true},
{"else":"bị từ chối"},
{"from":"pay","to":"ord","text":"declined","dashed":true,"color":"err"},
{"end":true},
{"divider":"Ghi"},
{"delay":"15 phút sau"}
```

- A fragment opens with one of `alt` `opt` `loop` `par` `group` `break` `critical` (the value is the condition shown in brackets) and closes with `{"end":true}`.
- `{"else":"condition"}` adds a dashed separator inside the open fragment.
- `divider` draws a full-width titled rule between two scenarios; use it outside frames only. `delay` writes a time gap between two messages.
- Frames span every lifeline and inset by nesting depth, so sibling frames line up. `"over":["a","b"]` on the opening entry narrows one.
- Fragments nest: an `alt` inside a `loop` is the retry pattern. A fragment inside a parent narrowed with `over` stays inside it.
- Defaults: `gap` 190, `step` 54. The opening entry takes `color` (default `muted`). Messages take `head` and `weight`.
- The actor box widens to fit its label (`aw` is the minimum, default 130) and `gap` grows with it.
- An actor label may take `\n` (`"Role admin\naccount 123"`): the column is then as wide as the longest line, and every actor box grows to the tallest label (17 × 1.35 per line + 11).
  A one-line `Role app-admin · account 456` made the column 277 wide and four actors 1 200 (aws1 run).
- Message `text` is one line. A header, payload or rule that does not fit goes in a `note` entry or a `code` block beside the diagram.
- A message label is centred over its arrow, anchored at its centre so the Patrick Hand swap does not shift it.
  A message that crosses other lifelines gets its label over the first gap from the sender (lessons rule 17), so that gap, not the whole arrow, must hold it.
  A self-message label starts 56 units right of its lifeline and must end before the next one.
  A self-message right after a frame opens moves up 20 units, since it has no label above its line (ds3 queue 2: a `break` holding one self-message had an empty band under its header).
- `"lost": true` on a message draws a request that stops short with an X: the call that never gets a reply. Use it for timeouts, then a self-message or a `note` for what the caller does next.
- A `note` entry takes `over` (default: first to last actor), `color` and `fill`. It is a dashed `muted` box reaching 40 units past the lifelines it covers on each side; inside a fragment it shrinks to stay within the frame.
  Its width comes from `over`, not from the text: over one actor it is only 80 wide, so a longer note needs a second actor in `over`.
  Note text may take `\n`: the box grows by 15 × 1.35 per line and the next message moves down with it (before the aws1 run it stayed 34 tall and Excalidraw grew it over the next message).

### `tree`

```json
{"t":"tree","id":"d","x":0,"y":0,"nw":170,"nh":110,"dx":30,"dy":56,
 "root":{"shape":"diamond","text":"cần đẩy?","w":250,"children":[
   {"edge":"không","text":"polling","h":56},
   {"edge":"có","text":"WebSocket","color":"l4","fill":"l4","h":56}]}}
```

- `nw` `nh`: default node size. `dx`: distance between two nodes on the same level. `dy`: distance between two levels.
- Each node: `text`, `shape` (`box` `ellipse` `diamond`), its own `w` `h`, `color` `fill`, `edge` (label on the edge from the parent), `edgeDashed`, `id`.
- `dir: "right"` for a tree growing sideways. `lines: true` for edges without arrowheads.
- `nh` must equal the height of the TALLEST node, because level spacing is computed from it.

### `ring`

```json
{"t":"ring","id":"r","cx":190,"cy":170,"r":120,
 "ticks":[{"angle":0,"label":"0"},{"angle":90,"label":"25"}],
 "arcs":[{"from":140,"to":250,"color":"warn","label":"dời sang A"}],
 "nodes":[{"id":"a","angle":310,"label":"node A","color":"node"}]}
```

Angle 0 is at the top, increasing clockwise.
`arcs` highlights an arc.
A node accepts `dashed`, `fillStyle`, `d` (diameter).
A tick within 12 degrees of a node gets its label pushed inward by half the node's `d`, so a node "at position 25" can carry the tick "25" without the two touching.

### `lanes`

```json
{"t":"lanes","x":0,"y":0,"w":700,"labelW":120,
 "lanes":[{"id":"app","label":"ứng dụng","h":80},{"id":"ker","label":"kernel","h":100,"fill":"soft"}]}
```

Horizontal lanes stacked top to bottom.
Place other elements on top using normal coordinates.

### `swimlane`: business flow, one column per role

```json
{"t":"swimlane","x":0,"y":0,"laneW":175,"rowH":100,
 "lanes":[{"id":"nv","label":"Nhân viên"},{"id":"sys","label":"Hệ thống","w":215}],
 "nodes":[
   {"id":"s","lane":"nv","row":0,"kind":"start"},
   {"id":"gui","lane":"nv","row":1,"text":"Gửi đơn nghỉ"},
   {"id":"du","lane":"sys","row":2,"kind":"decision","text":"đủ ngày?"},
   {"id":"tc","lane":"sys","row":3,"text":"Tự từ chối","color":"err","dashed":true},
   {"id":"e","lane":"nv","row":4,"kind":"end"}],
 "edges":[
   {"from":"s","to":"gui"},
   {"from":"gui","to":"du"},
   {"from":"du","to":"tc","text":"không","color":"err"}]}
```

- A node sits at the centre of its `lane` column on grid row `row`. `dx` `dy` nudge it. Two nodes may share a row in different lanes.
- `kind`: `step` (default, rounded box), `decision` (diamond), `merge` (small diamond), `start` (filled dot), `end` (ringed dot).
- Nodes take `text w h size color fill fillStyle dashed`. Macro defaults: `nw` 150, `nh` 56, `size` 16.
- Without `w`/`h` a node sizes itself to its text, including multi-line text. A diamond needs about twice its text width, so keep decision text to two or three words or the diamond outgrows its lane. An explicit `w`/`h` always wins.
- Two columns in one lane: widen the lane, set `w` on both nodes and give them `dx` (for example lane `w` 320, node `w` 120, `dx` -75 and +75). `fromAt`/`toAt` on an edge are fractions along the chosen side, measured from the left or the top.
- Edges are arrows and take every `arrow` property. Without `route`/`fromSide`/`toSide`/`bend` the macro routes them: straight between nodes on the same centre line or the same row, `vhv` from a step to a node in another column, `hv` out of the side of a decision that faces the target.
- A labelled edge leaving a decision gets its label 30 units from the diamond. On a short edge set `labelAt` or `labelDx` yourself.
- Lanes take `w` (default `laneW`, 190), `fill`, `color`. `rowH` (default 110) is the row pitch: it must leave 25 units or more between stacked nodes, so raise it when two decisions follow each other. `headH` is the header height (default 40).
- The lanes end just below the lowest node (26 units under its bottom edge). Free text under the figure, such as a one-line conclusion, goes 16 or more units below that edge; if it straddles it, the nudge prints the lanes box (`_s2 (box x 0-756, y 0-605)`), so read the bottom off it.

### `start` `end`: pseudo-states

```json
{"t":"start","id":"s","x":54,"y":40}
{"t":"end","id":"e1","x":712,"y":20}
```

A filled dot (22 units) and a ringed dot (26 units) for state machines and activity flows; `d` sets the diameter.
Both are arrow targets.

## Annotations

| `t` | Use for | Example |
|---|---|---|
| `note` | Free note, can point a dashed line at something. `color` colors the pointer too. Keep the note 45 units or more from its target or the pointer is too short | `{"t":"note","x":330,"y":60,"text":"đụng độ","to":"e2","color":"err"}` |
| `badge` | Numbered step circle | `{"t":"badge","x":276,"y":4,"n":1,"color":"node"}` |
| `steps` | Numbered step list placed beside the figure | `{"t":"steps","x":400,"y":60,"title":"Khi node C chết","items":["...", {"text":"...","color":"muted"}]}` |
| `card` | Card with an underlined title: API, requirements, figures | `{"t":"card","x":340,"y":250,"title":"API","text":"POST /orders","mono":true}` |
| `legend` | Legend for colors and stroke styles | `{"t":"legend","x":560,"y":330,"items":[{"color":"hot","fill":"hot","text":"đường đi"},{"color":"err","line":true,"dashed":true,"text":"lỗi"}]}` |
| `cross` | Red X | `{"t":"cross","x":596,"y":296}` |
| `check` | Green check mark | `{"t":"check","x":430,"y":250}` |

`note` accepts `to` (id of a shape or of an arrow), `toSide`, `fromSide`, `bend`.
A `legend` item with `line: true` draws a short arrow; add `"head":"none"` when the edges it explains have no head (tree `lines`, ER lines), or the key and the figure disagree (td2 closure table run).
Put `cross` and `check` at a shape's **corner**, never on top of text.

## Layout and reuse

### `row` / `col`: even spacing

```json
{"t":"row","x":0,"y":110,"gap":50,"elements":[
  {"t":"box","id":"p1","w":110,"h":56,"text":"Trừ tiền"},
  {"t":"box","id":"p2","w":110,"h":56,"text":"Giữ hàng"}]}
```

Child elements do not need `x`,`y`.
Use for same-kind boxes placed in a line.

### `group`: move a whole cluster, dim a whole cluster

```json
{"t":"group","dx":420,"prefix":"2","dim":true,"elements":[ ... ]}
```

`dx` `dy` move the whole cluster.
`prefix` is prepended to every id in the cluster, so two copies of the same frame can be drawn without id clashes.
`dim: true` drops the whole cluster to `muted`.

### `extends`: progressive figure series

```json
{"extends":"17a-progressive-1.json","elements":[ {"t":"db","id":"rd", ... ,"color":"l4","fill":"l4"} ]}
```

The new figure takes all elements of the base file, drops them to `muted`, then draws the new elements on top.
`dimBase: false` keeps the base colors.
`remove: ["id"]` drops some base elements.
Do not move old elements: a fixed position is what lets the reader see what is new.

## Icon

```json
{"t":"icon","id":"fw","name":"firewall","x":170,"y":30,"h":60,"text":"WAF","color":"err"}
```

- `python3 scripts/ve.py --icons` lists the 188 icons available in `assets/icons.json`.
- Set `h` or `w`, the other follows the aspect ratio. `text` is the label below the icon, each line centred under it (`\n` for a second line).
- The size is measured on the drawn strokes. Before the AWS 1 run the tool added a line's `width` to its `x` even when its points ran leftward, so 63 of the 130 icons came out up to half the requested size with the label off-centre or far below.
- `--lib path/to/file.excalidrawlib` loads any extra library, the icon name is the item name in that library.
- Icons are recolored to `color`, so they always match the theme.

## Command line

```bash
python3 scripts/ve.py a.json b.json            # outputs next to the spec
python3 scripts/ve.py a.json --out /tmp/figs   # outputs elsewhere
python3 scripts/ve.py a.json --lib aws.excalidrawlib
python3 scripts/ve.py --icons
python3 scripts/ve.py a.json --col 1100          # preview and font check at another column width
```

`--col` is for figures that will not sit in the default 666px reading column (a business document, a slide, a wiki page).
Never use it to silence the font check on a figure meant for the site.

Each figure prints one summary line, its `✗` and `•` lines, then a `→ LOOK:` block with the two PNG paths to open.
Exit code 1 when there is at least one `✗` line.

## What the tool checks

| Mark | Condition | Fix |
|---|---|---|
| `✗` | Shape expanded by Excalidraw because text does not fit | Set a larger `w`/`h`. When only the height grew, the message tells two cases apart by counting the lines Excalidraw drew: more lines than the spec text means it wrapped, so widen (minimum `w`/`cw` given; a larger `h`/`ch` does not help); the same line count means the box is just too short, so raise `h` to lines × size × 1.35 + 11 (Excalidraw sets Nunito at 1.35 line height: two lines at size 15 need 52, not 48, sd53 run) |
| `✗` | Text overflows its containing shape or the frame | Enlarge the shape, shorten the text |
| `✗` | Smallest text below 8px on screen | Figure too wide: stack vertically or split the figure |
| `✗` | A `code` block's `w` is narrower than its longest line or title | Raise `w` or shorten the line |
| `✗` | A non-token color remains | Only happens with unknown icons: report it |
| `✗` | Spec error: unknown color or fill token, unknown `t`, missing property, duplicate id, arrow end or swimlane node that matches no id, unknown `head`/`tail`, unclosed or stray fragment entry, multi-line message text, unknown icon, circular `extends` | The message names the element and the valid values |
| `•` | Smallest text below 12px | Compact the figure if possible |
| `•` | Arrow passes through a shape that is not one of its two ends. A `points` arrow counts too: the shapes its first and last points touch are its ends | `bend`, `route`, or move the shape |
| `•` | One arrow's head lands where another arrow starts (a pair `a → b`, `b → a` is exempt) | `fromAt`/`toAt`, another side, or different `points` so in and out have separate spots |
| `•` | Two arrows leave the same spot, or reach the same spot, in the same direction, so their first or last segments share one stroke for more than 12 units (a swimlane `vhv` edge and a straight edge both leaving the bottom centre of one node, dbi3 hero run) | `fromSide`/`fromAt` on one of them, or `toAt` for two arriving |
| `•` | An arrowhead is cut by the border of a box it does not land on: its tip is inside an enclosing `frame` and its base outside, or the reverse (an arrow entering a frame to a shape 14 units inside the border). The base is probed 26 units behind the tip, Excalidraw's ~25-unit head plus the rough stroke: a frame bottom 24 units under the tip cut the head of an arrow coming up from below and a 20-unit probe missed it (infra2 hero run) | Move the frame border 30 or more units clear of the tip, or move the target |
| `•` | Arrow shorter than 22 units, or 64 with `both` or a `tail` (a 50-long two-headed arrow still reads as a diamond): the heads hide the line | Move the two shapes apart |
| `•` | Label nearly as long as the arrow carrying it, measured along the arrow (its width on a horizontal arrow, its height on a vertical one) | Move the two shapes apart, shorten the label, or turn it into a `note` |
| `•` | Free text overlaps other text or straddles a box border | Move the text |
| `•` | Free text sits inside a frame-sized shape (3x the text or larger) less than 4 units from its edge: the rough stroke runs through the glyphs and the straddle test misses it (sd03 run) | Keep 6+ units clear of the edge, or grow the frame |
| `•` | An arrow's line runs through a free text (a `vh` arrow leaving the bottom of a `cells` strip ran down through the strip's caption, hang-doi 2.3 run) | Move the text beside the strip, or leave from another side |
| `•` | A label lies within 3 units of the hollow ring of a `zero-one`/`zero-many` end | Raise it with `labelDy`, slide it with `labelAt`, or lengthen the edge |
| `•` | A free label touches the bar or crow of an ER end (the last ~24 units of the edge, ~8 units either side of the line) | Slide it with `labelAt` toward the middle, raise it with `labelDy` (-22 on a horizontal edge under ~130 units), or lengthen the edge |
| `•` | A `sequence` message or self-message label runs across a lifeline (measured on Excalidraw's Nunito box, ~20% wider than the drawn glyphs, hang-doi 0.1 run) | Shorten the label, drop `n` numbers the text does not cite, or raise `gap` to the width the message gives |
| `•` | More than three accent colors | Remove some colors |
| `•` | Only rounded boxes joined by arrows (`code` blocks do not count, and at least one arrow must exist) | Reconsider the figure type |

The tool cannot check: whether the figure says the right thing, whether the layout is balanced, whether labels are true.
Those three must be checked by eye.

An arrow `text` label cuts a gap in its line with an SVG `<mask>`.
The tool writes the shapes inside that mask as `<path>`, not `<rect>`: `precheck.py` reads every `<rect>` as a possible background, mask content included, and failed every dark-mode text under a labelled arrow's box at about 1.2:1 (A3 run, `ba3-hai-thang-nhat-quan`).
Do not turn them back into `<rect>`.

That same gate compares `getBBox()` boxes, which are in each element's local space, and Excalidraw wraps every text in a `<g transform="translate(..)">`.
So the tool moves each unrotated text group's translate into the text's own `x`/`y` (same pixels), and puts a `<rect>` in `--pre-bg`, inset 8 units under the rough outline, beneath each `code` block.
Without both, the light text of a `code` block was measured against the page and failed at 1.26:1 (ds3 run).
