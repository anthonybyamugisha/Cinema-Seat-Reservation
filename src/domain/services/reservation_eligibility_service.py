from datetime import datetime

from src.domain.exceptions.domain_exceptions import ReservationNotEligibleError


class ReservationEligibilityService:
    """
    Domain Service for BR4.

    BR4: A Reservation is eligible for confirmation only when the Show has not
    started AND the customer has fewer than four confirmed seats for that Show.
    """

    MAX_CONFIRMED_SEATS_PER_SHOW = 4

    def __init__(self, reservation_repository):
        self._reservation_repository = reservation_repository

    def check_eligibility(
        self,
        customer_id: str,
        show_id: str,
        show_start_time: datetime,
        current_time: datetime,
    ) -> None:
        if current_time >= show_start_time:
            raise ReservationNotEligibleError("Show has already started.")

        confirmed_seats = self._reservation_repository.count_confirmed_seats(
            customer_id=customer_id,
            show_id=show_id,
        )

        if confirmed_seats >= self.MAX_CONFIRMED_SEATS_PER_SHOW:
            raise ReservationNotEligibleError(
                f"Customer already has {confirmed_seats} confirmed seats for this show."
            )