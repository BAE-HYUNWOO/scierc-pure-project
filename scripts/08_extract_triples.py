from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import PRETRAINED_RELATION_DIR, TABLES_DIR
from src.postprocess.extract_triples import extract_triples_from_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default=str(PRETRAINED_RELATION_DIR / "predictions.json"))
    parser.add_argument("--output_csv", default=str(TABLES_DIR / "relation_table.csv"))
    parser.add_argument("--mode", choices=["auto", "gold", "predicted"], default="auto")
    args = parser.parse_args()

    rows = extract_triples_from_file(args.input_file, args.output_csv, mode=args.mode)
    print(f"[OK] extracted triples: {len(rows)}")
    print(f"[SAVED] {args.output_csv}")


if __name__ == "__main__":
    main()
