# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp"]
# ///
"""Trainer CSV MCP server.

Owns all structured writes to the Trainer workspace's CSV files:

  - logs/misspellings.csv   (word,category,count)   -> tally_corrections
  - logs/interview_history.csv (wide, 2 header rows) -> save_session
  - current_topics.csv      (category,subtopic)      -> write_topics

Storage is an implementation detail of this server: callers only see the
three tools. Run manually with:  uv run mcp/trainer_csv_server.py
Self-test (no MCP client needed): uv run mcp/trainer_csv_server.py --selftest
"""

import csv
import sys
import tempfile
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
MISSPELLINGS = ROOT / "logs" / "misspellings.csv"
HISTORY = ROOT / "logs" / "interview_history.csv"
CATALOG = ROOT / "topic_catalog.csv"
TOPICS = ROOT / "current_topics.csv"

VALID_LABELS = ["On Point", "Could Be Better", "Vague", "Improvised", "Don't Know"]

mcp = FastMCP("trainer-csv")


# ---------------------------------------------------------------- helpers

def _read_csv(path: Path) -> list[list[str]]:
    """Read a CSV tolerating legacy CRLF line endings and a missing file."""
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [[cell.replace("\r", "") for cell in row] for row in csv.reader(f) if row]


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


# ------------------------------------------------------- tally_corrections

class Correction(BaseModel):
    word: str = Field(description="The corrected form (not the mistake)")
    category: Literal["spelling", "grammar", "phrasing"] = Field(
        description="What kind of mistake was corrected"
    )
    times: int = Field(default=1, ge=1, description="Occurrences in this message")


def _tally(corrections: list[Correction], path: Path) -> str:
    rows = _read_csv(path)
    if not rows:
        rows = [["word", "category", "count"]]
    # Auto-migrate legacy word,count schema
    if rows[0] == ["word", "count"]:
        rows = [["word", "category", "count"]] + [
            [r[0], "unknown", r[1] if len(r) > 1 else "1"] for r in rows[1:]
        ]
    index = {r[0]: i for i, r in enumerate(rows) if i > 0}
    report = []
    for c in corrections:
        if c.word in index:
            row = rows[index[c.word]]
            row[2] = str(int(row[2] or 0) + c.times)
            if row[1] == "unknown":  # upgrade legacy rows on first re-occurrence
                row[1] = c.category
            report.append(f"{c.word} -> count {row[2]} ({row[1]})")
        else:
            rows.append([c.word, c.category, str(c.times)])
            index[c.word] = len(rows) - 1
            report.append(f"{c.word} -> new ({c.category}, count {c.times})")
    _write_csv(path, rows)
    return "\n".join(report)


@mcp.tool()
def tally_corrections(corrections: list[Correction]) -> str:
    """Record language corrections in logs/misspellings.csv. For each corrected
    word or phrase: increments its count if already logged, otherwise appends a
    new row. Send one batch per user message. Returns the running count per entry."""
    if not corrections:
        return "Nothing to record."
    return _tally(corrections, MISSPELLINGS)


# ------------------------------------------------------------ save_session

class SubtopicResult(BaseModel):
    topic: str = Field(description="Topic exactly as used in the session log, e.g. 'Theory'")
    subtopic: str = Field(description="Subtopic exactly as used in the session log")
    label: str = Field(description="One of: " + " | ".join(VALID_LABELS))


def _save_session(session_date: str, results: list[SubtopicResult], path: Path) -> str:
    bad = [r.label for r in results if r.label not in VALID_LABELS]
    if bad:
        raise ValueError(f"Invalid label(s) {bad}. Allowed: {VALID_LABELS}")

    rows = _read_csv(path)
    if not rows:
        rows = [["session_date", "session_id"], ["", ""]]
    topics_hdr, subs_hdr = rows[0], rows[1]
    data = rows[2:]

    if any(r and r[0] == session_date for r in data):
        raise ValueError(
            f"A session for {session_date} is already saved. "
            "Refusing to duplicate — remove the existing row first if this is intentional."
        )

    columns = {(topics_hdr[i], subs_hdr[i]): i for i in range(2, len(topics_hdr))}
    added = 0
    for r in results:
        if (r.topic, r.subtopic) not in columns:
            topics_hdr.append(r.topic)
            subs_hdr.append(r.subtopic)
            for row in data:
                row.append("")
            columns[(r.topic, r.subtopic)] = len(topics_hdr) - 1
            added += 1

    new_row = [session_date, str(len(data) + 1)] + [""] * (len(topics_hdr) - 2)
    for r in results:
        new_row[columns[(r.topic, r.subtopic)]] = r.label

    _write_csv(path, [topics_hdr, subs_hdr] + data + [new_row])
    return (
        f"Session saved: {session_date} (Session {len(data) + 1})\n"
        f"Subtopics covered: {len(results)}\n"
        f"New columns added: {added}"
    )


@mcp.tool()
def save_session(session_date: str, results: list[SubtopicResult]) -> str:
    """Append one interview session as a row to logs/interview_history.csv.
    Validates answer-category labels, computes the next session_id, adds columns
    for never-asked subtopics (padding past rows), and refuses duplicate dates."""
    return _save_session(session_date, results, HISTORY)


# ------------------------------------------------------------ write_topics

class TopicPick(BaseModel):
    category: str = Field(description="Topic name exactly as in topic_catalog.csv row 1")
    subtopic: str = Field(description="Subtopic name exactly as in topic_catalog.csv row 2")


