# Evals

Each folder is one case for `claude plugin eval`: `prompt.md` is the task, `case.yaml` the expected outcome, `graders/` the checks.
The prompts are Vietnamese on purpose: the skill draws for Vietnamese readers.

## What the cases measure

The tool in `scripts/ve.py` already catches visible errors (overflow, crossings, text size).
The cases measure what it cannot: whether the figure says the right thing, and whether its reader understands it.

| Case | Source | Reader | Main question |
|---|---|---|---|
| `kafka-lag-partition`, `mvcc-isolation-level`, `oom-killer-137` | Technical lesson | Developer | Does the figure show the mechanism with real values? |
| `ghi-chu-ca-nhan`, `giang-day-khai-niem`, `quy-trinh-to-chuc`, `y-tuong-kinh-doanh` | Rough idea, note, process | Varies | Does the figure show the writer's idea in the writer's words? |
| `nguoi-moi-mat-khau-salt` | Security-adjacent article | Newcomer (parents, high school students) | Can a reader who never programmed answer three questions from the image alone? |

Two kinds of grader:

- **Figure quality** (most graders): files produced, not boxes-and-arrows, real values, color discipline, legible in the column, shows the mechanism or idea.
- **Reader understanding** (`nguoi-moi-mat-khau-salt`): the judge is shown the rendered PNG itself, not the trace, and answers as the named reader.
  `03-newcomer-retell` asks the three questions the article answers; it passes only if a parent can read the answers off the image in words the image gives.
  `04-terms-explained` fails any technical term shown with only its name.
  This is the measured form of the retell test in `references/review.md`.
  `07-premises-stated` does not ask whether a term has a gloss: the judge lists what the figure takes for granted, and fails any step that cannot be followed without something the figure never says, such as a rule of how a part normally works.
  It is the measured form of Part B of the fresh-eyes review in `references/review.md`, which is what a Java team's feedback on the Java4Shell figures showed a term check alone could not catch.

`05-mechanism-not-howto` checks the security rule in `SKILL.md`: mechanism and defence, no cracking instructions.

## Controlled comparison: with the skill and without it

A score alone says little: a strong model draws a decent figure without any skill.
What the skill is worth is the difference between the same case run with it and without it.

`claude plugin eval` runs that comparison itself.

**Known blocker on macOS (checked 2026-11-24, Claude Code 2.1.330):** the eval runs the agent in a sandbox where no Chromium can start.
Four smoke runs of `nguoi-moi-mat-khau-salt` all stopped at the render step: the sandbox blocks the download, hides `~/Library/Caches/ms-playwright`, makes the installed Chrome fail with `ProcessSingleton`, and kills a headless Chromium at launch with `bootstrap_check_in ... MachPortRendezvousServer: Permission denied`.
The skill loaded and the agent wrote a spec each time, so `02-skill-fired` passed and the case scored 1/9; every grader that needs the PNG failed with "path does not exist".
Until the eval sandbox allows a browser, scores from these cases measure the eval environment, not the skill.
Run them where Chromium can start (Linux CI is the next thing to try, unverified), or judge the figures by hand with the graders' text as the rubric.

From the repo root:

```bash
claude plugin eval . --allow-tools Bash Write Edit --ablation with-without --runs 3
```

- The target `.` is this repo: the eval loads it as the skill (`02-skill-fired` passes) and reads the cases from `evals/`. An installed copy works too: `claude plugin eval drawing-excalidraw-figures@skills-dir ...`.
- `--allow-tools Bash Write Edit` is required. Those tools are gated: `allowed_tools` in `prompt.md` asks for them, but only this flag grants them. Without it the agent cannot write the spec or run `ve.py`, every file grader fails, and the case scores 1/9 (the tool prints "cannot pass with the granted tools" before the run).
- The first run asks you to trust the folder; `--trust-plugin` answers it for CI.
- `--case nguoi-moi-mat-khau-salt --runs 1 --ablation none` is the cheap smoke run (one agent run; the four blocked runs above cost 0.6 to 1.4 USD each).
- `--ablation with-without` runs every case twice: once with the skill loaded (`WITH`) and once with no skill (`W/OUT`). The report adds `Δ` = with minus without; a positive `Δ` means the skill raised the score.
- `--runs 3` repeats each arm; the case score is the mean, so one lucky run does not decide it.
- `02-skill-fired` (`tool_used: Skill`) is reported as an indicator, not scored, in a two-arm run: it confirms the with-arm actually used the skill.
- Results land in `results/<timestamp>/`: `report.html` for reading, `aggregate-result.json` for numbers (`aggregates.meanDelta`, `cases[].aggregates.delta`).

Read the `Δ` per grader, not only per case.
A skill that raises "legible in column" but not "newcomer retell" helps the drawing, not the teaching, and the next change belongs in the workflow (step 1), not in the tool.

## Adding a case

- Give the output a fixed name in the prompt (`Đặt tên spec là ...`), so image graders can point at `hinh-ve/<name>-light.png`.
- An `llm` grader sees an image when its `focus` is that file: `focus: { source: file, path: hinh-ve/<name>-light.png }`. With `focus: trace` it only sees the first and last messages of the run.
- Write each `llm` grader as `PASS if ...` / `FAIL if ...`, one property per grader, so a failure names one thing to fix.
- For a reader-understanding grader, name the reader and what they do NOT know, then ask questions whose answers are in the source.
- Record what a run taught in `references/lessons-from-runs.md`.
