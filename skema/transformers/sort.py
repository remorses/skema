from lark import Visitor, Tree, Token, v_args
from .support import Transformer
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from orderedset import OrderedSet
from ..types import UniqueKey
import uuid
from copy import copy
from ..support import structure, composed_types


class SortOptionalsLast(Transformer):
    def object(self, children):
        optionals = [
            child for child in children if child.data == structure.OPTIONAL_PAIR
        ]
        required = [
            child for child in children if child.data == structure.REQUIRED_PAIR
        ]
        return Tree(composed_types.OBJECT, required + optionals)
