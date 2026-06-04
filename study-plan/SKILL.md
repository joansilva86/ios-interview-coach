---
name: study-plan
description: >
  Reads logs/interview_history.txt and delivers progress feedback about the
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

- **`logs/interview_history.txt`** — CSV with one row per (session, subtopic). Schema: `session_date, session_id, topic, subtopic, confidence, questions_asked, on_point_count, notes`. The cumulative record of all past sessions.

This skill does **not** access any other file. No personal info, no topic list, no current session log.

**If `logs/interview_history.txt` is missing or empty**: tell the candidate there's no history to analyze — they should run `/ios-interview` and `/save-progress` first. Then exit.

## Analysis logic

For each subtopic in history, compute its trend by comparing rows across sessions:

### Categorization

- **Improvement**: confidence went from `weak`/`unknown` → `ok`/`strong` over 2+ sessions
- **Persistent gap**: subtopic was `weak` in 3+ sessions in a row (current approach not working)
- **Regression**: confidence went from `strong` → `ok`/`weak`, or `ok` → `weak` (recall is fading)
- **Solid retention**: subtopic has been `strong` in 2+ recent sessions

### Confidence priorities (for context, not for prioritizing the report)
- `weak` / `unknown` → current gaps
- `ok` → middle ground, may or may not be at risk
- `strong` → retained
- `skip` → excluded from analysis entirely (the candidate marked it intentionally)

## Output format

Deliver a structured report. Use this exact format:

```
=== Progress Feedback ===

📈 Improvements
- [subtopic]: [old confidence] → [new confidence] (over N sessions)
- ...
(omit section if no improvements)

⚠️ Persistent gaps (3+ sessions weak)
- [subtopic]: [brief description from the notes column]
- ...
(omit section if no persistent gaps)

📉 Regressions
- [subtopic]: [old confidence] → [new confidence] ([N sessions / weeks] since)
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
- **Quote notes from history** when describing gaps — anchor in real data, don't invent.
- **Keep each bullet to one line.** No multi-line analysis per bullet.
- **Omit empty sections.** If there are no regressions, don't include the heading.
- **No recommendations or study tasks.** This skill is feedback only.
- **No verdict.** Don't say "qualifies" or "doesn't qualify" — that's a separate feedback skill's job (if/when created).

## Do not

- **Never read** any file other than `logs/interview_history.txt`.
- **Never write or modify any file.** This is a pure analysis skill.
- **Never deliver a verdict, recommendation, or study task list.** Trend feedback only.
- **Never run** if `logs/interview_history.txt` is missing or empty.
- **Never invent improvements, regressions, or retention claims** that aren't backed by rows in history.
- **Never rewrite `current_topics.txt`** — that's `/setup-session`'s job.
