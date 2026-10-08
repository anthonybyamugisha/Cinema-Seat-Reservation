# Cinema Seat Reservation

This is a group coursework project for Domain-Driven Design, Test-Driven Development and Clean Architecture.

## Domain

Cinema Reserved Seating

## Project Scope

The project focuses on confirming an existing seat reservation and reserving the corresponding seat in a specific cinema show.

## Main Use Case

Confirm a Seat Reservation.

## Connected Follow-Up Use Case

Reserve the corresponding seat in the Show after the Reservation is confirmed.

## Business Rules

BR1 (Value rule) - SeatNumber must contain one row letter from A-Z followed by a seat position from 1-50.

BR2 (Identity/state rule) - A Reservation starts as PENDING and may only transition to CONFIRMED from PENDING.

BR3 (Invariant rule) - Within one Show, a ShowSeat may be allocated to at most one Reservation.

BR4 (Cross-concept rule) - A Reservation is eligible only when the Show has not started and the customer has fewer than four confirmed seats for that Show.

BR5 (Follow-up rule) - When a Reservation is confirmed, a ReservationConfirmed domain event requests the Show to reserve the SeatNumber.

BR6 (Lookup rule) - A Reservation must already exist before confirmation can proceed.

## Where each business rule lives

| Rule | Enforced by |
| --- | --- |
| BR1 | `src/domain/value_objects/seat_number.py` - `SeatNumber` validates in its own constructor |
| BR2 | `src/domain/entities/reservation.py` - `Reservation.confirm()` |
| BR3 | `src/domain/entities/show.py` - `Show.reserve_seat()`; `ShowSeat._reserve()` is aggregate-internal |
| BR4 | `src/domain/services/reservation_eligibility_service.py` - `ReservationEligibilityService.check_eligibility()` |
| BR5 | `src/domain/events/reservation_confirmed.py`, dispatched by `src/application/events/event_dispatcher.py`, handled by `src/application/handlers/reservation_confirmed_handler.py` |
| BR6 | `src/application/services/confirm_reservation_service.py` - the lookup happens before anything else |

## Aggregates

- **Reservation (Aggregate A)** - Aggregate Root. Owns BR2 and raises the BR5 event.
- **Show (Aggregate B)** - Aggregate Root. Owns the seat map and BR3.

They are separate aggregates because they have separate lifecycles and separate invariants, and they are not updated in one atomic step here. They never hold a reference to each other: the only thing that crosses the boundary is the BR5 domain event, which carries plain data only.

## Architecture

The project uses four Clean Architecture layers:

- Domain
- Application
- Infrastructure
- Interface

The Domain layer contains the business rules and domain model.

The Application layer coordinates use cases using DTOs, repositories and application services.

The Infrastructure layer provides in-memory repository implementations.

The Interface layer provides a simple CLI entry point.

`python scripts/check_dependencies.py` verifies that no import points outward from a layer, and fails if one does.

## Design decisions

**Repository interfaces sit in the Application layer.** They are ports used by use cases rather than part of the domain model, so they are declared where they are used and implemented in Infrastructure. The Domain layer depends on neither, and it is given no repository at all: BR4 is decided from the `Reservation` and `Show` aggregates alone, and `Show.confirmed_seat_count_for()` answers "how many seats does this customer hold in this show?" from state the Show already owns.

**Domain Service for BR4.** The rule spans two aggregates, so it cannot live inside either one. `ReservationEligibilityService` is therefore a Domain Service, and it is stateless and holds no collaborators.

**Factory for Show.** `Show.create()` builds the entire seat map, because "every row exists and every seat starts AVAILABLE" is a construction rule rather than something each caller should assemble by hand. No other Factory is needed: a `Reservation` is fully described by its constructor, so a Factory would only add a name for it.

**Layer Supertype for events.** `DomainEvent` is the supertype of every domain event, so the dispatcher and any future subscriber program against the abstraction instead of a growing list of concrete event classes.

**Aggregate-internal mutation.** Only the Aggregate Root changes its own entities: `ShowSeat._reserve()` cannot be reached from outside `Show`, and `Reservation.pull_events()` is the only way to read back the recorded events.

**Explicit identity.** `Show` compares by `show_id` and `ShowSeat` by `seat_number`, because that is what makes them the same object across time - not how many fields happen to match.

## Testing

The project uses pytest.

Install requirements:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest -v
```

`pytest.ini` puts the project root on `sys.path`, so the tests import `src` whether pytest is started as `pytest` or as `python -m pytest`.

## Evidence

`evidence/` holds the recorded pytest output used in the presentation: the RED state from before each rule was implemented, and the final GREEN state.

## AI Usage Statement

The AI tool ChatGPT was used to support brainstorming, code planning, code assistance and code review in this project. The group remained responsible for understanding the design, writing and testing the application, and for reviewing and verifying every AI suggestion before including it.