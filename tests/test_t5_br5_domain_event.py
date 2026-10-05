import pytest

from src.application.events.event_dispatcher import EventDispatcher
from src.application.handlers.reservation_confirmed_handler import (
    ReservationConfirmedHandler,
)
from src.domain.entities.reservation import Reservation
from src.domain.entities.show import Show
from src.domain.entities.show_seat import ShowSeat, SeatStatus
from src.domain.events.domain_event import DomainEvent
from src.domain.events.reservation_confirmed import ReservationConfirmed
from src.domain.exceptions.domain_exceptions import InvalidReservationStateError
from src.domain.value_objects.seat_number import SeatNumber
from src.infrastructure.repositories.in_memory_show_repository import (
    InMemoryShowRepository,
)


# T5 — BR5: ReservationConfirmed Domain Event
# BR5: When a Reservation is confirmed, a ReservationConfirmed domain event
# requests the Show to reserve the SeatNumber.


def _reservation():
    return Reservation(
        reservation_id="R001",
        customer_id="C001",
        show_id="S001",
        seat_number=SeatNumber("A10"),
    )


def _show_repository():
    repository = InMemoryShowRepository()
    repository.save(
        Show(
            show_id="S001",
            start_time=None,
            seats=[ShowSeat(SeatNumber("A10")), ShowSeat(SeatNumber("A11"))],
        )
    )
    return repository


def _seat_status(show, seat_text):
    return next(s for s in show.seats if s.seat_number == SeatNumber(seat_text)).status


def test_t5_br5_confirming_a_reservation_raises_reservation_confirmed():
    reservation = _reservation()

    reservation.confirm()
    events = reservation.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], ReservationConfirmed)
    assert events[0].reservation_id == "R001"
    assert events[0].customer_id == "C001"
    assert events[0].show_id == "S001"
    assert events[0].seat_number == SeatNumber("A10")


def test_t5_br5_event_is_a_domain_event_so_callers_program_against_the_abstraction():
    reservation = _reservation()

    reservation.confirm()

    assert isinstance(reservation.pull_events()[0], DomainEvent)


def test_t5_br5_pulling_events_clears_them():
    reservation = _reservation()
    reservation.confirm()

    reservation.pull_events()

    assert reservation.pull_events() == []


def test_t5_br5_rejected_confirmation_raises_no_second_event():
    reservation = _reservation()
    reservation.confirm()
    reservation.pull_events()

    with pytest.raises(InvalidReservationStateError):
        reservation.confirm()

    assert reservation.pull_events() == []


def test_t5_br5_handler_asks_show_to_reserve_the_seat():
    shows = _show_repository()
    dispatcher = EventDispatcher()
    dispatcher.register(ReservationConfirmed, ReservationConfirmedHandler(shows).handle)
    reservation = _reservation()
    reservation.confirm()

    dispatcher.dispatch(reservation.pull_events())

    show = shows.get_by_id("S001")
    assert _seat_status(show, "A10") == SeatStatus.RESERVED
    assert _seat_status(show, "A11") == SeatStatus.AVAILABLE
