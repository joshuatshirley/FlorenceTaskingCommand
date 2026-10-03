"""Tests for _compose.py — currently pure pass-throughs, kept as named
seams for future formatting logic. Tests exist so a future change that
breaks the pass-through contract fails loudly.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import _compose as compose  # noqa: E402


def test_format_army_news_section_passthrough():
    assert compose.format_army_news_section("- a\n- b") == "- a\n- b"


def test_format_weather_section_passthrough():
    assert compose.format_weather_section("Today: sunny, 70°F") == "Today: sunny, 70°F"


def test_format_local_events_section_passthrough():
    assert compose.format_local_events_section("(none)") == "(none)"
