from dataclasses import dataclass
from typing import Optional


@dataclass
class Xxx:
    """ciao"""
    sd: Optional[float]
    zz: float


@dataclass
class Bo:
    """ciao"""
    ciao: float
    xxx: Xxx


@dataclass
class Example:
    """ciao"""
    a: float
    """ciao"""
    b: Bo
