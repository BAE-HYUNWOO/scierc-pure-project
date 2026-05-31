from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DEFAULT_DIRS


def main() -> None:
    for d in DEFAULT_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        print(f"[OK] {d}")


if __name__ == "__main__":
    main()
