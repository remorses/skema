from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Xxx:
    sd: Optional[str]
    ciao: Any
    zz: float


@dataclass
class Bo:
    ciao: float
    xxx: Optional[Xxx]


@dataclass
class Event:
    """ciao"""
    a: float
    b: Bo
