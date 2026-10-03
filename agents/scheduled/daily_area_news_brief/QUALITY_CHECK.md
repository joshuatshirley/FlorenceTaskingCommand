# Daily Area & Army News Brief — Quality Check

Not a "Policy Verifier" in the Level-3 sense used elsewhere in this repo — there's no eligibility/compliance claim to cross-walk here. This is a lightweight pre-publish check the pipeline should run on every generated brief before writing it to `briefings/`.

## Checks

1. **No PII.** Scan for anything resembling a name, SSN-shaped string, date of birth, or address tied to an individual. The brief should contain zero individual-level personal content by construction — if any slipped in, block publication and investigate the source, don't just strip it and continue.
2. **No fabricated-as-fact content.** Every fact in the Army News and Local Area Snapshot sections must trace to a tool call result from that run. If a section says something other than the literal "no live source configured for this run," confirm a tool call actually backs it.
3. **Rotating fact is sourced.** Confirm today's "Local Knowledge Fact" text actually appears (verbatim or as a close paraphrase) in `knowledge/local_reference/florence_area_resource_reference.md` — this section has the same "must trace to a real source" discipline as the other agents' doctrine citations, just against a different reference file.
4. **File hygiene.** Confirm the output path is `briefings/<today's date>.md` and that a file for today doesn't already exist (or, if it does, that this is an intentional re-run, not a silent double-write).

## On failure

Do not publish. A missing brief for one day is a minor, recoverable gap — a published brief containing fabricated news or any PII is not recoverable once distributed.
