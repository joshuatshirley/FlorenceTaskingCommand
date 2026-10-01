# Standards Registry

Machine-readable rule catalogs derived from the regulations in `knowledge/doctrine/`. Every row is a **rule about a regulation**, not applicant data — no PII of any kind lives in these files.

## `dodi_6130_03_seed.json`

43 DoDI 6130.03 disqualifying conditions across 18 body-system categories (the ~50 highest-frequency conditions a recruiter actually encounters — not exhaustive of the full regulation). Each entry carries:

- ICD-10 code(s) for matching
- A `rule` object the agent evaluates (`simple`, `temporal_treatment`, `temporal_episode`, `recurrence`, `surgery_recency`, `severity_threshold`, `asthma_temporal` — see `_meta.rule_types` in the file for definitions)
- Waiver authority and the exact citation back to DoDI 6130.03

This is the primary grounding source for `agents/20_medical_triage/`.

## `army_standards_seed.json`

25 general eligibility standards (age, AFQT, citizenship, dependents, etc.) sourced from AR 601-210 and DoDI 1304.26. Referenced by the Medical Triage agent where medical qualification interacts with a general standard (e.g., waiver authority chains), and will be the primary grounding source for future domain agents (Legal Adjudication, etc.) once built.

## Provenance

Both files are copied as-is from the Station Commander project's local doctrine RAG system (`Station_Commander/Army_Doctrine/.rag/data/`), where they are kept current by a regulation-refresh workflow tied to AR/DoDI publication updates. If the source regulation changes, these files need to be re-synced — they are not auto-updating in this repo.
