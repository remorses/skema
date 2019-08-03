"""
queue di tutte le foglie
prendi una fogliq dalla queue e sali al parent, fino a quando `not is_valid_reference(key)`, se arriva al root senza trovarne una, muova la foglia in fondo alla lista e continua con un'altra foglia
    trovata una key valida chiama reference = `make_reference(key)` (prende i fifgli della key e li rende figli di una reference_anchor,)
    yield reference
    chiama `anchor` = `replace_with_anchor(key)` sulla key (sostituisce i figli della key con una copia della reference anchor senza figli)
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
from functools import reduce
from .tree import Node
from .support import capitalize
from .constants import *

def replace_with_anchor(key):
    anchor = Node(compute_camel_cascaded_name(key), key)
    key.children = [anchor]
    return anchor

def make_reference(key):
    # if is_list_key(key):
    #     return Node(compute_camel_cascaded_name(key), key.parent).append(key.children[0].children)
    if is_or_key(key) or is_and_key(key):
        return Node(compute_camel_cascaded_name(key), key.parent).append(key.children)
    else:
        return Node(compute_camel_cascaded_name(key), key.parent).append(key.children)

def get_current_subtypes(root: Node):
    nodes = breadth_first_traversal(root,)
    nodes = filter(is_valid_as_reference, nodes)
    nodes = reversed(list(nodes))
    nodes = list(nodes)
    print(f'valid refs are {nodes}')
    return nodes
    
def split_references(root: Node):
    nodes = get_current_subtypes(root)
    while nodes:
        key = nodes.pop(0)
        ref = make_reference(key)
        replace_with_anchor(key)
        yield ref
        print(f'after {repr(ref)}')
        print(root)
        nodes = get_current_subtypes(root)



def dereference_objects_inside_lists(root: Node):
    def is_big_list(node):
        return (
            node.value == LIST 
            and (len(node.children) > 1 or is_big_list(node.children[0]))
        )
    nodes = breadth_first_traversal(root,)
    nodes = filter(is_big_list, nodes)
    nodes = reversed(list(nodes))
    for big_list in nodes:
        ref = make_reference(big_list)
        yield ref
        replace_with_anchor(big_list)


        



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

# def is_object_key(node: Node):
#     return is_key(node) and is_object(node.children[0])

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
    if is_scalar(child.value):
        return child.value
    parent = child.parent
    parent_names = []
    while isinstance(parent, Node):
        parent_names += [capitalize(parent.value)]
        parent = parent.parent
    parent_names = [x for x in parent_names if all([not s in x.lower() for s in FORBIDDEN_TYPE_NAMES])]
    parent_names = [x for x in parent_names if not is_scalar(x)]
    parent_name = ''.join(reversed(parent_names))
    # print('from ' + child.value + ' with parent ' + child.parent.value + ' computed ' + parent_name + capitalize(child.value))
    end_name = child.value if (child.value not in [LIST, AND, OR] and not is_scalar(child.value)) else ''
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
    if '//' in value:
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



def merge_ands(node, references):
    if is_and_key(node):
        result = Node(node.value, node.parent)
        items = node.children[0].children
        for child in items:
            ref = next((ref for ref in references if ref.value == child.value), None)
            if not ref:
                return node
                raise Exception(f'{child.value} not found in references: {[r.value for r in references]}')
            ref = merge_ands(ref, references)
            result_children_values = [c.value for c in result.children]
            children = [c for c in ref.children if c.value not in result_children_values]
            result.insert(*children) # TODO dont add props already present
        return result
    else:
        return node


def merge_scalar_unions(references):
    to_delete = {}
    for node in references:
        if is_or_key(node) and any([is_scalar(c.value) for c in node.children[0].children]):
            new_type = reduce(stronger_type, node.children[0].children,)
            obj = {node.value: new_type}
            print('new_type', obj)
            to_delete.update(obj)
    print('to_delete', to_delete)
    for ref in references:
        replace_occurrences(ref, to_delete)
    return [r for r in references if not r.value in to_delete.keys()]



    


def stronger_type(a, b):
    if STR in [a, b] or STRING in [a, b] or REGEX in [a, b]:
        return STR
    if ANY in [a, b]:
        return ANY # will be converted to Json scalar
    if FLOAT in [a, b]:
        return FLOAT
    if INT in [a, b]:
        return INT
    if BOOL in [a, b]:
        return BOOL
    return STR



def replace_occurrences(ref, to_delete):
    for c in ref.children:
        if c.value in to_delete.keys():
            c.value = to_delete[c.value]
        replace_occurrences(c, to_delete)
