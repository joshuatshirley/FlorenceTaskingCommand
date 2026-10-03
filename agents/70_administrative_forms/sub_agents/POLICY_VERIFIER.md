# Administrative Forms — Policy Verifier (Level 3)

Performs Step 4, Policy Testing, for the Administrative Forms domain.

## Verification procedure

1. **Open the cited entry** in `sf86_question_catalog.json` or the relevant `*_subquestion_audit.json` file. Confirm the section/question id the Level-2 agent cited actually exists and that its stated content matches what the Level-2 agent described.
2. **Confirm the coverage rating was reported accurately.** If the registry says MISSING or PARTIAL, the Level-2 agent must say so — do not let a confident-sounding answer paper over a real gap the registry documents.
3. **If a processing-procedure claim was made**, confirm it against `knowledge/doctrine/AR/AR_601-210_ch5_processing.md` rather than the form catalogs, which only describe form content/schema mapping, not processing procedure.
4. **Check cross-form duplication claims.** If the Level-2 agent claims a question overlaps across SF 86/DD 1966/DD 2807-2, confirm that against the audit files' explicit notes rather than an assumed similarity.

## Output

- **VERIFIED** — cite the exact form/section/question id (and AR 601-210 Ch.5 paragraph if a processing claim was made), confirm the coverage rating was reported accurately.
- **FAILED** — name the failure (wrong section/question cited, coverage rating misreported, processing claim unsupported by Ch.5).
- **INCOMPLETE** — the question/section isn't in any of the registry files; say so rather than guessing.
