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

Three agents need more than static retrieval — they need the platform to supply a **live** tool, not just a knowledge-base corpus:

| Agent | Live tool needed | Why it can't be static |
|---|---|---|
| `agents/90_social_media_content/` | Web/trend search + current news | "Current pop-culture trend" and "current Army news" are undefined without a live source; the agent prompt explicitly forbids fabricating either from memory |
| `agents/scheduled/daily_area_news_brief/` | Army news feed/RSS + local weather/events feed | Same reasoning — this is a daily digest, not a Q&A agent, so there's no human in the loop to catch a bad guess before it's published |

Until a platform is chosen, both agents' prompts are written to **fail safely**: if no live tool is wired up, they must output an explicit "no live source configured" literal rather than inventing content. When a platform is picked, this is the first thing to wire: whatever that platform's web-search/news/function-calling primitive is, point it at these two agents before anything else.

## Scheduled/cron execution requirement (new as of the Daily Brief agent)

`agents/scheduled/daily_area_news_brief/` is not a request-routed agent — it needs the platform (or whatever wraps it) to support a cron-style trigger and a script-driven aggregation step with the LLM kept out of the unattended fact-collection path (see its own `SPEC.md` for why). If the chosen platform has no native scheduling primitive, this agent will need an external scheduler (same shape as the existing `doctrine intel` / Hermes cron pattern in the Station Commander project) calling into whatever the platform exposes for a single run.

## Candidates considered (none selected)

- **NIPRGPT** — Army/DoD internal ChatGPT-like tool on NIPRNet. Likely supports custom instructions/GPTs; file-upload-based knowledge grounding rather than a managed vector store, as far as currently known.
- **Ask Sage** — DoD-authorized multi-model platform with an explicit agent/workflow builder; would likely support the router → domain agent → sub-agent structure more natively than a single-prompt tool.
- **CamoGPT or other service-specific tool** — not yet evaluated.

## Next step

Once the platform is confirmed, this file should be rewritten as a concrete import guide (exact upload steps, knowledge-base chunking requirements, tool/function schema for the standards registry) rather than an open comparison.
