from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import PRETRAINED_ENTITY_DIR, SCIERC_DATA_DIR
from src.inference.run_pure_entity import run_entity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=str(SCIERC_DATA_DIR))
    parser.add_argument("--output_dir", default=str(PRETRAINED_ENTITY_DIR))
    parser.add_argument("--eval_test", action="store_true")
    parser.add_argument("--context_window", type=int, default=0)
    args = parser.parse_args()

    run_entity(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        do_train=False,
        do_eval=True,
        eval_test=args.eval_test,
        context_window=args.context_window,
    )


if __name__ == "__main__":
    main()
