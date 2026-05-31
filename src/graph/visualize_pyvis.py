from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict

from src.utils.io_utils import ensure_dir


def make_vis_html(graph_data: Dict[str, Any], title: str = "Scientific Relation Graph") -> str:
    nodes = []
    for n in graph_data.get("nodes", []):
        nodes.append({
            "id": n["id"],
            "label": n["label"],
            "title": f"{html.escape(n.get('label', ''))}<br>type={html.escape(n.get('entity_type', ''))}<br>support={n.get('support_count', 0)}",
            "color": n.get("color", "#9D9D9D"),
            "value": max(1, int(float(n.get("support_count", 1) or 1))),
        })

    edges = []
    for e in graph_data.get("edges", []):
        edges.append({
            "from": e["source"],
            "to": e["target"],
            "label": f"{e.get('relation', '')} ({e.get('support_count', 1)})",
            "title": e.get("title", ""),
            "width": float(e.get("width", 1) or 1),
            "color": {"color": e.get("color", "#777777")},
            "arrows": "to",
        })

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; }}
    #header {{ padding: 14px 18px; border-bottom: 1px solid #ddd; }}
    #graph {{ width: 100vw; height: calc(100vh - 64px); }}
    .note {{ color: #555; font-size: 13px; }}
  </style>
</head>
<body>
  <div id="header">
    <b>{html.escape(title)}</b>
    <span class="note"> | edge thickness = support_count, node color = entity type, edge color = relation type</span>
  </div>
  <div id="graph"></div>
  <script>
    const nodes = new vis.DataSet({nodes_json});
    const edges = new vis.DataSet({edges_json});
    const container = document.getElementById("graph");
    const data = {{ nodes, edges }};
    const options = {{
      nodes: {{
        shape: "dot",
        scaling: {{ min: 8, max: 34 }},
        font: {{ size: 14, face: "Arial" }}
      }},
      edges: {{
        smooth: {{ type: "dynamic" }},
        font: {{ size: 10, align: "middle" }}
      }},
      physics: {{
        stabilization: true,
        barnesHut: {{
          gravitationalConstant: -24000,
          springLength: 140,
          springConstant: 0.04
        }}
      }},
      interaction: {{
        hover: true,
        tooltipDelay: 120
      }}
    }};
    new vis.Network(container, data, options);
  </script>
</body>
</html>"""


def visualize_graph(graph_json: str | Path, output_html: str | Path, title: str = "Scientific Relation Graph") -> None:
    graph_json = Path(graph_json)
    output_html = Path(output_html)
    ensure_dir(output_html.parent)

    graph_data = json.loads(graph_json.read_text(encoding="utf-8"))
    output_html.write_text(make_vis_html(graph_data, title=title), encoding="utf-8")
