

from .tree import Node
from .constants import *


def _make_schema(node, definitions):
    to_skip = [ELLIPSIS]

    if not len(node.children):
        raise Exception(f'missing definition {repr(node.value)} {"after " + repr(node.parent.value) if node.parent else None}')

    elif any([node.children[0].value == x for x in definitions]): # custom definition
        return {
            '$ref': f'#/definitions/{node.children[0].value}',
            'description': get_annotation(node),
        }
    elif node.children[0].value == ELLIPSIS:
        return { 'type': 'object', 'additionalProperties': True, 'title': node.value, 'description': get_annotation(node),}

    elif '..' in node.children[0].value:
        return make_range_schema(node)

    elif '"' in node.children[0].value:
        value = node.children[0].value.split('"')
        value = [x.strip() for x in value if x.strip()] or ['']
        value = value[0]
        return {
            'enum': [value],
            'title': node.value,
            'description': get_annotation(node),
        }

    elif node.children[0].value == OR:
        if all(['"' in node.value for node in node.children[0].children]):
            return {
                'enum': [c.value.replace('"', '', 2) for c in node.children[0].children],
                'description': get_annotation(node),
            }
        elif all([node.value.isdigit() for node in node.children[0].children]):
            return {
                'enum': [int(c.value) for c in node.children[0].children],
                'description': get_annotation(node),
            }
        else:
            return {
                'anyOf': [_make_schema(Node('').insert(c), definitions) for c in node.children[0].children],
                'description': get_annotation(node),
            }

    elif node.children[0].value == AND:
        options = [_make_schema(Node('').insert(c), definitions) for c in node.children[0].children]
        # strip = lambda opt: {**opt,'additionalProperties':True} if (isinstance(opt, dict) and not opt.get('additionalProperties', True)) else opt
        # options = [strip(opt) for opt in options]
        return {
            'allOf': options,
            'description': get_annotation(node),
        }

    elif node.children[0].value == LIST:
        return {
            'type': 'array',
            # 'title': node.value,
            'items': _make_schema(node.children[0], definitions),
            'description': get_annotation(node),
        }

    elif node.children[0].value == STR or node.children[0].value == STRING:
        obj = { 'type': 'string', 'title': node.value, 'description': get_annotation(node),}
        format = get_format(node.value)
        if format:
            obj.update({
                'format': format,
            })
        return obj

    elif node.children[0].value == REGEX:
        return { 'type': 'string', 'pattern': node.children[0].pattern, 'title': node.value, 'description': get_annotation(node),}

    elif node.children[0].value == ANY:
        return { 'title': node.value, 'description': get_annotation(node), }

    elif node.children[0].value == BOOL:
        return { 'type': 'boolean', 'title': node.value, 'description': get_annotation(node),}

    elif node.children[0].value == NULL:
        return { 'const': None }

    elif node.children[0].value == FLOAT:
        return { 'type': 'number', 'title': node.value, 'description': get_annotation(node),}

    elif node.children[0].value == INT:
        return { 'type': 'number', "multipleOf": 1.0, 'title': node.value, 'description': get_annotation(node),}


    else: # object
        ellipses = [ x for x in node.children if x.value == ELLIPSIS ]
        # if any(ellipses):
        #     _type = ellipses[0].children[0] if len(ellipses[0].children) else None # TODO don't know what is this
        obj = {
            'title': node.value,
            'description': get_annotation(node),
            'type': 'object',
            'required': [child.value for child in node.children if child.required and not child.value in to_skip],
            'properties': {
                child.value: _make_schema(child, definitions) for child in node.children if not child.value in to_skip
            },
            # 'additionalProperties': _make_schema(_type, definitions) if _type else True 
        }
        if len(ellipses):
            obj.update({'additionalProperties': True,})
        return obj


def get_annotation(node):
    if node.parent:
        annotations = node.parent.child_annotations
        return annotations.pop(0) if len(annotations) else ''
    else:
        # print(f'{node.value} has no parent')
        return ''

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
        'title': node.value,
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