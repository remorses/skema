from dataclasses import dataclass
from typing import Optional


@dataclass
class Object:
    b: str
    a: Optional[float] = None
