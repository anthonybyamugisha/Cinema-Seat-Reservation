import pytest

from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import InvalidSeatNumberError


# T1 — BR1: SeatNumber Validation
# BR1: A SeatNumber is valid only when it contains one row letter from A-Z
# followed by a seat position from 1-50.


def test_t1_br1_accepts_valid_seat_numbers():
    seat_one = SeatNumber("A1")
    seat_two = SeatNumber("B12")
    seat_three = SeatNumber("Z50")

    assert seat_one.value == "A1"
    assert seat_two.value == "B12"
    assert seat_three.value == "Z50"


def test_t1_br1_accepts_boundary_seat_numbers():
    first_valid_seat = SeatNumber("A1")
    last_valid_seat = SeatNumber("Z50")

    assert first_valid_seat.value == "A1"
    assert last_valid_seat.value == "Z50"


def test_t1_br1_rejects_invalid_seat_numbers():
    invalid_seats = [
        "",
        "A",
        "10A",
        "A0",
        "A51",
        "AA10",
        "1",
        "Z99",
        "a10",
    ]

    for seat in invalid_seats:
        with pytest.raises(InvalidSeatNumberError):
            SeatNumber(seat)