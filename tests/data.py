x = """
obj:
    a: Str
    b?: Int
    c: A | B
    z?:
        a: Int
        b: Str
        nn:
            a: Str
            lkk: [
                k: Int
            ]

ll:
    z: Str
    x: [
        x: Int
    ]

A:
    x: Str

B:
    y: Str
    l: [Str]

zzz: A &
    y: Int
    b: Str
    kkkkk: [
        z: Int
        o: [Int]
    ]




"""

x1 = '''
    obj: Str
    """
    ciao
    """
    x:
        y: Str
        z: "Str"
        v: 4
        b: X
        oo:
            a: [Str]
        ll: [
            x: Int
            u: Str
        ]
        x: /xxx/

    z: 0 .. 1
    x: 0 | 1 | 4
    xxx: Name | Str & Int

    zzz: X &
        x: 0 ..

    enum: "s" | "sd"

'''

y = """
obj:
    a: Str
    b?: Int
    c: A | B
    z?:
        a: Int
        b: Str
        nn:
            a: Str
            lkk: [
                k: Int
            ]
ll:
    z: Str
    x: [
        x: Int
    ]
zzz: A &
    y: Int
    b: Str
    kkkkk: [
        z: Int
        o: [Int]
    ]
A:
    x: Str
B:
    y: Str
    l: [Str]
"""

x = '''
obj:
    a: Str
    b?: Int
    c: A | B
    z?:
        a: Int
        b: Str
        nn:
            a: Str
            lkk: [
                k: Int
            ]
ll:
    z: Str
    x: [
        x: Int
    ]

zzz:
    y: Int
    b: Str
    kkkkk: [
        z: Int
        o: [Int]
    ]
'''