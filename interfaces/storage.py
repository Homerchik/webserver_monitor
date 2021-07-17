from abc import ABC, abstractmethod
from typing import Dict, List


class Storage(ABC):
    @abstractmethod
    def save(self, payload: Dict) -> None:
        pass

    @abstractmethod
    def prepare(self, tables: List[str]) -> None:
        pass
