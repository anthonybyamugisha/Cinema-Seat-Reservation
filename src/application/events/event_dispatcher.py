from collections import defaultdict
from typing import Callable, Iterable


class EventDispatcher:
    """Simple in-process dispatcher (BR5).

    Handlers are registered per event type and called synchronously, in the
    order they were registered. If a handler raises, the exception reaches the
    caller, so the use case can decide what the outcome is.
    """

    def __init__(self):
        self._handlers = defaultdict(list)

    def register(self, event_type: type, handler: Callable) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, events: Iterable) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                handler(event)
