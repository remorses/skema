from .support import *
import ast
from graphql import build_schema


@pytest.mark.parametrize("x", schemas, ids=names)
def test_schema_valid(x):
    code = gens.python(parse(x))
    print(code)
    ast.parse(code)
