from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str


class PolicyEngine:
    """Side-effect firewall used before any tool execution."""

    WRITE_SIDE_EFFECTS = {"write", "delete", "purchase", "email", "deploy", "exec"}

    def decide(self, requested_action: str, side_effect_level: str) -> PolicyDecision:
        if side_effect_level == "read_only" and requested_action in self.WRITE_SIDE_EFFECTS:
            return PolicyDecision(action="reject", reason="contract is read_only")

        return PolicyDecision(action="allow", reason="within contract limits")
