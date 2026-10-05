from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.show import Show


class ShowRepository(ABC):
    """Repository abstraction for the Show aggregate root."""

    @abstractmethod
    def get_by_id(self, show_id: str) -> Optional[Show]:
        """Return the Show, or None if it does not exist."""

    @abstractmethod
    def save(self, show: Show) -> None:
        """Store a new Show or replace an existing one."""
