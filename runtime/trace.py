from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class RuntimeTrace:
    timestamp: str
    task: str
    contract_version: str
    prompt_hash: str
    model: str
    eval_scores: Dict[str, float]
    policy_decisions: list[Dict[str, Any]]


class TraceEmitter:
    """Portable trace emitter. Can be wired into OpenTelemetry exporter."""

    def emit(self, trace: RuntimeTrace) -> Dict[str, Any]:
        payload = asdict(trace)
        payload["emitted_at"] = datetime.now(timezone.utc).isoformat()
        return payload