def _write_topics(picks: list[TopicPick], topics_path: Path,
                  catalog_path: Path, history_path: Path) -> str:
    if len(picks) != 10:
        raise ValueError(f"Exactly 10 picks required, got {len(picks)}.")

    catalog = _read_csv(catalog_path)
    if len(catalog) < 3:
        raise ValueError(f"Catalog at {catalog_path} is missing or malformed.")
    cat_pairs = {(catalog[0][i], catalog[1][i]): i for i in range(len(catalog[0]))}

    unknown = [(p.category, p.subtopic) for p in picks
               if (p.category, p.subtopic) not in cat_pairs]
    if unknown:
        raise ValueError(f"Not in topic_catalog.csv: {unknown}. "
                         "current_topics.csv must be a subset of the catalog.")
    dupes = len(picks) != len({(p.category, p.subtopic) for p in picks})
    if dupes:
        raise ValueError("Duplicate picks — each (category, subtopic) may appear once.")

    history = _read_csv(history_path)
    hist_pos = {}
    if len(history) >= 2:
        hist_pos = {(history[0][i], history[1][i]): i
                    for i in range(2, len(history[0]))}
    max_hist = max(hist_pos.values(), default=0)

    def sort_key(p: TopicPick):
        pair = (p.category, p.subtopic)
        return hist_pos.get(pair, max_hist + 1 + cat_pairs[pair])

    ordered = sorted(picks, key=sort_key)
    _write_csv(topics_path, [["category", "subtopic"]] +
               [[p.category, p.subtopic] for p in ordered])

    warnings = []
    for p in picks:
        flag = catalog[2][cat_pairs[(p.category, p.subtopic)]]
        if flag in ("pending", "deferred", "ignore"):
            warnings.append(f"  ! {p.subtopic}: catalog flag = {flag}")
    out = "current_topics.csv written - 10 subtopics queued:\n" + "\n".join(
        f"  {i + 1}. {p.category} / {p.subtopic}" for i, p in enumerate(ordered))
    if warnings:
        out += "\nWarnings:\n" + "\n".join(warnings)
    return out


@mcp.tool()
def write_topics(picks: list[TopicPick]) -> str:
    """Overwrite current_topics.csv with exactly 10 (category, subtopic) picks for
    the next interview. Every pick must exist in topic_catalog.csv. Rows are sorted
    into interview_history.csv column order (history-known first, then catalog order).
    Warns (without blocking) on picks flagged pending/deferred/ignore."""
    return _write_topics(picks, TOPICS, CATALOG, HISTORY)


# ---------------------------------------------------------------- selftest

def _selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        mis, hist, cat, top = (tmp / "m.csv", tmp / "h.csv", tmp / "c.csv", tmp / "t.csv")

        # tally: legacy migration + bump + append
        _write_csv(mis, [["word", "count"], ["responsibility", "8"]])
        _tally([Correction(word="responsibility", category="spelling"),
                Correction(word="it has", category="grammar", times=2)], mis)
        rows = _read_csv(mis)
        assert rows[0] == ["word", "category", "count"], rows[0]
        assert rows[1] == ["responsibility", "spelling", "9"], rows[1]
        assert rows[2] == ["it has", "grammar", "2"], rows[2]

        # save_session: new columns, padding, duplicate refusal
        _write_csv(hist, [["session_date", "session_id", "Theory"],
                          ["", "", "SOLID Principles"],
                          ["2026-07-01", "1", "On Point"]])
        _save_session("2026-07-08", [
            SubtopicResult(topic="Theory", subtopic="SOLID Principles", label="Vague"),
            SubtopicResult(topic="Security", subtopic="JWT Validation", label="On Point"),
        ], hist)
        rows = _read_csv(hist)
        assert rows[0] == ["session_date", "session_id", "Theory", "Security"]
        assert rows[2] == ["2026-07-01", "1", "On Point", ""], rows[2]      # padded
        assert rows[3] == ["2026-07-08", "2", "Vague", "On Point"], rows[3]
        try:
            _save_session("2026-07-08", [SubtopicResult(
                topic="Theory", subtopic="SOLID Principles", label="Vague")], hist)
            raise AssertionError("duplicate date accepted")
        except ValueError:
            pass

        # write_topics: catalog validation, exactly-10, history ordering
        _write_csv(cat, [["Theory", "Theory", "Security", "Security"] + [f"T{i}" for i in range(8)],
                         ["A", "B", "C", "D"] + [f"S{i}" for i in range(8)],
                         ["active", "deferred", "active", "active"] + ["active"] * 8])
        picks = [TopicPick(category="Theory", subtopic="B"),
                 TopicPick(category="Security", subtopic="C")] + [
                 TopicPick(category=f"T{i}", subtopic=f"S{i}") for i in range(8)]
        out = _write_topics(picks, top, cat, hist)
        assert "deferred" in out, out
        try:
            _write_topics(picks[:9], top, cat, hist)
            raise AssertionError("9 picks accepted")
        except ValueError:
            pass
        try:
            _write_topics(picks[:9] + [TopicPick(category="Nope", subtopic="Nada")],
                          top, cat, hist)
            raise AssertionError("off-catalog pick accepted")
        except ValueError:
            pass
    print("selftest: all assertions passed")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        mcp.run()
