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

@collecting
def unique(l, *, key):
    passed = set()
    for e in l:
        d = key(e)
        if not d in passed:
            yield e
        passed.add(d)


is_reference_parent = lambda node: (  # TODO add list reference k case
    node.data in ["optional_pair", "required_pair"]
    and node.children[1].data == "reference"
)

# is_reference_list_parent = lambda node: ( # TODO add list reference k case
#     node.data in ['optional_pair', 'required_pair'] and node.children[1].data == 'list'
#     and (node.children[1].children[0].data == 'list')
# )


def is_reference_list_parent(node: Tree):
    is_list_pair = (
        node.data in ["optional_pair", "required_pair"]
        and node.children[1].data == "list"
    )
    if not is_list_pair:
        return False
    list_node = node.children[1]
    return str(list_node.children[0].data) == "reference"