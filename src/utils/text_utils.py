import re
from typing import List


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_entity(text: str) -> str:
    text = normalize_space(text).lower()
    text = text.replace("-lrb-", "(").replace("-rrb-", ")")
    text = re.sub(r"^[^\w]+|[^\w]+$", "", text)
    return text


def simple_sentence_split(text: str) -> List[str]:
    text = normalize_space(text)
    if not text:
        return []
    # Simple splitter: enough for demo CSV. SciERC official data is already tokenized.
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def simple_tokenize(sentence: str) -> List[str]:
    # Keeps words, numbers, and punctuation as separate tokens.
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*|[^\w\s]", sentence)
