import lark
from skema.lark import Tree, Token, v_args, Transformer
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from ordered_set import OrderedSet
from ..types import UniqueKey
from ..support import structure, literals, composed_types
import uuid
from copy import copy



@v_args(tree=True)
class RemoveAnnotations(Transformer):
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
class RemoveEllipses(Transformer):
    def object(self, t: Tree):
        last = t.children[-1]
        meta = t.meta if isinstance(t.meta, dict) else {}
        if isinstance(last, Tree) and last.data == literals.ELLIPSIS:
            t._meta = {**meta, 'ellipsis': True}
            t.children.pop(-1)
            return t
        t._meta = {**meta, 'ellipsis': False}
        return t



@v_args(tree=True)
class GetDependencies(Transformer):
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
class AddListMetas(Transformer):
    def required_pair(self, tree: Tree):
        name, list_node = tree.children
        if not list_node.data == "list":
            return tree
        list_node._meta = {**list_node._meta, "parent_key": name}
        return tree

    optional_pair = required_pair
    root_pair = required_pair


@v_args(tree=True)
class AddUnionMetas(Transformer):
    def required_pair(self, tree: Tree):
        name, list_node = tree.children
        if not list_node.data == "union":
            return tree
        list_node._meta = {**list_node._meta, "parent_key": name}
        return tree

    optional_pair = required_pair
    # root_pair = required_pair # TODO these metas are then used to split unions
