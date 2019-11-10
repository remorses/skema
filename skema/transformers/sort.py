from skema.lark import Tree, Token, v_args, Transformer, MutatingTransformer
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from ordered_set import OrderedSet
from ..types import UniqueKey
import uuid
from copy import copy
from ..support import structure, composed_types


class SortOptionalsLast(MutatingTransformer):
    def object(self, t):
        optionals = []
        required = []
        for child in t.children:
            if child.data == structure.OPTIONAL_PAIR:
                optionals += [child]
            if child.data == structure.REQUIRED_PAIR:
                required += [child]
        t.children = required + optionals
