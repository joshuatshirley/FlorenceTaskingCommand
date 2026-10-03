"""Composition helpers for daily_brief.py.

Pure-Python, deterministic, no LLM. The only "composition" this brief
needs beyond the raw extracted sections is light formatting — unlike
sc_morning_brief.py's TOP_OF_DAY prioritization, there's no ranking
decision to make across these three independent sections.
"""

from __future__ import annotations


def format_army_news_section(raw: str) -> str:
    """Pass through as-is — extract_army_news() already returns markdown
    bullets or an explicit literal. Kept as a named seam so a future
    revision can add formatting without touching daily_brief.py.
    """
    return raw


def format_weather_section(raw: str) -> str:
    return raw


def format_local_events_section(raw: str) -> str:
    return raw
