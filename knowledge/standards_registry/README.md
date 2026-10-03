# Standards Registry

Machine-readable rule catalogs derived from the regulations in `knowledge/doctrine/`. Every row is a **rule about a regulation**, not applicant data — no PII of any kind lives in these files.

## `dodi_6130_03_seed.json`

43 DoDI 6130.03 disqualifying conditions across 18 body-system categories (the ~50 highest-frequency conditions a recruiter actually encounters — not exhaustive of the full regulation). Each entry carries:

- ICD-10 code(s) for matching
- A `rule` object the agent evaluates (`simple`, `temporal_treatment`, `temporal_episode`, `recurrence`, `surgery_recency`, `severity_threshold`, `asthma_temporal` — see `_meta.rule_types` in the file for definitions)
- Waiver authority and the exact citation back to DoDI 6130.03

This is the primary grounding source for `agents/20_medical_triage/`.

## `army_standards_seed.json`

25 general eligibility standards (age, AFQT, citizenship, dependents, felony, etc.) sourced from AR 601-210 and DoDI 1304.26. Primary grounding source for `agents/40_family_dependency/` (dependents) and `agents/50_test_classification/` (AFQT minimum), and a secondary source for `agents/20_medical_triage/` and `agents/30_legal_adjudication/` (felony) where their domain interacts with a general standard.

## `sf86_question_catalog.json`, `sf86_subquestion_audit.json`, `dd1966_subquestion_audit.json`, `dd2807_subquestion_audit.json`

Section- and sub-question-level coverage maps for SF 86, DD 1966, and DD 2807-2 — each question/sub-question tagged with a coverage rating (FULL/PARTIAL/FLAG/MISSING or CAPTURED/CAPTURED_ENC/DERIVED/NOTES) and a pointer to the data field it maps to. Pure schema metadata, not applicant answers. Primary grounding source for `agents/70_administrative_forms/`.

## Provenance

All files are copied as-is from the Station Commander project's local doctrine RAG system (`Station_Commander/Army_Doctrine/.rag/data/`), where they are kept current by a regulation-refresh workflow tied to AR/DoDI publication updates. If the source regulation or schema changes, these files need to be re-synced — they are not auto-updating in this repo.
