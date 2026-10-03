"""Tests for _sources.py extractors. Network calls are mocked — these
tests never touch the real network, so they're safe to run anywhere,
anytime, including in CI with no connectivity.
"""

from __future__ import annotations

import datetime as _dt
import sys
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import _sources as src  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def _mock_response(data: bytes):
    """Build a context-manager mock standing in for urllib's response object."""
    mock = MagicMock()
    mock.read.return_value = data
    mock.__enter__.return_value = mock
    mock.__exit__.return_value = False
    return mock


# ---------------------------------------------------------------------------
# extract_army_news
# ---------------------------------------------------------------------------

def test_extract_army_news_not_configured_on_empty_url():
    assert src.extract_army_news(feed_url="") == src.NOT_CONFIGURED_ARMY_NEWS


def test_extract_army_news_parses_titles_and_links():
    rss_bytes = (FIXTURES / "sample_war_gov_rss.xml").read_bytes()
    with patch("urllib.request.urlopen", return_value=_mock_response(rss_bytes)):
        out = src.extract_army_news(feed_url="https://example.invalid/rss")
    assert "[Example Headline One]" in out
    assert "[Example Headline Two]" in out
    assert "https://www.war.gov/News/News-Stories/Article/Article/0000001" in out


def test_extract_army_news_respects_max_items():
    rss_bytes = (FIXTURES / "sample_war_gov_rss.xml").read_bytes()
    with patch("urllib.request.urlopen", return_value=_mock_response(rss_bytes)):
        out = src.extract_army_news(feed_url="https://example.invalid/rss", max_items=1)
    assert "Example Headline One" in out
    assert "Example Headline Two" not in out


def test_extract_army_news_url_error_returns_failure_literal():
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("no connection"),
    ):
        out = src.extract_army_news(feed_url="https://example.invalid/rss")
    assert out.startswith("(fetch failed:")


def test_extract_army_news_malformed_xml_returns_failure_literal():
    with patch("urllib.request.urlopen", return_value=_mock_response(b"not xml at all")):
        out = src.extract_army_news(feed_url="https://example.invalid/rss")
    assert out.startswith("(fetch failed:")


def test_extract_army_news_empty_feed_returns_explicit_note():
    empty_rss = b'<?xml version="1.0"?><rss><channel></channel></rss>'
    with patch("urllib.request.urlopen", return_value=_mock_response(empty_rss)):
        out = src.extract_army_news(feed_url="https://example.invalid/rss")
    assert "no items" in out


# ---------------------------------------------------------------------------
# extract_weather
# ---------------------------------------------------------------------------

def test_extract_weather_not_configured_on_empty_url():
    assert src.extract_weather(forecast_url="") == src.NOT_CONFIGURED_WEATHER


def test_extract_weather_formats_daytime_period():
    json_bytes = (FIXTURES / "sample_nws_forecast.json").read_bytes()
    with patch("urllib.request.urlopen", return_value=_mock_response(json_bytes)):
        out = src.extract_weather(forecast_url="https://example.invalid/forecast")
    assert out == "This Afternoon: Showers And Thunderstorms Likely, 82°F"


def test_extract_weather_url_error_returns_failure_literal():
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("no connection"),
    ):
        out = src.extract_weather(forecast_url="https://example.invalid/forecast")
    assert out.startswith("(fetch failed:")


def test_extract_weather_unexpected_shape_returns_failure_literal():
    with patch("urllib.request.urlopen", return_value=_mock_response(b'{"unexpected": true}')):
        out = src.extract_weather(forecast_url="https://example.invalid/forecast")
    assert out.startswith("(fetch failed:")


# ---------------------------------------------------------------------------
# extract_local_events
# ---------------------------------------------------------------------------

def test_extract_local_events_is_always_not_configured():
    assert src.extract_local_events() == src.NOT_CONFIGURED_LOCAL_EVENTS


# ---------------------------------------------------------------------------
# extract_rotating_fact
# ---------------------------------------------------------------------------

def test_extract_rotating_fact_missing_file_returns_literal(tmp_path):
    out = src.extract_rotating_fact(_dt.date(2026, 1, 1), reference_path=tmp_path / "nope.md")
    assert "not found" in out


def test_extract_rotating_fact_empty_file_returns_literal(tmp_path):
    empty = tmp_path / "empty.md"
    empty.write_text("no headings here at all", encoding="utf-8")
    out = src.extract_rotating_fact(_dt.date(2026, 1, 1), reference_path=empty)
    assert "no sections" in out


def test_extract_rotating_fact_rotates_by_day_of_year():
    ref = FIXTURES / "sample_reference.md"
    # day-of-year 1 (Jan 1) % 2 sections -> index 1 -> "Section Two"
    out_day1 = src.extract_rotating_fact(_dt.date(2026, 1, 1), reference_path=ref)
    # day-of-year 2 (Jan 2) % 2 sections -> index 0 -> "Section One"
    out_day2 = src.extract_rotating_fact(_dt.date(2026, 1, 2), reference_path=ref)
    assert "Section Two" in out_day1
    assert "Section One" in out_day2
    assert out_day1 != out_day2


def test_extract_rotating_fact_truncates_long_body(tmp_path):
    long_body = "word " * 200  # well over 400 chars
    ref = tmp_path / "long.md"
    ref.write_text(f"# Title\n\n## Only Section\n\n{long_body}\n", encoding="utf-8")
    out = src.extract_rotating_fact(_dt.date(2026, 1, 1), reference_path=ref)
    assert out.endswith("...")
    assert len(out) < len(long_body)
