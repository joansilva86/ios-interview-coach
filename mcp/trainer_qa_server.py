# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp<2"]
# ///
import csv
import difflib
import os
import tempfile
from pathlib import Path

from pydantic import Field
from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
QA_BANK = ROOT / "qa_bank.csv"
HEADER = ["category", "question", "answer", "on_point_date"]
DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

mcp = FastMCP("trainer-qa")


def _read_bank(path: Path) -> list[list[str]]:
    if not path.exists():
        return [HEADER.copy()]
    with open(path, newline="", encoding="utf-8") as f:
        rows = [[cell.replace("\r", "") for cell in row] for row in csv.reader(f) if row]
    if not rows or rows[0] != HEADER:
        raise ValueError(f"{path} is malformed (expected header: {','.join(HEADER)}).")
    return [row + [""] * (len(HEADER) - len(row)) for row in rows]


def _write_bank(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


def _find_question(rows: list[list[str]], question: str) -> int:
    for i, row in enumerate(rows[1:], start=1):
        if row[1] == question:
            return i
    folded = question.casefold()
    matches = [i for i, row in enumerate(rows[1:], start=1) if row[1].casefold() == folded]
    if len(matches) == 1:
        return matches[0]
    close = difflib.get_close_matches(question, [r[1] for r in rows[1:]], n=3, cutoff=0.5)
    hint = f" Did you mean: {close}?" if close else ""
    raise ValueError(f"Question not found in qa_bank.csv: {question!r}.{hint}")


def _mark_on_point(question: str, date: str, path: Path) -> str:
    rows = _read_bank(path)
    i = _find_question(rows, question)
    previous = rows[i][3]
    rows[i][3] = date
    _write_bank(path, rows)
    prev = f"previous: {previous}" if previous else "first On Point"
    return f"on_point_date set to {date} for {rows[i][1]!r} ({prev})"


@mcp.tool()
def mark_on_point(
    question: str = Field(description="The question exactly as it appears in qa_bank.csv"),
    date: str = Field(description="Date of the On Point answer, YYYY-MM-DD", pattern=DATE_PATTERN),
) -> str:
    """Stamp on_point_date in qa_bank.csv for a question the candidate just answered
    On Point. Overwrites any previous date (the column holds the most recent one).
    Fails with suggestions if the question isn't in the bank."""
    return _mark_on_point(question, date, QA_BANK)


def _add_qa(category: str, question: str, answer: str, path: Path) -> str:
    rows = _read_bank(path)
    folded = question.casefold()
    if any(row[1].casefold() == folded for row in rows[1:]):
        raise ValueError(f"Question already in qa_bank.csv: {question!r}. "
                         "Edit the existing row instead of adding a duplicate.")
    rows.append([category, question, answer, ""])
    _write_bank(path, rows)
    return f"Added to qa_bank.csv under {category!r} ({len(rows) - 1} entries total)."


@mcp.tool()
def add_qa(
    category: str = Field(description="Category, using the exact strings from topic_catalog.csv"),
    question: str = Field(description="The interview question"),
    answer: str = Field(description="Polished spoken-English model answer"),
) -> str:
    """Append a new question/answer pair to qa_bank.csv with an empty on_point_date.
    Refuses duplicate questions (case-insensitive)."""
    return _add_qa(category, question, answer, QA_BANK)


if __name__ == "__main__":
    mcp.run()
