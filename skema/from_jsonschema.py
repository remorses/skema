from dataclasses import dataclass, fields
from .tree import Node
from .constants import *
from typing import Union, List
from .resolve_refs import resolve_refs

@dataclass
class SchemaBlock:
    type: Union[str, List[str]] = None
    items: list = None
    properties: dict = None 
    required: list = None
    anyOf: list = None
    allOf: list = None
    oneOf: list = None
    format: str = None
    @classmethod
    def make(cls, x):
        p = [f.name for f in fields(SchemaBlock)]
        x = {k:v for k, v in x.items() if k in p}
        return cls(**x)

def schema_to_tree(schema: SchemaBlock, node, references=[]):
    """
    type == integer -> node.insert(Node(INT, node))
    type == number -> node.insert(Node(FLOAT, node))
    type == string -> node.insert(Node(STR, node))
    type == array -> Node(LIST, node).insert(schema_to_tree(item, node))
    type == object -> Node(LIST, node).insert(schema_to_tree(item, node))
    type == or -> [OrNode.insert(schema_to_tree(item)) for item in items]
    """
    if schema.type == 'object':
        properties = schema.properties or {}
        if properties:
            for k, v in properties.items() or []:
                v = SchemaBlock.make(v)
                required = k in (schema.required or [])
                child = Node(k, node, required=required)
                child = schema_to_tree(v, child, references)
                node = node.insert(child)
        else:
            child = Node(ANY, node)
            node = node.insert(child)
        
    elif schema.type == 'array':
        subset = v = SchemaBlock.make(schema.items or {})
        child = Node(LIST, node)
        child = schema_to_tree(subset, child, references)
        node = node.insert(child)
        
    elif schema.type == 'string':
        child = Node(STR, node)
        node = node.insert(child)
    elif schema.type == 'integer':
        child = Node(INT, node)
        node = node.insert(child)
    elif schema.type == 'number':
        child = Node(FLOAT, node)
        node = node.insert(child)
    
    elif isinstance(schema.type, list):
        child = Node(OR, node)
        for subset in schema.type:
            if 'type' in subset:
                subset = SchemaBlock.make(subset)
                child = schema_to_tree(subset, child, references)
            elif isinstance(subset, str):
                subset = SchemaBlock(type=subset)
                child = schema_to_tree(subset, child, references)
            else:
                raise NotImplementedError(str(subset))
        node = node.insert(child,)

    elif schema.anyOf or schema.oneOf or schema.allOf:
        child = Node(AND if schema.allOf else OR, node)
        items = schema.oneOf or schema.anyOf or schema.allOf
        i = 0
        for subset in items:
            subset = SchemaBlock.make(subset)
            if subset.type in ['string', 'integer', 'number']:
                child = schema_to_tree(subset, child, references)
            else:
                reference_name = node.value.capitalize() + str(i)
                reference_root = Node(reference_name,)
                reference_root = schema_to_tree(subset, reference_root, references)
                references.append(reference_root)
                child = child.insert(Node(reference_name, child))
                i += 1

        node = node.insert(child,)
        
    else:
        # raise NotImplementedError(str(schema))
        print('!!!NotImplementedError!!!', (str(schema)))
        child = Node(ANY, node)
        node = node.insert(child)
        
    
    return node


def from_jsonschema(schema):
    schema = {**schema}
    resolve_refs(schema)
    schema = SchemaBlock.make(schema)
    references = []
    t = schema_to_tree(schema, node=Node('root'), references=references)
    res = ''
    res += t.to_skema()
    for ref in references:
        res += '\n\n'
        res += ref.to_skema()
    res += '\n'
    return res