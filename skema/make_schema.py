
from functools import reduce
from .tree import Node, get_annotation
from .constants import *


def _make_schema(node, definitions, root):
    to_skip = [ELLIPSIS]

    if not len(node.children):
        raise Exception(f'missing definition {repr(node.value)} {"after " + repr(node.parent.value) if node.parent else None}')

    elif any([node.children[0].value == x for x in definitions]): # custom definition
        return {
            '$ref': f'#/definitions/{node.children[0].value}',
            'title': get_title(node),
            'description': get_annotation(node),
        }
    elif node.children[0].value == ELLIPSIS:
        return { 
            'type': 'object', 
            'additionalProperties': True, 
            'title': get_title(node), 
            'description': get_annotation(node),
        }

    elif '..' in node.children[0].value:
        return make_range_schema(node)

    elif '"' in node.children[0].value:
        value = node.children[0].value.split('"')
        value = [x.strip() for x in value if x.strip()] or ['']
        value = value[0]
        return {
            'enum': [value],
            'type': 'string',
            'title': get_title(node),
            'description': get_annotation(node),
        }

    elif node.children[0].value == OR:
        if all(['"' in node.value for node in node.children[0].children]):
            return {
                'enum': [c.value.replace('"', '', 2) for c in node.children[0].children],
                'type': 'string',
                'title': get_title(node),
                'description': get_annotation(node),
            }
        elif all([node.value.isdigit() for node in node.children[0].children]):
            return {
                'enum': [int(c.value) for c in node.children[0].children],
                'type': 'number',
                'title': get_title(node),
                'multipleOf': 1,
                'description': get_annotation(node),
            }
        else:
            return {
                'anyOf': [_make_schema(Node('').insert(c), definitions, root) for c in node.children[0].children],
                'description': get_annotation(node),
            }

    elif node.children[0].value == AND:
        if (len(node.children) > 1): # inline and, interface
            options = []
            options += [_make_schema(Node('').insert(c), definitions, root) for c in node.children[0].children]
            interface_keys = reduce(lambda a, b: [*a, *get_properties(b, root)], options, [])
            children = [c for c in node.children if c.value != AND and c.value not in interface_keys]
            if children:
                inline_props = Node('',).insert(*children)
                options += [_make_schema(inline_props, definitions, root)]
            return {
                'type': 'object',
                'allOf': options,
                'description': get_annotation(node),
            }
        else:
            options = [_make_schema(Node('').insert(c), definitions, root) for c in node.children[0].children]
            return {
                'allOf': options,
                'description': get_annotation(node),
            }

    elif node.children[0].value == LIST:
        return {
            'type': 'array',
            'title': get_title(node),
            'items': _make_schema(Node(node.value, node.parent,).append(node.children[0].children), definitions, root),
            # 'description': get_annotation(node),
        }

    elif node.children[0].value == STR or node.children[0].value == STRING:
        obj = { 
            'type': 'string', 
            'title': get_title(node), 
            'description': get_annotation(node),
        }
        format = get_format(node.value)
        if format:
            obj.update({
                'format': format,
            })
        return obj

    elif node.children[0].value == REGEX:
        return { 
            'type': 'string', 
            'pattern': node.children[0].pattern, 
            'title': get_title(node), 
            'description': get_annotation(node),
        }

    elif node.children[0].value == ANY:
        return { 
            'title': get_title(node),
            'description': get_annotation(node), 
        }

    elif node.children[0].value == BOOL:
        return { 
            'type': 'boolean', 
            'title': get_title(node),
            'description': get_annotation(node),
        }

    elif node.children[0].value == NULL:
        return { 'const': None }

    elif node.children[0].value == FLOAT:
        return { 
            'type': 'number', 
            'title': get_title(node), 
            'description': get_annotation(node),
        }

    elif node.children[0].value == INT:
        return { 
            'type': 'number',
            "multipleOf": 1.0,
            'title': get_title(node),
            'description': get_annotation(node),
        }
    else: # object
        ellipses = [ x for x in node.children if x.value == ELLIPSIS ]
        # if any(ellipses):
        #     _type = ellipses[0].children[0] if len(ellipses[0].children) else None # TODO don't know what is this
        obj = {
            'title': get_title(node),
            'description': get_annotation(node),
            'type': 'object',
            'required': [child.value for child in node.children if child.required and not child.value in to_skip],
            'properties': {
                child.value: _make_schema(child, definitions, root) for child in node.children if not child.value in to_skip
            },
            # 'additionalProperties': _make_schema(_type, definitions) if _type else True 
        }
        if len(ellipses):
            obj.update({'additionalProperties': True,})
        return obj

def get_title(node):
    return node.value if node.value not in [LIST, OR, AND, REGEX,] else ''


# TODO
def make_schema(root):
    definitions = [child.value for child in root.children]
    # print(definitions)
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        '$ref': '#/definitions/' + definitions[0],
        'definitions': {},
    }
    for child in root.children:
        schema['definitions'][child.value] = _make_schema(child, definitions, root)

    return schema


def get_format(name):
    if name == 'DateTime':
        return 'date-time'
    if name == 'Date':
        return 'date'
    if name == 'Time':
        return 'time'
    if name == 'Email':
        return 'email'
    if name == 'Uri':
        return 'uri'
    if name == 'Iri':
        return 'iri'
    return None

def make_range_schema(node):
    value = node.children[0].value
    boundaries = value.split('..')
    boundaries = [b.strip() for b in boundaries]
    boundaries = [b for b in boundaries if b]
    obj = {
        'title': get_title(node),
        'type': 'number',
        'description': get_annotation(node),
    }
    if all([s.isdigit() for s in boundaries]):
        obj.update({
            'multipleOf': 1,
        })
        boundaries = [int(b) for b in boundaries]
    else:
        boundaries = [float(b) for b in boundaries]
    if len(boundaries) == 0:
        raise Exception('range must contain at least one bounding: 0.. ..100 0..100')
    elif len(boundaries) <= 1:
        if value.index('..') == 0:
            obj.update({
                'type': 'number',
                'exclusiveMaximum': boundaries[0],
            })
        else:
            obj.update({
                'type': 'number',
                'minimum': boundaries[0],
            })
    else:
        obj.update({
            'type': 'number',
            'minimum': boundaries[0],
            'exclusiveMaximum': boundaries[1],
        })
    return obj


def get_properties(block: dict, root: Node):
    if block.get('properties', {}):
        return block['properties']
    elif block.get('$ref', ''):
        ref_name = block.get('$ref', '').split('/')[-1]
        node = [n for n in root.children if n.value == ref_name][0]
        # print(node.children)
        return [c.value for c in node.children if c.value not in [OR, AND, LIST,]]
    else:
        raise Exception(f'cannot get properties from {block}')