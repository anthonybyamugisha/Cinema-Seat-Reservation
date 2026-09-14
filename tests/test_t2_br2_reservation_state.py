import pytest

from src.domain.entities.reservation import Reservation, ReservationStatus
from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import InvalidReservationStateError


# T2 — BR2: Reservation State Transition
# BR2: A Reservation starts in PENDING state and may transition to CONFIRMED
# only from PENDING.


def test_t2_br2_reservation_starts_in_pending_state():
    reservation = Reservation(
        reservation_id="R001",
        customer_id="C001",
        show_id="S001",
        seat_number=SeatNumber("A10"),
    )

    assert reservation.status == ReservationStatus.PENDING


def test_t2_br2_pending_reservation_can_be_confirmed():
    reservation = Reservation(
        reservation_id="R001",
        customer_id="C001",
        show_id="S001",
        seat_number=SeatNumber("A10"),
    )

    reservation.confirm()

    assert reservation.status == ReservationStatus.CONFIRMED


def test_t2_br2_confirmed_reservation_cannot_be_confirmed_again():
    reservation = Reservation(
        reservation_id="R001",
        customer_id="C001",
        show_id="S001",
        seat_number=SeatNumber("A10"),
    )

    reservation.confirm()

    with pytest.raises(InvalidReservationStateError):
        reservation.confirm()

    assert reservation.status == ReservationStatus.CONFIRMED