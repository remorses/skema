# skema: schema sdl that compiles to json-schema

<--- [bump] -->
## last version: 0.0.6
## example

this skema snippet
```yaml
AddedTodo:
    type: "added_todo"
    payload:
        todo:
            name: Str

RemovedTodo:
    type: "removed_todo"
    payload:
        id: Str
    todo_id: Int

Event: AddedTodo | RemovedTodo
```
generates the less readable json schema
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "AddedTodo": {
            "additional_properties": false,
            "type": "object",
            "properties": {
                "type": {
                    "const": "added_todo"
                },
                "payload": {
                    "additional_properties": false,
                    "type": "object",
                    "properties": {
                        "todo": {
                            "additional_properties": false,
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "name"
                            ],
                            "title": "todo"
                        }
                    },
                    "required": [
                        "todo"
                    ],
                    "title": "payload"
                }
            },
            "required": [
                "type",
                "payload"
            ],
            "title": "AddedTodo"
        },
        "RemovedTodo": {
            "additional_properties": false,
            "type": "object",
            "properties": {
                "type": {
                    "const": "removed_todo"
                },
                "payload": {
                    "additional_properties": false,
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "id"
                    ],
                    "title": "payload"
                },
                "todo_id": {
                    "type": "number",
                    "multipleOf": 1.0
                }
            },
            "required": [
                "type",
                "payload",
                "todo_id"
            ],
            "title": "RemovedTodo"
        },
        "Event": {
            "oneOf": [
                {
                    "$ref": "#/definitions/AddedTodo"
                },
                {
                    "$ref": "#/definitions/RemovedTodo"
                }
            ]
        }
    }
}
```
## spec

- all root properties are references and can be used as types
- types can be object whose properties are expressed as key: value or other primitive types like 
    - Str, 
    - Int, 
    - Bool, 
    - Float
- type inside [ ] is an array type
- types can be mixed together: 
    - `Str | Int` means one of string and int
    - `Object1 & Object2` means "all the properties of object 1 and 2"
    - `Object1 | Object2` means "properties of object 1 and not 2 or 2 and not 1"

TODO:
- tests for make_tree
- tests for make_schema
- optional keys
- root key as the main schema
- move extract_ast to tokens instead of a value, so value won't must contain spaces


