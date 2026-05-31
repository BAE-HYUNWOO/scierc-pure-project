from __future__ import annotations

from typing import Any, Dict, List


def get_entity_field(doc: Dict[str, Any], mode: str = "auto") -> str:
    if mode == "gold":
        return "ner"
    if mode == "predicted":
        return "predicted_ner" if "predicted_ner" in doc else "ner"
    if "predicted_ner" in doc:
        return "predicted_ner"
    return "ner"


def list_entities(doc: Dict[str, Any], mode: str = "auto") -> List[Dict[str, Any]]:
    from src.data.load_scierc import span_to_text

    field = get_entity_field(doc, mode)
    rows = []
    for sent_id, sent_entities in enumerate(doc.get(field, []) or []):
        for ent in sent_entities:
            if len(ent) < 3:
                continue
            s, e, label = int(ent[0]), int(ent[1]), str(ent[2])
            rows.append({
                "doc_key": doc.get("doc_key", ""),
                "sentence_id": sent_id,
                "start": s,
                "end": e,
                "entity_type": label,
                "entity_text": span_to_text(doc, s, e),
            })
    return rows
