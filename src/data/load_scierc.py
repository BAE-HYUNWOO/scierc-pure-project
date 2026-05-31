from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from src.utils.io_utils import read_jsonl


Span = Tuple[int, int]


def get_sentence_offsets(doc: Dict[str, Any]) -> List[Tuple[int, int]]:
    """Return inclusive document-level token offsets for each sentence."""
    offsets = []
    cursor = 0
    for sent in doc.get("sentences", []):
        start = cursor
        end = cursor + len(sent) - 1
        offsets.append((start, end))
        cursor = end + 1
    return offsets


def flatten_tokens(doc: Dict[str, Any]) -> List[str]:
    tokens: List[str] = []
    for sent in doc.get("sentences", []):
        tokens.extend(sent)
    return tokens


def span_to_text(doc: Dict[str, Any], start: int, end: int) -> str:
    tokens = flatten_tokens(doc)
    if start < 0 or end >= len(tokens) or start > end:
        return ""
    return " ".join(tokens[start : end + 1])


def span_to_sentence_id(doc: Dict[str, Any], start: int, end: int) -> int:
    for i, (s, e) in enumerate(get_sentence_offsets(doc)):
        if s <= start <= e and s <= end <= e:
            return i
    return -1


def entity_type_map(doc: Dict[str, Any], field: str = "ner") -> Dict[Span, str]:
    out: Dict[Span, str] = {}
    for sent_entities in doc.get(field, []) or []:
        for ent in sent_entities:
            if len(ent) >= 3:
                out[(int(ent[0]), int(ent[1]))] = str(ent[2])
    return out


def validate_doc(doc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ["doc_key", "sentences", "ner", "relations"]
    for key in required:
        if key not in doc:
            errors.append(f"missing key: {key}")

    if "sentences" in doc and not isinstance(doc["sentences"], list):
        errors.append("sentences must be a list")

    total_sents = len(doc.get("sentences", []))
    for key in ["ner", "relations"]:
        if key in doc and len(doc.get(key, [])) != total_sents:
            errors.append(f"{key} length != sentences length")

    token_count = sum(len(s) for s in doc.get("sentences", []))
    for field in ["ner", "predicted_ner"]:
        for sent_idx, sent_entities in enumerate(doc.get(field, []) or []):
            for ent in sent_entities:
                if len(ent) < 3:
                    errors.append(f"{field}[{sent_idx}] invalid entity: {ent}")
                    continue
                s, e = int(ent[0]), int(ent[1])
                if s < 0 or e < s or e >= token_count:
                    errors.append(f"{field}[{sent_idx}] invalid span: {ent}")

    for field in ["relations", "predicted_relations"]:
        for sent_idx, sent_relations in enumerate(doc.get(field, []) or []):
            for rel in sent_relations:
                if len(rel) < 5:
                    errors.append(f"{field}[{sent_idx}] invalid relation: {rel}")
                    continue
                s1, e1, s2, e2 = map(int, rel[:4])
                if min(s1, e1, s2, e2) < 0 or e1 < s1 or e2 < s2:
                    errors.append(f"{field}[{sent_idx}] invalid relation span: {rel}")
                if max(e1, e2) >= token_count:
                    errors.append(f"{field}[{sent_idx}] relation span outside doc: {rel}")

    return errors


def load_dataset(data_dir: str | Path) -> Dict[str, List[Dict[str, Any]]]:
    data_dir = Path(data_dir)
    return {
        split: read_jsonl(data_dir / f"{split}.json")
        for split in ["train", "dev", "test"]
        if (data_dir / f"{split}.json").exists()
    }


def dataset_stats(docs: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    doc_count = 0
    sent_count = 0
    ent_count = 0
    rel_count = 0
    ent_types = Counter()
    rel_types = Counter()

    for doc in docs:
        doc_count += 1
        sent_count += len(doc.get("sentences", []))
        for sent_entities in doc.get("ner", []) or []:
            ent_count += len(sent_entities)
            for ent in sent_entities:
                if len(ent) >= 3:
                    ent_types[str(ent[2])] += 1
        for sent_relations in doc.get("relations", []) or []:
            rel_count += len(sent_relations)
            for rel in sent_relations:
                if len(rel) >= 5:
                    rel_types[str(rel[4])] += 1

    return {
        "documents": doc_count,
        "sentences": sent_count,
        "entities": ent_count,
        "relations": rel_count,
        "entity_types": dict(ent_types),
        "relation_types": dict(rel_types),
    }
