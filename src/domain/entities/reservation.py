from enum import Enum
from dataclasses import dataclass, field

from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import InvalidReservationStateError


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"


@dataclass
class Reservation:
    """
    Entity / Aggregate Root for BR2.

    BR2: A Reservation starts in PENDING state and may transition
    to CONFIRMED only from PENDING.
    """

    reservation_id: str
    customer_id: str
    show_id: str
    seat_number: SeatNumber
    status: ReservationStatus = field(default=ReservationStatus.PENDING)

    def confirm(self):
        """
        Confirm the reservation if it is still pending.
        """

        if self.status != ReservationStatus.PENDING:
            raise InvalidReservationStateError(
                "Only a PENDING reservation can be confirmed."
            )

        self.status = ReservationStatus.CONFIRMED