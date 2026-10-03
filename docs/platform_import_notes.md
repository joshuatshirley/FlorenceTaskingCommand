# Platform Import Notes (open question)

The target DoD AI platform has not been chosen yet. Everything in `agents/` and `knowledge/` is written as platform-agnostic markdown/JSON on purpose, so it isn't locked to one vendor's agent-builder format. This doc tracks what would need to map where once a platform is picked.

## What each platform generally needs, mapped to what exists here

| Platform need | Where it lives here |
|---|---|
| System prompt per agent | `agents/<tier>/SYSTEM_PROMPT.md` or `AGENT_PROMPT.md` — already written, copy/paste or API-upload as-is |
| Retrieval / knowledge base corpus | `knowledge/doctrine/*.md` — may need chunking to the platform's preferred size; currently chapter-level |
| Structured rule data for tool-use / function calling | `knowledge/standards_registry/*.json` — would likely become a tool the agent calls rather than raw context, depending on the platform's tool-calling support |
| Routing / orchestration between agents | `agents/00_router/SYSTEM_PROMPT.md` routing table — most platforms have their own multi-agent orchestration primitive; this table is the source of truth to translate from |
| Test data for validating agent behavior before go-live | `data/synthetic/` |

## Live-data tool requirement (new as of the Training/Social Media/Daily Brief agents)

Two agents need more than static retrieval — they need a **live** tool, not just a knowledge-base corpus. Status as of 2026-10-06:

| Agent | Live tool needed | Status |
|---|---|---|
| `agents/90_social_media_content/` | Web/trend search + current news | **Still platform-dependent.** "Current pop-culture trend" has no reliable free keyless API — this has to be whatever web-search/function-calling primitive the eventual platform provides. The agent prompt explicitly forbids fabricating a trend from memory if no tool is wired up. |
| `agents/scheduled/daily_area_news_brief/` | Army news + local weather (+ local events) | **Mostly solved, platform-independent.** `scripts/_sources.py` implements real, working, stdlib-only fetchers against the official war.gov news RSS and the free `api.weather.gov` — no platform-specific tool needed, no API key, no dependency to install. Only local-events has no reliable free keyless source and stays an honest "not configured" stub (see that agent's `_README.md` for how to wire one later). |

So the daily brief agent's live-data need is **already met independent of platform choice** — it just needs something to run `python daily_brief.py` on a schedule (see below). Social Media Content is the one agent still genuinely blocked on the platform decision for its live-data need.

## Scheduled/cron execution requirement (new as of the Daily Brief agent)

`agents/scheduled/daily_area_news_brief/` is not a request-routed agent — it needs the platform (or whatever wraps it) to support a cron-style trigger and a script-driven aggregation step with the LLM kept out of the unattended fact-collection path (see its own `SPEC.md` for why). If the chosen platform has no native scheduling primitive, this agent will need an external scheduler (same shape as the existing `doctrine intel` / Hermes cron pattern in the Station Commander project) calling into whatever the platform exposes for a single run.

## Candidates considered (none selected)

- **NIPRGPT** — Army/DoD internal ChatGPT-like tool on NIPRNet. Likely supports custom instructions/GPTs; file-upload-based knowledge grounding rather than a managed vector store, as far as currently known.
- **Ask Sage** — DoD-authorized multi-model platform with an explicit agent/workflow builder; would likely support the router → domain agent → sub-agent structure more natively than a single-prompt tool.
- **CamoGPT or other service-specific tool** — not yet evaluated.

## Next step

Once the platform is confirmed, this file should be rewritten as a concrete import guide (exact upload steps, knowledge-base chunking requirements, tool/function schema for the standards registry) rather than an open comparison.
