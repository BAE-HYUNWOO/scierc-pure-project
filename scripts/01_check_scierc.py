from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from pathlib import Path

from src.config import SCIERC_DATA_DIR
from src.data.load_scierc import dataset_stats, load_dataset, validate_doc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=str(SCIERC_DATA_DIR))
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    dataset = load_dataset(data_dir)
    if not dataset:
        raise FileNotFoundError(
            f"No train/dev/test json files found in {data_dir}. "
            "Expected train.json, dev.json, test.json."
        )

    print(f"[DATA DIR] {data_dir}")
    total_errors = 0
    for split, docs in dataset.items():
        stats = dataset_stats(docs)
        print(f"\n[{split.upper()}]")
        print(f"documents: {stats['documents']}")
        print(f"sentences : {stats['sentences']}")
        print(f"entities  : {stats['entities']}")
        print(f"relations : {stats['relations']}")
        print(f"entity types   : {stats['entity_types']}")
        print(f"relation types : {stats['relation_types']}")

        for i, doc in enumerate(docs[:20]):
            errors = validate_doc(doc)
            if errors:
                total_errors += len(errors)
                print(f"[WARN] {split} doc {i} {doc.get('doc_key', '')}: {errors[:3]}")

    if total_errors == 0:
        print("\n[OK] SciERC processed data format looks valid.")
    else:
        print(f"\n[WARN] Found {total_errors} validation warnings in checked docs.")


if __name__ == "__main__":
    main()
