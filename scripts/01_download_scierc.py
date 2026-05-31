from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import tarfile
import urllib.request
from pathlib import Path

from src.config import DATA_DIR
from src.utils.io_utils import ensure_dir

SCIERC_URL = "https://nlp.cs.washington.edu/sciIE/data/sciERC_processed.tar.gz"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=SCIERC_URL)
    parser.add_argument("--output_dir", default=str(DATA_DIR / "scierc"))
    args = parser.parse_args()

    output_dir = ensure_dir(args.output_dir)
    archive_path = output_dir / "sciERC_processed.tar.gz"

    print(f"[DOWNLOAD] {args.url}")
    urllib.request.urlretrieve(args.url, archive_path)
    print(f"[SAVED] {archive_path}")

    print(f"[EXTRACT] {archive_path} -> {output_dir}")
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(output_dir)

    print("[DONE]")
    print(f"Expected data path: {output_dir / 'processed_data' / 'json'}")


if __name__ == "__main__":
    main()
