from .support import *


def test_1():
    t = parser.parse(x)
    # print(t.pretty())
    # mapper = MakeMap()
    # mapper.visit(t)
    # pretty(mapper.types)

    # t = MergeAnds().transform(t)
    # print('\nMERGED\n')
    # print(t.pretty())

    # t = Splitter().transform(t)
    # print(t.pretty())
    transformer = (
        MergeIntersections() * GetDependencies() * AddListMetas() * Splitter()
    )  # * ReplaceIds()
    t = transformer.transform(t)
    print(t.pretty())
    s = Graphql().transform(t)
    print(s)
