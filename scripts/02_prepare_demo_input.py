from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from pathlib import Path

from src.config import DEMO_INPUT_DIR, PURE_INPUT_DIR
from src.data.convert_abstracts_to_pure import convert_csv_to_docs, convert_txt_to_docs, write_demo_data_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", default="")
    parser.add_argument("--input_txt", default="")
    parser.add_argument("--output_dir", default=str(PURE_INPUT_DIR / "demo_data"))
    args = parser.parse_args()

    if args.input_csv:
        docs = convert_csv_to_docs(args.input_csv)
    elif args.input_txt:
        docs = convert_txt_to_docs(args.input_txt)
    else:
        default_csv = DEMO_INPUT_DIR / "abstracts_sample.csv"
        docs = convert_csv_to_docs(default_csv)

    if not docs:
        raise ValueError("No abstract documents were created. Check input file.")

    write_demo_data_dir(docs, args.output_dir)
    print(f"[OK] Wrote {len(docs)} demo docs to {args.output_dir}")
    print(f"     test file: {Path(args.output_dir) / 'test.json'}")


if __name__ == "__main__":
    main()
