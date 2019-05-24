# skema: schema sdl that compiles to json-schema

## example

```yaml
AddedTodo:
    type: "added_todo"
    payload:
        todo:
            name: Str

RemovedTodo:
    type: "removed_todo"
    payload:
    todo_id: Int

Event: AddedTodo | RemovedTodo
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


