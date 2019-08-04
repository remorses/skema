
from functools import reduce

from .constants import *
from .support import (capitalize, is_and_key, is_enum_key, is_key, is_list_key,
                      is_object, is_or_key, is_scalar, is_leaf, is_leaf_key)
from .tree import Node


def replace_with_anchor(key):
    anchor = Node(compute_camel_cascaded_name(key), key)
    key.children = [anchor]
    return anchor

def make_reference(key):
    if is_or_key(key) or is_and_key(key):
        return Node(compute_camel_cascaded_name(key), key.parent).append(key.children)
    else:
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
    if is_or_key(key) or is_and_key(key):
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




FORBIDDEN_TYPE_NAMES = ['root', OR, AND, LIST]



# def is_object_key(node: Node):
#     return is_key(node) and is_object(node.children[0])


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




def merge_ands(node, references):
    ref_indexes_to_delete = []
    if is_and_key(node):
        result = Node(node.value, node.parent)
        items = node.children[0].children
        for child in items:
            ref = next((ref for ref in references if ref.value == child.value), None)
            if not ref:
                print(f'WARNING: {child.value} not found in references: {[r.value for r in references]}')
                return node, []
            ref, new_indexes = merge_ands(ref, references)
            ref_indexes_to_delete += new_indexes
            result_children_values = [c.value for c in result.children]
            children = [c for c in ref.children if c.value not in result_children_values]
            result.insert(*children) # TODO dont add props already present
            # deletes reference
            ref_indexes_to_delete += [i for i, r in enumerate(references) if ref.value == r.value]
        return result, ref_indexes_to_delete
    else:
        return node, ref_indexes_to_delete


def merge_scalar_unions(references):
    to_delete = {}
    for node in references:
        if (is_or_key(node) or is_and_key(node)) and any([is_scalar(c.value) for c in node.children[0].children]) and not is_enum_key(node):
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
        if c.value in to_delete.keys():
            c.value = to_delete[c.value]
        replace_occurrences(c, to_delete)

def get_aliases(node: Node):
    res = {}
    for c in node.children: # TODO this presume tree has Root
        if is_leaf_key(c):
            res.update({c.value: c.children[0].value})
    return res

def replace_aliases(node: Node, ):
    aliases = get_aliases(node)
    # print('aliases', aliases)
    for leaf in get_leaves(node, ):
        if leaf.value in aliases.keys():
            leaf.value = aliases[leaf.value]
    return Node(node.value, node.parent).append([c for c in node.children if c.value not in aliases])

def is_enumeration(node):
    return node.parent and node.parent.parent and is_enum_key(node.parent.parent)


def replace_types(node: Node,):
    if not node:
        return
    if '"' in node.value and not is_enumeration(node):
        node.value = 'String' # TODO replace with possible enum found in references
    if node.value in map_types_to_graphql:
        node.value = map_types_to_graphql[node.value]
    if '..' in node.value:
        node.value = 'Float'
    for c in node.children:
        replace_types(c)
    return node


map_types_to_graphql = {
    STR: 'String',
    ANY: 'String', # TODO make scalar Json
    BOOL: 'Boolean',
    NULL: 'String', # TODO remove them
    REGEX: 'String',
}
