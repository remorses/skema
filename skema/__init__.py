from fastjsonschema import compile as compile_
from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
import sys
import json
from functools import reduce, partial

rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))

to_jsonschema = rcompose(
    tokenize,
    make_tree,
    make_schema
)


def compile(definition,):
    jsonschema = to_jsonschema(definition)
    return compile_(jsonschema)
