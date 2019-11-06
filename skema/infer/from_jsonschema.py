# import json
# from funcy import distinct
# from dataclasses import dataclass, fields

# from ..constants import *
# from ..support import capitalize
# from typing import Union, List
# from ..resolve_refs import resolve_refs

# @dataclass
# class SchemaBlock:
#     previous_key: str = ''
#     data: str = ''
#     type: Union[str, List[str]] = None
#     items: list = None
#     properties: dict = None 
#     required: list = None
#     anyOf: list = None
#     enum: list = None
#     allOf: list = None
#     oneOf: list = None
#     format: str = None
#     @classmethod
#     def make(cls, data, previous_key=''):            
#         p = [f.name for f in fields(SchemaBlock)]
#         x = {k:v for k, v in data.items() if k in p}
#         return cls(**x, data=json.dumps(data, indent=4), previous_key=previous_key)

# def schema_to_tree(schema: SchemaBlock, node, references=[]):
#     """
#     type == integer -> node.insert(Node(INT, node))
#     type == number -> node.insert(Node(FLOAT, node))
#     type == string -> node.insert(Node(STR, node))
#     type == array -> Node(LIST, node).insert(schema_to_tree(item, node))
#     type == object -> Node(LIST, node).insert(schema_to_tree(item, node))
#     type == or -> [OrNode.insert(schema_to_tree(item)) for item in items]
#     """
#     if False:
#         pass
#     elif schema.anyOf or schema.oneOf or schema.allOf or schema.enum:
#         child = Node(AND if schema.allOf else OR, node)
#         items = schema.oneOf or schema.anyOf or schema.allOf or schema.enum
#         items = distinct(items, key=get_type_name)
#         i = 0
#         for subset in items:
#             if isinstance(subset, str):
#                 subset = SchemaBlock(type=subset,)
#             else:
#                 subset = SchemaBlock.make(subset,)
#             if subset.type in ['string', 'integer', 'number', 'boolean', 'null']:
#                 child = schema_to_tree(subset, child, references)
#             else:
#                 if all([node.value != x for x in (LIST, OR, AND)]):
#                     reference_name = capitalize(node.value) + str(i)
#                 else:
#                     reference_name = capitalize(node.parent.value) + 'Elem' + str(i)
#                 reference_root = Node(reference_name, child)
#                 reference_root = schema_to_tree(subset, reference_root, references)
#                 references.append(reference_root)
#                 child = child.insert(Node(reference_name, child))
#                 i += 1
#         node = node.insert(child,)
#     elif schema.type == 'object':
#         properties = schema.properties or {}
#         if properties:
#             for k, v in properties.items() or []:
#                 v = SchemaBlock.make(v, previous_key=k)
#                 required = k in (schema.required or [])
#                 child = Node(k, node, required=required)
#                 child = schema_to_tree(v, child, references)
#                 node = node.insert(child)
#         else:
#             child = Node(ANY, node)
#             node = node.insert(child)
        
#     elif schema.type == 'array':
#         subset = v = SchemaBlock.make(schema.items or {})
#         child = Node(LIST, node)
#         child = schema_to_tree(subset, child, references)
#         node = node.insert(child)
        
#     elif schema.type == 'string':
#         child = Node(STR, node)
#         node = node.insert(child)
#     elif schema.type == 'integer':
#         child = Node(INT, node)
#         node = node.insert(child)
#     elif schema.type == 'number':
#         child = Node(FLOAT, node)
#         node = node.insert(child)
#     elif schema.type == 'boolean':
#         child = Node(BOOL, node)
#         node = node.insert(child)
    
#     elif isinstance(schema.type, list):
#         child = Node(OR, node)
#         items = distinct(schema.type, key=get_type_name)
#         for subset in items:
#             if 'type' in subset:
#                 subset = SchemaBlock.make(subset)
#                 child = schema_to_tree(subset, child, references)
#             elif isinstance(subset, str):
#                 subset = SchemaBlock(type=subset)
#                 child = schema_to_tree(subset, child, references)
#             else:
#                 raise NotImplementedError(str(subset))
#         node = node.insert(child,)
#     else:
#         # raise NotImplementedError(str(schema))
#         # print('!!!NotImplementedError!!!', schema.previous_key)
#         # print(str(schema))
#         child = Node(ANY, node)
#         node = node.insert(child)
#     return node


# def get_type_name(schema):
#     if isinstance(schema, str):
#         return 'string'
#     if isinstance(schema, dict):
#         if 'type' in schema:
#             if schema['type'] == 'object':
#                 return str(schema)
#             return schema['type']
#     if any([x in schema for x in ('anyOf', 'allOf', 'enum', 'oneOf',)]):
#         return str(schema)
#     return 'any'



# def from_jsonschema_to_tree(schema, ref_name=None, ):
#     references: list = []
#     schema = {**schema}
#     resolve_refs(schema, add_titles=True)
#     # print(json.dumps(schema, indent=4))
#     root_name = schema.get('title') or ref_name or 'Root'
#     root_name = root_name.replace('_', ' ')
#     root_name = ''.join([capitalize(x) for x in root_name.split(' ')])
#     schema = SchemaBlock.make(schema)
#     t = schema_to_tree(schema, node=Node(root_name), references=references)
#     return t, references

# def from_jsonschema(schema, ref_name=None):
#     t, references = from_jsonschema_to_tree(schema, ref_name)
#     res = ''
#     res += t.to_skema()
#     for ref in references:
#         res += '\n\n'
#         res += ref.to_skema()
#     res += '\n'
#     return res