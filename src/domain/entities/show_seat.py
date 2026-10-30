from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from src.domain.value_objects.seat_number import SeatNumber


class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"


@dataclass(eq=False)
class ShowSeat:
    seat_number: SeatNumber
    status: SeatStatus = field(default=SeatStatus.AVAILABLE)
    reservation_id: Optional[str] = None
    customer_id: Optional[str] = None

    @property
    def is_reserved(self) -> bool:
        return self.status == SeatStatus.RESERVED

    def _reserve(self, reservation_id: str, customer_id: str) -> None:
        """Aggregate-internal. Called by Show.reserve_seat() only."""
        self.status = SeatStatus.RESERVED
        self.reservation_id = reservation_id
        self.customer_id = customer_id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ShowSeat):
            return NotImplemented
        return self.seat_number == other.seat_number

    def __hash__(self) -> int:
        return hash(self.seat_number)

    def __repr__(self) -> str:
        holder = self.reservation_id or "free"
        return f"ShowSeat({self.seat_number.value}, {self.status.value}, {holder})"