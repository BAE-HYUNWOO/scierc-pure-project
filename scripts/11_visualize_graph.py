from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import FIGURES_DIR, GRAPH_DIR
from src.graph.visualize_pyvis import visualize_graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph_json", default=str(GRAPH_DIR / "graph_data.json"))
    parser.add_argument("--output_html", default=str(FIGURES_DIR / "relation_graph.html"))
    parser.add_argument("--title", default="Scientific Relation Graph")
    args = parser.parse_args()

    visualize_graph(args.graph_json, args.output_html, title=args.title)
    print(f"[SAVED] {args.output_html}")


if __name__ == "__main__":
    main()
