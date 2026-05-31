from __future__ import annotations

from pathlib import Path

from src.data.convert_abstracts_to_pure import convert_csv_to_docs, write_demo_data_dir
from src.inference.run_pure_entity import run_entity
from src.inference.run_pure_relation import run_relation


def predict_abstract_csv(
    input_csv: str | Path,
    demo_data_dir: str | Path,
    entity_output_dir: str | Path,
    relation_output_dir: str | Path,
) -> None:
    """Prepare demo data and run PURE entity+relation.

    Note: PURE's official scripts are evaluation-oriented. Custom abstracts do not
    have gold labels, so first verify the pipeline on SciERC test set.
    """
    docs = convert_csv_to_docs(input_csv)
    write_demo_data_dir(docs, demo_data_dir)

    run_entity(data_dir=demo_data_dir, output_dir=entity_output_dir, do_train=False, do_eval=True, eval_test=True)
    run_relation(
        data_dir=demo_data_dir,
        entity_output_dir=entity_output_dir,
        output_dir=relation_output_dir,
        do_train=False,
        do_eval=True,
        eval_test=True,
    )
