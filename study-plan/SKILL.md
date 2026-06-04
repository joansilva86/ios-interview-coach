---
name: study-plan
description: >
  Analyzes the cumulative interview history and produces two outputs:
  (1) silently rewrites current_topics.txt (project root) with a fresh prioritized
  topic list derived from history, and (2) delivers progress feedback to the
  candidate — improvements, persistent gaps, regressions, and solid retention.
  Reads ONLY logs/interview_history.txt — no candidate personal info, no
  topic list dependency.
  Use when the candidate says "give me a study plan", "what should I focus on",
  "how am I doing", "progress feedback", or invokes /study-plan.
---

# Study Plan & Progress Feedback

You analyze the candidate's interview history and do two things:

1. **Silently rewrite `current_topics.txt`** (project root) — this becomes the new prioritized topic list for the next `/ios-interview` session.
2. **Deliver progress feedback** to the candidate — trends across sessions (improvements, persistent gaps, regressions, solid retention).

The candidate sees the feedback. The file write is silent (no commentary about it beyond a one-line summary at the end).

## Mandatory inputs

This skill reads **only one file**:

- **`logs/interview_history.txt`** — CSV with one row per (session, subtopic). Schema: `session_date, session_id, topic, subtopic, confidence, questions_asked, on_point_count, notes`. The cumulative record of all past sessions.

This skill does **not** access any other file. No personal info, no existing topic list, no current session log.

**If `logs/interview_history.txt` is missing or empty**: tell the candidate there's no history to base a plan on — they should run `/ios-interview` and `/save-progress` first. Do not write `current_topics.txt`.

## Prioritization logic (drives both outputs)

For each subtopic in history, compute a priority tier:

### Confidence (most recent row per subtopic)
- **`weak`** → high priority
- **`unknown`** → high priority (baseline never solidified)
- **`ok`** → medium priority if eroding (older rows show `strong` → now `ok`)
- **`strong`** → low priority unless 3+ weeks since last practice (retention check)
- **`skip`** → exclude entirely; the candidate marked it intentionally

### Recency / erosion (compare older rows to most recent)
- Confidence **regressed** across sessions (`strong` → `weak`, `ok` → `weak`) → bump up one tier
- Subtopic was `weak` in 3+ sessions in a row → bump to P0 (persistent gap)
- Subtopic just covered in latest session and now `strong` → drop one tier (already retained)

### Priority tiers
- **P0 (Critical)**: persistent gap (3+ sessions weak) OR significant regression (`strong` → `weak`)
- **P1 (High)**: currently `weak` or `unknown` (single occurrence) OR mild regression (`strong` → `ok`)
- **P2 (Medium)**: `ok` with notes indicating gaps
- **P3 (Low)**: `strong` retention refresh after 3+ weeks of no practice

## Output 1 (silent): rewrite `current_topics.txt`

After computing priorities, **replace** `current_topics.txt` (in the project root) entirely with a fresh CSV.

### Schema

```csv
category,subtopic,priority,notes
```

| Column | Description |
|--------|-------------|
| `category` | High-level topic group (e.g., "Architecture", "Swift Language", "Security") — taken from the `topic` column in history |
| `subtopic` | Specific topic (taken from `subtopic` column in history) |
| `priority` | `P0` \| `P1` \| `P2` \| `P3` — derived from the prioritization logic above |
| `notes` | Short description of why it's prioritized (e.g., "Persistent gap: inverted definitions in 3 sessions" or "Regressed from strong to weak") |

### Rules

- **Replace the entire file** with the new content (overwrite, not append).
- **One row per subtopic** that has been practiced at least once. Subtopics with confidence `skip` are excluded entirely.
- **Sort rows by priority** (P0 first, then P1, P2, P3), then by category alphabetically.
- **Quote any field** containing commas or double quotes per CSV rules (RFC 4180).
- **Do not include topics that haven't been practiced** — this skill only knows what's in history.

## Output 2 (to the user): progress feedback

After writing the file, deliver a structured progress report. This is the main user-facing output.

### Format

```
=== Progress Feedback ===

📈 Improvements
- [subtopic]: [old confidence] → [new confidence] (over N sessions)
- ...
(omit section if no improvements)

⚠️ Persistent gaps (3+ sessions weak)
- [subtopic]: [brief description of the gap from notes column]
- ...
(omit section if no persistent gaps)

📉 Regressions
- [subtopic]: [old confidence] → [new confidence] ([weeks/sessions] since last practice)
- ...
(omit section if no regressions)

✅ Solid retention
- [subtopic]: N sessions strong
- ...
(omit section if nothing is solidly retained)

---
current_topics.txt updated for next session: X P0 / Y P1 / Z P2 / W P3
```

### Content rules

- **Concrete, not generic.** Use actual subtopic names from history, not categories.
- **Quote notes from history** when describing gaps — anchor in real data, don't invent.
- **Keep each bullet to one line.** No multi-line analysis per bullet.
- **Omit empty sections.** If there are no regressions, don't write "📉 Regressions (none)".
- **No recommendations or study tasks.** The actionable next step is the updated `current_topics.txt` — `/ios-interview` will use it.
- **No verdict.** Don't say "qualifies" or "doesn't qualify" — that's a separate feedback skill's job.

## Do not

- **Never read** any file other than `logs/interview_history.txt`.
- **Never preserve** the old `current_topics.txt` content — this skill is the owner of that file. Replace, don't merge.
- **Never include subtopics not in history** in `current_topics.txt`. If the candidate wants to add a topic that hasn't been practiced yet, they edit the file manually.
- **Never deliver a verdict, recommendation, or study task list.** Progress feedback only.
- **Never run** if `logs/interview_history.txt` is missing or empty. Tell the candidate to run an interview and save progress first.
- **Never invent improvements, regressions, or retention claims** that aren't backed by rows in history.
