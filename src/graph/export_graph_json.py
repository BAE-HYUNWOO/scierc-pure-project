from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.graph.build_nodes_edges import build_graph


def export_graph(input_csv: str | Path, nodes_csv: str | Path, edges_csv: str | Path, graph_json: str | Path) -> Dict[str, Any]:
    return build_graph(input_csv=input_csv, nodes_csv=nodes_csv, edges_csv=edges_csv, graph_json=graph_json)
