from src.application.exceptions.application_exceptions import ShowNotFoundError
from src.application.repositories.show_repository import ShowRepository
from src.domain.events.reservation_confirmed import ReservationConfirmed


class ReservationConfirmedHandler:
    """BR5 handler: asks the Show (Aggregate B) to reserve the seat.

    The handler only loads, calls and saves. Whether the seat may be reserved
    is decided by Show.reserve_seat (BR3), which raises
    SeatAlreadyReservedError if it is not.
    """

    def __init__(self, show_repository: ShowRepository):
        self._show_repository = show_repository

    def handle(self, event: ReservationConfirmed) -> None:
        show = self._show_repository.get_by_id(event.show_id)
        if show is None:
            raise ShowNotFoundError(f"Show {event.show_id} not found")

        show.reserve_seat(event.seat_number, event.reservation_id)
        self._show_repository.save(show)
