from .support import *
from graphql import build_schema


@pytest.mark.parametrize("x", schemas, ids=names)
def test_schema_valid(x):
    schema = gens.graphql(parse(x))
    print(schema)
    build_schema(schema)
