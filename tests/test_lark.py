from skema.lark import MutatingTransformer, chain_with
from lark import Transformer, Tree


def test_trans():
    class Example1(Transformer):
        def start(self, children):
            print("start 1")
            return Tree("start", [])

    @chain_with([Example1()])
    class Example2(Transformer):
        def start(self, children):
            print("start 2")
            return Tree("start", [])

    t = Tree("start", [])
    Example2().transform(t)


def test_visitor():
    class Example1(MutatingTransformer):
        def start(self, t):
            print("start 1")

    @chain_with([Example1()])
    class Example2(MutatingTransformer):
        def start(self, t):
            print("start 2")

    t = Tree("start", [])
    Example2().transform(t)

