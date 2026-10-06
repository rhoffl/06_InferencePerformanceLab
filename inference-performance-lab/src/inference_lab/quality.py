import json, re

def score(task: str, output: str, reference: object | None) -> float:
    if reference is None:
        return 1.0 if output.strip() else 0.0
    if task == "structured_extraction":
        try:
            parsed = json.loads(re.search(r"\{.*\}", output, re.S).group())
            expected = reference if isinstance(reference, dict) else {}
            return sum(parsed.get(k) == v for k, v in expected.items()) / max(1, len(expected))
        except (ValueError, AttributeError, json.JSONDecodeError):
            return 0.0
    expected = str(reference).lower().strip()
    actual = output.lower()
    return 1.0 if expected in actual else 0.0

