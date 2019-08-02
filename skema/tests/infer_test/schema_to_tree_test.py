from dataclasses import fields
from skema.infer import SchemaBlock, schema_to_tree, infer_schema
from skema.support import pretty

def test_1():
    x = infer_schema([
        {'a': 3, "cx": '123', 'asd': {'sdfds4': .34, 'dsf': 'asd'}},
        {'a': 3, "cy": '321', 'asd': {'sdfds4': [.34], 'dsf': 8}},
    ])
    pretty(x)
    schema = SchemaBlock.make(x)
    t = schema_to_tree(schema)
    print(t.to_skema())