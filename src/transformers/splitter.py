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


class TransformerWithMeta(Transformer):
    meta: dict = {}

    def transform(self, t):
        self.tree = t
        if not t.meta or not isinstance(t.meta, dict):
            raise Exception("needs meta")
        self.meta = t.meta
        # for k, v in t.meta["dependencies"].items():
        #     print(f"{k} -> {list(v)}")
        return super().transform(t)


def join_names(names):
    # print(repr(key))
    # print(self.dependencies[key])
    if not names:
        return str(uuid.uuid1())[:8]
    id = "_".join(names)
    assert id
    return id


class Splitter(TransformerWithMeta):
    types: dict = {}

    def __init__(
        self,
        objects_inside_objects=True,
        objects_inside_lists=True,
        unions_inside_objects=True,
        join_names=join_names,
    ):
        self.join_names = join_names
        self.objects_inside_objects = objects_inside_objects
        self.objects_inside_lists = objects_inside_lists
        self.unions_inside_objects = unions_inside_objects

    def make_new_name(self, name):
        if not isinstance(name, UniqueKey):
            name = UniqueKey(name)
        return self.join_names(list(self.dependencies[name]) + [name])

    @property
    def dependencies(self) -> dict:
        return self.meta["dependencies"]

    def root_pair(self, children):
        key, *_ = children
        self.types[key] = Tree("root_pair", children)
        return Tree("root_pair", children)

    def start(self, children):
        types = list(self.types.values())
        # tree.children.extend(types)
        return Tree("start", types)

    def object(self, children):
        if not self.objects_inside_objects:
            return Tree("object", children)
        for key in children:
            name, value = key.children  # TODO sometimes first is annotation
            if value.data in ["object"]:
                print("ok")
                id = self.make_new_name(name)
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
                key.children = [name, Tree("reference", [id])]
        return Tree("object", children)

    @v_args(meta=True)
    def list(self, children, meta):
        if not self.objects_inside_lists or not meta:
            return Tree("list", children)
        child, = children
        if not child.data in ["object", "list"]:
            return Tree("list", children)
        name = meta["parent_key"]
        id = self.make_new_name(name)
        old_children = copy(child.children)
        self.types[id] = Tree("root_pair", [id] + [Tree("object", old_children)])
        return Tree("list", [Tree("reference", [id])])

    @v_args(meta=True)
    def union(self, children, meta):
        if not self.unions_inside_objects or not meta:
            return Tree("union", children)
        name = meta["parent_key"]
        id = self.make_new_name(name)
        old_children = copy(children)
        self.types[id] = Tree("root_pair", [id] + [Tree("union", old_children)])
        return Tree("reference", [id])

