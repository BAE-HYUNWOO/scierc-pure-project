from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import FIGURES_DIR, GRAPH_DIR, SCIERC_DATA_DIR, TABLES_DIR
from src.graph.build_nodes_edges import build_graph
from src.graph.visualize_pyvis import visualize_graph
from src.postprocess.extract_triples import extract_triples_from_file
from src.postprocess.merge_duplicate_triples import merge_triples


def main() -> None:
    input_file = SCIERC_DATA_DIR / "test.json"
    relation_table = TABLES_DIR / "relation_table_gold_test.csv"
    merged = TABLES_DIR / "merged_triples_gold_test.csv"
    nodes_csv = GRAPH_DIR / "graph_nodes_gold_test.csv"
    edges_csv = GRAPH_DIR / "graph_edges_gold_test.csv"
    graph_json = GRAPH_DIR / "graph_data_gold_test.json"
    html = FIGURES_DIR / "relation_graph_gold_test.html"

    rows = extract_triples_from_file(input_file, relation_table, mode="gold")
    print(f"[1/4] extracted gold triples: {len(rows)}")

    merged_rows = merge_triples(relation_table, merged)
    print(f"[2/4] merged triples: {len(merged_rows)}")

    graph = build_graph(merged, nodes_csv, edges_csv, graph_json)
    print(f"[3/4] graph nodes={len(graph['nodes'])}, edges={len(graph['edges'])}")

    visualize_graph(graph_json, html, title="SciERC Gold Relation Graph")
    print(f"[4/4] saved graph html: {html}")


if __name__ == "__main__":
    main()
