#!/usr/bin/env python3
"""
Score History — Track scoring runs over time for comparison and A/B testing.

Logs every ATS/HR scoring run to a JSON file with timestamps and resume hashes.
Enables score progression tracking: Base → V1 → V2 → Final.

Usage:
    from score_history import log_score, get_history, format_progression

    # Log a score
    log_score(
        folder="../tailored-resumes/Deere - Embedded SWE",
        score_type="ats",
        score=78.3,
        details={"keyword_score": 85, "phrase_score": 62},
        resume_hash="abc123",
        label="v1"
    )

    # Get history for a folder
    history = get_history("../tailored-resumes/Deere - Embedded SWE")

    # Format as progression table
    print(format_progression("../tailored-resumes/Deere - Embedded SWE"))

CLI (debugging):
    python score_history.py --show "../tailored-resumes/Deere - Embedded SWE"
    python score_history.py --show-all
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

HISTORY_FILENAME = "score_history.json"


def _history_path(folder: str = None) -> str:
    """Return path to score_history.json.

    If folder is given, returns per-application history file.
    If folder is None, returns the global history file at project root.
    """
    if folder:
        return str(Path(folder).resolve() / HISTORY_FILENAME)
    return str(Path(__file__).parent / HISTORY_FILENAME)


def _read_history(filepath: str) -> list:
    """Read history file. Returns empty list if missing or invalid."""
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def _write_history(filepath: str, entries: list) -> None:
    """Write history entries to file."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2, default=str)


def hash_resume(text: str) -> str:
    """Generate a short hash of resume text for change detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def log_score(
    folder: str,
    score_type: str,
    score: float,
    details: dict = None,
    resume_hash: str = "",
    label: str = "",
) -> dict:
    """Log a scoring run to the history file.

    Parameters
    ----------
    folder : str
        Application folder (e.g., "../tailored-resumes/Deere - Embedded SWE").
    score_type : str
        "ats", "hr", or "combined".
    score : float
        The score value (0-100).
    details : dict, optional
        Component breakdown (keyword_score, phrase_score, etc.).
    resume_hash : str, optional
        Hash of the resume text for change detection.
    label : str, optional
        Human label for this version ("base", "v1", "v2", "final").

    Returns
    -------
    dict
        The entry that was logged.
    """
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "folder": folder,
        "score_type": score_type,
        "score": round(score, 1),
        "details": details or {},
        "resume_hash": resume_hash,
        "label": label,
    }

    # Write to per-folder history
    folder_path = _history_path(folder)
    folder_history = _read_history(folder_path)
    folder_history.append(entry)
    _write_history(folder_path, folder_history)

    # Also append to global history
    global_path = _history_path(None)
    global_history = _read_history(global_path)
    global_history.append(entry)
    _write_history(global_path, global_history)

    return entry


def get_history(folder: str = None, score_type: str = None) -> list:
    """Get scoring history, optionally filtered.

    Parameters
    ----------
    folder : str, optional
        If given, return only entries for this folder.
    score_type : str, optional
        If given, filter to "ats", "hr", or "combined".

    Returns
    -------
    list[dict]
        Matching history entries, ordered by timestamp.
    """
    if folder:
        entries = _read_history(_history_path(folder))
    else:
        entries = _read_history(_history_path(None))

    if score_type:
        entries = [e for e in entries if e.get("score_type") == score_type]

    return entries


def format_progression(folder: str) -> str:
    """Format score history for a folder as a progression table.

    Returns
    -------
    str
        Human-readable progression table.
    """
    entries = get_history(folder)
    if not entries:
        return f"No score history for: {folder}"

    lines = [
        f"Score Progression: {folder}",
        "-" * 70,
        f"{'Label':<10} {'Type':<8} {'Score':>7} {'Hash':<14} {'Timestamp':<20}",
        "-" * 70,
    ]

    for e in entries:
        label = e.get("label", "")[:10] or "-"
        stype = e.get("score_type", "?")[:8]
        score = f"{e.get('score', 0):.1f}%"
        rhash = e.get("resume_hash", "")[:12] or "-"
        ts = e.get("timestamp", "")[:19]
        lines.append(f"{label:<10} {stype:<8} {score:>7} {rhash:<14} {ts:<20}")

    # Show improvement if there are at least 2 ATS entries
    ats_entries = [e for e in entries if e.get("score_type") == "ats"]
    if len(ats_entries) >= 2:
        first = ats_entries[0]["score"]
        last = ats_entries[-1]["score"]
        delta = last - first
        lines.append("-" * 70)
        lines.append(f"ATS Improvement: {first:.1f}% → {last:.1f}% ({'+' if delta >= 0 else ''}{delta:.1f}%)")

    hr_entries = [e for e in entries if e.get("score_type") == "hr"]
    if len(hr_entries) >= 2:
        first = hr_entries[0]["score"]
        last = hr_entries[-1]["score"]
        delta = last - first
        lines.append(f"HR  Improvement: {first:.1f}% → {last:.1f}% ({'+' if delta >= 0 else ''}{delta:.1f}%)")

    return "\n".join(lines)


def _cli() -> None:
    """CLI for inspecting score history."""
    parser = argparse.ArgumentParser(description="Score History Viewer")
    parser.add_argument("--show", metavar="FOLDER", help="Show history for a folder")
    parser.add_argument("--show-all", action="store_true", help="Show global history")
    parser.add_argument("--type", choices=["ats", "hr", "combined"], help="Filter by score type")

    args = parser.parse_args()

    if args.show:
        print(format_progression(args.show))
    elif args.show_all:
        entries = get_history(score_type=args.type)
        if not entries:
            print("No score history found.")
            return
        for e in entries:
            label = e.get("label", "-")
            folder = e.get("folder", "?")
            stype = e.get("score_type", "?")
            score = e.get("score", 0)
            ts = e.get("timestamp", "")[:19]
            print(f"[{ts}] {folder} | {stype}: {score:.1f}% ({label})")
    else:
        parser.print_help()


if __name__ == "__main__":
    _cli()
