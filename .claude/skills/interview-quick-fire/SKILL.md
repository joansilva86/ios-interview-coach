---
name: interview-quick-fire
description: >
  Rapid-fire drill of short iOS questions — quick comparisons, definitions, and
  one-liners ("struct vs class", "weak vs unowned") fired one per turn at a fast pace.
  Reads topic_catalog.csv (project root) directly and draws from subtopics flagged
  active, pending, or mastered — never ignore or deferred. Silent during the round;
  all feedback is delivered in one summary at the end, and the round is then ALWAYS
  saved to logs/interview_history.csv via the trainer-csv MCP (save_session), using
  the same five answer-category labels as /interview-run. Writes no files directly
  and does not touch current_topics.csv or current_interview.txt.
  Use when the user says "quick fire", "drill me", "rapid questions", "short questions",
  "flashcards", or invokes /interview-quick-fire.
---

# Interview Quick Fire — Rapid Drill

You are running a **rapid-fire drill**: short questions, short answers, fast pace. This is practice, not a simulation — no interviewer persona, no STAR, no scenarios. Think flashcards, spoken out loud.

- **Target role**: Semi-Senior iOS Swift Developer — same calibration as `/interview-run`, but compressed into questions answerable in ~30 seconds.
- **Standalone but persisted.** It does not consume the interview queue and does not create session logs — but every round IS saved to `logs/interview_history.csv` (via the MCP), so drill results feed `/interview-setup-session` and `/interview-study-plan` like a regular session. Labels reflect ~30-second answers, not full-depth ones.

## Files

Reads **exactly one file**: `topic_catalog.csv` (project root). Long CSV, one row per subtopic: `category,subtopic,flag`.

- **Eligible subtopics**: flag `active`, `pending`, or `mastered` (quick drills are ideal for retention, so `mastered` stays in the pool).
- **Excluded**: `ignore` and `deferred` — never draw from these.

**Writes through the MCP only.** At the end of every round, persist the results with the `trainer-csv` MCP server's `save_session` tool (one call). **No direct file writes** — not `current_topics.csv`, not `logs/current_interview.txt`, and never `logs/interview_history.csv` by hand. If the MCP is unavailable or refuses the save (it rejects a duplicate `session_date` — e.g. a session was already saved today), tell the candidate the round could not be saved and why; do NOT fall back to editing the CSV directly.

## Round structure

1. Read `topic_catalog.csv`, build the eligible pool.
2. Announce the round in one line: "Quick-fire round — 15 questions, answers in ~30 seconds each. Say 'stop' anytime. Feedback at the end, then the round is saved to your history."
3. Fire questions. **Default round = 15 questions.** If the candidate asks for a different count up front ("give me 25"), honor it.
4. The candidate can say "stop", "enough", or "that's it" at any point — end the round there, deliver feedback on whatever was asked, and save those results.

## Question style

- **Short.** One line. Answerable verbally in ~30 seconds. Good shapes:
  - Comparisons: "`struct` vs `class`?", "`weak` vs `unowned`?", "`@StateObject` vs `@ObservedObject`?"
  - Definitions: "What is a retain cycle?", "What does `@escaping` mean?"
  - One-fact checks: "Which thread does `URLSession` call its completion handler on?"
  - Micro-decisions: "Token storage — Keychain or UserDefaults? One reason."
- **One question per turn. Never two.** Same rule as `/interview-run`.
- **No code writing, no scenarios, no multi-part questions, no follow-ups.** If an answer is wrong or incomplete, note it internally and fire the next question.
- **One catalog row per question — track exact strings.** Each question maps to exactly one catalog row; record the exact `category` and `subtopic` strings from `topic_catalog.csv` for it. `save_session` transcribes these into `interview_history.csv` columns, so exact strings keep drill rows aligned with the catalog and with past sessions (same rule `/interview-run` uses for its log headers).
- **Never repeat a subtopic within a round.** History holds one cell per subtopic per session, so each subtopic gets at most one question.
- **Variety**: hop across categories (Swift language, memory/ARC, concurrency, SwiftUI, testing, security, networking, architecture...). Don't ask two consecutive questions from the same category.
- **Pace**: no preamble between questions. Next question comes immediately. A drill that chats is not a drill.

## During the round — silent

No feedback, no corrections, no "correct!", no hints, no reactions. Classify each answer internally with the **same five labels as `/interview-run`**, calibrated to the ~30-second format:

1. **On Point** — correct and sufficient for the format.
2. **Could Be Better** — right direction, missed the key nuance.
3. **Vague** — too short or generic to show knowledge.
4. **Improvised** — wrong, dressed up as something that sounds right.
5. **Don't Know** — admits they don't know, or says "pass" / "skip" / "next". Just move on; don't explain mid-round.

If the candidate asks how they're doing mid-round: "Feedback at the end — next one:" and fire the next question.

## End of round — summary, then save

When the round ends (count reached or candidate stops), deliver a single compact summary, then persist it:

1. **Score line**: e.g. "15 asked — 8 On Point, 3 Could Be Better, 1 Vague, 1 Improvised, 2 Don't Know."
2. **Corrections list**: one line per non-On Point question — the question, what they said (if anything), and the correct short answer. Skip the On Point ones.
3. **Pattern note** (1–2 lines, only if real): if the misses cluster ("all three misses were ARC"), say so and suggest drilling that area.
4. **Save — always.** Call `save_session` once: `session_date` = today (YYYY-MM-DD), `results` = one entry per question asked, with the exact `topic` (catalog `category`), `subtopic`, and the label. Stopped-early rounds save whatever was asked. Confirm in one line (e.g. "Saved to history as session N."). If the call fails (duplicate date, server unavailable), report it in one line — the round is simply not persisted; never write the file by hand.

## Language rules interaction

Same treatment as `/interview-run`: **suppress the per-message verbal language flag during the round** to keep the pace — batch any language notes into the end-of-round summary instead. The silent CSV logging (`tally_corrections`) still runs after every candidate message as usual.

## Do not

- Don't give feedback, hints, or reactions mid-round.
- Don't ask scenario, STAR, or multi-part questions — that's `/interview-run` territory.
- Don't write any file directly — the end-of-round `save_session` MCP call is this skill's only persistence.
- Don't skip the save — every round ends with the `save_session` call, including stopped-early ones.
- Don't draw from `ignore` or `deferred` subtopics.
- Don't read `current_topics.csv`, `interview_history.csv`, or candidate files — the catalog is the only input (`save_session` owns the history append; you never read or edit it).
- Don't turn the summary into coaching mode — corrections are one line each; if they want depth on a topic, they can ask after the summary.
