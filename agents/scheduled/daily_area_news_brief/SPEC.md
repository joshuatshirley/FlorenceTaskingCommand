# Daily Area & Army News Brief — Spec

A cron-triggered daily agent, not a query-routed one. It does not go through the Level-1 Router and has no Algorithm-of-Thoughts "recruiter question" to process — it runs unattended on a schedule and produces one file.

## Why this is architecturally different from the other nine agents

The other nine agents answer a specific recruiter question and verify a specific claim against doctrine (a waiver call, a training citation, a compliance check). This agent has no claim to verify — it aggregates live information into a digest. Following the pattern already proven in this codebase (`doctrine intel` / `sc_morning_brief.py` — see `docs/platform_import_notes.md`), **the unattended aggregation step should be script-driven, not LLM-driven**: an LLM one-shot in a cron context cannot recover from a confused turn the way a multi-turn conversation can, which is exactly the failure mode that pattern was built to avoid. Use an LLM only for a thin narrative pass on top of already-collected, already-verified data — never let it originate facts in the unattended path.

## Schedule

Daily, once. (The existing `doctrine intel` precedent runs at 0530; this agent should run early enough that the brief is ready before the station's first battle-rhythm event of the day.)

## Pipeline — IMPLEMENTED in `scripts/` (2026-10-06)

1. **Collect** (script, no LLM — see `scripts/_sources.py`):
   - Army/DoD news headlines — **live and working**: the official war.gov (formerly defense.gov) news RSS feed, no API key required. Verified working at build time; see `scripts/_README.md` for what to do if the feed ever moves again.
   - Local weather — **live and working**: `api.weather.gov`, no API key required, pre-resolved gridpoint for the Florence, SC station area.
   - Local events — **honest stub**. No reliable free keyless API was found for hyper-local Florence event listings; this section always renders the explicit "no live local-events source configured" literal until a real source is wired (see `extract_local_events()`'s docstring for how).
   - One rotating fact from `knowledge/local_reference/florence_area_resource_reference.md` — cycles deterministically by day-of-year so it doesn't repeat on consecutive days.

2. **Compose** (`scripts/_compose.py`): currently pure pass-through formatting — no heuristic ranking is needed here (unlike `sc_morning_brief.py`'s TOP_OF_DAY logic) because these three sections are independent, not competing for "what matters most today."

3. **Quality check** (`daily_brief.py:run_quality_check()`): blocks publish on an SSN-shaped pattern, an unsubstituted `{{TOKEN}}`, or a brief missing today's date. See `QUALITY_CHECK.md`.

4. **Publish**: atomic write to `briefings/<YYYY-MM-DD>.md` (repo-root-relative), following `TEMPLATE.md`. Skips if today's brief already exists unless `--force` is passed.

Run it: `python scripts/daily_brief.py` (zero dependencies — stdlib only). Tests: `python -m pytest scripts/tests/ -v` (30 cases, all network calls mocked).

## Hard rules

- **No PII, ever.** No applicant data, no named individuals, no personal family content — this agent has no legitimate reason to touch any of that, unlike the eligibility-adjudication agents which at least discuss hypothetical/aggregate scenarios.
- **No fabricated "current" content.** If a live tool isn't available for a section, say so plainly in the output rather than guessing. This is the same anti-hallucination rule as `agents/90_social_media_content/`, applied to an unattended context where there's no human in the loop to catch a bad guess before it's published.
- **One file per day**, never overwritten silently — if the agent runs twice in a day, it should either skip or explicitly version, not silently clobber the first run's output.

## Reference implementation pattern

Mirror `Station_Commander/Army_Doctrine/.rag/scripts/` A1 pattern (`sc_morning_brief.py` + `_brief_sources.py` + `_brief_compose.py`): extractor module per source (each returns content or a specific empty-path literal, never raises), a composer module, an orchestrator with a CLI, and a template file with `{{TOKEN}}` placeholders shared between the automated path and any interactive/manual-trigger path.
