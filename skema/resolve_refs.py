from copy import deepcopy
import json


def recursive_resolve(schema, definitions, add_titles):
    if not isinstance(schema, dict):
        return
    for k, v in schema.items():
        # print(k)
        if isinstance(v, dict) and '$ref' in list(v.keys()):
            # print('_')
            ref = v['$ref'].split('/')[-1]
            schema[k] = definitions[ref]
            if add_titles:
                schema[k].update({'title': ref})
        elif isinstance(v, dict):
            recursive_resolve(schema[k], definitions, add_titles)
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict) and 'const' in list(item.keys()):
                    if add_titles:
                        item.update({'title': item['const']})
                if isinstance(item, dict) and '$ref' in list(item.keys()):
                    # print('_')
                    ref = item['$ref'].split('/')[-1]
                    if add_titles:
                        definitions[ref].update({'title': ref})
                    schema[k][i] = definitions[ref]
                elif isinstance(item, dict):
                    recursive_resolve(schema[k][i], definitions, add_titles)
                else:
                    value = json.dumps(v, indent=4)[:400] + "\n"
                    # print(f'should not be here, {k}={value}')
        else:
            value = json.dumps(v, indent=4)[:400] + "\n"
            # print(f'should not be here, {k}={value}')


def resolve_refs(schema, ref=None, add_titles=True):
    if not 'definitions' in schema:
        return
    definitions = schema['definitions']
    if ref:
        schema["$ref"] = "#/definitions/" + ref
    recursive_resolve(schema, definitions, add_titles)
    if '$ref' in schema:
        ref = schema['$ref'].split('/')[-1]
        schema.update(schema['definitions'][ref])
        if add_titles:
            schema.update({'title': ref})
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
    # print(json.dumps(schema, indent=4))