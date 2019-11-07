from skema.reconstruct import reconstruct_graphql
from graphql import build_schema

def test_1():
    print()
    s = (
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
    type Y implements Interface {
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
    tree = reconstruct_graphql(s)
    print()
