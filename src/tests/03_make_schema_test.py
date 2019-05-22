
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest



simple = """
X:
    ciao: Str
    b: Int
"""


@pytest.mark.parametrize('string', [simple], False, ['simple'])
def test_make_schema(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    schema = make_schema(tree)
    assert schema

