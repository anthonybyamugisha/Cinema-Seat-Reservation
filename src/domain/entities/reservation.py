from enum import Enum
from dataclasses import dataclass, field

from src.domain.events.reservation_confirmed import ReservationConfirmed
from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import InvalidReservationStateError


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"


@dataclass
class Reservation:
    """
    Entity / Aggregate Root for BR2 (and the source of the BR5 event).

    BR2: A Reservation starts in PENDING state and may transition
    to CONFIRMED only from PENDING.

    BR5: When it is confirmed, the Reservation records a ReservationConfirmed
    domain event. The event is collected with pull_events().
    """

    reservation_id: str
    customer_id: str
    show_id: str
    seat_number: SeatNumber
    status: ReservationStatus = field(default=ReservationStatus.PENDING)
    _events: list = field(default_factory=list, init=False, repr=False, compare=False)

    def confirm(self):
        """
        Confirm the reservation if it is still pending.
        """

        if self.status != ReservationStatus.PENDING:
            raise InvalidReservationStateError(
                "Only a PENDING reservation can be confirmed."
            )

        self.status = ReservationStatus.CONFIRMED
        self._events.append(
            ReservationConfirmed(
                reservation_id=self.reservation_id,
                show_id=self.show_id,
                seat_number=self.seat_number,
            )
        )

    def pull_events(self) -> list:
        """Return the recorded domain events and clear them."""
        events, self._events = self._events, []
        return events
