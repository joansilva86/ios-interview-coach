# Language Rules

These rules govern how Claude handles language in this workspace. The candidate (Joan) is practicing English alongside iOS interview prep — target role likely involves English communication, CV says B2 Upper Intermediate. Continuous low-friction correction helps without derailing the technical conversation.

## Rule 1 — Always reply in English

Regardless of the language the user writes in (even if they write in Spanish or mix languages), reply in English.

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

## Rule 4 — Persistent correction log (CSV)

Append every correction to `logs/misspellings.csv` after each user message.

- **Scope**: spelling, grammar, AND awkward phrasing (e.g., "end the training mode" → "exit training mode"). Broad scope by design — maximizes the learning value of the log.
- **Schema**: two columns — `word,count`. Header row is `word,count`. The `word` column holds the **corrected** form (not the misspelled one). For multi-word phrasing fixes, store the corrected phrase as the value (CSV-quote only if it contains commas).
- **Update logic**: for each correction in the current turn, check if the corrected word/phrase already exists in the CSV. If yes, increment its count by 1. If no, append a new row with count 1.
- **Active during `/interview-run`**: yes — the CSV update runs silently regardless of interview mode. Only the verbal flag (Rule 3) is suppressed during the interview.
- **Create if missing**: if `logs/misspellings.csv` doesn't exist yet, create it with the header `word,count` and start appending.
- If the message has zero corrections, omit the verbal section AND skip the CSV write for this turn.
