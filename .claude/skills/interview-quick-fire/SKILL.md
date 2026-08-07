---
name: interview-quick-fire
description: >
  Rapid-fire drill of short iOS questions — quick comparisons, definitions, and
  one-liners ("struct vs class", "weak vs unowned") fired one per turn at a fast pace.
  Reads topic_catalog.csv (project root) directly and draws from subtopics flagged
  active, pending, or mastered — never ignore or deferred. Silent during the round;
  all feedback is delivered in one summary at the end. Read-only — writes NO files,
  does not touch current_topics.csv, current_interview.txt, or interview_history.csv,
  and never influences /interview-setup-session.
  Use when the user says "quick fire", "drill me", "rapid questions", "short questions",
  "flashcards", or invokes /interview-quick-fire.
---

# Interview Quick Fire — Rapid Drill

You are running a **rapid-fire drill**: short questions, short answers, fast pace. This is practice, not a simulation — no interviewer persona, no STAR, no scenarios. Think flashcards, spoken out loud.

- **Target role**: Semi-Senior iOS Swift Developer — same calibration as `/interview-run`, but compressed into questions answerable in ~30 seconds.
- **This skill is standalone.** It does not consume the interview queue, does not create session logs, and its results never feed topic selection. A drill is warm-up, not evidence.

## Files

Reads **exactly one file**: `topic_catalog.csv` (project root). Wide CSV: row 1 = topics, row 2 = subtopics, row 3 = flag.

- **Eligible subtopics**: flag `active`, `pending`, or `mastered` (quick drills are ideal for retention, so `mastered` stays in the pool).
- **Excluded**: `ignore` and `deferred` — never draw from these.

**Writes NO files.** Not `current_topics.csv`, not `logs/current_interview.txt`, not `logs/interview_history.csv`. If the candidate wants their performance persisted, tell them that's what a real session (`/interview-setup-session` → `/interview-run` → `/interview-save-progress`) is for.

## Round structure

1. Read `topic_catalog.csv`, build the eligible pool.
2. Announce the round in one line: "Quick-fire round — 15 questions, answers in ~30 seconds each. Say 'stop' anytime. Feedback at the end."
3. Fire questions. **Default round = 15 questions.** If the candidate asks for a different count up front ("give me 25"), honor it.
4. The candidate can say "stop", "enough", or "that's it" at any point — end the round there and deliver feedback on whatever was asked.

## Question style

- **Short.** One line. Answerable verbally in ~30 seconds. Good shapes:
  - Comparisons: "`struct` vs `class`?", "`weak` vs `unowned`?", "`@StateObject` vs `@ObservedObject`?"
  - Definitions: "What is a retain cycle?", "What does `@escaping` mean?"
  - One-fact checks: "Which thread does `URLSession` call its completion handler on?"
  - Micro-decisions: "Token storage — Keychain or UserDefaults? One reason."
- **One question per turn. Never two.** Same rule as `/interview-run`.
- **No code writing, no scenarios, no multi-part questions, no follow-ups.** If an answer is wrong or incomplete, note it internally and fire the next question.
- **Variety**: hop across categories (Swift language, memory/ARC, concurrency, SwiftUI, testing, security, networking, architecture...). Don't ask two consecutive questions from the same subtopic; avoid repeating a subtopic within a round unless the pool is small.
- **Pace**: no preamble between questions. Next question comes immediately. A drill that chats is not a drill.

## During the round — silent

No feedback, no corrections, no "correct!", no hints, no reactions. Track each answer internally as:

- **✓ Correct** — right and sufficient for the format.
- **~ Partial** — right direction, missed the key nuance.
- **✗ Missed** — wrong, or a confident-sounding wrong answer.
- **— Skipped** — candidate said "pass" / "don't know". Just move on; don't explain mid-round.

If the candidate asks how they're doing mid-round: "Feedback at the end — next one:" and fire the next question.

## End of round — one summary

When the round ends (count reached or candidate stops), deliver a single compact summary:

1. **Score line**: e.g. "11/15 — 9 correct, 2 partial, 3 missed, 1 skipped."
2. **Corrections list**: one line per partial/missed/skipped question — the question, what they said (if anything), and the correct short answer. Skip the ✓ ones.
3. **Pattern note** (1–2 lines, only if real): if the misses cluster ("all three misses were ARC"), say so and suggest drilling that area or letting `/interview-setup-session` pick it up from real session data.

Nothing is saved. Remind them in one line that drill results don't count toward their history.

## Language rules interaction

Same treatment as `/interview-run`: **suppress the per-message verbal language flag during the round** to keep the pace — batch any language notes into the end-of-round summary instead. The silent CSV logging (`tally_corrections`) still runs after every candidate message as usual.

## Do not

- Don't give feedback, hints, or reactions mid-round.
- Don't ask scenario, STAR, or multi-part questions — that's `/interview-run` territory.
- Don't write any file.
- Don't draw from `ignore` or `deferred` subtopics.
- Don't read `current_topics.csv`, `interview_history.csv`, or candidate files — the catalog is the only input.
- Don't turn the summary into coaching mode — corrections are one line each; if they want depth on a topic, they can ask after the summary.
