from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SchemaValidationResult:
    ok: bool
    errors: list[str]


class SchemaValidator:
    """Minimal placeholder for contract input/output schema validation."""

    def validate(self, payload: Dict[str, Any], schema_name: str) -> SchemaValidationResult:
        if not isinstance(payload, dict):
            return SchemaValidationResult(ok=False, errors=["payload must be an object"]) 

        if not schema_name:
            return SchemaValidationResult(ok=False, errors=["schema_name must be set"])

        return SchemaValidationResult(ok=True, errors=[])
