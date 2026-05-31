from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import TABLES_DIR
from src.postprocess.merge_duplicate_triples import merge_triples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", default=str(TABLES_DIR / "relation_table.csv"))
    parser.add_argument("--output_csv", default=str(TABLES_DIR / "merged_triples.csv"))
    args = parser.parse_args()

    rows = merge_triples(args.input_csv, args.output_csv)
    print(f"[OK] merged triples: {len(rows)}")
    print(f"[SAVED] {args.output_csv}")


if __name__ == "__main__":
    main()
