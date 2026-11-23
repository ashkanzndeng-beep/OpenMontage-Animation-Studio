"""Animation Studio contract checks; OpenMontage remains the agent orchestrator."""

from .contracts import validate_episode_contract
from .quality_gate import evaluate_quality_gate

__all__ = ["validate_episode_contract", "evaluate_quality_gate"]
