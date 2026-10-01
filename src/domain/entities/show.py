from dataclasses import dataclass, field
from datetime import datetime

from src.domain.entities.show_seat import ShowSeat, SeatStatus
from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import (
    SeatAlreadyReservedError,
    DomainError,
)


@dataclass
class Show:
    """
    Aggregate Root for BR3.

    BR3: Within one Show, a ShowSeat may be allocated to at most one Reservation.
    A reserved seat cannot be allocated to another reservation.
    """

    show_id: str
    start_time: datetime
    seats: list[ShowSeat] = field(default_factory=list)

    def _find_seat(self, seat_number: SeatNumber) -> ShowSeat:
        for seat in self.seats:
            if seat.seat_number == seat_number:
                return seat
        raise DomainError(
            f"Seat {seat_number.value} does not exist in show {self.show_id}."
        )

    def reserve_seat(self, seat_number: SeatNumber, reservation_id: str) -> None:
        seat = self._find_seat(seat_number)

        if seat.status == SeatStatus.RESERVED:
            raise SeatAlreadyReservedError(
                f"Seat {seat_number.value} is already reserved for show {self.show_id}."
            )

        seat.reserve()