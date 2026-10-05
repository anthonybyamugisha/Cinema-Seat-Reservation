import copy
from typing import Dict, Optional

from src.application.repositories.show_repository import ShowRepository
from src.domain.entities.show import Show


class InMemoryShowRepository(ShowRepository):
    """Stores Shows (with their ShowSeats) in a dict, keyed by show_id.

    Stores and returns copies, so a rejected change never leaks into the store.
    """

    def __init__(self):
        self._store: Dict[str, Show] = {}

    def get_by_id(self, show_id: str) -> Optional[Show]:
        show = self._store.get(show_id)
        return copy.deepcopy(show) if show is not None else None

    def save(self, show: Show) -> None:
        self._store[show.show_id] = copy.deepcopy(show)
