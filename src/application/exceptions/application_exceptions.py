class ReservationNotFoundError(Exception):
    """BR6: the Reservation must already exist before confirmation can proceed."""


class ShowNotFoundError(Exception):
    """The Show referenced by a Reservation or event could not be found."""
