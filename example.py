from enum import Enum
from dataclasses import dataclass
from typing import Optional, Union


class Ciao(Enum):
    SDF = "sdf"
    SDG = "sdg"
    SSS = "sss"


@dataclass
class Xxx:
    sd: Optional[str]
    ciao: Ciao
    ints: Union[float, int]
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
