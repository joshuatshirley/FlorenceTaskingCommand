# Medical Triage — Agent Flow

How a recruiter's medical-eligibility question moves through the three agent tiers, mapped to the Algorithm of Thoughts framework.

```mermaid
flowchart TD
    Q["Recruiter question\ne.g. \"Applicant took ADHD meds until 10 months ago—qualified?\""] --> R

    subgraph L1["Level 1 — Router"]
        R["Step 1: Information Gathering\nStep 2: Hierarchical Analysis\n→ routes to Medical Triage"]
    end

    R --> D

    subgraph L2["Level 2 — Medical Triage Agent"]
        D["Step 3: Hypothesis Formulation\nLook up condition in dodi_6130_03_seed.json,\napply rule type, draft preliminary finding"]
        C["Step 5: Conclusion\nStep 6: Reflection"]
    end

    D --> V

    subgraph L3["Level 3 — Policy Verifier (sub-agent)"]
        V["Step 4: Policy Testing\nRe-derive rule arithmetic independently\nConfirm citation resolves to the right paragraph\nCheck accession vs. retention framing\nCheck waiver authority"]
    end

    V -->|VERIFIED| C
    V -->|FAILED or INCOMPLETE| E["Escalate: no definitive ruling,\nrecommend MEPS/medical examiner referral"]

    C --> OUT["Final guidance to recruiter,\nwith exact regulation + paragraph citation"]
    E --> OUT2["Guidance to recruiter:\nwhat's unverified + next step"]
```

## Why verification sits between hypothesis and conclusion

The Level-2 agent's Step 3 hypothesis is a draft, not a ruling. It only becomes a Step 5 Conclusion if the Level-3 sub-agent independently re-derives the same result from the doctrine and standards registry. A **FAILED** or **INCOMPLETE** verdict routes to escalation instead of a ruling — the system is built to say "I don't have a grounded answer" rather than let an unverified hypothesis reach a recruiter as definitive guidance.
