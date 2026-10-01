import pytest

from src.domain.entities.show import Show
from src.domain.entities.show_seat import ShowSeat, SeatStatus
from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import SeatAlreadyReservedError


# T3 — BR3: Show Seat Allocation
# BR3: Within one Show, a ShowSeat may be allocated to at most one Reservation.
# A reserved seat cannot be allocated to another reservation.


def _make_show(show_id="S001", seat_numbers=("A10", "A11")):
    seats = [ShowSeat(SeatNumber(s)) for s in seat_numbers]
    return Show(show_id=show_id, start_time=None, seats=seats)


def test_t3_br3_new_show_seats_start_available():
    show = _make_show()
    for seat in show.seats:
        assert seat.status == SeatStatus.AVAILABLE


def test_t3_br3_available_seat_can_be_reserved_once():
    show = _make_show()

    show.reserve_seat(SeatNumber("A10"), "R001")

    reserved = next(s for s in show.seats if s.seat_number == SeatNumber("A10"))
    assert reserved.status == SeatStatus.RESERVED


def test_t3_br3_reserved_seat_cannot_be_reserved_again():
    show = _make_show()

    show.reserve_seat(SeatNumber("A10"), "R001")

    with pytest.raises(SeatAlreadyReservedError):
        show.reserve_seat(SeatNumber("A10"), "R002")

    reserved = next(s for s in show.seats if s.seat_number == SeatNumber("A10"))
    assert reserved.status == SeatStatus.RESERVED


def test_t3_br3_same_seat_in_different_show_is_independent():
    show_one = _make_show(show_id="S001")
    show_two = _make_show(show_id="S002")

    show_one.reserve_seat(SeatNumber("A10"), "R001")
    show_two.reserve_seat(SeatNumber("A10"), "R002")

    seat_one = next(s for s in show_one.seats if s.seat_number == SeatNumber("A10"))
    seat_two = next(s for s in show_two.seats if s.seat_number == SeatNumber("A10"))

    assert seat_one.status == SeatStatus.RESERVED
    assert seat_two.status == SeatStatus.RESERVED


def test_t3_br3_different_seats_in_same_show_can_both_be_reserved():
    show = _make_show(seat_numbers=("A10", "A11"))

    show.reserve_seat(SeatNumber("A10"), "R001")
    show.reserve_seat(SeatNumber("A11"), "R002")

    for seat in show.seats:
        assert seat.status == SeatStatus.RESERVED