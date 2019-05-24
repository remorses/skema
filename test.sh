# cd ~
X='
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
'
echo "$X" | python -m skema