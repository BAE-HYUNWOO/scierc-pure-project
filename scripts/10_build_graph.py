from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import GRAPH_DIR, TABLES_DIR
from src.graph.build_nodes_edges import build_graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", default=str(TABLES_DIR / "merged_triples.csv"))
    parser.add_argument("--nodes_csv", default=str(GRAPH_DIR / "graph_nodes.csv"))
    parser.add_argument("--edges_csv", default=str(GRAPH_DIR / "graph_edges.csv"))
    parser.add_argument("--graph_json", default=str(GRAPH_DIR / "graph_data.json"))
    args = parser.parse_args()

    graph = build_graph(args.input_csv, args.nodes_csv, args.edges_csv, args.graph_json)
    print(f"[OK] nodes={len(graph['nodes'])}, edges={len(graph['edges'])}")
    print(f"[SAVED] {args.graph_json}")


if __name__ == "__main__":
    main()
