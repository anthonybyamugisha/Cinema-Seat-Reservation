# Integration notes (BR5, BR6, Clean Architecture)

## 1. One existing file is replaced: `src/domain/entities/reservation.py`

BR5 needs the aggregate itself to record the event, so `Reservation` now:
- has a hidden `_events` list (`init=False, repr=False, compare=False`, so its constructor and equality are unchanged),
- appends a `ReservationConfirmed` event at the end of `confirm()`, after the status becomes CONFIRMED,
- has a `pull_events()` method that returns and clears the events.

Everything else in that file is your original code. Your T2 tests still pass with it.

## 2. Assumptions to check

- The service catches `DomainError`, so every rule rejection (BR2, BR3, BR4) becomes a failed outcome.
  This relies on your exception classes all subclassing `DomainError`, which they do.
- `ReservationEligibilityService` must not import from `src.application` or `src.infrastructure`
  (it only needs an object with `count_confirmed_seats`). `python scripts/check_dependencies.py` confirms this.
- Test files go in `tests/`. Move them if yours live in subfolders.

## 3. Commands

```bash
python -m pytest -v
python scripts/check_dependencies.py
python -m src.interface.cli R001
```

## 4. Design decision to mention on Slide 14

The Reservation is saved only after the event handler succeeds. If the Show rejects the seat (T8),
nothing is saved, so the Reservation stays PENDING and the use case returns `success=False`.
BR2 allows only PENDING -> CONFIRMED, so there is no "undo" state; not saving is the rollback.
This works because the in-memory repositories store and return copies.
