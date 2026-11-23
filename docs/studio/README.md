# Animation Studio Bootstrap — Phase 1

This is an **additive, opt-in foundation** for the fork. No existing OpenMontage
pipeline, provider adapter, tool registry or main-branch source is modified.

## Files
- skills/meta/studio-executive-producer.md: central governance skill
- skills/meta/studio-continuity-reviewer.md: independent visual/audio QA rules
- docs/studio/AGENTS.md: logical agent responsibility matrix
- schemas/studio/episode_contract.schema.json: pre-generation episode plan
- studio/contracts.py: continuity, voice and frame timing *plan* checks
- studio/quality_gate.py: fail-closed final QA evidence checks
- tests/contracts/test_studio_contracts.py: offline contract tests
- docs/studio/FLOW_INTEGRATION.md: supported browser sign-in handoff

## Test from repository root
Run after installing requirements-dev.txt:

    python -m pytest tests/contracts/test_studio_contracts.py -q

Then run existing OpenMontage tests:

    python -m pytest tests/contracts/ -q
    python -m pytest tests/ -q

Do not run paid generation or set real API keys in public commits.
The existing CI workflow runs on pull_request to main and on pushes to main.

## Important limitations
These validation functions catch contradictions in structured plans, **not**
generated images, vocal timbre, true lip-sync or animated motion. Production
cannot be declared complete until real media is independently checked.
This is not a new orchestrator and does not bypass Rule Zero.
