---
name: save-progress
description: >
  Persists the most recent interview session's data into the interview_history file.
  Reads logs/current_interview.txt (the just-finished session), analyzes per-question
  categories to roll up topic confidence levels, and updates logs/interview_history.txt
  (topic mastery table + appends a session entry). Does NOT deliver feedback, verdict,
  or recommendations — only saves state. A separate feedback skill is responsible for
  user-facing analysis.
  Use when the candidate says "save the progress", "save the session",
  "save my interview", "log the session", or invokes /save-progress.
---

# Save Progress

You are persisting the most recent interview session's data into the cumulative history file. Your job is **save state, not deliver feedback**. The user-facing output is a brief confirmation, not an analysis.

## When this skill runs

- After an `ios-interview` session has ended (or at any later time when the user wants to persist the data).
- Standalone invocation — not chained automatically.
- Output is a confirmation, not coaching or recommendations.

## Mandatory inputs (read in order)

1. **`logs/current_interview.txt`** — The session to persist. Contains Q&A pairs with per-question categories (On Point / Could Be Better / Vague / Improvised / Don't Know) and notes per question.
2. **`logs/interview_history.txt`** — The existing cumulative history file. Contains the Topic Mastery table and prior session entries. You will update this file (append the new session, update existing topic rows).
3. **`candidate-information/linkedIn.txt`** — Used only for context (target role, level). Helps interpret topic relevance, but the skill does not analyze this for user output.

**If `logs/current_interview.txt` is missing or empty**: tell the user there's nothing to save and stop. Don't fabricate data.

**If `logs/interview_history.txt` doesn't exist**: create it with the standard format (Topic Mastery table header + Sessions section header), then populate.

## What this skill writes (the only output that matters)

Update `logs/interview_history.txt` with:

### 1. Topic Mastery table — update existing rows, add new ones

For each topic touched in the session, roll up the per-question categories into a single confidence level:

| Per-question signal | Confidence implication |
|---------------------|------------------------|
| Consistently **On Point** (≥2 questions) | `strong` |
| Mix of **On Point** and **Could Be Better**, no Vague/Improvised/Don't Know | `ok` |
| Any **Vague**, **Improvised**, or **Don't Know** | `weak` |
| Topic never touched before this session, single question | use the category (On Point→`strong`, Could Be Better→`ok`, Vague/Improvised/Don't Know→`weak`) |
| Topic never asked about | `unknown` (don't add a row unless explicitly relevant) |

**Update rules**:
- If a topic already exists in the table, update its `Confidence` and `Last Practiced` columns, and append a brief note to the `Notes` column (don't overwrite existing notes — extend them).
- If the topic is new, add a row in the appropriate alphabetical/category position.
- For topics where confidence **degraded** (e.g., was `strong`, now `weak`): note the regression in the Notes column ("regressed from strong, session N").

### 2. Sessions section — append a new entry

Append a new section under `## Sessions`:

```markdown
### YYYY-MM-DD (Session N)
- **Topics covered**: comma-separated list of topics from this session
- **Asked / on-point**: N total questions / M classified as On Point
- **Weaknesses surfaced**: 2–4 bullet points of what went poorly (Vague, Improvised, Don't Know answers), with a 1-line description of the gap
- **Patterns observed**: 2–3 bullets on HOW the candidate thinks — what they confuse, what they over-rely on, what reasoning habit they repeat (this is the most valuable field; describe behavior, not just content gaps)
- **Next session focus**: 3–5 specific topics to prioritize next session, derived from the weaknesses
```

Use the current date for `YYYY-MM-DD`. Determine session number by counting existing session entries + 1.

## Analysis rules (internal, not user-facing)

To populate the session entry properly:

- **Weaknesses surfaced**: take Vague + Improvised + Don't Know answers, group by topic, write 1 line each describing the gap (not the question — the gap). Example: "Repository vs Service: inverted definitions (said Repo returns DTOs, Service returns domain — should be opposite)."
- **Patterns observed**: look across questions for recurring habits. Examples:
  - "Defaults to pseudo-code under pressure instead of writing real syntax"
  - "Imports past work context without checking fit (e.g., used throws for X because Y used it)"
  - "Confuses framework names with pattern names (Observer vs Observation)"
- **Next session focus**: derive from the weaknesses + role priorities (from `linkedIn.txt`). Don't recommend generic study activities — those belong to `study-plan`. Just list the **topics** that need re-drilling.

## What the user sees (the brief confirmation)

After updating `logs/interview_history.txt`, output ONLY this:

```
✓ Session saved to logs/interview_history.txt

Updated: N topic mastery rows
Added: session entry "YYYY-MM-DD (Session N)"
Topics covered: [list, max 8]
Confidence summary: X strong, Y ok, Z weak, W unknown (this session's topics)

Next session focus (saved to history):
- Topic 1
- Topic 2
- Topic 3
```

That's it. **No further analysis, no verdict, no recommendations, no encouragement, no critique.**

If the user wants feedback or a study plan, they invoke a different skill (`feedback` for verdict, `study-plan` for between-session study).

## Do not

- **Never deliver a verdict** (qualifies / does not qualify).
- **Never give recommendations** beyond what goes into the saved file's "Next session focus" field — and even those are topic names, not study tasks.
- **Never comment on candidate performance** ("you did well on X", "you struggled with Y"). Just save and confirm.
- **Never overwrite existing data**. Update topic rows by extending notes; append session entries; don't delete history.
- **Never invent data**. If the per-question category is unclear, mark the topic confidence as `unknown` or skip it.
- **Never run** if `logs/current_interview.txt` is missing or empty — tell the user there's nothing to save.
- **Never analyze patterns the user didn't display**. Only describe behavior actually observed in the session log.

## Idempotency

If the user runs `/save-progress` twice for the same session:
- Detect that the session entry for today's date already exists.
- Ask the user: "A session for [date] is already saved. Overwrite, append a new entry, or cancel?"
- Don't silently duplicate.
