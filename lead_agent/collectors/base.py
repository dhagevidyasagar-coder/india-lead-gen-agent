from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCollector(ABC):
    """Abstract base class for all lead collectors."""

    @abstractmethod
    def collect(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Collect raw lead data based on a query."""
        pass
