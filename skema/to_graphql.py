"""
skema to graphql

to_gaphql
- make_tree(skema) -> tree
- extract_references(tree, dont_nest=[LIST]) -> references
- [merge_ands(ref) for ref in references] -> references
- [ref.to_graphql() for ref in references] -> graphql


Node(reference_name)
    Node(p)
        Node(STR)
    Node(ref)
        Node(Name)
    Node(p)
        Node(LIST)
            Node(Name)
    Node(obj)
        Node(a)
            Node(Str)
        Node(b)
            Node(Int)
    Node(union)
        Node(OR)
            Node(Str)
            Node(Int)

->

type reference_name {
    p: STR
    ref: Name
    p: [Name]
}
"""
from .tree import Node
from .constants import *
from .constants import constants
from .support import capitalize

def extract_references(node: Node, references=[], root=None):
    if root is None:
        root = node
    # print('is_object', repr(node), is_object(node))
    if is_and_key(node) or is_or_key(node):
        # print('OR AND', repr(node))
        children = node.children[0].children
        OP = AND if is_and_key(node) else OR
    elif is_object(node):
        children = node.children
        OP = None
    else:
        raise NotImplementedError(('unknown' + repr(node)))
        
    reference = Node(capitalize(node.value,), node.parent)
    reference = reference.insert(Node(OP, reference)) if OP else reference
    # reference = reference.children[0] if OP else reference
    for child in children:
        if is_end_key(child):
            child = copy(child)
            if OP:
                child.value = search_cascaded_name(root, child.value)
                # child.parent = reference.children[0]
                reference.children[0].insert(child)
            else:
                # child.parent = reference
                reference = reference.insert(child)
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
    parent_name = ''.join(reversed(parent_names))
    print('from ' + child.value + ' with parent ' + child.parent.value + ' computed ' + parent_name + capitalize(child.value))
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
    queue = []
    queue.append(root)
    while len(queue):
        node = queue.pop()
        for child in node.children:
            queue.append(child)
            if original == child.value:
                return compute_camel_cascaded_name(child)
    raise Exception('not found')

def all_nodes_have_parent(root,):
    misses = []
    queue = []
    ok = True
    queue.append(root)
    while len(queue):
        node = queue.pop()
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
    if len(node.children) == 1 and node.children[0].value == LIST:
        return True
    if is_key(node) and not len(node.children[0].children):
        return True
    return False


def copy(node: Node):
    res = Node(node.value, node.parent)
    if len(node.children):
        res.insert(*[copy(c) for c in node.children])
    return res


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



tab = '    '

def to_graphql(self: Node, indent=''):
    res = ''
    if is_or_key(self):
        res += 'union '
        res += str(self.value)
        res += ' = '
        for c in self.children:
            res += Node.to_skema(c, indent + tab, )
        res += '\n'
    elif is_object(self):
        res += 'type '
        res += str(self.value)
        res += ' {'
        for c in self.children:
            res += '\n' + Node.to_skema(c, indent + tab, )
        res += '\n}'
    else:
        raise NotImplementedError('no valid graphql')
    return res