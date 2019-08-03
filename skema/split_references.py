"""
queue di tutte le foglie
prendi una fogliq dalla queue e sali al parent, fino a quando `not is_valid_reference(key)`, se arriva al root senza trovarne una, muova la foglia in fondo alla lista e continua con un'altra foglia
    trovata una key valida chiama reference = `make_reference(key)` (prende i fifgli della key e li rende figli di una reference_anchor,)
    yield reference
    chiama `anchor` = `replace_with_anchor(key)` sulla key (sostituisce i figli della key con una compia della reference anchor senza figli)
    aggiunge quasta anchor (con key come parent) alla queue di fogie
    rimuovi n foglie dalla queue di foglie, dove n è  `len(get_leaves(reference))`
continua con la prossima foglia nella queue
fino a quando la queue non è vuota




is_valid_reference
true se è un oggetto con solo leaf_key oppure con piccole liste come figli
if is_object(key) and all([is_leaf_key(c) or (is_list_key(c) and is_leaf(c.children[0])) for c in key.children])

ture se è list con leaf come figlio
if is_list_key(key) and is_leaf(key.children[0])

true se è key di una unione
if is_or_key(key) or is_and_key(key)

def make_reference(key):
    if is_object(key): 
        return Node(computed_name(key), key.parent).append(key.children)
    if is_list_key: 
        return Node(computed_name(key), key.parent).append(key.children[0].children)
    if is_or_key(key) or is_and_key(key): 
        return Node(key, key.parent).append(key.children)

def replace_with_anchor(key):
    anchor = Node(computed_name(key), key)
    key.children = anchor
    return anchor

"""
from .tree import Node
from .support import capitalize
from .constants import *


def remove_objects_inside_lists(root: Node):
    pass


def remove_ellipses(node: Node):
    if not node.children:
        return
    for c in node.children:
        if len(node.children) == 1 and node.children[0].value == ELLIPSIS:
            node.children = [Node(ANY, node)]
        else:
            node.children = [x for x in node.children if x.value != ELLIPSIS]
            remove_ellipses(c)
    return node

def is_valid_as_reference(key: Node):
    def is_valid_list_key(key):
        if not is_key(key):
            return False
        list_node = key.children[0]
        return (
            is_key(key)
            and is_list_key(key)
            and (is_leaf_key(list_node) or is_valid_list_key(list_node))
        )
    # true se è un oggetto con solo leaf_key oppure con piccole liste come figli
    if is_object(key) and not is_list_key(key) and all([is_leaf_key(c) or is_valid_list_key(c) for c in key.children]):
        return True
    # ture se è list con leaf come figlio
    # if is_valid_list_key(key):
    #     return True
    # true se è key di una unione
    if is_or_key(key) or is_and_key(key):
        return True
    return False


FORBIDDEN_TYPE_NAMES = ['root', OR, AND, LIST]

# def replace_forbidden_names(s: str):
#     if OR in s:
#         return s.replace(OR, 'Union')
#     elif AND in s:
#         return s.replace(AND, 'Glued')
#     elif LIST in s:
#         return s.replace(LIST, 'List')
#     elif 'root' in s:
#         return ''
#     else:
#         raise Exception('should not be here')

def is_leaf(node):
    return (
        not node.children
    )

def is_leaf_key(node):
    return (
        len(node.children) == 1
        and is_leaf(node.children[0])
    )

def is_object(node):
    return (
        len(node.children) >= 1
        and all([len(c.children) for c in node.children if c.value != ELLIPSIS])
        and node.value not in [AND, OR, LIST,]
        # node.children[0] not in [c for c in constants if c != ELLIPSIS]
    )

def get_leaves(node):
    if is_leaf(node):
        return [node]
    else:
        leaves = [get_leaves(c) for c in node.children]
        leaves = [x for sublist in leaves for x in sublist]
        return leaves


def breadth_first_traversal(root: Node, operation=lambda x: x):
    queue = []
    queue.append(root)
    while len(queue):
        node = queue.pop(0)
        yield operation(node)
        for child in node.children:
            queue.append(child)



def search_cascaded_name(root, target):
    """
    always find node in a tree if it is taken from himself
    """
    # if is_scalar(target.value):
    #     return target.value
    def operation(node: Node):
        if target.value == node.value:
            if same_parents(node, target):
                return compute_camel_cascaded_name(node)
    results = list(breadth_first_traversal(root, operation))
    results = filter(bool, results)
    results = list(results)
    if not results:
        raise Exception(f'{target.value} not found')
    return results[0]


def same_parents(a, b, count=0):
    if count < 5:
        if a.parent and b.parent and a.parent == b.parent:
            return same_parents(a.parent, b.parent, count + 1)
        elif a.parent or b.parent:
            return False
        else:
            return True
    else:
        return True

def compute_camel_cascaded_name(child):
    parent = child.parent
    parent_names = []
    while isinstance(parent, Node):
        parent_names += [capitalize(parent.value)]
        parent = parent.parent
    parent_names = [x for x in parent_names if all([not s in x.lower() for s in FORBIDDEN_TYPE_NAMES])]
    parent_names = [x for x in parent_names if not is_scalar(x)]
    parent_name = ''.join(reversed(parent_names))
    # print('from ' + child.value + ' with parent ' + child.parent.value + ' computed ' + parent_name + capitalize(child.value))
    end_name = child.value if (child.value not in FORBIDDEN_TYPE_NAMES and not is_scalar(child.value)) else ''
    return parent_name + capitalize(end_name)


def is_scalar(value):
    value = value.lower()
    scalars = [STR, STRING, INT, FLOAT, REGEX, ANY, NULL, BOOL]
    if value in [x.lower() for x in scalars]:
        return True
    if '"' in value:
        return True
    if '..' in value:
        return True
    return False


def is_key(node):
    """opoosto di leaf o di oggetto"""
    return len(node.children) == 1

def is_and_key(node):
    return is_key(node) and node.children[0].value in [AND,]

def is_or_key(node):
    return is_key(node) and node.children[0].value in [OR,]

def is_list_key(node):
    return is_key(node) and node.children[0].value in [LIST,]