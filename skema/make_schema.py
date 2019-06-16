

from .tree import Node
from .constants import *


def _make_schema(node, definitions):
    to_skip = [ELLIPSIS]

    if not len(node.children):
        raise Exception(f'missing definition {repr(node.value)} {"after " + repr(node.parent.value) if node.parent else None}')

    elif any([node.children[0].value == x for x in definitions]): # custom definition
        return {
            '$ref': f'#/definitions/{node.children[0].value}'
        }

    elif '"' in node.children[0].value:
        value = node.children[0].value.split('"')
        value = [x.strip() for x in value if x.strip()] or ['']
        value = value[0]
        return {
            'const': value,
        }

    elif node.children[0].value == OR:
        return {
            'oneOf': [_make_schema(Node('_').insert(c), definitions) for c in node.children[0].children]
        }

    elif node.children[0].value == AND:
        return {
            'allOf': [_make_schema(Node('_').insert(c), definitions) for c in node.children[0].children]
        }

    elif node.children[0].value == LIST:
        return {
            'type': 'array',
            'title': node.parent.value,
            'items': _make_schema(node.children[0], definitions)
        }

    elif node.children[0].value == STR:
        return { 'type': 'string' }

    elif node.children[0].value == BOOL:
        return { 'type': 'boolean' }

    elif node.children[0].value == NULL:
        return { 'const': None }

    elif node.children[0].value == FLOAT:
        return { 'type': 'number' }

    elif node.children[0].value == INT:
        return { 'type': 'number', "multipleOf": 1.0 }

    elif node.children[0].value == ELLIPSIS:
        return { 'type': 'object', 'additionalProperties': True }

    else: # object
        ellipses = [ x for x in node.children if x.value == ELLIPSIS ]
        # if any(ellipses):
        #     _type = ellipses[0].children[0] if len(ellipses[0].children) else None # TODO don't know what is this
        return {
            'title': node.value,
            'type': 'object',
            'required': [child.value for child in node.children if child.required and not child.value in to_skip],
            'properties': {
                child.value: _make_schema(child, definitions) for child in node.children if not child.value in to_skip
            },
            'additionalProperties': True if len(ellipses) else False,
            # 'additionalProperties': _make_schema(_type, definitions) if _type else True 
        }



# TODO
def make_schema(root):
    definitions = [ child.value for child in root.children ]
    # print(definitions)
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        '$ref': '#/definitions/' + definitions[0],
        'definitions': {},
    }
    for child in root.children:
        schema['definitions'][child.value] = _make_schema(child, definitions)

    return schema
