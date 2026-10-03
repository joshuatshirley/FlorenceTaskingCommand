# Daily Area & Army News Brief — Spec

A cron-triggered daily agent, not a query-routed one. It does not go through the Level-1 Router and has no Algorithm-of-Thoughts "recruiter question" to process — it runs unattended on a schedule and produces one file.

## Why this is architecturally different from the other nine agents

The other nine agents answer a specific recruiter question and verify a specific claim against doctrine (a waiver call, a training citation, a compliance check). This agent has no claim to verify — it aggregates live information into a digest. Following the pattern already proven in this codebase (`doctrine intel` / `sc_morning_brief.py` — see `docs/platform_import_notes.md`), **the unattended aggregation step should be script-driven, not LLM-driven**: an LLM one-shot in a cron context cannot recover from a confused turn the way a multi-turn conversation can, which is exactly the failure mode that pattern was built to avoid. Use an LLM only for a thin narrative pass on top of already-collected, already-verified data — never let it originate facts in the unattended path.

## Schedule

Daily, once. (The existing `doctrine intel` precedent runs at 0530; this agent should run early enough that the brief is ready before the station's first battle-rhythm event of the day.)

## Pipeline

1. **Collect** (script, no LLM):
   - Army-wide news headlines relevant to recruiting — from whatever live news/RSS tool the hosting platform provides. If the platform has no such tool, this section must render as an explicit "no live Army news source configured" literal, never a guessed or remembered headline.
   - Local Florence-area snapshot — weather for the day, plus any notable local community events, from a live weather/local-events tool. Same empty-literal rule if no tool is configured.
   - One rotating fact from `knowledge/local_reference/florence_area_resource_reference.md` (the sanitized, de-personalized area reference — cycle through its sections so the same fact doesn't repeat every day).

2. **Compose** (script or thin LLM pass): assemble the three sections into the template below. If an LLM pass is used for phrasing, it may only rephrase already-collected content — it may not add a fact that wasn't in the collected data.

3. **Publish**: write one dated file, `briefings/<YYYY-MM-DD>.md`, following `TEMPLATE.md`.

## Hard rules

- **No PII, ever.** No applicant data, no named individuals, no personal family content — this agent has no legitimate reason to touch any of that, unlike the eligibility-adjudication agents which at least discuss hypothetical/aggregate scenarios.
- **No fabricated "current" content.** If a live tool isn't available for a section, say so plainly in the output rather than guessing. This is the same anti-hallucination rule as `agents/90_social_media_content/`, applied to an unattended context where there's no human in the loop to catch a bad guess before it's published.
- **One file per day**, never overwritten silently — if the agent runs twice in a day, it should either skip or explicitly version, not silently clobber the first run's output.

## Reference implementation pattern

Mirror `Station_Commander/Army_Doctrine/.rag/scripts/` A1 pattern (`sc_morning_brief.py` + `_brief_sources.py` + `_brief_compose.py`): extractor module per source (each returns content or a specific empty-path literal, never raises), a composer module, an orchestrator with a CLI, and a template file with `{{TOKEN}}` placeholders shared between the automated path and any interactive/manual-trigger path.
