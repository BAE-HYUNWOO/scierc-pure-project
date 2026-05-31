import sys
from pathlib import Path


def add_project_root_to_sys_path(current_file: str) -> Path:
    root = Path(current_file).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


def require_path(path: str | Path, label: str = "path") -> Path:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path
