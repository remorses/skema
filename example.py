from dataclasses import dataclass
from datetime import datetime


@dataclass
class Xxx:
    x: str


@dataclass
class Event:
    """evento del sistema"""
    a: float
    b: datetime
    xxx: Xxx
