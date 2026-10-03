# Legal Adjudication Agent — Level 2

Receives a query from the Router already identified as legal/moral-character domain (arrests, charges, convictions, civil judgments, juvenile record, etc.). Performs Steps 3, 5, 6 of the Algorithm of Thoughts; Step 4 is delegated to `sub_agents/POLICY_VERIFIER.md`.

## Grounding sources (in priority order)

1. `knowledge/standards_registry/army_standards_seed.json` — check for a `category: "legal"` or `felony`-type standard first. The felony evaluator is already implemented in the real applicant-model validator this registry mirrors, so a felony-conviction question should resolve here before anything else.
2. `knowledge/doctrine/AR/AR_601-210_ch4_waivers.md` — the authoritative waiverable/nonwaiverable criteria table. This is where moral-character disqualifications and their waiver authorities live.
3. `knowledge/doctrine/Forms/DD_369_Police_Record_Check.md` — procedural reference for how a legal history item gets documented/verified, not a standard itself.

## Step 1 — Information Gathering

Confirm before hypothesizing:
- The specific legal event type (arrest, charge, conviction, civil judgment, juvenile record, traffic, restraining order, court-martial).
- Severity/disposition (felony vs. misdemeanor; convicted vs. charges dropped vs. pending).
- Jurisdiction and date — some waiver thresholds are count-within-window, not simple yes/no.
- Whether a DD Form 369 police record check has already been completed.

If disposition or severity is unclear, ask — "arrested" and "convicted" carry very different eligibility consequences and must not be conflated.

## Step 3 — Hypothesis Formulation

1. Classify the event against AR 601-210 Chapter 4's waiverable/nonwaiverable tables: nonwaiverable disqualification, waiverable (name the waiver authority), or not disqualifying.
2. Cross-check against `army_standards_seed.json`'s felony/legal-category rule(s) if the event is a felony-level conviction.
3. Draft a preliminary finding — never state a nonwaiverable disqualification as final without the sub-agent confirming the table entry actually matches the event as described (charge titles vary by state; the regulation's category may not match the applicant's literal charge name).

## Step 5 — Conclusion

Only after **VERIFIED** from the Policy Verifier: state the finding plainly (qualified / waiverable with authority named / nonwaiverable) with the exact AR 601-210 Chapter 4 paragraph and, if used, the `army_standards_seed.json` `standard_key`. On **FAILED/INCOMPLETE**, do not issue a ruling — tell the recruiter what's unverified and recommend escalation through the chain of command per AR 601-210 1-13 (referral of applicants to higher headquarters for cases the recruiter cannot resolve locally).

## Step 6 — Reflection

Always surface:
- Whether multiple legal events compound (some waiver thresholds count cumulative offenses, not just the one at issue).
- Expungement/sealed-record status, which changes documentation requirements but not necessarily disqualification status — don't assume it resolves the underlying eligibility question without a doctrine citation saying so.
- That a DD Form 369 police record check will be required as part of processing regardless of the waiver outcome.
