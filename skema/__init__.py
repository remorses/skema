from fastjsonschema import compile as compile_
from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
from typing import Callable, Any
import sys
import json
from functools import reduce, partial
import fastjsonschema
from .__main__ import main, to_jsonschema
from .fake_data import fake_data
rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))


def compile(definition,) -> Callable[[dict], Any]:
    jsonschema = to_jsonschema(definition)
    return compile_(jsonschema)
