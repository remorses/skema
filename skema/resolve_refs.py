
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
                elif isinstance(item, dict):
                    _resolve(schema[k][i], definitions)
                else:
                    value = json.dumps(v, indent=4)[:400] + "\n"
                    print(f'should not be here, {k}={value}')
        else:
            value = json.dumps(v, indent=4)[:400] + "\n"
            print(f'should not be here, {k}={value}')

        

            
def resolve_refs(schema):
    if not 'definitions' in schema:
        return
    definitions = schema['definitions']
    _resolve(schema, definitions)
    if '$ref' in schema:
        ref = schema['$ref'].split('/')[-1]
        schema.update(schema['definitions'][ref])
        del schema['$ref']
    del schema['definitions']
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