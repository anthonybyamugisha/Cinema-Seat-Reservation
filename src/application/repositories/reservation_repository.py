from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.reservation import Reservation


class ReservationRepository(ABC):
    """Repository abstraction for the Reservation aggregate root (BR6)."""

    @abstractmethod
    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """Return the Reservation, or None if it does not exist."""

    @abstractmethod
    def save(self, reservation: Reservation) -> None:
        """Store a new Reservation or replace an existing one."""
