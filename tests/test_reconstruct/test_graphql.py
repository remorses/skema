from skema.reconstruct import print_schema
from graphql import build_schema

def test_1():
    print()
    s = build_schema(
        """
    type X {
        a: String
        b: Int
    }
    """
    )
    print(print_schema(s))
