import json
from schema.tree import Node

def extract_nodes(text: str):
    if '&' in text:
        parts = text.split('&')
        yield ('and', [x for p in parts for x in tuple(extract_nodes(p.strip()))])
    elif '|' in text:
        parts = text.split('|')
        yield ('or', [x for p in parts for x in tuple(extract_nodes(p.strip()))])
    else:
        yield text


x = next(extract_nodes('ciao & ok | bhu'))
# print(json.dumps(x, indent=4))
print(x)


# def aggregate_op(obj, ):
#     if isinstance(obj, tuple):
#         op, rest = obj
#         if op == root_op:
#             return (op, [rest])

def make_tree(ast, node = Node('root')):
    # children = next(extract_nodes(val))
    if isinstance(ast, tuple):
        op, rest = ast
        print(op, rest)
        child = Node(op)
        node.insert(child)
        # node = child
        for t in rest:
            make_tree(t, child)
    else:
        node.insert(Node(ast))
    return node


tree = make_tree(next(extract_nodes('wow')))
print(tree)