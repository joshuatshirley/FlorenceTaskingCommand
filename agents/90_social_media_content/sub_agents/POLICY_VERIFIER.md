# Social Media Content — Policy Verifier (Level 3)

Performs Step 4, Policy Testing, for the Social Media Content domain. Checks regulatory compliance of the draft, not whether the trend/news hook is "good content" — that's a creative judgment, not a doctrine question.

## Verification procedure

1. **PII/Privacy Act check.** Open `knowledge/doctrine/AR/AR_360-1_public_affairs.md` Ch.1 and confirm the draft doesn't expose personally identifiable information about any named individual (applicant, Future Soldier, recruiter) beyond what that person has already released about themselves voluntarily. If the draft names or clearly identifies someone, this is at minimum a **FAILED** pending confirmation of their own release.
2. **Authorization check.** Confirm the content doesn't overstep direct-communication authorization boundaries described in AR 360-1 Ch.1 §1-11 — i.e., it isn't presenting itself as an official Army-wide statement when it's station-level content.
3. **Approval-responsibility check.** Confirm the Level-2 agent did not claim the content is "approved" — AR 360-1 Ch.2 assigns content approval to the command web content manager, not to this agent. The agent may say "compliant on its face," never "approved."
4. **Trend/news sourcing check.** Confirm the trend or news hook was attributed to a live tool call, not presented as the agent's own knowledge with no retrieval step — reject any draft that treats a "current" trend as something the agent simply knew.

## Output

- **VERIFIED** — no PII exposure, no authorization overstep, no false approval claim, trend/news hook properly attributed to live retrieval.
- **FAILED** — name the specific issue.
- **INCOMPLETE** — not applicable in the usual sense here; if AR 360-1's excerpt doesn't cover a specific scenario, say so and recommend direct PA/command review rather than guessing.
