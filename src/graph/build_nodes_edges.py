from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any, Dict, List

from src.utils.io_utils import read_csv_dicts, write_csv_dicts, write_json
from src.utils.text_utils import normalize_entity


NODE_FIELDS = ["id", "label", "entity_type", "support_count", "color"]
EDGE_FIELDS = ["source", "target", "relation", "support_count", "paper_count", "papers", "width", "color", "title"]


ENTITY_COLORS = {
    "Method": "#4C78A8",
    "Task": "#F58518",
    "Metric": "#54A24B",
    "Material": "#B279A2",
    "OtherScientificTerm": "#72B7B2",
    "Generic": "#BAB0AC",
    "": "#9D9D9D",
}

RELATION_COLORS = {
    "USED-FOR": "#4C78A8",
    "FEATURE-OF": "#F58518",
    "HYPONYM-OF": "#54A24B",
    "PART-OF": "#E45756",
    "COMPARE": "#B279A2",
    "CONJUNCTION": "#72B7B2",
    "EVALUATE-FOR": "#FF9DA6",
}


def make_node_id(label: str, entity_type: str = "") -> str:
    key = f"{normalize_entity(label)}::{entity_type}".encode("utf-8")
    return hashlib.md5(key).hexdigest()[:12]


def build_graph(
    input_csv: str | Path,
    nodes_csv: str | Path,
    edges_csv: str | Path,
    graph_json: str | Path,
) -> Dict[str, List[Dict[str, Any]]]:
    rows = read_csv_dicts(input_csv)

    node_map: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, Any]] = []

    for row in rows:
        head = row.get("head_entity", "")
        tail = row.get("tail_entity", "")
        head_type = row.get("head_type", "")
        tail_type = row.get("tail_type", "")
        relation = row.get("relation", "")
        if not head or not tail or not relation:
            continue

        h_id = make_node_id(head, head_type)
        t_id = make_node_id(tail, tail_type)
        support = int(float(row.get("support_count", 1) or 1))
        paper_count = int(float(row.get("paper_count", 1) or 1))

        for node_id, label, etype in [(h_id, head, head_type), (t_id, tail, tail_type)]:
            if node_id not in node_map:
                node_map[node_id] = {
                    "id": node_id,
                    "label": label,
                    "entity_type": etype,
                    "support_count": 0,
                    "color": ENTITY_COLORS.get(etype, ENTITY_COLORS[""]),
                }
            node_map[node_id]["support_count"] += support

        width = 1 + math.log1p(support) * 2
        title = (
            f"{head} --{relation}--> {tail}<br>"
            f"support_count={support}<br>"
            f"paper_count={paper_count}<br>"
            f"papers={row.get('papers', '')}<br>"
            f"example={row.get('example_sentence', '')}"
        )
        edges.append({
            "source": h_id,
            "target": t_id,
            "relation": relation,
            "support_count": support,
            "paper_count": paper_count,
            "papers": row.get("papers", ""),
            "width": round(width, 3),
            "color": RELATION_COLORS.get(relation, "#777777"),
            "title": title,
        })

    nodes = sorted(node_map.values(), key=lambda n: (-int(n["support_count"]), n["label"].lower()))
    edges = sorted(edges, key=lambda e: (-int(e["support_count"]), e["relation"]))

    write_csv_dicts(nodes_csv, nodes, NODE_FIELDS)
    write_csv_dicts(edges_csv, edges, EDGE_FIELDS)
    write_json(graph_json, {"nodes": nodes, "edges": edges})
    return {"nodes": nodes, "edges": edges}
