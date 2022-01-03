from .events import Event, KeyEvent
from queue import Queue, Empty


class EventManager:
    queue: Queue[Event]

    def __init__(self):
        self.queue = Queue(maxsize=0)

    def add_event(self, e: Event):
        self.queue.put(e)

    def add_key_event(self, code: int, down: bool):
        self.add_event(KeyEvent(code, down))

    def get_event(self):
        try:
            return self.queue.get(block=False)
        except Empty:
            return None
