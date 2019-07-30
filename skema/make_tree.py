
from .tree import Node
from .constants import *
from .support import log

def dummy(iter):
    yield from iter




def extract_ast(text: str):
    if '&' in text:
        parts = text.split('&')
        yield (AND, [x for p in parts for x in tuple(extract_ast(p.strip()))])
    elif '|' in text:
        parts = text.split('|')
        yield (OR, [x for p in parts for x in tuple(extract_ast(p.strip()))])
    else:
        yield text

def make_value_tree(ast, node = Node('root')):
    # children = next(extract_nodes(val))
    # log('ast', ast)
    if isinstance(ast, tuple):
        op, rest = ast
        child = Node(op, node)
        node.insert(child)
        for t in rest:
            make_value_tree(t, child)
    else:
        node.insert(Node(ast, node, ))
    return node

# TODO parametrize this
INDENT_SIZE = 4

def _make_tree(tokens, node: Node=Node('root'), offset=0):
    log('call')
    # assert None
    if not node.parent and node.value != 'root':
        raise Exception('all nodes should have parents')

    for (i, token) in enumerate(tokens):
        log()
        log(i, token['type'], token['value'])
        log('node', node.value)
        log('offset', offset)
        
        if token['type'] == 'REQUIRED_KEY':
            child = Node(token['value'], node)    
            node = node.insert(child)
            node = child

        elif token['type'] == 'OPTIONAL_KEY': # TODO
            child = Node(token['value'], node, required=False)    
            node = node.insert(child)
            node = child
            
        elif token['type'] == 'VAL':
            ast = next(extract_ast(token['value']))
            root = make_value_tree(ast, node)
            node = node.parent
            
        elif token['type'] == 'REGEX':
            child = Node(REGEX, node,)
            child.pattern = token['value']
            node.insert(child)
            node = node.parent

        elif token['type'] == ELLIPSIS:
            child = Node(token['value'], node)    
            # child.insert(Node(ANY, child))
            node = node.insert(child)
            # node = child

        elif token['type'] == 'SEPARATOR':
            # log('here')
            if int(token['value']) == offset:
                # node = node.parent
                pass
            elif int(token['value']) > offset:
                log(f"{token['value']} > {offset}")
                node = _make_tree(tokens, node, int(token['value']))
                # node = node.parent
                # offset -= INDENT_SIZE
            else: # TODO, other root keys end here
                log(f"{token['value']} < {offset}")
                off = (offset - int(token['value'])) // INDENT_SIZE
                log('off', off)
                # offset -= off * INDENT_SIZE
                while off :
                    node = node.parent
                    off -= 1
                log('offset', offset)
                # log('value', node.value)
                return node

        elif token['type'] == '[':
            # log('here')
            child = Node(LIST, node)    
            node = node.insert(child)
            node = child
            node = _make_tree(tokens, node, offset )
        
        elif token['type'] == ']':
            log(node.value)
            # while node.value != LIST:
            #     node = node.parent
            node = node.parent
            return node
        
        elif token['type'] == 'ANNOTATION':
            node.child_annotations += [token['value']]
            # return node

        else:
            raise Exception(f'{token["type"]} not implemented')

    return node










def make_tree(tokens) -> Node:
    root = Node('root',)
    log(tokens)
    separators = list(filter(lambda x: x['type'] == 'SEPARATOR', tokens))
    is_4indents = [x['value'] % 4 == 0 for x in separators]
    is_2indents = [x['value'] % 2 == 0 for x in separators]
    if not all(is_4indents): #and not all(is_2indents):
        raise Exception('indents must be all 2 or 4 spaces') 
    INDENT_SIZE = 4 #separators[0]['value'] if separators else 4
    log(INDENT_SIZE)
    # root.parent = root
    res = _make_tree(dummy(tokens), root, 0)
    # log('res', res)
    return root
