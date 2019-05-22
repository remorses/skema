
from .tree import Node
from .constants import *

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
    print('ast', ast)
    if isinstance(ast, tuple):
        op, rest = ast
        child = Node(op)
        node.insert(child)
        # node = child
        for t in rest:
            make_value_tree(t, child)
    else:
        node.insert(Node(ast))
    return node

def _make_tree(tokens, node: Node=Node('root'), offset=0):
    print('call')

    for (i, token) in enumerate(tokens):
        print(i, token['type'], token['value'])
        print(node.value)
        if token['type'] == 'REQUIRED_KEY':
            child = Node(token['value'], node)    
            node = node.insert(child)
            node = child

        elif token['type'] == 'OPTIONAL_KEY': # TODO
            child = Node(token['value'], node)    
            node = node.insert(child)
            node = child
            
        elif token['type'] == 'VAL':
            ast = next(extract_ast(token['value']))
            root = make_value_tree(ast, node)
            print(ast)
            # node = node.insert(*root.children)
            # child = Node(token['value'], node)    
            # node = node.insert(child)

        elif token['type'] == MORE:
            child = Node(token['value'], node)    
            # child.insert(Node(ANY, child))
            node = node.insert(child)
            node = child

        elif token['type'] == 'SEPARATOR':
            # print('here')
            if int(token['value']) == offset:
                node = node.parent
            elif int(token['value']) > offset:
                # print(f"{token['value']} > {offset}")
                node = _make_tree(tokens, node, int(token['value']))
            else: # TODO, other root keys end here
                # print(f"{token['value']} < {offset}")
                off = (offset - int(token['value'])) // INDENT_SIZE
                print('off', off)
                while off:
                    node = node.parent
                    offset -= INDENT_SIZE
                    off -= 1
                node = node.parent
                print(offset)
                print(node.value)
                return node

        elif token['type'] == '[':
            # print('here')
            child = Node(LIST, node)    
            node = node.insert(child)
            node = child
            node = _make_tree(tokens, node, offset)
        
        elif token['type'] == ']':
            while node.value != LIST:
                node = node.parent
            node = node.parent
            return node


        else:
            raise Exception(f'{token["type"]} not implemented')

    return node

def make_tree(tokens) -> Node:
    root = Node('root',)
    print(tokens)
    INDENT_SIZE = list(filter(lambda x: x['type'] == 'SEPARATOR', tokens))
    INDENT_SIZE = INDENT_SIZE[0]['value'] if INDENT_SIZE else 2
    print(INDENT_SIZE)
    # root.parent = root
    res = _make_tree(dummy(tokens), root, 0)
    # print('res', res)
    return root
