import re
from dataclasses import dataclass

from src.domain.exceptions.domain_exceptions import InvalidSeatNumberError


@dataclass(frozen=True)
class SeatNumber:
    """
    Value Object for BR1.

    BR1: A SeatNumber is valid only when it contains one row letter from A-Z
    followed by a seat position from 1-50.
    """

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidSeatNumberError("Seat number must be a string.")

        if not re.fullmatch(r"[A-Z][1-9][0-9]?", self.value):
            raise InvalidSeatNumberError(
                "Seat number must contain one row letter A-Z followed by a position from 1-50."
            )

        position = int(self.value[1:])

        if position < 1 or position > 50:
            raise InvalidSeatNumberError(
                "Seat position must be between 1 and 50."
            )

    @property
    def row(self):
        return self.value[0]

    @property
    def position(self):
        return int(self.value[1:])