"""Tests for daily_brief.py's own logic: substitution, quality check, and
atomic write. Source extraction itself is tested in test_sources.py —
these tests patch collect_sources where the full pipeline matters.
"""

from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path
from unittest.mock import patch

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import daily_brief as db  # noqa: E402


# ---------------------------------------------------------------------------
# parse_date
# ---------------------------------------------------------------------------

def test_parse_date_none_returns_today():
    assert db.parse_date(None) == _dt.date.today()


def test_parse_date_explicit_iso():
    assert db.parse_date("2026-06-12") == _dt.date(2026, 6, 12)


# ---------------------------------------------------------------------------
# substitute
# ---------------------------------------------------------------------------

def test_substitute_replaces_every_token():
    template = "Date: {{DATE}}. News: {{NEWS}}."
    out = db.substitute(template, {"{{DATE}}": "2026-01-01", "{{NEWS}}": "nothing"})
    assert out == "Date: 2026-01-01. News: nothing."


def test_substitute_leaves_unknown_tokens_alone():
    template = "{{KNOWN}} and {{UNKNOWN}}"
    out = db.substitute(template, {"{{KNOWN}}": "yes"})
    assert out == "yes and {{UNKNOWN}}"


# ---------------------------------------------------------------------------
# run_quality_check
# ---------------------------------------------------------------------------

def test_quality_check_passes_clean_brief():
    rendered = "# Brief 2026-06-12\n\nNo issues here."
    problems = db.run_quality_check(rendered, _dt.date(2026, 6, 12))
    assert problems == []


def test_quality_check_catches_ssn_shaped_pattern():
    rendered = "# Brief 2026-06-12\n\nSomehow 123-45-6789 ended up here."
    problems = db.run_quality_check(rendered, _dt.date(2026, 6, 12))
    assert any("SSN" in p for p in problems)


def test_quality_check_catches_unsubstituted_token():
    rendered = "# Brief 2026-06-12\n\n{{STILL_A_TOKEN}}"
    problems = db.run_quality_check(rendered, _dt.date(2026, 6, 12))
    assert any("placeholder" in p for p in problems)


def test_quality_check_catches_missing_date():
    rendered = "# Brief for some other day\n\nNo date match here."
    problems = db.run_quality_check(rendered, _dt.date(2026, 6, 12))
    assert any("date" in p for p in problems)


# ---------------------------------------------------------------------------
# atomic_write
# ---------------------------------------------------------------------------

def test_atomic_write_creates_file(tmp_path):
    target = tmp_path / "subdir" / "out.md"
    db.atomic_write("hello world", target)
    assert target.read_text(encoding="utf-8") == "hello world"


def test_atomic_write_overwrites_existing(tmp_path):
    target = tmp_path / "out.md"
    target.write_text("old content", encoding="utf-8")
    db.atomic_write("new content", target)
    assert target.read_text(encoding="utf-8") == "new content"


# ---------------------------------------------------------------------------
# main() — end-to-end with sources mocked out
# ---------------------------------------------------------------------------

def test_main_writes_brief_with_mocked_sources(tmp_path, monkeypatch):
    template_path = tmp_path / "TEMPLATE.md"
    template_path.write_text(
        "# Brief {{DATE}}\n\n{{ARMY_NEWS_SECTION}}\n{{WEATHER_SECTION}}\n"
        "{{LOCAL_EVENTS_SECTION}}\n{{ROTATING_AREA_FACT}}\n{{GENERATED_TIMESTAMP}}\n",
        encoding="utf-8",
    )
    briefings_dir = tmp_path / "briefings"

    monkeypatch.setattr(db, "TEMPLATE_PATH", template_path)
    monkeypatch.setattr(db, "BRIEFINGS_DIR", briefings_dir)
    monkeypatch.setattr(
        db,
        "collect_sources",
        lambda date: {
            "{{DATE}}": date.isoformat(),
            "{{ARMY_NEWS_SECTION}}": "- Example headline",
            "{{WEATHER_SECTION}}": "Sunny, 70°F",
            "{{LOCAL_EVENTS_SECTION}}": "(none)",
            "{{ROTATING_AREA_FACT}}": "**Fact** — example",
            "{{GENERATED_TIMESTAMP}}": "2026-06-12T08:00:00",
        },
    )

    rc = db.main(["--date", "2026-06-12"])
    assert rc == 0

    written = briefings_dir / "2026-06-12.md"
    assert written.is_file()
    content = written.read_text(encoding="utf-8")
    assert "Example headline" in content
    assert "{{" not in content


def test_main_skips_existing_brief_without_force(tmp_path, monkeypatch):
    template_path = tmp_path / "TEMPLATE.md"
    template_path.write_text("{{DATE}}", encoding="utf-8")
    briefings_dir = tmp_path / "briefings"
    briefings_dir.mkdir()
    existing = briefings_dir / "2026-06-12.md"
    existing.write_text("already here", encoding="utf-8")

    monkeypatch.setattr(db, "TEMPLATE_PATH", template_path)
    monkeypatch.setattr(db, "BRIEFINGS_DIR", briefings_dir)

    rc = db.main(["--date", "2026-06-12"])
    assert rc == 0
    assert existing.read_text(encoding="utf-8") == "already here"
