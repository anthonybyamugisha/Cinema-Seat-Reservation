from datetime import datetime

from src.domain.entities.reservation import Reservation
from src.domain.entities.show import Show
from src.domain.exceptions.domain_exceptions import ReservationNotEligibleError


class ReservationEligibilityService:
    """Domain Service for BR4.

    BR4: A Reservation is eligible for confirmation only when the Show has not
    started AND the customer holds fewer than four confirmed seats for that Show.

    It is a Domain Service because the rule spans two aggregates - Reservation
    (Aggregate A) and Show (Aggregate B) - so it cannot live inside either one.
    It is stateless and holds no collaborators, in particular no repository:
    both inputs arrive as aggregates, so the rule is decided entirely inside the
    Domain layer. This is what keeps the dependency direction inward.
    """

    MAX_CONFIRMED_SEATS_PER_SHOW = 4

    def check_eligibility(
        self, reservation: Reservation, show: Show, current_time: datetime
    ) -> None:
        """Raise ReservationNotEligibleError if BR4 rejects the reservation."""
        if current_time >= show.start_time:
            raise ReservationNotEligibleError(
                f"Show {show.show_id} has already started, so reservation "
                f"{reservation.reservation_id} cannot be confirmed."
            )

        held = show.confirmed_seat_count_for(reservation.customer_id)
        if held >= self.MAX_CONFIRMED_SEATS_PER_SHOW:
            raise ReservationNotEligibleError(
                f"Customer {reservation.customer_id} already holds {held} seats for "
                f"show {show.show_id}; the limit is "
                f"{self.MAX_CONFIRMED_SEATS_PER_SHOW}."
            )