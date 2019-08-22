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
Radice:
    y: Int
    array: [
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
    x: Int
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
    type: "added_todo" | "upserted_todo"
    payload:
        todo:
            name: Str

RemovedTodo:
    type: "removed_todo"
    payload:
        ...
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
    Radice: EventA & EventB
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

    Radice: EventA & EventB
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
Radice: EventA & EventB
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
"evento del sistema"
Event:
    x: Int
    b: Ciao

"""
qualcosa
"""
Ciao: Any
'''

with_annotation_in_props = '''
"evento del sistema"
Event:
    """descripzione 1"""
    x: Int
    """descripzione 2"""
    b: [Ciao & Int]

"""
qualcosa
"""
Ciao: Any | Altro
Altro: Int

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

with_comments = '''
"""evento del sistema"""
Event:
    x: Int # un int
    b: Ciao
    pattern: /ciao/ # una regex uau
    patterns: [/cacca/]

Ciao: /eiii/
'''

with_range_int = '''
"""evento del sistema"""
Event:
    x: Int # un int
    range: 0..100
'''

with_range_float_1 = '''
"""evento del sistema"""
Event:
    x: Int # un int
    range: .0..1
'''

with_range_float_2 = '''
"""evento del sistema"""
Event:
    x: Int # un int
    range: 0..1.
'''

with_range_unbounded = '''
"""evento del sistema"""
Event:
    x: Int # un int
    range: 0..
    range1: ..0
'''

splittable_references = '''
Camp:
    oggetto:
        x: Int
        y: Float
    union: A | B
    array: [Float]

A:
    z: Int
B:
    t: Int
'''

splittable_references_and = '''
Camp:
    oggetto:
        x: Int
        y: Float
    union: A & B
    array: [Float]

A:
    z: Int
B:
    t: Int
'''

or_and = '''
R:
    x: Int & Str | Bool
'''

inline_and = '''
"""interface"""
Obj: A &
    a: Str
    b: Int

A:
    x: Int

B:
    y: Int
'''


inline_and_2 = '''
"""interface"""
Obj: A & B &
    a: Str
    b: Int

A:
    x: Int

B:
    y: Int
'''

find_enums = '''
Obj:
    enum: "ciao"

Saluti: "ciao" | "ei"
'''

problematic_comments = '''
Obj:
# sdf
    # 1
    enum: "ciao"

    # ciao
    # coma va
# commenti sannati
Saluti: "ciao" | "ei"

oggett:
    x: Int # sdfsdfdsf
    # dsfsdfsd
    ciao: Str # dsfsdf
    # dsfdsf
'''
trailing_spaces = '''
Obj:
    enum: "ciao" 
Saluti: "ciao" | "ei"

oggett:
    x: Int 
    ciao: Str  
'''
not_empty_1 = '''
Obj:
    not_empty_str: Str!
    array: [
        x: "ciao"
        y: Str!
    ]!

oggett:
    x: Int 
    ciao: Str  
'''
not_empty_2 = '''
Obj:
    not_empty_str: Str!
    array: [Str]!
    enums: ["ciao" | "xx"]!
'''
not_empty_3 = '''
Obj:
    matrix1: [[Str]!]!
    matrix2: [[Str]!]
    matrix3: [[Str]]!
    matrix4: [[Str]]
'''

# failing = """
# ciao: NonEsisto
# """

strings = {x: y for (x, y) in locals().items() if not x[0] == '_'}

# print(list(strings.keys()))