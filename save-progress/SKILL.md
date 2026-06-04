---
name: save-progress
description: >
  Persists the most recent interview session's data into the interview history CSV,
  then clears the working session log. Reads ONLY logs/current_interview.txt (does NOT
  access any candidate personal information). Appends one row per topic touched in the
  session to logs/interview_history.txt (CSV format), then deletes logs/current_interview.txt
  to make room for the next session. Save-only — no feedback, no verdict, no recommendations.
  Use when the candidate says "save the progress", "save the session",
  "save my interview", "log the session", or invokes /save-progress.
---

# Save Progress

You are persisting the most recent interview session's data into the cumulative history CSV. Your job is **append rows, not deliver feedback**. The user-facing output is a brief confirmation.

## When this skill runs

- After an `ios-interview` session has ended.
- Standalone invocation — not chained automatically.
- Output is a confirmation, not coaching or recommendations.

## Mandatory inputs (only these)

This skill reads **only one file**:

- **`logs/current_interview.txt`** — The session to persist. Contains Q&A pairs with per-question categories (On Point / Could Be Better / Vague / Improvised / Don't Know) and notes per question.

This skill does **NOT** read:
- `candidate-information/linkedIn.txt` (no personal information needed)
- `candidate-information/candidate_stories.md`
- Any other personal data

The skill operates purely on session Q&A data — anonymous to candidate identity.

## Output file

- **`logs/interview_history.txt`** — Cumulative history in **CSV format**. Append new rows. Never modify or delete existing rows.

## CSV format

The file uses standard CSV (RFC 4180):
- Comma-separated
- Double-quote any field containing commas, quotes, or newlines
- Escape internal double-quotes by doubling them (`"` → `""`)
- First row is the header

### Schema (columns)

| Column | Type | Description |
|--------|------|-------------|
| `session_date` | `YYYY-MM-DD` | Date of the interview session |
| `session_id` | integer | Incrementing session number (1, 2, 3, …). Determine by counting unique `session_date` values already in the file + 1. |
| `topic` | string | High-level category (e.g., "Swift Language", "Architecture", "Security", "Testing", "Swift Concurrency"). Use the question categories listed in `ios-interview/SKILL.md`. |
| `subtopic` | string | Specific topic within the category (e.g., "some vs any", "MVVM Navigation", "Keychain accessibility") |
| `confidence` | enum | `strong` \| `ok` \| `weak` \| `unknown` \| `skip` — derived from per-question categories (see rollup rules below). `skip` is only set manually by the user (replaces the previous `🟢 skip` convention) — this skill never writes `skip`. |
| `questions_asked` | integer | Number of questions about this subtopic this session |
| `on_point_count` | integer | Number of those questions answered "On Point" |
| `notes` | string (quoted) | Brief description of the gap, what was missing, what was confused. 1–2 sentences. Quote-escape as needed. |

### Header row (write once if file is new)

```csv
session_date,session_id,topic,subtopic,confidence,questions_asked,on_point_count,notes
```

### Example rows

```csv
2026-06-04,14,Architecture,Repo vs Service vs UseCase,weak,1,0,"Inverted definitions: said Repo returns DTOs, Service returns domain — should be opposite"
2026-06-04,14,Design Patterns,Strategy,strong,1,1,"First time generating own example from real experience"
2026-06-04,14,Swift Language,some vs any,weak,1,0,"Doesn't know opaque vs existential mechanism"
2026-06-04,14,Security,Keychain token storage,weak,1,0,"Chose Keychain but missing kSecAttrAccessible values and Secure Enclave"
```

## Confidence rollup (per-question → per-subtopic)

For each subtopic touched in the session, roll up the per-question categories:

| Per-question signal | Confidence |
|---------------------|------------|
| All questions **On Point** | `strong` |
| Mix of **On Point** and **Could Be Better**, no Vague/Improvised/Don't Know | `ok` |
| Any **Vague**, **Improvised**, or **Don't Know** | `weak` |
| Subtopic not asked about in any question | do not write a row for it |

`unknown` is reserved for subtopics the candidate has never been asked — this skill should not emit `unknown` rows since it only writes about topics that ARE in the current session.

## Workflow

1. **Read `logs/current_interview.txt`** in full.
2. **Determine `session_date`**: extract from the session header (e.g., `# Interview — 2026-06-04`). If missing, use today's date.
3. **Determine `session_id`**: read `logs/interview_history.txt`, count unique `session_date` values, add 1. If the file doesn't exist, `session_id = 1`.
4. **Group questions by (topic, subtopic)**: each Q&A pair has a topic and subtopic in its header (e.g., `### Q1 — Architecture / Repo vs Service vs UseCase`).
5. **Roll up each group** into a single row using the confidence table above.
6. **Compose CSV rows** with proper quoting.
7. **Append to `logs/interview_history.txt`**:
   - If file doesn't exist: create it with the header row, then append data rows.
   - If file exists: append data rows only (no duplicate header).
8. **Verify the append succeeded**: confirm the new rows are present in `logs/interview_history.txt` before proceeding.
9. **Delete `logs/current_interview.txt`**: only after step 8 confirms the data is safely in history. This clears the working session log to make room for the next interview.
10. **Output confirmation** to the user (see below).

**Critical ordering rule**: NEVER delete `logs/current_interview.txt` before verifying the data was appended successfully. If step 7 fails, leave `current_interview.txt` intact so the data isn't lost.

## Idempotency

Before writing, check if rows for the current `session_date` already exist in `logs/interview_history.txt`:
- If yes: ask the user "A session for [date] is already saved (N rows). Append anyway, replace those rows, or cancel?"
- Default to **cancel** if the user doesn't respond.
- Don't silently duplicate.

## What the user sees (the brief confirmation)

After appending to `logs/interview_history.txt` AND deleting `logs/current_interview.txt`, output ONLY this format:

```
✓ Session saved to logs/interview_history.txt
✓ logs/current_interview.txt cleared (ready for next session)

Session: YYYY-MM-DD (Session N)
Rows appended: M
Topics covered: [comma-separated list, max 8]
Confidence distribution: X strong, Y ok, Z weak
```

That's it. **No analysis, no verdict, no recommendations, no encouragement, no critique.**

If the user wants feedback or a study plan, they invoke a different skill.

## Do not

- **Never read `candidate-information/`** — this skill does not need personal info.
- **Never deliver a verdict** (qualifies / does not qualify).
- **Never give recommendations** or commentary on performance.
- **Never overwrite or delete existing rows in `interview_history.txt`**. Append-only.
- **Never delete `logs/current_interview.txt` before verifying** the append to `interview_history.txt` succeeded. Data loss risk is critical here — verify, then delete.
- **Never invent data**. If a Q&A pair is ambiguous (no clear topic/subtopic), skip it and note in the confirmation that N questions were skipped.
- **Never run** if `logs/current_interview.txt` is missing or empty — tell the user there's nothing to save and stop.
- **Never silently duplicate** session rows. Check for existing session_date before appending.
- **Never modify the CSV schema** without updating this SKILL.md first.
- **Never delete any file other than `logs/current_interview.txt`**. This skill cleans up only the working session log.
