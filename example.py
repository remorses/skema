from dataclasses import dataclass
from typing import Optional


@dataclass
class Object:
    b_com: str
    a_ciao: Optional[float] = None
    sdf: Optional[float] = None
