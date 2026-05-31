from __future__ import annotations

from typing import Any, Dict, List


def get_relation_field(doc: Dict[str, Any], mode: str = "auto") -> str:
    if mode == "gold":
        return "relations"
    if mode == "predicted":
        return "predicted_relations" if "predicted_relations" in doc else "relations"
    if "predicted_relations" in doc:
        return "predicted_relations"
    return "relations"


def relation_confidence(rel: List[Any]) -> str:
    if len(rel) >= 6:
        return rel[5]
    return ""
