from datetime import datetime, timedelta

import pytest

from src.application.dtos.confirm_reservation_dto import ConfirmReservationInput
from src.application.events.event_dispatcher import EventDispatcher
from src.application.exceptions.application_exceptions import ReservationNotFoundError
from src.application.handlers.reservation_confirmed_handler import (
    ReservationConfirmedHandler,
)
from src.application.services.confirm_reservation_service import (
    ConfirmReservationService,
)
from src.domain.entities.reservation import Reservation, ReservationStatus
from src.domain.entities.show import Show
from src.domain.entities.show_seat import ShowSeat, SeatStatus
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


# T6 — BR6: Reservation Lookup
# BR6: A Reservation must already exist before confirmation can proceed.
# The Application Service retrieves it through the ReservationRepository.

NOW = datetime(2026, 10, 1, 12, 0, 0)


def _build():
    reservations = InMemoryReservationRepository()
    shows = InMemoryShowRepository()
    shows.save(
        Show(
            show_id="S001",
            start_time=NOW + timedelta(hours=2),
            seats=[ShowSeat(SeatNumber("A10"))],
        )
    )
    dispatcher = EventDispatcher()
    dispatcher.register(ReservationConfirmed, ReservationConfirmedHandler(shows).handle)
    service = ConfirmReservationService(
        reservation_repository=reservations,
        show_repository=shows,
        eligibility_service=ReservationEligibilityService(),
        event_dispatcher=dispatcher,
        clock=lambda: NOW,
    )
    return service, reservations, shows


def test_t6_br6_missing_reservation_is_rejected():
    service, reservations, shows = _build()

    with pytest.raises(ReservationNotFoundError):
        service.execute(ConfirmReservationInput(reservation_id="R404"))

    show = shows.get_by_id("S001")
    assert show.seats[0].status == SeatStatus.AVAILABLE


def test_t6_br6_existing_reservation_is_found_and_confirmation_proceeds():
    service, reservations, shows = _build()
    reservations.save(Reservation("R001", "C001", "S001", SeatNumber("A10")))

    output = service.execute(ConfirmReservationInput(reservation_id="R001"))

    assert output.success is True
    assert reservations.get_by_id("R001").status == ReservationStatus.CONFIRMED


def test_t6_br6_repository_returns_none_for_unknown_id():
    _, reservations, _ = _build()

    assert reservations.get_by_id("R404") is None
