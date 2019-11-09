from skema.lark import Tree, Token, v_args, Transformer
from lark.tree import Meta
from ..support import capitalize, structure, composed_types, literals, types
from ..logger import logger
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from ordered_set import OrderedSet
from ..types import UniqueKey
import uuid
from copy import copy


class TransformerWithMeta(Transformer):
    meta: dict

    def __init__(self,):
        self.meta = {}

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
    id = str(names[0]) + "".join([capitalize(x) for x in names[1:]])
    assert id
    return id


class Splitter(TransformerWithMeta):
    types: dict

    def __init__(
        self,
        objects_inside_objects=True,
        objects_inside_lists=True,
        unions_inside_objects=True,
        unions_inside_lists=True,
        join_names=join_names,
    ):
        self.types = {}
        self.join_names = join_names
        self.objects_inside_objects = objects_inside_objects
        self.objects_inside_lists = objects_inside_lists
        self.unions_inside_lists = unions_inside_lists
        self.unions_inside_objects = unions_inside_objects

    def make_new_name(self, name):
        if not isinstance(name, UniqueKey):
            name = UniqueKey(name)
        return self.join_names(list(self.dependencies[name]) + [name])

    @property
    def dependencies(self) -> dict:
        return self.meta["dependencies"]

    @v_args(tree=True)
    def root_pair(self, t):
        key, *_ = t.children
        self.types[key] = t
        return t

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
                id = self.make_new_name(name)
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:],), meta={})
                key.children = [name, Tree("reference", [id])]
        return Tree("object", children)

    @v_args(meta=True)
    def list(self, children, meta):
        if not meta or isinstance(meta, Meta):
            logger.warn(f'list parent of {children[0].pretty()} has not meta')

        if not any([self.objects_inside_lists, self.unions_inside_lists]):
            return Tree(composed_types.LIST, children)
        TO_SPLIT = {
            composed_types.OBJECT: self.objects_inside_lists,
            composed_types.UNION: self.unions_inside_lists,
        }
        TO_SPLIT = [k for k, v in TO_SPLIT.items() if v]
        child, = children
        if not child.data in TO_SPLIT:
            return Tree("list", children)
        name = meta["parent_key"]
        id = self.make_new_name(name)
        old_child = copy(child)
        self.types[id] = Tree("root_pair", [id] + [old_child], meta={})
        return Tree("list", [Tree("reference", [id])])

    @v_args(tree=True)
    def union(self, t,):
        meta = t.meta
        children = t.children
        if not meta:
            logger.warning(f'no meta for {children} union')
            return t
        if not self.unions_inside_objects:
            return t
        name = meta["parent_key"]
        id = self.make_new_name(name)
        old_children = copy(children)
        self.types[id] = Tree("root_pair", [id] + [Tree("union", old_children)], meta={})
        return Tree("reference", [id])
