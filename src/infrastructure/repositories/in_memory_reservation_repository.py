import copy
from typing import Dict, Optional

from src.application.repositories.reservation_repository import ReservationRepository
from src.domain.entities.reservation import Reservation


class InMemoryReservationRepository(ReservationRepository):
    """Stores Reservations in a dict, keyed by reservation_id.

    It stores and returns copies, like a real database would. A change made to
    a loaded Reservation is therefore not visible until save() is called.
    """

    def __init__(self):
        self._store: Dict[str, Reservation] = {}

    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        reservation = self._store.get(reservation_id)
        return copy.deepcopy(reservation) if reservation is not None else None

    def save(self, reservation: Reservation) -> None:
        self._store[reservation.reservation_id] = copy.deepcopy(reservation)
