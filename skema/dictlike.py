from typing import Any, Optional, List, Union, Callable
from typing_extensions import Literal
import skema
import fastjsonschema
from jsonschema import validate
from prtty import prettify


class dictlike(dict):
    def __getattr__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return object.__getattribute__(self, name)

    @classmethod
    def from_dict(cls, obj: dict):
        assert isinstance(obj, dict)
        return cls(**obj)

    @classmethod
    def from_(cls, obj: dict):
        assert isinstance(obj, dict)
        return cls(**obj)
    
    from_dict = from_

    def validate(self):
        # return self.validate_(self)
        return validate(instance=self, schema=self._schema)

    @classmethod
    def fake(cls, resolvers={}):
        return cls(
            **(
                skema.fake_data(
                    cls._schema, amount=1, from_json=True, resolvers=resolvers
                )[0]
                or {}
            )
        )

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        return f"{self.__class__.__name__}({prettify(self)})"
