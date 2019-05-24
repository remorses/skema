import json
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest
from .data import strings
from .support import keys, values




@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_make_schema(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    schema = make_schema(tree)
    print(json.dumps(schema, indent=4))
    assert schema
