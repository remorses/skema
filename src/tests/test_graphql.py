from .support import *


def test_1():
    t = parser.parse(x)
    transformer = (
        MergeIntersections() * GetDependencies() * AddListMetas() * Splitter()
    )  # * ReplaceIds()
    t = transformer.transform(t)
    print(t.pretty())
    s = Graphql().transform(t)
    print(s)

def test_2():
    t = parser.parse(y)
    transformer = (
        MergeIntersections() * GetDependencies() * AddListMetas() * AddUnionMetas() * Splitter()
    )  # * ReplaceIds()
    t = transformer.transform(t)
    print(t.pretty())
    s = Graphql().transform(t)
    print(s)
