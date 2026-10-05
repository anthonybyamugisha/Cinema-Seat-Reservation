from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from src.domain.value_objects.seat_number import SeatNumber


class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"


@dataclass(eq=False)
class ShowSeat:
    """
    Entity inside the Show aggregate for BR3.

    BR3: Within one Show, a ShowSeat may be allocated to at most one Reservation.

    Identity is seat_number. Inside one Show there is exactly one seat with a
    given number, and it is the same seat before and after it is booked, so
    equality compares seat_number rather than every field.

    It also records who holds it (reservation_id, customer_id). That is what lets
    the Show answer BR4's "how many seats does this customer hold here?" without
    leaving its own boundary.

    Only Show may change a ShowSeat, which is why the mutating member is prefixed
    with "_" and the BR3 guard lives in Show.reserve_seat().
    """

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