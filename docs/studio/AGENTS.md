# Animation Studio logical agents (proposal v0.1)

The parent OpenMontage architecture is instruction-driven: these are logical
specialists supervised by the Studio Executive Producer, **not yet separate
running services**.

| Role | Input | Output | Approval |
| --- | --- | --- | --- |
| Studio Brain | brief, pipeline, budget | plan, decision_log, work orders | owner at major changes |
| Story Director | canon, brief | script and gag beats | creative gate |
| Creative Director | references, brief | approved playbook | creative gate |
| Character Supervisor | reference sheets | identity/spec/rig locks | character gate |
| Continuity Supervisor | prior scene, prop state | scene/layout lock | scene gate |
| Camera Director | beat + physical state | camera/action contract | scene gate |
| Voice & Sound | script + voice IDs | dialogue cues and SFX plan | voice sample gate |
| Production Agent | approved assets and vendor menu | render assets/manifest | paid cost gate |
| Independent QC | locked references and actual render | evidence-led QC report | hard quality gate |
| Publisher | final approved render | platform exports and metadata | publish gate |

Recommended rollout: first validate the contracts; next a reference-image
and acoustic verification implementation; then a pilot episode; only then
consider physically separate agents, queues and automated handoffs.
