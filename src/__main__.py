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

range: 0 .. 20
range: 0. .. 1.6
range: .. 1.6
range: .. 6
num: 3

interfaced: XXX &
    num: 9


obj:
    prop1: Str
    bca: Int

'''


def test():
    t = parser.parse(test_tree)
    print(t.pretty())
    # print(reconstructor.reconstruct(t))


test()
