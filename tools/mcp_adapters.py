from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MCPCall:
    tool: str
    params: Dict[str, Any]


class MCPAdapter:
    """Adapter boundary where runtime-enforced metadata can wrap MCP calls."""

    def invoke(self, call: MCPCall) -> Dict[str, Any]:
        return {
            "tool": call.tool,
            "params": call.params,
            "status": "stubbed",
            "note": "Replace with real MCP transport implementation.",
        }
