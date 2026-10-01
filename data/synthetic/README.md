# Synthetic Test Data

`applicant_medical_profile_synthetic.csv` is **entirely fabricated**. Every `synthetic_applicant_id`, date, and medical detail was invented to exercise the Medical Triage agent's logic against a range of `dodi_6130_03_seed.json` rule types (`temporal_treatment` — ADHD; `asthma_temporal` — asthma; `surgery_recency` — ACL reconstruction; permanent DQ — Type 1 Diabetes). No row corresponds to a real applicant, living or deceased.

Column names mirror (a subset of) the real applicant data model's `applicant_profile`, `applicant_medical_event`, and `applicant_mental_health_detail` tables — shape only, not source. The real schema lives in `Station_Commander/Army_Doctrine/.rag/scripts/db/008_schema.sql` and `010_schema.sql`, which stay local and are never checked into this repo.

## Why synthetic instead of real

Real applicant PII is handled under a separate, explicit local-only policy: encrypted at rest, never synced off-machine, audit-logged. That policy exists specifically so applicant data never ends up somewhere like a GitHub repo. This CSV lets the agents here be tested against the right shape of data without touching that boundary.

## If you need more synthetic rows

Add fabricated rows following the same column set, or add new columns if a future domain agent needs a field this slice doesn't cover (e.g., legal events for Legal Adjudication). Keep `synthetic_applicant_id` in the `SYN-####` format so it's never mistaken for a real identifier.
