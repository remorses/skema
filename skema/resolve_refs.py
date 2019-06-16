
import json



def _resolve(schema, definitions):
    if not isinstance(schema, dict):
        return
    for k, v in schema.items():
        # print(k)
        if isinstance(v, dict) and '$ref' in list(v.keys()):
            # print('_')
            ref = v['$ref'].split('/')[-1]
            schema[k] = definitions[ref]
        elif isinstance(v, dict):
            _resolve(schema[k], definitions)
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict) and '$ref' in list(item.keys()):
                    # print('_')
                    ref = item['$ref'].split('/')[-1]
                    schema[k][i] = definitions[ref]
                elif isinstance(v, dict):
                    _resolve(schema[k], definitions)

        

            
def resolve_refs(schema):
    definitions = schema['definitions']
    # for definition in definitions: 
    _resolve(schema, definitions)   
    ref = schema['$ref'].split('/')[-1]
    schema.update({**schema, **schema['definitions'][ref]})
    del schema['definitions']
    del schema['$ref']
    return


if __name__ == '__main__':
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$ref": "#/definitions/C",
        "definitions": {
            "X": {
                "title": "X",
                "type": "object",
                "required": [
                    "ciao",
                    "b",
                    "c"
                ],
                "properties": {
                    "ciao": {
                        "type": "string"
                    },
                    "b": {
                        "oneOf": [
                            {
                                "type": "number",
                                "multipleOf": 1.0
                            },
                            {
                                "type": "string"
                            }
                        ]
                    },
                    "c": {
                        "const": "ciao"
                    }
                },
                "additionalProperties": False
            },
            "B": {
                "title": "B",
                "type": "object",
                "required": [
                    "x"
                ],
                "properties": {
                    "x": {
                        "type": "number",
                        "multipleOf": 1.0
                    }
                },
                "additionalProperties": False
            },
            "C": {
                "title": "C",
                "type": "object",
                "required": [
                    "x",
                    "b"
                ],
                "properties": {
                    "x": {
                        "oneOf": [
                            {
                                "$ref": "#/definitions/X"
                            },
                            {
                                "$ref": "#/definitions/B"
                            }
                        ]
                    },
                    "b": {
                        "$ref": "#/definitions/B"
                    }
                },
                "additionalProperties": False
            }
        }
    }

    resolve_refs(schema,)
    print(json.dumps(schema, indent=4))