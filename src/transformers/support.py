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

class types:
    STR = 'type_str'
    BOOL = 'type_bool'
    ANY = 'type_any'
    INT = 'type_int'
    FLOAT = 'type_float'
    REGEX = 'regex'

class literals:
    NULL = 'null'
    TRUE = 'true'
    FALSE = 'false'
    STRING = 'literal_string'
    INTEGER = 'literal_integer'
    ELLIPSIS = 'literal_ellipsis'

class composed_types:
    OBJECT = 'obect'
    LIST = 'list'
    INTERSECTION = 'intersection'
    UNION = 'union'
    RANGE = 'bounded_range'
    LOW_RANGE = 'low_bounded_range'
    HIGH_RANGE = 'high_bounded_range'

class structure:
    ROOT_PAIR = 'root_pair'
    REQUIRED_PAIR = 'required_pair'
    OPTIONAL_PAIR = 'optional_par'
    REFERENCE = 'reference'
    ANNOTATION = 'annotation'



@v_args(tree=True)
class Printer(Transformer):
    def start(self, t):
        print(t.pretty())
        return t


@collecting
def unique(l, *, key):
    passed = set()
    for e in l:
        d = key(e)
        if not d in passed:
            yield e
        passed.add(d)


is_reference_parent = lambda node: (  # TODO add list reference k case
    node.data in [structure.REQUIRED_PAIR, structure.OPTIONAL_PAIR]
    and node.children[1].data == structure.REFERENCE
)

# is_reference_list_parent = lambda node: ( # TODO add list reference k case
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
