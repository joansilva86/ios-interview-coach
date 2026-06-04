# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trainer** is an iOS interview coaching workspace. It's a structured interview prep system with three skills that work together: one runs realistic interview simulations, one persists session data into the history file, and one generates study plans for between-session learning.

Candidate information lives in `candidate-information/`. Personal session logs live in `logs/` (gitignored).

## Skills (Entry Points)

- **`ios-interview/SKILL.md`** — Conducts realistic iOS technical interview simulations. The candidate is the interviewee, Claude asks questions with no mid-interview feedback.
  - Invoked via `/ios-interview` or "interview me"
  - See `ios-interview/SKILL.md` for the full workflow, question categories, calibration rules, and closing format.

- **`save-progress/SKILL.md`** — Persists the most recent interview session into `logs/interview_history.txt` (topic mastery table + session entry). Save-only — no feedback, verdict, or analysis delivered to the user.
  - Invoked via `/save-progress` or "save the session"
  - See `save-progress/SKILL.md` for the analysis rules and output format.

- **`study-plan/SKILL.md`** — Generates an actionable, prioritized study plan for between-session learning. Converts gaps from `logs/interview_history.txt` and `logs/current_interview.txt` into concrete, time-boxed study tasks.
  - Invoked via `/study-plan` or "what should I study?"
  - See `study-plan/SKILL.md` for the full prioritization logic and output format.

## Project Structure

```
candidate-information/        — candidate profile data (tracked)
  ├── linkedIn.txt            — CV / target role / stack
  └── candidate_stories.md    — canonical STAR stories for experience questions

logs/                         — personal session logs (gitignored)
  ├── current_interview.txt   — current/most recent session Q&A
  └── interview_history.txt   — topic mastery + session history

ios-interview/                — interview simulation skill
  └── SKILL.md

save-progress/                — saves session data to interview_history.txt
  └── SKILL.md

study-plan/                   — between-session study plan skill
  └── SKILL.md
```
