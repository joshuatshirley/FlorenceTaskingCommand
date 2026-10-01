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

## Candidates considered (none selected)

- **NIPRGPT** — Army/DoD internal ChatGPT-like tool on NIPRNet. Likely supports custom instructions/GPTs; file-upload-based knowledge grounding rather than a managed vector store, as far as currently known.
- **Ask Sage** — DoD-authorized multi-model platform with an explicit agent/workflow builder; would likely support the router → domain agent → sub-agent structure more natively than a single-prompt tool.
- **CamoGPT or other service-specific tool** — not yet evaluated.

## Next step

Once the platform is confirmed, this file should be rewritten as a concrete import guide (exact upload steps, knowledge-base chunking requirements, tool/function schema for the standards registry) rather than an open comparison.
