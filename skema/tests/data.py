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

union = """
X:
    ciao: Str
    b: Int | Str
    c: "ciao"

B:
    x: Int | null

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
"""

arrays = """
Array: [
    cosa: Int
    object:
        ciao: Str
    another: [
        cose: Str
        altre: Int
    ]
    types: [Type]
]

Type:
    x: Int

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
    payload: ...
    todo_id: Int

Event: AddedTodo | RemovedTodo
"""

real_no_ellipsis = """
Task:
    deadline: Date
    cron: Str
    script: Str
    variables: Str
    results: [
        events: [
            type: Str
            payload: Str
            obj:
                some: Int
                other: Str
        ]
        data: Str
    ]
Date: Str
"""

real_with_ellipsis = """
Task:
    deadline: Date
    cron: Str
    script: Str
    variables: 
        ...
    results: [
        events: [
            type: Str
            payload: Str
            obj:
                some: Int
                other:
                    ...
                ...
        ]
        data: Str
        array: [
            ...
        ]
    ]
Date: Str
"""

with_nulls = """
Data:
    never: Bool | null
    say: "ciao" | null
"""

matrix = """
Data:
    matrix: [[Int]]
    bo: [[Custom]]
Custom:
    ciao: Str
    ...
"""

with_spaces = """
Task:
    deadline: Date
    cron: Str
    script: Str
    variables: 
        ...
    results: [Result]


Result:
    events: [
        type: Str
        payload: Str
        obj:
            some: Int
            other:
                ...
            ...
    ]
    data: Str
    array: [
        ...
    ]

Date: Str
"""

with_optionals = """
Result:
    events?: [
        type: Str
        payload?: Str
        obj?:
            some: Int | null
            other:
                ...
            ...
    ]
    data?: Str
    array: [
        ...
    ]
"""

super_simple = """
req:
    ok: Bool
    bot:
        ...
"""

with_any = """
req:
    ok: Any
    bot:
        ...
"""

indented = """
    Root: EventA & EventB
    EventA:
        type: Str
        fields:
            args: [
                name: Str
                type: Str | Any
            ]
        ...

    EventB:
        timestamp: Int
        sentBy: Str
        madeBy: "me" | "you"
        ...
"""

indented_badly = """

    Root: EventA & EventB
    EventA:
        type: Str
        fields:
            args: [
                name: Str
                type: Str | Any
            ]
        ...


    EventB:
        timestamp: Int
        sentBy: Str
        madeBy: "me" | "you"
        ...
    """

allOf = """
Root: EventA & EventB
EventA:
    type: Str
    fields: Other & Str
EventB:
    timestamp: Int
    sentBy: Str
    madeBy: "me" | "you"
    ...
Other:
    ciao: Int
    Cose: Str
    arr: [
        many: Str
    ]
"""

with_annotation = '''
"""evento del sistema"""
Event:
    x: Int
    b: Ciao

"""
qualcosa
"""
Ciao: Any
'''

with_regex = '''
"""evento del sistema"""
Event:
    x: Int
    b: Ciao
    pattern: /ciao/
    patterns: [/cacca/]

Ciao: /eiii/
'''

# failing = """
# ciao: NonEsisto
# """

strings = {x: y for (x, y) in locals().items() if not x[0] == '_'}

# print(list(strings.keys()))