from lark import Transformer as _Transformer, Visitor, Tree as _Tree, v_args, Token
from lark.visitors import Interpreter


class Tree(_Tree):
    def __init__(self, data, children, meta=None):
        self.data = data
        self.children = children
        self._meta = meta or dict()
    @property
    def meta(self):
        return self._meta


class Transformer(_Transformer):
    tree: Tree
    def transform(self, tree):
        self.tree = tree
        self.meta = tree.meta
        return super().transform(tree)
    def __default__(self, data, children, meta):
        "Default operation on tree (for override)"
        if not isinstance(meta, dict):
            meta = dict()
        return Tree(data, children, meta)


class MutatingTransformer(Visitor):
    def transform(self, tree):
        self.tree = tree
        self.meta = tree.meta
        self.visit(tree)
        return tree


class TopDownTransformer(Interpreter):
    def transform(self, t):
        self.visit(t)
        return t


def chain_with(transformers: list):
    def wrapper(cls):
        class Wrapper(cls):
            def transform(self, tree):
                for t in transformers:
                    tree = t.transform(tree)
                tree = super().transform(tree)
                return tree

        return Wrapper

    return wrapper
