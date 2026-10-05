from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Union

from src.domain.entities.show_seat import SeatStatus, ShowSeat
from src.domain.exceptions.domain_exceptions import (
    SeatAlreadyReservedError,
    SeatNotInShowError,
)
from src.domain.value_objects.seat_number import SeatNumber

SeatRef = Union[SeatNumber, str]
MAX_ROWS = 26  # BR1 only allows the row letters A-Z


def _as_seat_number(seat: SeatRef) -> SeatNumber:
    """Accept a SeatNumber or raw text; raw text is validated by BR1."""
    return seat if isinstance(seat, SeatNumber) else SeatNumber(seat)


@dataclass(eq=False)
class Show:
    """
    Aggregate Root for BR3.

    BR3: Within one Show, a ShowSeat may be allocated to at most one Reservation.
    A reserved seat cannot be allocated to another reservation.

    The guard in reserve_seat() is the only place a ShowSeat changes from
    available to reserved, and ShowSeat._reserve() is aggregate-internal, so the
    invariant cannot be bypassed from outside.

    The Show also owns the seat map, so it is the Show - not a repository - that
    answers "how many seats does this customer hold in this show?" for BR4.
    """

    show_id: str
    start_time: datetime
    seats: List[ShowSeat] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        show_id: str,
        start_time: datetime,
        rows: int = 5,
        seats_per_row: int = 10,
    ) -> "Show":
        """Factory.

        Building the whole seat map is a construction rule - every row exists,
        every seat starts AVAILABLE - so it is not left to the caller to
        assemble by hand. Nothing else in the domain needs a Factory: a
        Reservation is fully described by its constructor.
        """
        if not 1 <= rows <= MAX_ROWS:
            raise ValueError(f"A show can have 1 to {MAX_ROWS} rows, got {rows}.")
        if seats_per_row < 1:
            raise ValueError("A row must have at least one seat.")

        seats = [
            ShowSeat(SeatNumber(f"{chr(ord('A') + row_index)}{position}"))
            for row_index in range(rows)
            for position in range(1, seats_per_row + 1)
        ]
        return cls(show_id=show_id, start_time=start_time, seats=seats)

    def seat(self, seat_number: SeatRef) -> ShowSeat:
        """Return one of this show's seats, or reject a seat it does not have."""
        reference = _as_seat_number(seat_number)
        for seat in self.seats:
            if seat.seat_number == reference:
                return seat
        raise SeatNotInShowError(
            f"Seat {reference.value} does not exist in show {self.show_id}."
        )

    def reserve_seat(
        self, seat_number: SeatRef, reservation_id: str, customer_id: str
    ) -> ShowSeat:
        """BR3 lives here. Refuse to overwrite an allocation that already exists."""
        seat = self.seat(seat_number)
        if seat.status == SeatStatus.RESERVED:
            raise SeatAlreadyReservedError(
                f"Seat {seat.seat_number.value} is already reserved for show "
                f"{self.show_id}."
            )
        seat._reserve(reservation_id, customer_id)
        return seat

    def confirmed_seat_count_for(self, customer_id: str) -> int:
        """How many seats this customer already holds in this show (used by BR4)."""
        return sum(
            1
            for seat in self.seats
            if seat.is_reserved and seat.customer_id == customer_id
        )

    @property
    def reserved_seat_count(self) -> int:
        return sum(1 for seat in self.seats if seat.is_reserved)

    @property
    def available_seat_count(self) -> int:
        return len(self.seats) - self.reserved_seat_count

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Show):
            return NotImplemented
        return self.show_id == other.show_id

    def __hash__(self) -> int:
        return hash(self.show_id)

    def __repr__(self) -> str:
        return f"Show({self.show_id}, {self.reserved_seat_count}/{len(self.seats)})"