from dataclasses import dataclass


@dataclass(frozen=True)
class ConfirmReservationInput:
    reservation_id: str


@dataclass(frozen=True)
class ConfirmReservationOutput:
    reservation_id: str
    status: str  # final stored status of the Reservation: "PENDING" or "CONFIRMED"
    success: bool
    message: str
