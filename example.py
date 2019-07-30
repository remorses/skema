from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Xxx:
    """ciao"""
    sd: Optional[str]
    ciao: Any
    zz: float


@dataclass
class Bo:
    """ciao"""
    ciao: float
    xxx: Optional[Xxx]


@dataclass
class Example:
    """ciao"""
    a: float
    """ciao"""
    b: Bo
