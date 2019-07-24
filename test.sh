# cd ~
X='
AddedTodo:
    type: "added_todo"
    payload:
        todo:
            name: Str
"un field a caso"
RemovedTodo:
    type: "removed_todo" # una costante
    payload:
        id: Str # una stringa
    todo_id: Int

Event: AddedTodo | RemovedTodo
'
echo "$X" | python -m skema