from dataclasses import dataclass
from abc import ABC


class Event(ABC):
    pass


@dataclass
class KeyEvent(Event):
    code: int
    down: bool
