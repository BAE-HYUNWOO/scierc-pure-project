from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

from src.utils.io_utils import ensure_dir, read_csv_dicts, write_jsonl
from src.utils.text_utils import simple_sentence_split, simple_tokenize


def make_empty_pure_doc(paper_id: str, abstract: str, title: str = "", source: str = "") -> Dict[str, Any]:
    sentences_text = simple_sentence_split(abstract)
    tokenized = [simple_tokenize(s) for s in sentences_text]
    tokenized = [s for s in tokenized if s]

    return {
        "doc_key": paper_id,
        "sentences": tokenized,
        "ner": [[] for _ in tokenized],
        "relations": [[] for _ in tokenized],
        "clusters": [],
        "metadata": {
            "title": title,
            "source": source,
            "raw_abstract": abstract,
        },
    }


def convert_csv_to_docs(input_csv: str | Path) -> List[Dict[str, Any]]:
    rows = read_csv_dicts(input_csv)
    docs: List[Dict[str, Any]] = []

    for idx, row in enumerate(rows, start=1):
        abstract = row.get("abstract", "") or row.get("Abstract", "")
        if not abstract.strip():
            continue
        paper_id = row.get("paper_id", "") or row.get("doc_key", "") or f"paper_{idx:04d}"
        title = row.get("title", "") or row.get("Title", "")
        source = row.get("source", "")
        docs.append(make_empty_pure_doc(paper_id=paper_id, abstract=abstract, title=title, source=source))

    return docs


def convert_txt_to_docs(input_txt: str | Path, paper_id: str = "demo_abstract") -> List[Dict[str, Any]]:
    text = Path(input_txt).read_text(encoding="utf-8").strip()
    if not text:
        return []
    return [make_empty_pure_doc(paper_id=paper_id, abstract=text)]


def write_demo_data_dir(docs: Iterable[Dict[str, Any]], output_dir: str | Path) -> None:
    """Create PURE-style data_dir containing train/dev/test json files.

    PURE expects a data_dir with train.json/dev.json/test.json. For demo inference,
    we put all documents in test.json and create empty train/dev files.
    """
    output_dir = ensure_dir(output_dir)
    docs = list(docs)
    write_jsonl(output_dir / "train.json", [])
    write_jsonl(output_dir / "dev.json", [])
    write_jsonl(output_dir / "test.json", docs)
