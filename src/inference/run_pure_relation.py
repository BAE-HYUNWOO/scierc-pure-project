from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from src.config import CONTEXT_WINDOW, MAX_SEQ_LENGTH, MODEL_NAME, PURE_DIR, SCIERC_DATA_DIR, TASK_NAME
from src.utils.io_utils import ensure_dir


def run_relation(
    entity_output_dir: str | Path,
    output_dir: str | Path = "models/fine_tuned/relation",
    pure_dir: str | Path = PURE_DIR,
    data_dir: str | Path = SCIERC_DATA_DIR,
    train_file: str | Path | None = None,
    do_train: bool = False,
    do_eval: bool = True,
    eval_test: bool = False,
    eval_with_gold: bool = False,
    context_window: int = CONTEXT_WINDOW,
    max_seq_length: int = MAX_SEQ_LENGTH,
    model_name: str = MODEL_NAME,
    train_batch_size: int = 32,
    eval_batch_size: int = 32,
    learning_rate: str = "2e-5",
    num_train_epochs: int = 10,
    use_approx: bool = False,
    batch_computation: bool = False,
    extra_args: Optional[List[str]] = None,
) -> subprocess.CompletedProcess:
    pure_dir = Path(pure_dir)
    data_dir = Path(data_dir)
    entity_output_dir = Path(entity_output_dir)
    output_dir = ensure_dir(output_dir)

    run_file = "run_relation_approx.py" if use_approx else "run_relation.py"
    if not (pure_dir / run_file).exists():
        raise FileNotFoundError(f"PURE {run_file} not found: {pure_dir / run_file}")
    if not entity_output_dir.exists():
        raise FileNotFoundError(f"entity_output_dir not found: {entity_output_dir}")

    cmd: List[str] = [
        sys.executable,
        run_file,
        "--task",
        TASK_NAME,
        "--model",
        model_name,
        "--do_lower_case",
        "--context_window",
        str(context_window),
        "--max_seq_length",
        str(max_seq_length),
        "--entity_output_dir",
        str(entity_output_dir.resolve()),
        "--output_dir",
        str(output_dir.resolve()),
    ]

    if data_dir.exists():
        cmd.extend(["--data_dir", str(data_dir.resolve())])

    if do_train:
        cmd.extend([
            "--do_train",
            "--train_batch_size",
            str(train_batch_size),
            "--eval_batch_size",
            str(eval_batch_size),
            "--learning_rate",
            str(learning_rate),
            "--num_train_epochs",
            str(num_train_epochs),
        ])
        if train_file is not None:
            cmd.extend(["--train_file", str(Path(train_file).resolve())])

    if do_eval:
        cmd.append("--do_eval")

    if eval_test:
        cmd.append("--eval_test")

    if eval_with_gold:
        cmd.append("--eval_with_gold")

    if use_approx and batch_computation:
        cmd.append("--batch_computation")

    if extra_args:
        cmd.extend(extra_args)

    print("[PURE RELATION CMD]", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(pure_dir), check=True)
