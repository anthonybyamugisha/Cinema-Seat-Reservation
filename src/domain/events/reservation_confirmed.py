from dataclasses import dataclass

from src.domain.value_objects.seat_number import SeatNumber


@dataclass(frozen=True)
class ReservationConfirmed:
    """BR5: raised by Reservation (Aggregate A) when it becomes CONFIRMED.

    It asks the Show (Aggregate B) to reserve the SeatNumber. It carries only
    plain data, so the event never holds a reference to another aggregate.
    """

    reservation_id: str
    customer_id: str
    show_id: str
    seat_number: SeatNumber