"""Non-negotiable final QC gate for studio productions.

This is *validation*, not a Python creative orchestrator. Actual verification
evidence must come from independent video/audio inspection.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_CHECKS = (
    "character_identity",
    "character_proportions",
    "scene_and_props_continuity",
    "movement_orientation",
    "speaker_lip_sync",
    "voice_identity",
    "render_frame_count",
    "human_visual_audio_review",
)


def evaluate_quality_gate(report: Mapping[str, Any]) -> dict[str, Any]:
    checks = report.get("checks", {})
    if not isinstance(checks, dict):
        checks = {}
    missing_or_failed = [name for name in REQUIRED_CHECKS if checks.get(name) is not True]
    findings = report.get("findings", [])
    if not isinstance(findings, list):
        findings = []
        missing_or_failed.append("findings_invalid")
    unresolved = [
        item for item in findings
        if isinstance(item, dict)
        and item.get("severity") == "critical"
        and item.get("status") != "resolved"
    ]
    blocked = bool(missing_or_failed or unresolved)
    return {
        "status": "blocked" if blocked else "pass",
        "failed_or_unverified_checks": missing_or_failed,
        "unresolved_critical_count": len(unresolved),
        "can_advance": not blocked,
    }
