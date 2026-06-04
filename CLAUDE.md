# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trainer** is an iOS interview coaching workspace. It's a structured interview prep system with five skills: one orchestrates onboarding and workflow navigation, one runs realistic interview simulations, one persists session data, one prepares topics for the next session, and one delivers progress feedback to the candidate.

Candidate information lives in `candidate-information/`. Personal session logs live in `logs/` (gitignored).

## Skills (Entry Points)

- **`helper/SKILL.md`** — Orchestrates onboarding and workflow navigation. On cold start, asks the candidate to add their `linkedIn.txt` and `cv.txt` files (the helper does NOT write those — the candidate provides them). Once the profile files are in place, creates the initial `current_topics.txt`. Otherwise, suggests the next command based on project state. Suggests skill invocations — never calls them directly.
  - Invoked via `/helper` or "where do I start?", "what's next?", "I'm new"

- **`ios-interview/SKILL.md`** — Conducts realistic iOS technical interview simulations. The candidate is the interviewee, Claude asks questions with no mid-interview feedback.
  - Invoked via `/ios-interview` or "interview me"
  - See `ios-interview/SKILL.md` for the full workflow, question categories, calibration rules, and closing format.

- **`save-progress/SKILL.md`** — Persists the most recent interview session into `logs/interview_history.txt`, then deletes `logs/current_interview.txt`. Save-only — no feedback, verdict, or analysis delivered to the user.
  - Invoked via `/save-progress` or "save the session"

- **`setup-session/SKILL.md`** — Reads `logs/interview_history.txt` and rewrites `current_topics.txt` with prioritized topics for the next interview. File-write only — no analysis, no feedback.
  - Invoked via `/setup-session` or "prepare topics for next session"

- **`study-plan/SKILL.md`** — Reads `logs/interview_history.txt` and delivers progress feedback (improvements, persistent gaps, regressions, solid retention). Read-only — no file writes.
  - Invoked via `/study-plan` or "how am I doing?"

## Project Structure

```
current_topics.txt            — prioritized CSV of subtopics for ios-interview to draw from. Written by setup-session based on interview_history.txt. Seed file (P1/P3 priorities mapped from original role_required) can be edited manually before first /setup-session run. (tracked)

candidate-information/        — candidate profile data (tracked; provided by the candidate, not generated)
  ├── linkedIn.txt            — LinkedIn profile content (the candidate places this file themselves)
  ├── cv.txt                  — CV / résumé content (the candidate places this file themselves)
  └── candidate_stories.md    — canonical STAR stories for experience questions

logs/                         — personal session logs (gitignored)
  ├── current_interview.txt   — current/most recent session Q&A
  └── interview_history.txt   — CSV: one row per (session, subtopic)

helper/                       — onboarding + workflow navigation
  └── SKILL.md

ios-interview/                — interview simulation skill
  └── SKILL.md

save-progress/                — saves session data to interview_history.txt
  └── SKILL.md

setup-session/                — rewrites current_topics.txt from history
  └── SKILL.md

study-plan/                   — delivers progress feedback (read-only)
  └── SKILL.md
```
