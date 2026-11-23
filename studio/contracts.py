"""Deterministic checks for episodic animation planning artifacts.

These validators do not inspect rendered pixels or audio. They surface planning
contradictions before any paid image/video/TTS operation. Visual and acoustic
checks remain required as separate human/automated review gates.
"""

from __future__ import annotations

from typing import Any, Mapping


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_episode_contract(episode: Mapping[str, Any]) -> list[dict[str, str]]:
    """Return blocking issues (empty list means only the *plan* passed)."""
    issues: list[dict[str, str]] = []

    def fail(code: str, path: str, message: str) -> None:
        issues.append({"severity": "critical", "code": code, "path": path, "message": message})

    for name in ("project_id", "episode_id", "scene_id", "scene_revision", "prop_layout_hash"):
        if not isinstance(episode.get(name), str) or not episode[name].strip():
            fail("missing_lock", name, f"{name} must be a nonempty string")

    if episode.get("aspect_ratio") not in ("9:16", "16:9", "1:1"):
        fail("invalid_aspect_ratio", "aspect_ratio", "Expected 9:16, 16:9, or 1:1")

    fps = episode.get("fps")
    duration = episode.get("duration_seconds")
    valid_time = isinstance(fps, int) and not isinstance(fps, bool) and fps > 0 and _is_number(duration) and duration > 0
    total_frames = round(fps * duration) if valid_time else 0
    if not valid_time or abs(fps * duration - total_frames) > 1e-6:
        fail("invalid_timing", "duration_seconds", "Positive fps and duration must yield an integer frame count")

    characters = episode.get("characters")
    if not isinstance(characters, list) or not characters:
        fail("missing_characters", "characters", "At least one character lock is required")
        characters = []

    by_id: dict[str, Mapping[str, Any]] = {}
    for index, character in enumerate(characters):
        path = f"characters[{index}]"
        if not isinstance(character, dict):
            fail("invalid_character", path, "Character must be an object")
            continue
        cid = character.get("id")
        if not isinstance(cid, str) or not cid:
            fail("missing_character_id", path + ".id", "Character ID is required")
            continue
        if cid in by_id:
            fail("duplicate_character", path + ".id", f"Duplicate character {cid}")
        by_id[cid] = character
        for key in ("species", "reference_id", "voice_id"):
            if not isinstance(character.get(key), str) or not character[key].strip():
                fail("missing_character_lock", path + "." + key, "Missing species, reference, or voice lock")
        height = character.get("relative_height")
        if not _is_number(height) or height <= 0:
            fail("invalid_height", path + ".relative_height", "Relative height must be positive")

    shots = episode.get("shots")
    if not isinstance(shots, list) or not shots:
        fail("missing_shots", "shots", "At least one timed shot is required")
        shots = []

    next_frame = 0
    shot_ids: set[str] = set()
    all_dialogues: list[tuple[int, int, str]] = []
    for i, shot in enumerate(shots):
        path = f"shots[{i}]"
        if not isinstance(shot, dict):
            fail("invalid_shot", path, "Shot must be an object")
            continue
        shot_id = shot.get("id")
        if not isinstance(shot_id, str) or not shot_id:
            fail("missing_shot_id", path + ".id", "Shot ID is required")
        elif shot_id in shot_ids:
            fail("duplicate_shot", path + ".id", f"Duplicate shot {shot_id}")
        else:
            shot_ids.add(shot_id)

        start, end = shot.get("start_frame"), shot.get("end_frame")
        frames_valid = (isinstance(start, int) and not isinstance(start, bool)
                        and isinstance(end, int) and not isinstance(end, bool)
                        and start >= 0 and end > start)
        if not frames_valid:
            fail("invalid_shot_frames", path, "Shot frame range must be [start,end), with end > start")
        else:
            if start != next_frame:
                fail("shot_gap_overlap", path + ".start_frame", f"Expected frame {next_frame}, got {start}")
            next_frame = end

        for lock in ("scene_id", "scene_revision", "prop_layout_hash"):
            if shot.get(lock) != episode.get(lock):
                fail("continuity_lock_mismatch", path + "." + lock, f"{lock} differs from episode lock")

        camera = shot.get("camera")
        if not isinstance(camera, dict) or not all(camera.get(k) for k in ("position", "angle", "movement", "subject_orientation")):
            fail("incomplete_camera", path + ".camera", "Camera position, angle, movement, subject orientation required")

        visible = shot.get("visible_characters", [])
        if not isinstance(visible, list):
            fail("invalid_visible_characters", path + ".visible_characters", "Expected list")
            visible = []
        for j, item in enumerate(visible):
            vpath = f"{path}.visible_characters[{j}]"
            if not isinstance(item, dict):
                fail("invalid_visible_character", vpath, "Expected character object")
                continue
            cid = item.get("character_id")
            if cid not in by_id:
                fail("unknown_visible_character", vpath, f"Unknown character: {cid}")
                continue
            expected = by_id[cid].get("relative_height")
            observed = item.get("relative_height")
            if not (_is_number(observed) and _is_number(expected)) or abs(observed - expected) > 0.005:
                fail("character_scale_mismatch", vpath, f"{cid} does not match locked relative height")

        events = shot.get("speaker_events", [])
        if not isinstance(events, list):
            fail("invalid_speaker_events", path + ".speaker_events", "Expected list")
            events = []
        for j, event in enumerate(events):
            epath = f"{path}.speaker_events[{j}]"
            if not isinstance(event, dict):
                fail("invalid_speaker_event", epath, "Expected speaker event object")
                continue
            cid = event.get("speaker_id")
            if cid not in by_id:
                fail("unknown_speaker", epath, f"Unknown speaker: {cid}")
                continue
            if event.get("voice_id") != by_id[cid].get("voice_id"):
                fail("voice_lock_mismatch", epath + ".voice_id", f"{cid} voice ID differs from lock")
            mouth_ids = event.get("mouth_animation_character_ids")
            if not isinstance(mouth_ids, list) or mouth_ids != [cid]:
                fail("lip_sync_ownership", epath + ".mouth_animation_character_ids",
                     "Only the speaking character may animate its mouth in this event")
            a, b = event.get("start_frame"), event.get("end_frame")
            if not (frames_valid and isinstance(a, int) and not isinstance(a, bool)
                    and isinstance(b, int) and not isinstance(b, bool) and start <= a < b <= end):
                fail("dialogue_timing", epath, "Dialogue must fit within the shot frame interval")
            else:
                all_dialogues.append((a, b, epath))

    if valid_time and shots and next_frame != total_frames:
        fail("duration_mismatch", "shots", f"Shots end at {next_frame}; expected {total_frames} frames")

    all_dialogues.sort()
    for prev, current in zip(all_dialogues, all_dialogues[1:]):
        if current[0] < prev[1]:
            fail("dialogue_overlap", current[2], f"Overlaps dialogue in {prev[2]}")

    return issues
