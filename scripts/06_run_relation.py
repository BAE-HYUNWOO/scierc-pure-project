from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from src.config import PRETRAINED_ENTITY_DIR, PRETRAINED_RELATION_DIR, SCIERC_DATA_DIR
from src.inference.run_pure_relation import run_relation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=str(SCIERC_DATA_DIR))
    parser.add_argument("--entity_output_dir", default=str(PRETRAINED_ENTITY_DIR))
    parser.add_argument("--output_dir", default=str(PRETRAINED_RELATION_DIR))
    parser.add_argument("--eval_test", action="store_true")
    parser.add_argument("--eval_with_gold", action="store_true")
    parser.add_argument("--context_window", type=int, default=0)
    parser.add_argument("--max_seq_length", type=int, default=128)
    parser.add_argument("--use_approx", action="store_true")
    parser.add_argument("--batch_computation", action="store_true")
    args = parser.parse_args()

    run_relation(
        data_dir=args.data_dir,
        entity_output_dir=args.entity_output_dir,
        output_dir=args.output_dir,
        do_train=False,
        do_eval=True,
        eval_test=args.eval_test,
        eval_with_gold=args.eval_with_gold,
        context_window=args.context_window,
        max_seq_length=args.max_seq_length,
        use_approx=args.use_approx,
        batch_computation=args.batch_computation,
    )


if __name__ == "__main__":
    main()
