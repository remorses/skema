import json
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest
from .data import strings
from .support import keys, values
from skema.to_graphql import extract_references


@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_extract_references(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    print()
    print(tree)
    refs = extract_references(tree, [])
    print('len', len(refs))
    res = '\n\n'.join([str(r) for r in refs])
    print(res)
    print()