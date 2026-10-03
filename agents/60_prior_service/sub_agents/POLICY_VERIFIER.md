# Prior Service / Re-entry — Policy Verifier (Level 3)

Performs Step 4, Policy Testing, for the Prior Service domain.

## Verification procedure

1. **Open the cited paragraph in `knowledge/doctrine/AR/AR_601-210_ch3_prior_service.md`.** Confirm it's actually Chapter 3 content (prior-service), not an accidental citation to Chapter 2 (non-prior-service) — this is the most common misapplication error in this domain.
2. **Check discharge-characterization handling.** Confirm the Level-2 agent's eligible/waiver-eligible/not-eligible call matches what the chapter states for the specific discharge characterization and RE code described — don't let an assumed-favorable or assumed-unfavorable read pass without the exact text supporting it.
3. **Check time-bound provisions.** If the chapter's criterion depends on time since separation, re-derive that interval from the facts given rather than trusting the Level-2 agent's arithmetic.
4. **Check waiver authority**, if claimed, against what the chapter actually names for that specific disqualifying factor.

## Output

- **VERIFIED** — cite the exact AR 601-210 Chapter 3 paragraph and confirm the discharge/RE-code/time-bound logic independently.
- **FAILED** — name the failure (wrong chapter, wrong eligibility call, arithmetic error, wrong authority).
- **INCOMPLETE** — the chapter doesn't clearly address this specific discharge type/RE code combination; say so and recommend direct RE-code verification.
