from datetime import datetime, timedelta

import pytest

from src.domain.services.reservation_eligibility_service import (
    ReservationEligibilityService,
)
from src.domain.exceptions.domain_exceptions import ReservationNotEligibleError


# T4 — BR4: Reservation Eligibility
# BR4: A Reservation is eligible for confirmation only when the Show has not
# started AND the customer has fewer than four confirmed seats for that Show.


class FakeReservationRepository:
    """Counts confirmed seats per (customer_id, show_id)."""

    def __init__(self, confirmed_counts=None):
        self._counts = confirmed_counts or {}

    def count_confirmed_seats(self, customer_id, show_id):
        return self._counts.get((customer_id, show_id), 0)


NOW = datetime(2026, 10, 1, 12, 0, 0)


def _service(counts=None):
    return ReservationEligibilityService(FakeReservationRepository(counts))


def test_t4_br4_future_show_with_no_confirmed_seats_is_eligible():
    service = _service()
    service.check_eligibility(
        customer_id="C001",
        show_id="S001",
        show_start_time=NOW + timedelta(hours=1),
        current_time=NOW,
    )


def test_t4_br4_future_show_with_three_confirmed_seats_is_eligible():
    service = _service({("C001", "S001"): 3})
    service.check_eligibility(
        customer_id="C001",
        show_id="S001",
        show_start_time=NOW + timedelta(hours=1),
        current_time=NOW,
    )


def test_t4_br4_future_show_with_four_confirmed_seats_is_rejected():
    service = _service({("C001", "S001"): 4})

    with pytest.raises(ReservationNotEligibleError):
        service.check_eligibility(
            customer_id="C001",
            show_id="S001",
            show_start_time=NOW + timedelta(hours=1),
            current_time=NOW,
        )


def test_t4_br4_past_show_is_rejected():
    service = _service()

    with pytest.raises(ReservationNotEligibleError):
        service.check_eligibility(
            customer_id="C001",
            show_id="S001",
            show_start_time=NOW - timedelta(hours=1),
            current_time=NOW,
        )


def test_t4_br4_show_starting_now_is_rejected():
    service = _service()

    with pytest.raises(ReservationNotEligibleError):
        service.check_eligibility(
            customer_id="C001",
            show_id="S001",
            show_start_time=NOW,
            current_time=NOW,
        )


def test_t4_br4_confirmed_seats_for_other_show_do_not_count():
    service = _service({("C001", "S999"): 4})
    service.check_eligibility(
        customer_id="C001",
        show_id="S001",
        show_start_time=NOW + timedelta(hours=1),
        current_time=NOW,
    )


def test_t4_br4_confirmed_seats_for_other_customer_do_not_count():
    service = _service({("C999", "S001"): 4})
    service.check_eligibility(
        customer_id="C001",
        show_id="S001",
        show_start_time=NOW + timedelta(hours=1),
        current_time=NOW,
    )