from datetime import datetime

from src.domain.entities.reservation import Reservation
from src.domain.entities.show import Show
from src.domain.exceptions.domain_exceptions import ReservationNotEligibleError


class ReservationEligibilityService:
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