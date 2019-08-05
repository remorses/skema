import json
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
from ..from_jsonschema import from_jsonschema
import pytest
from .data import strings
from .support import keys, values
from ..resolve_refs import resolve_refs
import skema


@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_from_schema(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    print(tree)
    print()
    schema = make_schema(tree)
    resolve_refs(schema)
    print(json.dumps(schema, indent=4))
    x = from_jsonschema(schema)
    print(x)
    print()

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_from_tree(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    print()
    print(tree)
    skema.tree.tab = '.   '
    print()
    print(tree.to_skema())
    skema.tree.tab = '    '
    print()
    
