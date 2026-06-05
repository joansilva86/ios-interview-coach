---
name: study-plan
description: >
  Reads logs/interview_history.csv and delivers progress feedback about the
  candidate's learning across all sessions — improvements, persistent gaps,
  regressions, and solid retention. Pure analysis skill — does NOT write any
  files. For topic preparation of the next session, use /setup-session.
  Use when the candidate says "give me progress feedback", "how am I doing",
  "show me my progress", or invokes /study-plan.
---

# Progress Feedback

You analyze the candidate's cumulative interview history and deliver a structured progress report. This skill is **read-only** — it does not write any files.

For preparing topics for the next interview session, the candidate should use `/setup-session`. This skill only delivers the human-readable analysis.

## Mandatory inputs

This skill reads **only one file**:

- **`logs/interview_history.csv`** — Wide/pivoted CSV with TWO header rows (topic row, then subtopic row with `session_date,session_id,...` prefix) and one row per session. Cells contain the notes text for that (session, subtopic), or are empty if the subtopic was not touched that session.

This skill does **not** access any other file. No personal info, no topic list, no current session log.

**If `logs/interview_history.csv` is missing or empty** (header only, no data rows): tell the candidate there's no history to analyze — they should run `/ios-interview` and `/save-progress` first. Then exit.

## Reading confidence from cells

Each non-empty cell in `interview_history.csv` is one of exactly five labels (written by `/save-progress`):

| Cell value | Confidence bucket (internal) |
|---|---|
| `On Point` | strong |
| `Could Be Better` | ok |
| `Vague` | weak |
| `Improvised` | weak |
| `Don't Know` | weak |
| (empty cell) | skip when computing trend |

The bucket drives trend categorization below. The report itself can reference the literal label when useful (e.g., "Property Wrappers: Don't Know → Could Be Better").

## Analysis logic

For each (topic, subtopic) column in history, walk the non-empty cells across sessions chronologically and compute its trend:

### Categorization

- **Improvement**: inferred confidence went from `weak` → `ok`/`strong` over 2+ sessions
- **Persistent gap**: subtopic was `weak` in 3+ sessions in a row (current approach not working)
- **Regression**: inferred confidence went from `strong` → `ok`/`weak`, or `ok` → `weak` (recall is fading)
- **Solid retention**: subtopic has been `strong` in 2+ recent non-empty cells

## Output format

Deliver a structured report. Use this exact format:

```
=== Progress Feedback ===

📈 Improvements
- [subtopic]: [old confidence] → [new confidence] (over N sessions)
- ...
(omit section if no improvements)

⚠️ Persistent gaps (3+ sessions weak)
- [subtopic]: weak in N consecutive sessions (most recent label: [label])
- ...
(omit section if no persistent gaps)

📉 Regressions
- [subtopic]: [old confidence] → [new confidence] (N sessions since)
- ...
(omit section if no regressions)

✅ Solid retention
- [subtopic]: N sessions strong
- ...
(omit section if nothing is solidly retained)

---
For next session topic prep, run /setup-session.
```

## Content rules

- **Concrete, not generic.** Use actual subtopic names from history, not categories.
- **Reference cell labels directly** when describing gaps (e.g., "Property Wrappers: Don't Know in S1 → Could Be Better in S3"). Notes are no longer stored; the label is the data.
- **Keep each bullet to one line.** No multi-line analysis per bullet.
- **Omit empty sections.** If there are no regressions, don't include the heading.
- **No recommendations or study tasks.** This skill is feedback only.
- **No verdict.** Don't say "qualifies" or "doesn't qualify" — that's a separate feedback skill's job (if/when created).

## Do not

- **Never read** any file other than `logs/interview_history.csv`.
- **Never write or modify any file.** This is a pure analysis skill.
- **Never deliver a verdict, recommendation, or study task list.** Trend feedback only.
- **Never run** if `logs/interview_history.csv` is missing or empty (no data rows).
- **Never invent improvements, regressions, or retention claims** that aren't backed by data in history.
- **Never rewrite `current_topics.csv`** — that's `/setup-session`'s job.
