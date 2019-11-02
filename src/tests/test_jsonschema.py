from .support import *


def test_1():
    tree = parser.parse(x)
    print(tree.pretty())
    pretty(JsonSchema().transform(tree))
