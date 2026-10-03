# Daily Brief Scripts

Pure stdlib Python (no `pip install` needed) implementing the `SPEC.md` pipeline. Mirrors the pattern proven in Station Commander's `sc_morning_brief.py`: extractor module per source (never raises, returns real content or an explicit literal), a thin composer module, an orchestrator with a CLI, a quality check before publish, and an atomic write.

## Run it

```bash
python daily_brief.py                    # today, skips if today's brief already exists
python daily_brief.py --date 2026-06-12   # a specific date
python daily_brief.py --force             # regenerate even if today's brief exists
```

Output: `<repo root>/briefings/<date>.md`.

## Files

- `daily_brief.py` — orchestrator + CLI. `collect_sources()` → `substitute()` → `run_quality_check()` → `atomic_write()`.
- `_sources.py` — the three live/semi-live extractors + the rotating-fact reader. **Verified working 2026-10-03**: Army/DoD news via the official war.gov (formerly defense.gov) news RSS feed, weather via `api.weather.gov` (no key required). Local events has no reliable free keyless source and is an honest "not configured" stub — see the docstring on `extract_local_events()` for how to wire a real one later.
- `_compose.py` — currently pure pass-throughs; kept as a seam for future formatting logic without touching `daily_brief.py`.
- `tests/` — 30 pytest cases, all network calls mocked (no live calls in CI). Run with `python -m pytest tests/ -v` (requires `pip install pytest` — the shipped scripts themselves have zero dependencies, only the test suite does).

## Wiring to a real cron

Nothing here depends on Hermes, Task Scheduler, or any specific platform — it's a plain CLI script. Point whatever scheduler the eventual DoD platform provides at `python daily_brief.py` once a day, early enough that the brief is ready before the station's first battle-rhythm event (the `doctrine intel` precedent in Station Commander runs at 0530).

## If war.gov moves again

It already moved once (`defense.gov` → `www.war.gov`, same RSS path). If `WAR_GOV_RSS_URL` in `_sources.py` starts returning errors, check whether the site moved again before assuming the feed is just down — don't guess a replacement URL; verify it actually returns parseable RSS first (same discipline this whole agent enforces on its own output).
