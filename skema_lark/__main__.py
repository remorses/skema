from .parse import parser
test_tree = """
a:
    c:
        d: Str
        e: Str
    f:
        g: Str
"""

test_tree = '''
x:
    y: Str
    z: Str
    b:
        x: Str
        s:
            z: AnotherType
    obj: Str
    arr: [Str]
    arr2: [
        x: Int
        y: Int
    ]
    string: "ciao"

z:
    ciao: Str

k: Str

ref: Ref

unione: Ref1 | Ref2 | X

and?: Ref1 & Ref2 & X

lista: [
    ciao: "sdf" | "ccc"
]

oggetto?:
    x: Int
    ...

z:
    ...


o:
    rx: /xxx/
# comment

""" # asas
aiii # asd
"""
oggett?:
    x: Str # comm
    y?: Int # sdfsdf
'''

def test():
    t = parser.parse(test_tree)
    print(t.pretty())
    # print(reconstructor.reconstruct(t))

test()
