class DomainError(Exception):
    """Base class for all domain errors."""
    pass


class InvalidSeatNumberError(DomainError):
    """Raised when a seat number is invalid (BR1)."""
    pass


class InvalidReservationStateError(DomainError):
    """Raised when a reservation state transition is invalid (BR2)."""
    pass


class SeatAlreadyReservedError(DomainError):
    """Raised when a seat is already reserved for a show (BR3)."""
    pass


class SeatNotInShowError(DomainError):
    """Raised when the seat is not part of this show's seat map (BR3)."""
    pass


class ReservationNotEligibleError(DomainError):
    """Raised when a reservation is not eligible for confirmation (BR4)."""
    pass