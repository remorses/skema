from lark import Visitor, Tree, Token, v_args
from .support import Transformer
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from orderedset import OrderedSet
from ..types import UniqueKey
from ..support import structure
import uuid
from copy import copy


class TranformerDictMeta(Transformer):
    def __default__(self, data, children, meta):
        "Default operation on tree (for override)"
        if not isinstance(meta, dict):
            meta = {}
        return Tree(data, children, meta)

@v_args(tree=True)
class RemoveAnnotations(TranformerDictMeta):
    def root_pair(self, t: Tree):
        first, *_ = t.children
        if isinstance(first, Tree) and first.data == structure.ANNOTATION:
            annotation = t.children.pop(0).children[0]
        else:
            annotation = ''
        meta = t.meta if isinstance(t.meta, dict) else {}
        t._meta = {**meta, 'annotation': str(annotation)}
        return t
    required_pair = root_pair
    optional_pair = root_pair


@v_args(tree=True)
class GetDependencies(TranformerDictMeta):
    dependencies: defaultdict
    
    def __init__(self,):
        self.dependencies = defaultdict(OrderedSet)
        
    def start(self, tree):
        ordered_deps = list(toposort_flatten(self.dependencies_as_sets))
        for k in ordered_deps:
            v = self.dependencies[k]
            to_process = [x for x in v if x in self.dependencies]
            for x in to_process:
                self.dependencies[(k)].update(self.dependencies[x])
        return Tree("start", tree.children, meta={"dependencies": self.dependencies})

    @property
    def dependencies_as_sets(self,):
        return {k: set(v) for k, v in self.dependencies.items()}

    def required_pair(self, t):
        this, value = t.children
        if value.data == "object":
            for child in value.children:
                k, _ = child.children
                self.dependencies[UniqueKey(k)].add(UniqueKey(this))
        return t

    optional_pair = required_pair
    root_pair = required_pair


@v_args(tree=True)
class AddListMetas(TranformerDictMeta):
    def required_pair(self, tree: Tree):
        name, list_node = tree.children
        if not list_node.data == "list":
            return tree
        list_node._meta = {**list_node._meta, "parent_key": name}
        return tree

    optional_pair = required_pair
    root_pair = required_pair


@v_args(tree=True)
class AddUnionMetas(TranformerDictMeta):
    def required_pair(self, tree: Tree):
        name, list_node = tree.children
        if not list_node.data == "union":
            return tree
        list_node._meta = {**list_node._meta, "parent_key": name}
        return tree

    # optional_pair = required_pair
    # root_pair = required_pair
