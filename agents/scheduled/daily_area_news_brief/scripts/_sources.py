"""Per-source extractors for daily_brief.py.

Each `extract_*` function returns a `str` block ready to substitute into
TEMPLATE.md. None of them raise on a missing/unreachable source — network
and parse failures are caught and turned into an explicit literal, same
discipline as Station_Commander's sc_morning_brief.py. Don't change the
literal strings without updating QUALITY_CHECK.md and anyone consuming
the brief.

Two sources are genuinely live right now (verified working 2026-10-03):
  - Army/DoD news: official Department of War news RSS (war.gov — the
    renamed defense.gov; the RSS path is unchanged post-rename).
  - Local weather: NWS api.weather.gov, no API key required.

One source has no reliable free keyless API and is an honest stub:
  - Local events: see extract_local_events() for how to wire a real one.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

# =============================================================================
# Empty-path / failure literals — DO NOT EDIT WITHOUT UPDATING QUALITY_CHECK.md
# =============================================================================

NOT_CONFIGURED_ARMY_NEWS = "No live Army news source configured for this run."
NOT_CONFIGURED_WEATHER = "No live local-area source configured for this run."
NOT_CONFIGURED_LOCAL_EVENTS = (
    "No live local-events source configured for this run. "
    "See _sources.py:extract_local_events() for how to wire one."
)

_FETCH_FAILED_PREFIX = "(fetch failed: "

# A descriptive User-Agent is required by api.weather.gov's usage policy.
# Replace the contact placeholder with a real address before production use.
_USER_AGENT = "FlorenceTaskingCommand-DailyBrief/1.0 (contact: recruiting-station@example.mil)"
_HTTP_TIMEOUT_SECONDS = 10


# =============================================================================
# Army / DoD news — war.gov (formerly defense.gov) RSS
# =============================================================================

# Verified working 2026-10-03. If this ever 404s, check whether the site has
# moved again (it redirected from defense.gov -> war.gov once already) and
# update this constant — don't silently fall back to a guessed URL.
WAR_GOV_RSS_URL = (
    "https://www.war.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=10"
)

_ARMY_NEWS_MAX_ITEMS = 5


def extract_army_news(
    feed_url: str = WAR_GOV_RSS_URL, max_items: int = _ARMY_NEWS_MAX_ITEMS
) -> str:
    """Fetch and format the top `max_items` headlines from the DoD news RSS feed.

    Returns a markdown bullet list, or a failure/not-configured literal.
    Never raises.
    """
    if not feed_url:
        return NOT_CONFIGURED_ARMY_NEWS

    try:
        request = urllib.request.Request(feed_url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(request, timeout=_HTTP_TIMEOUT_SECONDS) as response:
            raw = response.read()
    except urllib.error.URLError as exc:
        return f"{_FETCH_FAILED_PREFIX}{exc.reason})"
    except TimeoutError:
        return f"{_FETCH_FAILED_PREFIX}timeout after {_HTTP_TIMEOUT_SECONDS}s)"

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return f"{_FETCH_FAILED_PREFIX}malformed RSS XML: {exc})"

    items = root.findall("./channel/item")[:max_items]
    if not items:
        return "(DoD news feed returned no items this run)"

    lines = []
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title and link:
            lines.append(f"- [{title}]({link})")
        elif title:
            lines.append(f"- {title}")
    return "\n".join(lines) if lines else "(DoD news feed returned no usable items this run)"


# =============================================================================
# Local weather — NWS api.weather.gov
# =============================================================================

# Resolved once via GET https://api.weather.gov/points/34.1954,-79.7626 for
# the Florence, SC station area (2026-10-03). NWS gridpoints are stable for
# a given location; re-resolve via the /points endpoint if this ever starts
# 404ing rather than guessing a replacement.
NWS_FORECAST_URL = "https://api.weather.gov/gridpoints/ILM/23,66/forecast"


def extract_weather(forecast_url: str = NWS_FORECAST_URL) -> str:
    """Fetch today's NWS forecast period(s) for the Florence, SC gridpoint.

    Returns "<period name>: <short forecast>, high/low in detailedForecast"
    style text for the next 1-2 periods, or a failure/not-configured literal.
    Never raises.
    """
    if not forecast_url:
        return NOT_CONFIGURED_WEATHER

    try:
        request = urllib.request.Request(
            forecast_url,
            headers={"User-Agent": _USER_AGENT, "Accept": "application/geo+json"},
        )
        with urllib.request.urlopen(request, timeout=_HTTP_TIMEOUT_SECONDS) as response:
            raw = response.read()
    except urllib.error.URLError as exc:
        return f"{_FETCH_FAILED_PREFIX}{exc.reason})"
    except TimeoutError:
        return f"{_FETCH_FAILED_PREFIX}timeout after {_HTTP_TIMEOUT_SECONDS}s)"

    try:
        data = json.loads(raw)
        periods = data["properties"]["periods"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return f"{_FETCH_FAILED_PREFIX}unexpected NWS response shape: {exc})"

    if not periods:
        return "(NWS forecast returned no periods this run)"

    # Today's daytime period if present, else the first period available.
    today_period = next((p for p in periods if p.get("isDaytime")), periods[0])
    name = today_period.get("name", "Today")
    short = today_period.get("shortForecast", "")
    temp = today_period.get("temperature")
    unit = today_period.get("temperatureUnit", "F")
    temp_str = f"{temp}°{unit}" if temp is not None else "temperature unavailable"
    return f"{name}: {short}, {temp_str}"


# =============================================================================
# Local events — no reliable free keyless API found; honest stub
# =============================================================================

def extract_local_events() -> str:
    """Placeholder for a local Florence-area events feed.

    No free, keyless, reliably-available API for hyper-local Florence, SC
    event listings was found when this agent was built (2026-10-03). Rather
    than scrape a page likely to change shape without warning, this stays
    an explicit not-configured literal.

    To wire a real source later: City of Florence Parks & Recreation
    publishes a calendar on its website; if it ever exposes an iCal/JSON
    feed, parse it here the same way extract_weather() parses NWS JSON —
    fetch, parse defensively, return the not-configured literal on any
    failure, never raise.
    """
    return NOT_CONFIGURED_LOCAL_EVENTS


# =============================================================================
# Rotating local-knowledge fact — from the sanitized area reference
# =============================================================================

_REFERENCE_PATH = (
    Path(__file__).resolve().parents[4]
    / "knowledge"
    / "local_reference"
    / "florence_area_resource_reference.md"
)

_SECTION_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)


def _load_reference_sections(reference_path: Path) -> list[tuple[str, str]]:
    """Split the reference file into (heading, body) pairs by '## ' headings."""
    text = reference_path.read_text(encoding="utf-8")
    matches = [(m.group(1), m.start()) for m in _SECTION_RE.finditer(text)]
    if not matches:
        return []
    matches.append(("__END__", len(text)))

    sections: list[tuple[str, str]] = []
    for i in range(len(matches) - 1):
        heading, start = matches[i]
        _next_heading, end = matches[i + 1]
        body_start = text.find("\n", start) + 1
        body = text[body_start:end].strip()
        if body:
            sections.append((heading, body))
    return sections


def extract_rotating_fact(
    date: _dt.date, reference_path: Optional[Path] = None
) -> str:
    """Pick one section from the sanitized area reference, deterministically
    rotating by day-of-year so consecutive days don't repeat the same fact
    (for any reference file with more than one section).

    Returns the heading + a trimmed excerpt of its body, or an explicit
    literal if the reference file is missing or empty. Never raises on a
    missing file; a malformed file (unreadable) still surfaces as an
    OSError, which the caller/orchestrator is expected to let propagate —
    that's a repo-integrity problem, not a "live source unavailable" one.
    """
    path = reference_path if reference_path is not None else _REFERENCE_PATH
    if not path.is_file():
        return "(area reference file not found — see knowledge/local_reference/)"

    sections = _load_reference_sections(path)
    if not sections:
        return "(area reference file has no sections to draw from)"

    index = date.timetuple().tm_yday % len(sections)
    heading, body = sections[index]

    # Keep the fact short — first ~400 chars of the section body.
    excerpt = body if len(body) <= 400 else body[:400].rsplit(" ", 1)[0] + "..."
    return f"**{heading}** — {excerpt}"
