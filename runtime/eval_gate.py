from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvalResult:
    suite: str
    passed: bool
    score: float


class EvalGate:
    """Contract-specific eval gate before returning final output."""

    def check(self, suite_name: str, score: float, minimum: float = 0.8) -> EvalResult:
        return EvalResult(suite=suite_name, passed=score >= minimum, score=score)
