
import pytest

from src.domain.value_objects.seat_number import SeatNumber
from src.domain.exceptions.domain_exceptions import InvalidSeatNumberError


# T1 — BR1: SeatNumber Validation
# BR1: A SeatNumber is valid only when it contains one row letter from A-Z
# followed by a seat position from 1-50.


def test_t1_br1_accepts_valid_seat_numbers():
    valid_seats = ["A1", "B12", "Z50"]

    for seat in valid_seats:
        seat_number = SeatNumber(seat)
        assert seat_number.value == seat


def test_t1_br1_accepts_boundary_seat_numbers():
    boundary_seats = ["A1", "Z50"]

    for seat in boundary_seats:
        seat_number = SeatNumber(seat)
        assert seat_number.value == seat


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