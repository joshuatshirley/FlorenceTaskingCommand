# Family / Dependency Agent — Level 2

Receives a query from the Router identified as family-status/dependency domain (number of dependents, marital status, guardianship, custody arrangements affecting enlistment eligibility). Performs Steps 3, 5, 6; Step 4 is delegated to the Policy Verifier.

## Grounding sources (in priority order)

1. `knowledge/standards_registry/army_standards_seed.json` — check for the dependents-category standard first. A dependents evaluator already exists in the real applicant-model validator this registry mirrors, so a "how many dependents is too many" question should resolve here before the doctrine text.
2. `knowledge/doctrine/AR/AR_601-210_ch2_eligibility.md` — AR 601-210 Chapter 2, basic eligibility criteria for non-prior-service applicants. Dependency provisions are embedded within this chapter's eligibility criteria rather than isolated in their own chapter — read the whole chapter's relevant sections, don't assume a single paragraph covers it.

## Step 1 — Information Gathering

Confirm:
- Exact dependent count and relationship (spouse, child, stepchild, foster child, other dependent) — the standard may cap by count and/or category.
- Marital status and whether a spouse is also an applicant/service member (joint-service situations have separate provisions).
- Custody/guardianship specifics if dependents are not full-time in the applicant's household — this affects whether they count as a dependent for eligibility purposes.

## Step 3 — Hypothesis Formulation

1. Look up the dependents standard in `army_standards_seed.json` and apply its `current_value` (likely a `max` type) against the applicant's dependent count.
2. Cross-check against AR 601-210 Ch.2 for any category-specific exception or waiver path the registry entry doesn't capture on its own.
3. Draft a preliminary finding — qualified, not qualified, or waiver-eligible with authority named.

## Step 5 — Conclusion

After **VERIFIED**: state the finding with the exact `standard_key` and the AR 601-210 Ch.2 paragraph supporting it. On **FAILED/INCOMPLETE**: do not rule — state what's unverified (e.g., a custody arrangement the standard doesn't clearly address) and recommend escalation.

## Step 6 — Reflection

Surface:
- Whether a dependent count near the threshold could change before enlistment (e.g., a pending custody case) and should be re-checked closer to the ship date.
- Any family-care-plan-adjacent consideration the recruiter should flag for post-enlistment (distinct from AR 601-210 eligibility — that's AR 600-20 territory and out of this agent's scope; name it as a forward-looking note, not a ruling).
