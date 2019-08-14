from skema.tree import Node
from skema.from_jsonschema import from_jsonschema, schema_to_tree, from_jsonschema_to_tree
from skema.support import pretty
import skema

def test_1():
    schema = {
        'type': 'object',
        "anyOf": [
            {
                "type": "object",
            },
            {
                "type": "array",
                "items": {
                    "anyOf": [
                        {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "value": {
                                    "type": "string"
                                }
                            },
                            "firstProperty": [
                                "name"
                            ]
                        },
                        {
                            "type": "object",
                            "properties": {
                                "group": {
                                    "type": "string"
                                }
                            },
                            "firstProperty": [
                                "group"
                            ]
                        },
                        {
                            "type": "object",
                            "properties": {
                                "template": {
                                    "type": "string"
                                },
                                "parameters": {
                                    "type": "object",
                                }
                            },
                            "firstProperty": [
                                "template"
                            ]
                        }
                    ]
                }
            }
        ]
    }
    skema.tree.tab = '.   '
    t, refs = from_jsonschema_to_tree(schema, 'X')
    print(t)
    for r in refs:
        print(r)
    x = from_jsonschema(schema)
    print()
    print()
    print()
    print(x)
    x = x.replace('.', ' ')
    
    # pretty(infer_schema(data))
    # pretty(schema)