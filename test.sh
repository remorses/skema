# cd ~
X='
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
'
echo "$X" | python -m skema