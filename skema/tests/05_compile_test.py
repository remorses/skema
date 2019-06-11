import json
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest
from .data import strings
from .support import keys, values
from .. import compile




@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_make_schema(string):
    validate = compile(string)
