import logging
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from statistics import mean
from typing import Union

import graphbrain.semsim

logger = logging.getLogger(__name__)


class SemSimModelType(Enum):
    FIXED_EMBEDDING = auto()
    CONTEXT_EMBEDDING = auto()


@dataclass
class SemSimConfig:
    model_type: SemSimModelType
    model_name: str
    similarity_threshold: float


class SemSimMatcher(ABC):
    def __init__(self, config: SemSimConfig):
        self.type: SemSimModelType = config.model_type
        self._base_model_path: Path = self._create_model_dir()
        self._similarity_threshold: float = config.similarity_threshold

    @staticmethod
    def _create_model_dir() -> Path:
        model_dir_path: Path = Path(graphbrain.semsim.semsim.__file__).parent / "models"
        model_dir_path.mkdir(exist_ok=True)
        return model_dir_path

    def similar(
            self,
            candidate: str,
            references: list[str],
            threshold: float = None,
            **kwargs
    ) -> bool:
        logger.debug(f"Candidate string: {candidate} | References: {references} | Threshold: {threshold}")

        if not references:
            logger.error("No reference word(s) given for semantic similarity matching!")
            return False

        similarities: dict[str, float] = self._similarities(candidate, references, **kwargs)
        logger.debug(f"Similarities ('{candidate}'): {similarities}")
        if not similarities:
            return False

        similarity_threshold: float = threshold if threshold is not None else self._similarity_threshold
        if similarity := mean(similarities.values()) < similarity_threshold:
            return False

        logger.debug(f"Similarity is greater than threshold: "
                     f"semsim('{candidate}, {similarities.keys()}) = {similarity:.2f} > {similarity_threshold}")
        return True

    def _similarities(
            self,
            *args,
            **kwargs
    ) -> Union[dict[str, int], None]:
        raise NotImplementedError

    def filter_oov(self, words: list[str]) -> list[str]:
        raise NotImplementedError




