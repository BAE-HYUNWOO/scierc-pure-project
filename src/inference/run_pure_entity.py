from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from src.config import CONTEXT_WINDOW, MODEL_NAME, PURE_DIR, SCIERC_DATA_DIR, TASK_NAME
from src.utils.io_utils import ensure_dir


def run_entity(
    data_dir: str | Path = SCIERC_DATA_DIR,
    output_dir: str | Path = "models/fine_tuned/entity",
    pure_dir: str | Path = PURE_DIR,
    do_train: bool = False,
    do_eval: bool = True,
    eval_test: bool = False,
    context_window: int = CONTEXT_WINDOW,
    model_name: str = MODEL_NAME,
    learning_rate: str = "1e-5",
    task_learning_rate: str = "5e-4",
    train_batch_size: int = 16,
    extra_args: Optional[List[str]] = None,
) -> subprocess.CompletedProcess:
    pure_dir = Path(pure_dir)
    data_dir = Path(data_dir)
    output_dir = ensure_dir(output_dir)

    if not (pure_dir / "run_entity.py").exists():
        raise FileNotFoundError(f"PURE run_entity.py not found: {pure_dir / 'run_entity.py'}")
    if not data_dir.exists():
        raise FileNotFoundError(f"SciERC data_dir not found: {data_dir}")

    cmd: List[str] = [
        sys.executable,
        "run_entity.py",
        "--context_window",
        str(context_window),
        "--task",
        TASK_NAME,
        "--data_dir",
        str(data_dir.resolve()),
        "--model",
        model_name,
        "--output_dir",
        str(output_dir.resolve()),
    ]

    if do_train:
        cmd.extend([
            "--do_train",
            "--learning_rate",
            str(learning_rate),
            "--task_learning_rate",
            str(task_learning_rate),
            "--train_batch_size",
            str(train_batch_size),
        ])

    if do_eval:
        cmd.append("--do_eval")

    if eval_test:
        cmd.append("--eval_test")

    if extra_args:
        cmd.extend(extra_args)

    print("[PURE ENTITY CMD]", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(pure_dir), check=True)
