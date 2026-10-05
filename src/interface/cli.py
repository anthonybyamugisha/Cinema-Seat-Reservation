"""Minimal CLI entry point and composition root.

Run:  python -m src.interface.cli R001
This is the only place that knows both the Application and Infrastructure
layers, so it is where the repositories are injected into the service.
"""
import sys
from datetime import datetime, timedelta

from src.application.dtos.confirm_reservation_dto import ConfirmReservationInput
from src.application.events.event_dispatcher import EventDispatcher
from src.application.exceptions.application_exceptions import (
    ReservationNotFoundError,
    ShowNotFoundError,
)
from src.application.handlers.reservation_confirmed_handler import (
    ReservationConfirmedHandler,
)
from src.application.services.confirm_reservation_service import (
    ConfirmReservationService,
)
from src.domain.entities.reservation import Reservation
from src.domain.entities.show import Show
from src.domain.entities.show_seat import ShowSeat
from src.domain.events.reservation_confirmed import ReservationConfirmed
from src.domain.services.reservation_eligibility_service import (
    ReservationEligibilityService,
)
from src.domain.value_objects.seat_number import SeatNumber
from src.infrastructure.repositories.in_memory_reservation_repository import (
    InMemoryReservationRepository,
)
from src.infrastructure.repositories.in_memory_show_repository import (
    InMemoryShowRepository,
)


def build_service():
    reservations = InMemoryReservationRepository()
    shows = InMemoryShowRepository()

    dispatcher = EventDispatcher()
    dispatcher.register(ReservationConfirmed, ReservationConfirmedHandler(shows).handle)

    service = ConfirmReservationService(
        reservation_repository=reservations,
        show_repository=shows,
        eligibility_service=ReservationEligibilityService(reservations),
        event_dispatcher=dispatcher,
    )
    return service, reservations, shows


def seed(reservations, shows):
    shows.save(
        Show(
            show_id="S001",
            start_time=datetime.now() + timedelta(hours=2),
            seats=[ShowSeat(SeatNumber("A10")), ShowSeat(SeatNumber("A11"))],
        )
    )
    reservations.save(Reservation("R001", "C001", "S001", SeatNumber("A10")))


def main(argv):
    if len(argv) != 2:
        print("Usage: python -m src.interface.cli <reservation_id>   (demo data: R001)")
        return 1

    service, reservations, shows = build_service()
    seed(reservations, shows)

    try:
        output = service.execute(ConfirmReservationInput(reservation_id=argv[1]))
    except (ReservationNotFoundError, ShowNotFoundError) as error:
        print(f"Error: {error}")
        return 1

    print(f"{output.reservation_id}: {output.status} - {output.message}")
    return 0 if output.success else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
