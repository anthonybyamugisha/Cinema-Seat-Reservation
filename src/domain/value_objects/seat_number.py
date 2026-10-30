import re
from dataclasses import dataclass

from src.domain.exceptions.domain_exceptions import InvalidSeatNumberError


@dataclass(frozen=True)
class SeatNumber:

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidSeatNumberError("Seat number must be a string.")

        #Introduced a named capture group to extract the position substring immediately
        match = re.fullmatch(r"[A-Z](?P<pos>[1-9][0-9]?)", self.value)
        if not match:
            raise InvalidSeatNumberError(
                "Seat number must contain one row letter A-Z followed by a position from 1-50."
            )

        #Validates boundaries instantly using the captured token before full initialization
        if not (1 <= int(match.group("pos")) <= 50):
            raise InvalidSeatNumberError(
                "Seat position must be between 1 and 50."
            )

    @property
    def row(self):
        return self.value[0]

    @property
    def position(self):
        return int(self.value[1:])
