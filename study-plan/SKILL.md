---
name: study-plan
description: >
  Generates a prioritized, actionable study plan for the candidate between
  interview sessions. Reads ONLY logs/interview_history.txt — the cumulative
  history of all past sessions in CSV format. Outputs concrete time-boxed
  study tasks ordered by priority (weak topics first, with regressions and
  persistent gaps prioritized).
  Use when the candidate says "what should I study?", "give me a study plan",
  "what to focus on between sessions", "study recommendations", or invokes
  /study-plan.
---

# Study Plan Generator

You are generating an actionable study plan for the candidate to follow **between interview simulation sessions**. The goal is to convert gaps surfaced during interviews into concrete, time-boxed study tasks — not generic advice.

## When this skill runs

- Standalone, not tied to a session. The candidate can invoke it any time.
- Typical cadence: after a session closes (when `logs/interview_history.txt` has fresh data), or before a planned study block.
- Output is a study plan — not coaching feedback during an interview.

## Mandatory inputs

This skill reads **only one file**:

- **`logs/interview_history.txt`** — CSV with one row per (session, subtopic). Schema: `session_date, session_id, topic, subtopic, confidence, questions_asked, on_point_count, notes`. The cumulative record of all past sessions.

This skill does **not** access:
- Any candidate personal information (no `linkedIn.txt`, no `candidate_stories.md`)
- The topic list (`current_topics.txt`) — works purely from what's been practiced
- The current session log (`current_interview.txt`) — assumes the latest session has already been appended to history via `/save-progress`

**Workflow expectation**: run `/save-progress` first after a session to persist the latest data, then `/study-plan` to generate recommendations based on the updated history.

**If `logs/interview_history.txt` is missing or empty**: tell the user there's no history to base a plan on — they should run an interview session and save progress first.

## Prioritization logic

Rank topics by two signals derived from `interview_history.txt`:

### 1. Confidence gap (current state, most recent row per subtopic)
- **`weak`** → high priority
- **`unknown`** → high priority (baseline never solidified)
- **`ok`** → medium priority if eroding (was `strong` in an earlier row, now `ok`)
- **`strong`** → skip unless 3+ weeks since last practice (retention check via the most recent `session_date`)
- **`skip`** → do not include in the plan; the user marked it intentionally

### 2. Recency / erosion (compare older rows to the most recent row for each subtopic)
- Confidence **regressed** across sessions (e.g., `strong` → `weak`, `ok` → `weak`) → high priority (recall is fading)
- Subtopic appeared as `weak` in 3+ sessions in a row → high priority (persistent gap — current approach isn't working, needs a different angle)
- Subtopic was just covered in the latest session and is now `strong` → skip this cycle (already retained)

Combine into a 4-tier priority:

- **P0 (Critical)**: persistent gap (3+ sessions weak) OR significant regression (`strong` → `weak`)
- **P1 (High)**: currently `weak` or `unknown` (single occurrence) OR mild regression (`strong` → `ok`)
- **P2 (Medium)**: `ok` with notes indicating gaps, OR returning to `weak` after recent improvement
- **P3 (Low)**: `strong` retention refresh after 3+ weeks of no practice

## Output format

Structure the plan as follows:

```markdown
# Study Plan — [date range, e.g., "Week of 2026-06-04"]

## Summary
- **Total recommended effort**: X hours over Y days
- **Top 3 focus areas**: brief 1-line each
- **Skip this cycle**: topics that are solid + recently practiced (avoid over-drilling)

## P0 — Critical (do these first)
For each topic:
### [Topic name]
- **Why it's P0**: [persistent gap / significant regression / both]
- **Current state**: [quote from logs/interview_history.txt — e.g., "weak; couldn't recall kSecAttrAccessible values"]
- **Concrete actions**:
  1. [Specific action — e.g., "Write a custom @Clamped property wrapper from scratch (no reference)"]
  2. [Specific action — e.g., "Read Apple's Keychain Services docs section on access controls"]
  3. [Specific action — e.g., "Drill flashcards: kSecAttrAccessibleAfterFirstUnlock vs WhenUnlocked"]
- **Time**: [estimate, e.g., "1h drill + 2x 15min daily review for a week"]
- **Done when**: [observable criterion — e.g., "Can name 4 kSecAttrAccessible values + access vs refresh mapping without notes"]

## P1 — High
(Same structure as P0)

## P2 — Medium
(Brief — 1-2 actions per topic, time estimate, done-when criterion)

## P3 — Retention refreshes
(One-liner each — just a flashcard or quick re-explain to verify recall)

## Sequencing notes
- [Topic A] blocks [Topic B] — do A first because [reason]
- [Topic C] is best done with code, not reading — schedule for a 1h block, not commute time
- Suggested order: P0 → P1 (interleaved) → P2 → P3
```

## Rules for "concrete actions"

**Bad action** (vague):
- "Study property wrappers"
- "Review Keychain"
- "Practice testing"

**Good action** (specific, observable):
- "Write `@Clamped(min:max:)` property wrapper from memory. Should compile + work for `@Clamped(min: 0, max: 100) var volume = 50`"
- "Memorize: access token → `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`; refresh token → `kSecAttrAccessibleWhenUnlockedThisDeviceOnly + SecAccessControl.userPresence`. Flashcard drill 5 min/day for a week."
- "Write a Swift Testing test for LoginViewModel with success + error cases. Mock must be `class` (not struct). Use `@Test func name() async throws` + `#expect(...)`."

Every action should answer: **What exactly do I do? How will I know when I'm done?**

## Time estimates

Use these buckets, don't over-precise:
- **5 min**: flashcard review, single concept check
- **15 min**: read one doc section, watch one short video
- **30 min**: small code exercise, focused drill
- **1h**: substantial code exercise, deep doc read + notes
- **Multi-session**: complex topic needing multiple sittings (split it explicitly)

## What to skip / avoid

- **Don't list every weak topic** — pick the top 5-8 across all priorities. More than that = unactionable.
- **Don't recommend "watch videos"** unless naming a specific resource. Vague resource hunts kill momentum.
- **Don't pad with P3 retention refreshes** — only include if the topic is at real risk of fading.
- **Don't repeat the interview's veredicto** — the candidate already has that. Focus on actions, not assessment.

## Tone and length

- **Direct, actionable, no fluff.** This is a study plan, not coaching.
- **Total length**: ~1-2 pages max. If longer, you're listing too many topics.
- **Quote logs/interview_history.txt** when stating "current state" — anchors recommendations in real session data, not generic advice.
- **Don't recommend interview practice** — that's what `ios-interview` is for. This skill is for **between-session study**.

## Closing

End the plan with:
1. **Suggested next interview focus**: 3-4 topics to drill in the next `/ios-interview` session (so the candidate sees the loop close)
2. **Re-run this skill when**: e.g., "after 5+ hours of study completed, or after the next interview session"
