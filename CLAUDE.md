# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trainer** is an iOS interview coaching workspace: a structured interview prep system built from seven skills that cover onboarding, topic selection (algorithmic and manual), interview simulation, quick drills, session persistence, and progress feedback.

Candidate information lives in `candidate-information/`. Personal session logs live in `logs/` (gitignored).

## Skills (Entry Points)

Skills live in `.claude/skills/<name>/SKILL.md`. **Each SKILL.md is the single source of truth for its own behavior** — this list only routes; don't duplicate behavioral rules here.

| Skill | Purpose | Invoke via |
|---|---|---|
| `interview-helper` | Onboarding + workflow navigation; suggests the next command | `/interview-helper`, "where do I start?", "what's next?" |
| `interview-setup-session` | Algorithmically picks the next 10 subtopics → writes `current_topics.csv` | `/interview-setup-session`, "pick what to ask next" |
| `interview-custom-session` | Candidate picks the 10 subtopics manually → writes `current_topics.csv` | `/interview-custom-session`, "I want to choose the topics" |
| `interview-run` | Full interview simulation over `current_topics.csv`; logs to `logs/current_interview.txt` | `/interview-run`, "interview me" |
| `interview-quick-fire` | Rapid-fire drill of short questions; read-only, no persistence | `/interview-quick-fire`, "drill me", "quick fire" |
| `interview-save-progress` | Persists the last session into `logs/interview_history.csv` | `/interview-save-progress`, "save the session" |
| `interview-study-plan` | Progress feedback from history; read-only | `/interview-study-plan`, "how am I doing?" |

Typical loop: `setup-session` (or `custom-session`) → `run` → `save-progress` → `study-plan`.

## Language Rules

See **[`language-rules.md`](language-rules.md)** for the four rules that govern how Claude handles language in this workspace (English-only replies, clarification threshold, post-reply mistake flagging, and persistent correction logging to `logs/misspellings.csv`). These rules apply to every conversation in this workspace, including during skills (see the exceptions listed in that file).

## Shared File Contracts

These files are shared between skills, so their schemas and ownership are defined here (not in any single SKILL.md):

```
topic_catalog.csv             — source of truth for what CAN be asked. Wide CSV: row 1 = topics, row 2 = subtopics, row 3 = flag (active|pending|ignore|deferred|mastered). Tracked. Flag semantics: active=in scope, pending=in scope but flagged for review, ignore=permanently off, deferred=temporarily off, mastered=retention-refresh only.

current_topics.csv            — next session's queue: up to 10 subtopics, one question each. Schema: category,subtopic. Row order matches interview_history.csv column order. Owned by /interview-setup-session and /interview-custom-session — overwritten each run. MUST be a subset of topic_catalog.csv. (gitignored — local-only)

candidate-information/        — candidate profile data (gitignored — local-only; provided by the candidate, not generated)
  ├── linkedIn.txt            — LinkedIn profile content (the candidate places this file themselves)
  ├── cv.txt                  — CV / résumé content (the candidate places this file themselves)
  └── candidate_stories.md    — canonical STAR stories for experience questions

logs/                         — personal session logs (gitignored)
  ├── current_interview.txt   — current/most recent session Q&A. Written by /interview-run, consumed then deleted by /interview-save-progress.
  ├── interview_history.csv   — wide CSV: 2 header rows (topic, subtopic) + one row per session; each cell holds an answer-category label (On Point | Could Be Better | Vague | Improvised | Don't Know) or is empty
  └── misspellings.csv        — running log of language corrections (schema: word,category,count). Owned by the language rules (see language-rules.md).

mcp/                          — trainer-csv MCP server (Python, run via `uv run`). Owns structured CSV writes: tally_corrections (misspellings.csv), save_session (interview_history.csv), write_topics (current_topics.csv). Registered with `claude mcp add`; self-test: `uv run mcp/trainer_csv_server.py --selftest`.

language-rules.md             — workspace-wide language rules (see above).

.claude/skills/               — the seven skills (see table above), one SKILL.md each.
```

Trust chain: `topic_catalog.csv` is read by the topic-selection skills (and `/interview-quick-fire`); downstream skills trust `current_topics.csv` without re-reading the catalog.
