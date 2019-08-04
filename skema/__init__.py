from fastjsonschema import compile as compile_
from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
from typing import Callable, Any
import sys
import json
from functools import reduce, partial
from .to_jsonschema import to_jsonschema
from .support import rcompose
from .fake_data import fake_data


def compile(definition,) -> Callable[[dict], Any]:
    jsonschema = to_jsonschema(definition)
    return compile_(jsonschema)

def validate(schema, instance, **kwargs):
    return compile(schema)(instance, **kwargs)
