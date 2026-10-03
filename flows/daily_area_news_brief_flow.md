# Daily Area & Army News Brief — Pipeline Flow

Not a Router → Agent → Verifier flow — this is a cron-triggered Collect → Compose → Publish pipeline, modeled on the proven `sc_morning_brief.py` pattern.

```mermaid
flowchart TD
    T["Daily cron trigger"] --> C1
    subgraph Collect["Collect (script, no LLM)"]
        C1["Army news — live tool\nor 'no live source configured'"]
        C2["Local weather/events — live tool\nor 'no live source configured'"]
        C3["Rotating fact from\nflorence_area_resource_reference.md"]
    end
    C1 --> X
    C2 --> X
    C3 --> X
    X["Compose: fill TEMPLATE.md\n(LLM pass, if used, may only rephrase\n— never add unsourced content)"] --> QC
    QC["Quality Check:\nno PII, no fabricated content,\nfact traces to source, file hygiene"]
    QC -->|pass| PUB["Publish: briefings/<date>.md"]
    QC -->|fail| BLOCK["Do not publish —\ninvestigate before next run"]
```
