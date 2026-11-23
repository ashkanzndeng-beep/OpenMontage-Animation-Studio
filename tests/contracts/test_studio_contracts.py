"""No-network contract tests for studio episode planning and hard QC gate."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from studio.contracts import validate_episode_contract
from studio.quality_gate import REQUIRED_CHECKS, evaluate_quality_gate


def example():
    return {
        "project_id": "studio-demo", "episode_id": "ep-01",
        "fps": 30, "duration_seconds": 10, "aspect_ratio": "16:9",
        "scene_id": "kitchen", "scene_revision": "scene-v1",
        "prop_layout_hash": "layout-v1",
        "characters": [
            {"id": "dog", "species": "dog", "reference_id": "dog-v1",
             "voice_id": "dog-en-v1", "relative_height": 1.0},
            {"id": "fox", "species": "fox", "reference_id": "fox-v1",
             "voice_id": "fox-en-v1", "relative_height": 0.5},
        ],
        "shots": [{
            "id": "shot-01", "start_frame": 0, "end_frame": 300,
            "scene_id": "kitchen", "scene_revision": "scene-v1",
            "prop_layout_hash": "layout-v1",
            "camera": {"position": "front-left", "angle": "eye-level",
                       "movement": "locked", "subject_orientation": "3/4 front", "lens_mm": 35},
            "visible_characters": [
                {"character_id": "dog", "relative_height": 1.0},
                {"character_id": "fox", "relative_height": 0.5},
            ],
            "speaker_events": [{
                "speaker_id": "fox", "voice_id": "fox-en-v1",
                "start_frame": 90, "end_frame": 155,
                "mouth_animation_character_ids": ["fox"],
            }],
        }],
    }


def codes(data):
    return {issue["code"] for issue in validate_episode_contract(data)}


def test_example_passes_and_schema_is_valid():
    e = example()
    path = Path(__file__).resolve().parents[2] / "schemas/studio/episode_contract.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(e)
    assert validate_episode_contract(e) == []


def test_height_lock_is_hard_block():
    e = example()
    e["shots"][0]["visible_characters"][1]["relative_height"] = 0.9
    assert "character_scale_mismatch" in codes(e)


def test_scene_layout_changes_are_hard_block():
    e = example()
    e["shots"][0]["prop_layout_hash"] = "unapproved-change"
    assert "continuity_lock_mismatch" in codes(e)


def test_voice_lock_is_hard_block():
    e = example()
    e["shots"][0]["speaker_events"][0]["voice_id"] = "other-voice"
    assert "voice_lock_mismatch" in codes(e)


def test_only_active_speaker_may_lip_sync():
    e = example()
    e["shots"][0]["speaker_events"][0]["mouth_animation_character_ids"] = ["fox", "dog"]
    assert "lip_sync_ownership" in codes(e)


def test_duration_must_match_frame_count():
    e = example()
    e["shots"][0]["end_frame"] = 280
    assert "duration_mismatch" in codes(e)


def test_missing_camera_is_blocked():
    e = example()
    del e["shots"][0]["camera"]["subject_orientation"]
    assert "incomplete_camera" in codes(e)


def test_overlap_between_dialogues_is_blocked():
    e = example()
    e["shots"][0]["speaker_events"].append({
        "speaker_id": "dog", "voice_id": "dog-en-v1",
        "start_frame": 110, "end_frame": 170,
        "mouth_animation_character_ids": ["dog"],
    })
    assert "dialogue_overlap" in codes(e)


def test_unverified_final_check_fails_closed():
    report = {"checks": {name: True for name in REQUIRED_CHECKS if name != "human_visual_audio_review"}, "findings": []}
    assert evaluate_quality_gate(report)["can_advance"] is False


def test_unresolved_critical_finding_fails_closed():
    report = {"checks": {name: True for name in REQUIRED_CHECKS},
              "findings": [{"severity": "critical", "status": "open", "code": "extra_tail"}]}
    assert evaluate_quality_gate(report)["can_advance"] is False


def test_all_reviewed_without_critical_findings_passes():
    report = {"checks": {name: True for name in REQUIRED_CHECKS},
              "findings": [{"severity": "suggestion", "status": "open"}]}
    assert evaluate_quality_gate(report)["can_advance"] is True
