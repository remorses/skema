import poyo
from functools import reduce


import json
class Node:
    def __init__(self, value, parent=None):
        # self.key = key
        self.value = value
        self.children = []
        self.parent = parent
    
    def insert(self, *nodes):
        [self.children.append(n) for n in nodes]
        return self
    
    def __repr__(self, indent=''):
        res = (indent + str(self.value))
        res += ':' if len(self.children) else ''
        for c in self.children:
            res += '\n' + Node.__repr__(c, indent + '\t')
        return res



def make_tree(obj, key='root'):
    node = Node(key)
    for k, val in obj.items(): # properties
        if isinstance(val, dict): # is_object
            node.insert(make_tree(val, k))
        else:
            node.insert(Node(k,).insert(Node(val,)))
    return node









a = Node("1")
a \
    .insert(Node("2").insert(Node("2",))) \
    .insert(Node("3") \
        .insert(Node("4")
            .insert(Node("5").insert(Node("2",)))
        )
    ) \
    .insert(Node("6").insert(Node("2",)))

b = Node(1).insert(
        Node('&').insert(
            Node(2),
            Node(3)
        )
    )


t = make_tree({
    'a': 1,
    'b': 2,
    'e': 1,
    'f': 2,
    'c': {
        'a': {
            'a': 1,
            'b': 2,
        },
        'b': 2,
    }
})



"""
two:
  three: 3
  arr: [
    a: 1
    b: 2
    ...
  ]
four: 4
arr: [Str]


[
    {
        "SEPARATOR": 0
    },
    {
        "KEY": "two"
    },
    {
        "SEPARATOR": 2
    },
    {
        "KEY": "three"
    },
    {
        "VAL": "3"
    },
    {
        "SEPARATOR": 2
    },
    {
        "KEY": "arr"
    },
    {
        "[": "["
    },
    {
        "SEPARATOR": 4
    },
    {
        "KEY": "a"
    },
    {
        "VAL": "1"
    },
    {
        "SEPARATOR": 4
    },
    {
        "KEY": "b"
    },
    {
        "VAL": "2"
    },
    {
        "SEPARATOR": 4
    },
    {
        "ADDITIONAL_PROPERTIES": "..."
    },
    {
        "SEPARATOR": 2
    },
    {
        "]": "]"
    },
    {
        "SEPARATOR": 0
    },
    {
        "KEY": "four"
    },
    {
        "VAL": "4"
    },
    {
        "SEPARATOR": 0
    },
    {
        "KEY": "arr"
    },
    {
        "[": "["
    },
    {
        "VAL": "Str"
    },
    {
        "]": "]"
    },
    {
        "SEPARATOR": 0
    }
]


"""

def dummy(iter):
    yield from iter

LIST = '__LIST'
AND = '__AND'
OR = '__OR'
ANY = 'Any'
INT = 'Int'
STR = 'Str'
FLOAT = 'Float'
MORE = '...'
INDENT_SIZE = 2

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
            child = Node(token['value'], node)    
            node = node.insert(child)
            # node = child

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

        # elif token['type'] == '&':
        #     # print('here')
        #     child = Node(AND, node)
        #     child.insert(*node.parent.children)  
        #     node.parent.children = []
        #     node = node.parent.insert(child)
        #     node = child
        #     # node = _make_tree(tokens, node, offset)

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

def make(tokens):
    root = Node('root',)
    # root.parent = root
    res = _make_tree(dummy(tokens), root, 0)
    # print('res', res)
    return root





class dotdict(dict):
    __getattribute__ = dict.__getitem__
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setattr__






def make_schema(node, definitions):
    to_skip = [MORE]

    if not len(node.children):
        raise Exception(f'missing definition {node.value}')

    if any([node.children[0].value == x for x in definitions]): # custom definition
        return {
            '$ref': f'#/definitions/{node.children[0].value}'
        }

    if node.children[0].value == LIST:
        return {
            'type': 'array',
            'title': node.parent.value,
            'items': make_schema(node.children[0], definitions)
        }

    elif node.children[0].value == STR:
        return { 'type': 'string' }

    elif node.children[0].value == FLOAT:
        return { 'type': 'number' }

    elif node.children[0].value == INT:
        return { 'type': 'number', "multipleOf": 1.0 }

    elif node.children[0].value == MORE:
        return {}

    else: # object
        ellipses = [ x for x in node.children if x.value == MORE ]
        if any(ellipses):
            _type = ellipses[0].children[0] if len(ellipses[0].children) else None
            return {
                'additional_properties': make_schema(_type, definitions) if _type else True,
                'type': 'object',
                'properties': {
                    child.value: make_schema(child, definitions) for child in node.children if not child.value in to_skip
                },
                'title': node.value,
            }
        else:
            return {
                'additional_properties': False,
                'type': 'object',
                'properties': {
                    child.value: make_schema(child, definitions) for child in node.children if not child.value in to_skip
                },
                'required': [child.value for child in node.children],
                'title': node.value,
            }


# TODO
def root_schema(root):
    definitions = [ child.value for child in root.children ]
    print(definitions)
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        'definitions': {},
    }
    for child in root.children:
        schema['definitions'][child.value] = make_schema(child, definitions)

    return schema

test_schema = """
Bot:
    username: Str
    data:
        competitors: [Str]
    dependencies: [Url]
Url: Str

"""

if __name__ == "__main__":
    INDENT_SIZE = 4
    from test import tokenize
    tokens = tokenize(test_schema)
    # print([t for t in tokens if t['value'] == 'Cosa'])
    # print(json.dumps(tokens, indent=4))
    tree = make(tokens)
    print(tree)
    print()
    print(json.dumps(root_schema(tree), indent=4))

