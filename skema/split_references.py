import operator
from functools import reduce
from typing import Tuple, Callable, Iterator, TypeVar
from .constants import *
from .support import (capitalize, is_and_key, is_enum_key, is_key, is_list_key,
                      is_object, is_or_key, is_scalar, is_leaf, is_leaf_key, is_and_object)
from .tree import Node, copy


def replace_with_anchor(key):
    anchor = Node(compute_camel_cascaded_name(key), key)
    key.children = [anchor]
    return anchor

def make_reference(key):
        return Node(compute_camel_cascaded_name(key), key.parent).append(key.children)

def is_valid_as_reference(key: Node):
    def is_valid_list_key(key):
        if not is_key(key):
            return False
        list_node = key.children[0]
        return not is_big_list(list_node)
    # true se è un oggetto con solo leaf_key oppure con piccole liste come figli
    if is_object(key) and not is_list_key(key) and all([is_leaf_key(c) or is_valid_list_key(c) for c in key.children]):
        return True
    if is_or_key(key) or is_and_key(key) or is_and_object(key):
        return True
    return False

def get_current_subtypes(root: Node):
    nodes = breadth_first_traversal(root,)
    nodes = filter(lambda x: is_valid_as_reference(x) or is_big_list(x), nodes)
    nodes = reversed(list(nodes))
    nodes = list(nodes)
    # print(f'valid refs are {nodes}')
    return nodes
    
def split_references(root: Node):
    nodes = get_current_subtypes(root)
    while nodes:
        key = nodes.pop(0)
        ref = make_reference(key)
        replace_with_anchor(key)
        yield ref
        # yield from dereference_objects_inside_lists(ref)
        # print(f'after {repr(ref)}')
        # print(root)
        nodes = get_current_subtypes(root)

def is_big_list(node):
    return (
        node.value == LIST 
        and (
            len(node.children) > 1
            or (
                len(node.children) == 1 
                and (
                    (node.children[0].value != LIST and not is_leaf(node.children[0]))
                    or (node.children[0].value == LIST and is_big_list(node.children[0]))
                )
            )
        )
    )



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

def remove_nulls(node: Node):
    if not node.children:
        return
    for c in node.children:
        node.children = [x for x in node.children if x.value != NULL]
        remove_ellipses(c)
    return node

FORBIDDEN_TYPE_NAMES = ['root', OR, AND, LIST]
ENUM_END_KEYWORD = 'Enum'


# def is_object_key(node: Node):
#     return is_key(node) and is_object(node.children[0])


def get_leaves(node):
    if is_leaf(node):
        return [node]
    else:
        leaves = [get_leaves(c) for c in node.children]
        leaves = [x for sublist in leaves for x in sublist]
        return leaves

T = TypeVar('T')
def breadth_first_traversal(root: Node, operation: Callable[[Node], T]=lambda x: x) -> Iterator[T]:
    queue = []
    queue.append(root)
    while len(queue):
        node = queue.pop(0)
        yield operation(node)
        for child in node.children:
            queue.append(child)



def search_cascaded_name(root: Node, target: Node) -> Tuple[str, ...]:
    """
    always find node in a tree if it is taken from himself
    """
    # if is_scalar(target.value):
    #     return target.value
    def operation(node: Node) -> Tuple[str, ...]:
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

def compute_camel_cascaded_name(child: Node) -> Tuple[str, ...]: # TODO search if there are already same names
    if is_scalar(child.value):
        return child.value
    parent = child.parent
    parent_names = []
    while isinstance(parent, Node):
        parent_names += [capitalize(parent.value)]
        parent = parent.parent
    parent_names = [x for x in parent_names if all([not s in x.lower() for s in FORBIDDEN_TYPE_NAMES])]
    parent_names = [x for x in parent_names if not is_scalar(x)]
    parent_names = tuple(reversed(parent_names))
    # print('from ' + child.value + ' with parent ' + child.parent.value + ' computed ' + parent_name + capitalize(child.value))
    end_name = child.value if (child.value not in [LIST, AND, OR] and not is_scalar(child.value)) else ''
    return parent_names + (capitalize(end_name), ) if end_name else parent_names


INTERFACE_END_KEYWORD = '_'

def merge_ands(node, references):
    ref_indexes_to_delete = []
    if is_and_key(node) or is_and_object(node):
        result = Node(node.value, node.parent)
        items = node.children[0].children
        for child in items:
            ref = next((ref for ref in references if ref.value == child.value), None)
            if not ref:
                print(f'WARNING: {child.value} not found in references: {[r.value for r in references]}')
                return node, []
            ref, new_indexes = merge_ands(ref, references)
            ref_indexes_to_delete += new_indexes
            children = [c for c in ref.children if c.value not in [c.value for c in result.children]]
            result.insert(*children)
            result.implements += [ref.value + INTERFACE_END_KEYWORD]
            ref_indexes_to_delete += [i for i, r in enumerate(references) if ref.value == r.value]
            if node.children[1:]:
                result.append([n for n in node.children[1:] if n.value not in [c.value for c in result.children]])
                # result.implements += [ref.value]
        return result, ref_indexes_to_delete
    else:
        return node, ref_indexes_to_delete


def merge_scalar_unions(references):
    to_delete = {}
    for node in references:
        is_scalar_union = (
            (is_or_key(node) or is_and_key(node)) 
            and any([is_scalar(c.value) and c.value != NULL for c in node.children[0].children])
            and not is_enum_key(node)
        )
        if is_scalar_union:
            new_type = reduce(stronger_type, node.children[0].children,)
            obj = {node.value: new_type}
            # print('new_type', obj)
            to_delete.update(obj)
    # print('to_delete', to_delete)
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
        if is_leaf(c) and c.value in to_delete.keys():
            c.value = to_delete[c.value]
        replace_occurrences(c, to_delete)

def get_alias_nodes(node: Node):
    for c in node.children: # TODO this presume tree has Root
        if is_leaf_key(c):
            yield c


# def get_aliases(node: Node):
#     res = {}
#     for c in node.children: # TODO this presume tree has Root
#         if is_leaf_key(c):
#             res.update({c.value: c.children[0].value})
#     return res

# def replace_aliases(node: Node, ):
#     aliases = get_aliases(node)
#     # print('aliases', aliases)
#     for leaf in get_leaves(node, ):
#         if leaf.value in aliases.keys():
#             leaf.value = aliases[leaf.value]
#     return Node(node.value, node.parent).append([c for c in node.children if c.value not in aliases])

def is_enumeration(node):
    return node.parent and node.parent.parent and is_enum_key(node.parent.parent)


def search_enum_ref(value, refs):
    enums = [r for r in refs if is_enum_key(r)]
    get_enums = lambda x: [c.value for c in x.children[0].children]
    found = next((x.value for x in enums if value in get_enums(x)), None)
    return found


def replace_types(node: Node, refs):
    if not node:
        return
    if '"' in node.value and node.parent.value != OR:
        node.value = search_enum_ref(node.value, refs) or 'String'
    if node.value in map_types_to_graphql:
        node.value = map_types_to_graphql[node.value]
    if '..' in node.value:
        node.value = 'Float'
    for c in node.children:
        replace_types(c, refs)
    return node


map_types_to_graphql = {
    STR: 'String',
    ANY: 'Json',
    BOOL: 'Boolean',
    REGEX: 'String',
}

def mark_enums(refs):
    enums = [r for r in refs if is_enum_key(r)]
    for r in enums:
        if isinstance(r.value, tuple):
            r.value += (ENUM_END_KEYWORD,)
        else:
            r.value += ENUM_END_KEYWORD
    return refs