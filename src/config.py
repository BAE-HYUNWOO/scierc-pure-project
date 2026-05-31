from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXTERNAL_DIR = PROJECT_ROOT / "external"
PURE_DIR = EXTERNAL_DIR / "PURE"

DATA_DIR = PROJECT_ROOT / "data"
SCIERC_DATA_DIR = DATA_DIR / "scierc" / "processed_data" / "json"
DEMO_INPUT_DIR = DATA_DIR / "demo_inputs"
PROCESSED_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"
FINE_TUNED_ENTITY_DIR = MODELS_DIR / "fine_tuned" / "entity"
FINE_TUNED_RELATION_DIR = MODELS_DIR / "fine_tuned" / "relation"
PRETRAINED_ENTITY_DIR = MODELS_DIR / "scierc_ent_model" / "ent-scib-ctx0"
PRETRAINED_RELATION_DIR = MODELS_DIR / "scierc_rel_model" / "rel-scib-ctx0"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = OUTPUTS_DIR / "logs"
EVAL_DIR = OUTPUTS_DIR / "eval"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"

GRAPH_DIR = PROCESSED_DIR / "graph"
PURE_INPUT_DIR = PROCESSED_DIR / "pure_input"
PREDICTIONS_DIR = PROCESSED_DIR / "predictions"

TASK_NAME = "scierc"
MODEL_NAME = "allenai/scibert_scivocab_uncased"
CONTEXT_WINDOW = 0
MAX_SEQ_LENGTH = 128

ENTITY_TYPES = [
    "Method",
    "Task",
    "Metric",
    "Material",
    "OtherScientificTerm",
    "Generic",
]

RELATION_TYPES = [
    "USED-FOR",
    "FEATURE-OF",
    "HYPONYM-OF",
    "PART-OF",
    "COMPARE",
    "CONJUNCTION",
    "EVALUATE-FOR",
]

DEFAULT_DIRS = [
    EXTERNAL_DIR,
    SCIERC_DATA_DIR,
    DEMO_INPUT_DIR,
    PROCESSED_DIR,
    PURE_INPUT_DIR,
    PREDICTIONS_DIR,
    GRAPH_DIR,
    MODELS_DIR,
    FINE_TUNED_ENTITY_DIR,
    FINE_TUNED_RELATION_DIR,
    OUTPUTS_DIR,
    LOGS_DIR,
    EVAL_DIR,
    TABLES_DIR,
    FIGURES_DIR,
]
