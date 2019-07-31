from enum import Enum
from typing import Optional


class EnumEnum(Enum):
    CIAO_COME_VA = "ciaoComeVa"
    SDF_ADF = "sdf_adf"


class Xxx:
    """ciao"""
    sd: Optional[float]
    zz: float

    def __init__(self, sd: Optional[float], zz: float) -> None:
        self.sd = sd
        self.zz = zz


class BoCiao:
    """ciao"""
    ciaoComeVa: Optional[float]
    enum: Optional[EnumEnum]
    xxx: Optional[Xxx]

    def __init__(self, ciaoComeVa: Optional[float], enum: Optional[EnumEnum], xxx: Optional[Xxx]) -> None:
        self.ciaoComeVa = ciaoComeVa
        self.enum = enum
        self.xxx = xxx


class Example:
    """ciao"""
    a_come_stai: Optional[float]
    """ciao"""
    bCiaoComeVa: Optional[BoCiao]

    def __init__(self, a_come_stai: Optional[float], bCiaoComeVa: Optional[BoCiao]) -> None:
        self.a_come_stai = a_come_stai
        self.bCiaoComeVa = bCiaoComeVa
