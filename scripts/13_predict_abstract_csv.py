from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import PRETRAINED_ENTITY_DIR, PRETRAINED_RELATION_DIR, PURE_INPUT_DIR
from src.inference.predict_abstracts import predict_abstract_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--demo_data_dir", default=str(PURE_INPUT_DIR / "demo_data"))
    parser.add_argument("--entity_output_dir", default=str(PRETRAINED_ENTITY_DIR))
    parser.add_argument("--relation_output_dir", default=str(PRETRAINED_RELATION_DIR))
    args = parser.parse_args()

    predict_abstract_csv(
        input_csv=args.input_csv,
        demo_data_dir=args.demo_data_dir,
        entity_output_dir=args.entity_output_dir,
        relation_output_dir=args.relation_output_dir,
    )


if __name__ == "__main__":
    main()
