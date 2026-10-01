from dataclasses import dataclass, field
from enum import Enum

from src.domain.value_objects.seat_number import SeatNumber


class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"


@dataclass
class ShowSeat:
    """
    Entity inside the Show aggregate for BR3.

    BR3: Within one Show, a ShowSeat may be allocated to at most one Reservation.
    """

    seat_number: SeatNumber
    status: SeatStatus = field(default=SeatStatus.AVAILABLE)

    def reserve(self):
        if self.status == SeatStatus.RESERVED:
            return False
        self.status = SeatStatus.RESERVED
        return True