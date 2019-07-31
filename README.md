# skema: schema sdl that compiles to json-schema

<!---[bump]--->
## last version: 0.0.29
## example


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
    - /regex/
    - 0..100 (int range)
    - .0..1 (float range)
- type inside [ ] is an array type
- types can be mixed together: 
    - `Str | Int` means one of string and int
    - `Object1 & Object2` means "all the properties of object 1 and 2"
    - `Object1 | Object2` means "properties of object 1 and 2"
- types can be annotated writing annotations inside " or """ quotes
```yaml
"The event type"
Event:
    type: "trigger" | "unknown"
    data:
        ...
    by: User

"""
The annotation will be put in json schema description,
can also be used to write the type to use in fake_data:
:type datetime.datetime
The faker will try tu use this Class
"""
User:
    name: Str
    phone: Int
```

## todo:
- | and & don't work with [], because VAl is split with ARRAY and smaller VAL during tokenization, is hould add a rule during tokenization to exclude | and & in array tokens and add array logic inside VAL handling
- the same for regex
- better handling of comments and white space
- dynamic indentation (now is set as 4 spaces)




bugs:
- if key name is equal to another type name then fuck it up
- can't write `key: [Str] | Int`
- objects get additionalProps: true by default even if they haven't ... at the end like:
```
Object:
    a: Str
    b: Int
    ...
```
this is because i always forget to put them when doing `Object1 & Object2` so i just removed it