---
name: custom-session
description: >
  Manual alternative to /setup-session. Asks the candidate which subtopics they
  want to practice (up to 10), matches each entry against topic_catalog.csv —
  with fuzzy matching when the input is approximate — and writes the picked
  subtopics to current_topics.csv as the queue for the next /ios-interview.
  Warns (does NOT block) when a picked subtopic is flagged ignore, deferred, or
  pending in the catalog. Pure file-write skill once the picks are confirmed.
  Use when the candidate says "I want to choose the topics", "let me pick",
  "manual session", "custom session", or invokes /custom-session.
---

# Custom Session

You let the candidate hand-pick the subtopics for the next interview. This is the manual escape hatch alongside `/setup-session` (which picks algorithmically from history). The candidate is in full control — you just match their input to catalog names and write the queue.

## Mandatory inputs

This skill reads **two files**:

- **`topic_catalog.csv`** (project root, tracked) — source of truth. Wide CSV with 3 rows: topics, subtopics, flag (`active|pending|ignore|deferred|mastered`). Used to validate the user's picks and surface fuzzy matches when their input is approximate.
- **`logs/interview_history.csv`** (optional) — used only to determine the column order for the output. The history's labels (cell values) are ignored — manual picking doesn't use history for ranking. If the file doesn't exist, fall back to `topic_catalog.csv` column order for every pick.

This skill does **NOT** read `candidate-information/` or any other file. Manual picking ignores history for *what* to ask — but uses it for *what order* to write the queue, so `current_topics.csv` lines up visually with `interview_history.csv`.

## Workflow

### 1. Ask for picks

Open with a clear prompt:

> "Which subtopics do you want to practice in the next interview? Up to 10. Send them one per line, or comma-separated. Exact catalog names work best, but rough descriptions are fine — I'll match them."

Wait for the candidate's response.

### 2. Match each entry against `topic_catalog.csv`

Read the catalog. The set of valid `(topic, subtopic)` pairs = `{(row1[i], row2[i]) for each column i}`.

For each entry the candidate sent:

- **Exact match** (case-insensitive) on a subtopic name → use the catalog's canonical `(topic, subtopic)` verbatim. No confirmation needed.
- **Fuzzy match** (substring match, common-word overlap, or close spelling) → show the candidate up to 3 candidate matches with their topics, ask which they meant. Example:
  > "I matched 'wrappers' to:
  > 1. Swift Language / Property Wrappers
  > 2. Frameworks / @Observable Macro (uses wrappers)
  > 3. Frameworks / SwiftUI State Management
  > Which one? (number or 'none')"
- **No match** → show the catalog topics list (just the categories), ask which area they meant, then show subtopics in that category. Example:
  > "Couldn't find a clear match for 'auth flow'. Closest categories: Security, Architecture. Which one?"
- **Empty user response** for a clarification → drop that entry, continue with the rest.

Build a list of confirmed `(topic, subtopic)` pairs.

### 3. Apply the limit

If the candidate sent more than 10 picks (post-matching), keep the **first 10 in the order they gave** and tell them: "You picked N — keeping the first 10 in order." Drop the rest.

If they sent fewer than 10, fine — write what they have. `/ios-interview` handles short queues by asking every row and stopping.

### 4. Flag warnings (don't block)

For each confirmed pick, look up its flag in `topic_catalog.csv` row 3:

- `active` → no comment.
- `mastered` → no comment.
- `pending` → add a one-line warning to the confirmation: "Note: 'X' is flagged `pending review` in the catalog."
- `deferred` → warning: "Note: 'X' is flagged `deferred` in the catalog — you marked it temporarily off. Including it anyway."
- `ignore` → warning: "Note: 'X' is flagged `ignore` in the catalog — you marked it permanently off. Including it anyway."

Never refuse the pick — the candidate's manual override wins. Just surface the flag so they're aware.

### 5. Write `current_topics.csv`

Replace `current_topics.csv` (project root) entirely. Schema:

```csv
category,subtopic
```

**Row order — match `interview_history.csv` column order** (same convention as `/setup-session`):

1. Read `logs/interview_history.csv` (if it exists) to get the existing subtopic column order.
2. For each confirmed pick, find its position:
   - If the subtopic has a column in history: position = column index in history (left-to-right).
   - If it's never been asked: position = `<max history column index> + <its column index in topic_catalog.csv>`. Never-asked picks land after history-known ones, ordered by catalog position.
3. Sort the confirmed picks ascending by position and write them in that order.

The candidate's input order does NOT determine row order — the file always reflects history-column order so it lines up with `interview_history.csv` for easy side-by-side reading.

- Quote any field containing commas or double quotes (RFC 4180).
- No `notes` column. The flag warnings live only in the confirmation output (step 6), not in the file.

### 6. Confirmation

Output ONLY this format:

```
✓ current_topics.csv updated — N subtopics queued for next session (manual selection)

Picks (in order):
  1. <category> / <subtopic>
  2. <category> / <subtopic>
  ...

[Flag warnings, if any:]
  ⚠ <subtopic>: catalog flag = <flag>

Run /ios-interview when ready.
```

That's it. No analysis, no recommendations.

## Do not

- **Never read** any file other than `topic_catalog.csv`.
- **Never block** a pick because of its flag — warn only.
- **Never invent** a `(topic, subtopic)` pair not in the catalog. If a user request can't be matched even after fuzzy lookup, drop that entry and tell them.
- **Never overwrite `topic_catalog.csv`** — the catalog is the source of truth, not editable by this skill.
- **Never write more than 10 rows** to `current_topics.csv`.
- **Never preserve** the old `current_topics.csv` content — replace it entirely.
- **Never assign priorities** — there's no priority column. File order is the only ordering signal.
- **Never deliver a verdict, recommendation, or progress analysis** — that's `/study-plan`'s job.
