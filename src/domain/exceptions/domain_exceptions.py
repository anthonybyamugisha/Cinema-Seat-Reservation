class DomainError(Exception):
    """Base class for all domain errors."""
    pass


class InvalidSeatNumberError(DomainError):
    """Raised when a seat number is invalid."""
    pass