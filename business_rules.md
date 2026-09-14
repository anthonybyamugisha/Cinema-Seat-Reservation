# Business Rules

This project uses exactly six business rules for the Cinema Seat Reservation domain.

## BR1 — Value Rule

A SeatNumber is valid only when it contains one row letter from A-Z followed by a seat position from 1-50.

Responsible component: SeatNumber  
Violation outcome: InvalidSeatNumberError

## BR2 — Identity/State Rule

A Reservation starts in PENDING state and may transition to CONFIRMED only from PENDING.

Responsible component: Reservation  
Violation outcome: InvalidReservationStateError

## BR3 — Invariant Rule

Within one Show, a ShowSeat may be allocated to at most one Reservation.

Responsible component: Show  
Violation outcome: SeatAlreadyReservedError

## BR4 — Cross-Concept Rule

A Reservation is eligible for confirmation only when the Show has not started and the customer has fewer than four confirmed seats for that Show.

Responsible component: ReservationEligibilityService  
Violation outcome: ReservationNotEligibleError

## BR5 — Follow-Up Rule

When a Reservation successfully changes from PENDING to CONFIRMED, a ReservationConfirmed domain event must request the corresponding Show to reserve that SeatNumber.

Responsible components: ReservationConfirmed and ReservationConfirmedHandler  
Violation outcome: If the Show rejects allocation, confirmation is not persisted.

## BR6 — Lookup Rule

A Reservation must already exist before confirmation can proceed.

Responsible components: ReservationRepository and ConfirmReservationService  
Violation outcome: ReservationNotFoundError