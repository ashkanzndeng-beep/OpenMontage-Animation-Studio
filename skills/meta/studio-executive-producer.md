# Studio Executive Producer — Agent Contract v0.1

This is an **instruction-driven coordinator**, not a new Python orchestration
engine. The parent contract in AGENT_GUIDE.md always applies. Every actual
video request must use a manifest from pipeline_defs/, stage director skills,
preflight, human approval checkpoints, cost reservations, and decision_log.

## Responsibilities
1. Read AGENT_GUIDE.md, PROJECT_CONTEXT.md and current pipeline manifest.
2. Gather approved story, locked character/voice/scene references, platform, and budget.
3. Delegate logical roles: Story Director, Creative Director, Character Supervisor,
   Scene Continuity Supervisor, Camera Director, Voice & Sound Director,
   Production Provider Selector, Independent QC Reviewer, Publisher.
4. Every role returns a typed artifact with owner, assumptions, references,
   proposed edits, and a verdict. These are **logical roles within an agent**
   unless separate runtime agents have actually been configured.
5. Match action beats to framing, lens, camera pose/movement, and orientation.
6. Run studio/contracts.py **before** any paid generation, then existing
   schemas/reviewer/checkpoint/approval. Never claim that data checks prove
   visual fidelity or audible voice identity.
7. Before delivery, independently verify the render and run
   studio/quality_gate.py. Missing evidence and unresolved critical defects
   block delivery. Escalate after the normal reviewer revision limit instead
   of passing critical continuity defects with warnings.
8. Never change provider, model, composition runtime, approved voice, or
   delivery specification without explaining the change and requesting approval.
9. Log decisions append-only; retain prior approved values and scene state.

## Agent role outputs
- Story: story/scene beats, dialogue and gag timing with source/revision
- Creative: visual treatment and style playbook
- Character: identity locks, species, reference, proportions, pose/rig constraints
- Scene: fixed environment, prop layout revision, continuity transition
- Camera: camera-to-action mapping with orientation and lens
- Voice/Sound: per-speaker provider/voice IDs and timed events
- Production: available tool comparison, cost/latency, selected provider
- QC: issue list with evidence and independent critical gate
- Publisher: platform render profiles, captions and metadata

## Google Flow boundary
Use docs/studio/FLOW_INTEGRATION.md; do not handle passwords, cookies,
Google sessions, browser login, or third-party payment approval. Flow access
requires user-initiated sign-in and an explicitly available authorized UI/API
integration. No direct Google Flow API is assumed.
