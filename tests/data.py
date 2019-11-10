
simplest = '''

Shape:
    name: Str
    other: Enum

Enum: "dfgj" | "dsf" | "a4543"

'''

simple = """
Unioned: A | B

A:
    c: Str

B:
    d: Str

X:
    ciao: Str
    b: Unioned
    c: "ciao"
    inline: A | B
"""

middle = '''
Event: A | B | C

A:
    name: Str
    type: "a1a" | "a2a" | "a3a"

B:
    title: Str
    tags: [
        code: Str
    ]

C:
    code: Scalar
    coordinates: [
        x: Float
        y: Float
    ]

Scalar: Str
'''

with_intersection = '''
Elem1:
    name: Str

Elem2:
    surname: Str

Elem3:
    address: Str
    name: Int

Group: Elem1 & Elem2 & Elem3
'''

with_intersection_inline = '''
Base:
    name: Str

Elem2: Base &
    surname: Str

Elem3: Base &
    address: Str
    name: Int
'''

annotations = '''
"""
root annotation
"""
Cosa:
    nest:
        """
        field annotation
        """
        puppets: [
            name: Str
            type: "dog" | "cat"
        ]
        """
        ciao
        """
        position: Int
'''

comments = ''' # TODO commentsa not work
Cosa:
    nest:
        puppets: [
            name: Str
            type: "dog" | "cat"
        ]
        position: Int
'''

example = '''
unions3: Bot | User

User:
    x: Int
    y: Int
    unions3: unions2
    ...
Bot:
    settings?:
        x: Int
        y: Str
        obj:
            ciao: Str
    name?: Str
    unioned?: "dsfg" | "dfg"
    unions?: ["dsfg" | "dfg"]
    lista?: [
        x: Str
        y: Int
    ]
    x?: unions2

unions2: ["dsfg" | "dfg"]
'''
ellipsis = '''
Bot:
    settings?:
        x: Int
        y: Str
        obj:
            ciao: Str
        ...
    name?: Str
'''
# indent2 = """
# X:
#     ciao: Str
#     b: Int | Str
#     c: "ciao"
# B:
#     x: Int
# C:
#     c: Str
# """

# union = """
# X:
#     ciao: Str
#     b: Int | Str
#     c: "ciao"
# B:
#     x: Int | null
# C:
#     x: X | B
#     b: Int
    
# """



# complex_schema = """
# Bot:
#     username: "ciao"
#     data:
#         competitors: [Str]
#     dependencies: [Url]
# Url: Str
# Cosa:
#     a: Str
#     b: Str
#     c: Int
#     d:
#         cosa: Cosa
#         a: Int
#         b: Int
# """

# arrays = """
# Radice:
#     y: Int
#     array: [
#         cosa: Int
#         object:
#             ciao: Str
#         another: [
#             cose: Str
#             altre: Int
#         ]
#         types: [Type]
#     ]
# Type:
#     x: Int
# """


# events = """
# A:
#     x: Int
#     payload:
#         cosa: Int
# B:
#     x:
#         ciao: Str
# """


# with_lines = """
# Bot:
#     username: "ciao"
# Url: Str
# Cosa:
#     a: Str
#     b: Str
# """

# problematic = """
# AddedTodo:
#     type: "added_todo" | "upserted_todo"
#     payload:
#         todo:
#             name: Str
# RemovedTodo:
#     type: "removed_todo"
#     payload:
#         ...
#     todo_id: Int
# Event: AddedTodo | RemovedTodo
# """

# real_no_ellipsis = """
# Task:
#     deadline: Date
#     cron: Str
#     script: Str
#     variables: Str
#     results: [
#         events: [
#             type: Str
#             payload: Str
#             obj:
#                 some: Int
#                 other: Str
#         ]
#         data: Str
#     ]
# Date: Str
# """

# real_with_ellipsis = """
# Task:
#     deadline: Date
#     cron: Str
#     script: Str
#     variables: 
#         ...
#     results: [
#         events: [
#             type: Str
#             payload: Str
#             obj:
#                 some: Int
#                 other:
#                     ...
#                 ...
#         ]
#         data: Str
#         array: [
#             ...
#         ]
#     ]
# Date: Str
# """

# with_nulls = """
# Data:
#     never: Bool | null
#     say: "ciao" | null
# """

# matrix = """
# Data:
#     matrix: [[Int]]
#     bo: [[Custom]]
# Custom:
#     ciao: Str
#     ...
# """

# with_spaces = """
# Task:
#     deadline: Date
#     cron: Str
#     script: Str
#     variables: 
#         ...
#     results: [Result]
# Result:
#     events: [
#         type: Str
#         payload: Str
#         obj:
#             some: Int
#             other:
#                 ...
#             ...
#     ]
#     data: Str
#     array: [
#         ...
#     ]
# Date: Str
# """

# with_optionals = """
# Result:
#     events?: [
#         type: Str
#         payload?: Str
#         obj?:
#             some: Int | null
#             other:
#                 ...
#             ...
#     ]
#     data?: Str
#     array: [
#         ...
#     ]
# """

# base_indented = """
#     Radice: EventA & EventB
#     EventA:
#         type: Str
#         fields:
#             args: [
#                 name: Str
#                 type: Str | Any
#             ]
#         ...
#     EventB:
#         timestamp: Int
#         sentBy: Str
#         madeBy: "me" | "you"
#         ...
# """

# indented_badly = """
#     Radice: EventA & EventB
#     EventA:
#         type: Str
#         fields:
#             args: [
#                 name: Str
#                 type: Str | Any
#             ]
#         ...
#     EventB:
#         timestamp: Int
#         sentBy: Str
#         madeBy: "me" | "you"
#         ...
#     """

# allOf = """
# Radice: EventA & EventB
# EventA:
#     type: Str
#     fields: Other & Str
# EventB:
#     timestamp: Int
#     sentBy: Str
#     madeBy: "me" | "you"
#     ...
# Other:
#     ciao: Int
#     Cose: Str
#     arr: [
#         many: Str
#     ]
# """

# failing = """Ò
# ciao: NonEsisto
# """

strings = [(x, y) for (x, y) in locals().items() if not x[0] == '_']
names = [f'0{i}{x}' for i, (x, _) in enumerate(strings)]
schemas = [x for _, x in strings]

# print(list(strings.keys()))