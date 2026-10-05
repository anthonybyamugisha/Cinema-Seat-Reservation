from datetime import datetime, timedelta

import pytest

from src.domain.entities.reservation import Reservation
from src.domain.entities.show import Show
from src.domain.entities.show_seat import ShowSeat
from src.domain.exceptions.domain_exceptions import ReservationNotEligibleError
from src.domain.services.reservation_eligibility_service import (
    ReservationEligibilityService,
)
from src.domain.value_objects.seat_number import SeatNumber


# T4 — BR4: Reservation Eligibility
# BR4: A Reservation is eligible for confirmation only when the Show has not
# started AND the customer has fewer than four confirmed seats for that Show.


NOW = datetime(2026, 10, 1, 12, 0, 0)
SOON = NOW + timedelta(hours=1)
PAST = NOW - timedelta(hours=1)


def _reservation(customer_id="C001", seat="A10"):
    return Reservation(
        reservation_id="R001",
        customer_id=customer_id,
        show_id="S001",
        seat_number=SeatNumber(seat),
    )


def _show(show_id="S001", start_time=SOON, seat_numbers=("A1", "A2", "A3", "A4", "A5")):
    return Show(
        show_id=show_id,
        start_time=start_time,
        seats=[ShowSeat(SeatNumber(s)) for s in seat_numbers],
    )


def _hold(show, seat, reservation_id="RX", customer_id="C001"):
    """Make a customer genuinely hold a seat in this show."""
    show.reserve_seat(SeatNumber(seat), reservation_id, customer_id)


def _service():
    # The rule needs no collaborators: both aggregates are passed in per call.
    return ReservationEligibilityService()


def test_t4_br4_future_show_with_no_confirmed_seats_is_eligible():
    _service().check_eligibility(_reservation(), _show(), NOW)


def test_t4_br4_future_show_with_three_confirmed_seats_is_eligible():
    show = _show()
    for seat in ("A1", "A2", "A3"):
        _hold(show, seat)

    _service().check_eligibility(_reservation(), show, NOW)


def test_t4_br4_future_show_with_four_confirmed_seats_is_rejected():
    show = _show()
    for seat in ("A1", "A2", "A3", "A4"):
        _hold(show, seat)

    with pytest.raises(ReservationNotEligibleError):
        _service().check_eligibility(_reservation(), show, NOW)


def test_t4_br4_past_show_is_rejected():
    with pytest.raises(ReservationNotEligibleError):
        _service().check_eligibility(_reservation(), _show(start_time=PAST), NOW)


def test_t4_br4_show_starting_now_is_rejected():
    with pytest.raises(ReservationNotEligibleError):
        _service().check_eligibility(_reservation(), _show(start_time=NOW), NOW)


def test_t4_br4_confirmed_seats_for_other_show_do_not_count():
    # C001 is at the four-seat limit in S002, but the reservation is for S001.
    other_show = _show(show_id="S002")
    for seat in ("A1", "A2", "A3", "A4"):
        _hold(other_show, seat)

    _service().check_eligibility(_reservation(), _show(show_id="S001"), NOW)


def test_t4_br4_confirmed_seats_for_other_customer_do_not_count():
    show = _show()
    for seat in ("A1", "A2", "A3", "A4"):
        _hold(show, seat, customer_id="C999")

    _service().check_eligibility(_reservation(customer_id="C001"), show, NOW)