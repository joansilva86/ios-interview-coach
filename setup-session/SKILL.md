---
name: setup-session
description: >
  Selects exactly 10 subtopics for the next interview by combining the
  topic_catalog.csv (source of truth, with flags) and logs/interview_history.csv
  (past sessions), then writes them to current_topics.txt as the ordered queue
  ios-interview will walk through. Pure file-write skill — no progress feedback,
  no analysis output, just a brief confirmation. For human-readable progress
  feedback, use /study-plan.
  Use when the candidate says "setup the next session", "prepare topics for the
  next interview", "pick what to ask next", or invokes /setup-session.
---

# Setup Session

You select **exactly 10 subtopics** for the next interview session and write them to `current_topics.txt`. `ios-interview` will then ask one question per row, in order, for exactly 10 questions. This skill is **file-write only** — no analysis, no progress feedback, no recommendations beyond a brief confirmation.

For human-readable progress analysis (trends, regressions, retention), the candidate should use `/study-plan`.

## Mandatory inputs

This skill reads **two files**:

- **`topic_catalog.csv`** (project root, tracked) — source of truth. Wide CSV with 3 rows: topics, subtopics, flag (`active|pending|ignore|deferred|mastered`). Every column is a valid `(topic, subtopic)` pair. Flags filter eligibility.
- **`logs/interview_history.csv`** (optional) — Wide/pivoted CSV with two header rows (topics, then `session_date,session_id,...subtopics`) and one row per past session. Cells contain notes; empty cells mean the subtopic wasn't touched that session.

This skill does **NOT** access any other file. No personal info, no existing `current_topics.txt` (it gets overwritten), no current session log.

**Cold-start behavior**: if `logs/interview_history.csv` is missing or empty (header only, no data rows), proceed using the catalog only — pick 10 subtopics from Pool C (see below). Do NOT refuse to run on empty history.

## Inferring confidence from notes (read-time)

Confidence is **NOT stored** in the history file. Infer it from the notes text in each cell by scanning for answer-category keywords:

| Keywords in cell | Inferred confidence |
|---|---|
| Only "On Point" mentioned, no negative keywords | `strong` |
| Mix of "On Point" and "Could Be Better", no Vague/Improvised/Don't Know | `ok` |
| Any "Vague", "Improvised", "Don't Know" | `weak` |
| Cell empty | not asked this session — no signal |

If a cell is ambiguous (no answer-category keywords), default to `ok`.

## Selection algorithm — gap-first, then variety

Pick exactly 10 subtopics by walking these pools in order. Each subtopic enters at most one pool; once placed, it's locked.

**Exclude up front**: any catalog column flagged `ignore` or `deferred`. They are not eligible for any pool.

### Pool A — Persistent gaps (priority P0)
Subtopics with history where the most recent 3+ non-empty cells are all `weak`. Sort by most-recent-weak first. Cap at 10. Drop later pools if Pool A fills all 10.

### Pool B — Recent weak / regressions (priority P1)
Subtopics where one of these is true:
- Most recent non-empty cell is `weak` (single occurrence).
- Confidence regressed across sessions: `strong → ok`, `strong → weak`, or `ok → weak`.

Sort by most-recent-weak first. Take up to (10 − count so far).

### Pool C — Never-asked catalog subtopics (priority P2)
Catalog columns with flag in `{active, pending}` AND no non-empty cells in history.

Sort by:
1. Role-critical category first (`Security`, `Autonomy`, `Environments`).
2. Balanced spread across other categories — round-robin one per category until full, rather than packing many from the same category.
3. Tie-break alphabetically by subtopic.

Take up to (10 − count so far).

### Pool D — Retention refresh (priority P3)
Catalog columns flagged `mastered` that haven't been asked in 3+ sessions (or never asked). Take **at most 1** from this pool, only if there's room and only as the final slot.

### After all pools
If fewer than 10 subtopics are picked (catalog too small or too restrictive), write what you have and include an explicit warning in the confirmation message (see Output).

## Output (silent file write)

Replace `current_topics.txt` (project root) entirely. **Regenerate from scratch — no warning, no preservation of prior content.**

### Schema (unchanged)

```csv
category,subtopic,priority,notes
```

| Column | Description |
|--------|-------------|
| `category` | Topic from `topic_catalog.csv` row 1, matching the picked column. |
| `subtopic` | Subtopic from `topic_catalog.csv` row 2, matching the picked column. |
| `priority` | `P0` \| `P1` \| `P2` \| `P3` — derived from which pool placed the subtopic. |
| `notes` | Short explanation: why this was picked. Example values: `"Persistent gap: weak in last 3 sessions"`, `"Regressed strong→weak last session"`, `"Never asked; role-critical (Security)"`, `"Retention check; mastered, not asked in 5 sessions"`. For `pending` catalog-flagged subtopics, append `" (catalog flag: pending review)"`. |

### Write rules

- **Exactly 10 rows**, in queue order (P0 first, then P1, P2, P3 — same order ios-interview will ask them).
- Within the same priority tier, keep the pool's internal sort order (most-recent-weak first for Pools A/B; role-critical-first then round-robin for Pool C).
- **Quote any field** containing commas or double quotes (RFC 4180).
- **Every row must exist as a column in `topic_catalog.csv`** — never invent.
- **No duplicates** — each `(category, subtopic)` pair appears at most once.
- If fewer than 10 are available, write fewer (do not pad with anything).

## User-facing output (the only thing the candidate sees)

After writing the file, output ONLY this format:

```
✓ current_topics.txt updated — 10 subtopics queued for next session

  P0 (persistent gaps):  N
  P1 (recent weak):      M
  P2 (new / breadth):    K
  P3 (retention check):  W

For progress feedback, run /study-plan.
Then run /ios-interview to start the session.
```

If fewer than 10 were picked, replace the first line with:

```
⚠ current_topics.txt updated — only J subtopics available (catalog too restrictive or fully covered)
```

That's it. **No analysis, no regression details, no recommendations, no commentary.** If the candidate wants insights about their progress, they invoke `/study-plan`.

## Do not

- **Never read** any file other than `topic_catalog.csv` and `logs/interview_history.csv`.
- **Never deliver progress feedback** — improvements, regressions, retention analysis. Those belong to `/study-plan`.
- **Never preserve** the old `current_topics.txt` content — this skill owns that file. Replace, don't merge. Don't ask before overwriting.
- **Never include subtopics not in `topic_catalog.csv`** — the catalog is the bound.
- **Never include subtopics flagged `ignore` or `deferred`** — they are off-limits.
- **Never pick more than 1 from Pool D (retention)** in a single session.
- **Never pick more than 10 total** — the queue size is fixed.
- **Never deliver a verdict or recommendation.**
- **Never invent picking reasons** that aren't backed by the catalog flag or the history data.
