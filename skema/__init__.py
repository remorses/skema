from fastjsonschema import compile as compile_
from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
import sys
import json
from functools import reduce, partial
import jsonref
import fastjsonschema
from .__main__ import main, to_jsonschema

rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))


def compile(definition,):
    jsonschema = to_jsonschema(definition)
    return compile_(jsonschema)
