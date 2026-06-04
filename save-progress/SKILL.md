---
name: save-progress
description: >
  Persists the most recent interview session's data into the interview history CSV,
  then clears the working session log. Reads ONLY logs/current_interview.txt (does NOT
  access any candidate personal information). Appends ONE row per session to
  logs/interview_history.txt in WIDE/PIVOTED format — one column per (topic, subtopic),
  with notes only in the cells. Confidence and counts are NOT stored — they are inferred
  at read-time by /setup-session and /study-plan from the notes text. Save-only — no
  feedback, no verdict, no recommendations.
  Use when the candidate says "save the progress", "save the session",
  "save my interview", "log the session", or invokes /save-progress.
---

# Save Progress

You persist the most recent interview session's data into the cumulative history CSV. Your job is **append one row per session, not deliver feedback**. The user-facing output is a brief confirmation.

## When this skill runs

- After an `ios-interview` session has ended.
- Standalone invocation — not chained automatically.
- Output is a confirmation, not coaching or recommendations.

## Mandatory inputs (only these)

This skill reads:

- **`logs/current_interview.txt`** — The session to persist. Contains Q&A pairs with per-question categories (On Point / Could Be Better / Vague / Improvised / Don't Know) and notes per question.
- **`logs/interview_history.txt`** (if it exists) — to determine the next `session_id` and the existing column layout (subtopic columns to extend).

This skill does **NOT** read:
- `candidate-information/linkedIn.txt` (no personal information needed)
- `candidate-information/candidate_stories.md`
- `current_topics.txt`
- Any other personal data

## Output file format — wide/pivoted CSV

`logs/interview_history.txt` is a **wide CSV** with two header rows and one data row per session.

### Header layout

- **Row 1 (topic header)** — first two cells are empty (above `session_date` and `session_id`). Then one cell per subtopic column, containing the topic name (repeated when a topic spans multiple subtopic columns).
- **Row 2 (subtopic header)** — first two cells are `session_date` and `session_id`. Then one cell per subtopic column, containing the subtopic name.
- **Rows 3+ (session data)** — one row per session. First two cells are the session date and session id. Remaining cells contain the **notes** about that subtopic from that session, OR are empty if the subtopic was not touched.

### Example

```csv
,,Architecture,Architecture,Design Patterns,Swift Language
session_date,session_id,Repo vs Service vs UseCase,SwiftUI Navigation,Strategy,some vs any
2026-06-03,1,"Inverted definitions: Repo hits server (Service responsibility)","Chose Router without canonical pattern","Q2 On Point, Q6 same example, Q6b Don't Know","Correct intuition but missing mechanism"
2026-06-10,2,,"VM exposes @Published route, View observes — correct","","Now distinguishes opaque vs existential clearly"
```

### What goes in each cell

- **Cell content = the notes text only.** Encode confidence inside the notes by including the answer category words ("On Point", "Could Be Better", "Vague", "Improvised", "Don't Know") so downstream skills can infer confidence by reading the text.
- **Empty cell** = subtopic not touched in that session.
- **One column per (topic, subtopic) pair.** Subtopics with the same name under different topics are different columns.

## Workflow

1. **Read `logs/current_interview.txt`** in full.
2. **Determine `session_date`**: extract from the session header (e.g., `# Interview — 2026-06-04`). If missing, use today's date.
3. **Determine `session_id`**: count existing data rows in `logs/interview_history.txt` and add 1. If the file doesn't exist, `session_id = 1`.
4. **Group questions by (topic, subtopic)**: each Q&A pair has a topic and subtopic in its header (e.g., `### Q1 — Architecture / Repo vs Service vs UseCase`). Group across both main and experience Q&A sections.
5. **Compose a notes string per (topic, subtopic)**: combine the question(s) for that subtopic into one short summary (1–2 sentences). Include the answer-category words ("On Point", "Vague", "Don't Know", etc.) so confidence can be inferred from the text.
6. **Reconcile columns with existing file**:
   - If `logs/interview_history.txt` does NOT exist: write topic header row, subtopic header row, and the new session data row.
   - If file exists: read the existing topic + subtopic header rows. Identify which (topic, subtopic) pairs from this session are new. Append new columns to BOTH header rows AND to every existing data row (with empty cells). Then append the new session data row.
7. **Write the new session data row**: first cell = session_date, second cell = session_id, remaining cells = notes for subtopics covered this session, empty for everything else.
8. **Verify the append succeeded**: confirm the new row is present in `logs/interview_history.txt` before proceeding.
9. **Delete `logs/current_interview.txt`**: only after step 8 confirms the data is safely in history. This clears the working session log to make room for the next interview.
10. **Output confirmation** to the user (see below).

**Critical ordering rule**: NEVER delete `logs/current_interview.txt` before verifying the data was appended successfully. If the write fails, leave `current_interview.txt` intact so the data isn't lost.

## CSV escaping

Standard CSV (RFC 4180):
- Comma-separated.
- Double-quote any cell containing commas, quotes, or newlines.
- Escape internal double-quotes by doubling them (`"` → `""`).

## Idempotency

Before writing, check if a data row for the current `session_date` already exists in `logs/interview_history.txt`:
- If yes: ask the user "A session for [date] is already saved. Append anyway, replace that row, or cancel?"
- Default to **cancel** if the user doesn't respond.
- Don't silently duplicate.

## What the user sees (brief confirmation)

After appending to `logs/interview_history.txt` AND deleting `logs/current_interview.txt`, output ONLY this format:

```
✓ Session saved to logs/interview_history.txt
✓ logs/current_interview.txt cleared (ready for next session)

Session: YYYY-MM-DD (Session N)
Subtopics covered: M
New columns added: K
```

That's it. **No analysis, no verdict, no recommendations, no encouragement, no critique.**

If the user wants feedback or a study plan, they invoke a different skill.

## Do not

- **Never read `candidate-information/`** — this skill does not need personal info.
- **Never deliver a verdict** (qualifies / does not qualify).
- **Never give recommendations** or commentary on performance.
- **Never overwrite or delete data from past sessions** in `interview_history.txt`. Adding new subtopic columns to past rows means appending empty cells, not changing existing data.
- **Never delete `logs/current_interview.txt` before verifying** the append to `interview_history.txt` succeeded. Data loss risk is critical here — verify, then delete.
- **Never invent data**. If a Q&A pair is ambiguous (no clear topic/subtopic), skip it and note in the confirmation that N questions were skipped.
- **Never run** if `logs/current_interview.txt` is missing or empty — tell the user there's nothing to save and stop.
- **Never silently duplicate** session rows. Check for existing session_date before appending.
- **Never modify the CSV schema** without updating this SKILL.md first.
- **Never delete any file other than `logs/current_interview.txt`**. This skill cleans up only the working session log.
- **Never write a confidence column or counts columns.** Confidence is encoded in the notes text and inferred downstream.
