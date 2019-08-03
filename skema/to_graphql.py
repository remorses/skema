from functools import reduce
from .tree import Node
from .constants import *
from .constants import constants
from .support import capitalize

HIDDEN_TYPE_NAMES = ['root', OR, AND, LIST]



def extract_references(node: Node, references=[], root=None):
    if root is None:
        root = node
    # print('is_object', repr(node), is_object(node))
    # print('OR AND', repr(node))
        
    reference = Node(capitalize(node.value,), node.parent)
    # reference = reference.insert(Node(OP, reference)) if OP else reference
    # reference = reference.children[0] if OP else reference
    
    for child in node.children:
        if is_end_key(child):
            child = copy(child)
            child.value = search_cascaded_name(root, child.value)
            reference = reference.insert(child)
        elif child.value in HIDDEN_TYPE_NAMES:
            dummy_reference = reference     
            dummy_reference.insert(Node(child.value, dummy_reference))
            dummy_reference = dummy_reference.children[0]
            dummy_reference.insert(*child.children)
        else:   
            reference_child_name = compute_camel_cascaded_name(child)
            reference_key = Node(child.value, child.parent)
            reference_key = reference_key.insert(Node(reference_child_name, child))
            reference = reference.insert(reference_key)

            child_reference = Node(reference_child_name, child)
            # child_reference = child_reference.insert(Node(OP, child_reference)) if OP else child_reference
            child_reference.insert(*[copy(c) for c in child.children])
            ref_values = [ref.value for ref in references]
            references += [ref for ref in extract_references(child_reference, root=root) if not ref.value in ref_values]

    return references + [reference]

def compute_camel_cascaded_name(child):
    parent = child.parent
    parent_names = []
    while isinstance(parent, Node):
        parent_names += [capitalize(parent.value)]
        parent = parent.parent
    parent_names = [x for x in parent_names if not x.lower() in HIDDEN_TYPE_NAMES]
    parent_name = ''.join(reversed(parent_names))
    # print('from ' + child.value + ' with parent ' + child.parent.value + ' computed ' + parent_name + capitalize(child.value))
    return parent_name + capitalize(child.value)

# def compute_camel_cascaded_name(child):
#     parent = child.parent
#     parent_name = ''
#     while isinstance(parent, Node):
#         parent_name += capitalize(parent.value) # if node.value != 'root' else ''
#         parent = parent.parent
#     print('from ' + child.value + ' with parent ' + child.parent.value + ' computed ' + parent_name + capitalize(child.value))
#     return parent_name + capitalize(child.value)

def search_cascaded_name(root, original):
    if is_scalar(original):
        return original
    queue = []
    queue.append(root)
    while len(queue):
        node = queue.pop(0)
        if original == node.value:
            return compute_camel_cascaded_name(node)
        for child in node.children:
            queue.append(child)

    raise Exception('not found')

def all_nodes_have_parent(root,):
    misses = []
    queue = []
    ok = True
    queue.append(root)
    while len(queue):
        node = queue.pop(0)
        if not node.parent:
            ok = False 
            misses += [node.value]
        for child in node.children:
            queue.append(child)
    return ok, misses
            
    
    

def is_object(node: Node):
    return (
        len(node.children) >= 1 and 
        all([len(c.children) for c in node.children if c.value != ELLIPSIS]) and 
        node.value not in [AND, OR, LIST,] # and 
        # node.children[0] not in [c for c in constants if c != ELLIPSIS]
    )


def is_key(node):
    return len(node.children) == 1

def is_and_key(node):
    return is_key(node) and node.children[0].value in [AND,]

def is_or_key(node):
    return is_key(node) and node.children[0].value in [OR,]

def is_end_key(node):
    if not node:
        return True
    if not len(node.children):
        return True
    if (
        len(node.children) == 1 and 
        node.children[0].value == LIST 
        # and len(node.children[0].children) == 1 # TODO nested objects in list gets split badly
    ):
        return True
    if is_key(node) and not len(node.children[0].children):
        return True
    return False


def copy(node: Node):
    res = Node(node.value, node.parent)
    if len(node.children):
        res.insert(*[copy(c) for c in node.children])
    return res





tab = '    '


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


def get_scalar_union(node):
    new_type = reduce(stronger_type, node.children[0].children,)
    return {node.value: new_type}

def merge_scalar_unions(references):
    to_delete = {}
    for node in references:
        if is_or_key(node) and all([is_scalar(c.value) for c in node.children[0].children]):
            obj = get_scalar_union(node)
            print('new_type', obj)
            to_delete.update(obj)
    print('to_delete', to_delete)
    for ref in references:
        replace_occurrences(ref, to_delete)
    return [r for r in references if not r.value in to_delete]

def replace_occurrences(ref, to_delete):
    for c in ref.children:
        if c.value in to_delete.keys():
            c.value = to_delete[c.value]
        replace_occurrences(c, to_delete)


def to_graphql(self: Node, indent='',):
    res = ''
    if is_or_key(self) and all(['"' in c.value for c in self.children[0].children]):
        res += 'enum '
        res += str(self.value)
        res += ' {'
        for c in self.children[0].children:
            value = c.value.replace('"', '')
            res += '\n' + tab + value # TODO enum values should get namespace
        res += '\n}'
    elif is_or_key(self):
        res += 'union '
        res += str(self.value)
        res += ' = '
        for c in self.children:
            res += Node.to_skema(c, indent + tab, )
        # res += '\n'
    elif is_object(self):
        res += 'type '
        res += str(self.value)
        res += ' {'
        for c in self.children:
            res += '\n' + Node.to_skema(c, indent + tab, )
        res += '\n}'
    else:
        raise NotImplementedError(f'no valid graphql\n{str(self)}')
    return res



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


map_types_to_graphql = {
    STR: 'String',
    ANY: 'String', # TODO make scalar Json
    BOOL: 'Boolean',
    NULL: 'String', # TODO remove them
}


def replace_types(node: Node,):
    if not node:
        return
    if node.value in map_types_to_graphql:
        node.value = map_types_to_graphql[node.value]
    if '..' in node.value:
        node.value = 'Float'
    if '"' in node.value:
        node.value = 'String' # TODO make enums
    for c in node.children:
        replace_types(c)
    return node



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

