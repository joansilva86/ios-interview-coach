---
name: setup-session
description: >
  Reads logs/interview_history.txt and rewrites current_topics.txt with a fresh
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

- **`logs/interview_history.txt`** — CSV with one row per (session, subtopic). Schema: `session_date, session_id, topic, subtopic, confidence, questions_asked, on_point_count, notes`. The cumulative record of all past sessions.

This skill does **not** access any other file. No personal info, no existing `current_topics.txt`, no current session log.

**If `logs/interview_history.txt` is missing or empty**: tell the candidate there's no history to base topic prep on — they should run `/ios-interview` and `/save-progress` first. Do not write `current_topics.txt`.

## Prioritization logic

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

## Output (silent file write)

Replace `current_topics.txt` (project root) entirely with a fresh CSV.

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

### Write rules

- **Replace the entire file** with the new content (overwrite, not append).
- **One row per subtopic** that has been practiced at least once. Subtopics with confidence `skip` are excluded entirely.
- **Sort rows by priority** (P0 first, then P1, P2, P3), then by category alphabetically within each priority tier.
- **Quote any field** containing commas or double quotes per CSV rules (RFC 4180).
- **Do not include topics that haven't been practiced** — this skill only knows what's in history.

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

- **Never read** any file other than `logs/interview_history.txt`.
- **Never deliver progress feedback** — improvements, regressions, retention analysis. Those belong to `/study-plan`.
- **Never preserve** the old `current_topics.txt` content — this skill owns that file. Replace, don't merge.
- **Never include subtopics not in history** in `current_topics.txt`. If the candidate wants to add a topic that hasn't been practiced yet, they edit the file manually.
- **Never deliver a verdict or recommendation.**
- **Never run** if `logs/interview_history.txt` is missing or empty.
- **Never invent priority decisions** that aren't backed by rows in history.
