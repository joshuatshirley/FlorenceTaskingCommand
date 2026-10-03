# Daily Area & Army News Brief — Quality Check

Not a "Policy Verifier" in the Level-3 sense used elsewhere in this repo — there's no eligibility/compliance claim to cross-walk here. This is a lightweight pre-publish check the pipeline should run on every generated brief before writing it to `briefings/`.

**Implemented** as `run_quality_check()` in `scripts/daily_brief.py`, called automatically by `main()` before every write — it is not a separate manual step.

## Checks actually run at publish time (`run_quality_check()`)

1. **SSN-shaped pattern** (`\d{3}-\d{2}-\d{4}`) anywhere in the rendered brief — a backstop, not the primary control. The primary control is structural: no extractor in `_sources.py` ever touches applicant or personal-family data in the first place, so there should be nothing to catch.
2. **No unsubstituted `{{TOKEN}}`** left in the rendered output — catches a template/substitution-dict mismatch before it ships.
3. **Today's date string** must appear in the rendered brief — a cheap sanity check against a stale template or a date-parsing bug.

## Guaranteed by construction, not by a runtime scan

- **No fabricated-as-fact content**: `extract_army_news()` and `extract_weather()` only ever return real fetched content or one of the named failure/not-configured literals (see `_sources.py`) — there's no code path that invents a headline or forecast.
- **Rotating fact is sourced**: `extract_rotating_fact()` only ever reads from `knowledge/local_reference/florence_area_resource_reference.md` — it cannot return text from anywhere else.

## File hygiene

Handled in `daily_brief.py:main()`, not in the quality-check function itself: the script skips writing if `briefings/<date>.md` already exists, unless `--force` is passed — so a double run never silently clobbers the first run's output.

## On failure

`run_quality_check()` returning any problems blocks the write entirely (`daily_brief.py` exits 3) — nothing partial gets published. A missing brief for one day is a minor, recoverable gap; a published brief containing a PII-shaped pattern is not recoverable once distributed.
