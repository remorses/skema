from skema.lark import Tree, Token, v_args, Transformer
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from toposort import toposort, toposort_flatten
from ordered_set import OrderedSet
from ..types import UniqueKey
from ..logger import logger
from ..support import structure
import uuid
from copy import copy




@v_args(tree=True)
class Printer(Transformer):
    def start(self, t):
        logger.debug(t.pretty())
        return t
    


@collecting
def unique(l, *, key):
    passed = set()
    for e in l:
        d = key(e)
        if not d in passed:
            yield e
        passed.add(d)


is_reference_parent = lambda node: (
    node.data in [structure.REQUIRED_PAIR, structure.OPTIONAL_PAIR]
    and node.children[1].data == structure.REFERENCE
)

# is_reference_list_parent = lambda node: ( 
#     node.data in ['optional_pair', 'required_pair'] and node.children[1].data == 'list'
#     and (node.children[1].children[0].data == 'list')
# )


def is_reference_list_parent(node: Tree):
    is_list_pair = (
        node.data in [structure.REQUIRED_PAIR, structure.OPTIONAL_PAIR]
        and node.children[1].data == "list"
    )
    if not is_list_pair:
        return False
    list_node = node.children[1]
    return str(list_node.children[0].data) == structure.REFERENCE
