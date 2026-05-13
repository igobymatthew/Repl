# Repl

Minimal scaffold for an **AI Contract Runtime** prototype.

## Structure

- `contracts/`: versioned task contracts (typed interface for AI calls)
- `runtime/`: ABI runtime modules (router, policy, eval gate, tracing, schema checks)
- `tools/`: tool manifest + MCP adapter boundary
- `evals/`: golden/adversarial test cases + regression runner stub

## Quick start

```bash
python3 evals/regression_runner.py
```

```python
from runtime.router import ContractRuntime

runtime = ContractRuntime(contracts_dir="contracts")
result = runtime.run(
    task_name="summarize_customer_complaint",
    input_payload={"ticket_id": "T-1001"},
)
print(result)
```
