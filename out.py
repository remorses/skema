# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = out_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class X(Enum):
    CIAO = "ciao"
    SALUTI = "saluti"


@dataclass
class Out:
    y: float
    string: Optional[str] = None
    x: Optional[X] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Out':
        assert isinstance(obj, dict)
        y = from_float(obj.get("y"))
        string = from_union([from_str, from_none], obj.get("string"))
        x = from_union([X, from_none], obj.get("x"))
        return Out(y, string, x)

    def to_dict(self) -> dict:
        result: dict = {}
        result["y"] = to_float(self.y)
        result["string"] = from_union([from_str, from_none], self.string)
        result["x"] = from_union([lambda x: to_enum(X, x), from_none], self.x)
        return result


def out_from_dict(s: Any) -> Out:
    return Out.from_dict(s)


def out_to_dict(x: Out) -> Any:
    return to_class(Out, x)

x = Out.from_dict({'y': 0, 'adsf': 0})
print(x)