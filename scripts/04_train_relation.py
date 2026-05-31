from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from pathlib import Path

from src.config import FINE_TUNED_ENTITY_DIR, FINE_TUNED_RELATION_DIR, SCIERC_DATA_DIR
from src.inference.run_pure_relation import run_relation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=str(SCIERC_DATA_DIR))
    parser.add_argument("--entity_output_dir", default=str(FINE_TUNED_ENTITY_DIR))
    parser.add_argument("--output_dir", default=str(FINE_TUNED_RELATION_DIR))
    parser.add_argument("--train_file", default="")
    parser.add_argument("--eval_test", action="store_true")
    parser.add_argument("--eval_with_gold", action="store_true")
    parser.add_argument("--context_window", type=int, default=0)
    parser.add_argument("--max_seq_length", type=int, default=128)
    parser.add_argument("--train_batch_size", type=int, default=32)
    parser.add_argument("--eval_batch_size", type=int, default=32)
    parser.add_argument("--learning_rate", default="2e-5")
    parser.add_argument("--num_train_epochs", type=int, default=10)
    parser.add_argument("--use_approx", action="store_true")
    args = parser.parse_args()

    train_file = args.train_file or str(Path(args.data_dir) / "train.json")

    run_relation(
        data_dir=args.data_dir,
        train_file=train_file,
        entity_output_dir=args.entity_output_dir,
        output_dir=args.output_dir,
        do_train=True,
        do_eval=True,
        eval_test=args.eval_test,
        eval_with_gold=args.eval_with_gold,
        context_window=args.context_window,
        max_seq_length=args.max_seq_length,
        train_batch_size=args.train_batch_size,
        eval_batch_size=args.eval_batch_size,
        learning_rate=args.learning_rate,
        num_train_epochs=args.num_train_epochs,
        use_approx=args.use_approx,
    )


if __name__ == "__main__":
    main()
