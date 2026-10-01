# FlorenceTaskingCommand

Multi-tiered AI agent definitions for USAREC recruiting guidance, grounded strictly in official Army/DoD doctrine rather than model knowledge. Built for eventual deployment on a DoD-authorized AI platform (not yet finalized — see `docs/platform_import_notes.md`).

## What's in here — and what deliberately is not

**In scope (this pass):**
- `agents/` — the agent hierarchy: a top-level router (`00_router/`) using an Algorithm-of-Thoughts framework, and one fully-built domain agent (`20_medical_triage/`) with its policy-verification sub-agent.
- `knowledge/doctrine/` — public-domain Army regulations and DoD instructions in markdown, extracted from official PDFs. No FOUO/CUI material.
- `knowledge/standards_registry/` — machine-readable rule catalogs (eligibility standards, DoDI 6130.03 disqualifying conditions) derived from the regulations above. Pure rule metadata — no applicant data.
- `data/synthetic/` — **fabricated** CSVs shaped like the real applicant data schema, for testing agent parsing logic. Every row is invented.
- `flows/` — diagrams of how a query moves through the agent hierarchy.

**Explicitly out of scope (this pass):**
- **Real applicant PII.** Never goes in this repo. Real applicant data lives only in a local, encrypted, no-sync vault under a personal operating policy — it is not synced anywhere, including here.
- Station-specific SOPs, recruiting tactics, or market-intelligence documents. Only public-domain regulations/doctrine are included until those are separately reviewed for releasability.
- A finalized target-platform format. Agent definitions here are platform-agnostic markdown/JSON; the import mapping for a specific DoD AI platform is still open.
- The remaining domain agents (Legal Adjudication, Prospecting, Family/Dependency, Test & Classification, Prior Service, Administrative Forms). Medical Triage is the first complete vertical slice, built to prove the pattern before replicating it.

## Structure

```
agents/
  00_router/SYSTEM_PROMPT.md          top-level Algorithm-of-Thoughts router + routing table
  20_medical_triage/
    AGENT_PROMPT.md                   level-2 domain agent
    sub_agents/POLICY_VERIFIER.md     level-3 doctrine cross-walk / compliance check
knowledge/
  doctrine/AR/, doctrine/DoDI/        source regulations, markdown
  standards_registry/                 machine-readable rule catalogs + provenance
data/synthetic/                       fabricated, schema-matched test data
flows/                                mermaid diagrams of the agent hand-off flow
docs/platform_import_notes.md         open question: which DoD AI platform, and what it needs
```

## Why doctrine-grounded, not model-knowledge

Recruiting eligibility and medical/legal adjudication rulings have to trace to an exact regulation and paragraph — not a model's general training. Every agent prompt in this repo is written to cite `knowledge/doctrine/` and `knowledge/standards_registry/` rather than reason from memory, and the level-3 sub-agent's entire job is to verify that cross-walk before any guidance reaches a recruiter.
