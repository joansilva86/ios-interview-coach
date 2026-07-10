# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trainer** is an iOS interview coaching workspace. It's a structured interview prep system with five skills: one orchestrates onboarding and workflow navigation, one runs realistic interview simulations, one persists session data, one prepares topics for the next session, and one delivers progress feedback to the candidate.

Candidate information lives in `candidate-information/`. Personal session logs live in `logs/` (gitignored).

## Skills (Entry Points)

- **`interview-helper/SKILL.md`** — Orchestrates onboarding and workflow navigation. On cold start, asks the candidate to add their `linkedIn.txt` and `cv.txt` files, then points them at `/interview-setup-session` for the first topic pick. The helper writes NO files. Suggests skill invocations — never calls them directly.
  - Invoked via `/interview-helper` or "where do I start?", "what's next?", "I'm new"

- **`interview-run/SKILL.md`** — Conducts realistic iOS technical interview simulations. Walks `current_topics.csv` row by row, asking exactly one question per subtopic (10 rows = 10 questions, strict 1:1, no follow-ups). The candidate is the interviewee, Claude asks questions with no mid-interview feedback.
  - Invoked via `/interview-run` or "interview me"

- **`interview-save-progress/SKILL.md`** — Persists the most recent interview session into `logs/interview_history.csv`, then deletes `logs/current_interview.txt`. Read-and-transcribe only: reads `current_interview.txt` and `interview_history.csv` (for column reconciliation) and writes the new session row. Does not read the catalog — trust comes from the upstream chain (`/interview-setup-session` enforces catalog bounds).
  - Invoked via `/interview-save-progress` or "save the session"

- **`interview-setup-session/SKILL.md`** — Selects exactly 10 subtopics for the next interview by combining `topic_catalog.csv` (catalog + flags) and `logs/interview_history.csv` (past sessions). Algorithm: gap-first (persistent weaknesses), then recent weak/regressions, then never-asked breadth, then at most 1 retention refresh. Writes the queue to `current_topics.csv` in `interview_history.csv` column order (not importance order).
  - Invoked via `/interview-setup-session` or "pick what to ask next"

- **`interview-custom-session/SKILL.md`** — Manual alternative to `/interview-setup-session`. Asks the candidate which subtopics they want to practice (**exactly 10 required** — loops until met or cancels), matches them against `topic_catalog.csv` (with fuzzy matching if names are approximate), warns on `ignore`/`deferred`/`pending` flags, and writes `current_topics.csv`.
  - Invoked via `/interview-custom-session` or "I want to choose the topics"

- **`interview-study-plan/SKILL.md`** — Reads `logs/interview_history.csv` and delivers progress feedback (improvements, persistent gaps, regressions, solid retention). Read-only — no file writes.
  - Invoked via `/interview-study-plan` or "how am I doing?"

## Language Rules

See **[`language-rules.md`](language-rules.md)** for the four rules that govern how Claude handles language in this workspace (English-only replies, clarification threshold, post-reply mistake flagging, and persistent correction logging to `logs/misspellings.csv`). These rules apply to every conversation in this workspace and remain active even during `/interview-run` (with the verbal flag suppressed to preserve the simulation; the CSV log still updates silently).

## Project Structure

```
topic_catalog.csv             — source of truth for what CAN be asked. Wide CSV: row 1 = topics, row 2 = subtopics, row 3 = flag (active|pending|ignore|deferred|mastered). Tracked. Read ONLY by /interview-setup-session; downstream skills trust the chain. Flag semantics: active=in scope, pending=in scope but flagged for review, ignore=permanently off, deferred=temporarily off, mastered=retention-refresh only.

current_topics.csv            — next session's queue: up to 10 subtopics that interview-run will ask one question each. Schema: category,subtopic. Row order matches interview_history.csv column order (subtopics with history first in their original column order, then never-asked ones in catalog order). Owned by /interview-setup-session and /interview-custom-session — overwritten each run. MUST be a subset of topic_catalog.csv. (gitignored — local-only)

candidate-information/        — candidate profile data (gitignored — local-only; provided by the candidate, not generated)
  ├── linkedIn.txt            — LinkedIn profile content (the candidate places this file themselves)
  ├── cv.txt                  — CV / résumé content (the candidate places this file themselves)
  └── candidate_stories.md    — canonical STAR stories for experience questions

logs/                         — personal session logs (gitignored)
  ├── current_interview.txt   — current/most recent session Q&A
  ├── interview_history.csv   — wide CSV: 2 header rows (topic, subtopic) + one row per session; each cell holds an answer-category label (On Point | Could Be Better | Vague | Improvised | Don't Know) or is empty
  └── misspellings.csv        — running log of language corrections (schema: word,category,count; category = spelling|grammar|phrasing|unknown). Owned by the language rules (see language-rules.md). Written via the trainer-csv MCP server's tally_corrections tool after every user message; counts bump on repeat.

mcp/                          — trainer-csv MCP server (Python, run via `uv run`). Owns structured CSV writes: tally_corrections (misspellings.csv), save_session (interview_history.csv), write_topics (current_topics.csv). Registered with `claude mcp add`; self-test: `uv run mcp/trainer_csv_server.py --selftest`.

language-rules.md             — workspace-wide language rules: English-only replies, mistake flagging, CSV correction log. Active in every conversation, including /interview-run.

interview-helper/                — onboarding + workflow navigation
  └── SKILL.md

interview-run/                   — interview simulation skill
  └── SKILL.md

interview-save-progress/         — saves session data to interview_history.csv
  └── SKILL.md

interview-setup-session/         — rewrites current_topics.csv from history (algorithmic)
  └── SKILL.md

interview-custom-session/        — rewrites current_topics.csv from user-picked subtopics (manual)
  └── SKILL.md

interview-study-plan/            — delivers progress feedback (read-only)
  └── SKILL.md
```
