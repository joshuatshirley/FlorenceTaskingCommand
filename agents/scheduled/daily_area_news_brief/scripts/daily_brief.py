#!/usr/bin/env python
"""daily_brief — pure-Python daily Army/area-news brief generator.

Fetches live Army/DoD news (war.gov RSS) and local weather (NWS API),
pulls one rotating fact from the sanitized Florence-area reference, and
substitutes into TEMPLATE.md, writing one dated file to briefings/.

No LLM in this path. Every source either returns real content or an
explicit literal (never fabricated, never silently blank) — see
_sources.py. A quality check runs before publish; a failed check blocks
the write rather than publishing something broken (see SPEC.md / QUALITY_CHECK.md).

Exit codes:
    0 = success (brief written)
    1 = generic failure (caught at the top — stderr names the cause)
    2 = template not found
    3 = quality check failed — brief NOT written
    4 = write failed

Usage:
    python daily_brief.py                  # today
    python daily_brief.py --date 2026-06-12
    python daily_brief.py --force           # overwrite today's brief if it already exists
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from _sources import (  # noqa: E402
    extract_army_news,
    extract_local_events,
    extract_rotating_fact,
    extract_weather,
)
from _compose import (  # noqa: E402
    format_army_news_section,
    format_local_events_section,
    format_weather_section,
)

# =============================================================================
# Paths — relative to this repo. Edit here if the repo layout moves.
# =============================================================================

REPO_ROOT = _SCRIPT_DIR.parents[3]
TEMPLATE_PATH = _SCRIPT_DIR.parent / "TEMPLATE.md"
BRIEFINGS_DIR = REPO_ROOT / "briefings"
REFERENCE_PATH = (
    REPO_ROOT / "knowledge" / "local_reference" / "florence_area_resource_reference.md"
)

# A PII section's rotating-fact source must stay a known-safe file.
# If this ever points somewhere else, the quality check below should fail
# loudly rather than trust an unreviewed path.
_ALLOWED_REFERENCE_PATH = REFERENCE_PATH


# =============================================================================
# Helpers
# =============================================================================

def parse_date(arg: str | None) -> _dt.date:
    if arg is None:
        return _dt.date.today()
    return _dt.date.fromisoformat(arg)


def collect_sources(date: _dt.date) -> dict[str, str]:
    """Run every extractor; return the substitution dict for TEMPLATE.md.
    All substitutions are pure strings — placeholder names map 1:1 to
    template tokens.
    """
    army_news = format_army_news_section(extract_army_news())
    weather = format_weather_section(extract_weather())
    local_events = format_local_events_section(extract_local_events())
    rotating_fact = extract_rotating_fact(date, reference_path=REFERENCE_PATH)

    generated_at = _dt.datetime.now().replace(microsecond=0).isoformat()

    return {
        "{{DATE}}": date.isoformat(),
        "{{ARMY_NEWS_SECTION}}": army_news,
        "{{WEATHER_SECTION}}": weather,
        "{{LOCAL_EVENTS_SECTION}}": local_events,
        "{{ROTATING_AREA_FACT}}": rotating_fact,
        "{{GENERATED_TIMESTAMP}}": generated_at,
    }


def substitute(template: str, substitutions: dict[str, str]) -> str:
    result = template
    for token, value in substitutions.items():
        result = result.replace(token, value)
    return result


# =============================================================================
# Quality check (QUALITY_CHECK.md) — run before every publish
# =============================================================================

# Conservative patterns: a 9-digit SSN-shaped string, or a line that looks
# like an individual's name tied to a date of birth. This is a backstop,
# not the primary control — the primary control is that no source in this
# pipeline ever touches applicant or personal-family data in the first
# place (see SPEC.md "Hard rules").
_SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def run_quality_check(rendered: str, date: _dt.date) -> list[str]:
    """Return a list of problems found (empty list = pass). Never raises —
    a quality check that can crash defeats its own purpose.
    """
    problems: list[str] = []

    if _SSN_PATTERN.search(rendered):
        problems.append("SSN-shaped pattern found in rendered brief — blocking.")

    if "{{" in rendered and "}}" in rendered:
        problems.append("Unsubstituted {{TOKEN}} placeholder remains in rendered brief.")

    if date.isoformat() not in rendered:
        problems.append("Rendered brief does not contain today's date — possible template mismatch.")

    return problems


# =============================================================================
# Atomic write
# =============================================================================

def atomic_write(content: str, target: Path) -> None:
    """Write `content` to `target` via a sibling .tmp file + os.replace, so a
    crash mid-write never leaves a partially-written brief. Raises OSError
    on failure (caller handles).
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path_str = tempfile.mkstemp(
        prefix=target.name + ".", suffix=".tmp", dir=str(target.parent)
    )
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        os.replace(tmp_path, target)
    except OSError:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise


# =============================================================================
# Main
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the daily area/Army news brief.")
    parser.add_argument("--date", help="ISO date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite today's brief if one already exists (default: skip).",
    )
    args = parser.parse_args(argv)

    try:
        date = parse_date(args.date)
    except ValueError as exc:
        print(f"daily_brief: bad --date value: {exc}", file=sys.stderr)
        return 1

    if not TEMPLATE_PATH.is_file():
        print(f"daily_brief: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        return 2

    output_path = BRIEFINGS_DIR / f"{date.isoformat()}.md"
    if output_path.exists() and not args.force:
        print(
            f"daily_brief: {output_path} already exists; not overwriting "
            "(use --force to regenerate).",
            file=sys.stderr,
        )
        return 0

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    substitutions = collect_sources(date)
    rendered = substitute(template, substitutions)

    problems = run_quality_check(rendered, date)
    if problems:
        print("daily_brief: quality check FAILED — brief not written:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 3

    try:
        atomic_write(rendered, output_path)
    except OSError as exc:
        print(f"daily_brief: write failed: {exc}", file=sys.stderr)
        return 4

    print(f"Daily brief {date.isoformat()} written: {output_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
