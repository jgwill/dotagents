# relational-routing

Relational Action Routing skill for the MIADI chronicle system.

## When to Invoke

Invoke this skill when processing ceremony recordings, composition transcripts, or routing compositions that need to be connected to their proper chronicle episodes and operational destinations.

Typical triggers:
- A new composition dropped in `~/compositions-nyro/` references other episodes
- Cross-episode lineage needs to be made explicit
- A recording contains action items, unresolved threads, or implementation wishes
- Routing destinations need to be identified and committed

## Expected Inputs

- **Transcript or composition folder** — The source material to route
- **Target episode(s)** — Which chronicle episodes the material relates to
- **Composition metadata** — `composition.json` if available

## Expected Outputs

- **Action lines** — Short operational statements
- **Routing lines** — Where each action routes to (episode, skill, issue, thread)
- **Validation notes** — What remains uncertain
- **Chronicle commits** — New or updated episode content committed+pushed
- **Forgewright registration** — Episode registered in medicine-wheel store
- **Inquiry-weave registration** — Episode registered for discoverability

## Workflow Summary

```
Step 0: Pull-First Law (mandatory git pull --rebase)
Phase 1: Frame (read transcript, composition.json, ASR revision)
Phase 2: Synthesize (identify action-bearing fragments, classify)
Phase 3: Route (map to destinations, present compact output)
Phase 4: Revise (validation loop, remove noise, verify destinations)
Post: Commit -> Register Forgewright -> Register inquiry-weave
```

## Origin

Adapted from the ep097 `relational_action_routing_skill.md` ceremony agent skill, with additions for Pull-First Law, Forgewright registration, inquiry-weave integration, and the 4-phase conversation pattern.
