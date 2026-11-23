# Studio Continuity Reviewer — Independent Hard Gate v0.1

Run in addition to skills/meta/reviewer.md, not as a replacement.

## Before generation
Validate episode contract JSON against schemas/studio/episode_contract.schema.json
and run studio.contracts.validate_episode_contract. Treat all returned issues
as blocking. Compare approved character reference IDs, species, heights,
voice IDs, scene/layout revision and shot timing against the current versioned
project bible. If reference evidence is missing, ask for approval or mark unknown.

## After generation
Review sampled first/middle/last frames **and** frames near every action or
dialogue transition. Compare characters against approved reference sheets for:
- model identity, relative size, limbs/tails, wardrobe and pose
- scene layout, prop positions, floor contacts, lighting continuity
- camera framing/subject orientation and intended direction of motion
- mouth movement belonging only to the active speaker
Verify spoken voice identity by listening and comparison with approved samples.
Verify exact duration and frame count with ffprobe; do not use a loose
25% duration threshold for an exact-frame production.

## Evidence rules
A true check must have independent supporting evidence. Missing render,
reference, samples, playback inspection or approved voice samples means
"unverified" and blocks delivery. Never set checks to true based only on
an agent's written assertion.

## Decision
Use studio.quality_gate.evaluate_quality_gate. Do not accept production if
can_advance is false. On persistent critical defects, stop and request a
creative/technical decision; do not silently substitute providers or stills.
