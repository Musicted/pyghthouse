from dataclasses import dataclass
from abc import ABC


class BaseEvent(ABC):
    pass


@dataclass
class KeyEvent(BaseEvent):
    code: int
    down: bool
