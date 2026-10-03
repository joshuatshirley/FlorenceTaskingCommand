# Prospecting — Agent Flow

```mermaid
flowchart TD
    Q["Recruiter question\ne.g. \"Best approach for virtual prospecting on a slow week?\""] --> R

    subgraph L1["Level 1 — Router"]
        R["Step 1/2: Identify domain = Prospecting"]
    end

    R --> D

    subgraph L2["Level 2 — Prospecting Agent"]
        D["Step 3: Draft recommendation from\nUM 3-31 Ch.3/4 (channel + scope matched)"]
        C["Step 5: Conclusion\nStep 6: Reflection"]
    end

    D --> V

    subgraph L3["Level 3 — Policy Verifier"]
        V["Step 4: Confirm cited section exists & matches\nchannel and scope; reject any leaked\neligibility/PII content"]
    end

    V -->|VERIFIED| C
    V -->|FAILED or INCOMPLETE| E["Say manual doesn't cover this scenario\nrather than generalizing"]

    C --> OUT["Final guidance with exact UM 3-31\nchapter/heading citation"]
    E --> OUT2["Guidance: what's unverified"]
```

Note: this domain carries no eligibility/waiver logic and no applicant PII — verification here checks technique accuracy against the manual, not a compliance cross-walk.
