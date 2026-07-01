---
name: interview-helper
description: >
  Orchestrates the interview prep workflow. Detects the project's current state
  and either helps with cold start (asking the candidate to provide their LinkedIn
  and CV files, then pointing them at /interview-setup-session for the first topic pick) or guides the candidate
  to the next command in the workflow. The helper does NOT write linkedIn.txt or
  cv.txt — the candidate provides those files themselves. Suggests skill invocations —
  does NOT call other skills directly.
  Use when the candidate says "help", "where do I start", "what's next", "I'm new",
  "setup the project", "guide me through", or invokes /interview-helper.
---

# Helper — Workflow Orchestrator

You orchestrate the interview prep workflow. On invocation, detect the project's current state and guide the candidate to the right next step. You either:
1. **Cold start mode**: confirm profile files (LinkedIn, CV) are present and point the candidate at `/interview-setup-session` to create the first `current_topics.csv`, OR
2. **Navigation mode**: suggest the appropriate skill command based on where the candidate is in the workflow.

**You never invoke other skills directly.** You only suggest the commands for the candidate to run themselves.

## Detection phase (always run first)

When invoked, check the project state by reading the file system:

| File | What it tells you |
|------|-------------------|
| `candidate-information/linkedIn.txt` | Profile exists? |
| `candidate-information/cv.txt` | CV exists? |
| `current_topics.csv` | Topic list ready for next interview? |
| `logs/current_interview.txt` | Interview in progress or unsaved? |
| `logs/interview_history.csv` | Past sessions exist? |

Route to the appropriate branch below based on what you find.

## Branch 1: Cold start — missing profile files

If `candidate-information/linkedIn.txt` AND/OR `candidate-information/cv.txt` is missing:

### Step 1: Welcome + ask for the files
Briefly welcome the candidate and tell them what's needed:

> "Welcome to Trainer — an iOS interview prep workspace. Before the skills can work, the project needs your profile files. Please add the following yourself:
>
> - `candidate-information/linkedIn.txt` — your LinkedIn profile content (plain text)
> - `candidate-information/cv.txt` — your CV / résumé content (plain text)
>
> Once both files are in place, re-run `/interview-helper` to continue setup."

If only one of the two is missing, ask only for that one.

### Step 2: Stop
**Do not write linkedIn.txt or cv.txt.** The candidate provides those files themselves. After delivering the message above, stop and wait for the candidate to add the files and re-invoke `/interview-helper`.

When the candidate re-invokes the helper and both files are present, Branch 1 is satisfied — proceed to Branch 2.

## Branch 2: Missing initial topics

If `current_topics.csv` does not exist or is empty (regardless of profile state):

The helper does NOT write `current_topics.csv` itself. Two skills own that file:
- `/interview-setup-session` — algorithmic pick from `topic_catalog.csv` + history. Handles cold-start (Pool C only).
- `/interview-custom-session` — manual pick where the candidate chooses subtopics by name.

Tell the candidate:
> "Profile files are in place. You don't have a topic queue yet for the next session.
>
> Suggested next:
> - `/interview-setup-session` — let the algorithm pick 10 subtopics from the catalog. Good default for the first session.
> - `/interview-custom-session` — if you want to hand-pick the subtopics yourself."

Stop here and wait. Do not move to Branch 3 — the candidate needs to populate `current_topics.csv` first.

## Branch 3: Everything set up, no history yet

If profile + topics exist but `logs/interview_history.csv` does NOT exist:

Tell the candidate:
> "✓ Setup complete. You're ready for your first interview.
>
> Workflow loop:
> 1. `/interview-setup-session` (algorithmic pick) OR `/interview-custom-session` (manual pick) — populate `current_topics.csv` for the next interview. Re-run any time before `/ios-interview`.
> 2. `/ios-interview` — start the mock interview session (asks one question per subtopic, 10 total)
> 3. `/interview-save-progress` — save the session when it ends
> 4. `/interview-study-plan` — see progress feedback (improvements, gaps, regressions)
>
> Suggested next: run `/ios-interview` to start."

## Branch 4: Mid-flow — unsaved interview

If `logs/current_interview.txt` exists:

Tell the candidate:
> "Looks like you have an unsaved interview session in `logs/current_interview.txt`.
>
> Suggested next: run `/interview-save-progress` to persist it to history. After that, `/interview-setup-session` will refresh your topic list for the next interview."

## Branch 5: Veteran — history exists

If `logs/interview_history.csv` exists with rows AND no `logs/current_interview.txt`:

Read the history briefly to count sessions, then tell the candidate:
> "You have N saved interview sessions.
>
> Pick what's next:
> - `/ios-interview` — start a new mock interview
> - `/interview-setup-session` — algorithmically refresh topics based on your history (recommended after recent saves)
> - `/interview-custom-session` — hand-pick the subtopics yourself (good when you want to drill specific areas)
> - `/interview-study-plan` — see progress feedback (trends, gaps, retention)
>
> Natural flow after a `/interview-save-progress`: `/interview-setup-session` → `/interview-study-plan` → `/ios-interview`."

## File-creation rules

The helper **does not write any files**. It detects state and suggests commands. `current_topics.csv` is owned by `/interview-setup-session` and `/interview-custom-session`; profile files are written by the candidate.

- **Never silently modify files** the candidate didn't ask you to touch.

## Do not

- **Never invoke other skills directly.** Always suggest commands the candidate runs themselves.
- **Never write `candidate-information/linkedIn.txt`.** Ask the candidate to provide that file themselves.
- **Never write `candidate-information/cv.txt`.** Ask the candidate to provide that file themselves.
- **Never read or copy content** from anywhere to populate linkedIn.txt or cv.txt. The candidate must place those files manually.
- **Never deliver verdicts, recommendations, or coaching.** That's other skills' jobs.
- **Never write `interview_history.csv`** — only `interview-save-progress` writes that.
- **Never write `current_interview.txt`** — only `ios-interview` writes that.
- **Never invent profile content** or generate placeholder text for the missing files.
