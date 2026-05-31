from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.utils.io_utils import read_csv_dicts, write_csv_dicts
from src.utils.text_utils import normalize_entity


MERGED_FIELDS = [
    "head_entity",
    "head_type",
    "relation",
    "tail_entity",
    "tail_type",
    "support_count",
    "paper_count",
    "papers",
    "example_sentence",
]


def choose_most_common(values: List[str]) -> str:
    values = [v for v in values if v]
    if not values:
        return ""
    return Counter(values).most_common(1)[0][0]


def merge_triples(input_csv: str | Path, output_csv: str | Path) -> List[Dict[str, Any]]:
    rows = read_csv_dicts(input_csv)
    buckets: Dict[Tuple[str, str, str], List[Dict[str, str]]] = defaultdict(list)

    for row in rows:
        head_norm = normalize_entity(row.get("head_entity", ""))
        tail_norm = normalize_entity(row.get("tail_entity", ""))
        relation = row.get("relation", "").strip()
        if not head_norm or not tail_norm or not relation:
            continue
        buckets[(head_norm, relation, tail_norm)].append(row)

    merged: List[Dict[str, Any]] = []
    for (_head_norm, relation, _tail_norm), group in buckets.items():
        papers = sorted({r.get("paper_id", "") for r in group if r.get("paper_id", "")})
        head_entity = choose_most_common([r.get("head_entity", "") for r in group])
        tail_entity = choose_most_common([r.get("tail_entity", "") for r in group])
        head_type = choose_most_common([r.get("head_type", "") for r in group])
        tail_type = choose_most_common([r.get("tail_type", "") for r in group])
        example_sentence = choose_most_common([r.get("sentence_text", "") for r in group])

        merged.append({
            "head_entity": head_entity,
            "head_type": head_type,
            "relation": relation,
            "tail_entity": tail_entity,
            "tail_type": tail_type,
            "support_count": len(group),
            "paper_count": len(papers),
            "papers": ";".join(papers),
            "example_sentence": example_sentence,
        })

    merged.sort(key=lambda r: (-int(r["support_count"]), r["relation"], r["head_entity"].lower(), r["tail_entity"].lower()))
    write_csv_dicts(output_csv, merged, MERGED_FIELDS)
    return merged
