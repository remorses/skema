from lark import Visitor, Tree, Token, v_args
from .support import Transformer, unique
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from orderedset import OrderedSet
from ..types import UniqueKey
import uuid
from copy import copy


class MergeIntersections(Transformer):
    types: dict

    def __init__(self,):
        self.types = {}

    @v_args(tree=True)
    def root_pair(self, t):
        key, *_ = t.children
        self.types[key] = t
        # is_reference = lambda node: node.data == "reference"
        # for child in t.find_pred(is_reference):
        #     print(child)
        #  self.child_of
        return t

    # def intersection(self, tree: Tree):
    #     to_join = []
    #     for child in tree.children:
    #         if child.data == 'reference':
    #             ref, = child.children
    #             root_pair = self.types[ref]
    #             # only if object
    #             _, object = root_pair.children
    #             fields = object.children
    #             to_join += fields
    #         elif child.data == 'object':
    #             to_join += child.children
    #     tree.data = 'object'
    #     tree.children = to_join

    def intersection(self, children):
        to_join = []
        for child in children:
            if child.data == "reference":
                ref, = child.children
                root_pair = self.types[ref]
                # only if object
                _, object = root_pair.children
                fields = object.children
                to_join += fields
            elif child.data == "object":
                to_join += child.children
        children = unique(to_join, key=lambda x: x.children[0])
        return Tree("object", children)
