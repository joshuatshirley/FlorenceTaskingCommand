# FlorenceTaskingCommand

Multi-tiered AI agent definitions for USAREC recruiting guidance, grounded strictly in official Army/DoD doctrine rather than model knowledge. Built for eventual deployment on a DoD-authorized AI platform (not yet finalized — see `docs/platform_import_notes.md`).

## What's in here — and what deliberately is not

**In scope:**
- `agents/` — the agent hierarchy: a top-level router (`00_router/`) using an Algorithm-of-Thoughts framework, and seven fully-built domain agents, each with its own policy-verification sub-agent: Medical Triage, Legal Adjudication, Prospecting, Family/Dependency, Test & Classification, Prior Service/Re-entry, and Administrative Forms.
- `knowledge/doctrine/` — public-domain Army regulations, DoD instructions, and USAREC manuals in markdown, extracted from official PDFs. No FOUO/CUI material.
- `knowledge/standards_registry/` — machine-readable rule catalogs (eligibility standards, DoDI 6130.03 disqualifying conditions, SF86/DD1966/DD2807-2 form-coverage maps) derived from the sources above. Pure rule/schema metadata — no applicant data.
- `data/synthetic/` — **fabricated** CSVs shaped like the real applicant data schema (or, for Prospecting, generic lead-tracking fields), for testing agent parsing logic. Every row is invented.
- `flows/` — one mermaid diagram per domain, showing how a query moves through the agent hierarchy.

**Explicitly out of scope:**
- **Real applicant PII.** Never goes in this repo. Real applicant data lives only in a local, encrypted, no-sync vault under a personal operating policy — it is not synced anywhere, including here. (The repo and this content are public; that makes the "no real PII, ever" rule stricter to honor, not looser.)
- Station-specific SOPs, recruiting tactics, or market-intelligence documents. Only public-domain regulations/doctrine/manuals are included.
- A finalized target-platform format. Agent definitions here are platform-agnostic markdown/JSON; the import mapping for a specific DoD AI platform is still open — see `docs/platform_import_notes.md`.

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
knowledge/
  doctrine/AR/, DoDI/, Pamphlets/, Manuals/, Forms/   source regulations/manuals/forms, markdown
  standards_registry/                 machine-readable rule + form-coverage catalogs, with provenance README
data/synthetic/                       fabricated, schema-matched test data (one CSV per domain that needs it)
flows/                                one mermaid diagram per domain
docs/platform_import_notes.md         open question: which DoD AI platform, and what it needs
```

## Why doctrine-grounded, not model-knowledge

Recruiting eligibility and medical/legal adjudication rulings have to trace to an exact regulation and paragraph — not a model's general training. Every agent prompt in this repo is written to cite `knowledge/doctrine/` and `knowledge/standards_registry/` rather than reason from memory, and the level-3 sub-agent's entire job is to verify that cross-walk before any guidance reaches a recruiter.
