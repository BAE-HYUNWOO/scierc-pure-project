from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import subprocess
import sys
from pathlib import Path

from src.config import PURE_DIR


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction_file", required=True)
    args = parser.parse_args()

    pure_dir = Path(PURE_DIR)
    prediction_file = Path(args.prediction_file)
    if not (pure_dir / "run_eval.py").exists():
        raise FileNotFoundError(f"PURE run_eval.py not found: {pure_dir / 'run_eval.py'}")
    if not prediction_file.exists():
        raise FileNotFoundError(f"prediction file not found: {prediction_file}")

    cmd = [sys.executable, "run_eval.py", "--prediction_file", str(prediction_file.resolve())]
    print("[PURE EVAL CMD]", " ".join(cmd))
    subprocess.run(cmd, cwd=str(pure_dir), check=True)


if __name__ == "__main__":
    main()
