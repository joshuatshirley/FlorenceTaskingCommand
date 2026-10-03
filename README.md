# FlorenceTaskingCommand

Multi-tiered AI agent definitions for USAREC recruiting guidance, grounded strictly in official Army/DoD doctrine rather than model knowledge. Built for eventual deployment on a DoD-authorized AI platform (not yet finalized — see `docs/platform_import_notes.md`).

## What's in here — and what deliberately is not

**In scope:**
- `agents/` — a top-level router (`00_router/`, Algorithm-of-Thoughts framework) dispatching to nine query-routed domain agents (Medical Triage, Legal Adjudication, Prospecting, Family/Dependency, Test & Classification, Prior Service/Re-entry, Administrative Forms, Training Development, Social Media Content), each with its own policy-verification sub-agent — plus one agent the router does *not* dispatch to: `agents/scheduled/daily_area_news_brief/`, a cron-triggered daily digest (see its own `SPEC.md`).
- `knowledge/doctrine/` — public-domain Army regulations, DoD instructions, and USAREC manuals in markdown, extracted from official PDFs. No FOUO/CUI material.
- `knowledge/standards_registry/` — machine-readable rule catalogs (eligibility standards, DoDI 6130.03 disqualifying conditions, SF86/DD1966/DD2807-2 form-coverage maps) derived from the sources above. Pure rule/schema metadata — no applicant data.
- `knowledge/local_reference/` — a **sanitized, de-personalized** Florence-area community reference (schools, parks, churches, utilities, etc.), rewritten from a family-relocation planning document with every personal detail (individual preferences, specific family members, personal checklists) stripped out. Generic "local knowledge," not advice specific to any individual.
- `data/synthetic/` — **fabricated** CSVs shaped like the real applicant data schema (or generic tracking fields for the non-adjudication domains), for testing agent parsing logic. Every row is invented.
- `flows/` — one diagram per agent, showing how a query (or, for the daily brief, a cron trigger) moves through the pipeline.

**Explicitly out of scope:**
- **Real applicant PII**, and **real personal/family information about the repo's author** — neither ever goes in this repo. Real applicant data lives only in a local, encrypted, no-sync vault under a personal operating policy. Personal family content gets stripped to generic reference material before anything derived from it is included (see `knowledge/local_reference/`). The repo is public; that makes both rules stricter to honor, not looser.
- Station-specific **recruiting tactics** (prospecting-location/approach guidance tied to specific local businesses) and **market-intelligence** documents — these stay out even where they live alongside content that was brought in (e.g., `Florence_SC_Area_Guide.md` was deliberately excluded from the Florence-area reference work for exactly this reason).
- A finalized target-platform format. Agent definitions here are platform-agnostic markdown/JSON; the import mapping for a specific DoD AI platform is still open — see `docs/platform_import_notes.md`, which now also tracks which agents need a **live** search/news tool the static knowledge base can't provide.

## Structure

```
agents/
  00_router/SYSTEM_PROMPT.md          top-level Algorithm-of-Thoughts router + routing table
  10_prospecting/                     level-2 + sub_agents/POLICY_VERIFIER.md (level-3)
  20_medical_triage/                  "
  30_legal_adjudication/              "
  40_family_dependency/               "
  50_test_classification/             "
  60_prior_service/                   "
  70_administrative_forms/            "
  80_training_development/            "
  90_social_media_content/            " (needs a live search/news tool)
  scheduled/daily_area_news_brief/    cron-triggered, NOT router-dispatched — SPEC.md + TEMPLATE.md + QUALITY_CHECK.md
                                       scripts/ — working stdlib-only implementation, 30 passing tests, zero deps
knowledge/
  doctrine/AR/, DoDI/, Pamphlets/, Manuals/, Forms/, ADP/, FM/   source regulations/manuals/forms, markdown
  standards_registry/                 machine-readable rule + form-coverage catalogs, with provenance README
  local_reference/                    sanitized Florence-area community reference (no personal content)
data/synthetic/                       fabricated, schema-matched test data (one CSV per domain that needs it)
flows/                                one diagram per agent
docs/platform_import_notes.md         open question: which DoD AI platform, what it needs, which agents need a live tool
```

## Why doctrine-grounded, not model-knowledge

Recruiting eligibility and medical/legal adjudication rulings have to trace to an exact regulation and paragraph — not a model's general training. Every agent prompt in this repo is written to cite `knowledge/doctrine/` and `knowledge/standards_registry/` rather than reason from memory, and the level-3 sub-agent's entire job is to verify that cross-walk before any guidance reaches a recruiter.
