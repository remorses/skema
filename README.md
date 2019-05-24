# skema: schema sdl that compiles to json-schema

## example

```yaml
AddedTodo:
  type: "added_todo"
  payload: 
    todo:
      name: Str
      data:
        ...
  meta:
    ...

RemovedTodo:
  type: "removed_todo"
  payload:
    todo_id: Int

Event: AddedTodo | RemovedTodo
```

## spec

- types are root properties
- 

TODO:
- tests for make_tree
- tests for make_schema
- optional keys
- root key as the main schema
- move extract_ast to tokens instead of a value, so value won't must contain spaces


