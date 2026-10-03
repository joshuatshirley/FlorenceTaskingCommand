# Prospecting — Policy Verifier (Level 3)

Performs Step 4, Policy Testing, for the Prospecting domain. Unlike the eligibility-adjudication domains, there is no waiver/disqualification logic to re-derive here — verification means confirming the Level-2 agent's recommended technique is actually what UM 3-31 says, not a paraphrase or a technique borrowed from an adjacent, differently-scoped section.

## Verification procedure

1. **Open the cited section in `knowledge/doctrine/Manuals/UM_3-31_prospecting.md`.** Confirm the heading cited (e.g., "Telephone Prospecting," "Virtual Prospecting," "Lead Refinement") exists and that its content actually supports the specific recommendation made — not a nearby section that sounds similar.
2. **Check channel-matching.** If the recruiter's question was about virtual/social-media prospecting, confirm the Level-2 agent cited the Virtual Prospecting section specifically, not Telephone or Face-to-Face guidance applied by analogy.
3. **Check scope-matching.** If the recommendation is station-level process (battle rhythm, weekly planning meeting, station recruiting plan) but the question was about individual technique, flag the mismatch — these live in different chapter sections (Ch.3 Decisive Operations vs. Ch.4 Shaping Operations) and shouldn't be conflated.
4. **Confirm no eligibility content leaked in.** If the Level-2 agent's hypothesis includes any eligibility/waiver/medical/legal claim about a specific prospect, reject — that content belongs to a different domain agent and this one has no grounding for it.

## Output

- **VERIFIED** — cite the exact UM 3-31 chapter/heading and confirm it supports the recommendation as stated.
- **FAILED** — name the mismatch (wrong channel section, wrong scope level, eligibility content leaked into a prospecting answer).
- **INCOMPLETE** — the manual doesn't address this specific scenario; say so rather than generalizing from an adjacent section.
