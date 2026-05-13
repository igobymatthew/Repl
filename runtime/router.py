from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml

from runtime.eval_gate import EvalGate
from runtime.policy import PolicyEngine
from runtime.schema_validator import SchemaValidator
from runtime.trace import RuntimeTrace, TraceEmitter


@dataclass
class RouteDecision:
    model: str
    reason: str


class CapabilityRegistry:
    """Maps capability classes to concrete model aliases."""

    def __init__(self) -> None:
        self.mapping = {
            "fast_classifier": ["reasoning_fast", "local_private_fallback"],
            "long_context_reader": ["reasoning_medium", "local_private_fallback"],
            "strict_json_extractor": ["reasoning_medium", "local_private_fallback"],
        }

    def pick(self, capability_class: str, allowed_models: list[str]) -> RouteDecision:
        ranked = self.mapping.get(capability_class, [])
        for candidate in ranked:
            if candidate in allowed_models:
                return RouteDecision(model=candidate, reason=f"matched {capability_class}")

        return RouteDecision(model=allowed_models[0], reason="fallback to contract-allowed model")


class ContractRuntime:
    def __init__(self, contracts_dir: str = "contracts") -> None:
        self.contracts_dir = Path(contracts_dir)
        self.registry = CapabilityRegistry()
        self.schema_validator = SchemaValidator()
        self.policy_engine = PolicyEngine()
        self.eval_gate = EvalGate()
        self.trace_emitter = TraceEmitter()

    def load_contract(self, task_name: str) -> Dict[str, Any]:
        for file in self.contracts_dir.glob("*.yaml"):
            data = yaml.safe_load(file.read_text())
            if data.get("task") == task_name:
                return data
        raise FileNotFoundError(f"No contract found for task={task_name}")

    def run(self, task_name: str, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        contract = self.load_contract(task_name)

        validation = self.schema_validator.validate(input_payload, contract["input_schema"])
        if not validation.ok:
            return {"status": "schema_error", "errors": validation.errors}

        route = self.registry.pick(contract["capability_class"], contract["allowed_models"])
        policy = self.policy_engine.decide("read", contract["side_effects"])
        if policy.action != "allow":
            return {"status": "policy_blocked", "reason": policy.reason}

        eval_outcomes = {}
        for suite in contract.get("eval_suite", []):
            result = self.eval_gate.check(suite, score=0.9)
            eval_outcomes[suite] = result.score
            if not result.passed:
                return {"status": "quality_fail", "suite": suite, "score": result.score}

        trace = RuntimeTrace(
            timestamp="now",
            task=contract["task"],
            contract_version=contract["version"],
            prompt_hash="placeholder_hash",
            model=route.model,
            eval_scores=eval_outcomes,
            policy_decisions=[{"action": policy.action, "reason": policy.reason}],
        )

        return {
            "status": "ok",
            "model": route.model,
            "route_reason": route.reason,
            "trace": self.trace_emitter.emit(trace),
            "output": {"message": "replace with model output"},
        }
