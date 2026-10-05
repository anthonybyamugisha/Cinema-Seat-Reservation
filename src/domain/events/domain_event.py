from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent(ABC):
    """Layer Supertype for every event raised inside the Domain layer.

    BR5 defines one event today, ReservationConfirmed. Giving it a supertype
    means the Application layer can program against "any domain event"
    instead of a growing list of concrete classes: EventDispatcher.register
    and dispatch, and anything that logs or stores history, take DomainEvent.
    A second event type can then be added without touching those callers.

    It is frozen so an event is an immutable statement of something that
    already happened; it carries plain data only and never a reference to
    another aggregate.
    """