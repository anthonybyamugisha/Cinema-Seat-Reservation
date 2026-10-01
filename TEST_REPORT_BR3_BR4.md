# Test Report — BR3 and BR4

**Tester:** BEATRICE AKELLO 
**Date:** 2026-10-01
**Repo:** https://github.com/anthonybyamugisha/Cinema-Seat-Reservation
**Branch:** main

## Summary

BR3 and BR4 are **implemented and passing**. Full TDD cycle completed:
tests were written first (red phase), then implementation was added (green phase).

## Results

- T1 (BR1): 3 tests PASS
- T2 (BR2): 3 tests PASS
- T3 (BR3): 5 tests PASS
- T4 (BR4): 7 tests PASS
- **Total: 18 passed**

## Files added

- src/domain/entities/show.py
- src/domain/entities/show_seat.py
- src/domain/services/__init__.py
- src/domain/services/reservation_eligibility_service.py
- tests/test_t3_br3_show_seat_allocation.py
- tests/test_t4_br4_reservation_eligibility.py

## Files modified

- src/domain/exceptions/domain_exceptions.py
  (added SeatAlreadyReservedError, ReservationNotEligibleError)

## Evidence

- evidence/br3_red.txt — BR3 failing before implementation (TDD red)
- evidence/br4_red.txt — BR4 failing before implementation (TDD red)
- evidence/test_results_green.txt — all 18 tests passing (TDD green)

## Next steps for the next person

BR5 and BR6 (T5–T8) are still missing:
- ReservationConfirmed domain event
- ReservationConfirmedHandler
- ReservationRepository, ShowRepository
- InMemoryReservationRepository, InMemoryShowRepository
- ConfirmReservationService
- ConfirmReservationInput / ConfirmReservationOutput