from collections import defaultdict
from typing import Callable, Dict, List, Iterable

from src.domain.events.domain_event import DomainEvent


class EventDispatcher:
    """Simple in-process dispatcher (BR5).

    Handlers are registered per event type and called synchronously, in the
    order they were registered. If a handler raises, the exception reaches the
    caller, so the use case can decide what the outcome is.

    It takes DomainEvent, the Domain layer's Layer Supertype, so callers
    program against the abstraction and not against ReservationConfirmed.
    """

    def __init__(self) -> None:
        self._handlers: Dict[type, List[Callable[[DomainEvent], None]]] = defaultdict(list)

    def register(
        self, event_type: type, handler: Callable[[DomainEvent], None]
    ) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, events: Iterable[DomainEvent]) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                handler(event)