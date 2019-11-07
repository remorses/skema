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
    interface Interface {
        a: String
    }
    interface Node {
        b: String
    }
    type Y implements Interface & Node {
        a: String @direct
        b: X
    }
    union A = X | Y
    scalar Scalar

    directive @direct(
    reason: String = "No longer supported"
    ) on FIELD_DEFINITION | ENUM_VALUE

    type Listed {
        f: [X]
        j: String
    }

    input Input {
        a: Int
    }

    """
    )
    print(print_schema(s))
