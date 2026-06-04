---
name: setup-session
description: >
  Reads logs/interview_history.csv and rewrites current_topics.txt with a fresh
  prioritized topic list for the next interview session. Pure file-write skill —
  no progress feedback, no analysis output, just a brief confirmation. For
  human-readable progress feedback, use /study-plan.
  Use when the candidate says "setup the next session", "prepare topics for the
  next interview", "refresh the topic list", or invokes /setup-session.
---

# Setup Session

You rewrite `current_topics.txt` (project root) based on the cumulative interview history. This skill is **file-write only** — no analysis, no progress feedback, no recommendations. The candidate sees a brief confirmation.

For human-readable progress analysis (trends, regressions, retention), the candidate should use `/study-plan`. This skill produces the input for the next `/ios-interview` session.

## Mandatory inputs

This skill reads **only one file**:

- **`logs/interview_history.csv`** — Wide/pivoted CSV with TWO header rows (topic row, then subtopic row with `session_date,session_id,...` prefix) and one row per session. Cells contain the notes text for that (session, subtopic), or are empty if the subtopic was not touched that session.

This skill does **not** access any other file. No personal info, no existing `current_topics.txt`, no current session log.

**If `logs/interview_history.csv` is missing or empty** (header only, no data rows): tell the candidate there's no history to base topic prep on — they should run `/ios-interview` and `/save-progress` first. Do not write `current_topics.txt`.

## Inferring confidence from notes (read-time)

Confidence is **NOT stored** in the history file. You must infer it from the notes text by scanning for answer-category keywords:

| Keywords in cell | Inferred confidence |
|---|---|
| Only "On Point" mentioned, no negative keywords | `strong` |
| Mix of "On Point" and "Could Be Better", no Vague/Improvised/Don't Know | `ok` |
| Any "Vague", "Improvised", "Don't Know" | `weak` |
| Cell empty | not asked this session — no signal |

If a cell is ambiguous (no answer-category keywords), default to `ok` and continue.

## Prioritization logic

For each (topic, subtopic) column in history, walk the cells across sessions chronologically and compute a priority tier:

### Confidence (most recent non-empty cell per subtopic)
- **`weak`** → high priority
- **`ok`** → medium priority if eroding (older cells `strong` → now `ok`)
- **`strong`** → low priority unless 3+ sessions since last practice (retention check)

### Recency / erosion
- Confidence **regressed** across sessions (`strong` → `weak`, `ok` → `weak`) → bump up one tier
- Subtopic was `weak` in 3+ sessions in a row → bump to P0 (persistent gap)
- Subtopic just covered in latest session and now `strong` → drop one tier (already retained)

### Priority tiers
- **P0 (Critical)**: persistent gap (3+ sessions weak) OR significant regression (`strong` → `weak`)
- **P1 (High)**: currently `weak` (single occurrence) OR mild regression (`strong` → `ok`)
- **P2 (Medium)**: `ok` with notes indicating gaps
- **P3 (Low)**: `strong` retention refresh after 3+ sessions of no practice

## Output (silent file write)

Replace `current_topics.txt` (project root) entirely with a fresh CSV.

### Schema

```csv
category,subtopic,priority,notes
```

| Column | Description |
|--------|-------------|
| `category` | Topic group taken from the topic header row of history |
| `subtopic` | Subtopic taken from the subtopic header row of history |
| `priority` | `P0` \| `P1` \| `P2` \| `P3` — derived from the prioritization logic above |
| `notes` | Short description of why it's prioritized (e.g., "Persistent gap: inverted definitions in 3 sessions" or "Regressed from strong to weak") |

### Write rules

- **Replace the entire file** with the new content (overwrite, not append).
- **One row per (topic, subtopic) column** that has at least one non-empty cell in history.
- **Sort rows by priority** (P0 first, then P1, P2, P3), then by category alphabetically within each priority tier.
- **Quote any field** containing commas or double quotes per CSV rules (RFC 4180).
- **Do not include subtopics with no history data** — this skill only knows what's been practiced.
- **Every `(category, subtopic)` row written must exist as a column in `topic_catalog.csv`.** History columns are already bounded by the catalog (save-progress validates that), so this is automatic — but if you ever see a mismatch, treat it as a catalog reconciliation bug and surface it instead of silently writing.
- **Respect catalog flags** (row 3 of `topic_catalog.csv`):
  - Skip subtopics flagged `ignore` or `deferred` — they don't appear in `current_topics.txt` regardless of their history.
  - For `mastered` subtopics: cap at P3 (retention refresh) even if history would suggest higher priority. The user has marked them mastered for a reason.
  - For `pending` subtopics: keep the priority derived from history, but append `"(catalog flag: pending review)"` to the `notes` column so the candidate is reminded.
  - `active` subtopics: priority derived purely from history per the rules above.

## User-facing output (the only thing the candidate sees)

After writing the file, output ONLY this format:

```
✓ current_topics.txt updated for next session

  P0 (critical): N topics
  P1 (high):     M topics
  P2 (medium):   K topics
  P3 (low):      W topics

  Total: T topics

For progress feedback, run /study-plan.
```

That's it. **No analysis, no regression details, no recommendations, no commentary.** If the candidate wants insights about their progress, they invoke `/study-plan`.

## Do not

- **Never read** any file other than `logs/interview_history.csv`.
- **Never deliver progress feedback** — improvements, regressions, retention analysis. Those belong to `/study-plan`.
- **Never preserve** the old `current_topics.txt` content — this skill owns that file. Replace, don't merge.
- **Never include subtopics not in history** in `current_topics.txt`. If the candidate wants to add a topic that hasn't been practiced yet, they edit the file manually.
- **Never deliver a verdict or recommendation.**
- **Never run** if `logs/interview_history.csv` is missing or empty (no data rows).
- **Never invent priority decisions** that aren't backed by data in history.
