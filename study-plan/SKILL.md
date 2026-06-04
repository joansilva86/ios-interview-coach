---
name: study-plan
description: >
  Generates a prioritized, actionable study plan for the candidate between
  interview sessions. Reads logs/progress.txt (learning state), logs/interview.txt
  (most recent session), and candidate-information/linkedIn.txt (target role requirements). Outputs
  concrete time-boxed study tasks ordered by priority (role-required + weak
  topics first).
  Use when the candidate says "what should I study?", "give me a study plan",
  "what to focus on between sessions", "study recommendations", or invokes
  /study-plan.
---

# Study Plan Generator

You are generating an actionable study plan for the candidate to follow **between interview simulation sessions**. The goal is to convert gaps surfaced during interviews into concrete, time-boxed study tasks — not generic advice.

## When this skill runs

- Standalone, not tied to a session. The candidate can invoke it any time.
- Typical cadence: after a session closes (when `logs/progress.txt` has fresh data), or before a planned study block.
- Output is a study plan — not coaching feedback during an interview.

## Mandatory inputs (read in order)

1. **`candidate-information/linkedIn.txt`** — Candidate profile, target role, required skills. Determines which topics are **role-required** (must-cover) vs nice-to-have.
2. **`logs/progress.txt`** — Topic mastery table + session history. Source of truth for what's `weak` / `unknown` / `strong` / `ok`, and what the "Next session focus" was at last close.
3. **`logs/interview.txt`** — Most recent session's Q&A and patterns observed. Identifies fresh gaps not yet reflected in progress.txt's table.

If any of these are missing, say so and proceed with what's available.

## Prioritization logic

Rank topics by a combination of three signals:

### 1. Role criticality (from `candidate-information/linkedIn.txt`)
- **High**: explicitly required by the target role (e.g., "MFA", "security", "Keychain" for an auth-focused role)
- **Medium**: relevant to the level but not role-specific
- **Low**: nice-to-have for general seniority but not critical

### 2. Confidence gap (from `logs/progress.txt`)
- **`unknown`** (baseline never measured) → high priority if role-critical, otherwise medium
- **`weak`** → high priority always
- **`ok`** → medium priority if it's eroding (was `strong` in earlier session, now `ok`)
- **`strong`** → skip unless 3+ weeks since last practice (retention check)

### 3. Recency / erosion (from session history)
- Topic was `strong` 2+ sessions ago but degraded → high priority (recall is fading)
- Topic was identified weak 3+ sessions in a row → high priority (persistent gap, needs new approach)
- Topic was just covered last session and went well → skip this cycle

Combine into a 4-tier priority:

- **P0 (Critical)**: role-required + weak/unknown, OR persistent gap (3+ sessions weak)
- **P1 (High)**: weak + medium role-relevance, OR eroding from strong → ok
- **P2 (Medium)**: ok with detected nuance gaps, OR unknown but lower role-relevance
- **P3 (Low)**: strong but retention refresh needed

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
- **Why it's P0**: [role-required / persistent gap / both]
- **Current state**: [quote from logs/progress.txt — e.g., "weak; couldn't recall kSecAttrAccessible values"]
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
- **Quote logs/progress.txt** when stating "current state" — anchors recommendations in real session data, not generic advice.
- **Don't recommend interview practice** — that's what `ios-interview` is for. This skill is for **between-session study**.

## Closing

End the plan with:
1. **Suggested next interview focus**: 3-4 topics to drill in the next `/ios-interview` session (so the candidate sees the loop close)
2. **Re-run this skill when**: e.g., "after 5+ hours of study completed, or after the next interview session"
