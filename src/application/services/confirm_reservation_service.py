from datetime import datetime
from typing import Callable

from src.application.dtos.confirm_reservation_dto import (
    ConfirmReservationInput,
    ConfirmReservationOutput,
)
from src.application.events.event_dispatcher import EventDispatcher
from src.application.exceptions.application_exceptions import (
    ReservationNotFoundError,
    ShowNotFoundError,
)
from src.application.repositories.reservation_repository import ReservationRepository
from src.application.repositories.show_repository import ShowRepository
from src.domain.exceptions.domain_exceptions import DomainError
from src.domain.services.reservation_eligibility_service import (
    ReservationEligibilityService,
)


class ConfirmReservationService:
    """Main use case: Confirm a Seat Reservation.

    It coordinates only. The rules live in the domain:
    BR2 in Reservation.confirm(), BR3 in Show.reserve_seat(),
    BR4 in ReservationEligibilityService. BR6 (lookup) is done here, through
    the repository abstractions that are injected from outside.
    """

    def __init__(
        self,
        reservation_repository: ReservationRepository,
        show_repository: ShowRepository,
        eligibility_service: ReservationEligibilityService,
        event_dispatcher: EventDispatcher,
        clock: Callable[[], datetime] = datetime.now,
    ):
        self._reservations = reservation_repository
        self._shows = show_repository
        self._eligibility = eligibility_service
        self._dispatcher = event_dispatcher
        self._clock = clock

    def execute(self, request: ConfirmReservationInput) -> ConfirmReservationOutput:
        # BR6: the Reservation must already exist before confirmation proceeds.
        reservation = self._reservations.get_by_id(request.reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(
                f"Reservation {request.reservation_id} not found"
            )

        show = self._shows.get_by_id(reservation.show_id)
        if show is None:
            raise ShowNotFoundError(f"Show {reservation.show_id} not found")

        status_before = reservation.status

        try:
            # BR4
            self._eligibility.check_eligibility(
                customer_id=reservation.customer_id,
                show_id=reservation.show_id,
                show_start_time=show.start_time,
                current_time=self._clock(),
            )
            # BR2, records ReservationConfirmed (BR5)
            reservation.confirm()
            # BR5 -> handler -> Show.reserve_seat (BR3)
            self._dispatcher.dispatch(reservation.pull_events())
        except DomainError as error:
            # Any BR2, BR3 or BR4 rejection (ineligible, wrong state, seat taken).
            # Nothing is saved, so the stored Reservation keeps its old status.
            return ConfirmReservationOutput(
                reservation_id=reservation.reservation_id,
                status=status_before.value,
                success=False,
                message=str(error),
            )

        self._reservations.save(reservation)
        return ConfirmReservationOutput(
            reservation_id=reservation.reservation_id,
            status=reservation.status.value,
            success=True,
            message="Reservation confirmed and seat reserved",
        )
