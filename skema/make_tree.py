
from .tree import Node
from .constants import *
from .support import log

def dummy(iter):
    yield from iter



# (&, [A, B])
# (&, [])
def extract_ast(text: str):
    if '&' in text:
        parts = text.split('&')
        yield (AND, [x for p in parts for x in tuple(extract_ast(p.strip()))])
    elif '|' in text:
        parts = text.split('|')
        yield (OR, [x for p in parts for x in tuple(extract_ast(p.strip()))])
    else:
        yield (text, [])

def make_value_tree(ast, node):
    # children = next(extract_nodes(val))
    # log('ast', ast)
    op, rest = ast
    child = Node(op.replace('!', ''), node, not_empty=op.endswith('!'))
    node.insert(child)
    for op, rest in rest:
        t = op, rest
        if op == '':
            node = node.children[0]
        else:
            node = make_value_tree(t, child).parent
    return node

# TODO parametrize this
INDENT_SIZE = 4

def _make_tree(tokens, node: Node=Node('root'), offset=0):
    log('call')
    # assert None
    if not node.parent and node.value != 'root':
        raise Exception('all nodes should have parents')
    child_annotation = ''

    for (i, token) in enumerate(tokens):
        if not node:
            raise Exception(f'something went wrong at token `{token["value"]}`')
        
        if token['type'] == 'REQUIRED_KEY':
            child = Node(token['value'], node)
            child.annotation = child_annotation
            child_annotation = ''
            node = node.insert(child)
            node = child

        elif token['type'] == 'OPTIONAL_KEY':
            child = Node(token['value'], node, required=False)
            child.annotation = child_annotation
            child_annotation = ''
            node = node.insert(child)
            node = child
            
        elif token['type'] == 'VAL':
            ast = next(extract_ast(token['value']))
            # print(ast)
            node = make_value_tree(ast, node)
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
            else:
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
        
        elif token['type'] == ']!':
            log(node.value)
            # while node.value != LIST:
            #     node = node.parent
            node.children[0].not_empty = True # TODO better test ]!
            node = node.parent
            return node
        
        elif token['type'] == 'ANNOTATION':
            child_annotation = token['value']
            # return node

        else:
            raise Exception(f'{token["type"]} not implemented')

    return node










def make_tree(tokens, ) -> Node:
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
