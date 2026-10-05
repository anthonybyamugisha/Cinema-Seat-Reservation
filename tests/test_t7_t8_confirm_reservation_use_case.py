from datetime import datetime, timedelta

from src.application.dtos.confirm_reservation_dto import ConfirmReservationInput
from src.application.events.event_dispatcher import EventDispatcher
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


# T7 — Main use case: Confirm a Seat Reservation succeeds.
#      The ReservationConfirmed event is handled and the Show reserves the seat.
# T8 — Aggregate B (Show) rejects the follow-up action (seat already reserved).
#      The use case reports failure and the Reservation stays PENDING.

NOW = datetime(2026, 10, 1, 12, 0, 0)


def _build():
    reservations = InMemoryReservationRepository()
    shows = InMemoryShowRepository()
    shows.save(
        Show(
            show_id="S001",
            start_time=NOW + timedelta(hours=2),
            seats=[ShowSeat(SeatNumber("A10")), ShowSeat(SeatNumber("A11"))],
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


def _seat_status(show, seat_text):
    return next(s for s in show.seats if s.seat_number == SeatNumber(seat_text)).status


def test_t7_confirm_reservation_succeeds_and_show_reserves_seat():
    service, reservations, shows = _build()
    reservations.save(Reservation("R001", "C001", "S001", SeatNumber("A10")))

    output = service.execute(ConfirmReservationInput(reservation_id="R001"))

    assert output.success is True
    assert output.reservation_id == "R001"
    assert output.status == "CONFIRMED"
    assert reservations.get_by_id("R001").status == ReservationStatus.CONFIRMED
    show = shows.get_by_id("S001")
    assert _seat_status(show, "A10") == SeatStatus.RESERVED
    assert _seat_status(show, "A11") == SeatStatus.AVAILABLE


def test_t8_show_rejects_seat_already_reserved_and_reservation_stays_pending():
    service, reservations, shows = _build()
    # Another reservation already holds A10 in this show.
    show = shows.get_by_id("S001")
    show.reserve_seat(SeatNumber("A10"), "R001", "C001")
    shows.save(show)
    reservations.save(Reservation("R002", "C002", "S001", SeatNumber("A10")))

    output = service.execute(ConfirmReservationInput(reservation_id="R002"))

    assert output.success is False
    assert output.status == "PENDING"
    assert output.message != ""
    assert reservations.get_by_id("R002").status == ReservationStatus.PENDING
    assert _seat_status(shows.get_by_id("S001"), "A10") == SeatStatus.RESERVED
    assert _seat_status(shows.get_by_id("S001"), "A11") == SeatStatus.AVAILABLE
