from lark import Visitor, Tree, Transformer, Token, v_args
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from orderedset import OrderedSet
from ..types import UniqueKey
import uuid
from copy import copy


class Splitter(Transformer):
    types: dict = {}
    tree: Tree
    dependencies: dict

    def transform(self, t):
        self.tree = t
        if not t.meta or not "dependencies" in t.meta:
            raise Exception("needs tree with dependencies")
        self.dependencies = t.meta["dependencies"]
        for k, v in t.meta["dependencies"].items():
            print(f"{k} -> {list(v)}")
        return super().transform(t)

    def make_id(self, key):
        print(repr(key))
        print(self.dependencies[key])
        if not key:
            return str(uuid.uuid1())[:8]
        if not isinstance(key, UniqueKey):
            key = UniqueKey(key)
        id = "_".join(list(self.dependencies[key])) + "_" + str(key)
        assert id
        return id

    def root_pair(self, children):
        key, *_ = children
        self.types[key] = Tree("root_pair", children)
        return Tree("root_pair", children)

    def start(self, children):
        types = list(self.types.values())
        # tree.children.extend(types)
        return Tree("start", types)

    def __init__(self,):
        self.types = {}
        pass

    @v_args(meta=True)
    def list(self, children, meta):
        child, = children
        if not child.data in ["object", "list"]:
            return Tree("list", children)
        parent_key = meta["parent_key"]
        id = self.make_id(parent_key)
        old_children = copy(child.children)
        self.types[id] = Tree("root_pair", [id] + [Tree("object", old_children)])
        return Tree("list", [Tree("reference", [id])])

    def intersection(self, tree: Tree):
        raise Exception("cannot handle intersections")

    def object(self, children):
        for key in children:
            name, value = key.children  # TODO sometimes first is annotation
            if value.data in ["object"]:
                print("ok")
                id = self.make_id(name)
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
                key.children = [name, Tree("reference", [id])]
        return Tree("object", children)

