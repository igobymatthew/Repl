from __future__ import annotations

import json
from pathlib import Path


def load_jsonl(path: str):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def main() -> None:
    golden = load_jsonl("evals/golden_cases.jsonl")
    adversarial = load_jsonl("evals/adversarial_cases.jsonl")
    print(f"Loaded {len(golden)} golden cases")
    print(f"Loaded {len(adversarial)} adversarial cases")
    print("Stub runner: integrate with ContractRuntime and assert outputs.")


if __name__ == "__main__":
    main()
