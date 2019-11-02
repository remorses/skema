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


@v_args(tree=True)
class GetDependencies(Transformer):
    dependencies: defaultdict = defaultdict(OrderedSet)

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
class AddListMetas(Transformer):
    def required_pair(self, tree: Tree):
        name, list_node = tree.children
        if not list_node.data == "list":
            return tree
        list_node._meta = {"parent_key": name}
        return tree

    optional_pair = required_pair
    root_pair = required_pair
