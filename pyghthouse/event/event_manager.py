from .events import BaseEvent, KeyEvent
from queue import Queue, Empty


class EventManager:
    queue: Queue[BaseEvent]

    def __init__(self):
        self.queue = Queue(maxsize=0)

    def add_event(self, e: BaseEvent):
        self.queue.put(e)

    def add_key_event(self, code: int, down: bool):
        self.add_event(KeyEvent(code, down))

    def get_event(self):
        try:
            return self.queue.get(block=False)
        except Empty:
            return None

    def get_all_events(self):
        events = []
        while not self.queue.empty():
            events.append(self.queue.get(block=False))
        return events
