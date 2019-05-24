# from support import dotdict as _dotdict

simple = """
X:
    ciao: Str
    b: Int | Str
    c: "ciao"
"""

indent2 = """
X:
    ciao: Str
    b: Int | Str
    c: "ciao"
    ...

B:
    x: Int

C:
    c: Str
"""

reference_union = """
X:
    ciao: Str
    b: Int | Str
    c: "ciao"
    ...

B:
    x: Int

C:
    x: X | B
    b:
        c:
            ...
    
"""

tricky = """
AddedTodo:
  type: "added_todo"
  payload: 
    todo:
      name: Str
      data:
        ...
  meta:
    ...
"""


events = """
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
"""

complex_schema = """
Bot:
    username: "ciao"
    data:
        competitors: [Str]
    dependencies: [Url]
Url: Str
Cosa:
    a: Str
    b: Str
    c: Int
    d:
        cosa: Cosa
        a: Int
        b: Int

"""
with_lines = """
Bot:
    username: "ciao"

Url: Str

Cosa:
    a: Str
    b: Str

"""

strings = {x: y for (x, y) in locals().items() if not x[0] == '_'}

# print(list(strings.keys()))