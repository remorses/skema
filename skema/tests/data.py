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

B:
    x: Int

C:
    x: X | B
    b: Int

    
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

Array: [
    cosa: Int
    object:
        ciao: Str
]

"""


events = """
A:
    x: "Int"
    payload:
        cosa: Int

B:
    x:
        ciao: Str
"""
# problem = """
# AddedTodo:
#     type: "added_todo"
#     payload:
#         todo:
#             name: Str
# RemovedTodo:
#     type: "removed_todo"
#     payload:
#         todo_id: Int

# Event: AddedTodo | RemovedTodo
# """

with_lines = """
Bot:
    username: "ciao"

Url: Str

Cosa:
    a: Str
    b: Str

"""

problematic = """
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
"""

strings = {x: y for (x, y) in locals().items() if not x[0] == '_'}

# print(list(strings.keys()))