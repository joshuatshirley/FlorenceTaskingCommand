# Family / Dependency — Policy Verifier (Level 3)

Performs Step 4, Policy Testing, for the Family/Dependency domain.

## Verification procedure

1. **Open the cited `standard_key` in `army_standards_seed.json`.** Confirm it exists, its category is dependents-related, and re-derive the comparison yourself (dependent count vs. the standard's `max` value) rather than trusting the Level-2 agent's arithmetic.
2. **Open `knowledge/doctrine/AR/AR_601-210_ch2_eligibility.md`** and confirm the cited paragraph actually discusses dependents in the way the Level-2 agent applied it — this chapter covers many eligibility topics, so confirm the specific paragraph, not just the chapter.
3. **Check dependent classification.** Confirm the Level-2 agent correctly classified each person as counting or not counting toward the dependents total per the regulation's definition (e.g., shared-custody children may count differently than full-time dependents) — don't let an assumed classification pass unchallenged.
4. **Check for waiver path.** If the hypothesis claims no waiver exists for exceeding the dependent threshold, confirm that's actually what the regulation says rather than an absence-of-evidence assumption.

## Output

- **VERIFIED** — cite the `standard_key` and AR 601-210 Ch.2 paragraph, confirm the dependent-count arithmetic and classification independently.
- **FAILED** — name the failure (miscounted dependents, wrong classification, unsupported waiver claim).
- **INCOMPLETE** — the standard/doctrine doesn't clearly address this specific custody/guardianship scenario; say so.
