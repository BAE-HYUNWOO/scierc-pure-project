from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

from src.data.load_scierc import entity_type_map, span_to_text
from src.postprocess.parse_entity_predictions import get_entity_field
from src.postprocess.parse_relation_predictions import get_relation_field, relation_confidence
from src.utils.io_utils import read_jsonl, write_csv_dicts


TRIPLE_FIELDS = [
    "paper_id",
    "sentence_id",
    "sentence_text",
    "head_start",
    "head_end",
    "head_entity",
    "head_type",
    "relation",
    "tail_start",
    "tail_end",
    "tail_entity",
    "tail_type",
    "confidence",
]


def sentence_text(doc: Dict[str, Any], sentence_id: int) -> str:
    sents = doc.get("sentences", [])
    if 0 <= sentence_id < len(sents):
        return " ".join(sents[sentence_id])
    return ""


def extract_doc_triples(doc: Dict[str, Any], mode: str = "auto") -> List[Dict[str, Any]]:
    entity_field = get_entity_field(doc, mode)
    relation_field = get_relation_field(doc, mode)
    ent_map = entity_type_map(doc, entity_field)

    rows: List[Dict[str, Any]] = []
    paper_id = doc.get("doc_key", "")

    for sent_id, sent_relations in enumerate(doc.get(relation_field, []) or []):
        for rel in sent_relations:
            if len(rel) < 5:
                continue

            h_start, h_end, t_start, t_end = map(int, rel[:4])
            label = str(rel[4])

            head_text = span_to_text(doc, h_start, h_end)
            tail_text = span_to_text(doc, t_start, t_end)
            head_type = ent_map.get((h_start, h_end), "")
            tail_type = ent_map.get((t_start, t_end), "")

            rows.append({
                "paper_id": paper_id,
                "sentence_id": sent_id,
                "sentence_text": sentence_text(doc, sent_id),
                "head_start": h_start,
                "head_end": h_end,
                "head_entity": head_text,
                "head_type": head_type,
                "relation": label,
                "tail_start": t_start,
                "tail_end": t_end,
                "tail_entity": tail_text,
                "tail_type": tail_type,
                "confidence": relation_confidence(rel),
            })

    return rows


def extract_triples_from_file(input_file: str | Path, output_csv: str | Path, mode: str = "auto") -> List[Dict[str, Any]]:
    docs = read_jsonl(input_file)
    rows: List[Dict[str, Any]] = []
    for doc in docs:
        rows.extend(extract_doc_triples(doc, mode=mode))
    write_csv_dicts(output_csv, rows, TRIPLE_FIELDS)
    return rows
