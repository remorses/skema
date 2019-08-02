from dataclasses import fields
from skema.infer import SchemaBlock, infer_schema
from skema.support import pretty
from skema.make_schema import make_schema
from skema.tree import Node
from skema.from_jsonschema import schema_to_tree

def test_1():
    x = infer_schema([
        {'a': 3, "cx": '123', 'asd': {'sdfds4': .34, 'dsf': 'asd'}},
        {'a': 3, "cy": '321', 'asd': {'sdfds4': {'x': [.34], 'y': ''}, 'dsf': 8}},
        # { 'a': [{'b': 3, 'c': 98,}], 'x': 9, 's': {'x': 'asd'}},
        # { 'a': [{'b': '', 'c': 98,}], 'x': 9, 's': {'x': 'asd'}},
        # { 'a': [''], 'x': 9, 's': {'x': 'asd'}}
    ])
    pretty(x)
    schema = SchemaBlock.make(x)
    references = []
    t = schema_to_tree(schema, node=Node('root'), references=references)
    print(t.to_skema())
    for ref in references:
        print(ref.to_skema())
