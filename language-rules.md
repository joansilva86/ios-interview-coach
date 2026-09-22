# Language Rules

These rules govern how Claude handles language in this workspace. The candidate (Joan) is practicing English alongside iOS interview prep — target role likely involves English communication, CV says B2 Upper Intermediate. Continuous low-friction correction helps without derailing the technical conversation.

## Rule 1 — Reply in the user's language

*(Changed 2026-09-04 at Joan's request — previously "always reply in English".)* Reply in the language the user writes in: Spanish gets Spanish, English gets English. Rules 2–4 below still apply to messages written in English.

## Rule 2 — Clarification threshold

If a single user sentence contains **more than 3** grammar, spelling, or word-choice mistakes, ask the user to clarify or polish the sentence **before** acting on the request.

- Count mistakes **per sentence**, not per message. A message with 2 sentences × 2 mistakes each = trigger clarification only if any single sentence has 4+.
- Do not count: filename casing, code identifiers, API names, or other technical/stylistic details — only natural-language errors.

## Rule 3 — Post-reply feedback (verbal flag)

After answering each user message, append a short section at the end listing language mistakes found in their message (grammar, spelling, word choice, awkward phrasing).

- Keep it brief — bullet list, one line per mistake with the correction.
- Use a clear separator and header (e.g., `**Language notes:**`).
- Include this even when below the clarification threshold (1–3 mistakes still get flagged).
- If the message has zero mistakes, omit the section entirely.
- Do not flag stylistic preferences or informal-but-correct phrasing — only actual errors and clear awkward phrasing.
- **Exception**: during `/interview-run` (when the simulation is active and `logs/current_interview.txt` is being actively written this session), **suppress this verbal section** to preserve the simulation. Rule 4 (CSV logging) still runs silently.
- **Exception**: during an `/interview-quick-fire` round, **suppress this verbal section** to keep the drill pace — batch the language notes into the end-of-round summary instead. Rule 4 (CSV logging) still runs silently after every message.

## Rule 4 — Persistent correction log (CSV)

Append every correction to `logs/misspellings.csv` after each user message.

- **Scope**: spelling, grammar, AND awkward phrasing (e.g., "end the training mode" → "exit training mode"). Broad scope by design — maximizes the learning value of the log.
- **Schema**: three columns — `word,category,count`. Header row is `word,category,count`. The `word` column holds the **corrected** form (not the misspelled one); `category` is one of `spelling | grammar | phrasing` (`unknown` on rows migrated from the old two-column schema — upgraded automatically when the word recurs).
- **Granularity** *(added 2026-09-15)*: log the smallest reusable unit, so counts accumulate on what Joan should drill:
  - Single words and short phrases (up to ~4 words): store the corrected form (CSV-quote only if it contains commas).
  - Anything longer (a clause or a full sentence): store a **pattern label** from the canonical list below — never the full sentence. Reuse an existing label whenever one fits; only when none fits, coin a new one AND add it to the list below in the same turn.
- **Canonical pattern labels**: `passive -ed` ("is use" → "is used") · `third-person -s` ("it fail" → "it fails") · `present perfect` ("I never faced" → "I've never faced") · `question mark in questions` · `word order: modifier before noun` ("framework Observation" → "Observation framework") · `comma splice` · `duplicated subject it` ("add a hook it is good" → "adding a hook is good") · `gerund subject` ("add a hook is" → "adding a hook is") · `article a/an` · `preposition choice` ("work in a branch" → "work on a branch") · `missing plural -s` ("the change and new feature" → "the changes and new features")
- **How to write**: use the `trainer-csv` MCP server's `tally_corrections` tool (one batched call per user message). It handles the increment-or-append logic, quoting, and legacy-schema migration. Only fall back to direct file writes if the MCP server is unavailable.
- **Update logic** (implemented by the tool): for each correction in the current turn, check if the corrected word/phrase already exists in the CSV. If yes, increment its count. If no, append a new row.
- **Active during `/interview-run`**: yes — the CSV update runs silently regardless of interview mode. Only the verbal flag (Rule 3) is suppressed during the interview.
- **Create if missing**: if `logs/misspellings.csv` doesn't exist yet, create it with the header `word,count` and start appending.
- If the message has zero corrections, omit the verbal section AND skip the CSV write for this turn.
