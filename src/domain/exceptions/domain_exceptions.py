class DomainError(Exception):
    """Base class for all domain errors."""
    pass


class InvalidSeatNumberError(DomainError):
    """Raised when a seat number is invalid."""
    pass


class InvalidReservationStateError(DomainError):
    """Raised when a reservation state transition is invalid."""
    pass