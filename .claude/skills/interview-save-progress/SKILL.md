---
name: interview-save-progress
description: >
  Persists the most recent interview session's data into the interview history CSV,
  then clears the working session log. Reads logs/current_interview.txt and
  logs/interview_history.csv (does NOT access the catalog or any personal information).
  Appends ONE row per session to logs/interview_history.csv in WIDE/PIVOTED format —
  one column per (topic, subtopic). Cell content = the answer-category label only
  (On Point | Could Be Better | Vague | Improvised | Don't Know). No notes, no rollup,
  no confidence inference downstream — labels are read directly. Save-only — no
  feedback, no verdict, no recommendations.
  Use when the candidate says "save the progress", "save the session",
  "save my interview", "log the session", or invokes /interview-save-progress.
---

# Save Progress

You persist the most recent interview session's data into the cumulative history CSV. Your job is **append one row per session, not deliver feedback**. The user-facing output is a brief confirmation.

## When this skill runs

- Standalone invocation — not chained automatically.
- Output is a confirmation, not coaching or recommendations.

## Mandatory inputs (only these)

This skill reads **only two files**:

- **`logs/current_interview.txt`** — The session to persist. Contains Q&A pairs with per-question categories (On Point / Could Be Better / Vague / Improvised / Don't Know) and notes per question.
- **`logs/interview_history.csv`** (if it exists) — to determine the next `session_id` and the existing column layout (subtopic columns to extend).

This skill does **NOT** read:
- `topic_catalog.csv` — the chain of trust handles catalog bounds: `/interview-setup-session` produces a catalog-bounded `current_topics.csv`, `/interview-run` uses those names verbatim in question headers, so by the time save-progress sees `current_interview.txt` the names are already catalog-aligned. No re-validation here.
- `candidate-information/linkedIn.txt` (no personal information needed)
- `candidate-information/candidate_stories.md`
- `current_topics.csv`
- Any other file

## Output file format — wide/pivoted CSV

`logs/interview_history.csv` is a **wide CSV** with two header rows and one data row per session.

### Header layout

- **Row 1 (topic header)** — first two cells are empty (above `session_date` and `session_id`). Then one cell per subtopic column, containing the topic name (repeated when a topic spans multiple subtopic columns).
- **Row 2 (subtopic header)** — first two cells are `session_date` and `session_id`. Then one cell per subtopic column, containing the subtopic name.
- **Rows 3+ (session data)** — one row per session. First two cells are the session date and session id. Remaining cells contain the **notes** about that subtopic from that session, OR are empty if the subtopic was not touched.

### Example

```csv
,,Architecture,Architecture,Design Patterns,Swift Language
session_date,session_id,Repository Pattern,SwiftUI Navigation,Strategy,some vs any
2026-06-03,1,Improvised,Could Be Better,On Point,Don't Know
2026-06-10,2,On Point,Could Be Better,,On Point
```

### What goes in each cell

- **Cell content = the answer-category label, nothing else.** One of exactly five values: `On Point`, `Could Be Better`, `Vague`, `Improvised`, `Don't Know`. No notes, no explanations, no quoted text. Downstream skills read the label directly — no inference needed.
- **Empty cell** = subtopic not touched in that session.
- **One column per (topic, subtopic) pair.** Subtopics with the same name under different topics are different columns.
- **Since `/interview-run` is strict 1:1** (one question per subtopic, no follow-ups), each cell maps to exactly one classification. No rollup, no "mixed" cells.

## Workflow

1. **Read `logs/current_interview.txt`** in full.
2. **Determine `session_date`**: extract from the session header (e.g., `# Interview — 2026-06-04`). If missing, use today's date.
3. **Determine `session_id`**: count existing data rows in `logs/interview_history.csv` and add 1. If the file doesn't exist, `session_id = 1`.
4. **Group questions by (topic, subtopic)**: each Q&A pair has a topic and subtopic in its header (e.g., `### Q1 — Architecture / Repository Pattern`). Group across both main and experience Q&A sections.
5. **Extract the answer-category label per (topic, subtopic)**: each Q&A in `current_interview.txt` already has an `Answer category` field with one of the five values. Take that label verbatim — no summarizing, no adding context. With strict 1:1 (one question per subtopic), each subtopic has exactly one label.
6. **Write via the `trainer-csv` MCP server**: call its `save_session` tool with `session_date` and the list of `{topic, subtopic, label}` results. The tool computes the session_id, reconciles columns (new (topic, subtopic) pairs are appended to both header rows and every prior data row is padded with empty cells), validates labels against the five allowed values, and refuses duplicate session dates.
7. **Fallback only if the MCP server is unavailable**: perform the same reconciliation and append manually, following the file format above.
8. **Verify the write succeeded**: the tool's confirmation (session number, subtopics covered, new columns added) is the verification. On manual fallback, confirm the new row is present in `logs/interview_history.csv` before proceeding.
9. **Delete `logs/current_interview.txt`**: only after step 8 confirms the data is safely in history. This clears the working session log to make room for the next interview.
10. **Output confirmation** to the user (see below).

**Critical ordering rule**: NEVER delete `logs/current_interview.txt` before verifying the data was appended successfully. If the write fails, leave `current_interview.txt` intact so the data isn't lost.

## CSV escaping

Handled by the `save_session` tool. On manual fallback, use standard CSV (RFC 4180):
- Comma-separated.
- Double-quote any cell containing commas, quotes, or newlines.
- Escape internal double-quotes by doubling them (`"` → `""`).

## Idempotency

The `save_session` tool refuses to write if a data row for the current `session_date` already exists (on manual fallback, check before writing):
- If refused / already exists: ask the user "A session for [date] is already saved. Append anyway, replace that row, or cancel?"
- Default to **cancel** if the user doesn't respond.
- Don't silently duplicate.

## What the user sees (brief confirmation)

After appending to `logs/interview_history.csv` AND deleting `logs/current_interview.txt`, output ONLY this format:

```
✓ Session saved to logs/interview_history.csv
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
- **Never overwrite or delete data from past sessions** in `interview_history.csv`. Adding new subtopic columns to past rows means appending empty cells, not changing existing data.
- **Never delete `logs/current_interview.txt` before verifying** the append to `interview_history.csv` succeeded. Data loss risk is critical here — verify, then delete.
- **Never invent data**. If a Q&A pair is ambiguous (no clear topic/subtopic), skip it and note in the confirmation that N questions were skipped.
- **Never run** if `logs/current_interview.txt` is missing or empty — tell the user there's nothing to save and stop.
- **Never silently duplicate** session rows. Check for existing session_date before appending.
- **Never modify the CSV schema** without updating this SKILL.md first.
- **Never delete any file other than `logs/current_interview.txt`**. This skill cleans up only the working session log.
- **Never write a confidence column or counts columns.** Confidence is encoded in the notes text and inferred downstream.
